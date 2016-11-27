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

import os
import configparser
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
  def __init__(self, items = {}):
    super(GpxDocument, self).__init__(items)
    self.gpxmodel = gpx.GpxModel()

  def saveFile(self, filename):
    with open(filename, 'w') as file:
      self['NumberOfPoints'] = self.gpxmodel.rowCount()
      self['SkipPoints'] = self.gpxmodel.getIndexesWithIncludeState(gpx.INC_SKIP)
      self['MarkerPoints'] = self.gpxmodel.getIndexesWithIncludeState(gpx.INC_MARKER)
      self['CaptionPoints'] = self.gpxmodel.getIndexesWithIncludeState(gpx.INC_CAPTION)
      self['SplitLines'] = self.gpxmodel.getSplitLines()
      self['NeglectDistances'] = self.gpxmodel.getNeglectStates()

      self.update(TheConfig['ProfileStyle'])

      self['MarkerColors'] = self.gpxmodel.getPointStyles(gpx.MARKER_COLOR)
      self['MarkerStyles'] = self.gpxmodel.getPointStyles(gpx.MARKER_STYLE)
      self['MarkerSizes'] = self.gpxmodel.getPointStyles(gpx.MARKER_SIZE)

      self['SplitLineColors'] = self.gpxmodel.getPointStyles(gpx.LINE_COLOR)
      self['SplitLineStyles'] = self.gpxmodel.getPointStyles(gpx.LINE_STYLE)
      self['SplitLineWidths'] = self.gpxmodel.getPointStyles(gpx.LINE_WIDTH)

      self['CaptionPositionXs'] = self.gpxmodel.getPointStyles(gpx.CAPTION_POSX)
      self['CaptionPositionYs'] = self.gpxmodel.getPointStyles(gpx.CAPTION_POSY)
      self['CaptionSizes'] = self.gpxmodel.getPointStyles(gpx.CAPTION_SIZE)

      cfg = GpxConfigParser()
      cfg.read_dict({GPXMAGICK: self})
      cfg.write(file)

  def openFile(self, filename):
    cfg = GpxConfigParser()
    cfg.read(filename)
    if GPXMAGICK in cfg:
      self.update(cfg.items(GPXMAGICK))
      if os.path.exists(self['GPXFile']):
        self.gpxmodel.parse(self['GPXFile'])
        if self.gpxmodel.rowCount() != int(self['NumberOfPoints']):
          self.gpxmodel.resetModel()
          raise gpx.GpxWarning(self.tr('The file ') + self['GPXFile'] + self.tr(' has wrong number of valid waypoints. This file is likely to be damaged.'))

        self.gpxmodel.setIncludeStates(self['SkipPoints'], gpx.INC_SKIP)
        self.gpxmodel.setIncludeStates(self['MarkerPoints'], gpx.INC_MARKER)
        self.gpxmodel.setIncludeStates(self['CaptionPoints'], gpx.INC_CAPTION)
        self.gpxmodel.setSplitLines(self['SplitLines'], True)
        self.gpxmodel.setNeglectStates(self['NeglectDistances'], True)
        self.gpxmodel.updateDistance()

        TheConfig['ProfileStyle']['ProfileColor'] = self['ProfileColor']
        TheConfig['ProfileStyle']['FillColor'] = self['FillColor']
        TheConfig['ProfileStyle']['ProfileWidth'] = self['ProfileWidth']
        TheConfig['ProfileStyle']['MinimumAltitude'] = self['MinimumAltitude']
        TheConfig['ProfileStyle']['MaximumAltitude'] = self['MaximumAltitude']

        for i,m in zip(sorted(self['MarkerPoints'] + self['CaptionPoints']), self['MarkerColors']):
          self.gpxmodel.setPointStyle([i], gpx.MARKER_COLOR, m)
        for i,m in zip(sorted(self['MarkerPoints'] + self['CaptionPoints']), self['MarkerStyles']):
          self.gpxmodel.setPointStyle([i], gpx.MARKER_STYLE, m)
        for i,m in zip(sorted(self['MarkerPoints'] + self['CaptionPoints']), self['MarkerSizes']):
          self.gpxmodel.setPointStyle([i], gpx.MARKER_SIZE, m)

        for i,m in zip(self['SplitLines'], self['SplitLineColors']):
          self.gpxmodel.setPointStyle([i], gpx.LINE_COLOR, m)
        for i,m in zip(self['SplitLines'], self['SplitLineStyles']):
          self.gpxmodel.setPointStyle([i], gpx.LINE_STYLE, m)
        for i,m in zip(self['SplitLines'], self['SplitLineWidths']):
          self.gpxmodel.setPointStyle([i], gpx.LINE_WIDTH, m)

        for i,m in zip(self['CaptionPoints'], self['CaptionPositionXs']):
          self.gpxmodel.setPointStyle([i], gpx.CAPTION_POSX, m)
        for i,m in zip(self['CaptionPoints'], self['CaptionPositionYs']):
          self.gpxmodel.setPointStyle([i], gpx.CAPTION_POSY, m)
        for i,m in zip(self['CaptionPoints'], self['CaptionSizes']):
          self.gpxmodel.setPointStyle([i], gpx.CAPTION_SIZE, m)
      else: # GPXFile doesn't exist
        raise gpx.GpxWarning(self.tr('The file ') + self['GPXFile'] + self.tr(' doesn\'t exist.'))
    else: # GPXMAGICK not in cfg
      raise gpx.GpxWarning(self.tr('This file in not a valid GPX Viewer project file.'))

TheDocument = GpxDocument()
