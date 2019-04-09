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

from PyQt5.QtCore import Qt, QRect, pyqtSignal, pyqtSlot
from PyQt5.QtGui import qAlpha, QColor, QPainter
from PyQt5.QtWidgets import QColorDialog, QDialog, QPushButton, QStyle, QStyleOptionButton


class ColorChooser(QPushButton):
  def __init__(self, parent=None):
    super(ColorChooser, self).__init__(parent)
    self.buttonWidth = 60
    self.clicked.connect(self.openColorDialog)

  def mousePressEvent(self, e):
    if e.pos().x() > self.width() - self.buttonWidth:
      super(ColorChooser, self).mousePressEvent(e)

  def paintEvent(self, event):
    optBtn = QStyleOptionButton()
    optBtn.initFrom(self)
    optBtn.state = QStyle.State_Sunken if self.isDown() else QStyle.State_Raised
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
    p.drawText(QRect(0, 0, self.width() - self.buttonWidth, self.height()), Qt.AlignVCenter, label)
    self.style().drawControl(QStyle.CE_PushButton, optBtn, p, self)

  def setColor(self, rgba):
    self.color = QColor(rgba)
    self.color.setAlpha(qAlpha(rgba))

  @pyqtSlot()
  def openColorDialog(self):
    dlg = QColorDialog()
    dlg.setOption(QColorDialog.ShowAlphaChannel)
    dlg.setCurrentColor(self.color)
    if dlg.exec_() == QDialog.Accepted:
      self.color = dlg.currentColor()
      self.colorSet.emit()

  colorSet = pyqtSignal()
