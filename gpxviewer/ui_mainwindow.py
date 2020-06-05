# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 768)
        MainWindow.setAcceptDrops(True)
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
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuCoLumns = QtWidgets.QMenu(self.menuEdit)
        self.menuCoLumns.setObjectName("menuCoLumns")
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
        self.actionQuit.setShortcutContext(QtCore.Qt.ApplicationShortcut)
        self.actionQuit.setObjectName("actionQuit")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionAboutQt = QtWidgets.QAction(MainWindow)
        self.actionAboutQt.setObjectName("actionAboutQt")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSaveAs = QtWidgets.QAction(MainWindow)
        self.actionSaveAs.setObjectName("actionSaveAs")
        self.actionLoadGPXfile = QtWidgets.QAction(MainWindow)
        self.actionLoadGPXfile.setShortcut("Ctrl+L")
        self.actionLoadGPXfile.setObjectName("actionLoadGPXfile")
        self.actionDistanceProfile = QtWidgets.QAction(MainWindow)
        self.actionDistanceProfile.setShortcut("Ctrl+P")
        self.actionDistanceProfile.setObjectName("actionDistanceProfile")
        self.actionTimeProfile = QtWidgets.QAction(MainWindow)
        self.actionTimeProfile.setShortcut("Ctrl+T")
        self.actionTimeProfile.setObjectName("actionTimeProfile")
        self.actionSettings = QtWidgets.QAction(MainWindow)
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
        self.actionGpxViewerHelp.setObjectName("actionGpxViewerHelp")
        self.actionAboutGPXViewer = QtWidgets.QAction(MainWindow)
        self.actionAboutGPXViewer.setObjectName("actionAboutGPXViewer")
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionStatistics = QtWidgets.QAction(MainWindow)
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
        self.actionCopy = QtWidgets.QAction(MainWindow)
        self.actionCopy.setObjectName("actionCopy")
        self.actionResetColumns = QtWidgets.QAction(MainWindow)
        self.actionResetColumns.setObjectName("actionResetColumns")
        self.actionDetailedView = QtWidgets.QAction(MainWindow)
        self.actionDetailedView.setCheckable(True)
        self.actionDetailedView.setShortcut("Ctrl+D")
        self.actionDetailedView.setObjectName("actionDetailedView")
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
        self.menuView.addAction(self.actionDetailedView)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionShowSkipped)
        self.menuView.addAction(self.actionShowMarked)
        self.menuView.addAction(self.actionShowCaptioned)
        self.menuView.addAction(self.actionShowMarkedCaptioned)
        self.menuView.addAction(self.actionShowOther)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionResetFilters)
        self.menuTools.addAction(self.actionDistanceProfile)
        self.menuTools.addAction(self.actionTimeProfile)
        self.menuTools.addAction(self.actionStatistics)
        self.menuTools.addSeparator()
        self.menuTools.addAction(self.actionSettings)
        self.menuCoLumns.addAction(self.actionResetColumns)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.menuCoLumns.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
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
        self.actionOpen.triggered.connect(MainWindow.onFileOpen)
        self.actionAboutQt.triggered.connect(MainWindow.onAboutQt)
        self.actionDistanceProfile.triggered.connect(MainWindow.onPlotDistanceProfile)
        self.actionTimeProfile.triggered.connect(MainWindow.onPlotTimeProfile)
        self.actionSave.triggered.connect(MainWindow.onFileSave)
        self.actionSaveAs.triggered.connect(MainWindow.onFileSaveAs)
        self.actionLoadGPXfile.triggered.connect(MainWindow.onFileLoadGPXFile)
        self.actionSettings.triggered.connect(MainWindow.onShowSettings)
        self.actionShowSkipped.toggled['bool'].connect(MainWindow.onShowSkipped)
        self.actionShowMarked.toggled['bool'].connect(MainWindow.onShowMarked)
        self.actionShowOther.toggled['bool'].connect(MainWindow.onShowOther)
        self.actionShowCaptioned.toggled['bool'].connect(MainWindow.onShowCaptioned)
        self.actionGpxViewerHelp.triggered.connect(MainWindow.onGpxViewerHelp)
        self.actionAboutGPXViewer.triggered.connect(MainWindow.onAboutGPXViewer)
        self.actionNew.triggered.connect(MainWindow.onFileNew)
        self.actionStatistics.triggered.connect(MainWindow.onShowStatistics)
        self.actionSaveGPXfileAs.triggered.connect(MainWindow.onFileSaveGPXFileAs)
        self.actionClearList.triggered.connect(MainWindow.onClearRecentList)
        self.actionShowMarkedCaptioned.toggled['bool'].connect(MainWindow.onShowMarkedCaptioned)
        self.actionResetFilters.triggered.connect(MainWindow.onResetFilters)
        self.actionCopy.triggered.connect(MainWindow.onEditCopy)
        self.actionResetColumns.triggered.connect(MainWindow.onResetColumns)
        self.actionDetailedView.triggered.connect(MainWindow.onDetailedView)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.wptTab), _translate("MainWindow", "Waypoints"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.trkTab), _translate("MainWindow", "Tracks"))
        self.menuFile.setTitle(_translate("MainWindow", "&File"))
        self.menuRecentProjects.setTitle(_translate("MainWindow", "&Recent projects"))
        self.menuHelp.setTitle(_translate("MainWindow", "&Help"))
        self.menuView.setTitle(_translate("MainWindow", "&View"))
        self.menuTools.setTitle(_translate("MainWindow", "&Tools"))
        self.menuEdit.setTitle(_translate("MainWindow", "&Edit"))
        self.menuCoLumns.setTitle(_translate("MainWindow", "Co&lumns to be copied"))
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
        self.actionCopy.setText(_translate("MainWindow", "&Copy"))
        self.actionResetColumns.setText(_translate("MainWindow", "&Reset columns"))
        self.actionDetailedView.setText(_translate("MainWindow", "&Detailed view"))
