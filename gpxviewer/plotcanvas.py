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

from PyQt5.QtCore import QSortFilterProxyModel
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtGui import QColor, qAlpha
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib import rc
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from math import ceil
import gpxviewer.gpxmodel as gpx
from gpxviewer.gpxdocument import TheDocument
from gpxviewer.configstore import TheConfig


class PlotCanvas(FigureCanvas):
  def __init__(self, parent=None, width=12.8, height=10.24, dpi=100):
    # to be able to show cyrillic names
    font = {'family': ['Arial', 'Droid Sans'], 'weight': 'normal', 'size': 12}
    rc('font', **font)
    fig = Figure(figsize=(width, height), dpi=dpi, facecolor='w')
    self.axes = fig.add_subplot(111)

    FigureCanvas.__init__(self, fig)
    self.setParent(parent)

    FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
    FigureCanvas.updateGeometry(self)

    # filter out all skipped points
    self.model = QSortFilterProxyModel(self)
    self.model.setSourceModel(TheDocument.gpxmodel)
    self.model.setFilterKeyColumn(gpx.NAME)
    self.model.setFilterRole(gpx.IncludeRole)

  def plotProfile(self, column):
    self.model.setFilterRegExp(str(gpx.INC_DEFAULT) + '|' + str(gpx.INC_MARKER) + '|' + str(gpx.INC_CAPTION))
    self.axes.clear()
    self.axes.grid(axis='y')
    if column == gpx.DIST:
      self.axes.set_xlabel(self.tr('Distance with coefficient 1.2 (km)'))
    else:
      self.axes.set_xlabel(self.tr('Time (days)'))
    self.axes.set_ylabel(self.tr('Altitude (m)'))

    xx = []
    yy = []
    markers = []
    splitLines = []
    neglectPoints = [0]
    captions = []
    for i in range(self.model.rowCount()):
      xx +=  [float(self.model.index(i, column).data())]
      yy +=  [float(self.model.index(i, gpx.ALT).data())]
      if self.model.index(i, 0).data(gpx.IncludeRole) in {gpx.INC_MARKER, gpx.INC_CAPTION}:
        markers += [(i, self.model.index(i, 0).data(gpx.MarkerRole))]
      if self.model.index(i, 0).data(gpx.SplitStateRole):
        splitLines += [(i, self.model.index(i, 0).data(gpx.SplitLineRole))]
      if i != 0 and self.model.index(i, 0).data(gpx.NeglectRole):
        neglectPoints += [i]
      if self.model.index(i, 0).data(gpx.IncludeRole) == gpx.INC_CAPTION:
        captions += [(i, self.model.index(i, 0).data(gpx.CaptionRole))]
    neglectPoints += [self.model.rowCount()]

    self.axes.set_xlim(xmax=xx[-1])
    self.axes.set_ylim(ymin=int(TheConfig['ProfileStyle']['MinimumAltitude']), ymax=int(TheConfig['ProfileStyle']['MaximumAltitude']))

    if column == gpx.DIST:
      self.axes.set_xticks(range(0, int(ceil(xx[-1])), 5))
    else:
      self.axes.set_xticks(range(int(ceil(xx[-1]))))

    for l in splitLines:
      self.axes.plot([xx[l[0]]] * 2, [int(TheConfig['ProfileStyle']['MinimumAltitude']), yy[l[0]]], linestyle=l[1][gpx.LINE_STYLE], color=_colorTuple(l[1][gpx.LINE_COLOR]), linewidth=l[1][gpx.LINE_WIDTH])

    self.axes.fill_between(xx, int(TheConfig['ProfileStyle']['MinimumAltitude']), yy, color=_colorTuple(int(TheConfig['ProfileStyle']['FillColor'])))
    for n in range(1, len(neglectPoints)):
      self.axes.plot(xx[neglectPoints[n-1]:neglectPoints[n]], yy[neglectPoints[n-1]:neglectPoints[n]], color=_colorTuple(int(TheConfig['ProfileStyle']['ProfileColor'])), linewidth=float(TheConfig['ProfileStyle']['ProfileWidth']))

    for m in markers:
      self.axes.plot(xx[m[0]], yy[m[0]], marker=m[1][gpx.MARKER_STYLE], color=_colorTuple(m[1][gpx.MARKER_COLOR]), markersize=m[1][gpx.MARKER_SIZE])

    for c in captions:
      self.axes.annotate(self.model.index(c[0], gpx.NAME).data(), (xx[c[0]], yy[c[0]]), xytext=(c[1][gpx.CAPTION_POSX], c[1][gpx.CAPTION_POSY]), fontsize=c[1][gpx.CAPTION_SIZE], rotation='vertical', horizontalalignment='center', verticalalignment='bottom', textcoords='offset points')

    self.draw()

  def saveProfile(self, filename, figsize=None):
    origSize = self.figure.get_size_inches()
    if figsize != None:
      self.figure.set_size_inches(figsize[0]/100, figsize[1]/100)
    self.print_figure(filename)
    if figsize != None:
      self.figure.set_size_inches(origSize[0], origSize[1])
      self.draw()


def _colorTuple(rgba):
  color = QColor(rgba)
  color.setAlpha(qAlpha(rgba))
  return color.redF(), color.greenF(), color.blueF(), color.alphaF()
