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

from datetime import datetime, timedelta
from lxml import etree
from math import acos, cos, modf, pi, sin, sqrt
import re
from PyQt5.QtCore import Qt, QAbstractTableModel, QFileInfo, QModelIndex, QObject, QPointF, QSortFilterProxyModel, pyqtSignal
from PyQt5.QtGui import QColor, QFont, QGuiApplication, QPainter, QPainterPath, QPen, QPixmap, QPolygonF
from gpxviewer.configstore import TheConfig


WPTFIELDS = NAME, LAT, LON, ALT, DIST, TIME, TIME_DELTA, TIME_DAYS, DIST_DELTA, ALT_DELTA, SPEED, ALT_SPEED, SLOPE = range(13)
TRKFIELDS = TRKNAME, TRKSEGS, TRKPTS, TRKLEN, TRKALTGAIN, TRKALTDROP, TRKTIME, TRKDUR = range(8)
ValueRole, IDRole, IncludeRole, MarkerRole, CaptionRole, SplitLineRole, NeglectRole,\
  MarkerStyleRole, CaptionStyleRole, SplitLineStyleRole = range(Qt.ItemDataRole.UserRole, Qt.ItemDataRole.UserRole + 10)
MARKER_COLOR, MARKER_STYLE, MARKER_SIZE,\
  CAPTION_POSX, CAPTION_POSY, CAPTION_ROTATION, CAPTION_SIZE, CAPTION_BOLD, CAPTION_ITALIC,\
  LINE_COLOR, LINE_STYLE, LINE_WIDTH = \
  ('MarkerColor', 'MarkerStyle', 'MarkerSize',
   'CaptionPositionX', 'CaptionPositionY', 'CaptionRotation', 'CaptionSize', 'CaptionBold', 'CaptionItalic',
   'SplitLineColor', 'SplitLineStyle', 'SplitLineWidth')


class GpxWarning(Exception):
  def __init__(self, value):
    super(GpxWarning, self).__init__(value)


