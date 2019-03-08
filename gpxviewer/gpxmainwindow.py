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

import sys
import re
import webbrowser
from PyQt5 import QtCore, QtWidgets, QtGui
import gpxviewer.gpxmodel as gpx
import gpxviewer.statwindow as stat
import gpxviewer.plotviewer as plt
import gpxviewer.pointconfigdialog
import gpxviewer.settingsdialog
from gpxviewer.configstore import TheConfig
from gpxviewer.gpxdocument import TheDocument
import gpxviewer.ui_mainwindow


class GpxMainWindow(QtWidgets.QMainWindow):
  def __init__(self):
    super(GpxMainWindow, self).__init__()
    self.ui = gpxviewer.ui_mainwindow.Ui_MainWindow()
    self.ui.setupUi(self)
    self.ui.wptView.setFocus()

    self.setWindowIcon(QtGui.QIcon(':/icons/gpxviewer.svg'))
    self.ui.actionLoadGPXfile.setIcon(QtGui.QIcon(':/icons/xml-element-new.svg'))
    self.ui.actionSaveGPXfileAs.setIcon(QtGui.QIcon(':/icons/document-save-as-template.svg'))
    self.ui.actionNew.setIcon(QtGui.QIcon(':/icons/document-new.svg'))
    self.ui.actionOpen.setIcon(QtGui.QIcon(':/icons/document-open.svg'))
    self.ui.actionSave.setIcon(QtGui.QIcon(':/icons/document-save.svg'))
    self.ui.actionSaveAs.setIcon(QtGui.QIcon(':/icons/document-save-as.svg'))
    self.ui.menuRecentProjects.setIcon(QtGui.QIcon(':/icons/document-open-recent.svg'))
    self.ui.actionQuit.setIcon(QtGui.QIcon(':/icons/application-exit.svg'))
    self.ui.actionSettings.setIcon(QtGui.QIcon(':/icons/configure.svg'))
    self.ui.actionDistanceProfile.setIcon(QtGui.QIcon(':/icons/distanceprofile.svg'))
    self.ui.actionTimeProfile.setIcon(QtGui.QIcon(':/icons/timeprofile.svg'))
    self.ui.actionStatistics.setIcon(QtGui.QIcon(':/icons/view-statistics.svg'))
    self.ui.actionGpxViewerHelp.setIcon(QtGui.QIcon(':/icons/help-contents.svg'))
    self.ui.actionAboutQt.setIcon(QtGui.QIcon.fromTheme('qtlogo', QtGui.QIcon(':/icons/qtlogo.svg')))
    self.ui.actionAboutGPXViewer.setIcon(QtGui.QIcon(':/icons/gpxviewer.svg'))

    self.ui.actionNew.setShortcut(QtGui.QKeySequence.New)
    self.ui.actionOpen.setShortcut(QtGui.QKeySequence.Open)
    self.ui.actionSave.setShortcut(QtGui.QKeySequence.Save)
    self.ui.actionSaveAs.setShortcut(QtGui.QKeySequence.SaveAs)
    self.ui.actionQuit.setShortcut(QtGui.QKeySequence.Quit)

    wdg = QtWidgets.QWidget()
    wdg.setLayout(QtWidgets.QHBoxLayout())
    wdg.layout().addItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding))
    wdg.layout().addWidget(QtWidgets.QLabel(self.tr('Filter by name:')))
    self.filterLineEdit = QtWidgets.QLineEdit()
    self.filterLineEdit.setMinimumWidth(200)
    self.filterLineEdit.setPlaceholderText(self.tr('Enter regular expression'))
    self.filterLineEdit.setClearButtonEnabled(True)
    wdg.layout().addWidget(self.filterLineEdit)
    self.ui.filterToolBar.addWidget(wdg)

    self.filterModel = gpx.GpxSortFilterModel(self)
    self.filterModel.setSourceModel(TheDocument.wptmodel)
    self.filterModel.setFilterKeyColumn(gpx.NAME)
    self.updateIncludeFilter()

    self.ui.wptView.setModel(self.filterModel)
    self.ui.wptView.setSortingEnabled(True)
    self.ui.wptView.sortByColumn(gpx.TIME, QtCore.Qt.AscendingOrder)
    self.filterLineEdit.textChanged.connect(self.filterModel.setFilterRegExp)

    self.ui.trkView.setModel(TheDocument.trkmodel)

    self.ui.wptView.installEventFilter(self)
    self.ui.trkView.installEventFilter(self)

    self.ui.actionShowSkipped.setChecked(TheConfig['MainWindow'].getboolean('ShowSkipped'))
    self.ui.actionShowMarked.setChecked(TheConfig['MainWindow'].getboolean('ShowMarked'))
    self.ui.actionShowCaptioned.setChecked(TheConfig['MainWindow'].getboolean('ShowCaptioned'))
    self.ui.actionShowMarkedCaptioned.setChecked(TheConfig['MainWindow'].getboolean('ShowMarkedCaptioned'))
    self.ui.actionShowOther.setChecked(TheConfig['MainWindow'].getboolean('ShowDefault'))

    TheDocument.gpxparser.warningSent.connect(self.showWarning)
    TheDocument.wptmodel.wptDataChanged.connect(self.setProjectChanged)
    TheDocument.fileNotFound.connect(self.openedFileNotFound)

    self.projectSaved = False
    self.projectChanged = False
    self.titleFilename = None
    self.actionsRecent = []

    self.updateRecentProjects()
    self.resize(TheConfig['MainWindow'].getint('WindowWidth'), TheConfig['MainWindow'].getint('WindowHeight'))

    self.plot = plt.PlotWindow()
    self.stat = stat.StatWindow()

  def aboutQt(self):
    QtWidgets.QApplication.aboutQt()

  def eventFilter(self, obj, event):
    if event.type() == QtCore.QEvent.KeyPress and event.key() == QtCore.Qt.Key_Tab and event.modifiers() == QtCore.Qt.ControlModifier:
      self.keyPressEvent(QtGui.QKeyEvent(event))
      return True
    elif obj == self.ui.wptView and event.type() == QtCore.QEvent.KeyPress and event.key() == QtCore.Qt.Key_F2:
      self.keyPressEvent(QtGui.QKeyEvent(event))
      return True
    elif event.type() == QtCore.QEvent.ContextMenu or (event.type() == QtCore.QEvent.KeyPress and event.key() == QtCore.Qt.Key_Menu):
      if obj == self.ui.wptView:
        self.wptContextMenuEvent(event)
      elif obj == self.ui.trkView:
        self.trkContextMenuEvent(event)
      return True
    else:
      return super(GpxMainWindow, self).eventFilter(obj, event)

  def closeEvent(self, event):
    if self.projectChanged and len(TheDocument.doc['GPXFile']) != 0:
      result = QtWidgets.QMessageBox.information(self, self.tr('Close GPX Viewer'),
                                                 self.tr('There are unsaved changes. Do you want to save the project?'),
                                                 QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel,
                                                 QtWidgets.QMessageBox.Yes)
      if result == QtWidgets.QMessageBox.Yes:
        if not self.fileSave():
          event.ignore()
          return
      if result == QtWidgets.QMessageBox.Cancel:
        event.ignore()
        return

    self.plot.close()
    self.stat.close()
    TheConfig.save()
    super(GpxMainWindow, self).closeEvent(event)

  def wptContextMenuEvent(self, event):
    if self.ui.wptView.selectionModel().hasSelection():
      actSkip = QtWidgets.QAction(QtGui.QIcon(':/icons/waypoint-skip.svg'), self.tr('Skip points'), self)
      actSkip.setStatusTip(self.tr('Skip these waypoints when plotting profiles or calculating statistics'))
      actSkip.setCheckable(True)
      actSkip.setChecked(not self.ui.wptView.currentIndex().data(gpx.IncludeRole))
      actSkip.triggered.connect(self.skipPoints)

      actMarker = QtWidgets.QAction(QtGui.QIcon(':/icons/waypoint-marker.svg'), self.tr('Points with markers'), self)
      actMarker.setStatusTip(self.tr('Add markers to these waypoints when plotting profiles'))
      actMarker.setDisabled(actSkip.isChecked())
      actMarker.setCheckable(True)
      actMarker.setChecked(self.ui.wptView.currentIndex().data(gpx.MarkerRole))
      actMarker.triggered.connect(self.markerPoints)

      actCaption = QtWidgets.QAction(QtGui.QIcon(':/icons/waypoint-caption.svg'), self.tr('Points with captions'), self)
      actCaption.setStatusTip(self.tr('Add captions to these waypoints when plotting profiles'))
      actCaption.setDisabled(actSkip.isChecked())
      actCaption.setCheckable(True)
      actCaption.setChecked(self.ui.wptView.currentIndex().data(gpx.CaptionRole))
      actCaption.triggered.connect(self.captionPoints)

      actSplit = QtWidgets.QAction(QtGui.QIcon(':/icons/waypoint-splitline.svg'), self.tr('Points with splitting lines'), self)
      actSplit.setStatusTip(self.tr('Add splitting lines to these waypoints when plotting profiles'))
      actSplit.setDisabled(actSkip.isChecked())
      actSplit.setCheckable(True)
      actSplit.setChecked(self.ui.wptView.currentIndex().data(gpx.SplitLineRole))
      actSplit.triggered.connect(self.splitLines)

      actNeglect = QtWidgets.QAction(QtGui.QIcon(':/icons/waypoint-neglect-distance.svg'), self.tr('Neglect previous distance'), self)
      actNeglect.setStatusTip(self.tr('Neglect distance before these waypoints when plotting profiles'))
      actNeglect.setDisabled(actSkip.isChecked())
      actNeglect.setCheckable(True)
      actNeglect.setChecked(self.ui.wptView.currentIndex().data(gpx.NeglectRole))
      actNeglect.triggered.connect(self.neglectDistance)

      actReset = QtWidgets.QAction(QtGui.QIcon(':/icons/edit-clear-all.svg'), self.tr('Reset appearance'), self)
      actReset.setStatusTip(self.tr('Reset appearance of these waypoints'))
      actReset.setDisabled(actSkip.isChecked())
      actReset.triggered.connect(self.resetPoints)

      actRename = QtWidgets.QAction(QtGui.QIcon(':/icons/edit-rename.svg'), self.tr('Rename...'), self)
      actRename.setStatusTip(self.tr('Rename these waypoints'))
      actRename.triggered.connect(self.renamePoints)
      actResetName = QtWidgets.QAction(QtGui.QIcon(':/icons/edit-clear.svg'), self.tr('Reset name'), self)
      actResetName.setStatusTip(self.tr('Reset the names of these waypoints'))
      actResetName.triggered.connect(self.resetPointNames)

      actStyle = QtWidgets.QAction(QtGui.QIcon(':/icons/configure.svg'), self.tr('Point style'), self)
      actStyle.setStatusTip(self.tr('Change the style of these waypoints when plotting profiles'))
      actStyle.triggered.connect(self.pointStyle)

      menu = QtWidgets.QMenu(self)
      menu.addAction(actMarker)
      menu.addAction(actCaption)
      menu.addAction(actSplit)
      menu.addAction(actNeglect)
      menu.addAction(actReset)
      menu.addSeparator()
      menu.addAction(actSkip)
      menu.addSeparator()
      menu.addAction(actRename)
      menu.addAction(actResetName)
      menu.addSeparator()
      menu.addAction(actStyle)
      menu.addSeparator()

      actShowGoogleMap = QtWidgets.QAction(QtGui.QIcon(':/icons/googlemaps.png'), self.tr('Google Maps'), self)
      actShowGoogleMap.setStatusTip(self.tr('Show this waypoint on the website maps.google.com'))
      actShowGoogleMap.triggered.connect(self.showGoogleMap)
      actShowYandexMap = QtWidgets.QAction(QtGui.QIcon(':/icons/yandexmaps.png'), self.tr('Yandex Maps'), self)
      actShowYandexMap.setStatusTip(self.tr('Show this waypoint on the website maps.yandex.ru'))
      actShowYandexMap.triggered.connect(self.showYandexMap)
      actShowZoomEarthMap = QtWidgets.QAction(QtGui.QIcon(':/icons/zoomearth.png'), self.tr('Zoom Earth'), self)
      actShowZoomEarthMap.setStatusTip(self.tr('Show this waypoint on the website zoom.earth'))
      actShowZoomEarthMap.triggered.connect(self.showZoomEarthMap)
      actShowOpenCycleMap = QtWidgets.QAction(QtGui.QIcon(':/icons/openstreetmap.png'), self.tr('OpenCycleMap'), self)
      actShowOpenCycleMap.setStatusTip(self.tr('Show this waypoint on the website openstreetmap.org'))
      actShowOpenCycleMap.triggered.connect(self.showOpenCycleMap)
      actShowOpenTopoMap = QtWidgets.QAction(QtGui.QIcon(':/icons/opentopomap.png'), self.tr('OpenTopoMap'), self)
      actShowOpenTopoMap.setStatusTip(self.tr('Show this waypoint on the website opentopomap.org'))
      actShowOpenTopoMap.triggered.connect(self.showOpenTopoMap)
      actShowTopoMap = QtWidgets.QAction(QtGui.QIcon(':/icons/loadmap.png'), self.tr('Loadmap.net'), self)
      actShowTopoMap.setStatusTip(self.tr('Show this waypoint on the website loadmap.net'))
      actShowTopoMap.triggered.connect(self.showTopoMap)

      showMapMenu = QtWidgets.QMenu(self.tr('Show on map'), self)
      showMapMenu.setIcon(QtGui.QIcon(':/icons/internet-services.svg'))
      showMapMenu.addAction(actShowGoogleMap)
      showMapMenu.addAction(actShowYandexMap)
      showMapMenu.addAction(actShowZoomEarthMap)
      showMapMenu.addAction(actShowOpenCycleMap)
      showMapMenu.addAction(actShowOpenTopoMap)
      showMapMenu.addAction(actShowTopoMap)
      menu.addMenu(showMapMenu)

      menu.popup(QtGui.QCursor.pos())
      event.accept()

  def trkContextMenuEvent(self, event):
    if self.ui.trkView.selectionModel().hasSelection():
      actSkip = QtWidgets.QAction(QtGui.QIcon(':/icons/waypoint-skip.svg'), self.tr('Skip tracks'), self)
      actSkip.setStatusTip(self.tr('Skip these tracks when plotting profiles or calculating statistics'))
      actSkip.setCheckable(True)
      actSkip.setChecked(not self.ui.trkView.currentIndex().data(gpx.IncludeRole))
      actSkip.triggered.connect(self.skipTracks)

      menu = QtWidgets.QMenu(self)
      menu.addAction(actSkip)
      menu.popup(QtGui.QCursor.pos())
      event.accept()

  def keyPressEvent(self, event):
    if event.key() == QtCore.Qt.Key_F and event.modifiers() == QtCore.Qt.ControlModifier:
      self.filterLineEdit.setFocus()
      self.filterLineEdit.selectAll()
    elif event.key() == QtCore.Qt.Key_C and event.modifiers() == QtCore.Qt.ControlModifier:
      if self.ui.tabWidget.currentWidget() == self.ui.wptTab:
        TheDocument.wptmodel.copyToClipboard([i.data(gpx.IDRole) for i in self.ui.wptView.selectionModel().selectedRows()])
      else:
        TheDocument.trkmodel.copyToClipboard([i.row() for i in self.ui.trkView.selectionModel().selectedRows()])
    elif event.key() == QtCore.Qt.Key_F2:
      if self.ui.tabWidget.currentWidget() == self.ui.wptTab and self.ui.wptView.selectionModel().hasSelection():
        self.renamePoints()
    elif event.key() == QtCore.Qt.Key_Escape:
      if self.ui.tabWidget.currentWidget() == self.ui.wptTab:
        if self.ui.wptView.hasFocus():
          self.ui.wptView.clearSelection()
        else:
          self.ui.wptView.setFocus()
      else:
        if self.ui.trkView.hasFocus():
          self.ui.trkView.clearSelection()
        else:
          self.ui.trkView.setFocus()
    elif event.key() == QtCore.Qt.Key_Tab and event.modifiers() == QtCore.Qt.ControlModifier:
      self.ui.tabWidget.setCurrentIndex(1 - self.ui.tabWidget.currentIndex())

    super(GpxMainWindow, self).keyPressEvent(event)

  def resizeEvent(self, event):
    super(GpxMainWindow, self).resizeEvent(event)
    self.ui.wptView.resizeColumnsToContents()
    self.ui.trkView.resizeColumnsToContents()
    TheConfig['MainWindow']['WindowWidth'] = str(event.size().width())
    TheConfig['MainWindow']['WindowHeight'] = str(event.size().height())

  def aboutGPXViewer(self):
    aboutText = '<h3>GPX Viewer</h3><b>' + self.tr('Version') + ' ' + QtCore.QCoreApplication.applicationVersion() + '</b><br><br>' + \
                self.tr('Using') + ' Python ' + str(sys.version_info.major) + '.' + str(sys.version_info.minor) + '.' + str(sys.version_info.micro) + ', ' + \
                'PyQt5 ' + QtCore.PYQT_VERSION_STR + ', ' + \
                'Qt ' + QtCore.QT_VERSION_STR + '<br><br>' + \
                'Copyright 2016-2019 Sergey Salnikov <a href=mailto:salsergey@gmail.com>&lt;salsergey@gmail.com&gt;</a><br><br>' + \
                self.tr('License:') + ' <a href=http://www.gnu.org/licenses/gpl.html>GNU General Public License, version 3</a>'
    QtWidgets.QMessageBox.about(self, self.tr('About GPX Viewer'), aboutText)

  def gpxViewerHelp(self):
    aboutText = self.tr('''Notation:<br>
                           <font color=red>Red</font> - skipped points<br>
                           <font color=blue>Blue</font> - marked points<br>
                           <font color=green>Green</font> - captioned points<br>
                           <b>Bold</b> - points with splitting lines<br>
                           <i>Italic</i> - distance before these points is neglected<br>
                           <br>
                           Useful shortcuts:<br>
                           Ctrl+C - Copy points to clipboard<br>
                           Ctrl+P - Show distance profile<br>
                           Ctrl+T - Show time profile<br>
                           Ctrl+I - Show statistics<br>
                           F2 - Rename multiple points.
                           Several symbols "#" are replaced by sequential numbers.
                           The number of digits equals to the amount of symbols "#".<br>
                           <br>
                           Several cases are possible when plotting a profile:
                           <ul>
                           <li>All non-skipped points have timestamps: points and tracks with timestamps are taken into account</li>
                           <li>There are points without timestamps: only points are considered, tracks are skipped</li>
                           <li>There are no points: all non-skipped tracks are taken into account</li>
                           </ul>''')
    msg = QtWidgets.QMessageBox(self)
    msg.setWindowTitle(self.tr('GPX Viewer Help'))
    msg.setTextFormat(QtCore.Qt.RichText)
    msg.setText(aboutText)
    msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.exec_()

  def setProjectChanged(self, value):
    self.projectChanged = value
    self.updateTitleFilename()

  def skipPoints(self):
    TheDocument.wptmodel.setIncludeStates([i.data(gpx.IDRole) for i in self.ui.wptView.selectedIndexes() if i.column() == gpx.NAME],
                                          not self.sender().isChecked())
    self.filterModel.invalidateFilter()
    self.setProjectChanged(True)

  def markerPoints(self):
    TheDocument.wptmodel.setMarkerStates([i.data(gpx.IDRole) for i in self.ui.wptView.selectedIndexes() if i.column() == gpx.NAME],
                                         self.sender().isChecked())
    self.filterModel.invalidateFilter()
    self.setProjectChanged(True)

  def captionPoints(self):
    TheDocument.wptmodel.setCaptionStates([i.data(gpx.IDRole) for i in self.ui.wptView.selectedIndexes() if i.column() == gpx.NAME],
                                          self.sender().isChecked())
    self.filterModel.invalidateFilter()
    self.setProjectChanged(True)

  def splitLines(self):
    TheDocument.wptmodel.setSplitLines([i.data(gpx.IDRole) for i in self.ui.wptView.selectedIndexes() if i.column() == gpx.NAME],
                                       self.sender().isChecked())
    self.filterModel.invalidateFilter()
    self.setProjectChanged(True)

  def neglectDistance(self):
    TheDocument.wptmodel.setNeglectStates([i.data(gpx.IDRole) for i in self.ui.wptView.selectedIndexes() if i.column() == gpx.NAME],
                                          self.sender().isChecked())
    self.setProjectChanged(True)

  def resetPoints(self):
    indexes = [i.data(gpx.IDRole) for i in self.ui.wptView.selectedIndexes() if i.column() == gpx.NAME]
    TheDocument.wptmodel.setMarkerStates(indexes, False)
    TheDocument.wptmodel.setCaptionStates(indexes, False)
    TheDocument.wptmodel.setSplitLines(indexes, False)
    TheDocument.wptmodel.setNeglectStates(indexes, False)
    self.filterModel.invalidateFilter()
    self.setProjectChanged(True)

  def renamePoints(self):
    indexes = [i.data(gpx.IDRole) for i in self.ui.wptView.selectedIndexes() if i.column() == gpx.NAME]
    indexes.sort()
    first_name = TheDocument.wptmodel.index(indexes[0], gpx.NAME).data()

    dlg = QtWidgets.QDialog(self)
    dlg.setWindowTitle(self.tr('Rename waypoints'))
    vLayout = QtWidgets.QVBoxLayout(dlg)
    vLayout.addWidget(QtWidgets.QLabel(self.tr('Enter new name for ') + str(len(indexes)) + self.tr(' waypoints:')))
    dlg.setLayout(vLayout)

    nameEdit = QtWidgets.QLineEdit(dlg)
    nameEdit.setText(first_name + (' #' if len(indexes) > 1 else ''))
    nameEdit.setSelection(0, len(first_name))
    vLayout.addWidget(nameEdit)

    hLayout = QtWidgets.QHBoxLayout(dlg)
    hLayout.addWidget(QtWidgets.QLabel(self.tr('Several symbols "#" will be replaced by sequential numbers starting from:')))
    vLayout.addLayout(hLayout)

    numberBox = QtWidgets.QSpinBox(dlg)
    numberBox.setValue(1)
    hLayout.addWidget(numberBox)

    buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
    buttons.accepted.connect(dlg.accept)
    buttons.rejected.connect(dlg.reject)
    vLayout.addWidget(buttons)

    if dlg.exec_() == QtWidgets.QDialog.Accepted:
      for n, ind in enumerate(indexes, numberBox.value()):
        name = nameEdit.text()
        if re.match('.*#+', name):
          digits = len(re.findall('(#+)', name)[0])
          name = re.sub('#+', str(n).zfill(digits), name, 1)
        TheDocument.wptmodel.setData(TheDocument.wptmodel.index(ind, gpx.NAME), name, QtCore.Qt.EditRole)
      self.setProjectChanged(True)

  def resetPointNames(self):
    TheDocument.wptmodel.resetNames([i.data(gpx.IDRole) for i in self.ui.wptView.selectedIndexes() if i.column() == gpx.NAME])

  def showGoogleMap(self):
    lat = TheDocument.wptmodel.index(self.ui.wptView.currentIndex().data(gpx.IDRole), gpx.LAT).data()
    lon = TheDocument.wptmodel.index(self.ui.wptView.currentIndex().data(gpx.IDRole), gpx.LON).data()
    webbrowser.open('https://maps.google.com/maps?ll=' + lat + ',' + lon + '&t=h&q=' + lat + ',' + lon + '&z=15')

  def showYandexMap(self):
    lat = TheDocument.wptmodel.index(self.ui.wptView.currentIndex().data(gpx.IDRole), gpx.LAT).data()
    lon = TheDocument.wptmodel.index(self.ui.wptView.currentIndex().data(gpx.IDRole), gpx.LON).data()
    webbrowser.open('https://maps.yandex.ru?ll=' + lon + ',' + lat + '&spn=0.03,0.03&pt=' + lon + ',' + lat + '&l=sat')

  def showZoomEarthMap(self):
    lat = TheDocument.wptmodel.index(self.ui.wptView.currentIndex().data(gpx.IDRole), gpx.LAT).data()
    lon = TheDocument.wptmodel.index(self.ui.wptView.currentIndex().data(gpx.IDRole), gpx.LON).data()
    webbrowser.open('https://zoom.earth/#' + lat + ',' + lon + ',15z,map')

  def showOpenCycleMap(self):
    lat = TheDocument.wptmodel.index(self.ui.wptView.currentIndex().data(gpx.IDRole), gpx.LAT).data()
    lon = TheDocument.wptmodel.index(self.ui.wptView.currentIndex().data(gpx.IDRole), gpx.LON).data()
    webbrowser.open('https://openstreetmap.org/?mlat=' + lat + '&mlon=' + lon + '&zoom=15&layers=C')

  def showOpenTopoMap(self):
    lat = TheDocument.wptmodel.index(self.ui.wptView.currentIndex().data(gpx.IDRole), gpx.LAT).data()
    lon = TheDocument.wptmodel.index(self.ui.wptView.currentIndex().data(gpx.IDRole), gpx.LON).data()
    webbrowser.open('https://opentopomap.org/#marker=15/' + lat + '/' + lon)

  def showTopoMap(self):
    lat = TheDocument.wptmodel.index(self.ui.wptView.currentIndex().data(gpx.IDRole), gpx.LAT).data()
    lon = TheDocument.wptmodel.index(self.ui.wptView.currentIndex().data(gpx.IDRole), gpx.LON).data()
    webbrowser.open('http://loadmap.net/ru?q=' + lat + ' ' + lon + '&z=13&s=0')

  def pointStyle(self):
    style = {}
    style.update(self.ui.wptView.currentIndex().data(gpx.MarkerStyleRole))
    style.update(self.ui.wptView.currentIndex().data(gpx.CaptionStyleRole))
    style.update(self.ui.wptView.currentIndex().data(gpx.SplitLineStyleRole))
    dlg = gpxviewer.pointconfigdialog.PointConfigDialog(self, style)

    if dlg.exec_() == QtWidgets.QDialog.Accepted:
      self.setProjectChanged(True)
      TheConfig['PointStyle']['MarkerColor'] = str(dlg.style[gpx.MARKER_COLOR])
      TheConfig['PointStyle']['MarkerStyle'] = dlg.style[gpx.MARKER_STYLE]
      TheConfig['PointStyle']['MarkerSize'] = str(dlg.style[gpx.MARKER_SIZE])
      TheConfig['PointStyle']['CaptionPositionX'] = str(dlg.style[gpx.CAPTION_POSX])
      TheConfig['PointStyle']['CaptionPositionY'] = str(dlg.style[gpx.CAPTION_POSY])
      TheConfig['PointStyle']['CaptionSize'] = str(dlg.style[gpx.CAPTION_SIZE])
      TheConfig['PointStyle']['SplitLineColor'] = str(dlg.style[gpx.LINE_COLOR])
      TheConfig['PointStyle']['SplitLineStyle'] = dlg.style[gpx.LINE_STYLE]
      TheConfig['PointStyle']['SplitLineWidth'] = str(dlg.style[gpx.LINE_WIDTH])

      if TheConfig.getValue('PointStyle', 'MarkerColorEnabled'):
        self.setPointStyle(gpx.MARKER_COLOR, dlg.style[gpx.MARKER_COLOR])
      if TheConfig.getValue('PointStyle', 'MarkerStyleEnabled'):
        self.setPointStyle(gpx.MARKER_STYLE, dlg.style[gpx.MARKER_STYLE])
      if TheConfig.getValue('PointStyle', 'MarkerSizeEnabled'):
        self.setPointStyle(gpx.MARKER_SIZE, dlg.style[gpx.MARKER_SIZE])

      if TheConfig.getValue('PointStyle', 'CaptionPositionEnabled'):
        self.setPointStyle(gpx.CAPTION_POSX, dlg.style[gpx.CAPTION_POSX])
        self.setPointStyle(gpx.CAPTION_POSY, dlg.style[gpx.CAPTION_POSY])
      if TheConfig.getValue('PointStyle', 'CaptionSizeEnabled'):
        self.setPointStyle(gpx.CAPTION_SIZE, dlg.style[gpx.CAPTION_SIZE])

      if TheConfig.getValue('PointStyle', 'SplitLineColorEnabled'):
        self.setPointStyle(gpx.LINE_COLOR, dlg.style[gpx.LINE_COLOR])
      if TheConfig.getValue('PointStyle', 'SplitLineStyleEnabled'):
        self.setPointStyle(gpx.LINE_STYLE, dlg.style[gpx.LINE_STYLE])
      if TheConfig.getValue('PointStyle', 'SplitLineWidthEnabled'):
        self.setPointStyle(gpx.LINE_WIDTH, dlg.style[gpx.LINE_WIDTH])

  def setPointStyle(self, key, value):
    TheDocument.wptmodel.setPointStyle([i.data(gpx.IDRole) for i in self.ui.wptView.selectedIndexes() if i.column() == gpx.NAME], key, value)

  def skipTracks(self):
    TheDocument.trkmodel.setIncludeStates([i.row() for i in self.ui.trkView.selectedIndexes() if i.column() == gpx.TRKNAME],
                                          not self.sender().isChecked())
    self.setProjectChanged(True)

  def fileNew(self):
    if self.projectChanged and len(TheDocument.doc['GPXFile']) != 0:
      result = QtWidgets.QMessageBox.information(self, self.tr('Load GPX file'),
                                                 self.tr('There are unsaved changes. Do you want to save the project?'),
                                                 QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel,
                                                 QtWidgets.QMessageBox.Yes)
      if result == QtWidgets.QMessageBox.Yes:
        if not self.fileSave():
          return
      if result == QtWidgets.QMessageBox.Cancel:
        return

    self.reset()

  def fileLoadGPXFile(self):
    filenames = QtWidgets.QFileDialog.getOpenFileNames(self, self.tr('Open GPX file'), TheConfig['MainWindow']['LoadGPXDirectory'],
                                                       self.tr('GPX XML (*.gpx);;All files (*)'))[0]
    self.openGPXFiles(filenames)

  def fileSaveGPXFileAs(self):
    if TheDocument.wptmodel.rowCount() == len(TheDocument.wptmodel.getSkippedPoints()) and \
       TheDocument.trkmodel.rowCount() == len(TheDocument.trkmodel.getSkippedTracks()):
      QtWidgets.QMessageBox.warning(self, self.tr('Save error'), self.tr('The GPX file will be empty.'))
      return

    filename = QtWidgets.QFileDialog.getSaveFileName(self, self.tr('Save GPX file as'), TheConfig['MainWindow']['LoadGPXDirectory'],
                                                     self.tr('GPX XML (*.gpx);;All files (*)'))[0]
    if filename != '':
      TheConfig['MainWindow']['LoadGPXDirectory'] = QtCore.QFileInfo(filename).path()
      TheDocument.gpxparser.writeToFile(filename)

  def fileOpen(self):
    if self.projectChanged and len(TheDocument.doc['GPXFile']) != 0:
      result = QtWidgets.QMessageBox.information(self, self.tr('Open GPX Viewer project'),
                                                 self.tr('There are unsaved changes. Do you want to save the project?'),
                                                 QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel,
                                                 QtWidgets.QMessageBox.Yes)
      if result == QtWidgets.QMessageBox.Yes:
        if not self.fileSave():
          return
      if result == QtWidgets.QMessageBox.Cancel:
        return

    filename = QtWidgets.QFileDialog.getOpenFileName(self, self.tr('Open project file'), TheConfig['MainWindow']['ProjectDirectory'],
                                                     self.tr('GPX Viewer Projects (*.gpxv);;All files (*)'))[0]
    if filename != '':
      self.openGPXProject(filename)

  def fileSave(self):
    if not self.projectSaved:
      return self.fileSaveAs()
    else:
      try:
        TheDocument.saveFile(self.projectFile)
      except OSError as e:
        QtWidgets.QMessageBox.warning(self, self.tr('Save error'), e.args[0])
        return False
    self.setProjectChanged(False)
    return True

  def fileSaveAs(self):
    if len(TheDocument.doc['GPXFile']) != 0:
      filename = QtWidgets.QFileDialog.getSaveFileName(self, self.tr('Save project file as'), TheConfig['MainWindow']['ProjectDirectory'],
                                                       self.tr('GPX Viewer Projects (*.gpxv);;All files (*)'))[0]
      if filename != '':
        try:
          TheDocument.saveFile(filename)
          self.projectFile = filename
          self.projectSaved = True
          TheConfig['MainWindow']['ProjectDirectory'] = QtCore.QFileInfo(self.projectFile).path()
          self.setProjectChanged(False)
          self.updateTitleFilename(self.projectFile)
          self.addRecentProject(self.projectFile)
          return True
        except OSError as e:
          QtWidgets.QMessageBox.warning(self, self.tr('Save error'), e.args[0])
          return False
      else:
        return False
    else:
      QtWidgets.QMessageBox.warning(self, self.tr('Save error'), self.tr('The project is empty.'))
      return False

  def openGPXFiles(self, filenames):
    for f in filenames:
      self.openGPXFile(f)
    TheDocument.gpxparser.updatePoints()
    self.updateTabs()

  def openGPXFile(self, filename):
    TheConfig['MainWindow']['LoadGPXDirectory'] = QtCore.QFileInfo(filename).path()
    try:
      TheDocument.gpxparser.parse(filename)
      TheDocument.doc['GPXFile'] += [filename]
      self.setProjectChanged(True)
      if not self.projectSaved:
        if len(TheDocument.doc['GPXFile']) > 1:
          self.updateTitleFilename('[ ' + self.tr('Multiple GPX files') + ' ]')
        else:
          self.updateTitleFilename(filename)
    except gpx.GpxWarning as e:
      QtWidgets.QMessageBox.warning(self, self.tr('File read error'), e.args[0])

  def openGPXProject(self, filename):
    try:
      TheDocument.openFile(filename)
      self.projectFile = filename
      self.projectSaved = True
      TheConfig['MainWindow']['ProjectDirectory'] = QtCore.QFileInfo(self.projectFile).path()
      self.filterModel.invalidateFilter()
      self.ui.wptView.resizeColumnsToContents()
      self.ui.trkView.resizeColumnsToContents()
      self.setProjectChanged(False)
      self.updateTitleFilename(self.projectFile)
      self.updateTabs()
      self.addRecentProject(self.projectFile)
    except gpx.GpxWarning as e:
      self.reset()
      QtWidgets.QMessageBox.warning(self, self.tr('File read error'), e.args[0])

  def openedFileNotFound(self, file):
    result = QtWidgets.QMessageBox.warning(self, self.tr('File read error'), self.tr('The file ') + file + self.tr(' doesn\'t exist.\n\nDo you want to choose another location of this file?'),
                                           QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.YesToAll | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)
    if result in (QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.YesToAll):
      filename = QtWidgets.QFileDialog.getOpenFileName(self, self.tr('Open GPX file') + ' ' + QtCore.QFileInfo(file).fileName(), TheConfig['MainWindow']['LoadGPXDirectory'],
                                                       self.tr('GPX XML (*.gpx);;All files (*)'))[0]
      if filename != '':
        TheConfig['MainWindow']['LoadGPXDirectory'] = QtCore.QFileInfo(filename).path()
        TheDocument.newFilePath = filename
        if result == QtWidgets.QMessageBox.YesToAll:
          TheDocument.applyToAll = True

  def openRecentProject(self):
    if self.projectChanged and len(TheDocument.doc['GPXFile']) != 0:
      result = QtWidgets.QMessageBox.information(self, self.tr('Open GPX Viewer project'),
                                                 self.tr('There are unsaved changes. Do you want to save the project?'),
                                                 QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel,
                                                 QtWidgets.QMessageBox.Yes)
      if result == QtWidgets.QMessageBox.Yes:
        if not self.fileSave():
          return
      if result == QtWidgets.QMessageBox.Cancel:
        return

    for i, act in enumerate(self.actionsRecent):
      if self.sender() == act:
        filename = TheConfig.recentProjects[i]
        if QtCore.QFileInfo(filename).exists():
          self.openGPXProject(filename)
        else:
          result = QtWidgets.QMessageBox.information(self, self.tr('File read error'),
                                                     self.tr('The file ') + filename + self.tr(' doesn\'t exist.\n\nDo you want to remove it from recent projects?'),
                                                     QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
          if result == QtWidgets.QMessageBox.Yes:
            del TheConfig.recentProjects[i]
            self.updateRecentProjects()

  def plotDistanceProfile(self):
    if TheDocument.wptmodel.rowCount() - len(TheDocument.wptmodel.getSkippedPoints()) < 2 and \
       TheDocument.trkmodel.rowCount() == len(TheDocument.trkmodel.getSkippedTracks()):
      QtWidgets.QMessageBox.warning(self, self.tr('Plot error'), self.tr('Not enouph points or tracks.'))
      return

    self.plot.setWindowTitle(self.tr('Distance Profile'))
    if TheConfig.getValue('ProfileStyle', 'SelectedPointsOnly'):
      self.plot.plotProfile(gpx.DIST, [i.data(gpx.IDRole) for i in self.ui.wptView.selectionModel().selectedRows()], [i.row() for i in self.ui.trkView.selectionModel().selectedRows()])
    else:
      self.plot.plotProfile(gpx.DIST)
    self.plot.show()
    self.plot.activateWindow()

  def plotTimeProfile(self):
    # Check if there are at least two points with timestamps
    n = 0
    for i in range(TheDocument.wptmodel.rowCount()):
      if TheDocument.wptmodel.index(i, 0).data(gpx.IncludeRole) and TheDocument.wptmodel.index(i, gpx.TIME).data() != '':
        n += 1
      if n == 2:
        break
    if n < 2:
      for j in range(TheDocument.trkmodel.rowCount()):
        if TheDocument.trkmodel.index(j, 0).data(gpx.IncludeRole) and TheDocument.trkmodel.index(i, gpx.TRKTIME).data() != '':
          n = 2
          break
      if n < 2:
        QtWidgets.QMessageBox.warning(self, self.tr('Plot error'), self.tr('Not enouph points or tracks.'))
        return

    self.plot.setWindowTitle(self.tr('Time Profile'))
    if TheConfig.getValue('ProfileStyle', 'SelectedPointsOnly'):
      self.plot.plotProfile(gpx.TIME_DAYS, [i.data(gpx.IDRole) for i in self.ui.wptView.selectionModel().selectedRows()], [i.row() for i in self.ui.trkView.selectionModel().selectedRows()])
    else:
      self.plot.plotProfile(gpx.TIME_DAYS)
    self.plot.show()
    self.plot.activateWindow()

  def showStatistics(self):
    if TheDocument.wptmodel.rowCount() - len(TheDocument.wptmodel.getSkippedPoints()) < 2:
      QtWidgets.QMessageBox.warning(self, self.tr('Statistics error'), self.tr('Not enouph points.'))
      return

    self.stat.show()
    self.stat.activateWindow()

  def showSkipped(self, show):
    TheConfig['MainWindow']['ShowSkipped'] = str(show)
    self.updateIncludeFilter()

  def showMarked(self, show):
    TheConfig['MainWindow']['ShowMarked'] = str(show)
    self.updateIncludeFilter()

  def showCaptioned(self, show):
    TheConfig['MainWindow']['ShowCaptioned'] = str(show)
    self.updateIncludeFilter()

  def showMarkedCaptioned(self, show):
    TheConfig['MainWindow']['ShowMarkedCaptioned'] = str(show)
    self.updateIncludeFilter()

  def showOther(self, show):
    TheConfig['MainWindow']['ShowDefault'] = str(show)
    self.updateIncludeFilter()

  def resetFilters(self):
    self.ui.actionShowSkipped.setChecked(True)
    self.ui.actionShowMarked.setChecked(True)
    self.ui.actionShowCaptioned.setChecked(True)
    self.ui.actionShowMarkedCaptioned.setChecked(True)
    self.ui.actionShowOther.setChecked(True)

  def showSettings(self):
    dlg = gpxviewer.settingsdialog.SettingsDialog(self)
    if dlg.exec_() == QtWidgets.QDialog.Accepted:
      self.setProjectChanged(True)
      TheConfig['ProfileStyle']['ProfileColor'] = str(dlg.settings['ProfileColor'])
      TheConfig['ProfileStyle']['FillColor'] = str(dlg.settings['FillColor'])
      TheConfig['ProfileStyle']['ProfileWidth'] = str(dlg.settings['ProfileWidth'])
      TheConfig['ProfileStyle']['MinimumAltitude'] = str(dlg.settings['MinimumAltitude'])
      TheConfig['ProfileStyle']['MaximumAltitude'] = str(dlg.settings['MaximumAltitude'])
      TheConfig['ProfileStyle']['DistanceCoefficient'] = str(dlg.settings['DistanceCoefficient'])
      TheConfig['ProfileStyle']['TimeZoneOffset'] = str(dlg.settings['TimeZoneOffset'])
      TheConfig['ProfileStyle']['SelectedPointsOnly'] = str(dlg.settings['SelectedPointsOnly'])
      TheConfig['ProfileStyle']['ReadNameFromTag'] = str(dlg.settings['ReadNameFromTag'])
      TheConfig['ProfileStyle']['CoordinateFormat'] = str(dlg.settings['CoordinateFormat'])
      TheDocument.gpxparser.updateDistance()
      self.ui.wptView.resizeColumnsToContents()

  def showWarning(self, title, text):
    QtWidgets.QMessageBox.warning(self, title, text)

  def reset(self):
    self.projectFile = ''
    self.projectSaved = False
    self.setProjectChanged(False)
    TheDocument.doc['GPXFile'] = []
    TheDocument.gpxparser.resetModels()
    self.setWindowTitle('GPX Viewer')
    self.ui.wptView.setDisabled(True)
    self.ui.trkView.setDisabled(True)

  def updateIncludeFilter(self):
    self.filterModel.setFilterMask(TheConfig['MainWindow'].getboolean('ShowSkipped'),
                                          TheConfig['MainWindow'].getboolean('ShowMarked'),
                                          TheConfig['MainWindow'].getboolean('ShowCaptioned'),
                                          TheConfig['MainWindow'].getboolean('ShowMarkedCaptioned'),
                                          TheConfig['MainWindow'].getboolean('ShowDefault'))
    self.ui.wptView.resizeColumnsToContents()

  def updateTitleFilename(self, title=None):
    if title is not None:
      self.titleFilename = title
    if self.titleFilename is not None:
      self.setWindowTitle(self.titleFilename + ('*' if self.projectChanged else '') + ' — GPX Viewer')

  def updateTabs(self):
    self.ui.wptView.setEnabled(TheDocument.wptmodel.rowCount() != 0)
    self.ui.trkView.setEnabled(TheDocument.trkmodel.rowCount() != 0)
    if TheDocument.wptmodel.rowCount() != 0:
      self.ui.wptView.resizeColumnsToContents()
      if TheDocument.trkmodel.rowCount() == 0:
        self.ui.tabWidget.setCurrentWidget(self.ui.wptTab)
    if TheDocument.trkmodel.rowCount() != 0:
      self.ui.trkView.resizeColumnsToContents()
      if TheDocument.wptmodel.rowCount() == 0:
        self.ui.tabWidget.setCurrentWidget(self.ui.trkTab)

  def addRecentProject(self, filename):
    if filename in TheConfig.recentProjects:
      TheConfig.recentProjects.remove(filename)
    TheConfig.recentProjects.insert(0, filename)
    if len(TheConfig.recentProjects) > TheConfig['MainWindow'].getint('MaxRecentProjects'):
      del TheConfig.recentProjects[-1]
    self.updateRecentProjects()

  def updateRecentProjects(self):
    for act in self.actionsRecent:
      self.ui.menuRecentProjects.removeAction(act)
    self.actionsRecent = []
    for p in TheConfig.recentProjects:
      act = QtWidgets.QAction(QtCore.QFileInfo(p).fileName() + ' [' + p + ']', self)
      act.triggered.connect(self.openRecentProject)
      self.actionsRecent += [act]
    self.ui.menuRecentProjects.insertActions(self.ui.actionClearList, self.actionsRecent)
    if len(TheConfig.recentProjects) > 0:
      self.ui.menuRecentProjects.insertSeparator(self.ui.actionClearList)
      self.ui.actionClearList.setEnabled(True)
    else:
      self.ui.actionClearList.setDisabled(True)

  def clearRecentList(self):
    for act in self.actionsRecent:
      self.ui.menuRecentProjects.removeAction(act)
    self.actionsRecent = []
    TheConfig.recentProjects = []
    self.ui.actionClearList.setDisabled(True)
