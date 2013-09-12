#!/usr/bin/env python

from setuptools import setup

setup(
    name="inigo",
    setup_requires=["vcversioner"],
    vcversioner={},
    py_modules=["inigo"],
    author="Corbin Simpson",
    author_email="cds@corbinsimpson.com",
    description="Decaying list data structure",
    long_description=open("README.rst").read(),
    license="MIT/X11",
    url="http://github.com/MostAwesomeDude/inigo",
)
