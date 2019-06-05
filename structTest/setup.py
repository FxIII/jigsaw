import numpy
from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("test.pyx"),
    include_path=[numpy.get_include()]
)