class WptModel(QAbstractTableModel):
  def __init__(self, parent=None):
    super(WptModel, self).__init__(parent)

    # Workaround to init columns to copy for the first time
    if len(TheConfig.columnsToCopy) == 0:
      TheConfig.columnsToCopy = list(WPTFIELDS)

    self.fields = [self.tr('Name'), self.tr('Latitude'), self.tr('Longitude'), self.tr('Altitude (m)'),
                   self.tr('Distance (km)'), self.tr('Time'), self.tr('Time difference'), self.tr('Time in days'),
                   self.tr('Distance difference (km)'), self.tr('Altitude difference (m)'),
                   self.tr('Speed (km/h)'), self.tr('Climbing speed (m/h)'), self.tr('Slope (m/km)')]
    self.resetModel()
    self.pix = QPixmap(16, 16)
    self.pix.fill(Qt.GlobalColor.transparent)

    # Define colors that should look well for any color theme
    lightness = max(50, min(240, QGuiApplication.palette().base().color().lightness()))
    self.SkipColor = QColor.fromHsl(0, lightness, lightness)
    self.MarkerColor = QColor.fromHsl(240, lightness, lightness)
    self.CaptionColor = QColor.fromHsl(120, lightness, lightness)

  def rowCount(self, parent=None):
    if parent is not None and parent.isValid():
      return 0
    else:
      return len(self.waypoints)

  def columnCount(self, parent=None):
    if parent is not None and parent.isValid():
      return 0
    else:
      return len(self.fields)

  def data(self, index, role=Qt.ItemDataRole.DisplayRole):
    if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
      if index.column() == NAME and index.row() in self.changedNames:
        return self.changedNames[index.row()]
      elif index.column() == TIME and self.waypoints[index.row()][index.column()] != '':
        return str(self.waypoints[index.row()][index.column()] + timedelta(minutes=TheConfig.getValue('ProfileStyle', 'TimeZoneOffset')))
      elif index.column() in {LAT, LON}:
        if TheConfig.getValue('ProfileStyle', 'CoordinateFormat') == 0:  # Decimal degrees
          return str(round(self.waypoints[index.row()][index.column()], 6))
        elif TheConfig.getValue('ProfileStyle', 'CoordinateFormat') == 1:  # Degrees with decimal minutes
          mins, degs = modf(self.waypoints[index.row()][index.column()])
          mins = round(mins * 60, 4)
          return str(int(degs)) + '° ' + str(mins) + '\''
        else:  # Degrees, minutes, seconds
          mins, degs = modf(self.waypoints[index.row()][index.column()])
          mins = mins * 60
          sec, mins = modf(mins)
          sec = round(sec * 60, 2)
          return str(int(degs)) + '°' + str(int(mins)) + '\'' + str(sec) + '"'
      elif index.column() == ALT and index.row() in self.changedAltitudes:
        return str(self.changedAltitudes[index.row()])
      elif index.column() in {ALT, ALT_DELTA, ALT_SPEED, SLOPE} and self.waypoints[index.row()][index.column()] != '':
        return str(round(self.waypoints[index.row()][index.column()]))
      elif index.column() in {DIST, TIME_DAYS, DIST_DELTA, SPEED} and self.waypoints[index.row()][index.column()] != '':
        return str(round(self.waypoints[index.row()][index.column()], 3))
      else:
        return str(self.waypoints[index.row()][index.column()])
    elif role == Qt.ItemDataRole.DecorationRole and index.column() == NAME:
      if index.data(MarkerRole) and index.data(IncludeRole):
        return _markerIcon(index.data(MarkerStyleRole)[MARKER_STYLE], index.data(MarkerStyleRole)[MARKER_COLOR])
      else:
        return self.pix
    elif role == ValueRole:
      return self.waypoints[index.row()][index.column()]
    elif role == IDRole:
      return self.waypoints[index.row()]['ID']
    elif role == IncludeRole:
      return self.includeStates[index.row()]
    elif role == MarkerRole:
      return self.markerStates[index.row()]
    elif role == CaptionRole:
      return self.captionStates[index.row()]
    elif role == SplitLineRole:
      return self.splitStates[index.row()]
    elif role == NeglectRole:
      return self.neglectStates[index.row()]
    elif role == MarkerStyleRole:
      if all([k in self.pointStyles[index.row()] for k in {MARKER_COLOR, MARKER_STYLE, MARKER_SIZE}]):
        return {k: self.pointStyles[index.row()][k] for k in {MARKER_COLOR, MARKER_STYLE, MARKER_SIZE}}
      else:
        return {k: TheConfig.getValue('PointStyle', k) for k in {MARKER_COLOR, MARKER_STYLE, MARKER_SIZE}}
    elif role == CaptionStyleRole:
      if all([k in self.pointStyles[index.row()] for k in {CAPTION_POSX, CAPTION_POSY, CAPTION_ROTATION, CAPTION_SIZE, CAPTION_BOLD, CAPTION_ITALIC}]):
        return {k: self.pointStyles[index.row()][k] for k in {CAPTION_POSX, CAPTION_POSY, CAPTION_ROTATION, CAPTION_SIZE, CAPTION_BOLD, CAPTION_ITALIC}}
      else:
        return {k: TheConfig.getValue('PointStyle', k) for k in {CAPTION_POSX, CAPTION_POSY, CAPTION_ROTATION, CAPTION_SIZE, CAPTION_BOLD, CAPTION_ITALIC}}
    elif role == SplitLineStyleRole:
      if all([k in self.pointStyles[index.row()] for k in {LINE_COLOR, LINE_STYLE, LINE_WIDTH}]):
        return {k: self.pointStyles[index.row()][k] for k in {LINE_COLOR, LINE_STYLE, LINE_WIDTH}}
      else:
        return {k: TheConfig.getValue('PointStyle', k) for k in {LINE_COLOR, LINE_STYLE, LINE_WIDTH}}
    elif role == Qt.ItemDataRole.BackgroundRole:
      if not self.includeStates[index.row()]:
        return self.SkipColor
      elif self.captionStates[index.row()]:
        return self.CaptionColor
      elif self.markerStates[index.row()]:
        return self.MarkerColor
      else:
        return Qt.GlobalColor.transparent
    elif role == Qt.ItemDataRole.FontRole:
      font = QFont()
      if self.splitStates[index.row()]:
        font.setBold(True)
      if self.neglectStates[index.row()]:
        font.setItalic(True)
      return font
    return None

  def setData(self, index, value, role):
    if index.isValid() and role == Qt.ItemDataRole.EditRole and index.column() == NAME and value != self.waypoints[index.row()][NAME]:
      self.changedNames[index.row()] = value
      self.dataChanged.emit(index, index)
      self.wptDataChanged.emit()
      return True
    else:
      return False

  def flags(self, index):
    if index.column() == NAME:
      return super(WptModel, self).flags(index) | Qt.ItemFlag.ItemIsEditable
    else:
      return super(WptModel, self).flags(index)

  def headerData(self, section, orientation, role):
    if role == Qt.ItemDataRole.DisplayRole:
      return self.fields[section] if orientation == Qt.Orientation.Horizontal else section + 1
    return None

  def parent(self, index=None):
    if index is not None:
      return QModelIndex()
    else:
      return super(WptModel, self).parent()

  def copyToClipboard(self, IDs):
    if len(IDs) > 0:
      text = ''
      for i in IDs:
        text += '\t'.join([self.index(i, f).data() for f in TheConfig.columnsToCopy]) + '\n'
      QGuiApplication.clipboard().setText(text)

  def getSkippedPoints(self):
    return [i for i, s in enumerate(self.includeStates) if not s]

  def getMarkedPoints(self):
    return [i for i, s in enumerate(self.markerStates) if s]

  def getCaptionedPoints(self):
    return [i for i, s in enumerate(self.captionStates) if s]

  def getSplitLines(self):
    return [i for i, s in enumerate(self.splitStates) if s]

  def getNeglectStates(self):
    return [i for i, s in enumerate(self.neglectStates) if s]

  def getPointStyles(self, key):
    if key in {MARKER_COLOR, MARKER_STYLE, MARKER_SIZE}:
      return [p[key] for i, p in enumerate(self.pointStyles) if self.markerStates[i]]
    if key in {CAPTION_POSX, CAPTION_POSY, CAPTION_ROTATION, CAPTION_SIZE, CAPTION_BOLD, CAPTION_ITALIC}:
      return [p[key] for i, p in enumerate(self.pointStyles) if self.captionStates[i]]
    if key in {LINE_COLOR, LINE_STYLE, LINE_WIDTH}:
      return [p[key] for i, p in enumerate(self.pointStyles) if self.splitStates[i]]

  def resetModel(self):
    self.beginResetModel()
    self.waypoints = []
    self.includeStates = []
    self.markerStates = []
    self.captionStates = []
    self.splitStates = []
    self.neglectStates = []
    self.pointStyles = []
    self.changedNames = {}
    self.changedAltitudes = {}
    self.endResetModel()

  def setIncludeStates(self, IDs, state, update=True):
    for i in IDs:
      self.includeStates[i] = state
      self.dataChanged.emit(self.index(i, 0), self.index(i, self.columnCount()))
    if update:
      self.parent().updatePoints()
    self.wptDataChanged.emit()

  def setMarkerStates(self, IDs, state):
    for i in IDs:
      self.markerStates[i] = state
      for key in {MARKER_COLOR, MARKER_STYLE, MARKER_SIZE}:
        if key not in self.pointStyles[i]:
          self.pointStyles[i][key] = TheConfig.getValue('PointStyle', key)
      self.dataChanged.emit(self.index(i, 0), self.index(i, self.columnCount()))
    self.wptDataChanged.emit()

  def setCaptionStates(self, IDs, state):
    for i in IDs:
      self.captionStates[i] = state
      for key in {CAPTION_POSX, CAPTION_POSY, CAPTION_ROTATION, CAPTION_SIZE, CAPTION_BOLD, CAPTION_ITALIC}:
        if key not in self.pointStyles[i]:
          self.pointStyles[i][key] = TheConfig.getValue('PointStyle', key)
      self.dataChanged.emit(self.index(i, 0), self.index(i, self.columnCount()))
    self.wptDataChanged.emit()

  def setSplitLines(self, IDs, state):
    for i in IDs:
      self.splitStates[i] = state
      for key in {LINE_COLOR, LINE_STYLE, LINE_WIDTH}:
        if key not in self.pointStyles[i]:
          self.pointStyles[i][key] = TheConfig.getValue('PointStyle', key)
      self.dataChanged.emit(self.index(i, 0), self.index(i, self.columnCount()))
    self.wptDataChanged.emit()

  def setNeglectStates(self, IDs, state, update=True):
    for i in IDs:
      self.neglectStates[i] = state
      self.dataChanged.emit(self.index(i, 0), self.index(i, self.columnCount()))
    if update:
      self.parent().updateDistance()
    self.wptDataChanged.emit()

  def setPointStyle(self, IDs, key, value):
    for i in IDs:
      self.pointStyles[i][key] = value
    self.wptDataChanged.emit()

  def resetNames(self, IDs):
    for i in IDs:
      if i in self.changedNames:
        del self.changedNames[i]
        self.dataChanged.emit(self.index(i, NAME), self.index(i, NAME))
    self.wptDataChanged.emit()

  def setAltitudes(self, IDs, alts):
    for i, a in zip(IDs, alts):
      self.changedAltitudes[i] = a
      self.parent().updateMinMaxAltitudes(a)
      self.dataChanged.emit(self.index(i, ALT), self.index(i, SLOPE))

    self.parent().updateDetailedData()
    self.wptDataChanged.emit()

  def resetAltitudes(self, IDs):
    for i in IDs:
      if i in self.changedAltitudes:
        del self.changedAltitudes[i]
        self.parent().updateMinMaxAltitudes(self.waypoints[i][ALT])
        self.dataChanged.emit(self.index(i, ALT), self.index(i, SLOPE))

    self.parent().updateDetailedData()
    self.wptDataChanged.emit()

  wptDataChanged = pyqtSignal()


