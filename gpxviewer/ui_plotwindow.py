# Form implementation generated from reading ui file 'ui/plotwindow.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_PlotWindow(object):
    def setupUi(self, PlotWindow):
        PlotWindow.setObjectName("PlotWindow")
        PlotWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(parent=PlotWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.canvasWidget = PlotCanvas(parent=self.centralwidget)
        self.canvasWidget.setObjectName("canvasWidget")
        self.verticalLayout.addWidget(self.canvasWidget)
        PlotWindow.setCentralWidget(self.centralwidget)
        self.toolBar = QtWidgets.QToolBar(parent=PlotWindow)
        self.toolBar.setMovable(False)
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.toolBar.setObjectName("toolBar")
        PlotWindow.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, self.toolBar)
        self.actExportCurrentSize = QtGui.QAction(parent=PlotWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("ui/."), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actExportCurrentSize.setIcon(icon)
        self.actExportCurrentSize.setObjectName("actExportCurrentSize")
        self.actExportSelectedSize = QtGui.QAction(parent=PlotWindow)
        self.actExportSelectedSize.setIcon(icon)
        self.actExportSelectedSize.setObjectName("actExportSelectedSize")
        self.actFitWidth = QtGui.QAction(parent=PlotWindow)
        self.actFitWidth.setShortcut("Ctrl+R")
        self.actFitWidth.setObjectName("actFitWidth")
        self.actShowInformation = QtGui.QAction(parent=PlotWindow)
        self.actShowInformation.setCheckable(True)
        self.actShowInformation.setShortcut("Ctrl+I")
        self.actShowInformation.setObjectName("actShowInformation")
        self.toolBar.addAction(self.actExportCurrentSize)
        self.toolBar.addAction(self.actExportSelectedSize)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actFitWidth)
        self.toolBar.addAction(self.actShowInformation)

        self.retranslateUi(PlotWindow)
        self.actExportCurrentSize.triggered.connect(PlotWindow.onSaveCurrentSize) # type: ignore
        self.actExportSelectedSize.triggered.connect(PlotWindow.onSaveSelectedSize) # type: ignore
        self.actFitWidth.triggered.connect(PlotWindow.onFitWidth) # type: ignore
        self.actShowInformation.triggered['bool'].connect(PlotWindow.onShowInformation) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(PlotWindow)

    def retranslateUi(self, PlotWindow):
        _translate = QtCore.QCoreApplication.translate
        self.actExportCurrentSize.setText(_translate("PlotWindow", "Export current size"))
        self.actExportCurrentSize.setToolTip(_translate("PlotWindow", "Export current size"))
        self.actExportSelectedSize.setText(_translate("PlotWindow", "Export selected size"))
        self.actExportSelectedSize.setToolTip(_translate("PlotWindow", "Export selected size"))
        self.actFitWidth.setText(_translate("PlotWindow", "Fit width"))
        self.actShowInformation.setText(_translate("PlotWindow", "Show information"))
from gpxviewer.plotcanvas import PlotCanvas
