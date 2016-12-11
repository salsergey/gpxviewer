# setup.py
# A distutils setup script.

from setuptools import setup, Command
import sys, os, subprocess


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
      subprocess.call('pyuic5 ' + os.path.join('ui', ui_file) + '>' + os.path.join('gpxviewer', 'ui_' + ui_file[:-2] + 'py'), shell=True)

    for ts_file in os.listdir('data/translations'):
      if ts_file.endswith('.ts'):
        print('updating ' + os.path.join('data/translations', ts_file))
        subprocess.call('pylupdate5 gpxviewer/*.py -ts ' + os.path.join('data/translations', ts_file), shell=True)
        subprocess.call('lrelease-qt5 ' + os.path.join('data/translations', ts_file), shell=True)

    print('compiling data/gpxviewer.qrc')
    subprocess.call('pyrcc5 data/gpxviewer.qrc > gpxviewer/rc_gpxviewer.py', shell=True)


if os.name == 'nt':
  datafiles = []
else:
  datafiles = [
    (os.path.join(sys.prefix, 'share/applications'), ['data/gpxviewer.desktop']),
    (os.path.join(sys.prefix, 'share/pixmaps'), ['data/icons/gpxviewer.png'])
  ]


setup(
  name='gpxviewer',
  version='0.2',
  description='A GPX viewer',
  url='https://bitbucket.org/salsergey/gpxviewer',
  author='Sergey Salnikov',
  author_email='salsergey@gmail.com',
  license='GNU GPL3',
  packages=['gpxviewer'],
  install_requires=['matplotlib'],
  data_files=datafiles,
  entry_points={
    'gui_scripts': ['gpxv = gpxviewer:main']
  },
  cmdclass={
    'build_dep': build_dep
  }
)
