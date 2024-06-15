# gpxviewer
#
# Copyright (C) 2016-2024 Sergey Salnikov <salsergey@gmail.com>
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
from PyQt6.QtCore import Qt, QCoreApplication, QEvent, QFileInfo, QFileSelector, QUrl, QT_VERSION, QT_VERSION_STR, PYQT_VERSION_STR, pyqtSlot
from PyQt6.QtGui import QAction, QCursor, QIcon, QKeySequence
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from PyQt6.QtWidgets import (QApplication, QDialog, QDialogButtonBox, QFileDialog, QHBoxLayout, QLabel, QLineEdit,
                             QMainWindow, QMenu, QMessageBox, QSizePolicy, QSpacerItem, QSpinBox, QVBoxLayout, QWidget)
import gpxviewer.gpxmodel as gpx
import gpxviewer.statwindow as stat
import gpxviewer.plotviewer as plt
from gpxviewer.configstore import TheConfig
from gpxviewer.gpxdocument import *
from gpxviewer.pointconfigdialog import PointConfigDialog
from gpxviewer.settingsdialog import SettingsDialog
import gpxviewer.ui_mainwindow


class GpxMainWindow(QMainWindow):
  def __init__(self):
    super(GpxMainWindow, self).__init__()
    self.ui = gpxviewer.ui_mainwindow.Ui_MainWindow()
    self.ui.setupUi(self)

    self.updateTheme()
    self.initActions()
    self.ui.wptView.setFocus()

    wdg = QWidget()
    wdg.setLayout(QHBoxLayout())
    wdg.layout().addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding))
    wdg.layout().addWidget(QLabel(self.tr('Filter by name:')))
    self.filterLineEdit = QLineEdit()
    self.filterLineEdit.setMinimumWidth(200)
    self.filterLineEdit.setPlaceholderText(self.tr('Enter regular expression'))
    self.filterLineEdit.setClearButtonEnabled(True)
    wdg.layout().addWidget(self.filterLineEdit)
    self.ui.filterToolBar.addWidget(wdg)

    self.filterModel = gpx.GpxSortFilterModel(self)
    self.filterModel.setSourceModel(TheDocument.wptmodel)
    self.filterModel.setFilterKeyColumn(gpx.NAME)
    self.filterLineEdit.textChanged.connect(self.filterModel.setFilterRegularExpression)
    self.updateIncludeFilter()

    self.ui.wptView.setModel(self.filterModel)
    self.ui.wptView.setSortingEnabled(True)
    self.ui.wptView.sortByColumn(gpx.TIME, Qt.SortOrder.AscendingOrder)
    self.ui.trkView.setModel(TheDocument.trkmodel)
    self.ui.wptView.installEventFilter(self)
    self.ui.trkView.installEventFilter(self)

    self.networkManager = QNetworkAccessManager(self)
    if QT_VERSION >= 0x050f00:  # function introduced in 5.15.0
      self.networkManager.setTransferTimeout(10000)
    self.networkManager.finished[QNetworkReply].connect(self.replyReady)

    self.ui.actionDetailedView.setChecked(TheConfig['MainWindow'].getboolean('DetailedView'))
    self.ui.actionShowSkipped.setChecked(TheConfig['MainWindow'].getboolean('ShowSkipped'))
    self.ui.actionShowMarked.setChecked(TheConfig['MainWindow'].getboolean('ShowMarked'))
    self.ui.actionShowCaptioned.setChecked(TheConfig['MainWindow'].getboolean('ShowCaptioned'))
    self.ui.actionShowMarkedCaptioned.setChecked(TheConfig['MainWindow'].getboolean('ShowMarkedCaptioned'))
    self.ui.actionShowOther.setChecked(TheConfig['MainWindow'].getboolean('ShowDefault'))

    self.ui.tabWidget.currentChanged[int].connect(self.onTabChanged)
    TheDocument.gpxparser.warningSent[str, str].connect(self.showWarning)
    TheDocument.wptmodel.wptDataChanged.connect(self.setProjectChanged)
    TheDocument.trkmodel.trkDataChanged.connect(self.setProjectChanged)
    TheDocument.fileNotFound[str].connect(self.openedFileNotFound)
    TheDocument.askToExtractFiles[list].connect(self.askedExtractFiles)

    self.projectSaved = False
    self.projectChanged = False
    self.titleFilename = None
    self.actionsRecent = []
    self.actionsColumns = []

    self.updateRecentProjects()
    self.initColumnsToCopy()
    self.resize(TheConfig['MainWindow'].getint('WindowWidth'), TheConfig['MainWindow'].getint('WindowHeight'))

    self.plotWindow = plt.PlotWindow()
    self.plotWindow.profileChanged.connect(self.setProjectChanged)
    self.plotWindow.gotoMainWindow[int].connect(self.onGotoMainWindow)
    self.statWindow = stat.StatWindow()

  def updateTheme(self):
    self.themeSelector = QFileSelector()
    self.themeSelector.setExtraSelectors([TheConfig['MainWindow']['ColorTheme']])

    self.setWindowIcon(QIcon(':/icons/gpxviewer.svg'))
    self.ui.actionLoadFile.setIcon(QIcon(self.themeSelector.select(':/icons/xml-element-new.svg')))
    self.ui.actionSaveFileAs.setIcon(QIcon(self.themeSelector.select(':/icons/document-save-as-template.svg')))
    self.ui.actionNew.setIcon(QIcon(self.themeSelector.select(':/icons/document-new.svg')))
    self.ui.actionOpen.setIcon(QIcon(self.themeSelector.select(':/icons/document-open.svg')))
    self.ui.actionSave.setIcon(QIcon(self.themeSelector.select(':/icons/document-save.svg')))
    self.ui.actionSaveAs.setIcon(QIcon(self.themeSelector.select(':/icons/document-save-as.svg')))
    self.ui.menuRecentProjects.setIcon(QIcon(self.themeSelector.select(':/icons/document-open-recent.svg')))
    self.ui.actionQuit.setIcon(QIcon(':/icons/application-exit.svg'))
    self.ui.actionCopy.setIcon(QIcon(self.themeSelector.select(':/icons/edit-copy.svg')))
    self.ui.actionSettings.setIcon(QIcon(self.themeSelector.select(':/icons/configure.svg')))
    self.ui.actionDistanceProfile.setIcon(QIcon(self.themeSelector.select(':/icons/distanceprofile.svg')))
    self.ui.actionTimeProfile.setIcon(QIcon(self.themeSelector.select(':/icons/timeprofile.svg')))
    self.ui.actionStatistics.setIcon(QIcon(self.themeSelector.select(':/icons/view-statistics.svg')))
    self.ui.actionGpxViewerHelp.setIcon(QIcon(self.themeSelector.select(':/icons/help-contents.svg')))
    self.ui.actionAboutQt.setIcon(QIcon.fromTheme('qtlogo', QIcon(':/icons/qtlogo.svg')))
    self.ui.actionAboutGPXViewer.setIcon(QIcon(':/icons/gpxviewer.svg'))

  def initActions(self):
    self.ui.actionNew.setShortcut(QKeySequence.StandardKey.New)
    self.ui.actionOpen.setShortcut(QKeySequence.StandardKey.Open)
    self.ui.actionSave.setShortcut(QKeySequence.StandardKey.Save)
    self.ui.actionSaveAs.setShortcut(QKeySequence.StandardKey.SaveAs)
    self.ui.actionQuit.setShortcut(QKeySequence.StandardKey.Quit)
    self.ui.actionCopy.setShortcut(QKeySequence.StandardKey.Copy)
    self.ui.actionSettings.setShortcut(QKeySequence.StandardKey.Preferences)
    self.ui.actionGpxViewerHelp.setShortcut(QKeySequence.StandardKey.HelpContents)

    self.actSkipPoints = QAction(QIcon(self.themeSelector.select(':/icons/waypoint-skip.svg')), self.tr('Skip points'), self)
    self.actSkipPoints.setStatusTip(self.tr('Skip these waypoints when plotting profiles or calculating statistics'))
    self.actSkipPoints.setShortcut(QKeySequence(Qt.Key.Key_Delete))
    self.actSkipPoints.setCheckable(True)
    self.actSkipPoints.triggered.connect(self.skipPoints)
    self.addAction(self.actSkipPoints)

    self.actMarker = QAction(QIcon(self.themeSelector.select(':/icons/waypoint-marker.svg')), self.tr('Points with markers'), self)
    self.actMarker.setStatusTip(self.tr('Add markers to these waypoints when plotting profiles'))
    self.actMarker.setShortcut(QKeySequence(Qt.Key.Key_M))
    self.actMarker.setCheckable(True)
    self.actMarker.triggered.connect(self.markerPoints)
    self.addAction(self.actMarker)

    self.actCaption = QAction(QIcon(self.themeSelector.select(':/icons/waypoint-caption.svg')), self.tr('Points with captions'), self)
    self.actCaption.setStatusTip(self.tr('Add captions to these waypoints when plotting profiles'))
    self.actCaption.setShortcut(QKeySequence(Qt.Key.Key_C))
    self.actCaption.setCheckable(True)
    self.actCaption.triggered.connect(self.captionPoints)
    self.addAction(self.actCaption)

    self.actSplit = QAction(QIcon(self.themeSelector.select(':/icons/waypoint-splitline.svg')), self.tr('Points with splitting lines'), self)
    self.actSplit.setStatusTip(self.tr('Add splitting lines to these waypoints when plotting profiles'))
    self.actSplit.setShortcut(QKeySequence(Qt.Key.Key_S))
    self.actSplit.setCheckable(True)
    self.actSplit.triggered.connect(self.splitLines)
    self.addAction(self.actSplit)

    self.actNeglect = QAction(QIcon(self.themeSelector.select(':/icons/waypoint-neglect-distance.svg')), self.tr('Neglect previous distance'), self)
    self.actNeglect.setStatusTip(self.tr('Neglect distance before these waypoints when plotting profiles'))
    self.actNeglect.setShortcut(QKeySequence(Qt.Key.Key_N))
    self.actNeglect.setCheckable(True)
    self.actNeglect.triggered.connect(self.neglectDistance)
    self.addAction(self.actNeglect)

    self.actReset = QAction(QIcon(self.themeSelector.select(':/icons/edit-clear-all.svg')), self.tr('Reset appearance'), self)
    self.actReset.setStatusTip(self.tr('Reset appearance of these waypoints'))
    self.actReset.triggered.connect(self.resetPoints)
    self.addAction(self.actReset)

    self.actRename = QAction(QIcon(self.themeSelector.select(':/icons/edit-rename.svg')), self.tr('Rename...'), self)
    self.actRename.setStatusTip(self.tr('Rename these waypoints'))
    self.actRename.setShortcut(QKeySequence(Qt.Key.Key_F2))
    self.actRename.triggered.connect(self.renamePoints)
    self.addAction(self.actRename)

    self.actResetName = QAction(QIcon(self.themeSelector.select(':/icons/edit-clear.svg')), self.tr('Reset name'), self)
    self.actResetName.setStatusTip(self.tr('Reset the names of these waypoints'))
    self.actResetName.triggered.connect(self.resetPointNames)
    self.addAction(self.actResetName)

    self.actStyle = QAction(QIcon(self.themeSelector.select(':/icons/configure.svg')), self.tr('Point style'), self)
    self.actStyle.setStatusTip(self.tr('Change the style of these waypoints when plotting profiles'))
    self.actStyle.setShortcut(QKeySequence(Qt.Modifier.ALT | Qt.Key.Key_Return))
    self.actStyle.triggered.connect(self.pointStyle)
    self.addAction(self.actStyle)

    self.actGetAltitude = QAction(QIcon(self.themeSelector.select(':/icons/download.svg')), self.tr('Get altitudes from SRTM'), self)
    self.actGetAltitude.setStatusTip(self.tr('Get altitudes from online SRTM data'))
    self.actGetAltitude.triggered.connect(self.requestAltitudes)
    self.addAction(self.actGetAltitude)

    self.actResetAltitude = QAction(QIcon(self.themeSelector.select(':/icons/edit-clear.svg')), self.tr('Reset altitude'), self)
    self.actResetAltitude.setStatusTip(self.tr('Reset the altitudes of these waypoints'))
    self.actResetAltitude.triggered.connect(self.resetAltitudes)
    self.addAction(self.actResetAltitude)

    self.actSkipTracks = QAction(QIcon(self.themeSelector.select(':/icons/waypoint-skip.svg')), self.tr('Skip tracks'), self)
    self.actSkipTracks.setStatusTip(self.tr('Skip these tracks when plotting profiles or calculating statistics'))
    self.actSkipTracks.setShortcut(QKeySequence(Qt.Key.Key_Delete))
    self.actSkipTracks.setCheckable(True)
    self.actSkipTracks.triggered.connect(self.skipTracks)
    self.addAction(self.actSkipTracks)

    self.actGetTrackAltitude = QAction(QIcon(self.themeSelector.select(':/icons/download.svg')), self.tr('Get altitudes from SRTM'), self)
    self.actGetTrackAltitude.setStatusTip(self.tr('Get altitudes from online SRTM data'))
    self.actGetTrackAltitude.triggered.connect(self.requestTrackAltitudes)
    self.addAction(self.actGetTrackAltitude)

    self.actResetTrackAltitude = QAction(QIcon(self.themeSelector.select(':/icons/edit-clear.svg')), self.tr('Reset altitude'), self)
    self.actResetTrackAltitude.setStatusTip(self.tr('Reset the altitudes of these tracks'))
    self.actResetTrackAltitude.triggered.connect(self.resetTrackAltitudes)
    self.addAction(self.actResetTrackAltitude)

  @pyqtSlot()
  def onAboutQt(self):
    QApplication.aboutQt()

  def eventFilter(self, obj, event):
    if obj == self.ui.wptView:
      if event.type() == QEvent.Type.ContextMenu or (event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_Menu and event.modifiers() == Qt.KeyboardModifier.NoModifier):
        self.wptContextMenuEvent(event)
        return True

      elif event.type() == QEvent.Type.KeyPress:
        self.keyPressEvent(event)
        # Do not return True

    elif obj == self.ui.trkView:
      if event.type() == QEvent.Type.ContextMenu or (event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_Menu and event.modifiers() == Qt.KeyboardModifier.NoModifier):
        self.trkContextMenuEvent(event)
        return True

      elif event.type() == QEvent.Type.KeyPress:
        self.keyPressEvent(event)
        # Do not return True

    return super(GpxMainWindow, self).eventFilter(obj, event)

  def closeEvent(self, event):
    if not self.closeChangedProject(self.tr('Close GPX Viewer')):
      event.ignore()
      return

    self.plotWindow.close()
    self.statWindow.close()
    TheDocument.close()
    TheConfig.save()
    super(GpxMainWindow, self).closeEvent(event)

  def wptContextMenuEvent(self, event):
    if self.ui.wptView.selectionModel().hasSelection():
      self.actSkipPoints.setChecked(not self.ui.wptView.currentIndex().data(gpx.IncludeRole))
      self.actMarker.setChecked(self.ui.wptView.currentIndex().data(gpx.MarkerRole))
      self.actCaption.setChecked(self.ui.wptView.currentIndex().data(gpx.CaptionRole))
      self.actSplit.setChecked(self.ui.wptView.currentIndex().data(gpx.SplitLineRole))
      self.actNeglect.setChecked(self.ui.wptView.currentIndex().data(gpx.NeglectRole))

      menu = QMenu(self)
      menu.addAction(self.actMarker)
      menu.addAction(self.actCaption)
      menu.addAction(self.actSplit)
      menu.addAction(self.actNeglect)
      menu.addAction(self.actReset)
      menu.addSeparator()
      menu.addAction(self.actSkipPoints)
      menu.addSeparator()
      menu.addAction(self.actRename)
      menu.addAction(self.actResetName)
      menu.addSeparator()
      menu.addAction(self.actStyle)
      menu.addSeparator()
      menu.addAction(self.actGetAltitude)
      menu.addAction(self.actResetAltitude)

      actShowGoogleMap = QAction(QIcon(':/icons/googlemaps.png'), self.tr('Google Maps'), self)
      actShowGoogleMap.setStatusTip(self.tr('Show this waypoint on the website maps.google.com'))
      actShowGoogleMap.triggered.connect(self.showGoogleMap)

      actShowYandexMap = QAction(QIcon(':/icons/yandexmaps.png'), self.tr('Yandex Maps'), self)
      actShowYandexMap.setStatusTip(self.tr('Show this waypoint on the website maps.yandex.ru'))
      actShowYandexMap.triggered.connect(self.showYandexMap)

      actShowNakarteMap = QAction(QIcon(':/icons/nakarte.png'), self.tr('Nakarte.me'), self)
      actShowNakarteMap.setStatusTip(self.tr('Show this waypoint on the website nakarte.me'))
      actShowNakarteMap.triggered.connect(self.showNakarteMap)

      showMapMenu = QMenu(self.tr('Show on map'), self)
      showMapMenu.setIcon(QIcon(self.themeSelector.select(':/icons/internet-services.svg')))
      showMapMenu.addAction(actShowGoogleMap)
      showMapMenu.addAction(actShowYandexMap)
      showMapMenu.addAction(actShowNakarteMap)
      menu.addMenu(showMapMenu)

      menu.popup(QCursor.pos())
      event.accept()

  def trkContextMenuEvent(self, event):
    if self.ui.trkView.selectionModel().hasSelection():
      self.actSkipTracks.setChecked(not self.ui.trkView.currentIndex().data(gpx.IncludeRole))

      menu = QMenu(self)
      menu.addAction(self.actSkipTracks)
      menu.addSeparator()
      menu.addAction(self.actGetTrackAltitude)
      menu.addAction(self.actResetTrackAltitude)
      menu.popup(QCursor.pos())
      event.accept()

  def keyPressEvent(self, event):
    if event.matches(QKeySequence.StandardKey.Find):
      self.filterLineEdit.setFocus()
      self.filterLineEdit.selectAll()

    elif event.key() == Qt.Key.Key_Escape:
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

    elif event.key() == Qt.Key.Key_Tab and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
      self.ui.tabWidget.setCurrentIndex(1 - self.ui.tabWidget.currentIndex())

    super(GpxMainWindow, self).keyPressEvent(event)

  def resizeEvent(self, event):
    super(GpxMainWindow, self).resizeEvent(event)
    self.ui.wptView.resizeColumnsToContents()
    self.ui.trkView.resizeColumnsToContents()
    TheConfig['MainWindow']['WindowWidth'] = str(event.size().width())
    TheConfig['MainWindow']['WindowHeight'] = str(event.size().height())

  def dragEnterEvent(self, event):
    if event.mimeData().hasUrls():
      event.acceptProposedAction()

  def dropEvent(self, event):
    filenames = [url.toLocalFile() for url in event.mimeData().urls() if QFileInfo(url.toLocalFile()).exists()]
    if len(filenames) == 0:
      QMessageBox.warning(self, self.tr('File open error'), self.tr('Can\'t transform recieved data to local file names.'))
      return

    if filenames[0].lower().endswith('.gpx') or filenames[0].lower().endswith('.kml'):
      self.openGPXFiles(filenames)
    elif self.closeChangedProject(self.tr('Open GPX Viewer project')):
      self.openGPXProject(filenames[0])

  @pyqtSlot()
  def onAboutGPXViewer(self):
    aboutText = '<h3>GPX Viewer</h3><b>' + self.tr('Version') + ' ' + QCoreApplication.applicationVersion() + '</b><br><br>' + \
                self.tr('Using') + ' Python ' + str(sys.version_info.major) + '.' + str(sys.version_info.minor) + '.' + str(sys.version_info.micro) + ', ' + \
                'PyQt' + PYQT_VERSION_STR[0] + ' ' + PYQT_VERSION_STR + ', ' + \
                'Qt ' + QT_VERSION_STR + '<br><br>' + \
                'Copyright 2016-2024 Sergey Salnikov <a href=mailto:salsergey@gmail.com>&lt;salsergey@gmail.com&gt;</a><br><br>' + \
                self.tr('License:') + ' <a href=http://www.gnu.org/licenses/gpl.html>GNU General Public License, version 3</a>'
    QMessageBox.about(self, self.tr('About GPX Viewer'), aboutText)

  @pyqtSlot()
  def onGpxViewerHelp(self):
    aboutText = self.tr('''Notation:<br>
                           <font color=red>Red</font> - skipped points<br>
                           <font color=blue>Blue</font> - marked points<br>
                           <font color=green>Green</font> - captioned points<br>
                           <b>Bold</b> - points with splitting lines<br>
                           <i>Italic</i> - distance before these points is neglected<br>
                           <br>
                           F2 - Rename multiple points.
                           Several symbols "#" are replaced by sequential numbers.
                           The number of digits equals to the amount of symbols "#".<br>
                           <br>
                           Several cases are possible when plotting a profile:
                           <ul>
                           <li>All non-skipped points have timestamps: points and tracks with timestamps are taken into account</li>
                           <li>There are points without timestamps: only points are considered, tracks are skipped</li>
                           <li>There are no points: all non-skipped tracks are taken into account</li>
                           </ul><br>
                           <br>
                           Several interactions are possible in profile window:
                           <ul>
                           <li>Left/right mouse buttons select markers or captions</li>
                           <li>Hold Ctrl button to select multiple points</li>
                           <li>Selected captions are moved by up/down/left/right buttons (with or without Ctrl)</li>
                           <li>Selected markers are changed by left/right buttons (with or without Ctrl)</li>
                           <li>Mouse wheel zooms the image horizontally</li>
                           <li>Left mouse button drags the image horizontally</li>
                           <li>Mouse wheel over the left axis changes minimum/maximum altitude</li>
                           </ul>''')
    msg = QMessageBox(self)
    msg.setWindowTitle(self.tr('GPX Viewer Help'))
    msg.setTextFormat(Qt.TextFormat.RichText)
    msg.setText(aboutText)
    msg.setIcon(QMessageBox.Icon.Information)
    msg.exec()

  @pyqtSlot()
  @pyqtSlot(bool)
  def setProjectChanged(self, value=True):
    self.projectChanged = value
    self.updateTitleFilename()

  @pyqtSlot()
  def skipPoints(self):
    included = self.ui.wptView.currentIndex().data(gpx.IncludeRole)
    TheDocument.wptmodel.setIncludeStates([i.data(gpx.IDRole) for i in self.ui.wptView.selectionModel().selectedRows()], not included)
    self.filterModel.invalidateFilter()

  @pyqtSlot()
  def markerPoints(self):
    marked = self.ui.wptView.currentIndex().data(gpx.MarkerRole)
    TheDocument.wptmodel.setMarkerStates([i.data(gpx.IDRole) for i in self.ui.wptView.selectionModel().selectedRows()], not marked)
    self.filterModel.invalidateFilter()

  @pyqtSlot()
  def captionPoints(self):
    captioned = self.ui.wptView.currentIndex().data(gpx.CaptionRole)
    TheDocument.wptmodel.setCaptionStates([i.data(gpx.IDRole) for i in self.ui.wptView.selectionModel().selectedRows()], not captioned)
    self.filterModel.invalidateFilter()

  @pyqtSlot()
  def splitLines(self):
    splited = self.ui.wptView.currentIndex().data(gpx.SplitLineRole)
    TheDocument.wptmodel.setSplitLines([i.data(gpx.IDRole) for i in self.ui.wptView.selectionModel().selectedRows()], not splited)
    self.filterModel.invalidateFilter()

  @pyqtSlot()
  def neglectDistance(self):
    neglected = self.ui.wptView.currentIndex().data(gpx.NeglectRole)
    TheDocument.wptmodel.setNeglectStates([i.data(gpx.IDRole) for i in self.ui.wptView.selectionModel().selectedRows()], not neglected)

  @pyqtSlot()
  def resetPoints(self):
    indexes = [i.data(gpx.IDRole) for i in self.ui.wptView.selectionModel().selectedRows()]
    TheDocument.wptmodel.setMarkerStates(indexes, False)
    TheDocument.wptmodel.setCaptionStates(indexes, False)
    TheDocument.wptmodel.setSplitLines(indexes, False)
    TheDocument.wptmodel.setNeglectStates(indexes, False)
    self.filterModel.invalidateFilter()

  @pyqtSlot()
  def renamePoints(self):
    indexes = [i.data(gpx.IDRole) for i in self.ui.wptView.selectionModel().selectedRows()]
    indexes.sort()
    first_name = TheDocument.wptmodel.index(indexes[0], gpx.NAME).data()

    dlg = QDialog(self)
    dlg.setWindowTitle(self.tr('Rename waypoints'))
    vLayout = QVBoxLayout()
    vLayout.addWidget(QLabel(self.tr('Enter new name for ') + str(len(indexes)) + self.tr(' waypoints:')))
    dlg.setLayout(vLayout)

    nameEdit = QLineEdit(dlg)
    nameEdit.setText(first_name + (' #' if len(indexes) > 1 else ''))
    nameEdit.setSelection(0, len(first_name))
    vLayout.addWidget(nameEdit)

    hLayout = QHBoxLayout()
    hLayout.addWidget(QLabel(self.tr('Several symbols "#" will be replaced by sequential numbers starting from:')))
    vLayout.addLayout(hLayout)

    numberBox = QSpinBox(dlg)
    numberBox.setValue(1)
    hLayout.addWidget(numberBox)

    buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
    buttons.accepted.connect(dlg.accept)
    buttons.rejected.connect(dlg.reject)
    vLayout.addWidget(buttons)

    if dlg.exec() == QDialog.DialogCode.Accepted and len(nameEdit.text()) > 0:
      for n, ind in enumerate(indexes, numberBox.value()):
        name = nameEdit.text()
        if re.match('.*#+', name):
          digits = len(re.findall('(#+)', name)[0])
          name = re.sub('#+', str(n).zfill(digits), name, 1)
        TheDocument.wptmodel.setData(TheDocument.wptmodel.index(ind, gpx.NAME), name, Qt.ItemDataRole.EditRole)

  @pyqtSlot()
  def resetPointNames(self):
    TheDocument.wptmodel.resetNames([i.data(gpx.IDRole) for i in self.ui.wptView.selectionModel().selectedRows()])

  @pyqtSlot()
  def requestAltitudes(self):
    allIndexes = [i.data(gpx.IDRole) for i in self.ui.wptView.selectionModel().selectedRows()]
    maxCount = 20  # maximum number of coordinates requested at once
    cumNumber = 0
    self.requestedIndexes = {}
    self.showNetworkError = True

    while cumNumber < len(allIndexes):
      num = min(len(allIndexes) - cumNumber, maxCount)
      indexes = allIndexes[cumNumber:cumNumber + num]
      cumNumber += num
      lats = [str(TheDocument.wptmodel.index(i, gpx.LAT).data(gpx.ValueRole)) for i in indexes]
      lons = [str(TheDocument.wptmodel.index(i, gpx.LON).data(gpx.ValueRole)) for i in indexes]
      request = 'http://api.geonames.org/srtm1?lats=' + ','.join(lats) + '&lngs=' + ','.join(lons) + '&username=gpxviewer'
      self.requestedIndexes[request] = indexes
      self.networkManager.get(QNetworkRequest(QUrl(request)))
      self.ui.statusBar.showMessage(self.tr('Getting altitudes from SRTM data...'))

  @pyqtSlot(QNetworkReply)
  def replyReady(self, reply):
    reply.deleteLater()
    if reply.error() != QNetworkReply.NetworkError.NoError and self.showNetworkError:
      self.showNetworkError = False
      QMessageBox.warning(self, self.tr('Network error'),
                          self.tr('Error requesting SRTM data from http://geonames.org.') + '\n\n' + reply.errorString())

    else:
      request = reply.request().url().toString()
      line = ''
      try:
        indexes = self.requestedIndexes.pop(request)
        alts = []
        while not reply.atEnd():
          line = reply.readLine()
          alts += [int(line)]

        if type(indexes) == list:  # waypoints
          TheDocument.wptmodel.setAltitudes(indexes, alts)
        elif type(indexes) == tuple:  # tracks
          TheDocument.trkmodel.setPointsAltitudes(indexes[0], indexes[1], indexes[2], alts)

      except ValueError:
        self.showNetworkError = False
        QMessageBox.warning(self, self.tr('Network error'),
                            self.tr('Error requesting SRTM data from http://geonames.org.') + '\n\n' + str(line, 'utf-8'))

      if len(self.requestedIndexes) == 0:
        self.ui.statusBar.showMessage(self.tr('Getting altitudes from SRTM data finished.'), 2000)

  @pyqtSlot()
  def resetAltitudes(self):
    TheDocument.wptmodel.resetAltitudes([i.data(gpx.IDRole) for i in self.ui.wptView.selectionModel().selectedRows()])
    self.ui.statusBar.showMessage(self.tr('Altitudes reset to original values.'), 2000)

  @pyqtSlot()
  def requestTrackAltitudes(self):
    track = self.ui.trkView.currentIndex().row()
    maxCount = 20  # maximum number of coordinates requested at once
    self.requestedIndexes = {}

    for s, segment in enumerate(TheDocument.trkmodel.tracks[track]['SEGMENTS']):
      cumNumber = 0
      while cumNumber < len(segment):
        num = min(len(segment) - cumNumber, maxCount)
        indexes = range(cumNumber, cumNumber + num)
        cumNumber += num
        lats = [str(segment[i][gpx.LAT]) for i in indexes]
        lons = [str(segment[i][gpx.LON]) for i in indexes]
        request = 'http://api.geonames.org/srtm1?lats=' + ','.join(lats) + '&lngs=' + ','.join(lons) + '&username=gpxviewer'
        self.requestedIndexes[request] = (track, s, indexes)
        self.networkManager.get(QNetworkRequest(QUrl(request)))
        self.ui.statusBar.showMessage(self.tr('Getting altitudes from SRTM data...'))

  @pyqtSlot()
  def resetTrackAltitudes(self):
    TheDocument.trkmodel.resetAltitudes([i.row() for i in self.ui.trkView.selectionModel().selectedRows()])
    self.ui.statusBar.showMessage(self.tr('Altitudes reset to original values.'), 2000)

  @pyqtSlot(int)
  def onGotoMainWindow(self, index):
    model = self.ui.wptView.model()
    for row in range(model.rowCount()):
      if model.index(row, 0).data(gpx.IDRole) == index:
        self.ui.wptView.selectRow(row)
        self.activateWindow()
        break
    else:
      self.ui.wptView.clearSelection()
      self.activateWindow()
      QMessageBox.warning(self, self.tr('Go to point error'), self.tr('This point is hidden because of filter settings.'))

  @pyqtSlot()
  def showGoogleMap(self):
    lat = str(TheDocument.wptmodel.index(self.ui.wptView.currentIndex().data(gpx.IDRole), gpx.LAT).data(gpx.ValueRole))
    lon = str(TheDocument.wptmodel.index(self.ui.wptView.currentIndex().data(gpx.IDRole), gpx.LON).data(gpx.ValueRole))
    webbrowser.open('https://maps.google.com/maps?ll=' + lat + ',' + lon + '&t=h&q=' + lat + ',' + lon + '&z=15')

  @pyqtSlot()
  def showYandexMap(self):
    lat = str(TheDocument.wptmodel.index(self.ui.wptView.currentIndex().data(gpx.IDRole), gpx.LAT).data(gpx.ValueRole))
    lon = str(TheDocument.wptmodel.index(self.ui.wptView.currentIndex().data(gpx.IDRole), gpx.LON).data(gpx.ValueRole))
    webbrowser.open('https://maps.yandex.ru?ll=' + lon + ',' + lat + '&spn=0.03,0.03&pt=' + lon + ',' + lat + '&l=sat')

  @pyqtSlot()
  def showNakarteMap(self):
    lat = str(TheDocument.wptmodel.index(self.ui.wptView.currentIndex().data(gpx.IDRole), gpx.LAT).data(gpx.ValueRole))
    lon = str(TheDocument.wptmodel.index(self.ui.wptView.currentIndex().data(gpx.IDRole), gpx.LON).data(gpx.ValueRole))
    name = TheDocument.wptmodel.index(self.ui.wptView.currentIndex().data(gpx.IDRole), gpx.NAME).data()
    webbrowser.open('https://nakarte.me/#m=15/' + lat + '/' + lon + '&l=Otm&r=' + lat + '/' + lon + '/' + name)

  @pyqtSlot()
  def pointStyle(self):
    dlg = PointConfigDialog(self, self.ui.wptView.currentIndex().data(gpx.IDRole),
                            [i.data(gpx.IDRole) for i in self.ui.wptView.selectionModel().selectedRows()])
    dlg.exec()

  @pyqtSlot()
  def skipTracks(self):
    included = self.ui.trkView.currentIndex().data(gpx.IncludeRole)
    TheDocument.trkmodel.setIncludeStates([i.row() for i in self.ui.trkView.selectedIndexes() if i.column() == gpx.TRKNAME], not included)
    self.setProjectChanged()

  @pyqtSlot()
  def onFileNew(self):
    if not self.closeChangedProject(self.tr('New GPX Viewer project')):
      return

    self.reset()

  @pyqtSlot()
  def onFileLoadFile(self):
    filenames = QFileDialog.getOpenFileNames(self, self.tr('Open file'), TheConfig['MainWindow']['LoadGPXDirectory'],
                                             self.tr('All supported files (*.gpx *.GPX *.kml *.KML);;'
                                                     'GPX XML (*.gpx *.GPX);;'
                                                     'Keyhole Markup Language (*.kml *.KML);;'
                                                     'All files (*)'))[0]
    self.openGPXFiles(filenames)

  @pyqtSlot()
  def onFileSaveFileAs(self):
    if TheDocument.wptmodel.rowCount() == len(TheDocument.wptmodel.getSkippedPoints()) and \
       TheDocument.trkmodel.rowCount() == len(TheDocument.trkmodel.getSkippedTracks()):
      QMessageBox.warning(self, self.tr('Save error'), self.tr('The file will be empty.'))
      return

    filename, filter = QFileDialog.getSaveFileName(self, self.tr('Save file as'), TheConfig['MainWindow']['LoadGPXDirectory'],
                                                   self.tr('GPX XML (*.gpx *.GPX);;'
                                                           'Keyhole Markup Language (*.kml *.KML);;'
                                                           'All files (*)'),
                                                   TheConfig['MainWindow']['GPSFileExtension'])
    if filename != '':
      try:
        if filter.find('kml') != -1 or filename.lower().endswith('.kml'):
          TheDocument.gpxparser.writeKMLFile(filename)
        else:
          TheDocument.gpxparser.writeGPXFile(filename)
        TheConfig['MainWindow']['LoadGPXDirectory'] = QFileInfo(filename).path()
        TheConfig['MainWindow']['GPSFileExtension'] = filter
        self.ui.statusBar.showMessage(filename + self.tr(' written.'), 2000)
      except OSError as e:
        QMessageBox.warning(self, self.tr('Save error'), e.args[0])

  @pyqtSlot()
  def onFileOpen(self):
    if not self.closeChangedProject(self.tr('Open GPX Viewer project')):
      return

    filename = QFileDialog.getOpenFileName(self, self.tr('Open project file'), TheConfig['MainWindow']['ProjectDirectory'],
                                           self.tr('All GPX Viewer files (*.gpxv *.gpxz *.GPXV *.GPXZ);;'
                                                   'GPX Viewer projects (*.gpxv *.GPXV);;'
                                                   'GPX Viewer archives (*.gpxz *.GPXZ);;'
                                                   'All files (*)'))[0]
    if filename != '':
      self.openGPXProject(filename)

  @pyqtSlot()
  def onFileSave(self):
    if not self.projectSaved:
      return self.onFileSaveAs()
    else:
      try:
        TheDocument.saveFile(self.projectFile)
      except OSError as e:
        QMessageBox.warning(self, self.tr('Save error'), e.args[0])
        return False
    self.setProjectChanged(False)
    self.ui.statusBar.showMessage(self.projectFile + self.tr(' saved.'), 2000)
    return True

  @pyqtSlot()
  def onFileSaveAs(self):
    if len(TheDocument.doc['GPXFile']) != 0:
      filename, filter = QFileDialog.getSaveFileName(self, self.tr('Save project file as'), TheConfig['MainWindow']['ProjectDirectory'],
                                                     self.tr('GPX Viewer projects (*.gpxv *.GPXV);;'
                                                             'GPX Viewer archives (*.gpxz *.GPXZ);;'
                                                             'All files (*)'),
                                                     TheConfig['MainWindow']['ProjectExtension'])
      if filename != '':
        TheDocument.projectType = TYPE_GPXZ if (filter.find('gpxz') != -1 or filename.lower().endswith('.gpxz')) else TYPE_GPXV
        try:
          TheDocument.saveFile(filename)
          self.projectFile = filename
          self.projectSaved = True
          TheConfig['MainWindow']['ProjectDirectory'] = QFileInfo(self.projectFile).path()
          TheConfig['MainWindow']['ProjectExtension'] = filter
          self.setProjectChanged(False)
          self.updateTitleFilename(self.projectFile)
          self.addRecentProject(self.projectFile)
          self.ui.statusBar.showMessage(self.projectFile + self.tr(' saved.'), 2000)
          return True
        except OSError as e:
          QMessageBox.warning(self, self.tr('Save error'), e.args[0])
          return False
      else:
        return False
    else:
      QMessageBox.warning(self, self.tr('Save error'), self.tr('The project is empty.'))
      return False

  def openGPXFiles(self, filenames):
    if len(filenames) == 0:
      return

    for f in filenames:
      self.openGPXFile(f)
    TheDocument.gpxparser.updatePoints()
    self.updateTabs()
    message = (filenames[0] if len(filenames) == 1 else self.tr('Multiple GPX files')) + self.tr(' loaded.', '', len(filenames))
    self.ui.statusBar.showMessage(message, 2000)

  def openGPXFile(self, filename):
    TheConfig['MainWindow']['LoadGPXDirectory'] = QFileInfo(filename).path()
    try:
      TheDocument.gpxparser.parse(filename)
      TheDocument.doc['GPXFile'] += [filename]
      self.setProjectChanged()
      if not self.projectSaved:
        if len(TheDocument.doc['GPXFile']) > 1:
          self.updateTitleFilename('[ ' + self.tr('Multiple GPX files') + ' ]')
        else:
          self.updateTitleFilename(filename)
    except gpx.GpxWarning as e:
      QMessageBox.warning(self, self.tr('File read error'), e.args[0])

  def openGPXProject(self, filename):
    try:
      TheDocument.openFile(filename)
      self.projectFile = filename
      self.projectSaved = True
      TheConfig['MainWindow']['ProjectDirectory'] = QFileInfo(self.projectFile).path()
      self.filterModel.invalidateFilter()
      self.ui.wptView.resizeColumnsToContents()
      self.ui.trkView.resizeColumnsToContents()
      self.setProjectChanged(False)
      self.updateTitleFilename(self.projectFile)
      self.updateTabs()
      self.addRecentProject(self.projectFile)
      self.ui.statusBar.showMessage(self.projectFile + self.tr(' opened.'), 2000)
    except gpx.GpxWarning as e:
      self.reset()
      QMessageBox.warning(self, self.tr('File read error'), e.args[0])

  @pyqtSlot(str)
  def openedFileNotFound(self, file):
    result = QMessageBox.warning(self, self.tr('File read error'),
                                 self.tr('The file ') + file + self.tr(' doesn\'t exist.\n\nDo you want to choose another location of this file?'),
                                 QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.YesToAll | QMessageBox.StandardButton.No, QMessageBox.StandardButton.Yes)
    if result in (QMessageBox.StandardButton.Yes, QMessageBox.StandardButton.YesToAll):
      filename = QFileDialog.getOpenFileName(self, self.tr('Open GPX file') + ' ' + QFileInfo(file).fileName(), TheConfig['MainWindow']['LoadGPXDirectory'],
                                             self.tr('GPX XML (*.gpx *.GPX);;All files (*)'))[0]
      if filename != '':
        TheConfig['MainWindow']['LoadGPXDirectory'] = QFileInfo(filename).path()
        TheDocument.newFilePath = filename
        if result == QMessageBox.StandardButton.YesToAll:
          TheDocument.applyToAll = True

  @pyqtSlot(list)
  def askedExtractFiles(self, files):
    result = QMessageBox.warning(self, self.tr('Extract files?'), self.tr('This project refers to files that could be missing from the filesystem:\n')
                                                                  + '\n'.join(files)
                                                                  + self.tr('\n\nDo you want to write these files along with the saved project?\n'
                                                                            'NOTE: Some files can be overwritten.'),
                                 QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.Yes)
    if result == QMessageBox.StandardButton.Yes:
      TheDocument.doExtractFiles = True

  @pyqtSlot()
  def openRecentProject(self):
    if not self.closeChangedProject(self.tr('Open GPX Viewer project')):
      return

    for i, act in enumerate(self.actionsRecent):
      if self.sender() == act:
        filename = TheConfig.recentProjects[i]
        if QFileInfo(filename).exists():
          self.openGPXProject(filename)
        else:
          result = QMessageBox.information(self, self.tr('File read error'),
                                           self.tr('The file ') + filename + self.tr(' doesn\'t exist.\n\nDo you want to remove it from recent projects?'),
                                           QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
          if result == QMessageBox.StandardButton.Yes:
            del TheConfig.recentProjects[i]
            self.updateRecentProjects()

  @pyqtSlot()
  def onEditCopy(self):
    if self.ui.tabWidget.currentWidget() == self.ui.wptTab:
      TheDocument.wptmodel.copyToClipboard([i.data(gpx.IDRole) for i in self.ui.wptView.selectionModel().selectedRows()])
    else:
      TheDocument.trkmodel.copyToClipboard([i.row() for i in self.ui.trkView.selectionModel().selectedRows()])

  @pyqtSlot()
  def onResetColumns(self):
    TheConfig.columnsToCopy = list(gpx.WPTFIELDS)
    self.updateColumnsToCopy()

  @pyqtSlot()
  def onPlotDistanceProfile(self):
    if TheDocument.wptmodel.rowCount() - len(TheDocument.wptmodel.getSkippedPoints()) < 2 and \
       TheDocument.trkmodel.rowCount() == len(TheDocument.trkmodel.getSkippedTracks()):
      QMessageBox.warning(self, self.tr('Plot error'), self.tr('Not enouph points or tracks.'))
      return

    self.plotWindow.setWindowTitle(self.tr('Distance Profile'))
    self.plotWindow.show()
    if TheConfig.getValue('ProfileStyle', 'SelectedPointsOnly'):
      self.plotWindow.plotProfile(gpx.DIST,
                                  [i.data(gpx.IDRole) for i in self.ui.wptView.selectionModel().selectedRows()],
                                  [i.row() for i in self.ui.trkView.selectionModel().selectedRows()])
    else:
      self.plotWindow.plotProfile(gpx.DIST)
    self.plotWindow.activateWindow()

  @pyqtSlot()
  def onPlotTimeProfile(self):
    # Check if there are at least two points with timestamps
    n = 0
    for i in range(TheDocument.wptmodel.rowCount()):
      if TheDocument.wptmodel.index(i, 0).data(gpx.IncludeRole) and TheDocument.wptmodel.index(i, gpx.TIME).data() != '':
        n += 1
      if n == 2:
        break
    if n < 2:
      for j in range(TheDocument.trkmodel.rowCount()):
        if TheDocument.trkmodel.index(j, 0).data(gpx.IncludeRole) and TheDocument.trkmodel.index(j, gpx.TRKTIME).data() != '':
          n = 2
          break
      if n < 2:
        QMessageBox.warning(self, self.tr('Plot error'), self.tr('Not enouph points or tracks.'))
        return

    self.plotWindow.setWindowTitle(self.tr('Time Profile'))
    self.plotWindow.show()
    column = gpx.TIME if TheConfig.getValue('ProfileStyle', 'AbsoluteTime') else gpx.TIME_DAYS
    if TheConfig.getValue('ProfileStyle', 'SelectedPointsOnly'):
      self.plotWindow.plotProfile(column,
                                  [i.data(gpx.IDRole) for i in self.ui.wptView.selectionModel().selectedRows()],
                                  [i.row() for i in self.ui.trkView.selectionModel().selectedRows()])
    else:
      self.plotWindow.plotProfile(column)
    self.plotWindow.activateWindow()

  @pyqtSlot()
  def onShowStatistics(self):
    if TheDocument.wptmodel.rowCount() - len(TheDocument.wptmodel.getSkippedPoints()) < 2:
      QMessageBox.warning(self, self.tr('Statistics error'), self.tr('Not enouph points.'))
      return

    self.statWindow.show()
    self.statWindow.activateWindow()

  @pyqtSlot(bool)
  def onDetailedView(self, enable):
    TheConfig['MainWindow']['DetailedView'] = str(enable)
    self.filterModel.invalidateFilter()
    self.initColumnsToCopy()

  @pyqtSlot(bool)
  def onShowSkipped(self, show):
    TheConfig['MainWindow']['ShowSkipped'] = str(show)
    self.updateIncludeFilter()

  @pyqtSlot(bool)
  def onShowMarked(self, show):
    TheConfig['MainWindow']['ShowMarked'] = str(show)
    self.updateIncludeFilter()

  @pyqtSlot(bool)
  def onShowCaptioned(self, show):
    TheConfig['MainWindow']['ShowCaptioned'] = str(show)
    self.updateIncludeFilter()

  @pyqtSlot(bool)
  def onShowMarkedCaptioned(self, show):
    TheConfig['MainWindow']['ShowMarkedCaptioned'] = str(show)
    self.updateIncludeFilter()

  @pyqtSlot(bool)
  def onShowOther(self, show):
    TheConfig['MainWindow']['ShowDefault'] = str(show)
    self.updateIncludeFilter()

  @pyqtSlot()
  def onResetFilters(self):
    self.ui.actionShowSkipped.setChecked(True)
    self.ui.actionShowMarked.setChecked(True)
    self.ui.actionShowCaptioned.setChecked(True)
    self.ui.actionShowMarkedCaptioned.setChecked(True)
    self.ui.actionShowOther.setChecked(True)

  @pyqtSlot()
  def onShowSettings(self):
    dlg = SettingsDialog(self)
    if dlg.exec() == QDialog.DialogCode.Accepted and (TheDocument.wptmodel.rowCount() != 0 or TheDocument.trkmodel.rowCount() != 0):
      self.setProjectChanged()
      TheDocument.gpxparser.updateDistance()
      self.ui.wptView.resizeColumnsToContents()

  @pyqtSlot(str, str)
  def showWarning(self, title, text):
    QMessageBox.warning(self, title, text)

  def closeChangedProject(self, title):
    if self.projectChanged and len(TheDocument.doc['GPXFile']) != 0:
      result = QMessageBox.information(self, title,
                                       self.tr('There are unsaved changes. Do you want to save the project?'),
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel, QMessageBox.StandardButton.Yes)
      if result == QMessageBox.StandardButton.Yes:
        if not self.onFileSave():
          return False
      if result == QMessageBox.StandardButton.Cancel:
        return False

    return True

  def reset(self):
    self.projectFile = ''
    self.projectSaved = False
    self.setProjectChanged(False)
    TheDocument.doc['GPXFile'] = []
    TheDocument.gpxparser.resetModels()
    self.setWindowTitle(QCoreApplication.applicationName())
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
      self.setWindowTitle(self.titleFilename + ('*' if self.projectChanged else '') + ' — ' + QCoreApplication.applicationName())

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
    self.onTabChanged(self.ui.tabWidget.currentIndex())

  @pyqtSlot(int)
  def onTabChanged(self, index):
    self.actSkipPoints.setEnabled(index == 0)
    self.actSkipTracks.setEnabled(index == 1)

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
      act = QAction(QFileInfo(p).fileName() + ' [' + p + ']', self)
      act.triggered.connect(self.openRecentProject)
      self.actionsRecent += [act]
    self.ui.menuRecentProjects.insertActions(self.ui.actionClearList, self.actionsRecent)
    if len(TheConfig.recentProjects) > 0:
      self.ui.menuRecentProjects.insertSeparator(self.ui.actionClearList)
      self.ui.actionClearList.setEnabled(True)
    else:
      self.ui.actionClearList.setDisabled(True)

  @pyqtSlot()
  def onClearRecentList(self):
    for act in self.actionsRecent:
      self.ui.menuRecentProjects.removeAction(act)
    self.actionsRecent = []
    TheConfig.recentProjects = []
    self.ui.actionClearList.setDisabled(True)

  def initColumnsToCopy(self):
    if TheConfig.getboolean('MainWindow', 'DetailedView'):
      TheConfig.columnsToCopy += list(range(gpx.TIME_DAYS, len(gpx.WPTFIELDS)))
    else:
      TheConfig.columnsToCopy = [c for c in TheConfig.columnsToCopy if c < gpx.TIME_DAYS]

    for act in self.actionsColumns:
      self.ui.menuCoLumns.removeAction(act)
    self.actionsColumns = []

    for f in TheDocument.wptmodel.fields[:self.filterModel.columnCount()]:
      act = QAction(f, self)
      act.setCheckable(True)
      act.triggered[bool].connect(self.columnsToCopyChanged)
      self.actionsColumns += [act]
    self.ui.menuCoLumns.insertActions(self.ui.actionResetColumns, self.actionsColumns)
    self.ui.menuCoLumns.insertSeparator(self.ui.actionResetColumns)
    self.updateColumnsToCopy()

  def updateColumnsToCopy(self):
    for i, act in enumerate(self.actionsColumns):
      act.setChecked(i in TheConfig.columnsToCopy)

  @pyqtSlot(bool)
  def columnsToCopyChanged(self, checked):
    for i, act in enumerate(self.actionsColumns):
      if self.sender() == act:
        if checked:
          TheConfig.columnsToCopy += [i]
          TheConfig.columnsToCopy.sort()
        else:
          TheConfig.columnsToCopy.remove(i)
