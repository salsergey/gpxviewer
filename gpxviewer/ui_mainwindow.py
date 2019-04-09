# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 768)
        MainWindow.setWindowTitle("GPX Viewer")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setTabBarAutoHide(True)
        self.tabWidget.setObjectName("tabWidget")
        self.wptTab = QtWidgets.QWidget()
        self.wptTab.setObjectName("wptTab")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.wptTab)
        self.verticalLayout.setObjectName("verticalLayout")
        self.wptView = QtWidgets.QTableView(self.wptTab)
        self.wptView.setEnabled(False)
        self.wptView.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked|QtWidgets.QAbstractItemView.EditKeyPressed)
        self.wptView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.wptView.setObjectName("wptView")
        self.wptView.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.wptView)
        self.tabWidget.addTab(self.wptTab, "")
        self.trkTab = QtWidgets.QWidget()
        self.trkTab.setObjectName("trkTab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.trkTab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.trkView = QtWidgets.QTableView(self.trkTab)
        self.trkView.setEnabled(False)
        self.trkView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.trkView.setObjectName("trkView")
        self.trkView.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout_3.addWidget(self.trkView)
        self.tabWidget.addTab(self.trkTab, "")
        self.verticalLayout_2.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1024, 30))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuRecentProjects = QtWidgets.QMenu(self.menuFile)
        self.menuRecentProjects.setObjectName("menuRecentProjects")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuFilter = QtWidgets.QMenu(self.menubar)
        self.menuFilter.setObjectName("menuFilter")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        MainWindow.setMenuBar(self.menubar)
        self.fileToolBar = QtWidgets.QToolBar(MainWindow)
        self.fileToolBar.setMovable(False)
        self.fileToolBar.setAllowedAreas(QtCore.Qt.TopToolBarArea)
        self.fileToolBar.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.fileToolBar.setObjectName("fileToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.fileToolBar)
        self.toolsToolBar = QtWidgets.QToolBar(MainWindow)
        self.toolsToolBar.setMovable(False)
        self.toolsToolBar.setAllowedAreas(QtCore.Qt.TopToolBarArea)
        self.toolsToolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolsToolBar.setObjectName("toolsToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolsToolBar)
        self.filterToolBar = QtWidgets.QToolBar(MainWindow)
        self.filterToolBar.setMovable(False)
        self.filterToolBar.setAllowedAreas(QtCore.Qt.TopToolBarArea)
        self.filterToolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.filterToolBar.setObjectName("filterToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.filterToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.actionQuit = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("."), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionQuit.setIcon(icon)
        self.actionQuit.setShortcutContext(QtCore.Qt.ApplicationShortcut)
        self.actionQuit.setObjectName("actionQuit")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setIcon(icon)
        self.actionOpen.setObjectName("actionOpen")
        self.actionAboutQt = QtWidgets.QAction(MainWindow)
        self.actionAboutQt.setObjectName("actionAboutQt")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setIcon(icon)
        self.actionSave.setObjectName("actionSave")
        self.actionSaveAs = QtWidgets.QAction(MainWindow)
        self.actionSaveAs.setIcon(icon)
        self.actionSaveAs.setObjectName("actionSaveAs")
        self.actionLoadGPXfile = QtWidgets.QAction(MainWindow)
        self.actionLoadGPXfile.setIcon(icon)
        self.actionLoadGPXfile.setShortcut("Ctrl+L")
        self.actionLoadGPXfile.setObjectName("actionLoadGPXfile")
        self.actionDistanceProfile = QtWidgets.QAction(MainWindow)
        self.actionDistanceProfile.setIcon(icon)
        self.actionDistanceProfile.setShortcut("Ctrl+P")
        self.actionDistanceProfile.setObjectName("actionDistanceProfile")
        self.actionTimeProfile = QtWidgets.QAction(MainWindow)
        self.actionTimeProfile.setIcon(icon)
        self.actionTimeProfile.setShortcut("Ctrl+T")
        self.actionTimeProfile.setObjectName("actionTimeProfile")
        self.actionSettings = QtWidgets.QAction(MainWindow)
        self.actionSettings.setIcon(icon)
        self.actionSettings.setObjectName("actionSettings")
        self.actionShowSkipped = QtWidgets.QAction(MainWindow)
        self.actionShowSkipped.setCheckable(True)
        self.actionShowSkipped.setObjectName("actionShowSkipped")
        self.actionShowMarked = QtWidgets.QAction(MainWindow)
        self.actionShowMarked.setCheckable(True)
        self.actionShowMarked.setObjectName("actionShowMarked")
        self.actionShowCaptioned = QtWidgets.QAction(MainWindow)
        self.actionShowCaptioned.setCheckable(True)
        self.actionShowCaptioned.setObjectName("actionShowCaptioned")
        self.actionShowOther = QtWidgets.QAction(MainWindow)
        self.actionShowOther.setCheckable(True)
        self.actionShowOther.setObjectName("actionShowOther")
        self.actionGpxViewerHelp = QtWidgets.QAction(MainWindow)
        self.actionGpxViewerHelp.setShortcut("F1")
        self.actionGpxViewerHelp.setObjectName("actionGpxViewerHelp")
        self.actionAboutGPXViewer = QtWidgets.QAction(MainWindow)
        self.actionAboutGPXViewer.setObjectName("actionAboutGPXViewer")
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setIcon(icon)
        self.actionNew.setObjectName("actionNew")
        self.actionStatistics = QtWidgets.QAction(MainWindow)
        self.actionStatistics.setIcon(icon)
        self.actionStatistics.setShortcut("Ctrl+I")
        self.actionStatistics.setObjectName("actionStatistics")
        self.actionSaveGPXfileAs = QtWidgets.QAction(MainWindow)
        self.actionSaveGPXfileAs.setObjectName("actionSaveGPXfileAs")
        self.actionClearList = QtWidgets.QAction(MainWindow)
        self.actionClearList.setObjectName("actionClearList")
        self.actionShowMarkedCaptioned = QtWidgets.QAction(MainWindow)
        self.actionShowMarkedCaptioned.setCheckable(True)
        self.actionShowMarkedCaptioned.setObjectName("actionShowMarkedCaptioned")
        self.actionResetFilters = QtWidgets.QAction(MainWindow)
        self.actionResetFilters.setObjectName("actionResetFilters")
        self.menuRecentProjects.addAction(self.actionClearList)
        self.menuFile.addAction(self.actionLoadGPXfile)
        self.menuFile.addAction(self.actionSaveGPXfileAs)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSaveAs)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.menuRecentProjects.menuAction())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuHelp.addAction(self.actionGpxViewerHelp)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAboutQt)
        self.menuHelp.addAction(self.actionAboutGPXViewer)
        self.menuFilter.addAction(self.actionShowSkipped)
        self.menuFilter.addAction(self.actionShowMarked)
        self.menuFilter.addAction(self.actionShowCaptioned)
        self.menuFilter.addAction(self.actionShowMarkedCaptioned)
        self.menuFilter.addAction(self.actionShowOther)
        self.menuFilter.addSeparator()
        self.menuFilter.addAction(self.actionResetFilters)
        self.menuTools.addAction(self.actionDistanceProfile)
        self.menuTools.addAction(self.actionTimeProfile)
        self.menuTools.addAction(self.actionStatistics)
        self.menuTools.addSeparator()
        self.menuTools.addAction(self.actionSettings)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuFilter.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.fileToolBar.addAction(self.actionLoadGPXfile)
        self.fileToolBar.addAction(self.actionNew)
        self.fileToolBar.addAction(self.actionOpen)
        self.fileToolBar.addAction(self.actionSave)
        self.fileToolBar.addAction(self.actionSaveAs)
        self.fileToolBar.addSeparator()
        self.toolsToolBar.addAction(self.actionSettings)
        self.toolsToolBar.addSeparator()
        self.toolsToolBar.addAction(self.actionDistanceProfile)
        self.toolsToolBar.addAction(self.actionTimeProfile)
        self.toolsToolBar.addAction(self.actionStatistics)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.actionQuit.triggered.connect(MainWindow.close)
        self.actionOpen.triggered.connect(MainWindow.fileOpen)
        self.actionAboutQt.triggered.connect(MainWindow.aboutQt)
        self.actionDistanceProfile.triggered.connect(MainWindow.plotDistanceProfile)
        self.actionTimeProfile.triggered.connect(MainWindow.plotTimeProfile)
        self.actionSave.triggered.connect(MainWindow.fileSave)
        self.actionSaveAs.triggered.connect(MainWindow.fileSaveAs)
        self.actionLoadGPXfile.triggered.connect(MainWindow.fileLoadGPXFile)
        self.actionSettings.triggered.connect(MainWindow.showSettings)
        self.actionShowSkipped.toggled['bool'].connect(MainWindow.showSkipped)
        self.actionShowMarked.toggled['bool'].connect(MainWindow.showMarked)
        self.actionShowOther.toggled['bool'].connect(MainWindow.showOther)
        self.actionShowCaptioned.toggled['bool'].connect(MainWindow.showCaptioned)
        self.actionGpxViewerHelp.triggered.connect(MainWindow.gpxViewerHelp)
        self.actionAboutGPXViewer.triggered.connect(MainWindow.aboutGPXViewer)
        self.actionNew.triggered.connect(MainWindow.fileNew)
        self.actionStatistics.triggered.connect(MainWindow.showStatistics)
        self.actionSaveGPXfileAs.triggered.connect(MainWindow.fileSaveGPXFileAs)
        self.actionClearList.triggered.connect(MainWindow.clearRecentList)
        self.actionShowMarkedCaptioned.toggled['bool'].connect(MainWindow.showMarkedCaptioned)
        self.actionResetFilters.triggered.connect(MainWindow.resetFilters)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.wptTab), _translate("MainWindow", "Waypoints"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.trkTab), _translate("MainWindow", "Tracks"))
        self.menuFile.setTitle(_translate("MainWindow", "&File"))
        self.menuRecentProjects.setTitle(_translate("MainWindow", "&Recent projects"))
        self.menuHelp.setTitle(_translate("MainWindow", "&Help"))
        self.menuFilter.setTitle(_translate("MainWindow", "F&ilter"))
        self.menuTools.setTitle(_translate("MainWindow", "&Tools"))
        self.fileToolBar.setWindowTitle(_translate("MainWindow", "File"))
        self.toolsToolBar.setWindowTitle(_translate("MainWindow", "Tools"))
        self.filterToolBar.setWindowTitle(_translate("MainWindow", "Filter"))
        self.actionQuit.setText(_translate("MainWindow", "&Quit"))
        self.actionOpen.setText(_translate("MainWindow", "&Open project"))
        self.actionAboutQt.setText(_translate("MainWindow", "&About Qt"))
        self.actionSave.setText(_translate("MainWindow", "&Save project"))
        self.actionSaveAs.setText(_translate("MainWindow", "Save project &as..."))
        self.actionLoadGPXfile.setText(_translate("MainWindow", "&Load GPX file"))
        self.actionDistanceProfile.setText(_translate("MainWindow", "&Distance profile"))
        self.actionTimeProfile.setText(_translate("MainWindow", "&Time profile"))
        self.actionSettings.setText(_translate("MainWindow", "&Settings..."))
        self.actionShowSkipped.setText(_translate("MainWindow", "&Show skipped"))
        self.actionShowMarked.setText(_translate("MainWindow", "Show &marked only"))
        self.actionShowCaptioned.setText(_translate("MainWindow", "Show &captioned only"))
        self.actionShowOther.setText(_translate("MainWindow", "Show &other"))
        self.actionGpxViewerHelp.setText(_translate("MainWindow", "GPX Viewer &Help"))
        self.actionAboutGPXViewer.setText(_translate("MainWindow", "About &GPX Viewer"))
        self.actionNew.setText(_translate("MainWindow", "&New project"))
        self.actionStatistics.setText(_translate("MainWindow", "&Statistics"))
        self.actionSaveGPXfileAs.setText(_translate("MainWindow", "Save &GPX file as..."))
        self.actionClearList.setText(_translate("MainWindow", "&Clear list"))
        self.actionShowMarkedCaptioned.setText(_translate("MainWindow", "Show marked &and captioned"))
        self.actionResetFilters.setText(_translate("MainWindow", "&Reset filters"))


