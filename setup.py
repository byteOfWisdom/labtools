from setuptools import setup
from Cython.Build import cythonize

setup(
    name = "labtools",
    ext_modules = cythonize("src/labtools/*.py", compiler_directives={"language_level": 3, "profile": False}),
)