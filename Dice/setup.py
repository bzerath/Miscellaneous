from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
from Cython.Distutils import build_ext
 
extensions = [
    Extension("LibDice", ["LibDice.pyx"])  # a renommer selon les besoins
]
 
setup(
    cmdclass={'build_ext': build_ext},
    ext_modules=cythonize(extensions),
)
