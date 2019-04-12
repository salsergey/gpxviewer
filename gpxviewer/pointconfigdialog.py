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

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
import gpxviewer.gpxmodel as gpx
from gpxviewer.configstore import TheConfig
from gpxviewer.gpxdocument import TheDocument
import gpxviewer.ui_pointconfigdialog


class PointConfigDialog(QDialog):
  def __init__(self, parent, defaultIndex, indexes=None):
    super(PointConfigDialog, self).__init__(parent)
    self.ui = gpxviewer.ui_pointconfigdialog.Ui_pointConfigDialog()
    self.ui.setupUi(self)
    self.setMinimumWidth(420)
    self.style = {}
    self.style.update(TheDocument.wptmodel.index(defaultIndex, gpx.NAME).data(gpx.MarkerStyleRole))
    self.style.update(TheDocument.wptmodel.index(defaultIndex, gpx.NAME).data(gpx.CaptionStyleRole))
    self.style.update(TheDocument.wptmodel.index(defaultIndex, gpx.NAME).data(gpx.SplitLineStyleRole))
    self.indexes = indexes if indexes is not None else [defaultIndex]

    self.ui.markerColorCheckBox.setChecked(TheConfig.getValue('PointStyle', 'MarkerColorEnabled'))
    self.ui.markerStyleCheckBox.setChecked(TheConfig.getValue('PointStyle', 'MarkerStyleEnabled'))
    self.ui.markerSizeCheckBox.setChecked(TheConfig.getValue('PointStyle', 'MarkerSizeEnabled'))
    self.ui.lineColorCheckBox.setChecked(TheConfig.getValue('PointStyle', 'SplitLineColorEnabled'))
    self.ui.lineStyleCheckBox.setChecked(TheConfig.getValue('PointStyle', 'SplitLineStyleEnabled'))
    self.ui.lineWidthCheckBox.setChecked(TheConfig.getValue('PointStyle', 'SplitLineWidthEnabled'))
    self.ui.captionPositionCheckBox.setChecked(TheConfig.getValue('PointStyle', 'CaptionPositionEnabled'))
    self.ui.captionSizeCheckBox.setChecked(TheConfig.getValue('PointStyle', 'CaptionSizeEnabled'))

    self.markerStyles = [('.', self.tr('Point')),
                         (',', self.tr('Pixel')),
                         ('o', self.tr('Circle')),
                         ('v', self.tr('Triangle down')),
                         ('^', self.tr('Triangle up')),
                         ('<', self.tr('Triangle left')),
                         ('>', self.tr('Triangle right')),
                         ('1', self.tr('Tri down')),
                         ('2', self.tr('Tri up')),
                         ('3', self.tr('Tri left')),
                         ('4', self.tr('Tri right')),
                         ('s', self.tr('Square')),
                         ('p', self.tr('Pentagon')),
                         ('*', self.tr('Star')),
                         ('h', self.tr('Hexagon 1')),
                         ('H', self.tr('Hexagon 2')),
                         ('+', self.tr('Plus')),
                         ('x', self.tr('X')),
                         ('D', self.tr('Diamond')),
                         ('d', self.tr('Thin diamond')),
                         ('|', self.tr('Vertical line')),
                         ('_', self.tr('Horizontal line'))]
    self.lineStyles = [('-', self.tr('Solid')),
                       ('--', self.tr('Dashed')),
                       ('-.', self.tr('Dash-dot')),
                       (':', self.tr('Dotted'))]

    self.ui.markerStyleCombo.addItems([m[1] for m in self.markerStyles])
    for i, m in enumerate(self.markerStyles):
      if m[0] == self.style[gpx.MARKER_STYLE]:
        self.ui.markerStyleCombo.setCurrentIndex(i)
        break
    self.ui.markerColorButton.setColor(self.style[gpx.MARKER_COLOR])
    self.ui.markerSizeSpinBox.setValue(self.style[gpx.MARKER_SIZE])

    self.ui.captionPositionXSpinBox.setValue(self.style[gpx.CAPTION_POSX])
    self.ui.captionPositionYSpinBox.setValue(self.style[gpx.CAPTION_POSY])
    self.ui.captionSizeSpinBox.setValue(self.style[gpx.CAPTION_SIZE])

    self.ui.lineStyleCombo.addItems([m[1] for m in self.lineStyles])
    for i, m in enumerate(self.lineStyles):
      if m[0] == self.style[gpx.LINE_STYLE]:
        self.ui.lineStyleCombo.setCurrentIndex(i)
        break
    self.ui.lineColorButton.setColor(self.style[gpx.LINE_COLOR])
    self.ui.lineWidthSpinBox.setValue(self.style[gpx.LINE_WIDTH])

    self.ui.markerColorCheckBox.toggled[bool].connect(self.markerColorEnabled)
    self.ui.markerStyleCheckBox.toggled[bool].connect(self.markerStyleEnabled)
    self.ui.markerSizeCheckBox.toggled[bool].connect(self.markerSizeEnabled)
    self.ui.captionPositionCheckBox.toggled[bool].connect(self.captionPositionEnabled)
    self.ui.captionSizeCheckBox.toggled[bool].connect(self.captionSizeEnabled)
    self.ui.lineColorCheckBox.toggled[bool].connect(self.lineColorEnabled)
    self.ui.lineStyleCheckBox.toggled[bool].connect(self.lineStyleEnabled)
    self.ui.lineWidthCheckBox.toggled[bool].connect(self.lineWidthEnabled)

    self.ui.markerColorButton.colorSet.connect(self.setMarkerColor)
    self.ui.markerStyleCombo.activated.connect(self.setMarkerStyle)
    self.ui.markerSizeSpinBox.valueChanged.connect(self.setMarkerSize)
    self.ui.captionPositionXSpinBox.valueChanged.connect(self.setCaptionPositionX)
    self.ui.captionPositionYSpinBox.valueChanged.connect(self.setCaptionPositionY)
    self.ui.captionSizeSpinBox.valueChanged.connect(self.setCaptionSize)
    self.ui.lineColorButton.colorSet.connect(self.setLineColor)
    self.ui.lineStyleCombo.activated.connect(self.setLineStyle)
    self.ui.lineWidthSpinBox.valueChanged.connect(self.setLineWidth)

  def accept(self):
    super(PointConfigDialog, self).accept()

    TheConfig['PointStyle']['MarkerColor'] = str(self.style[gpx.MARKER_COLOR])
    TheConfig['PointStyle']['MarkerStyle'] = self.style[gpx.MARKER_STYLE]
    TheConfig['PointStyle']['MarkerSize'] = str(self.style[gpx.MARKER_SIZE])
    TheConfig['PointStyle']['CaptionPositionX'] = str(self.style[gpx.CAPTION_POSX])
    TheConfig['PointStyle']['CaptionPositionY'] = str(self.style[gpx.CAPTION_POSY])
    TheConfig['PointStyle']['CaptionSize'] = str(self.style[gpx.CAPTION_SIZE])
    TheConfig['PointStyle']['SplitLineColor'] = str(self.style[gpx.LINE_COLOR])
    TheConfig['PointStyle']['SplitLineStyle'] = self.style[gpx.LINE_STYLE]
    TheConfig['PointStyle']['SplitLineWidth'] = str(self.style[gpx.LINE_WIDTH])

    if TheConfig.getValue('PointStyle', 'MarkerColorEnabled'):
      TheDocument.wptmodel.setPointStyle(self.indexes, gpx.MARKER_COLOR, self.style[gpx.MARKER_COLOR])
    if TheConfig.getValue('PointStyle', 'MarkerStyleEnabled'):
      TheDocument.wptmodel.setPointStyle(self.indexes, gpx.MARKER_STYLE, self.style[gpx.MARKER_STYLE])
    if TheConfig.getValue('PointStyle', 'MarkerSizeEnabled'):
      TheDocument.wptmodel.setPointStyle(self.indexes, gpx.MARKER_SIZE, self.style[gpx.MARKER_SIZE])

    if TheConfig.getValue('PointStyle', 'CaptionPositionEnabled'):
      TheDocument.wptmodel.setPointStyle(self.indexes, gpx.CAPTION_POSX, self.style[gpx.CAPTION_POSX])
      TheDocument.wptmodel.setPointStyle(self.indexes, gpx.CAPTION_POSY, self.style[gpx.CAPTION_POSY])
    if TheConfig.getValue('PointStyle', 'CaptionSizeEnabled'):
      TheDocument.wptmodel.setPointStyle(self.indexes, gpx.CAPTION_SIZE, self.style[gpx.CAPTION_SIZE])

    if TheConfig.getValue('PointStyle', 'SplitLineColorEnabled'):
      TheDocument.wptmodel.setPointStyle(self.indexes, gpx.LINE_COLOR, self.style[gpx.LINE_COLOR])
    if TheConfig.getValue('PointStyle', 'SplitLineStyleEnabled'):
      TheDocument.wptmodel.setPointStyle(self.indexes, gpx.LINE_STYLE, self.style[gpx.LINE_STYLE])
    if TheConfig.getValue('PointStyle', 'SplitLineWidthEnabled'):
      TheDocument.wptmodel.setPointStyle(self.indexes, gpx.LINE_WIDTH, self.style[gpx.LINE_WIDTH])

  @pyqtSlot(bool)
  def markerColorEnabled(self, enabled):
    TheConfig['PointStyle']['MarkerColorEnabled'] = str(enabled)

  @pyqtSlot(bool)
  def markerStyleEnabled(self, enabled):
    TheConfig['PointStyle']['MarkerStyleEnabled'] = str(enabled)

  @pyqtSlot(bool)
  def markerSizeEnabled(self, enabled):
    TheConfig['PointStyle']['MarkerSizeEnabled'] = str(enabled)

  @pyqtSlot(bool)
  def captionPositionEnabled(self, enabled):
    TheConfig['PointStyle']['CaptionPositionEnabled'] = str(enabled)

  @pyqtSlot(bool)
  def captionSizeEnabled(self, enabled):
    TheConfig['PointStyle']['CaptionSizeEnabled'] = str(enabled)

  @pyqtSlot(bool)
  def lineColorEnabled(self, enabled):
    TheConfig['PointStyle']['SplitLineColorEnabled'] = str(enabled)

  @pyqtSlot(bool)
  def lineStyleEnabled(self, enabled):
    TheConfig['PointStyle']['SplitLineStyleEnabled'] = str(enabled)

  @pyqtSlot(bool)
  def lineWidthEnabled(self, enabled):
    TheConfig['PointStyle']['SplitLineWidthEnabled'] = str(enabled)

  @pyqtSlot()
  def setMarkerColor(self):
    self.style[gpx.MARKER_COLOR] = self.ui.markerColorButton.color.rgba()

  @pyqtSlot()
  def setMarkerStyle(self):
    self.style[gpx.MARKER_STYLE] = self.markerStyles[self.ui.markerStyleCombo.currentIndex()][0]

  @pyqtSlot()
  def setMarkerSize(self):
    self.style[gpx.MARKER_SIZE] = self.ui.markerSizeSpinBox.value()

  @pyqtSlot()
  def setLineColor(self):
    self.style[gpx.LINE_COLOR] = self.ui.lineColorButton.color.rgba()

  @pyqtSlot()
  def setLineStyle(self):
    self.style[gpx.LINE_STYLE] = self.lineStyles[self.ui.lineStyleCombo.currentIndex()][0]

  @pyqtSlot()
  def setLineWidth(self):
    self.style[gpx.LINE_WIDTH] = round(self.ui.lineWidthSpinBox.value(), self.ui.lineWidthSpinBox.decimals())

  @pyqtSlot()
  def setCaptionPositionX(self):
    self.style[gpx.CAPTION_POSX] = self.ui.captionPositionXSpinBox.value()

  @pyqtSlot()
  def setCaptionPositionY(self):
    self.style[gpx.CAPTION_POSY] = self.ui.captionPositionYSpinBox.value()

  @pyqtSlot()
  def setCaptionSize(self):
    self.style[gpx.CAPTION_SIZE] = self.ui.captionSizeSpinBox.value()
