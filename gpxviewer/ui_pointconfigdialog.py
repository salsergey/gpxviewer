# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/pointconfigdialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_pointConfigDialog(object):
    def setupUi(self, pointConfigDialog):
        pointConfigDialog.setObjectName("pointConfigDialog")
        pointConfigDialog.setWindowModality(QtCore.Qt.WindowModal)
        pointConfigDialog.resize(330, 552)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(pointConfigDialog)
        self.verticalLayout_4.setContentsMargins(3, -1, 3, -1)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.groupBox = QtWidgets.QGroupBox(pointConfigDialog)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_1 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_1.setObjectName("horizontalLayout_1")
        self.markerStyleCheckBox = QtWidgets.QCheckBox(self.groupBox)
        self.markerStyleCheckBox.setChecked(True)
        self.markerStyleCheckBox.setObjectName("markerStyleCheckBox")
        self.horizontalLayout_1.addWidget(self.markerStyleCheckBox)
        self.markerStyleWidget = QtWidgets.QWidget(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.markerStyleWidget.sizePolicy().hasHeightForWidth())
        self.markerStyleWidget.setSizePolicy(sizePolicy)
        self.markerStyleWidget.setObjectName("markerStyleWidget")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.markerStyleWidget)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_1 = QtWidgets.QLabel(self.markerStyleWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_1.sizePolicy().hasHeightForWidth())
        self.label_1.setSizePolicy(sizePolicy)
        self.label_1.setObjectName("label_1")
        self.horizontalLayout_5.addWidget(self.label_1)
        self.markerStyleCombo = QtWidgets.QComboBox(self.markerStyleWidget)
        self.markerStyleCombo.setObjectName("markerStyleCombo")
        self.horizontalLayout_5.addWidget(self.markerStyleCombo)
        self.horizontalLayout_1.addWidget(self.markerStyleWidget)
        self.verticalLayout.addLayout(self.horizontalLayout_1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.markerColorCheckBox = QtWidgets.QCheckBox(self.groupBox)
        self.markerColorCheckBox.setChecked(True)
        self.markerColorCheckBox.setObjectName("markerColorCheckBox")
        self.horizontalLayout_2.addWidget(self.markerColorCheckBox)
        self.markerColorButton = ColorChooser(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.markerColorButton.sizePolicy().hasHeightForWidth())
        self.markerColorButton.setSizePolicy(sizePolicy)
        self.markerColorButton.setObjectName("markerColorButton")
        self.horizontalLayout_2.addWidget(self.markerColorButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.markerSizeCheckBox = QtWidgets.QCheckBox(self.groupBox)
        self.markerSizeCheckBox.setChecked(True)
        self.markerSizeCheckBox.setObjectName("markerSizeCheckBox")
        self.horizontalLayout_3.addWidget(self.markerSizeCheckBox)
        self.markerSizeWidget = QtWidgets.QWidget(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.markerSizeWidget.sizePolicy().hasHeightForWidth())
        self.markerSizeWidget.setSizePolicy(sizePolicy)
        self.markerSizeWidget.setObjectName("markerSizeWidget")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.markerSizeWidget)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_2 = QtWidgets.QLabel(self.markerSizeWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_9.addWidget(self.label_2)
        self.markerSizeSpinBox = QtWidgets.QSpinBox(self.markerSizeWidget)
        self.markerSizeSpinBox.setMinimum(1)
        self.markerSizeSpinBox.setMaximum(100)
        self.markerSizeSpinBox.setObjectName("markerSizeSpinBox")
        self.horizontalLayout_9.addWidget(self.markerSizeSpinBox)
        self.horizontalLayout_3.addWidget(self.markerSizeWidget)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_4.addWidget(self.groupBox)
        self.groupBox_3 = QtWidgets.QGroupBox(pointConfigDialog)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.captionPositionCheckBox = QtWidgets.QCheckBox(self.groupBox_3)
        self.captionPositionCheckBox.setChecked(True)
        self.captionPositionCheckBox.setObjectName("captionPositionCheckBox")
        self.horizontalLayout_4.addWidget(self.captionPositionCheckBox)
        self.captionPositionWidget = QtWidgets.QWidget(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.captionPositionWidget.sizePolicy().hasHeightForWidth())
        self.captionPositionWidget.setSizePolicy(sizePolicy)
        self.captionPositionWidget.setObjectName("captionPositionWidget")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.captionPositionWidget)
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.label_3 = QtWidgets.QLabel(self.captionPositionWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_12.addWidget(self.label_3)
        self.captionPositionXSpinBox = QtWidgets.QSpinBox(self.captionPositionWidget)
        self.captionPositionXSpinBox.setMinimum(-999)
        self.captionPositionXSpinBox.setMaximum(999)
        self.captionPositionXSpinBox.setObjectName("captionPositionXSpinBox")
        self.horizontalLayout_12.addWidget(self.captionPositionXSpinBox)
        self.captionPositionYSpinBox = QtWidgets.QSpinBox(self.captionPositionWidget)
        self.captionPositionYSpinBox.setMinimum(-999)
        self.captionPositionYSpinBox.setMaximum(999)
        self.captionPositionYSpinBox.setObjectName("captionPositionYSpinBox")
        self.horizontalLayout_12.addWidget(self.captionPositionYSpinBox)
        self.horizontalLayout_4.addWidget(self.captionPositionWidget)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.captionRotationCheckBox = QtWidgets.QCheckBox(self.groupBox_3)
        self.captionRotationCheckBox.setChecked(True)
        self.captionRotationCheckBox.setObjectName("captionRotationCheckBox")
        self.horizontalLayout_15.addWidget(self.captionRotationCheckBox)
        self.captionRotationWidget = QtWidgets.QWidget(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.captionRotationWidget.sizePolicy().hasHeightForWidth())
        self.captionRotationWidget.setSizePolicy(sizePolicy)
        self.captionRotationWidget.setObjectName("captionRotationWidget")
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout(self.captionRotationWidget)
        self.horizontalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.label_5 = QtWidgets.QLabel(self.captionRotationWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_16.addWidget(self.label_5)
        self.captionRotationSpinBox = QtWidgets.QSpinBox(self.captionRotationWidget)
        self.captionRotationSpinBox.setMinimum(-179)
        self.captionRotationSpinBox.setMaximum(180)
        self.captionRotationSpinBox.setObjectName("captionRotationSpinBox")
        self.horizontalLayout_16.addWidget(self.captionRotationSpinBox)
        self.horizontalLayout_15.addWidget(self.captionRotationWidget)
        self.verticalLayout_3.addLayout(self.horizontalLayout_15)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.captionSizeCheckBox = QtWidgets.QCheckBox(self.groupBox_3)
        self.captionSizeCheckBox.setChecked(True)
        self.captionSizeCheckBox.setObjectName("captionSizeCheckBox")
        self.horizontalLayout_11.addWidget(self.captionSizeCheckBox)
        self.captionSizeWidget = QtWidgets.QWidget(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.captionSizeWidget.sizePolicy().hasHeightForWidth())
        self.captionSizeWidget.setSizePolicy(sizePolicy)
        self.captionSizeWidget.setObjectName("captionSizeWidget")
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout(self.captionSizeWidget)
        self.horizontalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.label_4 = QtWidgets.QLabel(self.captionSizeWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_14.addWidget(self.label_4)
        self.captionSizeSpinBox = QtWidgets.QSpinBox(self.captionSizeWidget)
        self.captionSizeSpinBox.setMinimum(1)
        self.captionSizeSpinBox.setObjectName("captionSizeSpinBox")
        self.horizontalLayout_14.addWidget(self.captionSizeSpinBox)
        self.horizontalLayout_11.addWidget(self.captionSizeWidget)
        self.verticalLayout_3.addLayout(self.horizontalLayout_11)
        self.verticalLayout_4.addWidget(self.groupBox_3)
        self.groupBox_2 = QtWidgets.QGroupBox(pointConfigDialog)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.lineStyleCheckBox = QtWidgets.QCheckBox(self.groupBox_2)
        self.lineStyleCheckBox.setChecked(True)
        self.lineStyleCheckBox.setObjectName("lineStyleCheckBox")
        self.horizontalLayout_13.addWidget(self.lineStyleCheckBox)
        self.lineStyleWidget = QtWidgets.QWidget(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineStyleWidget.sizePolicy().hasHeightForWidth())
        self.lineStyleWidget.setSizePolicy(sizePolicy)
        self.lineStyleWidget.setObjectName("lineStyleWidget")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.lineStyleWidget)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_6 = QtWidgets.QLabel(self.lineStyleWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_6.addWidget(self.label_6)
        self.lineStyleCombo = QtWidgets.QComboBox(self.lineStyleWidget)
        self.lineStyleCombo.setObjectName("lineStyleCombo")
        self.horizontalLayout_6.addWidget(self.lineStyleCombo)
        self.horizontalLayout_13.addWidget(self.lineStyleWidget)
        self.verticalLayout_2.addLayout(self.horizontalLayout_13)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.lineColorCheckBox = QtWidgets.QCheckBox(self.groupBox_2)
        self.lineColorCheckBox.setChecked(True)
        self.lineColorCheckBox.setObjectName("lineColorCheckBox")
        self.horizontalLayout_7.addWidget(self.lineColorCheckBox)
        self.lineColorButton = ColorChooser(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineColorButton.sizePolicy().hasHeightForWidth())
        self.lineColorButton.setSizePolicy(sizePolicy)
        self.lineColorButton.setObjectName("lineColorButton")
        self.horizontalLayout_7.addWidget(self.lineColorButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.lineWidthCheckBox = QtWidgets.QCheckBox(self.groupBox_2)
        self.lineWidthCheckBox.setChecked(True)
        self.lineWidthCheckBox.setObjectName("lineWidthCheckBox")
        self.horizontalLayout_8.addWidget(self.lineWidthCheckBox)
        self.lineWidthWidget = QtWidgets.QWidget(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineWidthWidget.sizePolicy().hasHeightForWidth())
        self.lineWidthWidget.setSizePolicy(sizePolicy)
        self.lineWidthWidget.setObjectName("lineWidthWidget")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.lineWidthWidget)
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_7 = QtWidgets.QLabel(self.lineWidthWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_10.addWidget(self.label_7)
        self.lineWidthSpinBox = QtWidgets.QDoubleSpinBox(self.lineWidthWidget)
        self.lineWidthSpinBox.setDecimals(1)
        self.lineWidthSpinBox.setMinimum(0.1)
        self.lineWidthSpinBox.setSingleStep(0.1)
        self.lineWidthSpinBox.setObjectName("lineWidthSpinBox")
        self.horizontalLayout_10.addWidget(self.lineWidthSpinBox)
        self.horizontalLayout_8.addWidget(self.lineWidthWidget)
        self.verticalLayout_2.addLayout(self.horizontalLayout_8)
        self.verticalLayout_4.addWidget(self.groupBox_2)
        spacerItem = QtWidgets.QSpacerItem(0, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(pointConfigDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_4.addWidget(self.buttonBox)

        self.retranslateUi(pointConfigDialog)
        self.buttonBox.accepted.connect(pointConfigDialog.accept)
        self.buttonBox.rejected.connect(pointConfigDialog.reject)
        self.markerStyleCheckBox.toggled['bool'].connect(self.markerStyleWidget.setEnabled)
        self.captionSizeCheckBox.toggled['bool'].connect(self.captionSizeWidget.setEnabled)
        self.captionPositionCheckBox.toggled['bool'].connect(self.captionPositionWidget.setEnabled)
        self.lineColorCheckBox.toggled['bool'].connect(self.lineColorButton.setEnabled)
        self.lineStyleCheckBox.toggled['bool'].connect(self.lineStyleWidget.setEnabled)
        self.lineWidthCheckBox.toggled['bool'].connect(self.lineWidthWidget.setEnabled)
        self.markerSizeCheckBox.toggled['bool'].connect(self.markerSizeWidget.setEnabled)
        self.markerColorCheckBox.toggled['bool'].connect(self.markerColorButton.setEnabled)
        self.captionRotationCheckBox.toggled['bool'].connect(self.captionRotationWidget.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(pointConfigDialog)

    def retranslateUi(self, pointConfigDialog):
        _translate = QtCore.QCoreApplication.translate
        pointConfigDialog.setWindowTitle(_translate("pointConfigDialog", "Configure point style"))
        self.groupBox.setTitle(_translate("pointConfigDialog", "Marker"))
        self.markerStyleCheckBox.setToolTip(_translate("pointConfigDialog", "Whether to change this property for selected points"))
        self.label_1.setText(_translate("pointConfigDialog", "Marker style"))
        self.markerStyleCombo.setToolTip(_translate("pointConfigDialog", "The shape of the marker"))
        self.markerColorCheckBox.setToolTip(_translate("pointConfigDialog", "Whether to change this property for selected points"))
        self.markerColorButton.setToolTip(_translate("pointConfigDialog", "The color of the marker"))
        self.markerColorButton.setText(_translate("pointConfigDialog", "Marker color"))
        self.markerSizeCheckBox.setToolTip(_translate("pointConfigDialog", "Whether to change this property for selected points"))
        self.label_2.setText(_translate("pointConfigDialog", "Marker size"))
        self.markerSizeSpinBox.setToolTip(_translate("pointConfigDialog", "The size of the marker"))
        self.groupBox_3.setTitle(_translate("pointConfigDialog", "Caption"))
        self.captionPositionCheckBox.setToolTip(_translate("pointConfigDialog", "Whether to change this property for selected points"))
        self.label_3.setText(_translate("pointConfigDialog", "Caption position (x, y)"))
        self.captionPositionXSpinBox.setToolTip(_translate("pointConfigDialog", "The position of the caption"))
        self.captionPositionYSpinBox.setToolTip(_translate("pointConfigDialog", "The position of the caption"))
        self.captionRotationCheckBox.setToolTip(_translate("pointConfigDialog", "Whether to change this property for selected points"))
        self.label_5.setText(_translate("pointConfigDialog", "Caption rotation"))
        self.captionRotationSpinBox.setToolTip(_translate("pointConfigDialog", "The rotation angle of the caption in degrees"))
        self.captionSizeCheckBox.setToolTip(_translate("pointConfigDialog", "Whether to change this property for selected points"))
        self.label_4.setText(_translate("pointConfigDialog", "Caption size"))
        self.captionSizeSpinBox.setToolTip(_translate("pointConfigDialog", "The size of the caption"))
        self.groupBox_2.setTitle(_translate("pointConfigDialog", "Split line"))
        self.lineStyleCheckBox.setToolTip(_translate("pointConfigDialog", "Whether to change this property for selected points"))
        self.label_6.setText(_translate("pointConfigDialog", "Split line style"))
        self.lineStyleCombo.setToolTip(_translate("pointConfigDialog", "The style of the split line"))
        self.lineColorCheckBox.setToolTip(_translate("pointConfigDialog", "Whether to change this property for selected points"))
        self.lineColorButton.setToolTip(_translate("pointConfigDialog", "The color of the split line"))
        self.lineColorButton.setText(_translate("pointConfigDialog", "Split line color"))
        self.lineWidthCheckBox.setToolTip(_translate("pointConfigDialog", "Whether to change this property for selected points"))
        self.label_7.setText(_translate("pointConfigDialog", "Split line width"))
        self.lineWidthSpinBox.setToolTip(_translate("pointConfigDialog", "The width of the split line"))
from gpxviewer.colorchooser import ColorChooser