class TrkModel(QAbstractTableModel):
  def __init__(self, parent=None):
    super(TrkModel, self).__init__(parent)
    self.fields = [self.tr('Name'), self.tr('Segments'), self.tr('Points'), self.tr('Length (km)'),
                   self.tr('Altitude gain (m)'), self.tr('Altitude drop (m)'), self.tr('Start time'), self.tr('Duration')]
    self.resetModel()

    # Define colors that should look well for any color theme
    lightness = max(50, min(240, QGuiApplication.palette().base().color().lightness()))
    self.SkipColor = QColor.fromHsl(0, lightness, lightness)

  def rowCount(self, parent=None):
    if parent is not None and parent.isValid():
      return 0
    else:
      return len(self.tracks)

  def columnCount(self, parent=None):
    if parent is not None and parent.isValid():
      return 0
    else:
      return len(self.fields)

  def data(self, index, role=Qt.ItemDataRole.DisplayRole):
    if role == Qt.ItemDataRole.DisplayRole:
      if index.column() == TRKTIME and self.tracks[index.row()][index.column()] != '':
        return str(self.tracks[index.row()][index.column()] + timedelta(minutes=TheConfig.getValue('ProfileStyle', 'TimeZoneOffset')))
      elif index.column() in {TRKALTGAIN, TRKALTDROP}:
        return str(round(self.tracks[index.row()][index.column()]))
      elif index.column() == TRKLEN:
        return str(round(self.tracks[index.row()][index.column()], 3))
      else:
        return str(self.tracks[index.row()][index.column()])
    elif role == IncludeRole:
      return self.includeStates[index.row()]
    elif role == Qt.ItemDataRole.BackgroundRole:
      return QGuiApplication.palette().base().color() if self.includeStates[index.row()] else self.SkipColor
    return None

  def getPointData(self, track, segment, index, column):
    if column == ALT and track in self.changedAltitudes:
      return self.changedAltitudes[track][(segment, index)]
    else:
      return self.tracks[track]['SEGMENTS'][segment][index][column]

  def headerData(self, section, orientation, role):
    if role == Qt.ItemDataRole.DisplayRole:
      return self.fields[section] if orientation == Qt.Orientation.Horizontal else section + 1
    return None

  def copyToClipboard(self, IDs):
    text = ''
    for i in IDs:
      text += '\t'.join([self.index(i, f).data() for f in TRKFIELDS]) + '\n'
    QGuiApplication.clipboard().setText(text)

  def getSkippedTracks(self):
    return [i for i, s in enumerate(self.includeStates) if not s]

  def getChangedAltitudes(self):
    return [v[(s, i)] for t, v in self.changedAltitudes.items() for s, seg in enumerate(self.tracks[t]['SEGMENTS']) for i in range(len(seg))]

  def resetModel(self):
    self.beginResetModel()
    self.tracks = []
    self.includeStates = []
    self.changedAltitudes = {}
    self.endResetModel()

  def setIncludeStates(self, IDs, state, update=True):
    for i in IDs:
      self.includeStates[i] = state
      self.dataChanged.emit(self.index(i, 0), self.index(i, self.columnCount()))
    if update:
      self.parent().updatePoints()

  def setTracksAltitudes(self, tracks, alts):
    n = 0
    for tnum, track in enumerate(tracks):
      self.changedAltitudes[track] = {}
      for s, seg in enumerate(self.tracks[track]['SEGMENTS']):
        for i in range(len(seg)):
          self.changedAltitudes[track][(s, i)] = alts[n]
          n += 1

      self.updateAltitudeGainDrop(tnum)

  def setPointsAltitudes(self, track, segment, IDs, alts):
    if track not in self.changedAltitudes:
      self.changedAltitudes[track] = {}
    for i, a in zip(IDs, alts):
      self.changedAltitudes[track][(segment, i)] = a
      self.parent().updateMinMaxAltitudes(a)

    # Update only if all data is downloaded
    if len(self.changedAltitudes[track]) == self.tracks[track][TRKPTS]:
      self.updateAltitudeGainDrop(track)
      self.dataChanged.emit(self.index(track, TRKALTGAIN), self.index(track, TRKALTDROP))
    self.trkDataChanged.emit()

  def resetAltitudes(self, tracks):
    for t in tracks:
      if t in self.changedAltitudes:
        del self.changedAltitudes[t]
      self.updateAltitudeGainDrop(t)
      self.dataChanged.emit(self.index(t, TRKALTGAIN), self.index(t, TRKALTDROP))

    self.trkDataChanged.emit()

  def updateAltitudeGainDrop(self, track):
    gain = 0
    drop = 0
    for snum, seg in enumerate(self.tracks[track]['SEGMENTS']):
      prev_alt = None
      for p in range(len(seg)):
        if prev_alt is not None:
          delta = self.getPointData(track, snum, p, ALT) - prev_alt
          if delta >= 0:
            gain += delta
          else:
            drop += delta
        prev_alt = self.getPointData(track, snum, p, ALT)

    self.tracks[track][TRKALTGAIN] = gain
    self.tracks[track][TRKALTDROP] = drop

  trkDataChanged = pyqtSignal()


