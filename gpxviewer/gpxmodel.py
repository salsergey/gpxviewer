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

import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from math import acos, cos, modf, pi, sin, sqrt
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QObject, QPointF, QSortFilterProxyModel, pyqtSignal
from PyQt5.QtGui import QColor, QFont, QGuiApplication, QPainter, QPainterPath, QPen, QPixmap, QPolygonF
from gpxviewer.configstore import TheConfig


WPTFIELDS = NAME, LAT, LON, ALT, DIST, TIME, TIMEDELTA, TIME_DAYS = range(8)
TRKFIELDS = TRKNAME, TRKSEGS, TRKPTS, TRKLEN, TRKTIME, TRKDUR = range(6)
ValueRole, IDRole, IncludeRole, MarkerRole, CaptionRole, SplitLineRole, NeglectRole, MarkerStyleRole, CaptionStyleRole, SplitLineStyleRole = range(Qt.UserRole, Qt.UserRole + 10)
SkipColor, MarkerColor, CaptionColor = (QColor(255, 225, 225), QColor(225, 225, 255), QColor(225, 255, 225))
MARKER_COLOR, MARKER_STYLE, MARKER_SIZE, CAPTION_POSX, CAPTION_POSY, CAPTION_SIZE, LINE_COLOR, LINE_STYLE, LINE_WIDTH = \
  ('MarkerColor', 'MarkerStyle', 'MarkerSize', 'CaptionPositionX', 'CaptionPositionY', 'CaptionSize', 'SplitLineColor', 'SplitLineStyle', 'SplitLineWidth')


class GpxWarning(Exception):
  def __init__(self, value):
    super(GpxWarning, self).__init__(value)


