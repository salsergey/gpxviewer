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

import sys
from math import sqrt, sin, cos, pi
import xml.etree.ElementTree as ET
from datetime import datetime
from math import pi, sin, cos, acos
from PyQt5 import QtCore
from PyQt5.QtGui import QColor, QFont, QGuiApplication, QPixmap, QPainter
from gpxviewer.configstore import TheConfig


GPXFIELDS = NAME, LAT, LON, ALT, DIST, TIME, TIMEDELTA, TIME_DAYS = range(8)
ValueRole, IDRole, IncludeRole, SplitStateRole, MarkerRole, SplitLineRole, CaptionRole, NeglectRole = range(QtCore.Qt.UserRole, QtCore.Qt.UserRole + 8)
INCSTATES = INC_DEFAULT, INC_SKIP, INC_MARKER, INC_CAPTION = range(4)
INCCOLORS = DefaultColor, SkipColor, MarkerColor, CaptionColor = QtCore.Qt.white, QColor(255, 225, 225), QColor(225, 225, 255), QColor(225, 255, 225)
MARKER_COLOR, MARKER_STYLE, MARKER_SIZE, LINE_COLOR, LINE_STYLE, LINE_WIDTH, CAPTION_POSX, CAPTION_POSY, CAPTION_SIZE = range(9)


class GpxWarning(Exception):
  def __init__(self, value):
    super(GpxWarning, self).__init__(value)


