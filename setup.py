# setup.py
# A distutils setup script.

import sys
from os import path
from setuptools import setup

setup(
  name='gpxviewer',
  version='0.1',
  description='A GPX viewer',
  url='https://bitbucket.org/salsergey/gpxviewer',
  author='Sergey Salnikov',
  author_email='salsergey@gmail.com',
  license='GNU GPL3',
  packages=['gpxviewer'],
  # TODO: dependencies
  install_requires=['matplotlib'],
  data_files=[(path.join(sys.prefix, 'share/gpxviewer/translations'), ['data/gpxviewer_ru.qm'])],
  #scripts=['gpxv']
  entry_points={
    'gui_scripts': ['gpxv = gpxviewer:main']
  }
)