class WptModel(QAbstractTableModel):
  def __init__(self, parent=None):
    super(WptModel, self).__init__(parent)
    # Workaround to init columns to copy for the first time
    if len(TheConfig.columnsToCopy) == 0:
      TheConfig.columnsToCopy = list(WPTFIELDS)

    self.fields = [self.tr('Name'), self.tr('Latitude'), self.tr('Longitude'), self.tr('Elevation'),
                   self.tr('Distance'), self.tr('Time'), self.tr('Time difference'), self.tr('Time in days')]
    self.resetModel()
    self.pix = QPixmap(16, 16)
    self.pix.fill(Qt.transparent)

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

  def data(self, index, role=Qt.DisplayRole):
    if role == Qt.DisplayRole or role == Qt.EditRole:
      if index.column() == NAME and index.row() in self.changedNames:
        return self.changedNames[index.row()]
      elif index.column() == TIME and self.waypoints[index.row()][index.column()] != '':
        return str(self.waypoints[index.row()][index.column()] + timedelta(minutes=TheConfig.getValue('ProfileStyle', 'TimeZoneOffset')))
      elif index.column() == LAT or index.column() == LON:
        if TheConfig.getValue('ProfileStyle', 'CoordinateFormat') == 0:  # Decimal degrees
          return str(round(self.waypoints[index.row()][index.column()], 6))
        elif TheConfig.getValue('ProfileStyle', 'CoordinateFormat') == 1:  # Degrees with decimal minutes
          min, deg = modf(self.waypoints[index.row()][index.column()])
          min = round(min * 60, 4)
          return str(int(deg)) + '° ' + str(min) + '\''
        else:  # Degrees, minutes, seconds
          min, deg = modf(self.waypoints[index.row()][index.column()])
          min = min * 60
          sec, min = modf(min)
          sec = round(sec * 60, 2)
          return str(int(deg)) + '°' + str(int(min)) + '\'' + str(sec) + '"'
      else:
        return str(self.waypoints[index.row()][index.column()])
    elif role == Qt.DecorationRole and index.column() == NAME:
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
      if all([k in self.pointStyles[index.row()] for k in {CAPTION_POSX, CAPTION_POSY, CAPTION_SIZE}]):
        return {k: self.pointStyles[index.row()][k] for k in {CAPTION_POSX, CAPTION_POSY, CAPTION_SIZE}}
      else:
        return {k: TheConfig.getValue('PointStyle', k) for k in {CAPTION_POSX, CAPTION_POSY, CAPTION_SIZE}}
    elif role == SplitLineStyleRole:
      if all([k in self.pointStyles[index.row()] for k in {LINE_COLOR, LINE_STYLE, LINE_WIDTH}]):
        return {k: self.pointStyles[index.row()][k] for k in {LINE_COLOR, LINE_STYLE, LINE_WIDTH}}
      else:
        return {k: TheConfig.getValue('PointStyle', k) for k in {LINE_COLOR, LINE_STYLE, LINE_WIDTH}}
    elif role == Qt.BackgroundRole:
      if not self.includeStates[index.row()]:
        return SkipColor
      elif self.captionStates[index.row()]:
        return CaptionColor
      elif self.markerStates[index.row()]:
        return MarkerColor
      else:
        return Qt.white
    elif role == Qt.FontRole:
      font = QFont()
      if self.splitStates[index.row()]:
        font.setBold(True)
      if self.neglectStates[index.row()]:
        font.setItalic(True)
      return font
    return None

  def setData(self, index, value, role):
    if index.isValid() and role == Qt.EditRole and value != self.waypoints[index.row()][NAME]:
      self.changedNames[index.row()] = value
      self.dataChanged.emit(index, index)
      self.wptDataChanged.emit()
      return True
    else:
      return False

  def flags(self, index):
    if index.column() == NAME:
      return super(WptModel, self).flags(index) | Qt.ItemIsEditable
    else:
      return super(WptModel, self).flags(index)

  def headerData(self, section, orientation, role):
    if role == Qt.DisplayRole:
      return self.fields[section] if orientation == Qt.Horizontal else section + 1
    return None

  def parent(self, index=None):
    if index is not None:
      return QModelIndex()
    else:
      return super(WptModel, self).parent()

  def copyToClipboard(self, IDs):
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
    if key in {CAPTION_POSX, CAPTION_POSY, CAPTION_SIZE}:
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
    self.endResetModel()

  def setIncludeStates(self, IDs, state, update=True):
    for i in IDs:
      self.includeStates[i] = state
    if update:
      self.parent().updatePoints()
    self.wptDataChanged.emit()

  def setMarkerStates(self, IDs, state):
    for i in IDs:
      self.markerStates[i] = state
      for key in {MARKER_COLOR, MARKER_STYLE, MARKER_SIZE}:
        if key not in self.pointStyles[i]:
          self.pointStyles[i][key] = TheConfig.getValue('PointStyle', key)
    self.wptDataChanged.emit()

  def setCaptionStates(self, IDs, state):
    for i in IDs:
      self.captionStates[i] = state
      for key in {CAPTION_POSX, CAPTION_POSY, CAPTION_SIZE}:
        if key not in self.pointStyles[i]:
          self.pointStyles[i][key] = TheConfig.getValue('PointStyle', key)
    self.wptDataChanged.emit()

  def setSplitLines(self, IDs, state):
    for i in IDs:
      self.splitStates[i] = state
      for key in {LINE_COLOR, LINE_STYLE, LINE_WIDTH}:
        if key not in self.pointStyles[i]:
          self.pointStyles[i][key] = TheConfig.getValue('PointStyle', key)
    self.wptDataChanged.emit()

  def setNeglectStates(self, IDs, state):
    for i in IDs:
      self.neglectStates[i] = state
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

  wptDataChanged = pyqtSignal()


