# gpxviewer
#
# Copyright (C) 2016-2019 Sergey Salnikov <salsergey@gmail.com>
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


import sys
from PyQt5.QtCore import QCoreApplication, QLocale, QTranslator
from PyQt5.QtWidgets import QApplication
from gpxviewer.configstore import TheConfig
import gpxviewer.rc_gpxviewer


def main():
  app = QApplication(sys.argv)
  QCoreApplication.setApplicationName('GPX Viewer')
  QCoreApplication.setApplicationVersion('1.2')

  if app.palette().window().color().lightness() < app.palette().windowText().color().lightness():
    TheConfig['MainWindow']['ColorTheme'] = 'dark_theme'
  else:
    TheConfig['MainWindow']['ColorTheme'] = 'light_theme'

  translator = QTranslator(app)
  translator.load(QLocale(), 'gpxviewer', '_', ':/translations')
  QCoreApplication.installTranslator(translator)

  # We need to install translator first
  from gpxviewer.gpxmainwindow import GpxMainWindow

  gpxMainWindow = GpxMainWindow()
  gpxMainWindow.show()
  if len(sys.argv) > 1:
    if sys.argv[1].lower().endswith('.gpx'):
      gpxMainWindow.openGPXFiles(sys.argv[1:])
    else:
      gpxMainWindow.openGPXProject(sys.argv[1])
  sys.exit(app.exec_())


if __name__ == '__main__':
  main()
