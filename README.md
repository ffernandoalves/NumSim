# NumSim

Este é um repositório para métodos numéricos em **C++** e **CPython**. Os "metódos númericos" vão ser escritos em `c++` e, 
por enquanto, a utilização do Python é repassar o dados iniciais para os metódos (em c++) e fazer a visualização
da simulação ([matplotlib](https://matplotlib.org/)).

Os "metodos" `init` dos "metódos númericos" são escritos em **CPython**. 

Livro de referência: *Numerical Simulation in Molecular Dynamics: 
Numerics, Algorithms, Parallelization, Applications by Michael Griebel, Gerhard Zumbusch, Stephan Knapek*

------------

## Instalação

A versão do Python utilizada na implementação é python3.7.

```
git clone https://github.com/ffernandoalves/NumSim.git
cd NumSim
python3.7 setup.py install
```

<!---
Usando virtualenv:

git clone https://github.com/ffernandoalves/NumSim.git
cd NumSim
virtualenv -p /usr/bin/python3.7 venv 
source venv/bin/activate
venv/bin/python3.7 setup.py install

ex: ```venv/bin/python3.7 my_sim.py```
-->

------------

## Exemplo

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

## TODO

- [ ] Melhorar o modulo [`animation.py`](https://github.com/ffernandoalves/NumSim/blob/main/numsim/animation.py) e torná-lo mais geral;

    - [x] Renomear nomes de variáveis, funções e classes;
    - [ ] Salvar simulação, formatos:
      - [x] `mp4`;
      - [x] `gif`;
      - [ ] `image (png)`.
    - [ ] Ajustar o Time da simulação.
- [ ] Criar um script para manipulação de dados, em um arquivo separado, em `c++` (ver [`velocity_verlet.cpp`](https://github.com/ffernandoalves/NumSim/blob/main/numsim/computer/velocity_verlet.cpp));
- [ ] Implementar os capítulos restantes [1].
------------

- [ ] Refazer a simulação em `c++` (`OpenGL`).

------------

## Referências

[1] Griebel, M.; Knapek, S.; Zumbush, G. Numerical Simulation in Molecular Dynamics; Springer: Berlin‐Heidelberg, 2007.

------------

## Licença

[MIT License](https://en.wikipedia.org/wiki/MIT_License).
