# gpxviewer
#
# Copyright (C) 2016 Sergey Salnikov <salsergey@gmail.com>
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
from os import path
from PyQt5.QtCore import QCoreApplication, QLocale, QTranslator
from PyQt5.QtWidgets import QApplication


app = None

def main():
  global app
  app = QApplication(sys.argv)

  translator = QTranslator(app)
  # TODO: rework paths
  if not translator.load(QLocale(), 'gpxviewer', '_', path.join(path.dirname(sys.argv[0]), 'data')):
    translator.load(QLocale(), 'gpxviewer', '_', path.join(path.dirname(sys.argv[0]), '../share/gpxviewer/translations'))
    #translator.load(QLocale(), 'gpxviewer', '_', path.join(sys.prefix, 'share/gpxviewer/translations'))
  QCoreApplication.installTranslator(translator)

  # We need to install translator first
  from gpxviewer.gpxmainwindow import GpxMainWindow

  my_mainWindow = GpxMainWindow()
  my_mainWindow.show()
  sys.exit(app.exec_())

if __name__ == '__main__':
  main()
