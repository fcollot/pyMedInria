# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from distutils.core import setup
from setuptools import find_packages


setup(name='pymedinria',
      version='@PROJECT_VERSION@',
      packages=find_packages(include=['pymedinria', 'pymedinria.*']),
      install_requires=[
      '@MED_PYSIDE_PACKAGE@',
      'numpy',
      'SimpleITK',
      'vtk',
      ],
)
