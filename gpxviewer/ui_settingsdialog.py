# Form implementation generated from reading ui file 'ui/settingsdialog.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_settingsDialog(object):
    def setupUi(self, settingsDialog):
        settingsDialog.setObjectName("settingsDialog")
        settingsDialog.setWindowModality(QtCore.Qt.WindowModality.WindowModal)
        settingsDialog.resize(420, 468)
        self.verticalLayout = QtWidgets.QVBoxLayout(settingsDialog)
        self.verticalLayout.setContentsMargins(3, -1, 3, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(parent=settingsDialog)
        self.tabWidget.setObjectName("tabWidget")
        self.tabProfile = QtWidgets.QWidget()
        self.tabProfile.setObjectName("tabProfile")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tabProfile)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.profileColorButton = ColorChooser(parent=self.tabProfile)
        self.profileColorButton.setObjectName("profileColorButton")
        self.verticalLayout_4.addWidget(self.profileColorButton)
        self.fillColorButton = ColorChooser(parent=self.tabProfile)
        self.fillColorButton.setObjectName("fillColorButton")
        self.verticalLayout_4.addWidget(self.fillColorButton)
        self.formLayout_3 = QtWidgets.QFormLayout()
        self.formLayout_3.setLabelAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.formLayout_3.setFormAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTop|QtCore.Qt.AlignmentFlag.AlignTrailing)
        self.formLayout_3.setObjectName("formLayout_3")
        self.profileWidthLabel = QtWidgets.QLabel(parent=self.tabProfile)
        self.profileWidthLabel.setObjectName("profileWidthLabel")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.profileWidthLabel)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.profileWidthSpinBox = QtWidgets.QDoubleSpinBox(parent=self.tabProfile)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.profileWidthSpinBox.sizePolicy().hasHeightForWidth())
        self.profileWidthSpinBox.setSizePolicy(sizePolicy)
        self.profileWidthSpinBox.setMaximumSize(QtCore.QSize(100, 16777215))
        self.profileWidthSpinBox.setDecimals(1)
        self.profileWidthSpinBox.setMinimum(0.1)
        self.profileWidthSpinBox.setSingleStep(0.1)
        self.profileWidthSpinBox.setObjectName("profileWidthSpinBox")
        self.horizontalLayout_2.addWidget(self.profileWidthSpinBox)
        self.formLayout_3.setLayout(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.horizontalLayout_2)
        self.useSystemThemeLabel = QtWidgets.QLabel(parent=self.tabProfile)
        self.useSystemThemeLabel.setObjectName("useSystemThemeLabel")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.useSystemThemeLabel)
        self.useSystemThemeCheckBox = QtWidgets.QCheckBox(parent=self.tabProfile)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.useSystemThemeCheckBox.sizePolicy().hasHeightForWidth())
        self.useSystemThemeCheckBox.setSizePolicy(sizePolicy)
        self.useSystemThemeCheckBox.setMinimumSize(QtCore.QSize(0, 32))
        self.useSystemThemeCheckBox.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.useSystemThemeCheckBox.setObjectName("useSystemThemeCheckBox")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.useSystemThemeCheckBox)
        self.selectedPointsLabel = QtWidgets.QLabel(parent=self.tabProfile)
        self.selectedPointsLabel.setObjectName("selectedPointsLabel")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.selectedPointsLabel)
        self.selectedPointsCheckBox = QtWidgets.QCheckBox(parent=self.tabProfile)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.selectedPointsCheckBox.sizePolicy().hasHeightForWidth())
        self.selectedPointsCheckBox.setSizePolicy(sizePolicy)
        self.selectedPointsCheckBox.setMinimumSize(QtCore.QSize(0, 32))
        self.selectedPointsCheckBox.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.selectedPointsCheckBox.setObjectName("selectedPointsCheckBox")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.selectedPointsCheckBox)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.startFromZeroLabel = QtWidgets.QLabel(parent=self.tabProfile)
        self.startFromZeroLabel.setObjectName("startFromZeroLabel")
        self.horizontalLayout_4.addWidget(self.startFromZeroLabel)
        self.formLayout_3.setLayout(3, QtWidgets.QFormLayout.ItemRole.LabelRole, self.horizontalLayout_4)
        self.startFromZeroCheckBox = QtWidgets.QCheckBox(parent=self.tabProfile)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.startFromZeroCheckBox.sizePolicy().hasHeightForWidth())
        self.startFromZeroCheckBox.setSizePolicy(sizePolicy)
        self.startFromZeroCheckBox.setMinimumSize(QtCore.QSize(0, 32))
        self.startFromZeroCheckBox.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.startFromZeroCheckBox.setObjectName("startFromZeroCheckBox")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.ItemRole.FieldRole, self.startFromZeroCheckBox)
        self.verticalLayout_4.addLayout(self.formLayout_3)
        spacerItem2 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_4.addItem(spacerItem2)
        self.tabWidget.addTab(self.tabProfile, "")
        self.tabAxes = QtWidgets.QWidget()
        self.tabAxes.setObjectName("tabAxes")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tabAxes)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.formLayout.setFormAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTop|QtCore.Qt.AlignmentFlag.AlignTrailing)
        self.formLayout.setObjectName("formLayout")
        self.minaltLabel = QtWidgets.QLabel(parent=self.tabAxes)
        self.minaltLabel.setObjectName("minaltLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.minaltLabel)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem3)
        self.minaltSpinBox = QtWidgets.QSpinBox(parent=self.tabAxes)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.minaltSpinBox.sizePolicy().hasHeightForWidth())
        self.minaltSpinBox.setSizePolicy(sizePolicy)
        self.minaltSpinBox.setMaximumSize(QtCore.QSize(100, 16777215))
        self.minaltSpinBox.setMaximum(10000)
        self.minaltSpinBox.setSingleStep(100)
        self.minaltSpinBox.setObjectName("minaltSpinBox")
        self.horizontalLayout_6.addWidget(self.minaltSpinBox)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.horizontalLayout_6)
        self.maxaltLabel = QtWidgets.QLabel(parent=self.tabAxes)
        self.maxaltLabel.setObjectName("maxaltLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.maxaltLabel)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)
        self.maxaltSpinBox = QtWidgets.QSpinBox(parent=self.tabAxes)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.maxaltSpinBox.sizePolicy().hasHeightForWidth())
        self.maxaltSpinBox.setSizePolicy(sizePolicy)
        self.maxaltSpinBox.setMaximumSize(QtCore.QSize(100, 16777215))
        self.maxaltSpinBox.setMaximum(10000)
        self.maxaltSpinBox.setSingleStep(100)
        self.maxaltSpinBox.setObjectName("maxaltSpinBox")
        self.horizontalLayout_3.addWidget(self.maxaltSpinBox)
        self.formLayout.setLayout(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.horizontalLayout_3)
        self.autoscaleAltitudesLabel = QtWidgets.QLabel(parent=self.tabAxes)
        self.autoscaleAltitudesLabel.setObjectName("autoscaleAltitudesLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.autoscaleAltitudesLabel)
        self.autoscaleAltitudesCheckBox = QtWidgets.QCheckBox(parent=self.tabAxes)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.autoscaleAltitudesCheckBox.sizePolicy().hasHeightForWidth())
        self.autoscaleAltitudesCheckBox.setSizePolicy(sizePolicy)
        self.autoscaleAltitudesCheckBox.setMinimumSize(QtCore.QSize(0, 32))
        self.autoscaleAltitudesCheckBox.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.autoscaleAltitudesCheckBox.setObjectName("autoscaleAltitudesCheckBox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.autoscaleAltitudesCheckBox)
        self.showHoursLabel = QtWidgets.QLabel(parent=self.tabAxes)
        self.showHoursLabel.setObjectName("showHoursLabel")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.LabelRole, self.showHoursLabel)
        self.showHoursCheckBox = QtWidgets.QCheckBox(parent=self.tabAxes)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.showHoursCheckBox.sizePolicy().hasHeightForWidth())
        self.showHoursCheckBox.setSizePolicy(sizePolicy)
        self.showHoursCheckBox.setMinimumSize(QtCore.QSize(0, 32))
        self.showHoursCheckBox.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.showHoursCheckBox.setObjectName("showHoursCheckBox")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.FieldRole, self.showHoursCheckBox)
        self.absoluteTimeLabel = QtWidgets.QLabel(parent=self.tabAxes)
        self.absoluteTimeLabel.setObjectName("absoluteTimeLabel")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.ItemRole.LabelRole, self.absoluteTimeLabel)
        self.absoluteTimeCheckBox = QtWidgets.QCheckBox(parent=self.tabAxes)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.absoluteTimeCheckBox.sizePolicy().hasHeightForWidth())
        self.absoluteTimeCheckBox.setSizePolicy(sizePolicy)
        self.absoluteTimeCheckBox.setMinimumSize(QtCore.QSize(0, 32))
        self.absoluteTimeCheckBox.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.absoluteTimeCheckBox.setObjectName("absoluteTimeCheckBox")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.ItemRole.FieldRole, self.absoluteTimeCheckBox)
        self.verticalLayout_2.addLayout(self.formLayout)
        self.groupBox_2 = QtWidgets.QGroupBox(parent=self.tabAxes)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout.setObjectName("gridLayout")
        self.fontFamilyBox = QtWidgets.QFontComboBox(parent=self.groupBox_2)
        self.fontFamilyBox.setObjectName("fontFamilyBox")
        self.gridLayout.addWidget(self.fontFamilyBox, 0, 0, 1, 2)
        self.fontSizeSpinBox = QtWidgets.QSpinBox(parent=self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fontSizeSpinBox.sizePolicy().hasHeightForWidth())
        self.fontSizeSpinBox.setSizePolicy(sizePolicy)
        self.fontSizeSpinBox.setMinimum(1)
        self.fontSizeSpinBox.setObjectName("fontSizeSpinBox")
        self.gridLayout.addWidget(self.fontSizeSpinBox, 0, 2, 1, 1)
        self.boldFontLabel = QtWidgets.QLabel(parent=self.groupBox_2)
        self.boldFontLabel.setObjectName("boldFontLabel")
        self.gridLayout.addWidget(self.boldFontLabel, 1, 0, 1, 1)
        self.boldFontCheckBox = QtWidgets.QCheckBox(parent=self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.boldFontCheckBox.sizePolicy().hasHeightForWidth())
        self.boldFontCheckBox.setSizePolicy(sizePolicy)
        self.boldFontCheckBox.setMinimumSize(QtCore.QSize(0, 32))
        self.boldFontCheckBox.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.boldFontCheckBox.setObjectName("boldFontCheckBox")
        self.gridLayout.addWidget(self.boldFontCheckBox, 1, 1, 1, 2)
        self.italicFontLabel = QtWidgets.QLabel(parent=self.groupBox_2)
        self.italicFontLabel.setObjectName("italicFontLabel")
        self.gridLayout.addWidget(self.italicFontLabel, 2, 0, 1, 1)
        self.italicFontCheckBox = QtWidgets.QCheckBox(parent=self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.italicFontCheckBox.sizePolicy().hasHeightForWidth())
        self.italicFontCheckBox.setSizePolicy(sizePolicy)
        self.italicFontCheckBox.setMinimumSize(QtCore.QSize(0, 32))
        self.italicFontCheckBox.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.italicFontCheckBox.setObjectName("italicFontCheckBox")
        self.gridLayout.addWidget(self.italicFontCheckBox, 2, 1, 1, 2)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        spacerItem5 = QtWidgets.QSpacerItem(20, 14, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_2.addItem(spacerItem5)
        self.tabWidget.addTab(self.tabAxes, "")
        self.tabSettings = QtWidgets.QWidget()
        self.tabSettings.setObjectName("tabSettings")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tabSettings)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setLabelAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.formLayout_2.setFormAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTop|QtCore.Qt.AlignmentFlag.AlignTrailing)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_8 = QtWidgets.QLabel(parent=self.tabSettings)
        self.label_8.setObjectName("label_8")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_8)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem6)
        self.distanceCoeffSpinBox = QtWidgets.QDoubleSpinBox(parent=self.tabSettings)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.distanceCoeffSpinBox.sizePolicy().hasHeightForWidth())
        self.distanceCoeffSpinBox.setSizePolicy(sizePolicy)
        self.distanceCoeffSpinBox.setMaximumSize(QtCore.QSize(120, 16777215))
        self.distanceCoeffSpinBox.setDecimals(1)
        self.distanceCoeffSpinBox.setMinimum(0.1)
        self.distanceCoeffSpinBox.setSingleStep(0.1)
        self.distanceCoeffSpinBox.setObjectName("distanceCoeffSpinBox")
        self.horizontalLayout_7.addWidget(self.distanceCoeffSpinBox)
        self.formLayout_2.setLayout(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.horizontalLayout_7)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem7 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem7)
        self.showCoefficientLabel = QtWidgets.QLabel(parent=self.tabSettings)
        self.showCoefficientLabel.setObjectName("showCoefficientLabel")
        self.horizontalLayout_5.addWidget(self.showCoefficientLabel)
        self.formLayout_2.setLayout(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.horizontalLayout_5)
        self.showCoefficientCheckBox = QtWidgets.QCheckBox(parent=self.tabSettings)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.showCoefficientCheckBox.sizePolicy().hasHeightForWidth())
        self.showCoefficientCheckBox.setSizePolicy(sizePolicy)
        self.showCoefficientCheckBox.setMinimumSize(QtCore.QSize(0, 32))
        self.showCoefficientCheckBox.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.showCoefficientCheckBox.setObjectName("showCoefficientCheckBox")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.showCoefficientCheckBox)
        self.label_10 = QtWidgets.QLabel(parent=self.tabSettings)
        self.label_10.setObjectName("label_10")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_10)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem8)
        self.timezoneSpinBox = QtWidgets.QSpinBox(parent=self.tabSettings)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.timezoneSpinBox.sizePolicy().hasHeightForWidth())
        self.timezoneSpinBox.setSizePolicy(sizePolicy)
        self.timezoneSpinBox.setMaximumSize(QtCore.QSize(120, 16777215))
        self.timezoneSpinBox.setMinimum(-999)
        self.timezoneSpinBox.setMaximum(999)
        self.timezoneSpinBox.setObjectName("timezoneSpinBox")
        self.horizontalLayout_8.addWidget(self.timezoneSpinBox)
        self.formLayout_2.setLayout(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.horizontalLayout_8)
        self.sortByTimeLabel = QtWidgets.QLabel(parent=self.tabSettings)
        self.sortByTimeLabel.setObjectName("sortByTimeLabel")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.ItemRole.LabelRole, self.sortByTimeLabel)
        self.sortByTimeCheckBox = QtWidgets.QCheckBox(parent=self.tabSettings)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sortByTimeCheckBox.sizePolicy().hasHeightForWidth())
        self.sortByTimeCheckBox.setSizePolicy(sizePolicy)
        self.sortByTimeCheckBox.setMinimumSize(QtCore.QSize(0, 32))
        self.sortByTimeCheckBox.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.sortByTimeCheckBox.setObjectName("sortByTimeCheckBox")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.ItemRole.FieldRole, self.sortByTimeCheckBox)
        self.label_11 = QtWidgets.QLabel(parent=self.tabSettings)
        self.label_11.setObjectName("label_11")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_11)
        self.nameTagBox = QtWidgets.QComboBox(parent=self.tabSettings)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nameTagBox.sizePolicy().hasHeightForWidth())
        self.nameTagBox.setSizePolicy(sizePolicy)
        self.nameTagBox.setObjectName("nameTagBox")
        self.nameTagBox.addItem("")
        self.nameTagBox.addItem("")
        self.nameTagBox.addItem("")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.ItemRole.FieldRole, self.nameTagBox)
        self.verticalLayout_3.addLayout(self.formLayout_2)
        self.groupBox = QtWidgets.QGroupBox(parent=self.tabSettings)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.coordinateBox = QtWidgets.QComboBox(parent=self.groupBox)
        self.coordinateBox.setObjectName("coordinateBox")
        self.coordinateBox.addItem("")
        self.coordinateBox.addItem("")
        self.coordinateBox.addItem("")
        self.horizontalLayout.addWidget(self.coordinateBox)
        self.verticalLayout_3.addWidget(self.groupBox)
        spacerItem9 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_3.addItem(spacerItem9)
        self.tabWidget.addTab(self.tabSettings, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.formLayout_4 = QtWidgets.QFormLayout()
        self.formLayout_4.setLabelAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.formLayout_4.setFormAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTop|QtCore.Qt.AlignmentFlag.AlignTrailing)
        self.formLayout_4.setObjectName("formLayout_4")
        self.pointsToTrackLabel = QtWidgets.QLabel(parent=self.tab)
        self.pointsToTrackLabel.setObjectName("pointsToTrackLabel")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.pointsToTrackLabel)
        self.pointsToTrackCheckBox = QtWidgets.QCheckBox(parent=self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pointsToTrackCheckBox.sizePolicy().hasHeightForWidth())
        self.pointsToTrackCheckBox.setSizePolicy(sizePolicy)
        self.pointsToTrackCheckBox.setMinimumSize(QtCore.QSize(0, 32))
        self.pointsToTrackCheckBox.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.pointsToTrackCheckBox.setObjectName("pointsToTrackCheckBox")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.pointsToTrackCheckBox)
        self.deletePointsLabel = QtWidgets.QLabel(parent=self.tab)
        self.deletePointsLabel.setObjectName("deletePointsLabel")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.deletePointsLabel)
        self.deletePointsCheckBox = QtWidgets.QCheckBox(parent=self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.deletePointsCheckBox.sizePolicy().hasHeightForWidth())
        self.deletePointsCheckBox.setSizePolicy(sizePolicy)
        self.deletePointsCheckBox.setMinimumSize(QtCore.QSize(0, 32))
        self.deletePointsCheckBox.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.deletePointsCheckBox.setObjectName("deletePointsCheckBox")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.deletePointsCheckBox)
        self.tracksToPointsLabel = QtWidgets.QLabel(parent=self.tab)
        self.tracksToPointsLabel.setObjectName("tracksToPointsLabel")
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.tracksToPointsLabel)
        self.tracksToPointsCheckBox = QtWidgets.QCheckBox(parent=self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tracksToPointsCheckBox.sizePolicy().hasHeightForWidth())
        self.tracksToPointsCheckBox.setSizePolicy(sizePolicy)
        self.tracksToPointsCheckBox.setMinimumSize(QtCore.QSize(0, 32))
        self.tracksToPointsCheckBox.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.tracksToPointsCheckBox.setObjectName("tracksToPointsCheckBox")
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.tracksToPointsCheckBox)
        self.deleteTracksLabel = QtWidgets.QLabel(parent=self.tab)
        self.deleteTracksLabel.setObjectName("deleteTracksLabel")
        self.formLayout_4.setWidget(3, QtWidgets.QFormLayout.ItemRole.LabelRole, self.deleteTracksLabel)
        self.deleteTracksCheckBox = QtWidgets.QCheckBox(parent=self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.deleteTracksCheckBox.sizePolicy().hasHeightForWidth())
        self.deleteTracksCheckBox.setSizePolicy(sizePolicy)
        self.deleteTracksCheckBox.setMinimumSize(QtCore.QSize(0, 32))
        self.deleteTracksCheckBox.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.deleteTracksCheckBox.setObjectName("deleteTracksCheckBox")
        self.formLayout_4.setWidget(3, QtWidgets.QFormLayout.ItemRole.FieldRole, self.deleteTracksCheckBox)
        self.verticalLayout_5.addLayout(self.formLayout_4)
        spacerItem10 = QtWidgets.QSpacerItem(20, 210, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_5.addItem(spacerItem10)
        self.tabWidget.addTab(self.tab, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=settingsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(settingsDialog)
        self.tabWidget.setCurrentIndex(0)
        self.buttonBox.accepted.connect(settingsDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(settingsDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(settingsDialog)

    def retranslateUi(self, settingsDialog):
        _translate = QtCore.QCoreApplication.translate
        settingsDialog.setWindowTitle(_translate("settingsDialog", "Settings"))
        self.profileColorButton.setText(_translate("settingsDialog", "Profile color"))
        self.fillColorButton.setText(_translate("settingsDialog", "Fill color"))
        self.profileWidthLabel.setText(_translate("settingsDialog", "Profile width"))
        self.useSystemThemeLabel.setToolTip(_translate("settingsDialog", "Use system color theme instead of default light theme"))
        self.useSystemThemeLabel.setText(_translate("settingsDialog", "Use system theme"))
        self.useSystemThemeCheckBox.setToolTip(_translate("settingsDialog", "Use system color theme instead of default light theme"))
        self.selectedPointsLabel.setToolTip(_translate("settingsDialog", "Plot profiles taking into account only selected points and tracks"))
        self.selectedPointsLabel.setText(_translate("settingsDialog", "Use only selected points"))
        self.selectedPointsCheckBox.setToolTip(_translate("settingsDialog", "Plot profiles taking into account only selected points and tracks"))
        self.startFromZeroLabel.setToolTip(_translate("settingsDialog", "Always start X axis from zero when plotting profile for selected points"))
        self.startFromZeroLabel.setText(_translate("settingsDialog", "Start from zero"))
        self.startFromZeroCheckBox.setToolTip(_translate("settingsDialog", "Always start X axis from zero when plotting profile for selected points"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabProfile), _translate("settingsDialog", "Profile style"))
        self.minaltLabel.setText(_translate("settingsDialog", "Minimum altitude"))
        self.maxaltLabel.setText(_translate("settingsDialog", "Maximum altitude"))
        self.autoscaleAltitudesLabel.setToolTip(_translate("settingsDialog", "Automatically scale minimum/maximum altitudes when plotting profile"))
        self.autoscaleAltitudesLabel.setText(_translate("settingsDialog", "Autoscale altitudes"))
        self.autoscaleAltitudesCheckBox.setToolTip(_translate("settingsDialog", "Automatically scale minimum/maximum altitudes when plotting profile"))
        self.showHoursLabel.setToolTip(_translate("settingsDialog", "Allow showing hours along with days under the X axis.\n"
"Otherwise only days or hours are shown."))
        self.showHoursLabel.setText(_translate("settingsDialog", "Show hours"))
        self.showHoursCheckBox.setToolTip(_translate("settingsDialog", "Allow showing hours along with days under the X axis.\n"
"Otherwise only days or hours are shown."))
        self.absoluteTimeLabel.setToolTip(_translate("settingsDialog", "Show absolute time of track instead of track duration"))
        self.absoluteTimeLabel.setText(_translate("settingsDialog", "Absolute time"))
        self.absoluteTimeCheckBox.setToolTip(_translate("settingsDialog", "Show absolute time of track instead of track duration"))
        self.groupBox_2.setTitle(_translate("settingsDialog", "Axes labels font"))
        self.fontFamilyBox.setToolTip(_translate("settingsDialog", "The font family used for axes labels and points captions"))
        self.fontSizeSpinBox.setToolTip(_translate("settingsDialog", "Font size"))
        self.boldFontLabel.setToolTip(_translate("settingsDialog", "Whether to use bold font for axes labels"))
        self.boldFontLabel.setText(_translate("settingsDialog", "Bold font"))
        self.boldFontCheckBox.setToolTip(_translate("settingsDialog", "Whether to use bold font for axes labels"))
        self.italicFontLabel.setToolTip(_translate("settingsDialog", "Whether to use italic font for axes labels"))
        self.italicFontLabel.setText(_translate("settingsDialog", "Italic font"))
        self.italicFontCheckBox.setToolTip(_translate("settingsDialog", "Whether to use italic font for axes labels"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabAxes), _translate("settingsDialog", "Axes style"))
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
        self.sortByTimeLabel.setToolTip(_translate("settingsDialog", "Sort imported points by time"))
        self.sortByTimeLabel.setText(_translate("settingsDialog", "Sort by time"))
        self.sortByTimeCheckBox.setToolTip(_translate("settingsDialog", "Sort imported points by time"))
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
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSettings), _translate("settingsDialog", "Import settings"))
        self.pointsToTrackLabel.setToolTip(_translate("settingsDialog", "Convert waypoints to track when exporting"))
        self.pointsToTrackLabel.setText(_translate("settingsDialog", "Convert points to track"))
        self.pointsToTrackCheckBox.setToolTip(_translate("settingsDialog", "Convert waypoints to track when exporting"))
        self.deletePointsLabel.setToolTip(_translate("settingsDialog", "Delete waypoints when exporting"))
        self.deletePointsLabel.setText(_translate("settingsDialog", "Delete points"))
        self.deletePointsCheckBox.setToolTip(_translate("settingsDialog", "Delete waypoints when exporting"))
        self.tracksToPointsLabel.setToolTip(_translate("settingsDialog", "Convert tracks to waypoints when exporting"))
        self.tracksToPointsLabel.setText(_translate("settingsDialog", "Convert tracks to points"))
        self.tracksToPointsCheckBox.setToolTip(_translate("settingsDialog", "Convert tracks to waypoints when exporting"))
        self.deleteTracksLabel.setToolTip(_translate("settingsDialog", "Delete tracks when exporting"))
        self.deleteTracksLabel.setText(_translate("settingsDialog", "Delete tracks"))
        self.deleteTracksCheckBox.setToolTip(_translate("settingsDialog", "Delete tracks when exporting"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("settingsDialog", "Export settings"))
from gpxviewer.colorchooser import ColorChooser
