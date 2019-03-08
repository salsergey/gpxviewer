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

from math import ceil
import matplotlib
from matplotlib import rc
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtCore import QSortFilterProxyModel
from PyQt5.QtGui import QColor, qAlpha
from PyQt5.QtWidgets import QSizePolicy
import gpxviewer.gpxmodel as gpx
from gpxviewer.configstore import TheConfig
from gpxviewer.gpxdocument import TheDocument


class PlotCanvas(FigureCanvas):
  def __init__(self, parent=None, width=12.8, height=10.24, dpi=100):
    # to be able to show cyrillic names
    font = {'family': ['CMU Sans Serif', 'Arial', 'DejaVu Sans'], 'style': 'normal', 'size': 12}
    rc('font', **font)
    fig = Figure(figsize=(width, height), dpi=dpi, facecolor='w')
    self.axes = fig.add_subplot(111)

    FigureCanvas.__init__(self, fig)
    self.setParent(parent)

    FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
    FigureCanvas.updateGeometry(self)

  def plotProfile(self, column, wptRows, trkRows):
    xx = []
    yy = []
    markers = []
    splitLines = []
    neglectPoints = [0]
    captions = []
    zeroDist = 0
    for p in TheDocument.gpxparser.points:
      if type(p) == int:
        if (p in wptRows or len(wptRows) == 0) and (column == gpx.DIST or TheDocument.wptmodel.index(p, column).data() != ''):
          xx += [float(TheDocument.wptmodel.index(p, column).data()) - zeroDist]
          yy += [float(TheDocument.wptmodel.index(p, gpx.ALT).data())]
          if len(xx) == 1:
            zeroDist = xx[0]
            xx[0] = 0
          if TheDocument.wptmodel.index(p, 0).data(gpx.MarkerRole):
            markers += [(xx[-1], yy[-1], TheDocument.wptmodel.index(p, 0).data(gpx.MarkerStyleRole))]
          if TheDocument.wptmodel.index(p, 0).data(gpx.SplitLineRole):
            splitLines += [(xx[-1], yy[-1], TheDocument.wptmodel.index(p, 0).data(gpx.SplitLineStyleRole))]
          if p != 0 and TheDocument.wptmodel.index(p, 0).data(gpx.NeglectRole):
            neglectPoints += [xx[-1]]
          if TheDocument.wptmodel.index(p, 0).data(gpx.CaptionRole):
            captions += [(p, xx[-1], yy[-1], TheDocument.wptmodel.index(p, 0).data(gpx.CaptionStyleRole))]
      elif p[0] in trkRows or len(trkRows) == 0 and len(wptRows) == 0:
        if column == gpx.DIST or TheDocument.trkmodel.index(p[0], gpx.TRKTIME).data() != '':
          xx += [float(TheDocument.trkmodel.tracks[p[0]]['SEGMENTS'][p[1]][p[2]][column]) - zeroDist]
          yy += [float(TheDocument.trkmodel.tracks[p[0]]['SEGMENTS'][p[1]][p[2]][gpx.ALT])]
          if len(xx) == 1:
            zeroDist = xx[0]
            xx[0] = 0
    neglectPoints += [xx[-1]]

    self.axes.clear()
    self.axes.grid(axis='y', linestyle='--', linewidth=0.5)
    if column == gpx.DIST:
      dist_coeff = TheConfig.getValue('ProfileStyle', 'DistanceCoefficient')
      if dist_coeff == 1.0:
        self.axes.set_xlabel(self.tr('Distance (km)'))
      else:
        self.axes.set_xlabel(self.tr('Distance with coefficient ') + str(dist_coeff) + self.tr(' (km)'))
    else:
      if xx[-1] > 1:
        self.axes.set_xlabel(self.tr('Time (days)'))
      else:
        self.axes.set_xlabel(self.tr('Time (hours)'))
    self.axes.set_ylabel(self.tr('Altitude (m)'))

    self.axes.set_xlim(right=xx[-1])
    self.axes.set_ylim(bottom=TheConfig.getValue('ProfileStyle', 'MinimumAltitude'), top=TheConfig.getValue('ProfileStyle', 'MaximumAltitude'))

    if column == gpx.DIST:
      if xx[-1] > 100:
        step = 10
      elif xx[-1] > 50:
        step = 5
      elif xx[-1] > 20:
        step = 2
      else:
        step = 1
      self.axes.set_xticks(range(0, ceil(xx[-1]), int(ceil(step))))
    else:
      if xx[-1] > 1:
        self.axes.set_xticks(range(int(ceil(xx[-1]))))
      else:
        self.axes.set_xticks([t / 24 for t in range(int(ceil(24 * xx[-1])))])
        self.axes.set_xticklabels([str(t) for t in range(int(ceil(24 * xx[-1])))])

    for l in splitLines:
      self.axes.plot([l[0]] * 2, [TheConfig.getValue('ProfileStyle', 'MinimumAltitude'), l[1]],
                     linestyle=l[2][gpx.LINE_STYLE], color=_colorTuple(l[2][gpx.LINE_COLOR]), linewidth=l[2][gpx.LINE_WIDTH])

    self.axes.fill_between(xx, TheConfig.getValue('ProfileStyle', 'MinimumAltitude'),
                           yy, color=_colorTuple(TheConfig.getValue('ProfileStyle', 'FillColor')))
    for n in range(1, len(neglectPoints)):
      self.axes.plot(xx[xx.index(neglectPoints[n-1]) + (1 if n > 1 else 0):xx.index(neglectPoints[n]) + 1],
                     yy[xx.index(neglectPoints[n-1]) + (1 if n > 1 else 0):xx.index(neglectPoints[n]) + 1],
                     color=_colorTuple(TheConfig.getValue('ProfileStyle', 'ProfileColor')),
                     linewidth=TheConfig.getValue('ProfileStyle', 'ProfileWidth'))

    for m in markers:
      self.axes.plot(m[0], m[1], marker=m[2][gpx.MARKER_STYLE], color=_colorTuple(m[2][gpx.MARKER_COLOR]), markersize=m[2][gpx.MARKER_SIZE])

    for c in captions:
      self.axes.annotate(TheDocument.wptmodel.index(c[0], gpx.NAME).data(), (c[1], c[2]), xytext=(c[3][gpx.CAPTION_POSX], c[3][gpx.CAPTION_POSY]),
                         fontsize=c[3][gpx.CAPTION_SIZE], rotation='vertical', horizontalalignment='center', verticalalignment='bottom', textcoords='offset points')

    self.draw()

  def saveProfile(self, filename, figsize=None):
    origSize = self.figure.get_size_inches()
    if figsize is not None:
      self.figure.set_size_inches(figsize[0]/100, figsize[1]/100)
    self.print_figure(filename)
    if figsize is not None:
      self.figure.set_size_inches(origSize[0], origSize[1])
      self.draw()


def _colorTuple(rgba):
  color = QColor(rgba)
  color.setAlpha(qAlpha(rgba))
  return color.redF(), color.greenF(), color.blueF(), color.alphaF()
