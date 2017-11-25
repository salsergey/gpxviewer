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

import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from math import pi, sin, cos, acos
from PyQt5 import QtCore
from PyQt5.QtGui import QColor, QFont, QGuiApplication, QPixmap, QPainter
from gpxviewer.configstore import TheConfig


WPTFIELDS = NAME, LAT, LON, ALT, DIST, TIME, TIMEDELTA, TIME_DAYS = range(8)
TRKFIELDS = TRKNAME, TRKSEGS, TRKPTS, TRKLEN, TRKTIME, TRKDUR = range(6)
ValueRole, IDRole, IncludeRole, SplitStateRole, MarkerRole, SplitLineRole, CaptionRole, NeglectRole = range(QtCore.Qt.UserRole, QtCore.Qt.UserRole + 8)
INCSTATES = INC_DEFAULT, INC_SKIP, INC_MARKER, INC_CAPTION = range(4)
INCCOLORS = DefaultColor, SkipColor, MarkerColor, CaptionColor = QtCore.Qt.white, QColor(255, 225, 225), QColor(225, 225, 255), QColor(225, 255, 225)
MARKER_COLOR, MARKER_STYLE, MARKER_SIZE, LINE_COLOR, LINE_STYLE, LINE_WIDTH, CAPTION_POSX, CAPTION_POSY, CAPTION_SIZE = range(9)


class GpxWarning(Exception):
  def __init__(self, value):
    super(GpxWarning, self).__init__(value)


class WptModel(QtCore.QAbstractTableModel):
  def __init__(self, parent=None):
    super(WptModel, self).__init__(parent)
    self.fields = [self.tr('Name'), self.tr('Latitude'), self.tr('Longitude'), self.tr('Elevation'),
                   self.tr('Distance'), self.tr('Time'), self.tr('Time difference'), self.tr('Time in days')]
    self.resetModel()
    self.pix = QPixmap(16, 16)
    self.pix.fill(QtCore.Qt.transparent)

  def rowCount(self, parent=None):
    return len(self.waypoints)

  def columnCount(self, parent=None):
    return len(self.fields)

  def data(self, index, role=QtCore.Qt.DisplayRole):
    if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
      if index.column() == TIME and self.waypoints[index.row()][index.column()] != '':
        return str(self.waypoints[index.row()][index.column()] + timedelta(minutes=TheConfig['ProfileStyle'].getint('TimeZoneOffset')))
      else:
        return str(self.waypoints[index.row()][index.column()])
    elif role == QtCore.Qt.DecorationRole and index.column() == NAME:
      if index.data(IncludeRole) in {INC_MARKER, INC_CAPTION}:
        return _markerIcon(index.data(MarkerRole)[MARKER_STYLE], index.data(MarkerRole)[MARKER_COLOR])
      else:
        return self.pix
    elif role == ValueRole:
      return self.waypoints[index.row()][index.column()]
    elif role == IDRole:
      return self.waypoints[index.row()]['ID']
    elif role == IncludeRole:
      return self.includeStates[index.row()]
    elif role == SplitStateRole:
      return self.splitStates[index.row()]
    elif role == NeglectRole:
      return self.neglectStates[index.row()]
    elif role == MarkerRole:
      return {k: self.pointStyles[index.row()][k] for k in {MARKER_COLOR, MARKER_STYLE, MARKER_SIZE}}
    elif role == SplitLineRole:
      return {k: self.pointStyles[index.row()][k] for k in {LINE_COLOR, LINE_STYLE, LINE_WIDTH}}
    elif role == CaptionRole:
      return {k: self.pointStyles[index.row()][k] for k in {CAPTION_POSX, CAPTION_POSY, CAPTION_SIZE}}
    elif role == QtCore.Qt.BackgroundRole:
      return INCCOLORS[self.includeStates[index.row()]]
    elif role == QtCore.Qt.FontRole:
      font = QFont()
      if self.splitStates[index.row()]:
        font.setBold(True)
      if self.neglectStates[index.row()]:
        font.setItalic(True)
      return font
    return None

  def setData(self, index, value, role):
    if index.isValid() and role == QtCore.Qt.EditRole and value != self.waypoints[index.row()][NAME]:
      self.waypoints[index.row()][NAME] = value
      self.changedNames += [index.row()]
      self.pointNames += [value]
      self.dataChanged.emit(index, index)
      self.namesChanged.emit(True)
      return True
    else:
      return False

  def flags(self, index):
    if index.column() == NAME:
      return super(WptModel, self).flags(index) | QtCore.Qt.ItemIsEditable
    else:
      return super(WptModel, self).flags(index)

  def headerData(self, section, orientation, role):
    if role == QtCore.Qt.DisplayRole:
      return self.fields[section] if orientation == QtCore.Qt.Horizontal else section + 1
    return None

  def copyToClipboard(self, IDs):
    text = ''
    for i in IDs:
      text += '\t'.join([self.index(i, f).data() for f in WPTFIELDS]) + '\n'
    QGuiApplication.clipboard().setText(text)

  def getIndexesWithIncludeState(self, state):
    return [i for i, s in enumerate(self.includeStates) if s == state]

  def getNeglectStates(self):
    return [i for i, s in enumerate(self.neglectStates) if s]

  def getPointStyles(self, key):
    if key in {MARKER_COLOR, MARKER_STYLE, MARKER_SIZE}:
      return [p[key] for i, p in enumerate(self.pointStyles) if self.includeStates[i] in {INC_MARKER, INC_CAPTION}]
    if key in {LINE_COLOR, LINE_STYLE, LINE_WIDTH}:
      return [p[key] for i, p in enumerate(self.pointStyles) if self.splitStates[i]]
    if key in {CAPTION_POSX, CAPTION_POSY, CAPTION_SIZE}:
      return [p[key] for i, p in enumerate(self.pointStyles) if self.includeStates[i] == INC_CAPTION]

  def getSplitLines(self):
    return [i for i, s in enumerate(self.splitStates) if s]

  def resetModel(self):
    self.beginResetModel()
    self.waypoints = []
    self.includeStates = []
    self.splitStates = []
    self.neglectStates = []
    self.pointStyles = []
    self.changedNames = []
    self.pointNames = []
    self.endResetModel()

  def setIncludeStates(self, IDs, state, update=True):
    for i in IDs:
      self.includeStates[i] = state
    if update:
      self.parent().updatePoints()

  def setNeglectStates(self, IDs, state):
    for i in IDs:
      self.neglectStates[i] = state
    self.parent().updateDistance()

  def setPointStyle(self, IDs, key, value):
    for i in IDs:
      self.pointStyles[i][key] = value

  def setSplitLines(self, IDs, state):
    for i in IDs:
      self.splitStates[i] = state

  namesChanged = QtCore.pyqtSignal(bool)