class GpxParser(QObject):
  def __init__(self, parent=None):
    super(GpxParser, self).__init__(parent)
    self.wptmodel = WptModel(self)
    self.trkmodel = TrkModel(self)
    self.resetModels()

  def resetModels(self):
    self.wptmodel.resetModel()
    self.trkmodel.resetModel()
    self.points = []
    self.minalt = 10000
    self.maxalt = -10000

  def parse(self, filename):
    try:
      doc = etree.parse(filename)
    except (etree.ParseError, IsADirectoryError, FileNotFoundError):
      raise GpxWarning(QFileInfo(filename).absoluteFilePath() + self.tr(' is an invalid file.'))

    self.ns = doc.getroot().nsmap
    self.ns['ns'] = self.ns[None]

    if filename.lower().endswith('.kml'):
      self.parseKMLDocument(doc.getroot().find('{%(ns)s}Document' % self.ns))
    else:
      self.parseGPXDocument(doc.getroot())

    self.updateMinMaxAltitudes()

  def parseGPXDocument(self, root):
    tag = 'name'
    if TheConfig.getValue('ProfileStyle', 'ReadNameFromTag') == 1:  # Comment
      tag = 'cmt'
    elif TheConfig.getValue('ProfileStyle', 'ReadNameFromTag') == 2:  # Description
      tag = 'desc'
    name = None

    for p in root.iterfind('{%(ns)s}wpt' % self.ns):
      try:
        name = p.findtext(('{%(ns)s}' + tag) % self.ns)
        ele = p.findtext('{%(ns)s}ele' % self.ns)
        time = p.findtext('{%(ns)s}time' % self.ns)

        point = {
          NAME: name.strip() if name is not None else '',
          LAT: float(p.get('lat')),
          LON: float(p.get('lon')),
          ALT: float(ele) if ele is not None else 0,
          TIME: datetime.fromisoformat(time[0:-1]).replace(microsecond=0) if time is not None else '',
          # Additional fields
          'CMT': p.findtext('{%(ns)s}cmt' % self.ns),
          'DESC': p.findtext('{%(ns)s}desc' % self.ns),
          'SYM': p.findtext('{%(ns)s}sym' % self.ns),
        }

        self.addPointToModel(point)

      except (TypeError, ValueError):
        self.warningSent.emit(self.tr('File read error'),
                              self.tr('Waypoint ') + (name + ' ' if name is not None else '') +
                              self.tr('is invalid and will be skipped.', 'Waypoint'))

    for t in root.iterfind('{%(ns)s}trk' % self.ns):
      try:
        name = t.findtext('{%(ns)s}name' % self.ns)
        track = {TRKNAME: name.strip() if name is not None else ''}

        pts = 0
        dist = 0.0
        track['SEGMENTS'] = []
        for s in t.iterfind('{%(ns)s}trkseg' % self.ns):
          prev_lat = None
          prev_lon = None
          segment = []
          for p in s.iterfind('{%(ns)s}trkpt' % self.ns):
            ele = p.findtext('{%(ns)s}ele' % self.ns)
            time = p.findtext('{%(ns)s}time' % self.ns)
            point = {
              LAT: float(p.get('lat')),
              LON: float(p.get('lon')),
              ALT: float(ele) if ele is not None else 0,
              TIME: datetime.fromisoformat(time[0:-1]) if time is not None else '',
            }
            self.minalt = min(self.minalt, point[ALT])
            self.maxalt = max(self.maxalt, point[ALT])

            if prev_lat is not None and prev_lon is not None:
              dist += _distance(point[LAT], point[LON], prev_lat, prev_lon)
            prev_lat, prev_lon = point[LAT], point[LON]

            segment += [point]
            pts += 1

          track['SEGMENTS'] += [segment]

        track[TRKPTS] = pts
        track['LENGTH'] = dist
        self.addTrackToModel(track)

      except (TypeError, ValueError):
        self.warningSent.emit(self.tr('File read error'),
                              self.tr('Track ') + (name + ' ' if name is not None else '') +
                              self.tr('is invalid and will be skipped.', 'Track'))

  def parseKMLDocument(self, root):
    tag = 'name'
    if TheConfig.getValue('ProfileStyle', 'ReadNameFromTag') == 2:  # Description
      tag = 'description'
    name = None

    for element in root.iterchildren():
      if element.tag == '{%(ns)s}Folder' % self.ns:
        self.parseKMLDocument(element)

      elif element.tag == '{%(ns)s}Placemark' % self.ns:
        if element.find('{%(ns)s}Point' % self.ns) is not None:  # waypoint
          try:
            name = element.findtext(('{%(ns)s}' + tag) % self.ns)
            time = element.findtext('.//{%(ns)s}when' % self.ns)
            point = {
              NAME: name.strip() if name is not None else '',
              TIME: datetime.fromisoformat(time[0:-1]) if time is not None else '',
              # Additional fields
              'DESC': element.findtext('{%(ns)s}description' % self.ns),
            }
            point[LON], point[LAT], point[ALT] = [float(n) for n in element.findtext('.//{%(ns)s}coordinates' % self.ns).split(',')]

            self.addPointToModel(point)

          except (TypeError, ValueError):
            self.warningSent.emit(self.tr('File read error'),
                                  self.tr('Waypoint ') + (name + ' ' if name is not None else '') +
                                  self.tr('is invalid and will be skipped.', 'Waypoint'))

        elif element.find('{%(gx)s}Track' % self.ns) is not None:  # track
          try:
            name = element.findtext('{%(ns)s}name' % self.ns)
            track = {TRKNAME: name.strip() if name is not None else ''}

            coords = [el.text.split(' ') for el in element.iterfind('.//{%(gx)s}coord' % self.ns)]
            times = [datetime.fromisoformat(el.text[0:19]) for el in element.iterfind('.//{%(ns)s}when' % self.ns)]
            if len(coords) != len(times):
              times = [None] * len(coords)

            prev_lat = None
            prev_lon = None
            dist = 0.0
            segment = []
            for c, t in zip(coords, times):
              point = {
                LON: float(c[0]),
                LAT: float(c[1]),
                ALT: float(c[2]),
                TIME: t if t is not None else ''
              }
              self.minalt = min(self.minalt, point[ALT])
              self.maxalt = max(self.maxalt, point[ALT])

              if prev_lat is not None and prev_lon is not None:
                dist += _distance(point[LAT], point[LON], prev_lat, prev_lon)
              prev_lat, prev_lon = point[LAT], point[LON]

              segment += [point]

            track['SEGMENTS'] = [segment]
            track[TRKPTS] = len(segment)
            track['LENGTH'] = dist
            self.addTrackToModel(track)

          except (TypeError, ValueError):
            self.warningSent.emit(self.tr('File read error'),
                                  self.tr('Track ') + (name + ' ' if name is not None else '') +
                                  self.tr('is invalid and will be skipped.', 'Track'))

        elif element.find('{%(ns)s}LineString' % self.ns) is not None:  # line
          try:
            name = element.findtext('{%(ns)s}name' % self.ns)
            track = {TRKNAME: name.strip() if name is not None else ''}

            coords = element.findtext('.//{%(ns)s}coordinates' % self.ns)
            coords = re.split(r'\s+', coords.strip()) if coords is not None else []
            times = [None] * len(coords)

            prev_lat = None
            prev_lon = None
            dist = 0.0
            segment = []
            for c, t in zip(coords, times):
              point = {TIME: ''}
              point[LON], point[LAT], point[ALT] = [float(n) for n in c.split(',')]
              self.minalt = min(self.minalt, point[ALT])
              self.maxalt = max(self.maxalt, point[ALT])

              if prev_lat is not None and prev_lon is not None:
                dist += _distance(point[LAT], point[LON], prev_lat, prev_lon)
              prev_lat, prev_lon = point[LAT], point[LON]

              segment += [point]

            track['SEGMENTS'] = [segment]
            track[TRKPTS] = len(segment)
            track['LENGTH'] = dist
            self.addTrackToModel(track)

          except (TypeError, ValueError):
            self.warningSent.emit(self.tr('File read error'),
                                  self.tr('Track ') + (name + ' ' if name is not None else '') +
                                  self.tr('is invalid and will be skipped.', 'Track'))

  def addPointToModel(self, point):
    point[DIST] = ''
    point[TIME_DELTA] = ''
    point[TIME_DAYS] = ''
    point[DIST_DELTA] = ''
    point[ALT_DELTA] = ''
    point[SPEED] = ''
    point[ALT_SPEED] = ''
    point[SLOPE] = ''

    wptid = self.wptmodel.rowCount()
    # Sort points by time
    if TheConfig.getValue('ProfileStyle', 'SortByTime') and point[TIME] != '':
      while wptid > 0 and self.wptmodel.waypoints[wptid - 1][TIME] != '' and point[TIME] < self.wptmodel.waypoints[wptid - 1][TIME]:
        wptid -= 1
      for i in range(wptid, self.wptmodel.rowCount()):
        self.wptmodel.waypoints[i]['ID'] += 1
    point['ID'] = wptid

    self.wptmodel.beginInsertRows(QModelIndex(), wptid, wptid)
    self.wptmodel.waypoints.insert(wptid, point)
    self.wptmodel.includeStates.insert(wptid, True)
    self.wptmodel.markerStates.insert(wptid, False)
    self.wptmodel.captionStates.insert(wptid, False)
    self.wptmodel.splitStates.insert(wptid, False)
    self.wptmodel.neglectStates.insert(wptid, False)
    self.wptmodel.pointStyles.insert(wptid, {})
    self.wptmodel.endInsertRows()

    self.minalt = min(self.minalt, point[ALT])
    self.maxalt = max(self.maxalt, point[ALT])

  def addTrackToModel(self, track):
    track[TRKSEGS] = len(track['SEGMENTS'])
    track[TRKLEN] = ''
    track[TRKALTGAIN] = ''
    track[TRKALTDROP] = ''
    if all([p[TIME] != '' for s in track['SEGMENTS'] for p in s]):
      track[TRKTIME] = track['SEGMENTS'][0][0][TIME]
      track[TRKDUR] = track['SEGMENTS'][-1][-1][TIME] - track['SEGMENTS'][0][0][TIME]
    else:
      track[TRKTIME] = ''
      track[TRKDUR] = ''

    trkid = self.trkmodel.rowCount()
    self.trkmodel.beginInsertRows(QModelIndex(), trkid, trkid)
    self.trkmodel.tracks += [track]
    self.trkmodel.includeStates += [True]
    self.trkmodel.updateAltitudeGainDrop(trkid)
    self.trkmodel.endInsertRows()

  def updatePoints(self):
    self.points = []
    includeTracks = True
    for i, p in enumerate(self.wptmodel.waypoints):
      if self.wptmodel.includeStates[i] and p[TIME] == '':
        includeTracks = False

    if self.trkmodel.rowCount() != 0 and includeTracks:
      for tind, track in enumerate(self.trkmodel.tracks):
        if self.trkmodel.includeStates[tind] and \
           (track[TRKTIME] != '' or self.wptmodel.rowCount() == len(self.wptmodel.getSkippedPoints())):
          for sind, segment in enumerate(track['SEGMENTS']):
            self.points += zip([tind] * len(segment), [sind] * len(segment), range(len(segment)))
      ind = 0
      i = 0
      while i < self.wptmodel.rowCount():
        if self.wptmodel.includeStates[i]:
          if ind < len(self.points) and \
             self.wptmodel.waypoints[i][TIME] < \
             self.trkmodel.getPointData(self.points[ind][0], self.points[ind][1], self.points[ind][2], TIME) or \
             ind == len(self.points):
            self.points.insert(ind, i)
            i += 1
          ind += 1
        else:
          i += 1
    else:
      for i, p in enumerate(self.wptmodel.waypoints):
        if self.wptmodel.includeStates[i]:
          self.points += [i]

    self.updateTimeDifference()
    self.updateDistance()

  def updateDistance(self):
    prev_lat = None
    prev_lon = None
    dist = 0.0
    dist_coeff = TheConfig.getValue('ProfileStyle', 'DistanceCoefficient')

    for p in self.points:
      if type(p) == int:
        lat = self.wptmodel.waypoints[p][LAT]
        lon = self.wptmodel.waypoints[p][LON]
        if not self.wptmodel.neglectStates[p] and prev_lat is not None and prev_lon is not None:
          dist += _distance(lat, lon, prev_lat, prev_lon) * dist_coeff
        self.wptmodel.waypoints[p][DIST] = dist
        prev_lat = lat
        prev_lon = lon
      else:
        lat = self.trkmodel.getPointData(p[0], p[1], p[2], LAT)
        lon = self.trkmodel.getPointData(p[0], p[1], p[2], LON)
        if prev_lat is not None and prev_lon is not None:
          dist += _distance(lat, lon, prev_lat, prev_lon) * dist_coeff
        self.trkmodel.tracks[p[0]]['SEGMENTS'][p[1]][p[2]][DIST] = dist
        prev_lat = lat
        prev_lon = lon

    for i in self.wptmodel.getSkippedPoints():
      self.wptmodel.waypoints[i][DIST] = ''

    for t in self.trkmodel.tracks:
      t[TRKLEN] = t['LENGTH'] * dist_coeff

    self.updateDetailedData()

  def updateTimeDifference(self):
    start_dt = None
    for i, p in enumerate(self.wptmodel.waypoints):
      if self.wptmodel.includeStates[i] and p[TIME] != '':
        start_dt = p[TIME]
        break
    for i, track in enumerate(self.trkmodel.tracks):
      if self.trkmodel.includeStates[i] and track[TRKTIME] != '' and (start_dt is None or track[TRKTIME] < start_dt):
        start_dt = track[TRKTIME]
        break

    for i, p in enumerate(self.wptmodel.waypoints):
      if self.wptmodel.includeStates[i] and p[TIME] != '':
        p[TIME_DELTA] = p[TIME] - start_dt
        p[TIME_DAYS] = p[TIME_DELTA].days + p[TIME_DELTA].seconds / 60.0 / 60.0 / 24.0
      else:
        p[TIME_DELTA] = ''
        p[TIME_DAYS] = ''

    for i, track in enumerate(self.trkmodel.tracks):
      if self.trkmodel.includeStates[i]:
        for seg in track['SEGMENTS']:
          for p in seg:
            if p[TIME] != '':
              time_delta = p[TIME] - start_dt
              p[TIME_DAYS] = time_delta.days + time_delta.seconds / 60.0 / 60.0 / 24.0
            else:
              p[TIME_DAYS] = ''

  def updateDetailedData(self):
    if len(self.wptmodel.getSkippedPoints()) == self.wptmodel.rowCount():
      return

    i = 0
    prev = {}
    for i, p in enumerate(self.wptmodel.waypoints):
      if self.wptmodel.includeStates[i]:
        prev = p
        break
      else:
        p[DIST_DELTA] = ''
        p[ALT_DELTA] = ''
        p[SPEED] = ''
        p[ALT_SPEED] = ''
        p[SLOPE] = ''

    prev[DIST_DELTA] = 0.0
    prev[ALT_DELTA] = 0
    prev[SPEED] = 0.0
    prev[ALT_SPEED] = 0.0
    prev[SLOPE] = 0.0

    for j, p in enumerate(self.wptmodel.waypoints[i+1:], i + 1):
      if self.wptmodel.includeStates[j]:
        dt = (p[TIME_DAYS] - prev[TIME_DAYS]) * 24.0 if p[TIME_DAYS] != '' and prev[TIME_DAYS] != '' and prev[TIME_DAYS] != 0 else 0
        p[DIST_DELTA] = p[DIST] - prev[DIST]
        p[ALT_DELTA] = int(self.wptmodel.index(p['ID'], ALT).data()) - int(self.wptmodel.index(prev['ID'], ALT).data())
        p[SPEED] = p[DIST_DELTA] / dt if dt != 0 else 0.0
        p[ALT_SPEED] = p[ALT_DELTA] / dt if dt != 0 else 0.0
        p[SLOPE] = p[ALT_DELTA] / p[DIST_DELTA] if p[DIST_DELTA] != 0 else 0.0
        prev = p
      else:
        p[DIST_DELTA] = ''
        p[ALT_DELTA] = ''
        p[SPEED] = ''
        p[ALT_SPEED] = ''
        p[SLOPE] = ''

  def updateMinMaxAltitudes(self, alt=None):
    if alt is not None:
      self.minalt = min(TheConfig.getValue('ProfileStyle', 'MinimumAltitude'), alt)
      self.maxalt = max(TheConfig.getValue('ProfileStyle', 'MaximumAltitude'), alt)

    TheConfig['ProfileStyle']['MinimumAltitude'] = str(int(round(self.minalt, -3) - 500 if round(self.minalt, -3) > self.minalt
                                                           else round(self.minalt, -3)))
    TheConfig['ProfileStyle']['MaximumAltitude'] = str(int(round(self.maxalt, -3) + 500 if round(self.maxalt, -3) < self.maxalt
                                                           else round(self.maxalt, -3)))

  def writePointToGPX(self, root, point, name=None, ele=None):
    element = etree.SubElement(root, 'wpt', lat=str(point[LAT]), lon=str(point[LON]))
    etree.SubElement(element, 'ele').text = self.wptmodel.index(point['ID'], ALT).data() if ele is None else ele
    self.minlat = min(self.minlat, point[LAT])
    self.minlon = min(self.minlon, point[LON])
    self.maxlat = max(self.maxlat, point[LAT])
    self.maxlon = max(self.maxlon, point[LON])
    if point[TIME] != '':
      etree.SubElement(element, 'time').text = point[TIME].isoformat() + 'Z'
    etree.SubElement(element, 'name').text = self.wptmodel.index(point['ID'], NAME).data() if name is None else name

    if 'CMT' in point and point['CMT'] is not None:
      etree.SubElement(element, 'cmt').text = point['CMT']
    if 'DESC' in point and point['DESC'] is not None:
      etree.SubElement(element, 'desc').text = point['DESC']
    if 'SYM' in point and point['SYM'] is not None:
      etree.SubElement(element, 'sym').text = point['SYM']

  def writePointToGPXTrack(self, root, point, ele):
    element = etree.SubElement(root, 'trkpt', lat=str(point[LAT]), lon=str(point[LON]))
    etree.SubElement(element, 'ele').text = ele
    self.minlat = min(self.minlat, point[LAT])
    self.minlon = min(self.minlon, point[LON])
    self.maxlat = max(self.maxlat, point[LAT])
    self.maxlon = max(self.maxlon, point[LON])
    if point[TIME] != '':
      etree.SubElement(element, 'time').text = point[TIME].isoformat() + 'Z'

  def writeGPXFile(self, filename):
    ns = {None: 'http://www.topografix.com/GPX/1/1'}
    root = etree.Element('gpx', nsmap=ns, version='1.1', creator='GPX Viewer - https://osdn.net/projects/gpxviewer')
    metadata = etree.SubElement(root, 'metadata')

    self.minlat = 90
    self.minlon = 180
    self.maxlat = -90
    self.maxlon = -180

    if not TheConfig.getValue('ProfileStyle', 'DeletePoints'):
      for point, state in zip(self.wptmodel.waypoints, self.wptmodel.includeStates):
        if state:
          self.writePointToGPX(root, point)

    if TheConfig.getValue('ProfileStyle', 'TracksToPoints'):
      num = self.wptmodel.rowCount() - len(self.wptmodel.getSkippedPoints())
      for tnum, state in zip(range(len(self.trkmodel.tracks)), self.trkmodel.includeStates):
        if state:
          for snum, seg in enumerate(self.trkmodel.tracks[tnum]['SEGMENTS']):
            for i, point in enumerate(seg):
              num += 1
              self.writePointToGPX(root, point,
                                   name='WPT{}'.format(num),
                                   ele=str(self.trkmodel.getPointData(tnum, snum, i, ALT)))

    if not TheConfig.getValue('ProfileStyle', 'DeleteTracks'):
      for tnum, state in zip(range(len(self.trkmodel.tracks)), self.trkmodel.includeStates):
        if state:
          elTrk = etree.SubElement(root, 'trk')
          track = self.trkmodel.tracks[tnum]
          etree.SubElement(elTrk, 'name').text = track[TRKNAME]
          for snum, seg in enumerate(track['SEGMENTS']):
            elSeg = etree.SubElement(elTrk, 'trkseg')
            for i, point in enumerate(seg):
              self.writePointToGPXTrack(elSeg, point, ele=str(self.trkmodel.getPointData(tnum, snum, i, ALT)))

    if TheConfig.getValue('ProfileStyle', 'PointsToTrack'):
      elTrk = etree.SubElement(root, 'trk')
      etree.SubElement(elTrk, 'name').text = self.tr('Waypoints')
      elSeg = etree.SubElement(elTrk, 'trkseg')
      for point, state in zip(self.wptmodel.waypoints, self.wptmodel.includeStates):
        if state:
          self.writePointToGPXTrack(elSeg, point, ele=self.wptmodel.index(point['ID'], ALT).data())

    etree.SubElement(metadata, 'time').text = datetime.utcnow().isoformat() + 'Z'
    etree.SubElement(metadata, 'bounds', minlat=str(self.minlat), minlon=str(self.minlon), maxlat=str(self.maxlat), maxlon=str(self.maxlon))

    with open(filename, 'w', encoding='utf-8') as file:
      file.write('<?xml version="1.0" encoding="UTF-8"?>\n' + etree.tostring(root, encoding='unicode', pretty_print=True))

  def writePointToKML(self, root, point, name=None, ele=None):
    place = etree.SubElement(root, 'Placemark')
    etree.SubElement(place, 'name').text = self.wptmodel.index(point['ID'], NAME).data() if name is None else name
    if 'DESC' in point and point['DESC'] is not None:
      etree.SubElement(place, 'description').text = point['DESC']
    if point[TIME] != '':
      ts = etree.SubElement(place, 'TimeStamp')
      etree.SubElement(ts, 'when').text = point[TIME].isoformat() + 'Z'
    p = etree.SubElement(place, 'Point')
    etree.SubElement(p, 'coordinates').text = '{},{},{}'.format(str(point[LON]),
                                                                str(point[LAT]),
                                                                self.wptmodel.index(point['ID'], ALT).data() if ele is None else ele)

  def writeKMLFile(self, filename):
    ns = {
      None: 'http://www.opengis.net/kml/2.2',
      'gx': 'http://www.google.com/kml/ext/2.2',
      'kml': 'http://www.opengis.net/kml/2.2',
      'atom': 'http://www.w3.org/2005/Atom'
    }
    root = etree.Element('kml', nsmap=ns, creator='GPX Viewer - https://osdn.net/projects/gpxviewer')
    document = etree.SubElement(root, 'Document')
    etree.SubElement(document, 'name').text = QFileInfo(filename).fileName()
    etree.SubElement(document, 'snippet').text = 'Created ' + datetime.utcnow().ctime()

    # Define simple styles for tracks
    trkStyle = etree.SubElement(document, 'Style', id='track_n')
    lineStyle = etree.SubElement(trkStyle, 'LineStyle')
    etree.SubElement(lineStyle, 'color').text = '99ffac59'
    etree.SubElement(lineStyle, 'width').text = '6'
    trkStyle = etree.SubElement(document, 'Style', id='track_h')
    lineStyle = etree.SubElement(trkStyle, 'LineStyle')
    etree.SubElement(lineStyle, 'color').text = '99ffac59'
    etree.SubElement(lineStyle, 'width').text = '8'
    trkStyleMap = etree.SubElement(document, 'StyleMap', id='track')
    pair = etree.SubElement(trkStyleMap, 'Pair')
    etree.SubElement(pair, 'key').text = 'normal'
    etree.SubElement(pair, 'styleUrl').text = '#track_n'
    pair = etree.SubElement(trkStyleMap, 'Pair')
    etree.SubElement(pair, 'key').text = 'highlight'
    etree.SubElement(pair, 'styleUrl').text = '#track_h'

    wptfolder = etree.SubElement(document, 'Folder')
    etree.SubElement(wptfolder, 'name').text = 'Waypoints'
    trkfolder = etree.SubElement(document, 'Folder')
    etree.SubElement(trkfolder, 'name').text = 'Tracks'

    if not TheConfig.getValue('ProfileStyle', 'DeletePoints'):
      for point, state in zip(self.wptmodel.waypoints, self.wptmodel.includeStates):
        if state:
          self.writePointToKML(wptfolder, point)

    if TheConfig.getValue('ProfileStyle', 'TracksToPoints'):
      num = self.wptmodel.rowCount() - len(self.wptmodel.getSkippedPoints())
      for tnum, state in zip(range(len(self.trkmodel.tracks)), self.trkmodel.includeStates):
        if state:
          for snum, seg in enumerate(self.trkmodel.tracks[tnum]['SEGMENTS']):
            for i, point in enumerate(seg):
              num += 1
              self.writePointToKML(wptfolder, point,
                                   name='WPT{}'.format(num),
                                   ele=str(self.trkmodel.getPointData(tnum, snum, i, ALT)))

    if not TheConfig.getValue('ProfileStyle', 'DeleteTracks'):
      for tnum, track, state in zip(range(len(self.trkmodel.tracks)), self.trkmodel.tracks, self.trkmodel.includeStates):
        if state:
          place = etree.SubElement(trkfolder, 'Placemark')
          etree.SubElement(place, 'name').text = track[TRKNAME]
          etree.SubElement(place, 'styleUrl').text = '#track'

          if track[TRKTIME] != '':
            tr = etree.SubElement(place, '{%(gx)s}Track' % ns)
            times = []
            coords = []
            for snum, seg in enumerate(track['SEGMENTS']):
              for i, point in enumerate(seg):
                times += [point[TIME].isoformat() + 'Z']
                coords += ['{} {} {}'.format(str(point[LON]), str(point[LAT]), str(self.trkmodel.getPointData(tnum, snum, i, ALT)))]
            for t in times:
              etree.SubElement(tr, 'when').text = t
            for c in coords:
              etree.SubElement(tr, '{%(gx)s}coord' % ns).text = c

          else:  # track[TRKTIME] == ''
            tr = etree.SubElement(place, 'LineString')
            coords = []
            for snum, seg in enumerate(track['SEGMENTS']):
              for i, point in enumerate(seg):
                coords += ['{},{},{}'.format(str(point[LON]), str(point[LAT]), str(self.trkmodel.getPointData(tnum, snum, i, ALT)))]
            etree.SubElement(tr, 'coordinates').text = ' '.join(coords)

    if TheConfig.getValue('ProfileStyle', 'PointsToTrack'):
      place = etree.SubElement(trkfolder, 'Placemark')
      etree.SubElement(place, 'name').text = self.tr('Waypoints')
      etree.SubElement(place, 'styleUrl').text = '#track'

      if self.wptmodel.waypoints[0][TIME] != '':
        tr = etree.SubElement(place, '{%(gx)s}Track' % ns)
        times = []
        coords = []
        for point, state in zip(self.wptmodel.waypoints, self.wptmodel.includeStates):
          if state:
            times += [point[TIME].isoformat() + 'Z']
            coords += ['{} {} {}'.format(str(point[LON]), str(point[LAT]), self.wptmodel.index(point['ID'], ALT).data())]
        for t in times:
          etree.SubElement(tr, 'when').text = t
        for c in coords:
          etree.SubElement(tr, '{%(gx)s}coord' % ns).text = c

      else:  # self.wptmodel.waypoints[0][TIME] == ''
        tr = etree.SubElement(place, 'LineString')
        coords = []
        for point, state in zip(self.wptmodel.waypoints, self.wptmodel.includeStates):
          if state:
            coords += ['{},{},{}'.format(str(point[LON]), str(point[LAT]), self.wptmodel.index(point['ID'], ALT).data())]
        etree.SubElement(tr, 'coordinates').text = ' '.join(coords)

    with open(filename, 'w', encoding='utf-8') as file:
      file.write('<?xml version="1.0" encoding="UTF-8"?>\n' + etree.tostring(root, encoding='unicode', pretty_print=True))

  warningSent = pyqtSignal(str, str)


