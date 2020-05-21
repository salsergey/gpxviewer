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

from PyQt5.QtCore import Qt, QFileInfo, QFileSelector, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QFileDialog, QHBoxLayout, QLabel, QMainWindow, QSizePolicy, QSpacerItem, QSpinBox, QWidget
from gpxviewer.configstore import TheConfig
import gpxviewer.ui_plotwindow


class PlotWindow(QMainWindow):
  def __init__(self, parent=None):
    super(PlotWindow, self).__init__(parent)
    self.ui = gpxviewer.ui_plotwindow.Ui_PlotWindow()
    self.ui.setupUi(self)

    self.setWindowIcon(QIcon(':/icons/gpxviewer.svg'))
    self.themeSelector = QFileSelector()
    self.themeSelector.setExtraSelectors([TheConfig['MainWindow']['ColorTheme']])
    self.ui.actExportCurrentSize.setIcon(QIcon(self.themeSelector.select(':/icons/document-save.svg')))
    self.ui.actExportSelectedSize.setIcon(QIcon(self.themeSelector.select(':/icons/document-save-as.svg')))
    self.ui.actFitWidth.setIcon(QIcon(self.themeSelector.select(':/icons/zoom-fit-width.svg')))

    self.ui.actExportCurrentSize.setShortcut(QKeySequence.Save)
    self.ui.actExportSelectedSize.setShortcut(QKeySequence.SaveAs)

    wdg = QWidget()
    wdg.setLayout(QHBoxLayout())
    wdg.layout().addItem(QSpacerItem(40, 20, QSizePolicy.Expanding))
    wdg.layout().addWidget(QLabel(self.tr('Set size for export:')))
    self.widthSpinBox = QSpinBox()
    self.widthSpinBox.setMaximum(10000)
    self.widthSpinBox.setValue(int(TheConfig['PlotWindow']['SaveProfileWidth']))
    self.heightSpinBox = QSpinBox()
    self.heightSpinBox.setMaximum(10000)
    self.heightSpinBox.setValue(int(TheConfig['PlotWindow']['SaveProfileHeight']))
    wdg.layout().addWidget(self.widthSpinBox)
    wdg.layout().addWidget(QLabel('x'))
    wdg.layout().addWidget(self.heightSpinBox)
    self.ui.toolBar.addWidget(wdg)

    self.widthSpinBox.valueChanged.connect(self.setExportWidth)
    self.heightSpinBox.valueChanged.connect(self.setExportHeight)
    self.ui.canvasWidget.profileChanged.connect(self.profileChanged)

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
    filename, filter = QFileDialog.getSaveFileName(self, dialogTitle, TheConfig['PlotWindow']['SaveProfileDirectory'],
                                                   self.tr('BMP images (*.bmp *.BMP);;'
                                                           'JPEG images (*.jpg *.jpeg *.JPG *.JPEG);;'
                                                           'Portable Document Format (*.pdf *.PDF);;'
                                                           'PNG images (*.png *.PNG);;'
                                                           'TIFF images (*.tif *tiff *.TIF *.TIFF);;'
                                                           'All files (*)'),
                                                   TheConfig['PlotWindow']['SaveFileExtension'])

    if filename != '':
      TheConfig['PlotWindow']['SaveProfileDirectory'] = QFileInfo(filename).path()
      TheConfig['PlotWindow']['SaveFileExtension'] = filter

    return filename

  def plotProfile(self, column, wptRows=[], trkRows=[]):
    self.ui.canvasWidget.plotProfile(column, wptRows, trkRows)
    self.ui.centralwidget.setFocus()

  @pyqtSlot()
  def onSaveCurrentSize(self):
    filename = self.getExportFileName(self.tr('Export profile of the current size'))

    if filename != '':
      self.ui.canvasWidget.saveProfile(filename)

  @pyqtSlot()
  def onSaveSelectedSize(self):
    filename = self.getExportFileName(self.tr('Export profile of the selected size'))

    if filename != '':
      self.ui.canvasWidget.saveProfile(filename, figsize=(self.widthSpinBox.value(), self.heightSpinBox.value()))

  @pyqtSlot()
  def onFitWidth(self):
    self.ui.canvasWidget.onFitWidth()

  @pyqtSlot()
  def setExportWidth(self):
    TheConfig['PlotWindow']['SaveProfileWidth'] = str(self.widthSpinBox.value())

  @pyqtSlot()
  def setExportHeight(self):
    TheConfig['PlotWindow']['SaveProfileHeight'] = str(self.heightSpinBox.value())

  profileChanged = pyqtSignal()
