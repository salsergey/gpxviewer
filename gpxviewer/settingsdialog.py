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

import os
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
    if os.name == 'nt':
      self.ui.useSystemThemeLabel.hide()
      self.ui.useSystemThemeCheckBox.hide()

    self.settings = {}
    for option in TheConfig['ProfileStyle'].keys():
      self.settings[option] = TheConfig.getValue('ProfileStyle', option)

    self.ui.minaltSpinBox.setMaximum(self.settings['MaximumAltitude'] - 1)
    self.ui.maxaltSpinBox.setMinimum(self.settings['MinimumAltitude'] + 1)

    self.ui.profileColorButton.setColor(self.settings['ProfileColor'])
    self.ui.fillColorButton.setColor(self.settings['FillColor'])
    self.ui.profileWidthSpinBox.setValue(self.settings['ProfileWidth'])
    self.ui.minaltSpinBox.setValue(self.settings['MinimumAltitude'])
    self.ui.maxaltSpinBox.setValue(self.settings['MaximumAltitude'])
    self.ui.selectedPointsCheckBox.setChecked(self.settings['SelectedPointsOnly'])
    self.ui.startFromZeroCheckBox.setChecked(self.settings['StartFromZero'])
    self.ui.autoscaleAltitudesCheckBox.setChecked(self.settings['AutoscaleAltitudes'])
    self.ui.showHoursCheckBox.setChecked(self.settings['ShowHours'])
    self.ui.absoluteTimeCheckBox.setChecked(self.settings['AbsoluteTime'])
    self.ui.useSystemThemeCheckBox.setChecked(self.settings['UseSystemTheme'])
    self.ui.fontFamilyBox.setCurrentText(self.settings['FontFamily'])
    self.ui.fontSizeSpinBox.setValue(self.settings['FontSize'])
    self.ui.distanceCoeffSpinBox.setValue(self.settings['DistanceCoefficient'])
    self.ui.showCoefficientCheckBox.setChecked(self.settings['ShowDistanceCoefficient'])
    self.ui.timezoneSpinBox.setValue(self.settings['TimeZoneOffset'])
    self.ui.sortByTimeCheckBox.setChecked(self.settings['SortByTime'])
    self.ui.nameTagBox.setCurrentIndex(self.settings['ReadNameFromTag'])
    self.ui.coordinateBox.setCurrentIndex(self.settings['CoordinateFormat'])

    self.ui.startFromZeroCheckBox.setEnabled(self.settings['SelectedPointsOnly'])
    self.ui.startFromZeroLabel.setEnabled(self.settings['SelectedPointsOnly'])
    self.ui.showCoefficientCheckBox.setEnabled(self.settings['DistanceCoefficient'] != 1.0)
    self.ui.showCoefficientLabel.setEnabled(self.settings['DistanceCoefficient'] != 1.0)

    self.ui.profileColorButton.colorSet.connect(self.setProfileColor)
    self.ui.fillColorButton.colorSet.connect(self.setFillColor)
    self.ui.profileWidthSpinBox.valueChanged.connect(self.setProfileWidth)
    self.ui.minaltSpinBox.valueChanged.connect(self.setMinimumAltitude)
    self.ui.maxaltSpinBox.valueChanged.connect(self.setMaximumAltitude)
    self.ui.selectedPointsCheckBox.toggled[bool].connect(self.setSelectedPointsOnly)
    self.ui.startFromZeroCheckBox.toggled[bool].connect(self.setStartFromZero)
    self.ui.autoscaleAltitudesCheckBox.toggled[bool].connect(self.setAutoscaleAltitudes)
    self.ui.showHoursCheckBox.toggled[bool].connect(self.setShowHours)
    self.ui.absoluteTimeCheckBox.toggled[bool].connect(self.setAbsoluteTime)
    self.ui.useSystemThemeCheckBox.toggled[bool].connect(self.setUseSystemTheme)
    self.ui.fontFamilyBox.currentTextChanged.connect(self.setFontFamily)
    self.ui.fontSizeSpinBox.valueChanged.connect(self.setFontSize)
    self.ui.distanceCoeffSpinBox.valueChanged.connect(self.setDistanceCoefficient)
    self.ui.showCoefficientCheckBox.toggled[bool].connect(self.setShowDistanceCoefficient)
    self.ui.timezoneSpinBox.valueChanged.connect(self.setTimeZoneOffset)
    self.ui.sortByTimeCheckBox.toggled[bool].connect(self.setSortByTime)
    self.ui.nameTagBox.currentIndexChanged.connect(self.setNameTag)
    self.ui.coordinateBox.currentIndexChanged.connect(self.setCoordinateFormat)

  def accept(self):
    super(SettingsDialog, self).accept()

    for option in TheConfig['ProfileStyle'].keys():
      TheConfig['ProfileStyle'][option] = str(self.settings[option])

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
    self.ui.maxaltSpinBox.setMinimum(self.settings['MinimumAltitude'] + 1)

  @pyqtSlot()
  def setMaximumAltitude(self):
    self.settings['MaximumAltitude'] = self.ui.maxaltSpinBox.value()
    self.ui.minaltSpinBox.setMaximum(self.settings['MaximumAltitude'] - 1)

  @pyqtSlot(bool)
  def setSelectedPointsOnly(self, enabled):
    self.settings['SelectedPointsOnly'] = enabled
    self.ui.startFromZeroCheckBox.setEnabled(self.settings['SelectedPointsOnly'])
    self.ui.startFromZeroLabel.setEnabled(self.settings['SelectedPointsOnly'])

  @pyqtSlot(bool)
  def setStartFromZero(self, enabled):
    self.settings['StartFromZero'] = enabled

  @pyqtSlot(bool)
  def setAutoscaleAltitudes(self, enabled):
    self.settings['AutoscaleAltitudes'] = enabled

  @pyqtSlot(bool)
  def setShowHours(self, enabled):
    self.settings['ShowHours'] = enabled

  @pyqtSlot(bool)
  def setAbsoluteTime(self, enabled):
    self.settings['AbsoluteTime'] = enabled

  @pyqtSlot(bool)
  def setUseSystemTheme(self, enabled):
    self.settings['UseSystemTheme'] = enabled

  @pyqtSlot()
  def setFontFamily(self):
    self.settings['FontFamily'] = self.ui.fontFamilyBox.currentText()

  @pyqtSlot()
  def setFontSize(self):
    self.settings['FontSize'] = self.ui.fontSizeSpinBox.value()

  @pyqtSlot()
  def setDistanceCoefficient(self):
    self.settings['DistanceCoefficient'] = round(self.ui.distanceCoeffSpinBox.value(), self.ui.distanceCoeffSpinBox.decimals())
    self.ui.showCoefficientCheckBox.setEnabled(self.settings['DistanceCoefficient'] != 1.0)
    self.ui.showCoefficientLabel.setEnabled(self.settings['DistanceCoefficient'] != 1.0)

  @pyqtSlot(bool)
  def setShowDistanceCoefficient(self, enabled):
    self.settings['ShowDistanceCoefficient'] = enabled

  @pyqtSlot()
  def setTimeZoneOffset(self):
    self.settings['TimeZoneOffset'] = self.ui.timezoneSpinBox.value()

  @pyqtSlot(bool)
  def setSortByTime(self, enabled):
    self.settings['SortByTime'] = enabled

  @pyqtSlot()
  def setNameTag(self):
    self.settings['ReadNameFromTag'] = self.ui.nameTagBox.currentIndex()

  @pyqtSlot()
  def setCoordinateFormat(self):
    self.settings['CoordinateFormat'] = self.ui.coordinateBox.currentIndex()
