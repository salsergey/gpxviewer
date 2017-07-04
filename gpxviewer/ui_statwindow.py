# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/statwindow.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_StatWindow(object):
    def setupUi(self, StatWindow):
        StatWindow.setObjectName("StatWindow")
        StatWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(StatWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.statWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.statWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.statWidget.setColumnCount(5)
        self.statWidget.setObjectName("statWidget")
        self.statWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.statWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.statWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.statWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.statWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.statWidget.setHorizontalHeaderItem(4, item)
        self.statWidget.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout_5.addWidget(self.statWidget)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.labelDist = QtWidgets.QLabel(self.groupBox)
        self.labelDist.setText("")
        self.labelDist.setAlignment(QtCore.Qt.AlignCenter)
        self.labelDist.setObjectName("labelDist")
        self.verticalLayout.addWidget(self.labelDist)
        self.horizontalLayout.addLayout(self.verticalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(93, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.labelRaise = QtWidgets.QLabel(self.groupBox)
        self.labelRaise.setText("")
        self.labelRaise.setAlignment(QtCore.Qt.AlignCenter)
        self.labelRaise.setObjectName("labelRaise")
        self.verticalLayout_2.addWidget(self.labelRaise)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        spacerItem2 = QtWidgets.QSpacerItem(92, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.labelDrop = QtWidgets.QLabel(self.groupBox)
        self.labelDrop.setText("")
        self.labelDrop.setAlignment(QtCore.Qt.AlignCenter)
        self.labelDrop.setObjectName("labelDrop")
        self.verticalLayout_3.addWidget(self.labelDrop)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        spacerItem3 = QtWidgets.QSpacerItem(93, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_4.addWidget(self.label_4)
        self.labelTime = QtWidgets.QLabel(self.groupBox)
        self.labelTime.setText("")
        self.labelTime.setAlignment(QtCore.Qt.AlignCenter)
        self.labelTime.setObjectName("labelTime")
        self.verticalLayout_4.addWidget(self.labelTime)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.verticalLayout_5.addWidget(self.groupBox)
        StatWindow.setCentralWidget(self.centralwidget)
        self.toolBar = QtWidgets.QToolBar(StatWindow)
        self.toolBar.setWindowTitle("toolBar")
        self.toolBar.setMovable(False)
        self.toolBar.setObjectName("toolBar")
        StatWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionBySplittingLines = QtWidgets.QAction(StatWindow)
        self.actionBySplittingLines.setCheckable(True)
        self.actionBySplittingLines.setObjectName("actionBySplittingLines")
        self.toolBar.addAction(self.actionBySplittingLines)

        self.retranslateUi(StatWindow)
        self.actionBySplittingLines.toggled['bool'].connect(StatWindow.BySplittingLinesToggled)
        QtCore.QMetaObject.connectSlotsByName(StatWindow)

    def retranslateUi(self, StatWindow):
        _translate = QtCore.QCoreApplication.translate
        StatWindow.setWindowTitle(_translate("StatWindow", "Statistics"))
        item = self.statWidget.horizontalHeaderItem(0)
        item.setText(_translate("StatWindow", "Name"))
        item = self.statWidget.horizontalHeaderItem(1)
        item.setText(_translate("StatWindow", "Distance"))
        item = self.statWidget.horizontalHeaderItem(2)
        item.setText(_translate("StatWindow", "Altitude raise"))
        item = self.statWidget.horizontalHeaderItem(3)
        item.setText(_translate("StatWindow", "Altitude drop"))
        item = self.statWidget.horizontalHeaderItem(4)
        item.setText(_translate("StatWindow", "Time"))
        self.groupBox.setTitle(_translate("StatWindow", "Total"))
        self.label.setText(_translate("StatWindow", "Distance"))
        self.label_2.setText(_translate("StatWindow", "Altitude raise"))
        self.label_3.setText(_translate("StatWindow", "Altitude drop"))
        self.label_4.setText(_translate("StatWindow", "Time"))
        self.actionBySplittingLines.setText(_translate("StatWindow", "By splitting lines"))