class TrkModel(QtCore.QAbstractTableModel):
  def __init__(self, parent=None):
    super(TrkModel, self).__init__(parent)
    self.fields = [self.tr('Name'), self.tr('Segments'), self.tr('Points'), self.tr('Length'), self.tr('Time'), self.tr('Duration')]
    self.resetModel()

  def rowCount(self, parent=None):
    return len(self.tracks)

  def columnCount(self, parent=None):
    return len(self.fields)

  def data(self, index, role=QtCore.Qt.DisplayRole):
    if role == QtCore.Qt.DisplayRole:
      if index.column() == TRKTIME and self.tracks[index.row()][index.column()] != '':
        return str(self.tracks[index.row()][index.column()] + timedelta(minutes=TheConfig['ProfileStyle'].getint('TimeZoneOffset')))
      else:
        return str(self.tracks[index.row()][index.column()])
    elif role == IncludeRole:
      return self.includeStates[index.row()]
    elif role == QtCore.Qt.BackgroundRole:
      return INCCOLORS[self.includeStates[index.row()]]
    return None

  def headerData(self, section, orientation, role):
    if role == QtCore.Qt.DisplayRole:
      return self.fields[section] if orientation == QtCore.Qt.Horizontal else section + 1
    return None

  def copyToClipboard(self, IDs):
    text = ''
    for i in IDs:
      text += '\t'.join([self.index(i, f).data() for f in TRKFIELDS]) + '\n'
    QGuiApplication.clipboard().setText(text)

  def getIndexesWithIncludeState(self, state):
    return [i for i, s in enumerate(self.includeStates) if s == state]

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