class GpxSortFilterModel(QSortFilterProxyModel):
  def __init__(self, parent=None):
    super(GpxSortFilterModel, self).__init__(parent)

    self.includeSkipped = True
    self.includeMarked = True
    self.includeCaptioned = True
    self.includeMarkedCaptioned = True
    self.includeOther = True

  def setSourceModel(self, sourceModel):
    super(GpxSortFilterModel, self).setSourceModel(sourceModel)
    sourceModel.dataChanged.connect(self.dataChanged)

  def lessThan(self, left, right):
    if left.column() == right.column() and right.column() != NAME:
      if left.data() != '' and right.data() != '':
        return left.data(ValueRole) < right.data(ValueRole)
      elif right.data() == '':
        return False
      else:
        return True

    return super(GpxSortFilterModel, self).lessThan(left, right)

  def filterAcceptsRow(self, source_row, source_parent):
    ind = self.sourceModel().index(source_row, NAME, source_parent)
    if (ind.data(IncludeRole) or self.includeSkipped) and \
       (not ind.data(MarkerRole) or ind.data(CaptionRole) or self.includeMarked) and \
       (not ind.data(CaptionRole) or ind.data(MarkerRole) or self.includeCaptioned) and \
       (not ind.data(MarkerRole) or not ind.data(CaptionRole) or self.includeMarkedCaptioned) and \
       (not ind.data(IncludeRole) or ind.data(MarkerRole) or ind.data(CaptionRole) or self.includeOther):
      return super(GpxSortFilterModel, self).filterAcceptsRow(source_row, source_parent)
    else:
      return False

  def filterAcceptsColumn(self, source_column, source_parent):
    if TheConfig.getboolean('MainWindow', 'DetailedView'):
      return True
    else:
      return source_column < TheConfig.defaultColumnsNumber

  def setFilterMask(self, skipped, marked, captioned, markedCaptioned, other):
    self.includeSkipped = skipped
    self.includeMarked = marked
    self.includeCaptioned = captioned
    self.includeMarkedCaptioned = markedCaptioned
    self.includeOther = other
    self.invalidateFilter()


