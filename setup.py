# gpxviewer
#
# Copyright (C) 2016-2020 Sergey Salnikov <salsergey@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3
# as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# setup.py
# A distutils setup script.

import os
import subprocess
import sys
from setuptools import Command, setup


class build_dep(Command):
  '''
  Compile all Qt-specific files including UIs, translations and resources.
  '''
  user_options = []

  def initialize_options(self):
    pass

  def finalize_options(self):
    pass

  def run(self):
    for ui_file in os.listdir('ui'):
      print('converting ' + os.path.join('ui', ui_file) + ' -> ' + os.path.join('gpxviewer', 'ui_' + ui_file[:-2] + 'py'))
      subprocess.call('pyuic5 -o ' + os.path.join('gpxviewer', 'ui_' + ui_file[:-2] + 'py ') + os.path.join('ui', ui_file), shell=True)

    for ts_file in os.listdir('data/translations'):
      if ts_file.endswith('.ts'):
        print('updating ' + os.path.join('data/translations', ts_file))
        subprocess.call('pylupdate5 gpxviewer/*.py -ts ' + os.path.join('data/translations', ts_file), shell=True)
        subprocess.call('lrelease-qt5 ' + os.path.join('data/translations', ts_file), shell=True)

    print('compiling data/gpxviewer.qrc')
    subprocess.call('pyrcc5 -o gpxviewer/rc_gpxviewer.py data/gpxviewer.qrc', shell=True)


if os.name == 'nt':
  datafiles = []
else:
  datafiles = [
    (os.path.join(sys.prefix, 'share/applications'), ['data/gpxviewer.desktop']),
    (os.path.join(sys.prefix, 'share/mime/packages'), ['data/gpxviewer.xml']),
    (os.path.join(sys.prefix, 'share/pixmaps'), ['data/icons/gpxviewer.png']),
    (os.path.join(sys.prefix, 'share/icons/hicolor/128x128/mimetypes'), ['data/icons/gpxviewer.png'])
  ]


setup(
  name='gpxviewer',
  version='2.1',
  description='GPX Viewer is an application for viewing GPX files and plotting altitude profiles',
  url='https://osdn.net/projects/gpxviewer',
  author='Sergey Salnikov',
  author_email='salsergey@gmail.com',
  license='GNU GPL3',
  packages=['gpxviewer'],
  install_requires=['lxml', 'QCustomPlot2>=2'],
  data_files=datafiles,
  entry_points={
    'gui_scripts': ['gpxv = gpxviewer:main']
  },
  cmdclass={
    'build_dep': build_dep
  }
)