class GpxModel(QtCore.QAbstractTableModel):
  def __init__(self, parent = None):
    super(GpxModel, self).__init__(parent)
    self.fields = [self.tr('Name'), self.tr('Latitude'), self.tr('Longitude'), self.tr('Altitude'), self.tr('Distance'), self.tr('Time'), self.tr('Time difference'), self.tr('Time in days')]
    self.resetModel()

  def rowCount(self, parent = None):
    return len(self.points)

  def columnCount(self, parent = None):
    return len(self.fields)

  def data(self, index, role = QtCore.Qt.DisplayRole):
    if role == QtCore.Qt.DisplayRole:
      return str(self.points[index.row()][index.column()])
    elif role == QtCore.Qt.DecorationRole and index.column() == NAME:
      if index.data(IncludeRole) in {INC_MARKER, INC_CAPTION}:
        return _markerIcon(index.data(MarkerRole)[MARKER_STYLE], index.data(MarkerRole)[MARKER_COLOR])
      else:
        pix = QPixmap(16, 16)
        pix.fill(QtCore.Qt.transparent)
        return pix
    elif role == ValueRole:
      return self.points[index.row()][index.column()]
    elif role == IDRole:
      return self.points[index.row()]['ID']
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

  def headerData(self, section, orientation, role):
    if role == QtCore.Qt.DisplayRole:
      return self.fields[section] if orientation == QtCore.Qt.Horizontal else section + 1
    return None

  def copyToClipboard(self, IDs):
    text = ''
    for i in IDs:
      text += '\t'.join([self.index(i, f).data() for f in GPXFIELDS]) + '\n'
    QGuiApplication.clipboard().setText(text)

  def getIndexesWithIncludeState(self, state):
    return [i for i,s in enumerate(self.includeStates) if s == state]

  def getNeglectStates(self):
    return [i for i,s in enumerate(self.neglectStates) if s]

  def getPointStyles(self, key):
    if key in {MARKER_COLOR, MARKER_STYLE, MARKER_SIZE}:
      return [p[key] for i,p in enumerate(self.pointStyles) if self.includeStates[i] in {INC_MARKER, INC_CAPTION}]
    if key in {LINE_COLOR, LINE_STYLE, LINE_WIDTH}:
      return [p[key] for i,p in enumerate(self.pointStyles) if self.splitStates[i]]
    if key in {CAPTION_POSX, CAPTION_POSY, CAPTION_SIZE}:
      return [p[key] for i,p in enumerate(self.pointStyles) if self.includeStates[i] == INC_CAPTION]

  def getSplitLines(self):
    return [i for i,s in enumerate(self.splitStates) if s]

  def resetModel(self):
    self.beginResetModel()
    self.points = []
    self.includeStates = []
    self.splitStates = []
    self.neglectStates = []
    self.pointStyles = []
    self.endResetModel()

  def setIncludeStates(self, IDs, state):
    for i in IDs:
      self.includeStates[i] = state
    self.updateDistance()

  def setNeglectStates(self, IDs, state):
    for i in IDs:
      self.neglectStates[i] = state
    self.updateDistance()

  def setPointStyle(self, IDs, key, value):
    for i in IDs:
      self.pointStyles[i][key] = value

  def setSplitLines(self, IDs, state):
    for i in IDs:
      self.splitStates[i] = state

  def parse(self, filename):
    self.resetModel()

    namespaces = {'ns0' : 'http://www.topografix.com/GPX/1/0',
                  'ns1' : 'http://www.topografix.com/GPX/1/1'}
    try:
      #ET.register_namespace('', ns['ns0'])
      doc = ET.parse(filename)
    except:
      raise GpxWarning(filename + self.tr(' is an invalid GPX file.'))

    ns = {'ns': namespaces['ns1']}
    data = doc.findall('.//{%(ns)s}wpt' % ns)
    if len(data) == 0:
      ns = {'ns': namespaces['ns0']}
      data = doc.findall('.//{%(ns)s}wpt' % ns)
    if len(data) == 0:
      raise GpxWarning(self.tr('GPX file is empty.'))

    id = 0
    minalt = 10000
    maxalt = 0
    while data[0].findtext('{%(ns)s}time' % ns) == None:
      del data[0]
    start = data[0]
    start_t = start.findtext('{%(ns)s}time' % ns).strip()
    try:
      start_dt = datetime.strptime(start_t, '%Y-%m-%dT%H:%M:%SZ')
    except ValueError as e:
      raise GpxWarning(self.tr('Waypoint time format is invalid.'))

    defaultStyle = {MARKER_COLOR: int(TheConfig['PointStyle']['MarkerColor']),
                    MARKER_STYLE: TheConfig['PointStyle']['MarkerStyle'],
                    MARKER_SIZE: int(TheConfig['PointStyle']['MarkerSize']),
                    LINE_COLOR: int(TheConfig['PointStyle']['SplitLineColor']),
                    LINE_STYLE: TheConfig['PointStyle']['SplitLineStyle'],
                    LINE_WIDTH: float(TheConfig['PointStyle']['SplitLineWidth']),
                    CAPTION_POSX: int(TheConfig['PointStyle']['CaptionPositionX']),
                    CAPTION_POSY: int(TheConfig['PointStyle']['CaptionPositionY']),
                    CAPTION_SIZE: int(TheConfig['PointStyle']['CaptionSize'])}

    for p in data:
      try:
        point = {}
        name = p.findtext('{%(ns)s}name' % ns)
        point[NAME] = name.strip() if name != None else ''
        point[LAT] = float(p.get('lat'))
        point[LON] = float(p.get('lon'))
        point[ALT] = int(round(float(p.findtext('{%(ns)s}ele' % ns))))
        minalt = min(minalt, point[ALT])
        maxalt = max(maxalt, point[ALT])
        dt = datetime.strptime(p.findtext('{%(ns)s}time' % ns).strip(), '%Y-%m-%dT%H:%M:%SZ')
        point[TIME] = dt
        time_delta = dt - start_dt
        point[TIMEDELTA] = time_delta
        point[TIME_DAYS] = round(time_delta.days + time_delta.seconds / 60.0 / 60.0 / 24.0, 3)
        point['ID'] = id

        self.beginInsertRows(QtCore.QModelIndex(), id, id)
        self.points += [point]
        self.includeStates += [INC_DEFAULT]
        self.splitStates += [False]
        self.neglectStates += [False]
        self.pointStyles += [defaultStyle.copy()]
        self.endInsertRows()
        id += 1

      except (TypeError, ValueError):
        print(self.tr('Waypoint ') + (point[NAME] + ' ' if point[NAME] != '' else '') + self.tr('is invalid and will be skipped.'))

    self.updateDistance()
    self.layoutChanged.emit()

    TheConfig['ProfileStyle']['MinimumAltitude'] = str(round(minalt, -3) - 500 if round(minalt, -3) > minalt else round(minalt, -3))
    TheConfig['ProfileStyle']['MaximumAltitude'] = str(round(maxalt, -3) + 500 if round(maxalt, -3) < maxalt else round(maxalt, -3))

  def updateDistance(self):
    for i in range(self.rowCount()):
      if self.index(i, 0).data(IncludeRole) != INC_SKIP:
        break
    prev_lat = float(self.index(i, LAT).data())
    prev_lon = float(self.index(i, LON).data())
    dist = 0.0

    for i in range(self.rowCount()):
      if self.index(i, 0).data(IncludeRole) != INC_SKIP:
        lat = float(self.index(i, LAT).data())
        lon = float(self.index(i, LON).data())

        if self.index(i, 0).data(NeglectRole):
          self.points[i][DIST] =  round(dist, 3)
        else:
          dist += _distance(lat, lon, prev_lat, prev_lon) * 1.2  # with mountain coefficient
          self.points[i][DIST] =  round(dist, 3)

        prev_lat = lat
        prev_lon = lon
      else:
        self.points[i][DIST] = ''


class GpxSortFilterModel(QtCore.QSortFilterProxyModel):
  def __init__(self, parent):
    super(GpxSortFilterModel, self).__init__(parent)

  def lessThan(self, left, right):
    if left.column() == TIME and right.column() == TIME:
      return datetime.strptime(left.data(), '%Y-%m-%d %H:%M:%S') < datetime.strptime(right.data(), '%Y-%m-%d %H:%M:%S')
    else:
      return super(GpxSortFilterModel, self).lessThan(left, right)


def _distance(lat1, lon1, lat2, lon2):
  Radius = 6378.14 # The equatorial radius of the Earth
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
