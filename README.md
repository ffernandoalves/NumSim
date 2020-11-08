# NumSim

Este é um repositório para métodos numéricos em C++ e Python.

Exemplo:
```python
from numsim import init_verlet, load_data_generated, start_animation

data_in  = "examples/data/sun_system.csv"
data_out = "examples/data/output.csv"

init_verlet(data_in, data_out, delta_t=0.05, t_end=30.5)
df = load_data_generated(data_out)
start_animation(df)
```
![Deploy](https://github.com/ffernandoalves/NumSim/blob/main/examples/data/sun_system.gif)


------------

## Referências (ou _"copiado de"_)

O método - _Velocidade de Verlet_ - foi adaptado a partir do livro: 

[1] Griebel, M.; Knapek, S.; Zumbush, G. Numerical Simulation in Molecular Dynamics; Springer: Berlin‐Heidelberg, 2007.
