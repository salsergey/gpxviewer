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

from PyQt5.QtWidgets import QDialog
from gpxviewer.configstore import TheConfig
import gpxviewer.ui_pointconfigdialog
import gpxviewer.gpxmodel as gpx


class PointConfigDialog(QDialog):
  def __init__(self, parent, style):
    super(PointConfigDialog, self).__init__(parent)
    self.ui = gpxviewer.ui_pointconfigdialog.Ui_pointConfigDialog()
    self.ui.setupUi(self)
    self.setMinimumWidth(350)
    self.style = style

    self.ui.markerColorCheckBox.setChecked(TheConfig['PointStyle'].getboolean('MarkerColorEnabled'))
    self.ui.markerStyleCheckBox.setChecked(TheConfig['PointStyle'].getboolean('MarkerStyleEnabled'))
    self.ui.markerSizeCheckBox.setChecked(TheConfig['PointStyle'].getboolean('MarkerSizeEnabled'))
    self.ui.lineColorCheckBox.setChecked(TheConfig['PointStyle'].getboolean('SplitLineColorEnabled'))
    self.ui.lineStyleCheckBox.setChecked(TheConfig['PointStyle'].getboolean('SplitLineStyleEnabled'))
    self.ui.lineWidthCheckBox.setChecked(TheConfig['PointStyle'].getboolean('SplitLineWidthEnabled'))
    self.ui.captionPositionCheckBox.setChecked(TheConfig['PointStyle'].getboolean('CaptionPositionEnabled'))
    self.ui.captionSizeCheckBox.setChecked(TheConfig['PointStyle'].getboolean('CaptionSizeEnabled'))

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

    self.ui.markerColorButton.setColor(self.style[gpx.MARKER_COLOR])
    self.ui.lineColorButton.setColor(self.style[gpx.LINE_COLOR])

    self.ui.markerStyleCombo.addItems([m[1] for m in self.markerStyles])
    for i,m in enumerate(self.markerStyles):
      if m[0] == self.style[gpx.MARKER_STYLE]:
        self.ui.markerStyleCombo.setCurrentIndex(i)
    self.ui.lineStyleCombo.addItems([m[1] for m in self.lineStyles])
    for i,m in enumerate(self.lineStyles):
      if m[0] == self.style[gpx.LINE_STYLE]:
        self.ui.lineStyleCombo.setCurrentIndex(i)

    self.ui.markerSizeSpinBox.setValue(self.style[gpx.MARKER_SIZE])
    self.ui.lineWidthSpinBox.setValue(self.style[gpx.LINE_WIDTH])

    self.ui.captionPositionXSpinBox.setValue(self.style[gpx.CAPTION_POSX])
    self.ui.captionPositionYSpinBox.setValue(self.style[gpx.CAPTION_POSY])
    self.ui.captionSizeSpinBox.setValue(self.style[gpx.CAPTION_SIZE])

    self.ui.markerColorCheckBox.toggled.connect(self.markerColorEnabled)
    self.ui.markerStyleCheckBox.toggled.connect(self.markerStyleEnabled)
    self.ui.markerSizeCheckBox.toggled.connect(self.markerSizeEnabled)
    self.ui.lineColorCheckBox.toggled.connect(self.lineColorEnabled)
    self.ui.lineStyleCheckBox.toggled.connect(self.lineStyleEnabled)
    self.ui.lineWidthCheckBox.toggled.connect(self.lineWidthEnabled)
    self.ui.captionPositionCheckBox.toggled.connect(self.captionPositionEnabled)
    self.ui.captionSizeCheckBox.toggled.connect(self.captionSizeEnabled)

    self.ui.markerColorButton.colorSet.connect(self.setMarkerColor)
    self.ui.markerStyleCombo.activated.connect(self.setMarkerStyle)
    self.ui.markerSizeSpinBox.valueChanged.connect(self.setMarkerSize)
    self.ui.lineColorButton.colorSet.connect(self.setLineColor)
    self.ui.lineStyleCombo.activated.connect(self.setLineStyle)
    self.ui.lineWidthSpinBox.valueChanged.connect(self.setLineWidth)
    self.ui.captionPositionXSpinBox.valueChanged.connect(self.setCaptionPositionX)
    self.ui.captionPositionYSpinBox.valueChanged.connect(self.setCaptionPositionY)
    self.ui.captionSizeSpinBox.valueChanged.connect(self.setCaptionSize)
    # TODO: tooltips

  def markerColorEnabled(self, enabled):
    TheConfig['PointStyle']['MarkerColorEnabled'] = str(enabled)

  def markerStyleEnabled(self, enabled):
    TheConfig['PointStyle']['MarkerStyleEnabled'] = str(enabled)

  def markerSizeEnabled(self, enabled):
    TheConfig['PointStyle']['MarkerSizeEnabled'] = str(enabled)

  def lineColorEnabled(self, enabled):
    TheConfig['PointStyle']['SplitLineColorEnabled'] = str(enabled)

  def lineStyleEnabled(self, enabled):
    TheConfig['PointStyle']['SplitLineStyleEnabled'] = str(enabled)

  def lineWidthEnabled(self, enabled):
    TheConfig['PointStyle']['SplitLineWidthEnabled'] = str(enabled)

  def captionPositionEnabled(self, enabled):
    TheConfig['PointStyle']['CaptionPositionEnabled'] = str(enabled)

  def captionSizeEnabled(self, enabled):
    TheConfig['PointStyle']['CaptionSizeEnabled'] = str(enabled)

  def setMarkerColor(self):
    self.style[gpx.MARKER_COLOR] = self.ui.markerColorButton.color.rgba()

  def setMarkerStyle(self):
    self.style[gpx.MARKER_STYLE] = self.markerStyles[self.ui.markerStyleCombo.currentIndex()][0]

  def setMarkerSize(self):
    self.style[gpx.MARKER_SIZE] = self.ui.markerSizeSpinBox.value()

  def setLineColor(self):
    self.style[gpx.LINE_COLOR] = self.ui.lineColorButton.color.rgba()

  def setLineStyle(self):
    self.style[gpx.LINE_STYLE] = self.lineStyles[self.ui.lineStyleCombo.currentIndex()][0]

  def setLineWidth(self):
    self.style[gpx.LINE_WIDTH] = round(self.ui.lineWidthSpinBox.value(), 1)

  def setCaptionPositionX(self):
    self.style[gpx.CAPTION_POSX] = self.ui.captionPositionXSpinBox.value()

  def setCaptionPositionY(self):
    self.style[gpx.CAPTION_POSY] = self.ui.captionPositionYSpinBox.value()

  def setCaptionSize(self):
    self.style[gpx.CAPTION_SIZE] = self.ui.captionSizeSpinBox.value()
