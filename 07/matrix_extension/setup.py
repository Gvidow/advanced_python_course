from setuptools import setup, Extension


setup(
    name="matrix",
    version="1.0.0",
    ext_modules=[Extension("matrix", ["matrix.c"])]
)
