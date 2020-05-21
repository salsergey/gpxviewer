# gpxviewer
#
# Copyright (C) 2017-2019 Sergey Salnikov <salsergey@gmail.com>
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

from datetime import timedelta
from PyQt5.QtCore import Qt, QRegularExpression, pyqtSlot
from PyQt5.QtGui import QGuiApplication, QIcon
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QMainWindow, QSizePolicy, QSpacerItem, QTableWidgetItem, QWidget
import gpxviewer.gpxmodel as gpx
from gpxviewer.configstore import TheConfig
from gpxviewer.gpxdocument import TheDocument
import gpxviewer.ui_statwindow


NAME, DIST, RAISE, DROP, TIME = range(5)


class StatWindow(QMainWindow):
  def __init__(self, parent=None):
    super(StatWindow, self).__init__(parent)
    self.ui = gpxviewer.ui_statwindow.Ui_StatWindow()
    self.ui.setupUi(self)

    self.setWindowIcon(QIcon(':/icons/gpxviewer.svg'))

    wdg = QWidget()
    wdg.setLayout(QHBoxLayout())
    wdg.layout().addItem(QSpacerItem(40, 20, QSizePolicy.Expanding))
    self.filterLabel = QLabel(self.tr('By name:'))
    wdg.layout().addWidget(self.filterLabel)
    self.filterLineEdit = QLineEdit()
    self.filterLineEdit.setMinimumWidth(200)
    self.filterLineEdit.setPlaceholderText(self.tr('Enter regular expression'))
    self.filterLineEdit.setClearButtonEnabled(True)
    wdg.layout().addWidget(self.filterLineEdit)
    self.ui.toolBar.addWidget(wdg)
    self.filterLineEdit.textChanged.connect(self.updateStatistics)

    self.ui.statWidget.itemSelectionChanged.connect(self.updateTotalStatistics)

    self.ui.actionBySplittingLines.setChecked(TheConfig['StatWindow'].getboolean('BySplittingLines'))
    self.resize(TheConfig['StatWindow'].getint('WindowWidth'), TheConfig['StatWindow'].getint('WindowHeight'))

  def keyPressEvent(self, event):
    if event.key() == Qt.Key_Escape:
      if self.ui.statWidget.selectionModel().hasSelection():
        self.ui.statWidget.clearSelection()
      else:
        self.hide()
    if event.key() == Qt.Key_C and event.modifiers() == Qt.ControlModifier:
      self.copyToClipboard()
    super(StatWindow, self).keyPressEvent(event)

  def resizeEvent(self, event):
    super(StatWindow, self).resizeEvent(event)
    self.ui.statWidget.resizeColumnsToContents()
    TheConfig['StatWindow']['WindowWidth'] = str(event.size().width())
    TheConfig['StatWindow']['WindowHeight'] = str(event.size().height())

  def show(self):
    self.updateStatistics()
    self.updateTotalStatistics()
    super(StatWindow, self).show()

  @pyqtSlot(bool)
  def onBySplittingLinesToggled(self, checked):
    self.filterLabel.setEnabled(not checked)
    self.filterLineEdit.setEnabled(not checked)
    TheConfig['StatWindow']['BySplittingLines'] = str(checked)
    self.updateStatistics()

  @pyqtSlot()
  def updateStatistics(self):
    self.ui.statWidget.clearContents()
    n = 0
    alt_raise = 0
    alt_drop = 0

    for i in range(TheDocument.wptmodel.rowCount()):
      if TheDocument.wptmodel.index(i, 0).data(gpx.IncludeRole):
        point_start = TheDocument.wptmodel.waypoints[i]
        point_prev = point_start
        break
    for i in range(TheDocument.wptmodel.rowCount() - 1, -1, -1):
      if TheDocument.wptmodel.index(i, 0).data(gpx.IncludeRole):
        i_stop = i
        break

    segments = []
    for i, p in enumerate(TheDocument.wptmodel.waypoints):
      if TheDocument.wptmodel.index(i, 0).data(gpx.IncludeRole):
        if self.ui.actionBySplittingLines.isChecked() and TheDocument.wptmodel.index(i, 0).data(gpx.SplitLineRole) or \
           not self.ui.actionBySplittingLines.isChecked() and QRegularExpression(self.filterLineEdit.text()).match(p[gpx.NAME]).hasMatch() or \
           i == i_stop:
          if p['ID'] != point_start['ID']:
            segments += [i]
    self.ui.statWidget.setRowCount(len(segments))

    for i, p in enumerate(TheDocument.wptmodel.waypoints):
      if TheDocument.wptmodel.index(i, 0).data(gpx.IncludeRole):
        if p[gpx.ALT] > point_prev[gpx.ALT]:
          alt_raise += round(p[gpx.ALT] - point_prev[gpx.ALT])
        else:
          alt_drop += round(point_prev[gpx.ALT] - p[gpx.ALT])
        point_prev = p

        if i in segments:
          self.ui.statWidget.setItem(n, NAME, QTableWidgetItem(point_start[gpx.NAME] + ' — ' + p[gpx.NAME]))
          self.ui.statWidget.setItem(n, DIST, QTableWidgetItem(str(round(p[gpx.DIST] - point_start[gpx.DIST], 3))))
          self.ui.statWidget.setItem(n, RAISE, QTableWidgetItem(str(alt_raise)))
          self.ui.statWidget.setItem(n, DROP, QTableWidgetItem(str(alt_drop)))
          time_item = QTableWidgetItem(str(p[gpx.TIME] - point_start[gpx.TIME]))
          time_item.setData(Qt.UserRole, p[gpx.TIME] - point_start[gpx.TIME])
          self.ui.statWidget.setItem(n, TIME, time_item)
          point_start = p
          n += 1
          alt_raise = 0
          alt_drop = 0

    self.ui.statWidget.resizeColumnsToContents()

  @pyqtSlot()
  def updateTotalStatistics(self):
    total_dist = 0
    total_raise = 0
    total_drop = 0
    total_time = timedelta(0)

    if self.ui.statWidget.selectionModel().hasSelection():
      rows = [i.row() for i in self.ui.statWidget.selectionModel().selectedRows()]
      self.ui.totalGroupBox.setTitle(self.tr('Total (for selected segments)'))
    else:
      rows = range(self.ui.statWidget.rowCount())
      self.ui.totalGroupBox.setTitle(self.tr('Total'))

    for i in rows:
      total_dist += round(float(self.ui.statWidget.item(i, DIST).data(Qt.DisplayRole)), 3)
      total_raise += int(self.ui.statWidget.item(i, RAISE).data(Qt.DisplayRole))
      total_drop += int(self.ui.statWidget.item(i, DROP).data(Qt.DisplayRole))
      total_time += self.ui.statWidget.item(i, TIME).data(Qt.UserRole)

    self.ui.labelDist.setText(str(round(total_dist, 3)))
    self.ui.labelRaise.setText(str(total_raise))
    self.ui.labelDrop.setText(str(total_drop))
    self.ui.labelTime.setText(str(total_time))

  def copyToClipboard(self):
    text = ''
    for i in self.ui.statWidget.selectionModel().selectedRows():
      text += '\t'.join([self.ui.statWidget.item(i.row(), c).data(Qt.DisplayRole) for c in range(self.ui.statWidget.columnCount())]) + '\n'
    QGuiApplication.clipboard().setText(text)
