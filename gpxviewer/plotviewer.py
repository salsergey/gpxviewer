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

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtCore import Qt, QFileInfo
from gpxviewer.configstore import TheConfig
import gpxviewer.ui_plotwindow


class PlotWindow(QtWidgets.QMainWindow):
  def __init__(self, parent=None):
    super(PlotWindow, self).__init__(parent)
    self.ui = gpxviewer.ui_plotwindow.Ui_PlotWindow()
    self.ui.setupUi(self)

    self.setWindowIcon(QIcon(':/icons/gpxviewer.svg'))
    self.ui.actExportCurrentSize.setIcon(QIcon.fromTheme('document-save', QIcon(':/icons/document-save.svg')))
    self.ui.actExportSelectedSize.setIcon(QIcon.fromTheme('document-save-as', QIcon(':/icons/document-save-as.svg')))

    self.ui.actExportCurrentSize.setShortcut(QKeySequence.Save)
    self.ui.actExportSelectedSize.setShortcut(QKeySequence.SaveAs)

    wdg = QtWidgets.QWidget()
    wdg.setLayout(QtWidgets.QHBoxLayout())
    wdg.layout().addItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding))
    wdg.layout().addWidget(QtWidgets.QLabel(self.tr('Set size for export:')))
    self.widthSpinBox = QtWidgets.QSpinBox()
    self.widthSpinBox.setMaximum(10000)
    self.widthSpinBox.setValue(int(TheConfig['PlotWindow']['SaveProfileWidth']))
    self.heightSpinBox = QtWidgets.QSpinBox()
    self.heightSpinBox.setMaximum(10000)
    self.heightSpinBox.setValue(int(TheConfig['PlotWindow']['SaveProfileHeight']))
    wdg.layout().addWidget(self.widthSpinBox)
    wdg.layout().addWidget(QtWidgets.QLabel('x'))
    wdg.layout().addWidget(self.heightSpinBox)
    self.ui.toolBar.addWidget(wdg)

    self.widthSpinBox.valueChanged.connect(self.setExportWidth)
    self.heightSpinBox.valueChanged.connect(self.setExportHeight)

    self.resize(TheConfig['PlotWindow'].getint('WindowWidth'), TheConfig['PlotWindow'].getint('WindowHeight'))

  def keyPressEvent(self, event):
    if event.key() == Qt.Key_Escape:
      self.hide()
    super(PlotWindow, self).keyPressEvent(event)

  def resizeEvent(self, event):
    super(PlotWindow, self).resizeEvent(event)
    TheConfig['PlotWindow']['WindowWidth'] = str(event.size().width())
    TheConfig['PlotWindow']['WindowHeight'] = str(event.size().height())

  def getExportFileName(self, dialogTitle):
    filename, filter = QtWidgets.QFileDialog.getSaveFileName(self, dialogTitle, TheConfig['PlotWindow']['SaveProfileDirectory'],
                                                             self.tr('Encapsulated Postscript (*.eps);;'
                                                                     'Portable Document Format (*.pdf);;'
                                                                     'PGF files (*.pgf);;'
                                                                     'PNG images (*.png);;'
                                                                     'Postscript files (*.ps);;'
                                                                     'SVG files (*.svg);;'
                                                                     'SVGZ files (*.svgz);;'
                                                                     'All files (*.*)'),
                                                             TheConfig['PlotWindow']['SaveFileExtension'])

    if filename != '':
      TheConfig['PlotWindow']['SaveProfileDirectory'] = QFileInfo(filename).path()
      TheConfig['PlotWindow']['SaveFileExtension'] = filter

    return filename

  def plotProfile(self, column, wptRows=[], trkRows=[]):
    self.ui.canvasWidget.plotProfile(column, wptRows, trkRows)
    self.ui.centralwidget.setFocus()

  def saveCurrentSize(self):
    filename = self.getExportFileName(self.tr('Export profile of the current size'))

    if filename != '':
      self.ui.canvasWidget.saveProfile(filename)

  def saveSelectedSize(self):
    filename = self.getExportFileName(self.tr('Export profile of the selected size'))

    if filename != '':
      self.ui.canvasWidget.saveProfile(filename, figsize=(self.widthSpinBox.value(), self.heightSpinBox.value()))

  def setExportWidth(self):
    TheConfig['PlotWindow']['SaveProfileWidth'] = str(self.widthSpinBox.value())

  def setExportHeight(self):
    TheConfig['PlotWindow']['SaveProfileHeight'] = str(self.heightSpinBox.value())
