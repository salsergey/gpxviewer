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
from PyQt5 import QtCore
import gpxviewer.gpxmodel as gpx
from gpxviewer.configstore import GpxConfigParser, TheConfig


GPXMAGICK = '9e27ea8e'


class GpxDocument(QtCore.QObject):
  def __init__(self, parent=None):
    super(GpxDocument, self).__init__(parent)
    self.gpxparser = gpx.GpxParser()
    self.wptmodel = self.gpxparser.wptmodel
    self.trkmodel = self.gpxparser.trkmodel
    self.doc = {}
    self.doc['GPXFile'] = []

  def saveFile(self, filename):
    with open(filename, 'w', encoding='utf-8') as file:
      # Number of points/tracks to check the validity of the files
      self.doc['NumberOfPoints'] = self.wptmodel.rowCount()
      self.doc['NumberOfTracks'] = self.trkmodel.rowCount()

      self.doc['SkipPoints'] = self.wptmodel.getIndexesWithIncludeState(gpx.INC_SKIP)
      self.doc['MarkerPoints'] = self.wptmodel.getIndexesWithIncludeState(gpx.INC_MARKER)
      self.doc['CaptionPoints'] = self.wptmodel.getIndexesWithIncludeState(gpx.INC_CAPTION)
      self.doc['SplitLines'] = self.wptmodel.getSplitLines()
      self.doc['NeglectDistances'] = self.wptmodel.getNeglectStates()
      self.doc['SkipTracks'] = self.trkmodel.getIndexesWithIncludeState(gpx.INC_SKIP)

      self.doc.update(TheConfig['ProfileStyle'])

      self.doc['MarkerColors'] = self.wptmodel.getPointStyles(gpx.MARKER_COLOR)
      self.doc['MarkerStyles'] = self.wptmodel.getPointStyles(gpx.MARKER_STYLE)
      self.doc['MarkerSizes'] = self.wptmodel.getPointStyles(gpx.MARKER_SIZE)

      self.doc['SplitLineColors'] = self.wptmodel.getPointStyles(gpx.LINE_COLOR)
      self.doc['SplitLineStyles'] = self.wptmodel.getPointStyles(gpx.LINE_STYLE)
      self.doc['SplitLineWidths'] = self.wptmodel.getPointStyles(gpx.LINE_WIDTH)

      self.doc['CaptionPositionXs'] = self.wptmodel.getPointStyles(gpx.CAPTION_POSX)
      self.doc['CaptionPositionYs'] = self.wptmodel.getPointStyles(gpx.CAPTION_POSY)
      self.doc['CaptionSizes'] = self.wptmodel.getPointStyles(gpx.CAPTION_SIZE)

      self.doc['ChangedNames'] = self.wptmodel.changedNames
      self.doc['PointNames'] = self.wptmodel.pointNames

      cfg = GpxConfigParser()
      cfg.read_dict({GPXMAGICK: self.doc})
      cfg.write(file)

  def openFile(self, filename):
    cfg = GpxConfigParser()
    try:
      cfg.read(filename, encoding='utf-8')
    except (configparser.ParsingError, UnicodeDecodeError):
      raise gpx.GpxWarning(QtCore.QCoreApplication.translate('GpxDocument', 'This file in not a valid GPX Viewer project file.'))

    if GPXMAGICK in cfg:
      self.doc.clear()
      self.doc.update(cfg.items(GPXMAGICK))
      self.gpxparser.resetModels()
      # Fix to handle legacy files
      if type(self.doc['GPXFile']) == str:
        self.doc['GPXFile'] = [self.doc['GPXFile']]

      self.applyToAll = False
      for i, file in enumerate(self.doc['GPXFile']):
        if not QtCore.QFileInfo(file).exists():
          self.newFilePath = ''
          self.fileNotFound.emit(file)
          if self.newFilePath != '':
            self.doc['GPXFile'][i] = self.newFilePath
            file = self.newFilePath
            if self.applyToAll:
              for j in range(i + 1, len(self.doc['GPXFile'])):
                self.doc['GPXFile'][j] = self.doc['GPXFile'][j].replace(QtCore.QFileInfo(self.doc['GPXFile'][j]).path(), QtCore.QFileInfo(self.newFilePath).path())
          else:
            raise gpx.GpxWarning(QtCore.QCoreApplication.translate('GpxDocument', 'One of GPX files doesn\'t exist. This project can\'t be opened.'))
        self.gpxparser.parse(file)

      if ('NumberOfPoints' in self.doc and self.wptmodel.rowCount() != int(self.doc['NumberOfPoints'])) or \
         ('NumberOfTracks' in self.doc and self.trkmodel.rowCount() != int(self.doc['NumberOfTracks'])):
        raise gpx.GpxWarning(QtCore.QCoreApplication.translate('GpxDocument', 'One of the files has wrong number of valid waypoints or tracks. This file is likely to be damaged or changed from outside.'))

      if 'SkipPoints' in self.doc:
        self.wptmodel.setIncludeStates(self.doc['SkipPoints'], gpx.INC_SKIP, False)
      if 'MarkerPoints' in self.doc:
        self.wptmodel.setIncludeStates(self.doc['MarkerPoints'], gpx.INC_MARKER, False)
      if 'CaptionPoints' in self.doc:
        self.wptmodel.setIncludeStates(self.doc['CaptionPoints'], gpx.INC_CAPTION, False)
      if 'SplitLines' in self.doc:
        self.wptmodel.setSplitLines(self.doc['SplitLines'], True)
      if 'NeglectDistances' in self.doc:
        self.wptmodel.setNeglectStates(self.doc['NeglectDistances'], True)
      if 'SkipTracks' in self.doc:
        self.trkmodel.setIncludeStates(self.doc['SkipTracks'], gpx.INC_SKIP, False)

      if 'ProfileColor' in self.doc:
        TheConfig['ProfileStyle']['ProfileColor'] = self.doc['ProfileColor']
      if 'FillColor' in self.doc:
        TheConfig['ProfileStyle']['FillColor'] = self.doc['FillColor']
      if 'ProfileWidth' in self.doc:
        TheConfig['ProfileStyle']['ProfileWidth'] = self.doc['ProfileWidth']
      if 'MinimumAltitude' in self.doc:
        TheConfig['ProfileStyle']['MinimumAltitude'] = self.doc['MinimumAltitude']
      if 'MaximumAltitude' in self.doc:
        TheConfig['ProfileStyle']['MaximumAltitude'] = self.doc['MaximumAltitude']
      if 'DistanceCoefficient' in self.doc:
        TheConfig['ProfileStyle']['DistanceCoefficient'] = self.doc['DistanceCoefficient']
      if 'TimeZoneOffset' in self.doc:
        TheConfig['ProfileStyle']['TimeZoneOffset'] = self.doc['TimeZoneOffset']
      if 'SelectedPointsOnly' in self.doc:
        TheConfig['ProfileStyle']['SelectedPointsOnly'] = self.doc['SelectedPointsOnly']

      # After distance coefficient is set
      self.gpxparser.updatePoints()

      if 'MarkerPoints' in self.doc and 'CaptionPoints' in self.doc and 'MarkerColors' in self.doc:
        for i, m in zip(sorted(self.doc['MarkerPoints'] + self.doc['CaptionPoints']), self.doc['MarkerColors']):
          self.wptmodel.setPointStyle([i], gpx.MARKER_COLOR, m)
      if 'MarkerPoints' in self.doc and 'CaptionPoints' in self.doc and 'MarkerStyles' in self.doc:
        for i, m in zip(sorted(self.doc['MarkerPoints'] + self.doc['CaptionPoints']), self.doc['MarkerStyles']):
          self.wptmodel.setPointStyle([i], gpx.MARKER_STYLE, m)
      if 'MarkerPoints' in self.doc and 'CaptionPoints' in self.doc and 'MarkerSizes' in self.doc:
        for i, m in zip(sorted(self.doc['MarkerPoints'] + self.doc['CaptionPoints']), self.doc['MarkerSizes']):
          self.wptmodel.setPointStyle([i], gpx.MARKER_SIZE, m)

      if 'SplitLines' in self.doc and 'SplitLineColors' in self.doc:
        for i, m in zip(self.doc['SplitLines'], self.doc['SplitLineColors']):
          self.wptmodel.setPointStyle([i], gpx.LINE_COLOR, m)
      if 'SplitLines' in self.doc and 'SplitLineStyles' in self.doc:
        for i, m in zip(self.doc['SplitLines'], self.doc['SplitLineStyles']):
          self.wptmodel.setPointStyle([i], gpx.LINE_STYLE, m)
      if 'SplitLines' in self.doc and 'SplitLineWidths' in self.doc:
        for i, m in zip(self.doc['SplitLines'], self.doc['SplitLineWidths']):
          self.wptmodel.setPointStyle([i], gpx.LINE_WIDTH, m)

      if 'CaptionPoints' in self.doc and 'CaptionPositionXs' in self.doc:
        for i, m in zip(self.doc['CaptionPoints'], self.doc['CaptionPositionXs']):
          self.wptmodel.setPointStyle([i], gpx.CAPTION_POSX, m)
      if 'CaptionPoints' in self.doc and 'CaptionPositionYs' in self.doc:
        for i, m in zip(self.doc['CaptionPoints'], self.doc['CaptionPositionYs']):
          self.wptmodel.setPointStyle([i], gpx.CAPTION_POSY, m)
      if 'CaptionPoints' in self.doc and 'CaptionSizes' in self.doc:
        for i, m in zip(self.doc['CaptionPoints'], self.doc['CaptionSizes']):
          self.wptmodel.setPointStyle([i], gpx.CAPTION_SIZE, m)

      if 'ChangedNames' in self.doc and 'PointNames' in self.doc:
        for i, n in zip(self.doc['ChangedNames'], self.doc['PointNames']):
          self.wptmodel.setData(self.wptmodel.index(i, gpx.NAME), n, QtCore.Qt.EditRole)
    else:  # GPXMAGICK not in cfg
      raise gpx.GpxWarning(QtCore.QCoreApplication.translate('GpxDocument', 'This file in not a valid GPX Viewer project file.'))

  fileNotFound = QtCore.pyqtSignal(str)


TheDocument = GpxDocument()
