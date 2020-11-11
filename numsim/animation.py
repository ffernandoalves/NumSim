import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

from itertools import chain

DT = 0.015
COLOR_OBJ = [np.array([np.nan] * 3)] #armazena as cores de cada corpo celeste para evitar repetição de cores.

def join_mat_funcs(*funcs):
    return lambda *args: tuple(chain.from_iterable(f(*args) for f in funcs))

class ObjectProperties: # or Attributes
    """
    Object Properties (OP)
    """
    def __init__(self, **entries):
        self.__dict__.update(entries)

def choose_color():
    color = np.random.rand(3)
    comparison = color == COLOR_OBJ
    if comparison.any():
        choose_color()
    COLOR_OBJ.append(color)
    return color

class AnimateSimulation:
    """
    Animate Simulation (AN)
    """
    def __init__(self, s_obj, ax):
        """
        + s_obj - object to simulate
        """
        self.x, self.y = s_obj.x0, s_obj.x1
        self.saveImg = s_obj.saveImg
        self.ax = ax
        #self.ax.grid()
                
        #color = np.random.rand(3)
        color = choose_color()
         
        self.obj_repr, = self.ax.plot([], [], 'o-', color=color, label=s_obj.name, lw=1) #object representation
        self.obj_repr_trail, = self.ax.plot([], [], color=color, lw=0.5)
        self.leg = plt.legend()
        self.leg_lines = self.leg.get_lines()
        self.leg_texts = self.leg.get_texts()
        plt.setp(self.leg_lines, linewidth=4)
        plt.setp(self.leg_texts, fontsize='x-large')
        self.time_template = 'Time = %.2fs'
        self.time_text = self.ax.text(0.05, 0.9, '', transform=self.ax.transAxes)

    def init(self):
        self.obj_repr.set_data([self.x[0]], [self.y[0]])
        self.obj_repr_trail.set_data([], [])
        self.time_text.set_text("")
        return self.obj_repr, self.obj_repr_trail, self.time_text,

    def animate(self, i):
        self.obj_repr.set_data(self.x[i], self.y[i])
        self.obj_repr_trail.set_data(self.x[:i], self.y[:i])
        self.time_text.set_text(self.time_template % (i * DT))

        #if self.saveImg:
        #    if i == len(self.x) - 1:
        #        salve(None, saveAnim=False, saveImg=self.saveImg)
        return self.obj_repr, self.obj_repr_trail, self.time_text,


class SimulationComponentsGenerator:
    """
    Simulation Components Generator (SCG)
    """
    def __init__(self, data_frame, ax, saveImg=None):
        self.data_frame = data_frame
        self.delta_t = self.data_frame["delta_t"][0]
        self.ax = ax
        self.saveImg = saveImg

        self.N = int(self.data_frame["N"][0])
        self.time = self.data_frame["time"]

        self.l_OP = []              # list of the ObjectProperties objects that will be part of the simulation
        self._data_to_OP_object()
        self.l_AN = []              # list of the AnimateSimulation objects that will be part of the simulation
        self.store_animate = []     # list of methods "animate" of the AnimateSimulation objects
        self.store_init = []        # list of methods "init" of the AnimateSimulation objects

        self.TAM_SHAPE = len(self.l_OP[0].x0)

    def _generate_list_AN(self):
        for i in range(len(self.l_OP)):
            self.l_AN += [AnimateSimulation(self.l_OP[i], self.ax)]
        return True
    
    def _data_to_OP_object(self):
        obj_proper = {}
        data_frame = self.data_frame.to_dict("list")
        TAM = []
        for i in range(self.N):
            obj_proper[i] = [{"name": data_frame["names"][i],
                        "x0": data_frame["x0"][i::self.N], 
                        "x1": data_frame["x1"][i::self.N],
                        "saveImg": self.saveImg}]
            self.l_OP.append(ObjectProperties(**obj_proper[i][0]))
            TAM += [len(self.l_OP[i].x0)]

        self._truncate_list_OP(TAM) 

    def _truncate_list_OP(self, listOfLengths): 
        """
        Para padronizar os tamanhos das listas.
        Em algum casos algumas ficam maior do que outras
        """

        ID = []
        for i in range(self.N):

            if listOfLengths[i] > listOfLengths[-i-1]:              
                ID += [i]

        if ID:
            for j in ID:
                del self.l_OP[j].x0[-1]
                del self.l_OP[j].x1[-1]
        return True

    def init(self):
        self._generate_list_AN()
        self._store_methods()
        return True

    def _store_methods(self):
        """
        Armazena os metodos `animate()` e `init()` de todos os objetos.
        """
        for i in range(len(self.l_AN)):
            self.store_animate += [self.l_AN[i].animate]
            self.store_init += [self.l_AN[i].init]
        return True
    
def init_animate(self, fig, repeat=False):
    anim = animation.FuncAnimation(fig, 
                                   join_mat_funcs(*self.store_animate), 
                                   frames    = np.arange(1, self.TAM_SHAPE),
                                   interval  = int(100 * DT),
                                   #blit     = True, #causa erro o "_on_time" quando usado no terminal
                                   init_func = join_mat_funcs(*self.store_init),
                                   repeat    = repeat)
    return anim

def start_animation(data_frame, p_output=None, show=True, saveas=None, repeat=False):
    fig, ax = plt.subplots()
    ax.set_xlim((-40, 40))
    ax.set_ylim((-40, 40))
    ax.set_aspect("equal")
    ax.grid()

    gerador = SimulationComponentsGenerator(data_frame, ax, saveas)
    gerador.init()

    anim = init_animate(gerador, fig, repeat=repeat)


    if saveas:
        salve(anim, p_output=p_output, saveas=saveas)

    if show:
        plt.show()

def salve(anim, p_output:str="", saveas:str="", dpi=200):
    import os
    from datetime import datetime

    formats = ["mp4", "gif"]

    if not os.path.exists(p_output):
        print(f"Não exite o diretório \"{p_output}\".")
        print("Tente com um diretório existente.")
        return False

    if saveas.startswith("."): saveas = saveas.replace(".", "")

    if not saveas in formats:
        print(f"Formato \"{saveas}\" não suportado.")
        print(f"""Tente um dos formatos: {", ".join(formats)}.""")
        return False

    file_base = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    file_name = os.path.join(p_output, file_base + "." + saveas)

    writer_base = {"fps": 60, "metadata": dict(artist='Me'), "codec": "libx264", "bitrate": -1}

    if saveas == "mp4":
        writer_base["fps"] = 1 / DT
        Writer = animation.writers['ffmpeg']
        writer = Writer(**writer_base)

    elif saveas == "gif":
        writer_base["fps"] = 15
        writer = LoopingPillowWriter(**writer_base)
        dpi = 100

    #TODO - está salvando a penas o primeiro frame
    # elif saveas == ".png":
    #     print(f"Salvando imagem em {file_name}")
    #     plt.savefig(file_name, dpi=dpi)

    print(f"Salvando animação em {file_name}")
    anim.save(file_name, writer=writer, dpi=dpi)
    print("Concluido.")

    return True

class LoopingPillowWriter(animation.PillowWriter):
    def finish(self):
        self._frames[0].save(
            self.outfile, save_all=True, append_images=self._frames[1:],
            duration=int(1000 / self.fps), loop=0)
