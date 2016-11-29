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
from os import path
from PyQt5 import QtCore, QtWidgets, QtGui
import gpxviewer.plotviewer as plt
import gpxviewer.gpxmodel as gpx
from gpxviewer.configstore import TheConfig
from gpxviewer.gpxdocument import TheDocument
import gpxviewer.ui_mainwindow
import gpxviewer.profileconfigdialog
import gpxviewer.pointconfigdialog


class GpxMainWindow(QtWidgets.QMainWindow):
  def __init__(self):
    super(GpxMainWindow, self).__init__()
    self.ui = gpxviewer.ui_mainwindow.Ui_MainWindow()
    self.ui.setupUi(self)
    self.ui.gpxView.setFocus()

    self.setWindowIcon(QtGui.QIcon(':/icons/gpxviewer.svg'))
    self.ui.actionLoadGPXfile.setIcon(QtGui.QIcon.fromTheme('text-xml', QtGui.QIcon(':/icons/text-xml.svg')))
    self.ui.actionOpen.setIcon(QtGui.QIcon.fromTheme('document-open', QtGui.QIcon(':/icons/document-open.svg')))
    self.ui.actionSave.setIcon(QtGui.QIcon.fromTheme('document-save', QtGui.QIcon(':/icons/document-save.svg')))
    self.ui.actionSaveAs.setIcon(QtGui.QIcon.fromTheme('document-save-as', QtGui.QIcon(':/icons/document-save-as.svg')))
    self.ui.actionQuit.setIcon(QtGui.QIcon.fromTheme('application-exit', QtGui.QIcon(':/icons/application-exit.svg')))
    self.ui.actionProfileStyle.setIcon(QtGui.QIcon.fromTheme('configure', QtGui.QIcon(':/icons/configure.svg')))
    self.ui.actionDistanceProfile.setIcon(QtGui.QIcon(':/icons/distanceprofile.svg'))
    self.ui.actionTimeProfile.setIcon(QtGui.QIcon(':/icons/timeprofile.svg'))
    self.ui.actionAboutGPXViewer.setIcon(QtGui.QIcon(':/icons/gpxviewer.svg'))

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
    self.ui.secondaryToolBar.addWidget(wdg)

    self.includefiltermodel = QtCore.QSortFilterProxyModel(self)
    self.includefiltermodel.setSourceModel(TheDocument.gpxmodel)
    self.includefiltermodel.setFilterKeyColumn(gpx.NAME)
    self.includefiltermodel.setFilterRole(gpx.IncludeRole)
    self.updateIncludeFilter()

    self.namefiltermodel = gpx.GpxSortFilterModel(self)
    self.namefiltermodel.setSourceModel(self.includefiltermodel)
    self.ui.gpxView.setModel(self.namefiltermodel)

    self.ui.gpxView.setSortingEnabled(True)
    self.ui.gpxView.sortByColumn(gpx.TIME, QtCore.Qt.AscendingOrder)
    self.namefiltermodel.setSortRole(gpx.ValueRole)
    self.namefiltermodel.setFilterKeyColumn(gpx.NAME)
    self.filterLineEdit.textChanged.connect(self.namefiltermodel.setFilterRegExp)

    self.ui.actionShowSkipped.setChecked(TheConfig['MainWindow'].getboolean('ShowSkipped'))
    self.ui.actionShowMarked.setChecked(TheConfig['MainWindow'].getboolean('ShowMarked'))
    self.ui.actionShowCaptioned.setChecked(TheConfig['MainWindow'].getboolean('ShowCaptioned'))
    self.ui.actionShowOther.setChecked(TheConfig['MainWindow'].getboolean('ShowDefault'))
    self.resize(TheConfig['MainWindow'].getint('WindowWidth'), TheConfig['MainWindow'].getint('WindowHeight'))

    # TODO: Do we need both?
    self.projectSaved = False
    self.projectChanged = False
    self.titleFilename = None
    self.plot = plt.PlotWindow()

  def updateTitleFilename(self, title = None):
    if title != None:
      self.titleFilename = title
    if self.titleFilename != None:
      self.setWindowTitle(self.titleFilename + ('*' if self.projectChanged else '') + ' — GPX Viewer')

  def setProjectChanged(self, value):
    self.projectChanged = value
    self.updateTitleFilename()

  def skipPoints(self):
    TheDocument.gpxmodel.setIncludeStates([i.data(gpx.IDRole) for i in self.ui.gpxView.selectionModel().selection().indexes() if i.column() == gpx.NAME], gpx.INC_SKIP)
    self.includefiltermodel.invalidateFilter()
    self.setProjectChanged(True)

  def markerPoints(self):
    TheDocument.gpxmodel.setIncludeStates([i.data(gpx.IDRole) for i in self.ui.gpxView.selectionModel().selection().indexes() if i.column() == gpx.NAME], gpx.INC_MARKER)
    self.includefiltermodel.invalidateFilter()
    self.setProjectChanged(True)

  def captionPoints(self):
    TheDocument.gpxmodel.setIncludeStates([i.data(gpx.IDRole) for i in self.ui.gpxView.selectionModel().selection().indexes() if i.column() == gpx.NAME], gpx.INC_CAPTION)
    self.includefiltermodel.invalidateFilter()
    self.setProjectChanged(True)

  def splitLines(self):
    TheDocument.gpxmodel.setSplitLines([i.data(gpx.IDRole) for i in self.ui.gpxView.selectionModel().selection().indexes() if i.column() == gpx.NAME], True)
    self.includefiltermodel.invalidateFilter()
    self.setProjectChanged(True)

  def neglectDistance(self):
    TheDocument.gpxmodel.setNeglectStates([i.data(gpx.IDRole) for i in self.ui.gpxView.selectionModel().selection().indexes() if i.column() == gpx.NAME], True)
    self.setProjectChanged(True)

  def resetPoints(self):
    indexes = [i.data(gpx.IDRole) for i in self.ui.gpxView.selectionModel().selection().indexes() if i.column() == gpx.NAME]
    TheDocument.gpxmodel.setIncludeStates(indexes, gpx.INC_DEFAULT)
    TheDocument.gpxmodel.setSplitLines(indexes, False)
    TheDocument.gpxmodel.setNeglectStates(indexes, False)
    self.includefiltermodel.invalidateFilter()
    self.setProjectChanged(True)

  def pointStyle(self):
    style = {}
    style.update(self.ui.gpxView.selectionModel().selection().indexes()[0].data(gpx.MarkerRole))
    style.update(self.ui.gpxView.selectionModel().selection().indexes()[0].data(gpx.SplitLineRole))
    style.update(self.ui.gpxView.selectionModel().selection().indexes()[0].data(gpx.CaptionRole))
    dlg = gpxviewer.pointconfigdialog.PointConfigDialog(self, style)
    if dlg.exec_() == QtWidgets.QDialog.Accepted:
      self.setProjectChanged(True)
      TheConfig['PointStyle']['MarkerColor'] = str(dlg.style[gpx.MARKER_COLOR])
      TheConfig['PointStyle']['MarkerStyle'] = dlg.style[gpx.MARKER_STYLE]
      TheConfig['PointStyle']['MarkerSize'] = str(dlg.style[gpx.MARKER_SIZE])
      TheConfig['PointStyle']['SplitLineColor'] = str(dlg.style[gpx.LINE_COLOR])
      TheConfig['PointStyle']['SplitLineStyle'] = dlg.style[gpx.LINE_STYLE]
      TheConfig['PointStyle']['SplitLineWidth'] = str(dlg.style[gpx.LINE_WIDTH])
      TheConfig['PointStyle']['CaptionPositionX'] = str(dlg.style[gpx.CAPTION_POSX])
      TheConfig['PointStyle']['CaptionPositionY'] = str(dlg.style[gpx.CAPTION_POSY])
      TheConfig['PointStyle']['CaptionSize'] = str(dlg.style[gpx.CAPTION_SIZE])

      if TheConfig['PointStyle'].getboolean('MarkerColorEnabled'):
        self.setPointStyle(gpx.MARKER_COLOR, dlg.style[gpx.MARKER_COLOR])
      if TheConfig['PointStyle'].getboolean('MarkerStyleEnabled'):
        self.setPointStyle(gpx.MARKER_STYLE, dlg.style[gpx.MARKER_STYLE])
      if TheConfig['PointStyle'].getboolean('MarkerSizeEnabled'):
        self.setPointStyle(gpx.MARKER_SIZE, dlg.style[gpx.MARKER_SIZE])

      if TheConfig['PointStyle'].getboolean('SplitLineColorEnabled'):
        self.setPointStyle(gpx.LINE_COLOR, dlg.style[gpx.LINE_COLOR])
      if TheConfig['PointStyle'].getboolean('SplitLineStyleEnabled'):
        self.setPointStyle(gpx.LINE_STYLE, dlg.style[gpx.LINE_STYLE])
      if TheConfig['PointStyle'].getboolean('SplitLineWidthEnabled'):
        self.setPointStyle(gpx.LINE_WIDTH, dlg.style[gpx.LINE_WIDTH])

      if TheConfig['PointStyle'].getboolean('CaptionPositionEnabled'):
        self.setPointStyle(gpx.CAPTION_POSX, dlg.style[gpx.CAPTION_POSX])
        self.setPointStyle(gpx.CAPTION_POSY, dlg.style[gpx.CAPTION_POSY])
      if TheConfig['PointStyle'].getboolean('CaptionSizeEnabled'):
        self.setPointStyle(gpx.CAPTION_SIZE, dlg.style[gpx.CAPTION_SIZE])

  def setPointStyle(self, key, value):
    TheDocument.gpxmodel.setPointStyle([i.data(gpx.IDRole) for i in self.ui.gpxView.selectionModel().selection().indexes() if i.column() == gpx.NAME], key, value)

  def resizeEvent(self, event):
    super(GpxMainWindow, self).resizeEvent(event)
    self.ui.gpxView.resizeColumnsToContents()
    TheConfig['MainWindow']['WindowWidth'] = str(event.size().width())
    TheConfig['MainWindow']['WindowHeight'] = str(event.size().height())

  def closeEvent(self, event):
    if self.projectChanged:
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
    TheConfig.save()
    super(GpxMainWindow, self).closeEvent(event)

  def keyPressEvent(self, event):
    if event.key() == QtCore.Qt.Key_F and event.modifiers() == QtCore.Qt.ControlModifier:
      self.filterLineEdit.setFocus()
      self.filterLineEdit.selectAll()
    if event.key() == QtCore.Qt.Key_C and event.modifiers() == QtCore.Qt.ControlModifier:
      TheDocument.gpxmodel.copyToClipboard([i.data(gpx.IDRole) for i in self.ui.gpxView.selectionModel().selection().indexes() if i.column() == gpx.NAME])
    if event.key() == QtCore.Qt.Key_Escape:
      self.ui.gpxView.setFocus()
    super(GpxMainWindow, self).keyPressEvent(event)

  def contextMenuEvent(self, event):
    if self.ui.gpxView.selectionModel().hasSelection():
      actSkip = QtWidgets.QAction(self.tr('Skip points'), self)
      actSkip.triggered.connect(self.skipPoints)
      actMarker = QtWidgets.QAction(self.tr('Points with markers'), self)
      actMarker.triggered.connect(self.markerPoints)
      actCaption = QtWidgets.QAction(self.tr('Points with captions and markers'), self)
      actCaption.triggered.connect(self.captionPoints)
      actSplit = QtWidgets.QAction(self.tr('Points with splitting lines'), self)
      actSplit.triggered.connect(self.splitLines)
      actNeglect = QtWidgets.QAction(self.tr('Neglect previous distance'), self)
      actNeglect.triggered.connect(self.neglectDistance)
      actReset = QtWidgets.QAction(self.tr('Reset'), self)
      actReset.triggered.connect(self.resetPoints)
      actStyle = QtWidgets.QAction(QtGui.QIcon.fromTheme('configure', QtGui.QIcon(':/icons/configure.svg')), self.tr('Point style'), self)
      actStyle.triggered.connect(self.pointStyle)

      menu = QtWidgets.QMenu(self)
      menu.addAction(actSkip)
      menu.addAction(actMarker)
      menu.addAction(actCaption)
      menu.addSeparator()
      menu.addAction(actSplit)
      menu.addAction(actNeglect)
      menu.addSeparator()
      menu.addAction(actReset)
      menu.addSeparator()
      menu.addAction(actStyle)
      menu.popup(event.globalPos())

  def loadGPXFile(self):
    if self.projectChanged:
      result = QtWidgets.QMessageBox.information(self, self.tr('Load GPX file'),
                                                 self.tr('There are unsaved changes. Do you want to save the project?'),
                                                 QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel,
                                                 QtWidgets.QMessageBox.Yes)
      if result == QtWidgets.QMessageBox.Yes:
        if not self.fileSave():
          return
      if result == QtWidgets.QMessageBox.Cancel:
        return

    filename = QtWidgets.QFileDialog.getOpenFileName(self, self.tr('Open GPX file'), TheConfig['MainWindow']['LoadGPXDirectory'],
                                                     self.tr('GPX XML (*.gpx);;All files (*)'))[0]
    if filename != '':
      self.openGPXFile(filename)

  def openGPXFile(self, filename):
    TheConfig['MainWindow']['LoadGPXDirectory'] = path.dirname(filename)
    TheDocument['GPXFile'] = filename
    self.projectSaved = False
    try:
      TheDocument.gpxmodel.parse(filename)
      self.ui.gpxView.resizeColumnsToContents()
      self.setProjectChanged(False)
      self.updateTitleFilename(filename)
    except gpx.GpxWarning as e:
      QtWidgets.QMessageBox.warning(self, self.tr('File read error'), e.args[0])

  def fileOpen(self):
    if self.projectChanged:
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

  def openGPXProject(self, filename):
    self.projectFile = filename
    self.projectSaved = True
    try:
      TheDocument.openFile(filename)
      self.includefiltermodel.invalidateFilter()
      self.ui.gpxView.resizeColumnsToContents()
      self.setProjectChanged(False)
      self.updateTitleFilename(self.projectFile)
      TheConfig['MainWindow']['ProjectDirectory'] = path.dirname(self.projectFile)
    except gpx.GpxWarning as e:
      QtWidgets.QMessageBox.warning(self, self.tr('File read error'), e.args[0])

  def fileSave(self):
    if not self.projectSaved:
      return self.fileSaveAs()
    else:
      TheDocument.saveFile(self.projectFile)
    self.setProjectChanged(False)
    self.updateTitleFilename()
    return True

  def fileSaveAs(self):
    if 'GPXFile' in TheDocument:
      filename = QtWidgets.QFileDialog.getSaveFileName(self, self.tr('Save project file as'), TheConfig['MainWindow']['ProjectDirectory'],
                                                       self.tr('GPX Viewer Projects (*.gpxv);;All files (*)'))[0]
      if filename != '':
        self.projectFile = filename
        self.projectSaved = True
        TheConfig['MainWindow']['ProjectDirectory'] = path.dirname(self.projectFile)
        TheDocument.saveFile(self.projectFile)
        self.setProjectChanged(False)
        self.updateTitleFilename(self.projectFile)
        return True

    return False

  def showSkipped(self, show):
    TheConfig['MainWindow']['ShowSkipped'] = str(show)
    self.updateIncludeFilter()

  def showMarked(self, show):
    TheConfig['MainWindow']['ShowMarked'] = str(show)
    self.updateIncludeFilter()

  def showCaptioned(self, show):
    TheConfig['MainWindow']['ShowCaptioned'] = str(show)
    self.updateIncludeFilter()

  def showOther(self, show):
    TheConfig['MainWindow']['ShowDefault'] = str(show)
    self.updateIncludeFilter()

  def updateIncludeFilter(self):
    mask = [TheConfig['MainWindow'].getboolean('ShowDefault'), TheConfig['MainWindow'].getboolean('ShowSkipped'),
            TheConfig['MainWindow'].getboolean('ShowMarked'), TheConfig['MainWindow'].getboolean('ShowCaptioned')]
    filter = [gpx.INCSTATES[i] for i,m in enumerate(mask) if m]
    self.includefiltermodel.setFilterRegExp('|'.join([str(f) for f in filter]))

  def showProfileStyleOptions(self):
    dlg = gpxviewer.profileconfigdialog.ProfileConfigDialog(self)
    if dlg.exec_() == QtWidgets.QDialog.Accepted:
      self.setProjectChanged(True)
      TheConfig['ProfileStyle']['ProfileColor'] = str(dlg.style['ProfileColor'])
      TheConfig['ProfileStyle']['FillColor'] = str(dlg.style['FillColor'])
      TheConfig['ProfileStyle']['ProfileWidth'] = str(dlg.style['ProfileWidth'])
      TheConfig['ProfileStyle']['MinimumAltitude'] = str(dlg.style['MinimumAltitude'])
      TheConfig['ProfileStyle']['MaximumAltitude'] = str(dlg.style['MaximumAltitude'])

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
                           Ctrl+T - Show time profile''')
    msg = QtWidgets.QMessageBox(self)
    msg.setWindowTitle(self.tr('GPX Viewer Help'))
    msg.setTextFormat(QtCore.Qt.RichText)
    msg.setText(aboutText)
    msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.exec_()

  def aboutQt(self):
    QtWidgets.QApplication.aboutQt()

  def aboutGPXViewer(self):
    aboutText = '<h3>GPX Viewer</h3><b>' + self.tr('Version') + ' ' + QtCore.QCoreApplication.applicationVersion() + '</b><br><br>' + \
                self.tr('Using') + ' Python ' + str(sys.version_info.major) + '.' + str(sys.version_info.minor) + '.' + str(sys.version_info.micro) + ', ' + \
                'PyQt5 ' + QtCore.PYQT_VERSION_STR + ', ' + \
                'Qt ' + QtCore.QT_VERSION_STR + '<br><br>' + \
                'Copyright 2016 Sergey Salnikov<br><br>' + \
                self.tr('License:') + ' <a href=http://www.gnu.org/licenses/gpl.html>GNU General Public License, version 3</a>'
    QtWidgets.QMessageBox.about(self, self.tr('About GPX Viewer'), aboutText)

  def plotDistanceProfile(self):
    if len(TheDocument.gpxmodel.getIndexesWithIncludeState(gpx.INC_SKIP)) < TheDocument.gpxmodel.rowCount():
      self.plot.setWindowTitle(self.tr('Distance Profile'))
      self.plot.plotProfile(gpx.DIST)
      self.plot.show()
      self.plot.activateWindow()

  def plotTimeProfile(self):
    if len(TheDocument.gpxmodel.getIndexesWithIncludeState(gpx.INC_SKIP)) < TheDocument.gpxmodel.rowCount():
      self.plot.setWindowTitle(self.tr('Time Profile'))
      self.plot.plotProfile(gpx.TIME_DAYS)
      self.plot.show()
      self.plot.activateWindow()
