# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/plotwindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PlotWindow(object):
    def setupUi(self, PlotWindow):
        PlotWindow.setObjectName("PlotWindow")
        PlotWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(PlotWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.canvasWidget = PlotCanvas(self.centralwidget)
        self.canvasWidget.setObjectName("canvasWidget")
        self.verticalLayout.addWidget(self.canvasWidget)
        PlotWindow.setCentralWidget(self.centralwidget)
        self.toolBar = QtWidgets.QToolBar(PlotWindow)
        self.toolBar.setMovable(False)
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolBar.setObjectName("toolBar")
        PlotWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actExportCurrentSize = QtWidgets.QAction(PlotWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("ui/."), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actExportCurrentSize.setIcon(icon)
        self.actExportCurrentSize.setObjectName("actExportCurrentSize")
        self.actExportSelectedSize = QtWidgets.QAction(PlotWindow)
        self.actExportSelectedSize.setIcon(icon)
        self.actExportSelectedSize.setObjectName("actExportSelectedSize")
        self.actFitWidth = QtWidgets.QAction(PlotWindow)
        self.actFitWidth.setShortcut("Ctrl+R")
        self.actFitWidth.setObjectName("actFitWidth")
        self.toolBar.addAction(self.actExportCurrentSize)
        self.toolBar.addAction(self.actExportSelectedSize)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actFitWidth)

        self.retranslateUi(PlotWindow)
        self.actExportCurrentSize.triggered.connect(PlotWindow.onSaveCurrentSize)
        self.actExportSelectedSize.triggered.connect(PlotWindow.onSaveSelectedSize)
        self.actFitWidth.triggered.connect(PlotWindow.onFitWidth)
        QtCore.QMetaObject.connectSlotsByName(PlotWindow)

    def retranslateUi(self, PlotWindow):
        _translate = QtCore.QCoreApplication.translate
        self.actExportCurrentSize.setText(_translate("PlotWindow", "Export current size"))
        self.actExportCurrentSize.setToolTip(_translate("PlotWindow", "Export current size"))
        self.actExportSelectedSize.setText(_translate("PlotWindow", "Export selected size"))
        self.actExportSelectedSize.setToolTip(_translate("PlotWindow", "Export selected size"))
        self.actFitWidth.setText(_translate("PlotWindow", "Fit width"))
from gpxviewer.plotcanvas import PlotCanvas
