# setup.py
# A distutils setup script.

# Always prefer setuptools over distutils
from setuptools import setup

setup(
  name='gpxviewer',
  version='0.1',
  description='A GPX viewer',
  author='Sergey Salnikov',
  author_email='salsergey@gmail.com',
  license='GNU GPL3',
  packages=['gpxviewer'],
  #install_requires=['peppercorn'],
  data_files=[('share/gpxviewer/translations', ['data/gpxviewer_ru.qm'])],
  scripts=['gpxv']
)
