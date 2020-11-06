import os.path
from setuptools import find_packages
from distutils.core import setup, Extension

p_source = os.path.dirname(os.path.abspath(__file__))
p_computer = os.path.join(p_source, "numsim/computer/")

with open('requirements.txt') as f:
    requirements = f.read().splitlines()


module1 = Extension("numsim.computer.velocity_verlet",
                    sources=[os.path.join(p_computer, "velocity_verlet.cpp")], 
                    language='c++')

data_file1 = ("examples", ["examples/celetial_body.py"])
data_file2 = ("examples/data", ["examples/data/input.csv.example", 
                                "examples/data/sun_system.csv", 
                                "examples/data/output.csv.example",
                                "examples/data/2020-07-16-03-33-55.png"])


setup(name            = "numsim",
    version           = "0.0.1",
    author            = "Fernando Ribeiro Alves",
    author_email      = "fernandoribeiro889@gmail.com",
    keywords          = "numeric simulate math cfd phisic particle",
    # license           = "",
    # description       = "",
    long_description  = open('README.md').read(),
    install_requires  = requirements,
    ext_modules       = [module1],
    packages          = find_packages(),
    data_files        = [data_file1, data_file2]
)
