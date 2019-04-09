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
from gpxviewer.configstore import TheConfig
import gpxviewer.ui_settingsdialog


class SettingsDialog(QDialog):
  def __init__(self, parent):
    super(SettingsDialog, self).__init__(parent)
    self.ui = gpxviewer.ui_settingsdialog.Ui_settingsDialog()
    self.ui.setupUi(self)
    self.setMinimumWidth(260)
    self.settings = {}
    self.settings['ProfileColor'] = TheConfig.getValue('ProfileStyle', 'ProfileColor')
    self.settings['FillColor'] = TheConfig.getValue('ProfileStyle', 'FillColor')
    self.settings['ProfileWidth'] = TheConfig.getValue('ProfileStyle', 'ProfileWidth')
    self.settings['MinimumAltitude'] = TheConfig.getValue('ProfileStyle', 'MinimumAltitude')
    self.settings['MaximumAltitude'] = TheConfig.getValue('ProfileStyle', 'MaximumAltitude')
    self.settings['DistanceCoefficient'] = TheConfig.getValue('ProfileStyle', 'DistanceCoefficient')
    self.settings['TimeZoneOffset'] = TheConfig.getValue('ProfileStyle', 'TimeZoneOffset')
    self.settings['SelectedPointsOnly'] = TheConfig.getValue('ProfileStyle', 'SelectedPointsOnly')
    self.settings['ReadNameFromTag'] = TheConfig.getValue('ProfileStyle', 'ReadNameFromTag')
    self.settings['CoordinateFormat'] = TheConfig.getValue('ProfileStyle', 'CoordinateFormat')

    self.ui.profileColorButton.setColor(self.settings['ProfileColor'])
    self.ui.fillColorButton.setColor(self.settings['FillColor'])
    self.ui.profileWidthSpinBox.setValue(self.settings['ProfileWidth'])
    self.ui.minaltSpinBox.setValue(self.settings['MinimumAltitude'])
    self.ui.maxaltSpinBox.setValue(self.settings['MaximumAltitude'])
    self.ui.distanceCoeffSpinBox.setValue(self.settings['DistanceCoefficient'])
    self.ui.timezoneSpinBox.setValue(self.settings['TimeZoneOffset'])
    self.ui.selectedPointsCheckBox.setChecked(self.settings['SelectedPointsOnly'])
    self.ui.nameTagBox.setCurrentIndex(self.settings['ReadNameFromTag'])
    self.ui.coordinateBox.setCurrentIndex(self.settings['CoordinateFormat'])

    self.ui.profileColorButton.colorSet.connect(self.setProfileColor)
    self.ui.fillColorButton.colorSet.connect(self.setFillColor)
    self.ui.profileWidthSpinBox.valueChanged.connect(self.setProfileWidth)
    self.ui.minaltSpinBox.valueChanged.connect(self.setMinimumAltitude)
    self.ui.maxaltSpinBox.valueChanged.connect(self.setMaximumAltitude)
    self.ui.distanceCoeffSpinBox.valueChanged.connect(self.setDistanceCoefficient)
    self.ui.timezoneSpinBox.valueChanged.connect(self.setTimeZoneOffset)
    self.ui.selectedPointsCheckBox.toggled.connect(self.setSelectedPointsOnly)
    self.ui.nameTagBox.currentIndexChanged.connect(self.setNameTag)
    self.ui.coordinateBox.currentIndexChanged.connect(self.setCoordinateFormat)

  @pyqtSlot()
  def setProfileColor(self):
    self.settings['ProfileColor'] = self.ui.profileColorButton.color.rgba()

  @pyqtSlot()
  def setFillColor(self):
    self.settings['FillColor'] = self.ui.fillColorButton.color.rgba()

  @pyqtSlot()
  def setProfileWidth(self):
    self.settings['ProfileWidth'] = round(self.ui.profileWidthSpinBox.value(), self.ui.profileWidthSpinBox.decimals())

  @pyqtSlot()
  def setMinimumAltitude(self):
    self.settings['MinimumAltitude'] = self.ui.minaltSpinBox.value()

  @pyqtSlot()
  def setMaximumAltitude(self):
    self.settings['MaximumAltitude'] = self.ui.maxaltSpinBox.value()

  @pyqtSlot()
  def setDistanceCoefficient(self):
    self.settings['DistanceCoefficient'] = round(self.ui.distanceCoeffSpinBox.value(), self.ui.distanceCoeffSpinBox.decimals())

  @pyqtSlot()
  def setTimeZoneOffset(self):
    self.settings['TimeZoneOffset'] = self.ui.timezoneSpinBox.value()

  @pyqtSlot()
  def setSelectedPointsOnly(self, enabled):
    self.settings['SelectedPointsOnly'] = enabled

  @pyqtSlot()
  def setNameTag(self):
    self.settings['ReadNameFromTag'] = self.ui.nameTagBox.currentIndex()

  @pyqtSlot()
  def setCoordinateFormat(self):
    self.settings['CoordinateFormat'] = self.ui.coordinateBox.currentIndex()