def _distance(lat1, lon1, lat2, lon2):
  Radius = 6378.14  # The equatorial radius of the Earth
  # angle between two points
  angle = acos(min(1.0, sin(lat1*pi/180.0) * sin(lat2*pi/180.0) +
                   cos(lat1*pi/180.0) * cos(lat2*pi/180.0) * cos((lon1 - lon2)*pi/180.0)))
  # local radius of the Earth
  r = Radius * (0.99832407 + 0.00167644 * cos(2.0*lat1) - 0.00000352 * cos(4.0*lat1))
  dist = r * angle

  return dist


def markerPath(style, size):
  r = size / 2.0
  center = QPointF(r, r)
  path = QPainterPath()

  if style == '.':
    path.addEllipse(center, 3, 3)
  elif style == ',':
    path.addEllipse(center, 1, 1)
  elif style == 'o':
    path.addEllipse(center, 0.8 * r,  0.8 * r)
  elif style == 'v':
    path.addPolygon(QPolygonF([center + r * QPointF(cos(pi/2), sin(pi/2)),
                               center + r * QPointF(cos(7*pi/6), sin(7*pi/6)),
                               center + r * QPointF(cos(11*pi/6), sin(11*pi/6))]))
  elif style == '^':
    path.addPolygon(QPolygonF([center + r * QPointF(cos(3*pi/2), sin(3*pi/2)),
                               center + r * QPointF(cos(pi/6), sin(pi/6)),
                               center + r * QPointF(cos(5*pi/6), sin(5*pi/6))]))
  elif style == '<':
    path.addPolygon(QPolygonF([center + r * QPointF(cos(pi), sin(pi)),
                               center + r * QPointF(cos(5*pi/3), sin(5*pi/3)),
                               center + r * QPointF(cos(pi/3), sin(pi/3))]))
  elif style == '>':
    path.addPolygon(QPolygonF([center + r * QPointF(cos(0), sin(0)),
                               center + r * QPointF(cos(2*pi/3), sin(2*pi/3)),
                               center + r * QPointF(cos(4*pi/3), sin(4*pi/3))]))
  elif style == '1':
    path.moveTo(center)
    path.lineTo(center + r * QPointF(cos(pi/2), sin(pi/2)))
    path.moveTo(center)
    path.lineTo(center + r * QPointF(cos(7*pi/6), sin(7*pi/6)))
    path.moveTo(center)
    path.lineTo(center + r * QPointF(cos(11*pi/6), sin(11*pi/6)))
  elif style == '2':
    path.moveTo(center)
    path.lineTo(center - r * QPointF(cos(pi/2), sin(pi/2)))
    path.moveTo(center)
    path.lineTo(center - r * QPointF(cos(7*pi/6), sin(7*pi/6)))
    path.moveTo(center)
    path.lineTo(center - r * QPointF(cos(11*pi/6), sin(11*pi/6)))
  elif style == '3':
    path.moveTo(center)
    path.lineTo(center + r * QPointF(cos(pi), sin(pi)))
    path.moveTo(center)
    path.lineTo(center + r * QPointF(cos(pi/3), sin(pi/3)))
    path.moveTo(center)
    path.lineTo(center + r * QPointF(cos(5*pi/3), sin(5*pi/3)))
  elif style == '4':
    path.moveTo(center)
    path.lineTo(center + r * QPointF(cos(0), sin(0)))
    path.moveTo(center)
    path.lineTo(center + r * QPointF(cos(2*pi/3), sin(2*pi/3)))
    path.moveTo(center)
    path.lineTo(center + r * QPointF(cos(4*pi/3), sin(4*pi/3)))
  elif style == 'ad':
    path.moveTo(center + r * QPointF(0, 1))
    path.lineTo(center + 0.7 * r * QPointF(-1, 0))
    path.moveTo(center + r * QPointF(0, 1))
    path.lineTo(center + 0.7 * r * QPointF(1, 0))
    path.moveTo(center + r * QPointF(0, 1))
    path.lineTo(center + r * QPointF(0, -1))
  elif style == 'au':
    path.moveTo(center + r * QPointF(0, -1))
    path.lineTo(center + 0.7 * r * QPointF(-1, 0))
    path.moveTo(center + r * QPointF(0, -1))
    path.lineTo(center + 0.7 * r * QPointF(1, 0))
    path.moveTo(center + r * QPointF(0, -1))
    path.lineTo(center + r * QPointF(0, 1))
  elif style == 'al':
    path.moveTo(center + r * QPointF(-1, 0))
    path.lineTo(center + 0.7 * r * QPointF(0, -1))
    path.moveTo(center + r * QPointF(-1, 0))
    path.lineTo(center + 0.7 * r * QPointF(0, 1))
    path.moveTo(center + r * QPointF(-1, 0))
    path.lineTo(center + r * QPointF(1, 0))
  elif style == 'ar':
    path.moveTo(center + r * QPointF(1, 0))
    path.lineTo(center + 0.7 * r * QPointF(0, -1))
    path.moveTo(center + r * QPointF(1, 0))
    path.lineTo(center + 0.7 * r * QPointF(0, 1))
    path.moveTo(center + r * QPointF(1, 0))
    path.lineTo(center + r * QPointF(-1, 0))
  elif style == 's':
    path.addRect((1 - sqrt(0.5)) * r, (1 - sqrt(0.5)) * r, sqrt(2.0) * r, sqrt(2.0) * r)
  elif style == 'p':
    path.addPolygon(QPolygonF([center + r * QPointF(cos(3*pi/2), sin(3*pi/2)),
                               center + r * QPointF(cos(19*pi/10), sin(19*pi/10)),
                               center + r * QPointF(cos(3*pi/10), sin(3*pi/10)),
                               center + r * QPointF(cos(7*pi/10), sin(7*pi/10)),
                               center + r * QPointF(cos(11*pi/10), sin(11*pi/10))]))
  elif style == '*':
    path.addPolygon(QPolygonF([center + r * QPointF(cos(3*pi/2), sin(3*pi/2)),
                               center + r/2 * QPointF(cos(17*pi/10), sin(17*pi/10)),
                               center + r * QPointF(cos(19*pi/10), sin(19*pi/10)),
                               center + r/2 * QPointF(cos(pi/10), sin(pi/10)),
                               center + r * QPointF(cos(3*pi/10), sin(3*pi/10)),
                               center + r/2 * QPointF(cos(pi/2), sin(pi/2)),
                               center + r * QPointF(cos(7*pi/10), sin(7*pi/10)),
                               center + r/2 * QPointF(cos(9*pi/10), sin(9*pi/10)),
                               center + r * QPointF(cos(11*pi/10), sin(11*pi/10)),
                               center + r/2 * QPointF(cos(13*pi/10), sin(13*pi/10))]))
  elif style == 'h':
    path.addPolygon(QPolygonF([center + r * QPointF(cos(pi/6), sin(pi/6)),
                               center + r * QPointF(cos(pi/2), sin(pi/2)),
                               center + r * QPointF(cos(5*pi/6), sin(5*pi/6)),
                               center + r * QPointF(cos(7*pi/6), sin(7*pi/6)),
                               center + r * QPointF(cos(3*pi/2), sin(3*pi/2)),
                               center + r * QPointF(cos(11*pi/6), sin(11*pi/6))]))
  elif style == 'H':
    path.addPolygon(QPolygonF([center + r * QPointF(cos(0), sin(0)),
                               center + r * QPointF(cos(pi/3), sin(pi/3)),
                               center + r * QPointF(cos(2*pi/3), sin(2*pi/3)),
                               center + r * QPointF(cos(pi), sin(pi)),
                               center + r * QPointF(cos(4*pi/3), sin(4*pi/3)),
                               center + r * QPointF(cos(5*pi/3), sin(5*pi/3))]))
  elif style == '+':
    path.moveTo(r, 0)
    path.lineTo(r, size)
    path.moveTo(0, r)
    path.lineTo(size, r)
  elif style == 'x':
    path.moveTo((1 - sqrt(0.5)) * r, (1 - sqrt(0.5)) * r)
    path.lineTo((1 + sqrt(0.5)) * r, (1 + sqrt(0.5)) * r)
    path.moveTo((1 + sqrt(0.5)) * r, (1 - sqrt(0.5)) * r)
    path.lineTo((1 - sqrt(0.5)) * r, (1 + sqrt(0.5)) * r)
  elif style == 'D':
    path.addPolygon(QPolygonF([center + QPointF(r, 0), center + QPointF(0, r),
                               center - QPointF(r, 0), center - QPointF(0, r)]))
  elif style == 'd':
    path.addPolygon(QPolygonF([center + QPointF(0.6 * r, 0), center + QPointF(0, r),
                               center - QPointF(0.6 * r, 0), center - QPointF(0, r)]))
  elif style == '|':
    path.moveTo(r, 0)
    path.lineTo(r, size)
  elif style == '_':
    path.moveTo(0, r)
    path.lineTo(size, r)

  path.closeSubpath()
  return path.translated(-center)


def _markerIcon(style, color):
  size = 16
  pix = QPixmap(size, size)
  pix.fill(Qt.GlobalColor.transparent)
  p = QPainter(pix)
  p.setRenderHint(QPainter.RenderHint.Antialiasing)
  if style in {'1', '2', '3', '4', 'ad', 'au', 'al', 'ar', '+', 'x', '_', '|'}:
    p.setPen(QPen(QColor(color), 3, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
  else:
    p.setPen(QPen(QColor(color), 1, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
  p.setBrush(QColor(color))
  p.drawPath(markerPath(style, 0.8 * size).translated(QPointF(size / 2.0, size / 2.0)))

  return pix
