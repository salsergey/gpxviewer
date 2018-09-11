# gpxviewer
#
# Copyright (C) 2016-2018 Sergey Salnikov <salsergey@gmail.com>
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

import configparser
import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor


class GpxConfigParser(configparser.ConfigParser):
  def __init__(self):
    super(GpxConfigParser, self).__init__()

  def items(self, section, raw=False, vars=None):
    items = dict(super(GpxConfigParser, self).items(section, raw=raw, vars=vars))
    for i in items:
      if items[i][0] == '[' and items[i][-1] == ']':
        items[i] = eval(items[i])
    return items

  def optionxform(self, optionstr):
    return optionstr


class ConfigStore(configparser.ConfigParser):
  def __init__(self):
    super(ConfigStore, self).__init__()
    self.recentProjects = []

    defaults = {'MainWindow': {'WindowWidth': '1024',
                               'WindowHeight': '768',
                               'LoadGPXDirectory': os.path.expanduser('~'),
                               'ProjectDirectory': os.path.expanduser('~'),
                               'ShowDefault': 'True',
                               'ShowSkipped': 'True',
                               'ShowMarked': 'True',
                               'ShowCaptioned': 'True',
                               'RecentProjects': [],
                               'MaxRecentProjects': 10},
                'PlotWindow': {'WindowWidth': '1024',
                               'WindowHeight': '768',
                               'SaveProfileDirectory': os.path.expanduser('~'),
                               'SaveFileExtension': 'PNG images (*.png)',
                               'SaveProfileWidth': '1280',
                               'SaveProfileHeight': '1024'},
                'StatWindow': {'WindowWidth': '1024',
                               'WindowHeight': '768',
                               'BySplittingLines': True},
                'ProfileStyle': {'ProfileColor': QColor(Qt.blue).rgba(),
                                 'FillColor': QColor(Qt.white).rgba(),
                                 'ProfileWidth': '1',
                                 'MinimumAltitude': '0',
                                 'MaximumAltitude': '1000',
                                 'DistanceCoefficient': '1',
                                 'TimeZoneOffset': '420',
                                 'SelectedPointsOnly': False},
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
                               'CaptionSize': '12'}}
    self.read_dict(defaults)

    if os.name == 'nt':
      self.configfile = os.path.expanduser('~/AppData/Local/gpxviewerrc')
    else:
      self.configfile = os.path.expanduser('~/.config/gpxviewerrc')
    if os.path.exists(self.configfile):
      self.read(self.configfile)
      self.recentProjects = eval(self['MainWindow']['RecentProjects'])

  def optionxform(self, optionstr):
    return optionstr

  def save(self):
    with open(self.configfile, 'w') as cfg:
      self['MainWindow']['RecentProjects'] = str(self.recentProjects)
      self.write(cfg)


TheConfig = ConfigStore()