class GpxParser(QtCore.QObject):
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

    defaultStyle = {MARKER_COLOR: int(TheConfig['PointStyle']['MarkerColor']),
                    MARKER_STYLE: TheConfig['PointStyle']['MarkerStyle'],
                    MARKER_SIZE: int(TheConfig['PointStyle']['MarkerSize']),
                    LINE_COLOR: int(TheConfig['PointStyle']['SplitLineColor']),
                    LINE_STYLE: TheConfig['PointStyle']['SplitLineStyle'],
                    LINE_WIDTH: float(TheConfig['PointStyle']['SplitLineWidth']),
                    CAPTION_POSX: int(TheConfig['PointStyle']['CaptionPositionX']),
                    CAPTION_POSY: int(TheConfig['PointStyle']['CaptionPositionY']),
                    CAPTION_SIZE: int(TheConfig['PointStyle']['CaptionSize'])}

    wptid = len(self.wptmodel.waypoints)
    for p in doc.iterfind('.//{%(ns)s}wpt' % ns):
      try:
        point = {}
        name = p.findtext('{%(ns)s}name' % ns)
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

        self.wptmodel.beginInsertRows(QtCore.QModelIndex(), wptid, wptid)
        self.wptmodel.waypoints += [point]
        self.wptmodel.includeStates += [INC_DEFAULT]
        self.wptmodel.splitStates += [False]
        self.wptmodel.neglectStates += [False]
        self.wptmodel.pointStyles += [defaultStyle.copy()]
        self.wptmodel.endInsertRows()
        wptid += 1

      except (TypeError, ValueError):
        self.warningSent.emit(self.tr('File read error'),
                              self.tr('Waypoint ') + (point[NAME] + ' ' if point[NAME] != '' else '') + self.tr('is invalid and will be skipped.', 'Waypoint'))

    trkid = len(self.wptmodel.waypoints)
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
              dist += _distance(point[LAT], point[LON], prev_lat, prev_lon) * 1.2  # with mountain coefficient
            prev_lat = point[LAT]
            prev_lon = point[LON]

            segment += [point]
            pts += 1

          track['SEGMENTS'] += [segment]
          tot_dist += dist

        track[TRKSEGS] = len(track['SEGMENTS'])
        track[TRKPTS] = pts
        track[TRKLEN] = round(tot_dist, 3)
        track[TRKTIME] = track['SEGMENTS'][0][0][TIME]
        track[TRKDUR] = track['SEGMENTS'][-1][-1][TIME] - track['SEGMENTS'][0][0][TIME] \
                        if track['SEGMENTS'][0][0][TIME] != '' and track['SEGMENTS'][-1][-1][TIME] != '' else ''

        self.trkmodel.beginInsertRows(QtCore.QModelIndex(), trkid, trkid)
        self.trkmodel.tracks += [track]
        self.trkmodel.includeStates += [INC_DEFAULT]
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
      if self.wptmodel.includeStates[i] != INC_SKIP and p[TIME] == '':
        includeTracks = False

    if len(self.trkmodel.tracks) != 0 and includeTracks:
      for tind, track in enumerate(self.trkmodel.tracks):
        if self.trkmodel.includeStates[tind] != INC_SKIP and \
           (track[TRKTIME] != '' or len(self.wptmodel.waypoints) == len(self.wptmodel.getIndexesWithIncludeState(INC_SKIP))):
          for sind, segment in enumerate(track['SEGMENTS']):
            self.points += zip([tind] * len(segment), [sind] * len(segment), range(len(segment)))
      ind = 0
      i = 0
      while i < len(self.wptmodel.waypoints):
        if self.wptmodel.includeStates[i] != INC_SKIP:
          if ind < len(self.points) and self.wptmodel.waypoints[i][TIME] < self.trkmodel.tracks[self.points[ind][0]]['SEGMENTS'][self.points[ind][1]][self.points[ind][2]][TIME] or ind == len(self.points):
            self.points.insert(ind, i)
            i += 1
          ind += 1
        else:
          i += 1
    else:
      for i, p in enumerate(self.wptmodel.waypoints):
        if self.wptmodel.includeStates[i] != INC_SKIP:
          self.points += [i]

    self.updateDistance()
    self.updateTimeDifference()

  def updateDistance(self):
    prev_lat = None
    prev_lon = None
    dist = 0.0
    dist_coeff = float(TheConfig['ProfileStyle']['DistanceCoefficient'])

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

    for i in self.wptmodel.getIndexesWithIncludeState(INC_SKIP):
      self.wptmodel.waypoints[i][DIST] = ''

  def updateTimeDifference(self):
    start_dt = None
    for i, p in enumerate(self.wptmodel.waypoints):
      if self.wptmodel.includeStates[i] != INC_SKIP and p[TIME] != '':
        start_dt = p[TIME]
        break
    for i, track in enumerate(self.trkmodel.tracks):
      if self.trkmodel.includeStates[i] != INC_SKIP and track[TRKTIME] != '' and (start_dt is None or track[TRKTIME] < start_dt):
        start_dt = track[TRKTIME]
        break

    for i, p in enumerate(self.wptmodel.waypoints):
      if self.wptmodel.includeStates[i] != INC_SKIP and p[TIME] != '':
        p[TIMEDELTA] = p[TIME] - start_dt
        p[TIME_DAYS] = round(p[TIMEDELTA].days + p[TIMEDELTA].seconds / 60.0 / 60.0 / 24.0, 3)
      else:
        p[TIMEDELTA] = ''
        p[TIME_DAYS] = ''

    for i, track in enumerate(self.trkmodel.tracks):
      if self.trkmodel.includeStates[i] != INC_SKIP:
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
      if s != INC_SKIP:
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
      if s != INC_SKIP:
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

  warningSent = QtCore.pyqtSignal(str, str)


