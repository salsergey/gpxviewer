# gpxviewer
#
# Copyright (C) 2016-2017 Sergey Salnikov <salsergey@gmail.com>
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
import gpxviewer.ui_profileconfigdialog


class ProfileConfigDialog(QDialog):
  def __init__(self, parent):
    super(ProfileConfigDialog, self).__init__(parent)
    self.ui = gpxviewer.ui_profileconfigdialog.Ui_profileConfigDialog()
    self.ui.setupUi(self)
    self.setMinimumWidth(260)
    self.style = {}
    self.style['ProfileColor'] = int(TheConfig['ProfileStyle']['ProfileColor'])
    self.style['FillColor'] = int(TheConfig['ProfileStyle']['FillColor'])
    self.style['ProfileWidth'] = float(TheConfig['ProfileStyle']['ProfileWidth'])
    self.style['MinimumAltitude'] = int(TheConfig['ProfileStyle']['MinimumAltitude'])
    self.style['MaximumAltitude'] = int(TheConfig['ProfileStyle']['MaximumAltitude'])

    self.ui.profileColorButton.setColor(self.style['ProfileColor'])
    self.ui.fillColorButton.setColor(self.style['FillColor'])
    self.ui.profileWidthSpinBox.setValue(self.style['ProfileWidth'])
    self.ui.minaltSpinBox.setValue(self.style['MinimumAltitude'])
    self.ui.maxaltSpinBox.setValue(self.style['MaximumAltitude'])

    self.ui.profileColorButton.colorSet.connect(self.setProfileColor)
    self.ui.fillColorButton.colorSet.connect(self.setFillColor)
    self.ui.profileWidthSpinBox.valueChanged.connect(self.setProfileWidth)
    self.ui.minaltSpinBox.valueChanged.connect(self.setMinimumAltitude)
    self.ui.maxaltSpinBox.valueChanged.connect(self.setMaximumAltitude)

  def setProfileColor(self):
    self.style['ProfileColor'] = self.ui.profileColorButton.color.rgba()

  def setFillColor(self):
    self.style['FillColor'] = self.ui.fillColorButton.color.rgba()

  def setProfileWidth(self):
    self.style['ProfileWidth'] = round(self.ui.profileWidthSpinBox.value(), 1)

  def setMinimumAltitude(self):
    self.style['MinimumAltitude'] = self.ui.minaltSpinBox.value()

  def setMaximumAltitude(self):
    self.style['MaximumAltitude'] = self.ui.maxaltSpinBox.value()
