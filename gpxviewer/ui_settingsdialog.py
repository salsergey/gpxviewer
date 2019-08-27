# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/settingsdialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_settingsDialog(object):
    def setupUi(self, settingsDialog):
        settingsDialog.setObjectName("settingsDialog")
        settingsDialog.setWindowModality(QtCore.Qt.WindowModal)
        self.verticalLayout = QtWidgets.QVBoxLayout(settingsDialog)
        self.verticalLayout.setContentsMargins(3, -1, 3, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(settingsDialog)
        self.tabWidget.setObjectName("tabWidget")
        self.tabProfile = QtWidgets.QWidget()
        self.tabProfile.setObjectName("tabProfile")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tabProfile)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.profileColorButton = ColorChooser(self.tabProfile)
        self.profileColorButton.setObjectName("profileColorButton")
        self.verticalLayout_2.addWidget(self.profileColorButton)
        self.fillColorButton = ColorChooser(self.tabProfile)
        self.fillColorButton.setObjectName("fillColorButton")
        self.verticalLayout_2.addWidget(self.fillColorButton)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout.setFormAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.formLayout.setObjectName("formLayout")
        self.label_1 = QtWidgets.QLabel(self.tabProfile)
        self.label_1.setObjectName("label_1")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_1)
        self.profileWidthSpinBox = QtWidgets.QDoubleSpinBox(self.tabProfile)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.profileWidthSpinBox.sizePolicy().hasHeightForWidth())
        self.profileWidthSpinBox.setSizePolicy(sizePolicy)
        self.profileWidthSpinBox.setDecimals(1)
        self.profileWidthSpinBox.setMinimum(0.1)
        self.profileWidthSpinBox.setSingleStep(0.1)
        self.profileWidthSpinBox.setObjectName("profileWidthSpinBox")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.profileWidthSpinBox)
        self.label_3 = QtWidgets.QLabel(self.tabProfile)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.minaltSpinBox = QtWidgets.QSpinBox(self.tabProfile)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.minaltSpinBox.sizePolicy().hasHeightForWidth())
        self.minaltSpinBox.setSizePolicy(sizePolicy)
        self.minaltSpinBox.setMaximum(10000)
        self.minaltSpinBox.setSingleStep(100)
        self.minaltSpinBox.setObjectName("minaltSpinBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.minaltSpinBox)
        self.label_4 = QtWidgets.QLabel(self.tabProfile)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.maxaltSpinBox = QtWidgets.QSpinBox(self.tabProfile)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.maxaltSpinBox.sizePolicy().hasHeightForWidth())
        self.maxaltSpinBox.setSizePolicy(sizePolicy)
        self.maxaltSpinBox.setMaximum(10000)
        self.maxaltSpinBox.setSingleStep(100)
        self.maxaltSpinBox.setObjectName("maxaltSpinBox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.maxaltSpinBox)
        self.label_6 = QtWidgets.QLabel(self.tabProfile)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.autoscaleAltitudesCheckBox = QtWidgets.QCheckBox(self.tabProfile)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.autoscaleAltitudesCheckBox.sizePolicy().hasHeightForWidth())
        self.autoscaleAltitudesCheckBox.setSizePolicy(sizePolicy)
        self.autoscaleAltitudesCheckBox.setMinimumSize(QtCore.QSize(0, 32))
        self.autoscaleAltitudesCheckBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.autoscaleAltitudesCheckBox.setObjectName("autoscaleAltitudesCheckBox")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.autoscaleAltitudesCheckBox)
        self.useSystemThemeLabel = QtWidgets.QLabel(self.tabProfile)
        self.useSystemThemeLabel.setObjectName("useSystemThemeLabel")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.useSystemThemeLabel)
        self.useSystemThemeCheckBox = QtWidgets.QCheckBox(self.tabProfile)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.useSystemThemeCheckBox.sizePolicy().hasHeightForWidth())
        self.useSystemThemeCheckBox.setSizePolicy(sizePolicy)
        self.useSystemThemeCheckBox.setMinimumSize(QtCore.QSize(0, 32))
        self.useSystemThemeCheckBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.useSystemThemeCheckBox.setObjectName("useSystemThemeCheckBox")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.useSystemThemeCheckBox)
        self.label_5 = QtWidgets.QLabel(self.tabProfile)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.selectedPointsCheckBox = QtWidgets.QCheckBox(self.tabProfile)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.selectedPointsCheckBox.sizePolicy().hasHeightForWidth())
        self.selectedPointsCheckBox.setSizePolicy(sizePolicy)
        self.selectedPointsCheckBox.setMinimumSize(QtCore.QSize(0, 32))
        self.selectedPointsCheckBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.selectedPointsCheckBox.setObjectName("selectedPointsCheckBox")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.selectedPointsCheckBox)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.startFromZeroLabel = QtWidgets.QLabel(self.tabProfile)
        self.startFromZeroLabel.setObjectName("startFromZeroLabel")
        self.horizontalLayout_4.addWidget(self.startFromZeroLabel)
        self.formLayout.setLayout(6, QtWidgets.QFormLayout.LabelRole, self.horizontalLayout_4)
        self.startFromZeroCheckBox = QtWidgets.QCheckBox(self.tabProfile)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.startFromZeroCheckBox.sizePolicy().hasHeightForWidth())
        self.startFromZeroCheckBox.setSizePolicy(sizePolicy)
        self.startFromZeroCheckBox.setMinimumSize(QtCore.QSize(0, 32))
        self.startFromZeroCheckBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.startFromZeroCheckBox.setObjectName("startFromZeroCheckBox")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.startFromZeroCheckBox)
        self.verticalLayout_2.addLayout(self.formLayout)
        self.groupBox_2 = QtWidgets.QGroupBox(self.tabProfile)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.fontFamilyBox = QtWidgets.QFontComboBox(self.groupBox_2)
        self.fontFamilyBox.setObjectName("fontFamilyBox")
        self.horizontalLayout_2.addWidget(self.fontFamilyBox)
        self.fontSizeSpinBox = QtWidgets.QSpinBox(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fontSizeSpinBox.sizePolicy().hasHeightForWidth())
        self.fontSizeSpinBox.setSizePolicy(sizePolicy)
        self.fontSizeSpinBox.setMinimum(1)
        self.fontSizeSpinBox.setObjectName("fontSizeSpinBox")
        self.horizontalLayout_2.addWidget(self.fontSizeSpinBox)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.tabWidget.addTab(self.tabProfile, "")
        self.tabSettings = QtWidgets.QWidget()
        self.tabSettings.setObjectName("tabSettings")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tabSettings)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout_2.setFormAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_8 = QtWidgets.QLabel(self.tabSettings)
        self.label_8.setObjectName("label_8")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.distanceCoeffSpinBox = QtWidgets.QDoubleSpinBox(self.tabSettings)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.distanceCoeffSpinBox.sizePolicy().hasHeightForWidth())
        self.distanceCoeffSpinBox.setSizePolicy(sizePolicy)
        self.distanceCoeffSpinBox.setDecimals(1)
        self.distanceCoeffSpinBox.setMinimum(0.1)
        self.distanceCoeffSpinBox.setSingleStep(0.1)
        self.distanceCoeffSpinBox.setObjectName("distanceCoeffSpinBox")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.distanceCoeffSpinBox)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.showCoefficientLabel = QtWidgets.QLabel(self.tabSettings)
        self.showCoefficientLabel.setObjectName("showCoefficientLabel")
        self.horizontalLayout_5.addWidget(self.showCoefficientLabel)
        self.formLayout_2.setLayout(1, QtWidgets.QFormLayout.LabelRole, self.horizontalLayout_5)
        self.showCoefficientCheckBox = QtWidgets.QCheckBox(self.tabSettings)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.showCoefficientCheckBox.sizePolicy().hasHeightForWidth())
        self.showCoefficientCheckBox.setSizePolicy(sizePolicy)
        self.showCoefficientCheckBox.setMinimumSize(QtCore.QSize(0, 32))
        self.showCoefficientCheckBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.showCoefficientCheckBox.setObjectName("showCoefficientCheckBox")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.showCoefficientCheckBox)
        self.label_10 = QtWidgets.QLabel(self.tabSettings)
        self.label_10.setObjectName("label_10")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_10)
        self.timezoneSpinBox = QtWidgets.QSpinBox(self.tabSettings)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.timezoneSpinBox.sizePolicy().hasHeightForWidth())
        self.timezoneSpinBox.setSizePolicy(sizePolicy)
        self.timezoneSpinBox.setMinimum(-999)
        self.timezoneSpinBox.setMaximum(999)
        self.timezoneSpinBox.setObjectName("timezoneSpinBox")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.timezoneSpinBox)
        self.label_11 = QtWidgets.QLabel(self.tabSettings)
        self.label_11.setObjectName("label_11")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_11)
        self.nameTagBox = QtWidgets.QComboBox(self.tabSettings)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nameTagBox.sizePolicy().hasHeightForWidth())
        self.nameTagBox.setSizePolicy(sizePolicy)
        self.nameTagBox.setObjectName("nameTagBox")
        self.nameTagBox.addItem("")
        self.nameTagBox.addItem("")
        self.nameTagBox.addItem("")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.nameTagBox)
        self.verticalLayout_3.addLayout(self.formLayout_2)
        self.groupBox = QtWidgets.QGroupBox(self.tabSettings)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.coordinateBox = QtWidgets.QComboBox(self.groupBox)
        self.coordinateBox.setObjectName("coordinateBox")
        self.coordinateBox.addItem("")
        self.coordinateBox.addItem("")
        self.coordinateBox.addItem("")
        self.horizontalLayout.addWidget(self.coordinateBox)
        self.verticalLayout_3.addWidget(self.groupBox)
        spacerItem3 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem3)
        self.tabWidget.addTab(self.tabSettings, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.buttonBox = QtWidgets.QDialogButtonBox(settingsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(settingsDialog)
        self.tabWidget.setCurrentIndex(0)
        self.buttonBox.accepted.connect(settingsDialog.accept)
        self.buttonBox.rejected.connect(settingsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(settingsDialog)

    def retranslateUi(self, settingsDialog):
        _translate = QtCore.QCoreApplication.translate
        settingsDialog.setWindowTitle(_translate("settingsDialog", "Settings"))
        self.profileColorButton.setText(_translate("settingsDialog", "Profile color"))
        self.fillColorButton.setText(_translate("settingsDialog", "Fill color"))
        self.label_1.setText(_translate("settingsDialog", "Profile width"))
        self.label_3.setText(_translate("settingsDialog", "Minimum altitude"))
        self.label_4.setText(_translate("settingsDialog", "Maximum altitude"))
        self.label_6.setToolTip(_translate("settingsDialog", "Automatically scale minimum/maximum altitudes when plotting profile"))
        self.label_6.setText(_translate("settingsDialog", "Autoscale altitudes"))
        self.autoscaleAltitudesCheckBox.setToolTip(_translate("settingsDialog", "Automatically scale minimum/maximum altitudes when plotting profile"))
        self.useSystemThemeLabel.setToolTip(_translate("settingsDialog", "Use system color theme instead of default light theme"))
        self.useSystemThemeLabel.setText(_translate("settingsDialog", "Use system theme"))
        self.useSystemThemeCheckBox.setToolTip(_translate("settingsDialog", "Use system color theme instead of default light theme"))
        self.label_5.setToolTip(_translate("settingsDialog", "Plot profiles taking into account only selected points and tracks"))
        self.label_5.setText(_translate("settingsDialog", "Use only selected points"))
        self.selectedPointsCheckBox.setToolTip(_translate("settingsDialog", "Plot profiles taking into account only selected points and tracks"))
        self.startFromZeroLabel.setToolTip(_translate("settingsDialog", "Always start X axis from zero when plotting profile for selected points"))
        self.startFromZeroLabel.setText(_translate("settingsDialog", "Start from zero"))
        self.startFromZeroCheckBox.setToolTip(_translate("settingsDialog", "Always start X axis from zero when plotting profile for selected points"))
        self.groupBox_2.setTitle(_translate("settingsDialog", "Axes labels font"))
        self.fontSizeSpinBox.setToolTip(_translate("settingsDialog", "Font size"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabProfile), _translate("settingsDialog", "Profile style"))
        self.label_8.setToolTip(_translate("settingsDialog", "Calculate distance with additional coefficient"))
        self.label_8.setText(_translate("settingsDialog", "Distance coefficient"))
        self.distanceCoeffSpinBox.setToolTip(_translate("settingsDialog", "Calculate distance with additional coefficient"))
        self.showCoefficientLabel.setToolTip(_translate("settingsDialog", "Show distance coefficient under the X axis"))
        self.showCoefficientLabel.setText(_translate("settingsDialog", "Show coefficient"))
        self.showCoefficientCheckBox.setToolTip(_translate("settingsDialog", "Show distance coefficient under the X axis"))
        self.label_10.setToolTip(_translate("settingsDialog", "The difference between your time zone and UTC (used in GPX-files)"))
        self.label_10.setText(_translate("settingsDialog", "Time zone offset"))
        self.timezoneSpinBox.setToolTip(_translate("settingsDialog", "The difference between your time zone and UTC (used in GPX-files)"))
        self.timezoneSpinBox.setSuffix(_translate("settingsDialog", " min"))
        self.label_11.setToolTip(_translate("settingsDialog", "Read point names from one of the tags in GPX file: <name>, <cmt>, <desc>"))
        self.label_11.setText(_translate("settingsDialog", "Point names are in tag"))
        self.nameTagBox.setToolTip(_translate("settingsDialog", "Read point names from one of the tags in GPX file: <name>, <cmt>, <desc>"))
        self.nameTagBox.setItemText(0, _translate("settingsDialog", "Name"))
        self.nameTagBox.setItemText(1, _translate("settingsDialog", "Comment"))
        self.nameTagBox.setItemText(2, _translate("settingsDialog", "Description"))
        self.groupBox.setTitle(_translate("settingsDialog", "Coordinate format"))
        self.coordinateBox.setItemText(0, _translate("settingsDialog", "Decimal degrees"))
        self.coordinateBox.setItemText(1, _translate("settingsDialog", "Degrees with minutes"))
        self.coordinateBox.setItemText(2, _translate("settingsDialog", "Degrees, minutes, seconds"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSettings), _translate("settingsDialog", "GPX settings"))
from gpxviewer.colorchooser import ColorChooser
