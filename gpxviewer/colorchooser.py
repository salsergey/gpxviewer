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

from PyQt5 import QtCore, QtWidgets, QtGui


class ColorChooser(QtWidgets.QPushButton):
  def __init__(self, parent = None):
    super(ColorChooser, self).__init__(parent)
    self.buttonWidth = 60
    self.clicked.connect(self.openColorDialog)

  def mousePressEvent(self, e):
    if e.pos().x() > self.width() - self.buttonWidth:
      super(ColorChooser, self).mousePressEvent(e)

  def paintEvent(self, event):
    optBtn = QtWidgets.QStyleOptionButton()
    optBtn.initFrom(self)
    optBtn.state = QtWidgets.QStyle.State_Sunken if self.isDown() else QtWidgets.QStyle.State_Raised
    optBtn.rect.setLeft(optBtn.rect.right() - self.buttonWidth)
    label = self.text()[1:] if self.text().startswith('&') else self.text()
    self.setStyleSheet('QPushButton { background-color: rgba(' + str(self.color.red()) + ',' +
                                                                 str(self.color.green()) + ',' +
                                                                 str(self.color.blue()) + ',' +
                                                                 str(self.color.alpha()) + ')}')

    p = QtGui.QPainter(self)
    p.drawText(QtCore.QRect(0, 0, self.width() - self.buttonWidth, self.height()), QtCore.Qt.AlignVCenter, label)
    self.style().drawControl(QtWidgets.QStyle.CE_PushButton, optBtn, p, self)

  def setColor(self, rgba):
    self.color = QtGui.QColor(rgba)
    self.color.setAlpha(QtGui.qAlpha(rgba))

  def openColorDialog(self):
    dlg = QtWidgets.QColorDialog()
    dlg.setOption(QtWidgets.QColorDialog.ShowAlphaChannel)
    dlg.setCurrentColor(self.color)
    if dlg.exec_() == QtWidgets.QDialog.Accepted:
      self.color = dlg.currentColor()
      self.colorSet.emit()

  colorSet = QtCore.pyqtSignal()