class TrkModel(QAbstractTableModel):
  def __init__(self, parent=None):
    super(TrkModel, self).__init__(parent)
    self.fields = [self.tr('Name'), self.tr('Segments'), self.tr('Points'), self.tr('Length'), self.tr('Time'), self.tr('Duration')]
    self.resetModel()

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

  def data(self, index, role=Qt.DisplayRole):
    if role == Qt.DisplayRole:
      if index.column() == TRKTIME and self.tracks[index.row()][index.column()] != '':
        return str(self.tracks[index.row()][index.column()] + timedelta(minutes=TheConfig.getValue('ProfileStyle', 'TimeZoneOffset')))
      else:
        return str(self.tracks[index.row()][index.column()])
    elif role == IncludeRole:
      return self.includeStates[index.row()]
    elif role == Qt.BackgroundRole:
      return Qt.white if self.includeStates[index.row()] else SkipColor
    return None

  def headerData(self, section, orientation, role):
    if role == Qt.DisplayRole:
      return self.fields[section] if orientation == Qt.Horizontal else section + 1
    return None

  def copyToClipboard(self, IDs):
    text = ''
    for i in IDs:
      text += '\t'.join([self.index(i, f).data() for f in TRKFIELDS]) + '\n'
    QGuiApplication.clipboard().setText(text)

  def getSkippedTracks(self):
    return [i for i, s in enumerate(self.includeStates) if not s]

  def resetModel(self):
    self.beginResetModel()
    self.tracks = []
    self.includeStates = []
    self.endResetModel()

  def setIncludeStates(self, IDs, state, update=True):
    for i in IDs:
      self.includeStates[i] = state
    if update:
      self.parent().updatePoints()


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
    self.maxalt = 0

  def parse(self, filename):
    try:
      doc = ET.parse(filename)
    except ET.ParseError:
      raise GpxWarning(filename + self.tr(' is an invalid GPX file.'))
    ns = {'ns': doc.getroot().tag.split('}')[0][1:]}

    tag = 'name'
    if TheConfig.getValue('ProfileStyle', 'ReadNameFromTag') == 1:  # Comment
      tag = 'cmt'
    elif TheConfig.getValue('ProfileStyle', 'ReadNameFromTag') == 2:  # Description
      tag = 'desc'

    wptid = self.wptmodel.rowCount()
    for p in doc.iterfind('.//{%(ns)s}wpt' % ns):
      try:
        point = {}
        name = p.findtext(('{%(ns)s}' + tag) % ns)
        point[NAME] = name.strip() if name is not None else ''
        point[LAT] = float(p.get('lat'))
        point[LON] = float(p.get('lon'))
        point[ALT] = int(round(float(p.findtext('{%(ns)s}ele' % ns))))
        self.minalt = min(self.minalt, point[ALT])
        self.maxalt = max(self.maxalt, point[ALT])
        if p.findtext('{%(ns)s}time' % ns) is not None:
          dt = datetime.strptime(p.findtext('{%(ns)s}time' % ns).strip(), '%Y-%m-%dT%H:%M:%SZ')
          point[TIME] = dt
        else:
          point[TIME] = ''
        point[DIST] = ''
        point[TIMEDELTA] = ''
        point[TIME_DAYS] = ''
        point['ID'] = wptid

        # Additional fields
        point['CMT'] = p.findtext('{%(ns)s}cmt' % ns)
        point['DESC'] = p.findtext('{%(ns)s}desc' % ns)
        point['SYM'] = p.findtext('{%(ns)s}sym' % ns)

        self.wptmodel.beginInsertRows(QModelIndex(), wptid, wptid)
        self.wptmodel.waypoints += [point]
        self.wptmodel.includeStates += [True]
        self.wptmodel.markerStates += [False]
        self.wptmodel.captionStates += [False]
        self.wptmodel.splitStates += [False]
        self.wptmodel.neglectStates += [False]
        self.wptmodel.pointStyles += [{}]
        self.wptmodel.endInsertRows()
        wptid += 1

      except (TypeError, ValueError):
        self.warningSent.emit(self.tr('File read error'),
                              self.tr('Waypoint ') + (point[NAME] + ' ' if point[NAME] != '' else '') + self.tr('is invalid and will be skipped.', 'Waypoint'))

    trkid = self.trkmodel.rowCount()
    for t in doc.iterfind('.//{%(ns)s}trk' % ns):
      try:
        track = {}
        name = t.findtext('{%(ns)s}name' % ns)
        track[TRKNAME] = name.strip() if name is not None else ''

        track['SEGMENTS'] = []
        pts = 0
        tot_dist = 0.0
        for s in t.iterfind('.//{%(ns)s}trkseg' % ns):
          segment = []
          prev_lat = None
          prev_lon = None
          dist = 0.0
          for p in s.iterfind('.//{%(ns)s}trkpt' % ns):
            point = {}
            point[LAT] = float(p.get('lat'))
            point[LON] = float(p.get('lon'))
            point[ALT] = int(round(float(p.findtext('{%(ns)s}ele' % ns))))
            self.minalt = min(self.minalt, point[ALT])
            self.maxalt = max(self.maxalt, point[ALT])
            if p.findtext('{%(ns)s}time' % ns) is not None:
              dt = datetime.strptime(p.findtext('{%(ns)s}time' % ns).strip(), '%Y-%m-%dT%H:%M:%SZ')
              point[TIME] = dt
            else:
              point[TIME] = ''

            if prev_lat is not None and prev_lon is not None:
              dist += _distance(point[LAT], point[LON], prev_lat, prev_lon)
            prev_lat = point[LAT]
            prev_lon = point[LON]

            segment += [point]
            pts += 1

          track['SEGMENTS'] += [segment]
          tot_dist += dist

        track[TRKSEGS] = len(track['SEGMENTS'])
        track[TRKPTS] = pts
        track['LENGTH'] = tot_dist
        track[TRKLEN] = ''
        track[TRKTIME] = track['SEGMENTS'][0][0][TIME]
        track[TRKDUR] = track['SEGMENTS'][-1][-1][TIME] - track['SEGMENTS'][0][0][TIME] \
                        if track['SEGMENTS'][0][0][TIME] != '' and track['SEGMENTS'][-1][-1][TIME] != '' else ''

        self.trkmodel.beginInsertRows(QModelIndex(), trkid, trkid)
        self.trkmodel.tracks += [track]
        self.trkmodel.includeStates += [True]
        self.trkmodel.endInsertRows()
        trkid += 1

      except (TypeError, ValueError):
        self.warningSent.emit(self.tr('File read error'),
                              self.tr('Track ') + (track[TRKNAME] + ' ' if track[TRKNAME] != '' else '') + self.tr('is invalid and will be skipped.', 'Track'))

    TheConfig['ProfileStyle']['MinimumAltitude'] = str(round(self.minalt, -3) - 500 if round(self.minalt, -3) > self.minalt else round(self.minalt, -3))
    TheConfig['ProfileStyle']['MaximumAltitude'] = str(round(self.maxalt, -3) + 500 if round(self.maxalt, -3) < self.maxalt else round(self.maxalt, -3))

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
          if ind < len(self.points) and self.wptmodel.waypoints[i][TIME] < self.trkmodel.tracks[self.points[ind][0]]['SEGMENTS'][self.points[ind][1]][self.points[ind][2]][TIME] or ind == len(self.points):
            self.points.insert(ind, i)
            i += 1
          ind += 1
        else:
          i += 1
    else:
      for i, p in enumerate(self.wptmodel.waypoints):
        if self.wptmodel.includeStates[i]:
          self.points += [i]

    self.updateDistance()
    self.updateTimeDifference()

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
        self.wptmodel.waypoints[p][DIST] = round(dist, 3)
        prev_lat = lat
        prev_lon = lon
      else:
        lat = self.trkmodel.tracks[p[0]]['SEGMENTS'][p[1]][p[2]][LAT]
        lon = self.trkmodel.tracks[p[0]]['SEGMENTS'][p[1]][p[2]][LON]
        if prev_lat is not None and prev_lon is not None:
          dist += _distance(lat, lon, prev_lat, prev_lon) * dist_coeff
        self.trkmodel.tracks[p[0]]['SEGMENTS'][p[1]][p[2]][DIST] = round(dist, 3)
        prev_lat = lat
        prev_lon = lon

    for i in self.wptmodel.getSkippedPoints():
      self.wptmodel.waypoints[i][DIST] = ''

    for i in self.trkmodel.tracks:
      i[TRKLEN] = round(i['LENGTH'] * dist_coeff, 3)

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
        p[TIMEDELTA] = p[TIME] - start_dt
        p[TIME_DAYS] = round(p[TIMEDELTA].days + p[TIMEDELTA].seconds / 60.0 / 60.0 / 24.0, 3)
      else:
        p[TIMEDELTA] = ''
        p[TIME_DAYS] = ''

    for i, track in enumerate(self.trkmodel.tracks):
      if self.trkmodel.includeStates[i]:
        for seg in track['SEGMENTS']:
          for p in seg:
            if p[TIME] != '':
              time_delta = p[TIME] - start_dt
              p[TIME_DAYS] = round(time_delta.days + time_delta.seconds / 60.0 / 60.0 / 24.0, 3)
            else:
              p[TIME_DAYS] = ''

  def writeToFile(self, filename):
    root = ET.Element('gpx', attrib={'version': '1.1',
                                     'creator': 'GPXViewer - https://bitbucket.org/salsergey/gpxviewer',
                                     'xmlns': 'http://www.topografix.com/GPX/1/1'})
    metadata = ET.Element('metadata')
    root.append(metadata)

    minlat = 90
    minlon = 180
    maxlat = 0
    maxlon = -180
    for p, s in zip(self.wptmodel.waypoints, self.wptmodel.includeStates):
      if s:
        element = ET.Element('wpt', attrib={'lat': str(p[LAT]), 'lon': str(p[LON])})
        root.append(element)
        if p[LAT] < minlat:
          minlat = p[LAT]
        if p[LON] < minlon:
          minlon = p[LON]
        if p[LAT] > maxlat:
          maxlat = p[LAT]
        if p[LON] > maxlon:
          maxlon = p[LON]
        el = ET.Element('ele')
        el.text = str(p[ALT])
        element.append(el)
        el = ET.Element('time')
        el.text = p[TIME].strftime('%Y-%m-%dT%H:%M:%SZ')
        element.append(el)
        el = ET.Element('name')
        if p['ID'] in self.wptmodel.changedNames:
          el.text = self.wptmodel.changedNames[p['ID']]
        else:
          el.text = p[NAME]
        element.append(el)
        if p['CMT'] is not None:
          el = ET.Element('cmt')
          el.text = p['CMT']
          element.append(el)
        if p['DESC'] is not None:
          el = ET.Element('desc')
          el.text = p['DESC']
          element.append(el)
        if p['SYM'] is not None:
          el = ET.Element('sym')
          el.text = p['SYM']
          element.append(el)

    for track, s in zip(self.trkmodel.tracks, self.trkmodel.includeStates):
      if s:
        elTrk = ET.Element('trk')
        root.append(elTrk)
        el = ET.Element('name')
        el.text = track[TRKNAME]
        elTrk.append(el)
        for seg in track['SEGMENTS']:
          elSeg = ET.Element('trkseg')
          elTrk.append(elSeg)
          for p in seg:
            elP = ET.Element('trkpt', attrib={'lat': str(p[LAT]), 'lon': str(p[LON])})
            elSeg.append(elP)
            if p[LAT] < minlat:
              minlat = p[LAT]
            if p[LON] < minlon:
              minlon = p[LON]
            if p[LAT] > maxlat:
              maxlat = p[LAT]
            if p[LON] > maxlon:
              maxlon = p[LON]
            el = ET.Element('ele')
            el.text = str(p[ALT])
            elP.append(el)
            el = ET.Element('time')
            el.text = p[TIME].strftime('%Y-%m-%dT%H:%M:%SZ')
            elP.append(el)

    el = ET.Element('time')
    el.text = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    metadata.append(el)
    el = ET.Element('bounds', attrib={'minlat': str(minlat), 'minlon': str(minlon), 'maxlat': str(maxlat), 'maxlon': str(maxlon)})
    metadata.append(el)

    outgpx = '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(root, encoding='unicode') + '\n'
    outgpx = outgpx.replace('<metadata', '\n  <metadata')
    outgpx = outgpx.replace('</metadata', '\n  </metadata')
    outgpx = outgpx.replace('<wpt', '\n  <wpt')
    outgpx = outgpx.replace('<trk', '\n  <trk')
    outgpx = outgpx.replace('<bounds', '\n    <bounds')
    outgpx = outgpx.replace('<ele', '\n    <ele')
    outgpx = outgpx.replace('<time', '\n    <time')
    outgpx = outgpx.replace('<name', '\n    <name')
    outgpx = outgpx.replace('<cmt', '\n    <cmt')
    outgpx = outgpx.replace('<desc', '\n    <desc')
    outgpx = outgpx.replace('<sym', '\n    <sym')
    outgpx = outgpx.replace('</wpt', '\n  </wpt')
    outgpx = outgpx.replace('</trk', '\n  </trk')
    outgpx = outgpx.replace('</gpx', '\n</gpx')
    with open(filename, 'w', encoding='utf-8') as file:
      file.write(outgpx)

  warningSent = pyqtSignal(str, str)


class GpxSortFilterModel(QSortFilterProxyModel):
  def __init__(self, parent):
    super(GpxSortFilterModel, self).__init__(parent)

    self.includeSkipped = True
    self.includeMarked = True
    self.includeCaptioned = True
    self.includeMarkedCaptioned = True
    self.includeOther = True

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
  pix.fill(Qt.transparent)
  p = QPainter(pix)
  p.setRenderHint(QPainter.Antialiasing)
  if style in {'1', '2', '3', '4', '+', 'x', '_', '|'}:
    p.setPen(QPen(QColor(color), 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
  else:
    p.setPen(QPen(QColor(color), 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
  p.setBrush(QColor(color))
  p.drawPath(markerPath(style, 0.8 * size).translated(QPointF(size / 2.0, size / 2.0)))

  return pix
