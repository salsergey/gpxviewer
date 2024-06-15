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

from PyQt6.QtCore import Qt, QRect, pyqtSignal, pyqtSlot
from PyQt6.QtGui import qAlpha, QColor, QPainter
from PyQt6.QtWidgets import QColorDialog, QDialog, QPushButton, QStyle, QStyleOptionButton


class ColorChooser(QPushButton):
  def __init__(self, parent=None):
    super(ColorChooser, self).__init__(parent)
    self.buttonWidth = 70
    self.clicked.connect(self.openColorDialog)

  def mousePressEvent(self, e):
    if e.pos().x() > self.width() - self.buttonWidth:
      super(ColorChooser, self).mousePressEvent(e)

  def paintEvent(self, event):
    optBtn = QStyleOptionButton()
    optBtn.initFrom(self)
    optBtn.state = QStyle.StateFlag.State_Sunken if self.isDown() else QStyle.StateFlag.State_Raised
    optBtn.rect.setLeft(optBtn.rect.right() - self.buttonWidth)
    label = self.text()[1:] if self.text().startswith('&') else self.text()
    color = self.color
    if not self.isEnabled():
      color = self.color.darker()
    self.setStyleSheet('QPushButton { background-color: rgba(' + str(color.red()) + ',' +
                                                                 str(color.green()) + ',' +
                                                                 str(color.blue()) + ',' +
                                                                 str(color.alpha()) + ')}')

    p = QPainter(self)
    p.drawText(QRect(0, 0, self.width() - self.buttonWidth, self.height()), Qt.AlignmentFlag.AlignVCenter, label)
    self.style().drawControl(QStyle.ControlElement.CE_PushButton, optBtn, p, self)

  def setColor(self, rgba):
    self.color = QColor(rgba)
    self.color.setAlpha(qAlpha(rgba))

  @pyqtSlot()
  def openColorDialog(self):
    dlg = QColorDialog()
    dlg.setOption(QColorDialog.ColorDialogOption.ShowAlphaChannel)
    dlg.setCurrentColor(self.color)
    if dlg.exec() == QDialog.DialogCode.Accepted:
      self.color = dlg.currentColor()
      self.colorSet.emit()

  colorSet = pyqtSignal()
