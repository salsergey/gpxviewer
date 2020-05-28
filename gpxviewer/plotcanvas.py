# gpxviewer
#
# Copyright (C) 2016-2020 Sergey Salnikov <salsergey@gmail.com>
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
from datetime import timedelta
from PyQt5.QtCore import Qt, QCoreApplication, QDate, QDateTime, QFileSelector, QMargins, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QColor, QCursor, QFont, QGuiApplication, QIcon, QPen
from PyQt5.QtWidgets import QAction, QDialog, QMenu, QMessageBox
from QCustomPlot2 import (QCP, QCustomPlot, QCPAxisTickerDateTime, QCPAxisTickerFixed, QCPDataRange, QCPDataSelection,
                          QCPGraph, QCPItemPosition, QCPItemText, QCPItemTracer, QCPScatterStyle, QCPTextElement)
import gpxviewer.gpxmodel as gpx
from gpxviewer.configstore import TheConfig
from gpxviewer.gpxdocument import TheDocument
from gpxviewer.pointconfigdialog import PointConfigDialog


class PlotCanvas(QCustomPlot):
  def __init__(self, parent=None):
    super(QCustomPlot, self).__init__(parent)

    self.leftButtonPressed = False
    self.rightButtonPressed = False
    self.font = QFont()
    self.font.setStyleHint(QFont.SansSerif)
    self.themeSelector = QFileSelector()
    self.themeSelector.setExtraSelectors([TheConfig['MainWindow']['ColorTheme']])

    self.addLayer('profile', self.layer('main'), QCustomPlot.limBelow)

    self.setInteraction(QCP.iSelectItems)
    self.setInteraction(QCP.iSelectPlottables)
    self.setInteraction(QCP.iRangeDrag)
    self.setInteraction(QCP.iRangeZoom)
    self.axisRect().setRangeDrag(Qt.Horizontal)
    self.axisRect().setRangeZoom(Qt.Horizontal)

    self.axisRect().setupFullAxesBox(True)
    self.xAxis.setTickLabelPadding(10)
    self.yAxis.setTickLabelPadding(10)
    self.xAxis.grid().setVisible(False)

    self.xTicker = AxisTicker(Qt.Horizontal)
    self.xAxis.setTicker(self.xTicker)
    self.xAxis2.setTicker(self.xTicker)
    self.yTicker = AxisTicker(Qt.Vertical)
    self.yAxis.setTicker(self.yTicker)
    self.yAxis2.setTicker(self.yTicker)

    self.showInfo = False
    self.setAutoAddPlottableToLegend(False)
    self.xLegendText = QCPTextElement(self)
    self.yLegendText = QCPTextElement(self)
    self.xLegendText.setMinimumSize(200, 0)
    self.yLegendText.setMinimumSize(200, 0)
    self.xLegendText.setLayer(self.legend.layer())
    self.yLegendText.setLayer(self.legend.layer())
    self.legend.addElement(self.xLegendText)
    self.legend.addElement(self.yLegendText)
    self.xLegendText.setMargins(QMargins(10, 5, 10, 5))
    self.yLegendText.setMargins(QMargins(10, 5, 10, 5))

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
    self.infoMarkers = []
    self.captions = []
    self.splitLines = []
    self.neglectPoints = []

  def fitWidth(self):
    self.xAxis.setRange(self.xx[0], self.xx[-1])
    self.replot()

  def updatePoints(self):
    if TheConfig.getValue('ProfileStyle', 'SelectedPointsOnly') \
       and TheConfig.getValue('ProfileStyle', 'StartFromZero') \
       and self.column in {gpx.DIST, gpx.TIME_DAYS} and len(self.wptRows) != 0:
      startDist = float(TheDocument.wptmodel.index(self.wptRows[0], self.column).data())
    else:
      startDist = 0

    for p in TheDocument.gpxparser.points:
      if type(p) == int:  # points
        if (p in self.wptRows or len(self.wptRows) == 0) \
           and (self.column == gpx.DIST or TheDocument.wptmodel.index(p, self.column).data() != ''):
          if self.column in {gpx.DIST, gpx.TIME_DAYS}:
            self.xx += [float(TheDocument.wptmodel.index(p, self.column).data()) - startDist]
          else:  # absolute time
            self.xx += [QCPAxisTickerDateTime.dateTimeToKey(QDateTime.fromString(
                        TheDocument.wptmodel.index(p, self.column).data(), 'yyyy-MM-dd HH:mm:ss'))]
          self.yy += [float(TheDocument.wptmodel.index(p, gpx.ALT).data())]
          if p != 0 and self.column == gpx.DIST and TheDocument.wptmodel.index(p, 0).data(gpx.NeglectRole):
            self.neglectPoints += [self.xx[-1]]
          if TheDocument.wptmodel.index(p, 0).data(gpx.SplitLineRole):
            self.splitLines += [SplitLine(self, p, self.xx[-1], self.yy[-1])]
          if TheDocument.wptmodel.index(p, 0).data(gpx.MarkerRole):
            self.markers += [MarkerItem(self, p, self.xx[-1], self.yy[-1])]
          else:
            self.infoMarkers += [MarkerItem(self, p, self.xx[-1], self.yy[-1])]
            self.infoMarkers[-1].setVisible(False)
          if TheDocument.wptmodel.index(p, 0).data(gpx.CaptionRole):
            self.captions += [CaptionItem(self, p, self.xx[-1], self.yy[-1])]
      elif p[0] in self.trkRows or len(self.trkRows) == 0 and len(self.wptRows) == 0:  # tracks
        if self.column == gpx.DIST or TheDocument.trkmodel.index(p[0], gpx.TRKTIME).data() != '':
          if self.column in {gpx.DIST, gpx.TIME_DAYS}:
            self.xx += [float(TheDocument.trkmodel.tracks[p[0]]['SEGMENTS'][p[1]][p[2]][self.column]) - startDist]
          else:  # absolute time
            # Convert track time to a proper timezone
            self.xx += [QCPAxisTickerDateTime.dateTimeToKey(QDateTime.fromString(
                        str(TheDocument.trkmodel.tracks[p[0]]['SEGMENTS'][p[1]][p[2]][self.column]
                            + timedelta(minutes=TheConfig.getValue('ProfileStyle', 'TimeZoneOffset'))), 'yyyy-MM-dd HH:mm:ss'))]
          self.yy += [float(TheDocument.trkmodel.tracks[p[0]]['SEGMENTS'][p[1]][p[2]][gpx.ALT])]
    self.neglectPoints = [self.xx[0]] + self.neglectPoints + [self.xx[-1]]

    if TheConfig.getValue('ProfileStyle', 'AutoscaleAltitudes'):
      minalt, maxalt = min(self.yy), max(self.yy)
      self.minalt = int(round(minalt, -3) - 500 if round(minalt, -3) > minalt else round(minalt, -3))
      self.maxalt = int(round(maxalt, -3) + 500 if round(maxalt, -3) < maxalt else round(maxalt, -3))
    else:
      self.minalt = TheConfig.getValue('ProfileStyle', 'MinimumAltitude')
      self.maxalt = TheConfig.getValue('ProfileStyle', 'MaximumAltitude')

  def updateAxes(self):
    if TheConfig.getValue('ProfileStyle', 'UseSystemTheme'):
      textColor = QGuiApplication.palette().text().color()
      self.setBackground(QGuiApplication.palette().base())
      self.legend.setBorderPen(textColor)
      self.legend.setBrush(QGuiApplication.palette().base())
      gridColor = QGuiApplication.palette().light().color() if TheConfig['MainWindow']['ColorTheme'] == 'dark_theme' \
             else QGuiApplication.palette().mid().color()
    else:
      textColor = QColor(Qt.black)
      self.setBackground(QColor(Qt.white))
      self.legend.setBorderPen(textColor)
      self.legend.setBrush(QColor(Qt.white))
      gridColor = QColor(Qt.gray)

    for axis in {self.xAxis, self.xAxis2, self.yAxis, self.yAxis2}:
      axis.setBasePen(QPen(textColor))
      axis.setTickPen(QPen(textColor))
      axis.setSubTickPen(QPen(textColor))
      axis.setLabelColor(textColor)
      axis.setTickLabelColor(textColor)
    gridColor.setAlpha(150)
    self.yAxis.grid().setPen(QPen(gridColor, 1, Qt.DashLine))

    self.yAxis.setRange(self.minalt, self.maxalt)
    self.xTicker.setType(self.column)

    self.font.setFamily(TheConfig.getValue('ProfileStyle', 'FontFamily'))
    self.font.setPointSize(TheConfig.getValue('ProfileStyle', 'FontSize'))
    self.xAxis.setTickLabelFont(self.font)
    self.xAxis.setLabelFont(self.font)
    self.yAxis.setTickLabelFont(self.font)
    self.yAxis.setLabelFont(self.font)

    for text in {self.xLegendText, self.yLegendText}:
      text.setFont(self.font)
      text.setTextColor(textColor)

    if self.column == gpx.TIME:
      self.xAxis.setTickLabelRotation(-90)
    else:
      self.xAxis.setTickLabelRotation(0)

    if self.column == gpx.DIST:
      dist_coeff = TheConfig.getValue('ProfileStyle', 'DistanceCoefficient')
      if dist_coeff != 1.0 and TheConfig.getValue('ProfileStyle', 'ShowDistanceCoefficient'):
        self.xAxis.setLabel(self.tr('Distance with coefficient ') + str(dist_coeff) + self.tr(' (km)'))
      else:
        self.xAxis.setLabel(self.tr('Distance (km)'))
    else:  # time
      if self.xx[-1] - self.xx[0] > 1:
        self.xAxis.setLabel(self.tr('Time (days)'))
      else:
        self.xAxis.setLabel(self.tr('Time (hours)'))
    self.yAxis.setLabel(self.tr('Altitude (m)'))

  def plotProfile(self, column, wptRows, trkRows, fit=True):
    self.column = column
    self.wptRows = wptRows
    self.trkRows = trkRows
    self.reset()
    self.setCurrentLayer('main')
    self.updatePoints()
    self.updateAxes()
    if fit:
      self.fitWidth()

    self.setCurrentLayer('profile')
    for n in range(1, len(self.neglectPoints)):
      self.addGraph()
      self.graph().setPen(QPen(QColor.fromRgba(TheConfig.getValue('ProfileStyle', 'ProfileColor')),
                               TheConfig.getValue('ProfileStyle', 'ProfileWidth'), Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
      self.graph().setBrush(QColor.fromRgba(TheConfig.getValue('ProfileStyle', 'FillColor')))
      self.graph().setData(self.xx[self.xx.index(self.neglectPoints[n-1]) + (1 if n > 1 else 0):self.xx.index(self.neglectPoints[n]) + 1],
                           self.yy[self.xx.index(self.neglectPoints[n-1]) + (1 if n > 1 else 0):self.xx.index(self.neglectPoints[n]) + 1])
      self.graph().setSelectable(False)

    self.setCurrentLayer('main')
    if self.showInfo:
      self.showInformation(True)
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

  def showInformation(self, enable):
    if enable:
      self.tracer = QCPItemTracer(self)
      self.tracer.setSelectable(False)
      lineColor = QGuiApplication.palette().text().color() if TheConfig.getValue('ProfileStyle', 'UseSystemTheme') else QColor(Qt.black)
      self.tracer.setPen(QPen(lineColor))

    self.showInfo = enable
    self.tracer.setVisible(enable)
    self.legend.setVisible(enable)
    for m in self.infoMarkers:
      m.setVisible(enable)
      m.setSelectable(enable)
    self.deselectAll()
    self.replot()

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

  def mouseMoveEvent(self, event):
    # Show information
    if self.showInfo and self.axisRect().rect().contains(event.pos()):
      for profile in self.layer('profile').children():
        if profile.getKeyRange()[0].contains(self.xAxis.pixelToCoord(event.pos().x())):
          self.tracer.setGraph(profile)
      self.tracer.setGraphKey(self.xAxis.pixelToCoord(event.pos().x()))
      self.replot()
      if self.column == gpx.DIST:
        self.xLegendText.setText(self.tr('Distance: ') + str(round(self.tracer.position.key(), 3)))
      elif self.column == gpx.TIME_DAYS:
        self.xLegendText.setText(self.tr('Time: ') + str(round(self.tracer.position.key(), 3)))
      else:  # absolute time
        self.xLegendText.setText(self.tr('Time: ') +
                                 QCPAxisTickerDateTime.keyToDateTime(self.tracer.position.key()).toString('yyyy-MM-dd HH:mm:ss'))
      self.yLegendText.setText(self.tr('Altitude: ') + str(round(self.tracer.position.value())))
      self.replot()

    self.updateCursorShape(event.pos())
    self.rightButtonPressed = False

    super(PlotCanvas, self).mouseMoveEvent(event)

  def mousePressEvent(self, event):
    if event.button() == Qt.LeftButton:
      self.leftButtonPressed = True
      if self.plottableAt(event.pos(), True) is None and self.itemAt(event.pos(), True) is None:
        self.setCursor(QCursor(Qt.ClosedHandCursor))
    elif event.button() == Qt.RightButton:
      self.rightButtonPressed = True

    super(PlotCanvas, self).mousePressEvent(event)

  def mouseReleaseEvent(self, event):
    if event.button() == Qt.LeftButton:
      self.leftButtonPressed = False
      self.updateCursorShape(event.pos())

    if event.button() == Qt.RightButton and self.rightButtonPressed and not self.leftButtonPressed:
      self.rightButtonPressed = False
      self.deselectAll()
      item = self.itemAt(event.pos(), True)
      if item is None:
        item = self.plottableAt(event.pos(), True)
      if item is not None:
        item.setSelected(True)
        self.onSelectionChanged()
        self.contextMenu()
      self.replot()

    super(PlotCanvas, self).mouseReleaseEvent(event)

  def wheelEvent(self, event):
    # Outside the axes rect
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

    else:  # inside the axes rect
      super(PlotCanvas, self).wheelEvent(event)

  def updateCursorShape(self, pos):
    if self.leftButtonPressed:
      self.setCursor(QCursor(Qt.ClosedHandCursor))
    else:
      # Inside the axes rect
      if self.axisRect().rect().contains(pos):
        if self.plottableAt(pos, True) is None and self.itemAt(pos, True) is None:
          self.setCursor(QCursor(Qt.CrossCursor if self.showInfo else Qt.OpenHandCursor))
        else:
          self.setCursor(QCursor(Qt.PointingHandCursor))
      else:  # outside the axes rect
        self.setCursor(QCursor(Qt.SizeVerCursor if pos.x() < self.axisRect().rect().left() else Qt.ArrowCursor))

  def contextMenu(self):
    actMarker = QAction(QIcon(self.themeSelector.select(':/icons/waypoint-marker.svg')), self.tr('Point with marker'), self)
    actMarker.setCheckable(True)
    actMarker.setChecked(TheDocument.wptmodel.index(self.selectedElement.idx, gpx.NAME).data(gpx.MarkerRole))
    actMarker.triggered[bool].connect(self.onMarkerPoints)
    actCaption = QAction(QIcon(self.themeSelector.select(':/icons/waypoint-caption.svg')), self.tr('Point with caption'), self)
    actCaption.setCheckable(True)
    actCaption.setChecked(TheDocument.wptmodel.index(self.selectedElement.idx, gpx.NAME).data(gpx.CaptionRole))
    actCaption.triggered[bool].connect(self.onCaptionPoints)
    actSplit = QAction(QIcon(self.themeSelector.select(':/icons/waypoint-splitline.svg')), self.tr('Point with splitting line'), self)
    actSplit.setCheckable(True)
    actSplit.setChecked(TheDocument.wptmodel.index(self.selectedElement.idx, gpx.NAME).data(gpx.SplitLineRole))
    actSplit.triggered[bool].connect(self.onSplitLines)
    actSkip = QAction(QIcon(self.themeSelector.select(':/icons/waypoint-skip.svg')), self.tr('Skip point'), self)
    actSkip.setCheckable(True)
    actSkip.setChecked(not TheDocument.wptmodel.index(self.selectedElement.idx, gpx.NAME).data(gpx.IncludeRole))
    actSkip.triggered[bool].connect(self.onSkipPoints)
    actStyle = QAction(QIcon(self.themeSelector.select(':/icons/configure.svg')), self.tr('Point style'), self)
    actStyle.triggered.connect(self.onPointStyle)

    menu = QMenu(self)
    menu.addAction(actMarker)
    menu.addAction(actCaption)
    menu.addAction(actSplit)
    menu.addSeparator()
    menu.addAction(actSkip)
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
    showMapMenu.setIcon(QIcon(self.themeSelector.select(':/icons/internet-services.svg')))
    showMapMenu.addAction(actShowGoogleMap)
    showMapMenu.addAction(actShowYandexMap)
    showMapMenu.addAction(actShowZoomEarthMap)
    showMapMenu.addAction(actShowOpenCycleMap)
    showMapMenu.addAction(actShowOpenTopoMap)
    showMapMenu.addAction(actShowTopoMap)
    menu.addMenu(showMapMenu)
    menu.popup(QCursor.pos())

  @pyqtSlot(bool)
  def onMarkerPoints(self, marker):
    TheDocument.wptmodel.setMarkerStates([self.selectedElement.idx], marker)
    if marker:
      index = [m.idx for m in self.infoMarkers].index(self.selectedElement.idx)
      self.markers += [self.infoMarkers.pop(index)]
    else:
      index = [m.idx for m in self.markers].index(self.selectedElement.idx)
      self.infoMarkers += [self.markers.pop(index)]
      if not self.showInfo:
        self.infoMarkers[-1].setVisible(False)
        self.infoMarkers[-1].setSelectable(False)

    self.replot()

  @pyqtSlot(bool)
  def onCaptionPoints(self, caption):
    TheDocument.wptmodel.setCaptionStates([self.selectedElement.idx], caption)
    if caption:
      self.captions += [CaptionItem(self, self.selectedElement.idx, self.selectedElement.posX, self.selectedElement.posY)]
    else:
      for i, c in enumerate(self.captions):
        if c.idx == self.selectedElement.idx:
          self.removeItem(c)
          del self.captions[i]
          break
    self.replot()

  @pyqtSlot(bool)
  def onSplitLines(self, split):
    TheDocument.wptmodel.setSplitLines([self.selectedElement.idx], split)
    if split:
      self.splitLines += [SplitLine(self, self.selectedElement.idx, self.selectedElement.posX, self.selectedElement.posY)]
    else:
      for i, l in enumerate(self.splitLines):
        if l.idx == self.selectedElement.idx:
          self.removeGraph(l)
          del self.splitLines[i]
          break
    self.replot()

  @pyqtSlot(bool)
  def onSkipPoints(self, skip):
    TheDocument.wptmodel.setIncludeStates([self.selectedElement.idx], not skip)
    self.plotProfile(self.column, self.wptRows, self.trkRows, False)

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
    if self.type == gpx.TIME:
      self.setTickOrigin(QCPAxisTickerDateTime.dateTimeToKey(QDate(2019, 1, 1)))
    else:
      self.setTickOrigin(0)

  def getTickStep(self, range):
    if self.orientation == Qt.Horizontal:
      if self.type == gpx.DIST:
        availableSteps = [0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100]
      else:  # time
        availableSteps = [1.0 / 24, 2.0 / 24, 3.0 / 24, 6.0 / 24, 12.0 / 24, 1, 2]
        if self.type == gpx.TIME:
          availableSteps = [s * 24 * 3600 for s in availableSteps]  # convert to seconds
      return self.pickClosest(range.size() / 10, availableSteps)
    else:  # vertical
      availableSteps = [10, 20, 50, 100, 200, 500, 1000]
      return self.pickClosest(range.size() / 7, availableSteps)

  def getSubTickCount(self, tickStep):
    if self.orientation == Qt.Horizontal:
      if self.type == gpx.DIST:
        if tickStep in {0.1, 0.5, 1, 5, 10, 50, 100}:
          return 4
        else:
          return 1
      else:  # time
        if tickStep in {12.0 / 24, 12.0 * 3600}:
          return 3
        elif tickStep in {3.0 / 24, 3.0 * 3600}:
          return 2
        elif tickStep in {2.0 / 24, 6.0 / 24, 2, 2.0 * 3600, 6.0 * 3600, 2 * 24 * 3600}:
          return 1
        else:
          return 0
    else:  # vertical
      if tickStep in {10, 50, 100, 500, 1000}:
        return 4
      else:
        return 1

  def createLabelVector(self, ticks, locale, formatChar, precision):
    if self.orientation == Qt.Horizontal:
      if self.type == gpx.TIME_DAYS:
        if ticks[-1] < 1:  # hours
          return [str(int(round(24 * t))) for t in ticks]
        elif any([t % 1.0 != 0 for t in ticks]):  # days and hours
          if TheConfig.getValue('ProfileStyle', 'ShowHours'):
            return [QCoreApplication.translate('PlotCanvas', 'day ') + str(int(t)) + "\n"
                    + str(int(round(24 * t)) % 24).zfill(2) + ":00" for t in ticks]
          else:
            return [str(int(t)) if t % 1.0 == 0 else "" for t in ticks]
      elif self.type == gpx.TIME:
        if any([QCPAxisTickerDateTime.keyToDateTime(t).toString('HH') != '00' for t in ticks]) \
           and TheConfig.getValue('ProfileStyle', 'ShowHours'):  # days and hours
          return [QCPAxisTickerDateTime.keyToDateTime(t).toString('d MMM\nHH:mm') for t in ticks]
        else:
          return [QCPAxisTickerDateTime.keyToDateTime(t).toString('d MMM')
                  if QCPAxisTickerDateTime.keyToDateTime(t).toString('HH') == '00' else "" for t in ticks]

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
    scatterStyle = QCPScatterStyle()
    if self.idx in TheDocument.wptmodel.getMarkedPoints():
      markerStyle = TheDocument.wptmodel.index(self.idx, gpx.NAME).data(gpx.MarkerStyleRole)
      scatterStyle.setCustomPath(gpx.markerPath(markerStyle[gpx.MARKER_STYLE], 2 * markerStyle[gpx.MARKER_SIZE]))  # for better compatibility with matplotlib
      scatterStyle.setBrush(QColor.fromRgba(markerStyle[gpx.MARKER_COLOR]))
      if markerStyle[gpx.MARKER_STYLE] in {'1', '2', '3', '4', 'ad', 'au', 'al', 'ar', '+', 'x', '_', '|'}:
        scatterStyle.setPen(QPen(QColor.fromRgba(markerStyle[gpx.MARKER_COLOR]), 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
      else:
        scatterStyle.setPen(QPen(QColor.fromRgba(markerStyle[gpx.MARKER_COLOR]), 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
    else:
      scatterStyle.setShape(QCPScatterStyle.ssDisc)
      scatterStyle.setSize(3 * TheConfig.getValue('ProfileStyle', 'ProfileWidth'))
      scatterStyle.setBrush(QColor.fromRgba(TheConfig.getValue('ProfileStyle', 'ProfileColor')))
      scatterStyle.setPen(QPen(QColor.fromRgba(TheConfig.getValue('ProfileStyle', 'ProfileColor')), 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

    selectedScatterStyle = QCPScatterStyle()
    if self.idx in TheDocument.wptmodel.getMarkedPoints():
      selectedScatterStyle.setCustomPath(gpx.markerPath(markerStyle[gpx.MARKER_STYLE], 3 * markerStyle[gpx.MARKER_SIZE]))
      selectedScatterStyle.setPen(QPen(QGuiApplication.palette().highlight().color(), 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
    else:
      selectedScatterStyle.setShape(QCPScatterStyle.ssCircle)
      selectedScatterStyle.setSize(6 * TheConfig.getValue('ProfileStyle', 'ProfileWidth'))
      selectedScatterStyle.setPen(QPen(QGuiApplication.palette().highlight().color(), 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

    self.setScatterStyle(scatterStyle)
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

    if TheConfig.getValue('ProfileStyle', 'UseSystemTheme'):
      self.setColor(QGuiApplication.palette().text().color())
      self.setSelectedColor(QGuiApplication.palette().highlightedText().color())
    else:
      self.setColor(QColor(Qt.black))
      self.setSelectedColor(QColor(Qt.black))

    self.setClipToAxisRect(False)
    self.setPadding(QMargins(3, 1, 3, 1))
    self.setRotation(-TheDocument.wptmodel.index(self.idx, gpx.NAME).data(gpx.CaptionStyleRole)[gpx.CAPTION_ROTATION])
    self.setPositionAlignment(Qt.AlignLeft | Qt.AlignVCenter)
    self.position.setType(QCPItemPosition.ptPlotCoords)

    fillColor = QGuiApplication.palette().highlight().color()
    fillColor.setAlpha(150)
    self.setSelectedBrush(fillColor)
    self.setSelectedPen(QGuiApplication.palette().highlight().color())

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
