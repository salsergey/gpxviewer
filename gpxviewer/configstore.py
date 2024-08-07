# gpxviewer
#
# Copyright (C) 2016-2024 Sergey Salnikov <salsergey@gmail.com>
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
from PyQt6.QtCore import QCoreApplication
from PyQt6.QtGui import qRgba


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
    self.defaultColumnsNumber = 7
    self.recentProjects = []
    self.columnsToCopy = []

    defaults = {'MainWindow': {'WindowWidth': 1200,
                               'WindowHeight': 800,
                               'LoadGPXDirectory': os.path.expanduser('~'),
                               'GPSFileExtension': QCoreApplication.translate('ConfigStore', 'GPX XML (*.gpx *.GPX)'),
                               'ProjectDirectory': os.path.expanduser('~'),
                               'ProjectExtension': QCoreApplication.translate('ConfigStore', 'GPX Viewer Projects (*.gpxv *.GPXV)'),
                               'DetailedView': False,
                               'ShowDefault': True,
                               'ShowSkipped': True,
                               'ShowMarked': True,
                               'ShowCaptioned': True,
                               'ShowMarkedCaptioned': True,
                               'RecentProjects': [],
                               'MaxRecentProjects': 10,
                               'ColumnsToCopy': []},
                'PlotWindow': {'WindowWidth': 1200,
                               'WindowHeight': 800,
                               'SaveProfileDirectory': os.path.expanduser('~'),
                               'SaveFileExtension': QCoreApplication.translate('ConfigStore', 'PNG images (*.png *.PNG)'),
                               'SaveProfileWidth': 1280,
                               'SaveProfileHeight': 1024},
                'StatWindow': {'WindowWidth': 800,
                               'WindowHeight': 800,
                               'BySplittingLines': True},
                'ProfileStyle': {'ProfileColor': qRgba(255, 0, 0, 150),
                                 'FillColor': qRgba(255, 0, 0, 50),
                                 'ProfileWidth': 1.0,
                                 'SelectedPointsOnly': False,
                                 'StartFromZero': True,
                                 'MinimumAltitude': 0,
                                 'MaximumAltitude': 1000,
                                 'AutoscaleAltitudes': False,
                                 'ShowHours': True,
                                 'AbsoluteTime': False,
                                 'UseSystemTheme': False,
                                 'FontSize': 12,
                                 'BoldFont': False,
                                 'ItalicFont': False,
                                 'DistanceCoefficient': 1.0,
                                 'ShowDistanceCoefficient': True,
                                 'TimeZoneOffset': 420,
                                 'SortByTime': False,
                                 'ReadNameFromTag': 0,
                                 'CoordinateFormat': 0,
                                 'PointsToTrack': False,
                                 'DeletePoints': False,
                                 'TracksToPoints': False,
                                 'DeleteTracks': False},
                'PointStyle': {'MarkerColorEnabled': True,
                               'MarkerColor': qRgba(255, 0, 0, 200),
                               'MarkerStyleEnabled': True,
                               'MarkerStyle': '.',
                               'MarkerSizeEnabled': True,
                               'MarkerSize': 5,
                               'CaptionPositionEnabled': True,
                               'CaptionPositionX': 0,
                               'CaptionPositionY': 5,
                               'CaptionRotationEnabled': True,
                               'CaptionRotation': 90,
                               'CaptionSizeEnabled': True,
                               'CaptionSize': 12,
                               'CaptionBoldEnabled': True,
                               'CaptionBold': False,
                               'CaptionItalicEnabled': True,
                               'CaptionItalic': False,
                               'SplitLineColorEnabled': True,
                               'SplitLineColor': qRgba(255, 0, 0, 150),
                               'SplitLineStyleEnabled': True,
                               'SplitLineStyle': '--',
                               'SplitLineWidthEnabled': True,
                               'SplitLineWidth': 1.0}}
    defaults['ProfileStyle']['FontFamily'] = 'Arial' if os.name == 'nt' else 'Sans Serif'
    self.read_dict(defaults)

    if os.name == 'nt':
      self.configfile = os.path.expanduser('~/AppData/Local/gpxviewerrc')
    else:
      self.configfile = os.path.expanduser('~/.config/gpxviewerrc')
    if os.path.exists(self.configfile):
      self.read(self.configfile)
      self.recentProjects = eval(self['MainWindow']['RecentProjects'])
      self.columnsToCopy = eval(self['MainWindow']['ColumnsToCopy'])

  def optionxform(self, optionstr):
    return optionstr

  def save(self):
    with open(self.configfile, 'w') as cfg:
      self['MainWindow']['RecentProjects'] = str(self.recentProjects)
      self['MainWindow']['ColumnsToCopy'] = str(self.columnsToCopy)
      self.write(cfg)

  def getValue(self, group, key):
    if group == 'ProfileStyle':
      if key in {'ProfileColor', 'FillColor', 'FontSize', 'MinimumAltitude', 'MaximumAltitude',
                 'TimeZoneOffset', 'ReadNameFromTag', 'CoordinateFormat'}:
        return int(self['ProfileStyle'][key])
      elif key in {'ProfileWidth', 'DistanceCoefficient'}:
        return float(self['ProfileStyle'][key])
      elif key in {'SelectedPointsOnly', 'StartFromZero', 'AutoscaleAltitudes', 'ShowHours', 'AbsoluteTime',
                   'BoldFont', 'ItalicFont', 'UseSystemTheme', 'ShowDistanceCoefficient', 'SortByTime',
                   'PointsToTrack', 'DeletePoints', 'TracksToPoints', 'DeleteTracks'}:
        return self['ProfileStyle'].getboolean(key)
      else:
        return self['ProfileStyle'][key]

    elif group == 'PointStyle':
      if key in {'MarkerColor', 'MarkerSize', 'CaptionPositionX', 'CaptionPositionY',
                 'CaptionRotation', 'CaptionSize', 'SplitLineColor'}:
        return int(self['PointStyle'][key])
      elif key in {'SplitLineWidth'}:
        return float(self['PointStyle'][key])
      elif key in {'MarkerColorEnabled', 'MarkerStyleEnabled', 'MarkerSizeEnabled',
                   'CaptionPositionEnabled', 'CaptionRotationEnabled', 'CaptionSizeEnabled',
                   'CaptionBoldEnabled', 'CaptionBold', 'CaptionItalicEnabled', 'CaptionItalic',
                   'SplitLineColorEnabled', 'SplitLineStyleEnabled', 'SplitLineWidthEnabled'}:
        return self['PointStyle'].getboolean(key)
      else:
        return self['PointStyle'][key]

    else:
      return self['PointStyle'][key]


TheConfig = ConfigStore()
