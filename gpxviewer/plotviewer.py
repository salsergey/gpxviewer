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

from os import path
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from gpxviewer.configstore import TheConfig
import gpxviewer.ui_plotwindow


class PlotWindow(QtWidgets.QMainWindow):
  def __init__(self, parent = None):
    super(PlotWindow, self).__init__(parent)
    self.ui = gpxviewer.ui_plotwindow.Ui_PlotWindow()
    self.ui.setupUi(self)

    self.ui.actExportCurrentSize.setIcon(QtGui.QIcon.fromTheme('document-save', QtGui.QIcon(':/icons/document-save.svg')))
    self.ui.actExportSelectedSize.setIcon(QtGui.QIcon.fromTheme('document-save-as', QtGui.QIcon(':/icons/document-save-as.svg')))

    self.ui.actExportCurrentSize.setShortcut(QtGui.QKeySequence.Save)
    self.ui.actExportSelectedSize.setShortcut(QtGui.QKeySequence.SaveAs)

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

  def resizeEvent(self, event):
    super(PlotWindow, self).resizeEvent(event)
    TheConfig['PlotWindow']['WindowWidth'] = str(event.size().width())
    TheConfig['PlotWindow']['WindowHeight'] = str(event.size().height())

  def plotProfile(self, column):
    self.ui.canvasWidget.plotProfile(column)

  def getExportFileName(self):
    filename, filter = QtWidgets.QFileDialog.getSaveFileName(self, 'Save profile as', TheConfig['PlotWindow']['SaveProfileDirectory'], 'EPS images (*.eps);;PDF images (*.pdf);;PGF images (*.pgf);;PNG images (*.png);;PS images (*.ps);;SVG images (*.svg);;SVGZ images (*.svgz);;All files (*.*)', TheConfig['PlotWindow']['SaveFileExtension'])

    if filename != '':
      TheConfig['PlotWindow']['SaveProfileDirectory'] = path.dirname(filename)
      TheConfig['PlotWindow']['SaveFileExtension'] = filter

    return filename

  def saveCurrentSize(self):
    filename = self.getExportFileName()

    if filename != '':
      self.ui.canvasWidget.saveProfile(filename)

  def saveSelectedSize(self):
    filename = self.getExportFileName()

    if filename != '':
      self.ui.canvasWidget.saveProfile(filename, figsize=(self.widthSpinBox.value(), self.heightSpinBox.value()))

  def setExportWidth(self):
    TheConfig['PlotWindow']['SaveProfileWidth'] = str(self.widthSpinBox.value())

  def setExportHeight(self):
    TheConfig['PlotWindow']['SaveProfileHeight'] = str(self.heightSpinBox.value())