class GpxSortFilterModel(QtCore.QSortFilterProxyModel):
  def __init__(self, parent):
    super(GpxSortFilterModel, self).__init__(parent)

  def lessThan(self, left, right):
    if (left.column() == right.column() == TIME) or (left.column() == right.column() == TIMEDELTA):
      if left.data() != '' and right.data() != '':
        return left.data(ValueRole) < right.data(ValueRole)
      elif right.data() == '':
        return False
      else:
        return True

    return super(GpxSortFilterModel, self).lessThan(left, right)


def _distance(lat1, lon1, lat2, lon2):
  Radius = 6378.14  # The equatorial radius of the Earth
  # angle between two points
  angle = acos(min(1.0, sin(lat1*pi/180.0) * sin(lat2*pi/180.0) +
               cos(lat1*pi/180.0) * cos(lat2*pi/180.0) * cos((lon1 - lon2)*pi/180.0)))
  # local radius of the Earth
  r = Radius * (0.99832407 + 0.00167644 * cos(2.0*lat1) - 0.00000352 * cos(4.0*lat1))
  dist = r * angle

  return dist


def _markerIcon(style, color):
  size = 16
  r = 2 * size / 5
  pix = QPixmap(size, size)
  pix.fill(QtCore.Qt.transparent)
  p = QPainter(pix)
  p.setRenderHint(QPainter.Antialiasing)
  p.setPen(QColor(color))
  p.setBrush(QColor(color))
  center = QtCore.QPoint(size/2, size/2)

  if style == '.':
    p.drawEllipse(QtCore.QPoint(size/2, size/2), 3, 3)
  elif style == ',':
    #p.drawPoint(QtCore.QPoint(size/2, size/2))
    p.drawEllipse(QtCore.QPoint(size/2, size/2), 1, 1)
  elif style == 'o':
    p.drawEllipse(QtCore.QPoint(size/2, size/2), size/3, size/3)
  elif style == 'v':
    p.drawPolygon(center + r * QtCore.QPointF(cos(pi/2), sin(pi/2)), center + r * QtCore.QPointF(cos(7*pi/6), sin(7*pi/6)), center + r * QtCore.QPointF(cos(11*pi/6), sin(11*pi/6)))
  elif style == '^':
    p.drawPolygon(center + r * QtCore.QPointF(cos(3*pi/2), sin(3*pi/2)), center + r * QtCore.QPointF(cos(pi/6), sin(pi/6)), center + r * QtCore.QPointF(cos(5*pi/6), sin(5*pi/6)))
  elif style == '<':
    p.drawPolygon(center + r * QtCore.QPointF(cos(pi), sin(pi)), center + r * QtCore.QPointF(cos(5*pi/3), sin(5*pi/3)), center + r * QtCore.QPointF(cos(pi/3), sin(pi/3)))
  elif style == '>':
    p.drawPolygon(center + r * QtCore.QPointF(cos(0), sin(0)), center + r * QtCore.QPointF(cos(2*pi/3), sin(2*pi/3)), center + r * QtCore.QPointF(cos(4*pi/3), sin(4*pi/3)))
  elif style == '1':
    p.drawLine(center, center + r * QtCore.QPointF(cos(pi/2), sin(pi/2)))
    p.drawLine(center, center + r * QtCore.QPointF(cos(7*pi/6), sin(7*pi/6)))
    p.drawLine(center, center + r * QtCore.QPointF(cos(11*pi/6), sin(11*pi/6)))
  elif style == '2':
    p.drawLine(center, center - r * QtCore.QPointF(cos(pi/2), sin(pi/2)))
    p.drawLine(center, center - r * QtCore.QPointF(cos(7*pi/6), sin(7*pi/6)))
    p.drawLine(center, center - r * QtCore.QPointF(cos(11*pi/6), sin(11*pi/6)))
  elif style == '3':
    p.drawLine(center, center + r * QtCore.QPointF(cos(pi), sin(pi)))
    p.drawLine(center, center + r * QtCore.QPointF(cos(pi/3), sin(pi/3)))
    p.drawLine(center, center + r * QtCore.QPointF(cos(5*pi/3), sin(5*pi/3)))
  elif style == '4':
    p.drawLine(center, center + r * QtCore.QPointF(cos(0), sin(0)))
    p.drawLine(center, center + r * QtCore.QPointF(cos(2*pi/3), sin(2*pi/3)))
    p.drawLine(center, center + r * QtCore.QPointF(cos(4*pi/3), sin(4*pi/3)))
  elif style == 's':
    p.drawPolygon(center + QtCore.QPointF(r, r), center + QtCore.QPointF(-r, r), center - QtCore.QPointF(r, r), center + QtCore.QPointF(r, -r))
  elif style == 'p':
    p.drawPolygon(center + r * QtCore.QPointF(cos(3*pi/2), sin(3*pi/2)), center + r * QtCore.QPointF(cos(19*pi/10), sin(19*pi/10)), center + r * QtCore.QPointF(cos(3*pi/10), sin(3*pi/10)), center + r * QtCore.QPointF(cos(7*pi/10), sin(7*pi/10)), center + r * QtCore.QPointF(cos(11*pi/10), sin(11*pi/10)))
  elif style == '*':
    p.drawPolygon(center + r * QtCore.QPointF(cos(3*pi/2), sin(3*pi/2)), center + r/2 * QtCore.QPointF(cos(17*pi/10), sin(17*pi/10)), center + r * QtCore.QPointF(cos(19*pi/10), sin(19*pi/10)), center + r/2 * QtCore.QPointF(cos(pi/10), sin(pi/10)), center + r * QtCore.QPointF(cos(3*pi/10), sin(3*pi/10)), center + r/2 * QtCore.QPointF(cos(pi/2), sin(pi/2)), center + r * QtCore.QPointF(cos(7*pi/10), sin(7*pi/10)), center + r/2 * QtCore.QPointF(cos(9*pi/10), sin(9*pi/10)), center + r * QtCore.QPointF(cos(11*pi/10), sin(11*pi/10)), center + r/2 * QtCore.QPointF(cos(13*pi/10), sin(13*pi/10)))
  elif style == 'h':
    p.drawPolygon(center + r * QtCore.QPointF(cos(pi/6), sin(pi/6)), center + r * QtCore.QPointF(cos(pi/2), sin(pi/2)), center + r * QtCore.QPointF(cos(5*pi/6), sin(5*pi/6)), center + r * QtCore.QPointF(cos(7*pi/6), sin(7*pi/6)), center + r * QtCore.QPointF(cos(3*pi/2), sin(3*pi/2)), center + r * QtCore.QPointF(cos(11*pi/6), sin(11*pi/6)))
  elif style == 'H':
    p.drawPolygon(center + r * QtCore.QPointF(cos(0), sin(0)), center + r * QtCore.QPointF(cos(pi/3), sin(pi/3)), center + r * QtCore.QPointF(cos(2*pi/3), sin(2*pi/3)), center + r * QtCore.QPointF(cos(pi), sin(pi)), center + r * QtCore.QPointF(cos(4*pi/3), sin(4*pi/3)), center + r * QtCore.QPointF(cos(5*pi/3), sin(5*pi/3)))
  elif style == '+':
    p.drawLine(center + QtCore.QPointF(0, r), center - QtCore.QPointF(0, r))
    p.drawLine(center + QtCore.QPointF(r, 0), center - QtCore.QPointF(r, 0))
  elif style == 'x':
    p.drawLine(center + QtCore.QPointF(r, r), center - QtCore.QPointF(r, r))
    p.drawLine(center + QtCore.QPointF(r, -r), center + QtCore.QPointF(-r, r))
  elif style == 'D':
    p.drawPolygon(center + QtCore.QPointF(r, 0), center + QtCore.QPointF(0, r), center - QtCore.QPointF(r, 0), center - QtCore.QPointF(0, r))
  elif style == 'd':
    p.drawPolygon(center + QtCore.QPointF(r/2, 0), center + QtCore.QPointF(0, r), center - QtCore.QPointF(r/2, 0), center - QtCore.QPointF(0, r))
  elif style == '|':
    p.drawLine(center + QtCore.QPointF(0, r), center - QtCore.QPointF(0, r))
  elif style == '_':
    p.drawLine(center + QtCore.QPointF(r, 0), center - QtCore.QPointF(r, 0))

  return pix
