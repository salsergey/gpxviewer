# gpxviewer
#
# Copyright (C) 2016-2017 Sergey Salnikov <salsergey@gmail.com>
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

import os
import configparser
from PyQt5.QtCore import QCoreApplication
import gpxviewer.gpxmodel as gpx
from gpxviewer.configstore import TheConfig


GPXMAGICK = '9e27ea8e'


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


class GpxDocument(dict):
  def __init__(self, items={}):
    super(GpxDocument, self).__init__(items)
    self.gpxparser = gpx.GpxParser()
    self.wptmodel = self.gpxparser.wptmodel
    self.trkmodel = self.gpxparser.trkmodel
    self['GPXFile'] = []

  def saveFile(self, filename):
    with open(filename, 'w') as file:
      self['NumberOfPoints'] = self.wptmodel.rowCount()
      self['NumberOfTracks'] = self.trkmodel.rowCount()
      self['SkipPoints'] = self.wptmodel.getIndexesWithIncludeState(gpx.INC_SKIP)
      self['MarkerPoints'] = self.wptmodel.getIndexesWithIncludeState(gpx.INC_MARKER)
      self['CaptionPoints'] = self.wptmodel.getIndexesWithIncludeState(gpx.INC_CAPTION)
      self['SplitLines'] = self.wptmodel.getSplitLines()
      self['NeglectDistances'] = self.wptmodel.getNeglectStates()
      self['SkipTracks'] = self.trkmodel.getIndexesWithIncludeState(gpx.INC_SKIP)

      self.update(TheConfig['ProfileStyle'])

      self['MarkerColors'] = self.wptmodel.getPointStyles(gpx.MARKER_COLOR)
      self['MarkerStyles'] = self.wptmodel.getPointStyles(gpx.MARKER_STYLE)
      self['MarkerSizes'] = self.wptmodel.getPointStyles(gpx.MARKER_SIZE)

      self['SplitLineColors'] = self.wptmodel.getPointStyles(gpx.LINE_COLOR)
      self['SplitLineStyles'] = self.wptmodel.getPointStyles(gpx.LINE_STYLE)
      self['SplitLineWidths'] = self.wptmodel.getPointStyles(gpx.LINE_WIDTH)

      self['CaptionPositionXs'] = self.wptmodel.getPointStyles(gpx.CAPTION_POSX)
      self['CaptionPositionYs'] = self.wptmodel.getPointStyles(gpx.CAPTION_POSY)
      self['CaptionSizes'] = self.wptmodel.getPointStyles(gpx.CAPTION_SIZE)

      cfg = GpxConfigParser()
      cfg.read_dict({GPXMAGICK: self})
      cfg.write(file)

  def openFile(self, filename):
    cfg = GpxConfigParser()
    try:
      cfg.read(filename)
    except (configparser.ParsingError, UnicodeDecodeError):
      raise gpx.GpxWarning(QCoreApplication.translate('GpxDocument', 'This file in not a valid GPX Viewer project file.'))

    if GPXMAGICK in cfg:
      self.update(cfg.items(GPXMAGICK))
      self.gpxparser.resetModels()
      # Fix to handle legacy files
      if type(self['GPXFile']) == str:
        self['GPXFile'] = [self['GPXFile']]

      for file in self['GPXFile']:
        if os.path.exists(file):
          self.gpxparser.parse(file)
        else:  # file doesn't exist
          raise gpx.GpxWarning(QCoreApplication.translate('GpxDocument', 'The file ') + file + QCoreApplication.translate('GpxDocument', ' doesn\'t exist.'))

      if 'NumberOfPoints' in self and self.wptmodel.rowCount() != int(self['NumberOfPoints']) or \
         'NumberOfTracks' in self and self.trkmodel.rowCount() != int(self['NumberOfTracks']):
        raise gpx.GpxWarning(QCoreApplication.translate('GpxDocument', 'One of the files has wrong number of valid waypoints or tracks. This file is likely to be damaged or changed from outside.'))

      if 'SkipPoints' in self:
        self.wptmodel.setIncludeStates(self['SkipPoints'], gpx.INC_SKIP, False)
      if 'MarkerPoints' in self:
        self.wptmodel.setIncludeStates(self['MarkerPoints'], gpx.INC_MARKER, False)
      if 'CaptionPoints' in self:
        self.wptmodel.setIncludeStates(self['CaptionPoints'], gpx.INC_CAPTION, False)
      if 'SplitLines' in self:
        self.wptmodel.setSplitLines(self['SplitLines'], True)
      if 'NeglectDistances' in self:
        self.wptmodel.setNeglectStates(self['NeglectDistances'], True)
      if 'SkipTracks' in self:
        self.trkmodel.setIncludeStates(self['SkipTracks'], gpx.INC_SKIP, False)
      self.gpxparser.updatePoints()

      if 'ProfileColor' in self:
        TheConfig['ProfileStyle']['ProfileColor'] = self['ProfileColor']
      if 'FillColor' in self:
        TheConfig['ProfileStyle']['FillColor'] = self['FillColor']
      if 'ProfileWidth' in self:
        TheConfig['ProfileStyle']['ProfileWidth'] = self['ProfileWidth']
      if 'MinimumAltitude' in self:
        TheConfig['ProfileStyle']['MinimumAltitude'] = self['MinimumAltitude']
      if 'MaximumAltitude' in self:
        TheConfig['ProfileStyle']['MaximumAltitude'] = self['MaximumAltitude']
      if 'TimeZoneOffset' in self:
        TheConfig['ProfileStyle']['TimeZoneOffset'] = self['TimeZoneOffset']

      if 'MarkerPoints' in self and 'CaptionPoints' in self and 'MarkerColors' in self:
        for i, m in zip(sorted(self['MarkerPoints'] + self['CaptionPoints']), self['MarkerColors']):
          self.wptmodel.setPointStyle([i], gpx.MARKER_COLOR, m)
      if 'MarkerPoints' in self and 'CaptionPoints' in self and 'MarkerStyles' in self:
        for i, m in zip(sorted(self['MarkerPoints'] + self['CaptionPoints']), self['MarkerStyles']):
          self.wptmodel.setPointStyle([i], gpx.MARKER_STYLE, m)
      if 'MarkerPoints' in self and 'CaptionPoints' in self and 'MarkerSizes' in self:
        for i, m in zip(sorted(self['MarkerPoints'] + self['CaptionPoints']), self['MarkerSizes']):
          self.wptmodel.setPointStyle([i], gpx.MARKER_SIZE, m)

      if 'SplitLines' in self and 'SplitLineColors' in self:
        for i, m in zip(self['SplitLines'], self['SplitLineColors']):
          self.wptmodel.setPointStyle([i], gpx.LINE_COLOR, m)
      if 'SplitLines' in self and 'SplitLineStyles' in self:
        for i, m in zip(self['SplitLines'], self['SplitLineStyles']):
          self.wptmodel.setPointStyle([i], gpx.LINE_STYLE, m)
      if 'SplitLines' in self and 'SplitLineWidths' in self:
        for i, m in zip(self['SplitLines'], self['SplitLineWidths']):
          self.wptmodel.setPointStyle([i], gpx.LINE_WIDTH, m)

      if 'CaptionPoints' in self and 'CaptionPositionXs' in self:
        for i, m in zip(self['CaptionPoints'], self['CaptionPositionXs']):
          self.wptmodel.setPointStyle([i], gpx.CAPTION_POSX, m)
      if 'CaptionPoints' in self and 'CaptionPositionYs' in self:
        for i, m in zip(self['CaptionPoints'], self['CaptionPositionYs']):
          self.wptmodel.setPointStyle([i], gpx.CAPTION_POSY, m)
      if 'CaptionPoints' in self and 'CaptionSizes' in self:
        for i, m in zip(self['CaptionPoints'], self['CaptionSizes']):
          self.wptmodel.setPointStyle([i], gpx.CAPTION_SIZE, m)
    else:  # GPXMAGICK not in cfg
      raise gpx.GpxWarning(QCoreApplication.translate('GpxDocument', 'This file in not a valid GPX Viewer project file.'))


TheDocument = GpxDocument()
