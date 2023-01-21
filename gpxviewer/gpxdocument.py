# gpxviewer
#
# Copyright (C) 2016-2023 Sergey Salnikov <salsergey@gmail.com>
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
import shutil
from tempfile import mkdtemp
import zipfile
from PyQt5.QtCore import Qt, QCoreApplication, QFileInfo, QObject, pyqtSignal
import gpxviewer.gpxmodel as gpx
from gpxviewer.configstore import GpxConfigParser, TheConfig


__all__ = ['TheDocument', 'TYPE_GPXV', 'TYPE_GPXZ']


GPXMAGICK = '9e27ea8e'
FORMAT_VERSION = 2
TYPE_GPXV, TYPE_GPXZ = range(2)


class GpxDocument(QObject):
  def __init__(self, parent=None):
    super(GpxDocument, self).__init__(parent)
    self.gpxparser = gpx.GpxParser()
    self.wptmodel = self.gpxparser.wptmodel
    self.trkmodel = self.gpxparser.trkmodel
    self.tmpdir = mkdtemp(prefix='gpxviewer_tmpdir.')
    self.projectType = TYPE_GPXV
    self.doc = {'GPXFile': []}

  def close(self):
    shutil.rmtree(self.tmpdir)

  def saveFile(self, filename):
    self.doc['FormatVersion'] = FORMAT_VERSION

    # Number of points/tracks to check the validity of the files
    self.doc['NumberOfPoints'] = self.wptmodel.rowCount()
    self.doc['NumberOfTracks'] = self.trkmodel.rowCount()

    self.doc['SkipPoints'] = self.wptmodel.getSkippedPoints()
    self.doc['MarkerPoints'] = self.wptmodel.getMarkedPoints()
    self.doc['CaptionPoints'] = self.wptmodel.getCaptionedPoints()
    self.doc['SplitLines'] = self.wptmodel.getSplitLines()
    self.doc['NeglectDistances'] = self.wptmodel.getNeglectStates()
    self.doc['SkipTracks'] = self.trkmodel.getSkippedTracks()

    self.doc.update(TheConfig['ProfileStyle'])

    self.doc['MarkerColors'] = self.wptmodel.getPointStyles(gpx.MARKER_COLOR)
    self.doc['MarkerStyles'] = self.wptmodel.getPointStyles(gpx.MARKER_STYLE)
    self.doc['MarkerSizes'] = self.wptmodel.getPointStyles(gpx.MARKER_SIZE)

    self.doc['SplitLineColors'] = self.wptmodel.getPointStyles(gpx.LINE_COLOR)
    self.doc['SplitLineStyles'] = self.wptmodel.getPointStyles(gpx.LINE_STYLE)
    self.doc['SplitLineWidths'] = self.wptmodel.getPointStyles(gpx.LINE_WIDTH)

    self.doc['CaptionPositionXs'] = self.wptmodel.getPointStyles(gpx.CAPTION_POSX)
    self.doc['CaptionPositionYs'] = self.wptmodel.getPointStyles(gpx.CAPTION_POSY)
    self.doc['CaptionRotation'] = self.wptmodel.getPointStyles(gpx.CAPTION_ROTATION)
    self.doc['CaptionSizes'] = self.wptmodel.getPointStyles(gpx.CAPTION_SIZE)

    self.doc['ChangedNames'] = list(self.wptmodel.changedNames.keys())
    self.doc['PointNames'] = list(self.wptmodel.changedNames.values())

    self.doc['ChangedAltitudes'] = list(self.wptmodel.changedAltitudes.keys())
    self.doc['PointAltitudes'] = list(self.wptmodel.changedAltitudes.values())

    self.doc['ChangedTrackAltitudes'] = list(self.trkmodel.changedAltitudes.keys())
    self.doc['TrackAltitudes'] = self.trkmodel.getChangedAltitudes()

    cfg = GpxConfigParser()

    if self.projectType == TYPE_GPXV:
      # Check if we want to extract some GPX files
      self.doExtractFiles = False
      if any([QFileInfo(gpxfile).isRelative() for gpxfile in self.doc['GPXFile']]):
        self.askToExtractFiles.emit([gpxfile for gpxfile in self.doc['GPXFile'] if QFileInfo(gpxfile).isRelative()])

      for i, gpxfile in enumerate(self.doc['GPXFile']):
        if QFileInfo(gpxfile).isRelative() and self.doExtractFiles:
          newgpxfile = os.path.join(QFileInfo(filename).path(), gpxfile)
          shutil.copy(os.path.join(self.tmpdir, gpxfile), newgpxfile)
          self.doc['GPXFile'][i] = newgpxfile

      cfg.read_dict({GPXMAGICK: self.doc})
      with open(filename, 'w', encoding='utf-8') as file:
        cfg.write(file)

    else:  # TYPE_GPXZ
      with zipfile.ZipFile(filename, mode='w', compression=zipfile.ZIP_DEFLATED) as archive:
        for gpxfile in self.doc['GPXFile']:
          if QFileInfo(gpxfile).isRelative():  # make absolute path
            gpxfile = os.path.join(self.tmpdir, gpxfile)
          archive.write(gpxfile, arcname=QFileInfo(gpxfile).fileName())

        # Make all paths relative
        self.doc['GPXFile'] = [QFileInfo(gpxfile).fileName() for gpxfile in self.doc['GPXFile']]
        cfg.read_dict({GPXMAGICK: self.doc})
        with open(os.path.join(self.tmpdir, 'doc.gpxv'), 'w', encoding='utf-8') as file:
          cfg.write(file)
          file.flush()
          archive.write(file.name, arcname='doc.gpxv')

  def openFile(self, filename):
    if not QFileInfo(filename).isFile():
      raise gpx.GpxWarning(QFileInfo(filename).absoluteFilePath() + QCoreApplication.translate('GpxDocument', ' is not a file.'))

    cfg = GpxConfigParser()
    curFileName = filename

    if filename.lower().endswith('.gpxv'):
      self.projectType = TYPE_GPXV
    else:
      try:
        tmpfile = os.path.join(self.tmpdir, 'doc.gpxv')
        # We should remove older version of doc.gpxv
        if QFileInfo(tmpfile).exists():
          os.remove(tmpfile)
        with zipfile.ZipFile(filename, mode='r', compression=zipfile.ZIP_DEFLATED) as archive:
          archive.extractall(self.tmpdir)
          curFileName = tmpfile
          if not QFileInfo(curFileName).exists():
            raise gpx.GpxWarning(QFileInfo(filename).absoluteFilePath() + QCoreApplication.translate('GpxDocument', ' is not a valid GPX Viewer archive.'))
        self.projectType = TYPE_GPXZ
      except zipfile.BadZipFile:  # filename is not a ZIP archive
        self.projectType = TYPE_GPXV

    try:
      cfg.read(curFileName, encoding='utf-8')
    except (configparser.ParsingError, UnicodeDecodeError):
      raise gpx.GpxWarning(QFileInfo(filename).absoluteFilePath() + QCoreApplication.translate('GpxDocument', ' is not a valid GPX Viewer project.'))

    if GPXMAGICK in cfg:
      self.doc.clear()
      self.doc.update(cfg.items(GPXMAGICK))
      # Determine format version (was not stored for version 1)
      formatVersion = 1
      if 'FormatVersion' in self.doc:
        formatVersion = self.doc['FormatVersion']

      self.gpxparser.resetModels()
      # Fix to handle legacy files
      if type(self.doc['GPXFile']) == str:
        self.doc['GPXFile'] = [self.doc['GPXFile']]

      self.applyToAll = False
      for i, file in enumerate(self.doc['GPXFile']):
        if self.projectType == TYPE_GPXV:
          if not QFileInfo(file).exists():
            self.newFilePath = ''
            self.fileNotFound.emit(file)
            if self.newFilePath != '':
              self.doc['GPXFile'][i] = self.newFilePath
              file = self.newFilePath
              if self.applyToAll:
                for j in range(i + 1, len(self.doc['GPXFile'])):
                  self.doc['GPXFile'][j] = self.doc['GPXFile'][j].replace(QFileInfo(self.doc['GPXFile'][j]).path(), QFileInfo(self.newFilePath).path())
            else:
              raise gpx.GpxWarning(QCoreApplication.translate('GpxDocument', 'One of GPX files doesn\'t exist. This project can\'t be opened.'))
          self.gpxparser.parse(file)
        else:  # TYPE_GPXZ
          self.gpxparser.parse(os.path.join(self.tmpdir, file))

      if ('NumberOfPoints' in self.doc and self.wptmodel.rowCount() != int(self.doc['NumberOfPoints'])) or \
         ('NumberOfTracks' in self.doc and self.trkmodel.rowCount() != int(self.doc['NumberOfTracks'])):
        raise gpx.GpxWarning(QCoreApplication.translate('GpxDocument', 'One of the files has wrong number of valid waypoints or tracks. This file is likely to be damaged or changed from outside.'))

      if 'SkipPoints' in self.doc:
        self.wptmodel.setIncludeStates(self.doc['SkipPoints'], False, False)
      if 'MarkerPoints' in self.doc:
        self.wptmodel.setMarkerStates(self.doc['MarkerPoints'], True)
      if 'CaptionPoints' in self.doc:
        self.wptmodel.setCaptionStates(self.doc['CaptionPoints'], True)
        # Handle old version, where all captioned points had markers too.
        if formatVersion == 1:
          self.wptmodel.setMarkerStates(self.doc['CaptionPoints'], True)
      if 'SplitLines' in self.doc:
        self.wptmodel.setSplitLines(self.doc['SplitLines'], True)
      if 'NeglectDistances' in self.doc:
        self.wptmodel.setNeglectStates(self.doc['NeglectDistances'], True, False)
      if 'SkipTracks' in self.doc:
        self.trkmodel.setIncludeStates(self.doc['SkipTracks'], False, False)

      for option in TheConfig['ProfileStyle'].keys():
        if option in self.doc:
          TheConfig['ProfileStyle'][option] = self.doc[option]

      # After distance coefficient is set
      self.gpxparser.updatePoints()

      # Handle old version, where all captioned points had markers too.
      if formatVersion == 1:
        if 'MarkerPoints' in self.doc and 'CaptionPoints' in self.doc and 'MarkerColors' in self.doc:
          for i, m in zip(sorted(self.doc['MarkerPoints'] + self.doc['CaptionPoints']), self.doc['MarkerColors']):
            self.wptmodel.setPointStyle([i], gpx.MARKER_COLOR, m)
        if 'MarkerPoints' in self.doc and 'CaptionPoints' in self.doc and 'MarkerStyles' in self.doc:
          for i, m in zip(sorted(self.doc['MarkerPoints'] + self.doc['CaptionPoints']), self.doc['MarkerStyles']):
            self.wptmodel.setPointStyle([i], gpx.MARKER_STYLE, m)
        if 'MarkerPoints' in self.doc and 'CaptionPoints' in self.doc and 'MarkerSizes' in self.doc:
          for i, m in zip(sorted(self.doc['MarkerPoints'] + self.doc['CaptionPoints']), self.doc['MarkerSizes']):
            self.wptmodel.setPointStyle([i], gpx.MARKER_SIZE, m)
      else:
        if 'MarkerPoints' in self.doc and 'MarkerColors' in self.doc:
          for i, m in zip(self.doc['MarkerPoints'], self.doc['MarkerColors']):
            self.wptmodel.setPointStyle([i], gpx.MARKER_COLOR, m)
        if 'MarkerPoints' in self.doc and 'MarkerStyles' in self.doc:
          for i, m in zip(self.doc['MarkerPoints'], self.doc['MarkerStyles']):
            self.wptmodel.setPointStyle([i], gpx.MARKER_STYLE, m)
        if 'MarkerPoints' in self.doc and 'MarkerSizes' in self.doc:
          for i, m in zip(self.doc['MarkerPoints'], self.doc['MarkerSizes']):
            self.wptmodel.setPointStyle([i], gpx.MARKER_SIZE, m)

      if 'CaptionPoints' in self.doc and 'CaptionPositionXs' in self.doc:
        for i, m in zip(self.doc['CaptionPoints'], self.doc['CaptionPositionXs']):
          self.wptmodel.setPointStyle([i], gpx.CAPTION_POSX, m)
      if 'CaptionPoints' in self.doc and 'CaptionPositionYs' in self.doc:
        for i, m in zip(self.doc['CaptionPoints'], self.doc['CaptionPositionYs']):
          self.wptmodel.setPointStyle([i], gpx.CAPTION_POSY, m)
      if 'CaptionPoints' in self.doc and 'CaptionRotation' in self.doc:
        for i, m in zip(self.doc['CaptionPoints'], self.doc['CaptionRotation']):
          self.wptmodel.setPointStyle([i], gpx.CAPTION_ROTATION, m)
      if 'CaptionPoints' in self.doc and 'CaptionSizes' in self.doc:
        for i, m in zip(self.doc['CaptionPoints'], self.doc['CaptionSizes']):
          self.wptmodel.setPointStyle([i], gpx.CAPTION_SIZE, m)

      if 'SplitLines' in self.doc and 'SplitLineColors' in self.doc:
        for i, m in zip(self.doc['SplitLines'], self.doc['SplitLineColors']):
          self.wptmodel.setPointStyle([i], gpx.LINE_COLOR, m)
      if 'SplitLines' in self.doc and 'SplitLineStyles' in self.doc:
        for i, m in zip(self.doc['SplitLines'], self.doc['SplitLineStyles']):
          self.wptmodel.setPointStyle([i], gpx.LINE_STYLE, m)
      if 'SplitLines' in self.doc and 'SplitLineWidths' in self.doc:
        for i, m in zip(self.doc['SplitLines'], self.doc['SplitLineWidths']):
          self.wptmodel.setPointStyle([i], gpx.LINE_WIDTH, m)

      if 'ChangedNames' in self.doc and 'PointNames' in self.doc:
        for i, n in zip(self.doc['ChangedNames'], self.doc['PointNames']):
          self.wptmodel.setData(self.wptmodel.index(i, gpx.NAME), n, Qt.ItemDataRole.EditRole)
      if 'ChangedAltitudes' in self.doc and 'PointAltitudes' in self.doc:
        self.wptmodel.setAltitudes(self.doc['ChangedAltitudes'], self.doc['PointAltitudes'])

      if 'ChangedTrackAltitudes' in self.doc and 'TrackAltitudes' in self.doc:
        self.trkmodel.setTracksAltitudes(self.doc['ChangedTrackAltitudes'], self.doc['TrackAltitudes'])
    else:  # GPXMAGICK not in cfg
      raise gpx.GpxWarning(QFileInfo(filename).absoluteFilePath() + QCoreApplication.translate('GpxDocument', ' is not a valid GPX Viewer project.'))

  fileNotFound = pyqtSignal(str)
  askToExtractFiles = pyqtSignal(list)


TheDocument = GpxDocument()
