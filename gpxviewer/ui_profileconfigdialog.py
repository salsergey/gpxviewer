# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/profileconfigdialog.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_profileConfigDialog(object):
    def setupUi(self, profileConfigDialog):
        profileConfigDialog.setObjectName("profileConfigDialog")
        profileConfigDialog.setWindowModality(QtCore.Qt.WindowModal)
        profileConfigDialog.resize(247, 308)
        self.verticalLayout = QtWidgets.QVBoxLayout(profileConfigDialog)
        self.verticalLayout.setContentsMargins(3, -1, 3, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(profileConfigDialog)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.profileColorButton = ColorChooser(self.frame)
        self.profileColorButton.setObjectName("profileColorButton")
        self.verticalLayout_2.addWidget(self.profileColorButton)
        self.fillColorButton = ColorChooser(self.frame)
        self.fillColorButton.setObjectName("fillColorButton")
        self.verticalLayout_2.addWidget(self.fillColorButton)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_4 = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.profileWidthSpinBox = QtWidgets.QDoubleSpinBox(self.frame)
        self.profileWidthSpinBox.setDecimals(1)
        self.profileWidthSpinBox.setMinimum(0.1)
        self.profileWidthSpinBox.setSingleStep(0.1)
        self.profileWidthSpinBox.setObjectName("profileWidthSpinBox")
        self.horizontalLayout.addWidget(self.profileWidthSpinBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_5 = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.minaltSpinBox = QtWidgets.QSpinBox(self.frame)
        self.minaltSpinBox.setMaximum(10000)
        self.minaltSpinBox.setObjectName("minaltSpinBox")
        self.horizontalLayout_2.addWidget(self.minaltSpinBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_6 = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_3.addWidget(self.label_6)
        self.maxaltSpinBox = QtWidgets.QSpinBox(self.frame)
        self.maxaltSpinBox.setMaximum(10000)
        self.maxaltSpinBox.setObjectName("maxaltSpinBox")
        self.horizontalLayout_3.addWidget(self.maxaltSpinBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_7 = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_4.addWidget(self.label_7)
        self.timezoneSpinBox = QtWidgets.QSpinBox(self.frame)
        self.timezoneSpinBox.setMinimum(-999)
        self.timezoneSpinBox.setMaximum(999)
        self.timezoneSpinBox.setObjectName("timezoneSpinBox")
        self.horizontalLayout_4.addWidget(self.timezoneSpinBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.verticalLayout.addWidget(self.frame)
        self.buttonBox = QtWidgets.QDialogButtonBox(profileConfigDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(profileConfigDialog)
        self.buttonBox.accepted.connect(profileConfigDialog.accept)
        self.buttonBox.rejected.connect(profileConfigDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(profileConfigDialog)

    def retranslateUi(self, profileConfigDialog):
        _translate = QtCore.QCoreApplication.translate
        profileConfigDialog.setWindowTitle(_translate("profileConfigDialog", "Configure profile style"))
        self.profileColorButton.setText(_translate("profileConfigDialog", "Profile color"))
        self.fillColorButton.setText(_translate("profileConfigDialog", "Fill color"))
        self.label_4.setText(_translate("profileConfigDialog", "Profile width"))
        self.label_5.setText(_translate("profileConfigDialog", "Minimum altitude"))
        self.label_6.setText(_translate("profileConfigDialog", "Maximum altitude"))
        self.label_7.setText(_translate("profileConfigDialog", "Time zone offset"))
        self.timezoneSpinBox.setSuffix(_translate("profileConfigDialog", " min"))

from gpxviewer.colorchooser import ColorChooser
