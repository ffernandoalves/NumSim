import os
import pandas as pd


# path's
p_numsim   = os.path.dirname(os.path.abspath(__file__))
modulo_dir = p_numsim.replace('numsim', '')
p_computer = os.path.join(p_numsim, "computer/")

def load_data_generated(data_output, sep="&", engine="c"):
    data_frame = pd.read_csv(data_output, sep=sep, engine=engine)
    return data_frame