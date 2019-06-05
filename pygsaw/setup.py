import numpy

from setuptools import setup, find_packages
from setuptools.extension import Extension
from Cython.Build import cythonize

extensions = [
    Extension(
        "pygsaw._pygsaw",
        ["pygsaw/_pygsaw.pyx"],
        language="c++",
        include_dirs=['../src/', numpy.get_include()],  # not needed for fftw unless it is installed in an unusual place
        libraries=[],
        library_dirs=["../src/"],  # not needed for fftw unless it is installed in an unusual place
        extra_compile_args=["-std=c++11", "-D __lib_jigsaw"],
    )
]

setup(
    name="pygsaw",
    packages=find_packages(),
    ext_modules=cythonize(extensions)
)
