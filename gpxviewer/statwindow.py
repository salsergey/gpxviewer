# gpxviewer
#
# Copyright (C) 2017 Sergey Salnikov <salsergey@gmail.com>
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

from datetime import datetime, timedelta
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIcon
import gpxviewer.gpxmodel as gpx
from gpxviewer.configstore import TheConfig
from gpxviewer.gpxdocument import TheDocument
import gpxviewer.ui_statwindow


NAME, DIST, RAISE, DROP, TIME = range(5)


class StatWindow(QtWidgets.QMainWindow):
  def __init__(self, parent=None):
    super(StatWindow, self).__init__(parent)
    self.ui = gpxviewer.ui_statwindow.Ui_StatWindow()
    self.ui.setupUi(self)

    self.setWindowIcon(QIcon(':/icons/gpxviewer.svg'))

    wdg = QtWidgets.QWidget()
    wdg.setLayout(QtWidgets.QHBoxLayout())
    wdg.layout().addItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding))
    self.filterLabel = QtWidgets.QLabel(self.tr('By name:'))
    wdg.layout().addWidget(self.filterLabel)
    self.filterLineEdit = QtWidgets.QLineEdit()
    self.filterLineEdit.setMinimumWidth(200)
    self.filterLineEdit.setPlaceholderText(self.tr('Enter regular expression'))
    self.filterLineEdit.setClearButtonEnabled(True)
    wdg.layout().addWidget(self.filterLineEdit)
    self.ui.toolBar.addWidget(wdg)
    self.filterLineEdit.textChanged.connect(self.updateStatistics)

    self.ui.actionBySplittingLines.setChecked(TheConfig['StatWindow'].getboolean('BySplittingLines'))

    self.resize(TheConfig['StatWindow'].getint('WindowWidth'), TheConfig['StatWindow'].getint('WindowHeight'))

  def keyPressEvent(self, event):
    if event.key() == QtCore.Qt.Key_Escape:
      self.hide()
    if event.key() == QtCore.Qt.Key_C and event.modifiers() == QtCore.Qt.ControlModifier:
      self.copyToClipboard()
    super(StatWindow, self).keyPressEvent(event)

  def resizeEvent(self, event):
    super(StatWindow, self).resizeEvent(event)
    self.ui.statWidget.resizeColumnsToContents()
    TheConfig['StatWindow']['WindowWidth'] = str(event.size().width())
    TheConfig['StatWindow']['WindowHeight'] = str(event.size().height())

  def BySplittingLinesToggled(self, checked):
    self.filterLabel.setEnabled(not checked)
    self.filterLineEdit.setEnabled(not checked)
    TheConfig['StatWindow']['BySplittingLines'] = str(checked)
    self.updateStatistics()

  def updateStatistics(self):
    self.ui.statWidget.clearContents()
    n = 0
    alt_raise = 0
    alt_drop = 0
    total_dist = 0
    total_raise = 0
    total_drop = 0
    total_time = timedelta(0)

    for i, s in enumerate(TheDocument.wptmodel.includeStates):
      if s != gpx.INC_SKIP:
        point_start = TheDocument.wptmodel.waypoints[i]
        point_prev = point_start
        break
    for i, s in enumerate(TheDocument.wptmodel.includeStates[::-1]):
      if s != gpx.INC_SKIP:
        i_stop = TheDocument.wptmodel.rowCount() - i - 1
        break

    segments = []
    for i, p in enumerate(TheDocument.wptmodel.waypoints):
      if TheDocument.wptmodel.includeStates[i] != gpx.INC_SKIP:
        if self.ui.actionBySplittingLines.isChecked() and TheDocument.wptmodel.splitStates[i] or \
           not self.ui.actionBySplittingLines.isChecked() and QtCore.QRegularExpression(self.filterLineEdit.text()).match(p[gpx.NAME]).hasMatch() or \
           i == i_stop:
             if p['ID'] != point_start['ID']:
              segments += [i]
    self.ui.statWidget.setRowCount(len(segments))

    for i, p in enumerate(TheDocument.wptmodel.waypoints):
      if TheDocument.wptmodel.includeStates[i] != gpx.INC_SKIP:
        if p[gpx.ALT] > point_prev[gpx.ALT]:
          alt_raise += p[gpx.ALT] - point_prev[gpx.ALT]
        else:
          alt_drop += point_prev[gpx.ALT] - p[gpx.ALT]
        point_prev = p

        if i in segments:
          self.ui.statWidget.setItem(n, NAME, QtWidgets.QTableWidgetItem(point_start[gpx.NAME] + ' — ' + p[gpx.NAME]))
          self.ui.statWidget.setItem(n, DIST, QtWidgets.QTableWidgetItem(str(round(p[gpx.DIST] - point_start[gpx.DIST], 3))))
          self.ui.statWidget.setItem(n, RAISE, QtWidgets.QTableWidgetItem(str(alt_raise)))
          self.ui.statWidget.setItem(n, DROP, QtWidgets.QTableWidgetItem(str(alt_drop)))
          self.ui.statWidget.setItem(n, TIME, QtWidgets.QTableWidgetItem(str(p[gpx.TIME] - point_start[gpx.TIME])))
          total_dist += round(p[gpx.DIST] - point_start[gpx.DIST], 3)
          total_raise += alt_raise
          total_drop += alt_drop
          total_time += p[gpx.TIME] - point_start[gpx.TIME]
          point_start = p
          n += 1
          alt_raise = 0
          alt_drop = 0

    self.ui.labelDist.setText(str(round(total_dist, 3)))
    self.ui.labelRaise.setText(str(total_raise))
    self.ui.labelDrop.setText(str(total_drop))
    self.ui.labelTime.setText(str(total_time))

    self.ui.statWidget.resizeColumnsToContents()

  def copyToClipboard(self):
    text = ''
    for i in self.ui.statWidget.selectionModel().selectedRows():
      text += '\t'.join([self.ui.statWidget.item(i.row(), c).data(QtCore.Qt.DisplayRole) for c in range(self.ui.statWidget.columnCount())]) + '\n'
    QGuiApplication.clipboard().setText(text)
