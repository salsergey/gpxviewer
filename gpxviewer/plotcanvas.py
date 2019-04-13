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

import webbrowser
from math import ceil
from PyQt5.QtCore import Qt, QCoreApplication, QEvent, QMargins, QSortFilterProxyModel, pyqtSignal, pyqtSlot
from PyQt5.QtGui import qAlpha, QColor, QCursor, QFont, QGuiApplication, QIcon, QPalette, QPen
from PyQt5.QtWidgets import QAction, QDialog, QMenu, QMessageBox, QSizePolicy
from qcustomplot import (QCP, QCustomPlot, QCPAxisTickerFixed, QCPDataRange, QCPDataSelection,
                         QCPGraph, QCPItemPosition, QCPItemText, QCPScatterStyle)
import gpxviewer.gpxmodel as gpx
from gpxviewer.configstore import TheConfig
from gpxviewer.gpxdocument import TheDocument
from gpxviewer.pointconfigdialog import PointConfigDialog


class PlotCanvas(QCustomPlot):
  def __init__(self, parent=None):
    super(QCustomPlot, self).__init__(parent)
    self.font = QFont()
    self.font.setStyleHint(QFont.SansSerif)

    self.axisRect().setupFullAxesBox(True)
    self.xTicker = AxisTicker(Qt.Horizontal)
    self.xAxis.setTicker(self.xTicker)
    self.xTicker2 = AxisTicker(Qt.Horizontal)
    self.xAxis2.setTicker(self.xTicker2)
    self.yTicker = AxisTicker(Qt.Vertical)
    self.yAxis.setTicker(self.yTicker)
    self.yTicker2 = AxisTicker(Qt.Vertical)
    self.yAxis2.setTicker(self.yTicker2)

    self.xAxis.grid().setVisible(False)
    gridColor = QColor(Qt.gray)
    gridColor.setAlpha(150)
    self.yAxis.grid().setPen(QPen(gridColor, 1, Qt.DashLine))

    self.addLayer('profile', self.layer('main'), QCustomPlot.limBelow)

    self.setInteraction(QCP.iSelectItems)
    self.setInteraction(QCP.iSelectPlottables)

    self.selectionChangedByUser.connect(self.onSelectionChanged)

  def deselectAll(self):
    super(PlotCanvas, self).deselectAll()
    self.onSelectionChanged()

  def removeGraph(self, graph):
    if graph.selected():
      self.deselectAll()
    super(PlotCanvas, self).removeGraph(graph)

  def removeItem(self, item):
    if item.selected():
      self.deselectAll()
    super(PlotCanvas, self).removeItem(item)

  def reset(self):
    self.clearPlottables()
    self.clearItems()

    self.selectedElement = None
    self.xx = []
    self.yy = []
    self.markers = []
    self.captions = []
    self.splitLines = []
    self.neglectPoints = [0]

  def updatePoints(self, wptRows, trkRows):
    zeroDist = 0
    for p in TheDocument.gpxparser.points:
      if type(p) == int:  # points
        if (p in wptRows or len(wptRows) == 0) and (self.column == gpx.DIST or TheDocument.wptmodel.index(p, self.column).data() != ''):
          self.xx += [float(TheDocument.wptmodel.index(p, self.column).data()) - zeroDist]
          self.yy += [float(TheDocument.wptmodel.index(p, gpx.ALT).data())]
          if len(self.xx) == 1:
            zeroDist = self.xx[0]
            self.xx[0] = 0
          if p != 0 and TheDocument.wptmodel.index(p, 0).data(gpx.NeglectRole):
            self.neglectPoints += [self.xx[-1]]
          if TheDocument.wptmodel.index(p, 0).data(gpx.SplitLineRole):
            self.splitLines += [SplitLine(self, p, self.xx[-1], self.yy[-1])]
          if TheDocument.wptmodel.index(p, 0).data(gpx.MarkerRole):
            self.markers += [MarkerItem(self, p, self.xx[-1], self.yy[-1])]
          if TheDocument.wptmodel.index(p, 0).data(gpx.CaptionRole):
            self.captions += [CaptionItem(self, p, self.xx[-1], self.yy[-1])]
      elif p[0] in trkRows or len(trkRows) == 0 and len(wptRows) == 0:  # tracks
        if self.column == gpx.DIST or TheDocument.trkmodel.index(p[0], gpx.TRKTIME).data() != '':
          self.xx += [float(TheDocument.trkmodel.tracks[p[0]]['SEGMENTS'][p[1]][p[2]][self.column]) - zeroDist]
          self.yy += [float(TheDocument.trkmodel.tracks[p[0]]['SEGMENTS'][p[1]][p[2]][gpx.ALT])]
          if len(self.xx) == 1:
            zeroDist = self.xx[0]
            self.xx[0] = 0
    self.neglectPoints += [self.xx[-1]]

    if TheConfig.getValue('ProfileStyle', 'AutoscaleAltitudes'):
      minalt, maxalt = min(self.yy), max(self.yy)
      self.minalt = int(round(minalt, -3) - 500 if round(minalt, -3) > minalt else round(minalt, -3))
      self.maxalt = int(round(maxalt, -3) + 500 if round(maxalt, -3) < maxalt else round(maxalt, -3))
    else:
      self.minalt = TheConfig.getValue('ProfileStyle', 'MinimumAltitude')
      self.maxalt = TheConfig.getValue('ProfileStyle', 'MaximumAltitude')

  def updateAxes(self):
    self.xAxis.setRangeUpper(self.xx[-1])
    self.yAxis.setRange(self.minalt, self.maxalt)
    self.xTicker.setType(self.column)

    self.font.setFamily(TheConfig.getValue('ProfileStyle', 'FontFamily'))
    self.font.setPointSize(TheConfig.getValue('ProfileStyle', 'FontSize'))
    self.xAxis.setTickLabelFont(self.font)
    self.xAxis.setLabelFont(self.font)
    self.yAxis.setTickLabelFont(self.font)
    self.yAxis.setLabelFont(self.font)

    if self.column == gpx.DIST:
      dist_coeff = TheConfig.getValue('ProfileStyle', 'DistanceCoefficient')
      if dist_coeff == 1.0:
        self.xAxis.setLabel(self.tr('Distance (km)'))
      else:
        self.xAxis.setLabel(self.tr('Distance with coefficient ') + str(dist_coeff) + self.tr(' (km)'))
    else:  # time
      if self.xx[-1] > 1:
        self.xAxis.setLabel(self.tr('Time (days)'))
      else:
        self.xAxis.setLabel(self.tr('Time (hours)'))
    self.yAxis.setLabel(self.tr('Altitude (m)'))

  def plotProfile(self, column, wptRows, trkRows):
    self.column = column
    self.reset()
    self.setCurrentLayer('main')
    self.updatePoints(wptRows, trkRows)
    self.updateAxes()

    self.setCurrentLayer('profile')
    for n in range(1, len(self.neglectPoints)):
      self.addGraph()
      self.graph().setPen(QPen(QColor.fromRgba(TheConfig.getValue('ProfileStyle', 'ProfileColor')),
                               TheConfig.getValue('ProfileStyle', 'ProfileWidth'), Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
      self.graph().setBrush(QColor.fromRgba(TheConfig.getValue('ProfileStyle', 'FillColor')))
      self.graph().setData(self.xx[self.xx.index(self.neglectPoints[n-1]) + (1 if n > 1 else 0):self.xx.index(self.neglectPoints[n]) + 1],
                           self.yy[self.xx.index(self.neglectPoints[n-1]) + (1 if n > 1 else 0):self.xx.index(self.neglectPoints[n]) + 1])
      self.graph().setSelectable(False)

    self.replot()

  def saveProfile(self, filename, figsize=None):
    self.deselectAll()
    if figsize is None:
      figsize = self.width(), self.height()

    if filename.lower().endswith('.pdf'):
      result = self.savePdf(filename, figsize[0], figsize[1], QCP.epNoCosmetic, QCoreApplication.applicationName())
    else:
      result = self.saveRastered(filename, figsize[0], figsize[1], 1, None)
    self.replot()

    if not result:
      QMessageBox.warning(self, self.tr('Save error'), self.tr('Error writing file ') + filename +
                          self.tr('.\nProbably the given format isn\'t supported by the system.'))

  def keyPressEvent(self, event):
    if event.key() == Qt.Key_Escape:
      if self.selectedElement is not None:
        self.deselectAll()
        self.replot()
      else:
        super(PlotCanvas, self).keyPressEvent(event)
    elif event.key() == Qt.Key_Menu and self.selectedElement is not None:
      self.contextMenu()
    elif event.key() in {Qt.Key_Left, Qt.Key_Right, Qt.Key_Down, Qt.Key_Up} and len(self.selectedItems()) == 1:
      x = TheDocument.wptmodel.index(self.selectedElement.idx, gpx.NAME).data(gpx.CaptionStyleRole)[gpx.CAPTION_POSX]
      y = TheDocument.wptmodel.index(self.selectedElement.idx, gpx.NAME).data(gpx.CaptionStyleRole)[gpx.CAPTION_POSY]
      if event.key() == Qt.Key_Left:
        TheDocument.wptmodel.setPointStyle([self.selectedElement.idx], gpx.CAPTION_POSX, x - 1)
      elif event.key() == Qt.Key_Right:
        TheDocument.wptmodel.setPointStyle([self.selectedElement.idx], gpx.CAPTION_POSX, x + 1)
      elif event.key() == Qt.Key_Down:
        TheDocument.wptmodel.setPointStyle([self.selectedElement.idx], gpx.CAPTION_POSY, y - 1)
      elif event.key() == Qt.Key_Up:
        TheDocument.wptmodel.setPointStyle([self.selectedElement.idx], gpx.CAPTION_POSY, y + 1)
      self.replot()
    else:
      super(PlotCanvas, self).keyPressEvent(event)

  def mouseReleaseEvent(self, event):
    if event.button() == Qt.RightButton:
      self.deselectAll()
      item = self.itemAt(event.pos())
      if item is None:
        item = self.plottableAt(event.pos(), True)
      if item is not None:
        item.setSelected(True)
        self.onSelectionChanged()
        self.contextMenu()
      self.replot()
    super(PlotCanvas, self).mouseReleaseEvent(event)

  def wheelEvent(self, event):
    if event.pos().x() < self.axisRect().rect().left():
      if event.pos().y() < self.axisRect().rect().center().y():
        self.maxalt = max(self.maxalt + (100 if event.angleDelta().y() > 0 else -100), self.minalt + 100)
      else:
        self.minalt = min(self.minalt + (100 if event.angleDelta().y() > 0 else -100), self.maxalt - 100)
      if not TheConfig.getValue('ProfileStyle', 'AutoscaleAltitudes'):
        TheConfig['ProfileStyle']['MinimumAltitude'] = str(self.minalt)
        TheConfig['ProfileStyle']['MaximumAltitude'] = str(self.maxalt)
      self.updateAxes()
      self.replot()
      self.profileChanged.emit()
    super(PlotCanvas, self).wheelEvent(event)

  def contextMenu(self):
    actMarker = QAction(QIcon(':/icons/waypoint-marker.svg'), self.tr('Points with markers'), self)
    actMarker.setCheckable(True)
    actMarker.setChecked(TheDocument.wptmodel.index(self.selectedElement.idx, gpx.NAME).data(gpx.MarkerRole))
    actMarker.triggered.connect(self.onMarkerPoints)
    actCaption = QAction(QIcon(':/icons/waypoint-caption.svg'), self.tr('Points with captions'), self)
    actCaption.setCheckable(True)
    actCaption.setChecked(TheDocument.wptmodel.index(self.selectedElement.idx, gpx.NAME).data(gpx.CaptionRole))
    actCaption.triggered.connect(self.onCaptionPoints)
    actSplit = QAction(QIcon(':/icons/waypoint-splitline.svg'), self.tr('Points with splitting lines'), self)
    actSplit.setCheckable(True)
    actSplit.setChecked(TheDocument.wptmodel.index(self.selectedElement.idx, gpx.NAME).data(gpx.SplitLineRole))
    actSplit.triggered.connect(self.onSplitLines)
    actStyle = QAction(QIcon(':/icons/configure.svg'), self.tr('Point style'), self)
    actStyle.triggered.connect(self.onPointStyle)

    menu = QMenu(self)
    menu.addAction(actMarker)
    menu.addAction(actCaption)
    menu.addAction(actSplit)
    menu.addSeparator()
    menu.addAction(actStyle)
    menu.addSeparator()

    actShowGoogleMap = QAction(QIcon(':/icons/googlemaps.png'), self.tr('Google Maps'), self)
    actShowGoogleMap.triggered.connect(self.showGoogleMap)
    actShowYandexMap = QAction(QIcon(':/icons/yandexmaps.png'), self.tr('Yandex Maps'), self)
    actShowYandexMap.triggered.connect(self.showYandexMap)
    actShowZoomEarthMap = QAction(QIcon(':/icons/zoomearth.png'), self.tr('Zoom Earth'), self)
    actShowZoomEarthMap.triggered.connect(self.showZoomEarthMap)
    actShowOpenCycleMap = QAction(QIcon(':/icons/openstreetmap.png'), self.tr('OpenCycleMap'), self)
    actShowOpenCycleMap.triggered.connect(self.showOpenCycleMap)
    actShowOpenTopoMap = QAction(QIcon(':/icons/opentopomap.png'), self.tr('OpenTopoMap'), self)
    actShowOpenTopoMap.triggered.connect(self.showOpenTopoMap)
    actShowTopoMap = QAction(QIcon(':/icons/loadmap.png'), self.tr('Loadmap.net'), self)
    actShowTopoMap.triggered.connect(self.showTopoMap)

    showMapMenu = QMenu(self.tr('Show on map'), self)
    showMapMenu.setIcon(QIcon(':/icons/internet-services.svg'))
    showMapMenu.addAction(actShowGoogleMap)
    showMapMenu.addAction(actShowYandexMap)
    showMapMenu.addAction(actShowZoomEarthMap)
    showMapMenu.addAction(actShowOpenCycleMap)
    showMapMenu.addAction(actShowOpenTopoMap)
    showMapMenu.addAction(actShowTopoMap)
    menu.addMenu(showMapMenu)
    menu.popup(QCursor.pos())

  @pyqtSlot()
  def onMarkerPoints(self):
    checked = self.sender().isChecked()
    TheDocument.wptmodel.setMarkerStates([self.selectedElement.idx], checked)
    if checked:
      self.markers += [MarkerItem(self, self.selectedElement.idx, self.selectedElement.posX, self.selectedElement.posY)]
    else:
      for i, m in enumerate(self.markers):
        if m.idx == self.selectedElement.idx:
          self.removeGraph(m)
          del self.markers[i]
          break
    self.replot()

  @pyqtSlot()
  def onCaptionPoints(self):
    checked = self.sender().isChecked()
    TheDocument.wptmodel.setCaptionStates([self.selectedElement.idx], checked)
    if checked:
      self.captions += [CaptionItem(self, self.selectedElement.idx, self.selectedElement.posX, self.selectedElement.posY)]
    else:
      for i, c in enumerate(self.captions):
        if c.idx == self.selectedElement.idx:
          self.removeItem(c)
          del self.captions[i]
          break
    self.replot()

  @pyqtSlot()
  def onSplitLines(self):
    checked = self.sender().isChecked()
    TheDocument.wptmodel.setSplitLines([self.selectedElement.idx], checked)
    if checked:
      self.splitLines += [SplitLine(self, self.selectedElement.idx, self.selectedElement.posX, self.selectedElement.posY)]
    else:
      for i, l in enumerate(self.splitLines):
        if l.idx == self.selectedElement.idx:
          self.removeGraph(l)
          del self.splitLines[i]
          break
    self.replot()

  def onPointStyle(self):
    dlg = PointConfigDialog(self, self.selectedElement.idx)
    if dlg.exec_() == QDialog.Accepted:
      self.replot()

  @pyqtSlot()
  def showGoogleMap(self):
    lat = TheDocument.wptmodel.index(self.selectedElement.idx, gpx.LAT).data()
    lon = TheDocument.wptmodel.index(self.selectedElement.idx, gpx.LON).data()
    webbrowser.open('https://maps.google.com/maps?ll=' + lat + ',' + lon + '&t=h&q=' + lat + ',' + lon + '&z=15')

  @pyqtSlot()
  def showYandexMap(self):
    lat = TheDocument.wptmodel.index(self.selectedElement.idx, gpx.LAT).data()
    lon = TheDocument.wptmodel.index(self.selectedElement.idx, gpx.LON).data()
    webbrowser.open('https://maps.yandex.ru?ll=' + lon + ',' + lat + '&spn=0.03,0.03&pt=' + lon + ',' + lat + '&l=sat')

  @pyqtSlot()
  def showZoomEarthMap(self):
    lat = TheDocument.wptmodel.index(self.selectedElement.idx, gpx.LAT).data()
    lon = TheDocument.wptmodel.index(self.selectedElement.idx, gpx.LON).data()
    webbrowser.open('https://zoom.earth/#' + lat + ',' + lon + ',15z,map')

  @pyqtSlot()
  def showOpenCycleMap(self):
    lat = TheDocument.wptmodel.index(self.selectedElement.idx, gpx.LAT).data()
    lon = TheDocument.wptmodel.index(self.selectedElement.idx, gpx.LON).data()
    webbrowser.open('https://openstreetmap.org/?mlat=' + lat + '&mlon=' + lon + '&zoom=15&layers=C')

  @pyqtSlot()
  def showOpenTopoMap(self):
    lat = TheDocument.wptmodel.index(self.selectedElement.idx, gpx.LAT).data()
    lon = TheDocument.wptmodel.index(self.selectedElement.idx, gpx.LON).data()
    webbrowser.open('https://opentopomap.org/#marker=15/' + lat + '/' + lon)

  @pyqtSlot()
  def showTopoMap(self):
    lat = TheDocument.wptmodel.index(self.selectedElement.idx, gpx.LAT).data()
    lon = TheDocument.wptmodel.index(self.selectedElement.idx, gpx.LON).data()
    webbrowser.open('http://loadmap.net/ru?q=' + lat + ' ' + lon + '&z=13&s=0')

  @pyqtSlot()
  def onSelectionChanged(self):
    if len(self.selectedItems()) == 1:
      self.selectedElement = self.selectedItems()[0]
    elif len(self.selectedPlottables()) == 1:
      self.selectedElement = self.selectedPlottables()[0]
    else:
      self.selectedElement = None

  profileChanged = pyqtSignal()


class AxisTicker(QCPAxisTickerFixed):
  def __init__(self, orientation):
    super(AxisTicker, self).__init__()
    self.orientation = orientation
    self.type = gpx.DIST

  def setType(self, type):
    self.type = type

  def getTickStep(self, range):
    if self.orientation == Qt.Horizontal:
      if self.type == gpx.DIST:
        if range.upper > 200:
          return 20
        elif range.upper > 100:
          return 10
        elif range.upper > 50:
          return 5
        elif range.upper > 20:
          return 2
        else:
          return 1
      else:  # time
        if range.upper > 1:  # days
          return 1
        else:  # hours
          return 1.0 / 24
    else:  # vertical
      if range.size() >= 2000:
        return 500
      elif range.size() >= 1000:
        return 200
      else:
        return 100

  def getSubTickCount(self, tickStep):
    if self.orientation == Qt.Horizontal:
      if self.type == gpx.DIST and tickStep % 2 == 0:
        return 1
      else:
        return 0
    else:  # vertical
      return int(tickStep / 100) - 1

  def createLabelVector(self, ticks, locale, formatChar, precision):
    if self.orientation == Qt.Horizontal and self.type == gpx.TIME_DAYS and ticks[-1] <= 1:  # hours
      return [str(int(round(24 * t))) for t in ticks]
    else:
      return super(AxisTicker, self).createLabelVector(ticks, locale, formatChar, precision)


class MarkerItem(QCPGraph):
  def __init__(self, parent, idx, x, y):
    super(MarkerItem, self).__init__(parent.xAxis, parent.yAxis)
    self.idx = idx
    self.posX, self.posY = x, y
    self.setData([self.posX], [self.posY])
    self.setLineStyle(QCPGraph.lsNone)

  def setSelected(self, selected):
    self.setSelection(QCPDataSelection(QCPDataRange(0, 1)) if selected else QCPDataSelection())

  def draw(self, painter):
    self.updateStyle()
    super(MarkerItem, self).draw(painter)

  def updateStyle(self):
    markerStyle = TheDocument.wptmodel.index(self.idx, gpx.NAME).data(gpx.MarkerStyleRole)
    scatterStyle = QCPScatterStyle()
    scatterStyle.setCustomPath(gpx.markerPath(markerStyle[gpx.MARKER_STYLE], 2 * markerStyle[gpx.MARKER_SIZE]))  # for better compatibility with matplotlib
    scatterStyle.setBrush(QColor.fromRgba(markerStyle[gpx.MARKER_COLOR]))
    if markerStyle[gpx.MARKER_STYLE] in {'1', '2', '3', '4', '+', 'x', '_', '|'}:
      scatterStyle.setPen(QPen(QColor.fromRgba(markerStyle[gpx.MARKER_COLOR]), 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
    else:
      scatterStyle.setPen(QPen(QColor.fromRgba(markerStyle[gpx.MARKER_COLOR]), 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
    self.setScatterStyle(scatterStyle)

    selectedScatterStyle = QCPScatterStyle()
    selectedScatterStyle.setCustomPath(gpx.markerPath(markerStyle[gpx.MARKER_STYLE], 3 * markerStyle[gpx.MARKER_SIZE]))
    selectedScatterStyle.setPen(QPen(QGuiApplication.palette().color(QPalette.Highlight), 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
    self.selectionDecorator().setScatterStyle(selectedScatterStyle)
    self.selectionDecorator().setUsedScatterProperties(QCPScatterStyle.ScatterProperty(QCPScatterStyle.spPen | QCPScatterStyle.spShape))


class CaptionItem(QCPItemText):
  def __init__(self, parent, idx, x, y):
    super(CaptionItem, self).__init__(parent)
    self.idx = idx
    self.posX, self.posY = x, y
    self.font = QFont()
    self.font.setStyleHint(QFont.SansSerif)
    self.font.setFamily(TheConfig.getValue('ProfileStyle', 'FontFamily'))
    self.setText(TheDocument.wptmodel.index(self.idx, gpx.NAME).data())

    self.setClipToAxisRect(False)
    self.setPadding(QMargins(3, 1, 3, 1))
    self.setRotation(-90)
    self.setPositionAlignment(Qt.AlignLeft | Qt.AlignVCenter)
    self.position.setType(QCPItemPosition.ptPlotCoords)

    fillColor = QGuiApplication.palette().color(QPalette.Highlight)
    fillColor.setAlpha(100)
    self.setSelectedBrush(fillColor)
    self.setSelectedPen(QGuiApplication.palette().color(QPalette.Highlight))
    self.setSelectedColor(QColor(Qt.black))

  def draw(self, painter):
    self.update()
    super(CaptionItem, self).draw(painter)

  def update(self):
    self.font.setPointSize(TheDocument.wptmodel.index(self.idx, gpx.NAME).data(gpx.CaptionStyleRole)[gpx.CAPTION_SIZE])
    self.setFont(self.font)
    self.setSelectedFont(self.font)

    xscale = float(self.parentPlot().xAxis.range().size()) / self.parentPlot().axisRect().width()
    yscale = float(self.parentPlot().yAxis.range().size()) / self.parentPlot().axisRect().height()
    captionStyle = TheDocument.wptmodel.index(self.idx, gpx.NAME).data(gpx.CaptionStyleRole)
    self.position.setCoords((self.posX / xscale + captionStyle[gpx.CAPTION_POSX]) * xscale,
                            (self.posY / yscale + captionStyle[gpx.CAPTION_POSY]) * yscale)


class SplitLine(QCPGraph):
  def __init__(self, parent, idx, x, y):
    super(SplitLine, self).__init__(parent.xAxis, parent.yAxis)
    self.idx = idx
    self.posX, self.posY = x, y
    self.setData([self.posX] * 2, [0, self.posY])
    self.setSelectable(False)

  def draw(self, painter):
    self.updateStyle()
    super(SplitLine, self).draw(painter)

  def updateStyle(self):
    splitLineStyle = TheDocument.wptmodel.index(self.idx, gpx.NAME).data(gpx.SplitLineStyleRole)
    slPen = QPen(QColor.fromRgba(splitLineStyle[gpx.LINE_COLOR]), splitLineStyle[gpx.LINE_WIDTH])
    if splitLineStyle[gpx.LINE_STYLE] == '-':
      slPen.setStyle(Qt.SolidLine)
    elif splitLineStyle[gpx.LINE_STYLE] == '--':
      slPen.setStyle(Qt.DashLine)
    elif splitLineStyle[gpx.LINE_STYLE] == '-.':
      slPen.setStyle(Qt.DashDotLine)
    elif splitLineStyle[gpx.LINE_STYLE] == ':':
      slPen.setStyle(Qt.DotLine)
    self.setPen(slPen)
