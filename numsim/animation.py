import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

from itertools import chain

DT = 0.015
COLOR_BOGY = [np.array([np.nan] * 3)] #armazena as cores de cada corpo celeste para evitar repetição de cores.

def join_mat_funcs(*funcs):
    return lambda *args: tuple(chain.from_iterable(f(*args) for f in funcs))

class CelestialBody:
    def __init__(self, **entries):
        self.__dict__.update(entries)

def choose_color():
    color = np.random.rand(3)
    comparison = color == COLOR_BOGY
    if comparison.any():
        choose_color()
    COLOR_BOGY.append(color)
    return color

class CelestialBodyAnimate:
    """
    + CB - CelestialBody obj
    """
    def __init__(self, CB, ax):
        self.x, self.y = CB.x0, CB.x1
        self.saveImg = CB.saveImg
        self.ax = ax
        #self.ax.grid()
                
        #color = np.random.rand(3)
        color = choose_color()
         
        self.body, = self.ax.plot([], [], 'o-', color=color, label=CB.name, lw=1)
        self.body_trail, = self.ax.plot([], [], color=color, lw=0.5)
        self.leg = plt.legend()
        self.leg_lines = self.leg.get_lines()
        self.leg_texts = self.leg.get_texts()
        plt.setp(self.leg_lines, linewidth=4)
        plt.setp(self.leg_texts, fontsize='x-large')
        self.time_template = 'Time = %.2fs'
        self.time_text = self.ax.text(0.05, 0.9, '', transform=self.ax.transAxes)

    def init(self):
        self.body.set_data([self.x[0]], [self.y[0]])
        self.body_trail.set_data([], [])
        self.time_text.set_text("")
        return self.body, self.body_trail, self.time_text,

    def animate(self, i):
        self.body.set_data(self.x[i], self.y[i])
        self.body_trail.set_data(self.x[:i], self.y[:i])
        self.time_text.set_text(self.time_template % (i * DT))

        #if self.saveImg:
        #    if i == len(self.x) - 1:
        #        salve(None, saveAnim=False, saveImg=self.saveImg)
        return self.body, self.body_trail, self.time_text,


class GeradorCOA:
    def __init__(self, data_frame, ax, saveImg=False):
        self.data_frame = data_frame
        self.delta_t = self.data_frame["delta_t"][0]
        self.ax = ax
        self.saveImg = saveImg

        self.N = int(self.data_frame["N"][0])
        self.time = self.data_frame["time"]

        self.CB = []
        self._convertBodyforObj()
        self.G_CBA = []
        self.store_animate = []
        self.store_init = []

        self.TAM_SHAPE = len(self.CB[0].x0)

    def _gerarListOfObj(self):
        for i in range(len(self.CB)):
            self.G_CBA += [CelestialBodyAnimate(self.CB[i], self.ax)]
        return True
    
    def _convertBodyforObj(self):
        body = {}
        data_frame = self.data_frame.to_dict("list")
        TAM = []
        for i in range(self.N):
            body[i] = [{"name": data_frame["names"][i],
                        "x0": data_frame["x0"][i::self.N], 
                        "x1": data_frame["x1"][i::self.N],
                        "saveImg": self.saveImg}]
            self.CB.append(CelestialBody(**body[i][0]))
            TAM += [len(self.CB[i].x0)]

        self._truncateListCB(TAM) 

    def _truncateListCB(self, listOfLengths): 
        """
        Para padronizar os tamanhos das listas.
        Em algum casos algumas ficam maior do que outras
        """

        ID = []
        for i in range(self.N):

            if listOfLengths[i] > listOfLengths[-i-1]:              
                ID += [i]

        if ID:
            print("ID: ", ID)
            for j in ID:
                del self.CB[j].x0[-1]
                del self.CB[j].x1[-1]
        return True

    def init(self):
        self._gerarListOfObj()
        self._storeMethods()
        return True

    def _storeMethods(self):
        """
        Armazena os metodos `animate()` e `init()` de todos os objetos.
        """
        for i in range(len(self.G_CBA)):
            self.store_animate += [self.G_CBA[i].animate]
            self.store_init += [self.G_CBA[i].init]
        return True
    
def init_animate(self, fig, repeat=False):
    anim = animation.FuncAnimation(fig, 
                                    join_mat_funcs(*self.store_animate), 
                                    frames=np.arange(1, self.TAM_SHAPE),
                                    interval=int(100 * DT),
                                    #blit=True, #causa erro de _on_time no terminal
                                    init_func=join_mat_funcs(*self.store_init),
                                    repeat=repeat)
    return anim

def start_animation(data_frame, show=True, saveAnim=False, saveImg=False, repeat=False):
    fig, ax = plt.subplots()
    ax.set_xlim((-40, 40))
    ax.set_ylim((-40, 40))
    ax.set_aspect("equal")
    ax.grid()

    gerador = GeradorCOA(data_frame, ax, saveImg)
    gerador.init()

    anim = init_animate(gerador, fig, repeat=repeat)


    if saveAnim or saveImg:
        salve(anim, saveAnim=saveAnim, saveImg=saveImg)

    if show:
        plt.show()


def salve(anim, p_output, saveAnim=False, saveImg=False):
    import os
    from datetime import datetime
    file_base = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    file_name = f"{os.path.join(p_output, file_base)}"

    if saveAnim:
        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=1/DT, metadata=dict(artist='Me'), codec="libx264", bitrate=-1)
        print(f"Salvando animação em {file_name}.mp4")
        anim.save(file_name + ".mp4", writer=writer, dpi=200)

    if saveImg:
        #TODO
        #está salvando a penas o primeiro frame
        print(f"Salvando imagem em {file_name}.png")
        plt.savefig(file_name, dpi=200)

    print("Concluido.")
    return True
