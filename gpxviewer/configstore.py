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

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
import os
import configparser


class ConfigStore(configparser.ConfigParser):
  def __init__(self):
    super(ConfigStore, self).__init__()
    defaults = {'MainWindow': {'WindowWidth': '1024',
                               'WindowHeight': '768',
                               'LoadGPXDirectory': os.path.expanduser('~'),
                               'ProjectDirectory': os.path.expanduser('~'),
                               'ShowDefault': 'True',
                               'ShowSkipped': 'True',
                               'ShowMarked': 'True',
                               'ShowCaptioned': 'True'},
                'PlotWindow': {'WindowWidth': '1024',
                               'WindowHeight': '768',
                               'SaveProfileDirectory': os.path.expanduser('~'),
                               'SaveFileExtension': 'PNG images (*.png)',
                               'SaveProfileWidth': '1280',
                               'SaveProfileHeight': '1024'},
                'ProfileStyle': {'ProfileColor': QColor(Qt.blue).rgba(),
                                 'FillColor': QColor(Qt.white).rgba(),
                                 'ProfileWidth': '1',
                                 'MinimumAltitude': '0',
                                 'MaximumAltitude': '1000'},
                'PointStyle': {'MarkerColorEnabled': True,
                               'MarkerColor': QColor(Qt.blue).rgba(),
                               'MarkerStyleEnabled': True,
                               'MarkerStyle': '.',
                               'MarkerSizeEnabled': True,
                               'MarkerSize': '5',
                               'SplitLineColorEnabled': True,
                               'SplitLineColor': QColor(Qt.red).rgba(),
                               'SplitLineStyleEnabled': True,
                               'SplitLineStyle': '-',
                               'SplitLineWidthEnabled': True,
                               'SplitLineWidth': '1',
                               'CaptionPositionEnabled': True,
                               'CaptionPositionX': '0',
                               'CaptionPositionY': '5',
                               'CaptionSizeEnabled': True,
                               'CaptionSize': '12'}
               }
    self.read_dict(defaults)
    if os.name == 'nt':
      self.configfile = os.path.expanduser('~/AppData/Local/gpxviewerrc')
    else:
      self.configfile = os.path.expanduser('~/.config/gpxviewerrc')
    if os.path.exists(self.configfile):
      self.read(self.configfile)

  def optionxform(self, optionstr):
    return optionstr

  def save(self):
    with open(self.configfile, 'w') as cfg:
      self.write(cfg)


TheConfig = ConfigStore()
