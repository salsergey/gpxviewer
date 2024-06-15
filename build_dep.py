#!/usr/bin/env python3

# gpxviewer
#
# Copyright (C) 2024 Sergey Salnikov <salsergey@gmail.com>
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

import glob
import os
import re
import subprocess
from shutil import which


if __name__ == '__main__':
  for ui_file in os.listdir('ui'):
    print('converting ' + os.path.join('ui', ui_file) + ' -> ' + os.path.join('gpxviewer', 'ui_' + ui_file[:-2] + 'py'))
    uic_exe = which('pyuic6')
    subprocess.call(uic_exe + ' -o ' + os.path.join('gpxviewer', 'ui_' + ui_file[:-2] + 'py ') + os.path.join('ui', ui_file), shell=True)

  for ts_file in os.listdir('data/translations'):
    if ts_file.endswith('.ts'):
      print('updating ' + os.path.join('data/translations', ts_file))
      files = glob.glob('gpxviewer/*.py') + glob.glob('ui/*.ui')
      subprocess.call('pylupdate6 ' + ' '.join(files) + ' -ts ' + os.path.join('data/translations', ts_file), shell=True)
      lrelease_exe = which('lrelease')
      subprocess.call(lrelease_exe + os.path.join(' data/translations', ts_file), shell=True)

  print('compiling data/gpxviewer.qrc')
  rcc_exe = which('rcc')
  subprocess.call(rcc_exe + ' -g python -o gpxviewer/rc_gpxviewer.py data/gpxviewer.qrc', shell=True)
  with open('gpxviewer/rc_gpxviewer.py', 'r') as rc_file:
    lines = rc_file.readlines()
  with open('gpxviewer/rc_gpxviewer.py', 'w') as rc_file:
    for line in lines:
      rc_file.write(re.sub('PySide6', 'PyQt6', line))
