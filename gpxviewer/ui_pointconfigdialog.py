# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/pointconfigdialog.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_pointConfigDialog(object):
    def setupUi(self, pointConfigDialog):
        pointConfigDialog.setObjectName("pointConfigDialog")
        pointConfigDialog.setWindowModality(QtCore.Qt.WindowModal)
        pointConfigDialog.resize(320, 444)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(pointConfigDialog)
        self.verticalLayout_4.setContentsMargins(3, -1, 3, -1)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.frame = QtWidgets.QFrame(pointConfigDialog)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.markerStyleCheckBox = QtWidgets.QCheckBox(self.frame)
        self.markerStyleCheckBox.setChecked(True)
        self.markerStyleCheckBox.setObjectName("markerStyleCheckBox")
        self.horizontalLayout.addWidget(self.markerStyleCheckBox)
        self.widget = QtWidgets.QWidget(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName("widget")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.horizontalLayout_5.addWidget(self.label)
        self.markerStyleCombo = QtWidgets.QComboBox(self.widget)
        self.markerStyleCombo.setObjectName("markerStyleCombo")
        self.horizontalLayout_5.addWidget(self.markerStyleCombo)
        self.horizontalLayout.addWidget(self.widget)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.markerColorCheckBox = QtWidgets.QCheckBox(self.frame)
        self.markerColorCheckBox.setChecked(True)
        self.markerColorCheckBox.setObjectName("markerColorCheckBox")
        self.horizontalLayout_2.addWidget(self.markerColorCheckBox)
        self.markerColorButton = ColorChooser(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.markerColorButton.sizePolicy().hasHeightForWidth())
        self.markerColorButton.setSizePolicy(sizePolicy)
        self.markerColorButton.setObjectName("markerColorButton")
        self.horizontalLayout_2.addWidget(self.markerColorButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.markerSizeCheckBox = QtWidgets.QCheckBox(self.frame)
        self.markerSizeCheckBox.setChecked(True)
        self.markerSizeCheckBox.setObjectName("markerSizeCheckBox")
        self.horizontalLayout_7.addWidget(self.markerSizeCheckBox)
        self.widget_3 = QtWidgets.QWidget(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy)
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.widget_3)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_3 = QtWidgets.QLabel(self.widget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_9.addWidget(self.label_3)
        self.markerSizeSpinBox = QtWidgets.QSpinBox(self.widget_3)
        self.markerSizeSpinBox.setMinimum(1)
        self.markerSizeSpinBox.setMaximum(100)
        self.markerSizeSpinBox.setObjectName("markerSizeSpinBox")
        self.horizontalLayout_9.addWidget(self.markerSizeSpinBox)
        self.horizontalLayout_7.addWidget(self.widget_3)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.verticalLayout_4.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(pointConfigDialog)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lineStyleCheckBox = QtWidgets.QCheckBox(self.frame_2)
        self.lineStyleCheckBox.setChecked(True)
        self.lineStyleCheckBox.setObjectName("lineStyleCheckBox")
        self.horizontalLayout_3.addWidget(self.lineStyleCheckBox)
        self.widget_2 = QtWidgets.QWidget(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_2 = QtWidgets.QLabel(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_6.addWidget(self.label_2)
        self.lineStyleCombo = QtWidgets.QComboBox(self.widget_2)
        self.lineStyleCombo.setObjectName("lineStyleCombo")
        self.horizontalLayout_6.addWidget(self.lineStyleCombo)
        self.horizontalLayout_3.addWidget(self.widget_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.lineColorCheckBox = QtWidgets.QCheckBox(self.frame_2)
        self.lineColorCheckBox.setChecked(True)
        self.lineColorCheckBox.setObjectName("lineColorCheckBox")
        self.horizontalLayout_4.addWidget(self.lineColorCheckBox)
        self.lineColorButton = ColorChooser(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineColorButton.sizePolicy().hasHeightForWidth())
        self.lineColorButton.setSizePolicy(sizePolicy)
        self.lineColorButton.setObjectName("lineColorButton")
        self.horizontalLayout_4.addWidget(self.lineColorButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.lineWidthCheckBox = QtWidgets.QCheckBox(self.frame_2)
        self.lineWidthCheckBox.setChecked(True)
        self.lineWidthCheckBox.setObjectName("lineWidthCheckBox")
        self.horizontalLayout_8.addWidget(self.lineWidthCheckBox)
        self.widget_4 = QtWidgets.QWidget(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_4.sizePolicy().hasHeightForWidth())
        self.widget_4.setSizePolicy(sizePolicy)
        self.widget_4.setObjectName("widget_4")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.widget_4)
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_4 = QtWidgets.QLabel(self.widget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_10.addWidget(self.label_4)
        self.lineWidthSpinBox = QtWidgets.QDoubleSpinBox(self.widget_4)
        self.lineWidthSpinBox.setDecimals(1)
        self.lineWidthSpinBox.setMinimum(0.1)
        self.lineWidthSpinBox.setSingleStep(0.1)
        self.lineWidthSpinBox.setObjectName("lineWidthSpinBox")
        self.horizontalLayout_10.addWidget(self.lineWidthSpinBox)
        self.horizontalLayout_8.addWidget(self.widget_4)
        self.verticalLayout_2.addLayout(self.horizontalLayout_8)
        self.verticalLayout_4.addWidget(self.frame_2)
        self.frame_3 = QtWidgets.QFrame(pointConfigDialog)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.captionPositionCheckBox = QtWidgets.QCheckBox(self.frame_3)
        self.captionPositionCheckBox.setChecked(True)
        self.captionPositionCheckBox.setObjectName("captionPositionCheckBox")
        self.horizontalLayout_11.addWidget(self.captionPositionCheckBox)
        self.widget_5 = QtWidgets.QWidget(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_5.sizePolicy().hasHeightForWidth())
        self.widget_5.setSizePolicy(sizePolicy)
        self.widget_5.setObjectName("widget_5")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.widget_5)
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.label_5 = QtWidgets.QLabel(self.widget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_12.addWidget(self.label_5)
        self.captionPositionXSpinBox = QtWidgets.QSpinBox(self.widget_5)
        self.captionPositionXSpinBox.setMinimum(-99)
        self.captionPositionXSpinBox.setMaximum(99)
        self.captionPositionXSpinBox.setObjectName("captionPositionXSpinBox")
        self.horizontalLayout_12.addWidget(self.captionPositionXSpinBox)
        self.captionPositionYSpinBox = QtWidgets.QSpinBox(self.widget_5)
        self.captionPositionYSpinBox.setMinimum(-99)
        self.captionPositionYSpinBox.setMaximum(99)
        self.captionPositionYSpinBox.setObjectName("captionPositionYSpinBox")
        self.horizontalLayout_12.addWidget(self.captionPositionYSpinBox)
        self.horizontalLayout_11.addWidget(self.widget_5)
        self.verticalLayout_3.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.captionSizeCheckBox = QtWidgets.QCheckBox(self.frame_3)
        self.captionSizeCheckBox.setChecked(True)
        self.captionSizeCheckBox.setObjectName("captionSizeCheckBox")
        self.horizontalLayout_13.addWidget(self.captionSizeCheckBox)
        self.widget_6 = QtWidgets.QWidget(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_6.sizePolicy().hasHeightForWidth())
        self.widget_6.setSizePolicy(sizePolicy)
        self.widget_6.setObjectName("widget_6")
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout(self.widget_6)
        self.horizontalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.label_6 = QtWidgets.QLabel(self.widget_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_14.addWidget(self.label_6)
        self.captionSizeSpinBox = QtWidgets.QSpinBox(self.widget_6)
        self.captionSizeSpinBox.setMinimum(1)
        self.captionSizeSpinBox.setMaximum(100)
        self.captionSizeSpinBox.setObjectName("captionSizeSpinBox")
        self.horizontalLayout_14.addWidget(self.captionSizeSpinBox)
        self.horizontalLayout_13.addWidget(self.widget_6)
        self.verticalLayout_3.addLayout(self.horizontalLayout_13)
        self.verticalLayout_4.addWidget(self.frame_3)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(pointConfigDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_4.addWidget(self.buttonBox)

        self.retranslateUi(pointConfigDialog)
        self.buttonBox.accepted.connect(pointConfigDialog.accept)
        self.buttonBox.rejected.connect(pointConfigDialog.reject)
        self.markerStyleCheckBox.toggled['bool'].connect(self.widget.setEnabled)
        self.markerColorCheckBox.toggled['bool'].connect(self.markerColorButton.setEnabled)
        self.lineStyleCheckBox.toggled['bool'].connect(self.widget_2.setEnabled)
        self.lineColorCheckBox.toggled['bool'].connect(self.lineColorButton.setEnabled)
        self.markerSizeCheckBox.toggled['bool'].connect(self.widget_3.setEnabled)
        self.lineWidthCheckBox.toggled['bool'].connect(self.widget_4.setEnabled)
        self.captionSizeCheckBox.toggled['bool'].connect(self.widget_6.setEnabled)
        self.captionPositionCheckBox.toggled['bool'].connect(self.widget_5.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(pointConfigDialog)

    def retranslateUi(self, pointConfigDialog):
        _translate = QtCore.QCoreApplication.translate
        pointConfigDialog.setWindowTitle(_translate("pointConfigDialog", "Configure point style"))
        self.label.setText(_translate("pointConfigDialog", "Marker style"))
        self.markerColorButton.setText(_translate("pointConfigDialog", "Marker color"))
        self.label_3.setText(_translate("pointConfigDialog", "Marker size"))
        self.label_2.setText(_translate("pointConfigDialog", "Split line style"))
        self.lineColorButton.setText(_translate("pointConfigDialog", "Split line color"))
        self.label_4.setText(_translate("pointConfigDialog", "Split line width"))
        self.label_5.setText(_translate("pointConfigDialog", "Caption position (x, y)"))
        self.label_6.setText(_translate("pointConfigDialog", "Caption size"))

from gpxviewer.colorchooser import ColorChooser
