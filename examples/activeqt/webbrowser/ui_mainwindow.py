# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Tue Oct 31 21:22:31 2006
#      by: PyQt4 UI code generator 4-snapshot-20061029
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,812,605).size()).expandedTo(MainWindow.minimumSizeHint()))

        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")

        self.hboxlayout = QtGui.QHBoxLayout(self.centralWidget)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.Frame3 = QtGui.QFrame(self.centralWidget)
        self.Frame3.setFrameShape(QtGui.QFrame.StyledPanel)
        self.Frame3.setFrameShadow(QtGui.QFrame.Sunken)
        self.Frame3.setObjectName("Frame3")

        self.vboxlayout = QtGui.QVBoxLayout(self.Frame3)
        self.vboxlayout.setMargin(1)
        self.vboxlayout.setSpacing(0)
        self.vboxlayout.setObjectName("vboxlayout")

        self.WebBrowser = QAxContainer.QAxWidget(self.Frame3)
        self.WebBrowser.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.WebBrowser.setControl("{8856F961-340A-11D0-A96B-00C04FD705A2}")
        self.WebBrowser.setObjectName("WebBrowser")
        self.vboxlayout.addWidget(self.WebBrowser)
        self.hboxlayout.addWidget(self.Frame3)
        MainWindow.setCentralWidget(self.centralWidget)

        self.tbNavigate = QtGui.QToolBar(MainWindow)
        self.tbNavigate.setOrientation(QtCore.Qt.Horizontal)
        self.tbNavigate.setObjectName("tbNavigate")
        MainWindow.addToolBar(self.tbNavigate)

        self.tbAddress = QtGui.QToolBar(MainWindow)
        self.tbAddress.setOrientation(QtCore.Qt.Horizontal)
        self.tbAddress.setObjectName("tbAddress")
        MainWindow.addToolBar(self.tbAddress)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,812,26))
        self.menubar.setObjectName("menubar")

        self.PopupMenu = QtGui.QMenu(self.menubar)
        self.PopupMenu.setObjectName("PopupMenu")

        self.FileNewGroup_2 = QtGui.QMenu(self.PopupMenu)
        self.FileNewGroup_2.setObjectName("FileNewGroup_2")

        self.unnamed = QtGui.QMenu(self.menubar)
        self.unnamed.setObjectName("unnamed")
        MainWindow.setMenuBar(self.menubar)

        self.actionGo = QtGui.QAction(MainWindow)
        self.actionGo.setIcon(QtGui.QIcon(":/icons/image0.xpm"))
        self.actionGo.setObjectName("actionGo")

        self.actionBack = QtGui.QAction(MainWindow)
        self.actionBack.setIcon(QtGui.QIcon(":/icons/image1.xpm"))
        self.actionBack.setObjectName("actionBack")

        self.actionForward = QtGui.QAction(MainWindow)
        self.actionForward.setIcon(QtGui.QIcon(":/icons/image2.xpm"))
        self.actionForward.setObjectName("actionForward")

        self.actionStop = QtGui.QAction(MainWindow)
        self.actionStop.setIcon(QtGui.QIcon(":/icons/image3.xpm"))
        self.actionStop.setObjectName("actionStop")

        self.actionRefresh = QtGui.QAction(MainWindow)
        self.actionRefresh.setIcon(QtGui.QIcon(":/icons/image4.xpm"))
        self.actionRefresh.setObjectName("actionRefresh")

        self.actionHome = QtGui.QAction(MainWindow)
        self.actionHome.setIcon(QtGui.QIcon(":/icons/image5.xpm"))
        self.actionHome.setObjectName("actionHome")

        self.actionFileClose = QtGui.QAction(MainWindow)
        self.actionFileClose.setObjectName("actionFileClose")

        self.actionSearch = QtGui.QAction(MainWindow)
        self.actionSearch.setIcon(QtGui.QIcon(":/icons/image6.xpm"))
        self.actionSearch.setObjectName("actionSearch")

        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")

        self.actionAboutQt = QtGui.QAction(MainWindow)
        self.actionAboutQt.setObjectName("actionAboutQt")

        self.FileNewGroup = QtGui.QActionGroup(MainWindow)
        self.FileNewGroup.setObjectName("FileNewGroup")

        self.actionNewWindow = QtGui.QAction(self.FileNewGroup)
        self.actionNewWindow.setObjectName("actionNewWindow")
        self.tbNavigate.addAction(self.actionBack)
        self.tbNavigate.addAction(self.actionForward)
        self.tbNavigate.addAction(self.actionStop)
        self.tbNavigate.addAction(self.actionRefresh)
        self.tbNavigate.addAction(self.actionHome)
        self.tbNavigate.addSeparator()
        self.tbNavigate.addAction(self.actionSearch)
        self.tbAddress.addAction(self.actionGo)
        self.FileNewGroup_2.addAction(self.actionNewWindow)
        self.PopupMenu.addAction(self.FileNewGroup_2.menuAction())
        self.PopupMenu.addSeparator()
        self.PopupMenu.addAction(self.actionFileClose)
        self.unnamed.addAction(self.actionAbout)
        self.unnamed.addAction(self.actionAboutQt)
        self.menubar.addAction(self.PopupMenu.menuAction())
        self.menubar.addAction(self.unnamed.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Qt WebBrowser", None, QtGui.QApplication.UnicodeUTF8))
        self.tbNavigate.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Navigation", None, QtGui.QApplication.UnicodeUTF8))
        self.tbAddress.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Address", None, QtGui.QApplication.UnicodeUTF8))
        self.PopupMenu.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.FileNewGroup_2.setTitle(QtGui.QApplication.translate("MainWindow", "New", None, QtGui.QApplication.UnicodeUTF8))
        self.unnamed.setTitle(QtGui.QApplication.translate("MainWindow", "&Help", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGo.setIconText(QtGui.QApplication.translate("MainWindow", "Go", None, QtGui.QApplication.UnicodeUTF8))
        self.actionBack.setIconText(QtGui.QApplication.translate("MainWindow", "Back", None, QtGui.QApplication.UnicodeUTF8))
        self.actionBack.setShortcut(QtGui.QApplication.translate("MainWindow", "Backspace", None, QtGui.QApplication.UnicodeUTF8))
        self.actionForward.setIconText(QtGui.QApplication.translate("MainWindow", "Forward", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStop.setIconText(QtGui.QApplication.translate("MainWindow", "Stop", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRefresh.setIconText(QtGui.QApplication.translate("MainWindow", "Refresh", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHome.setIconText(QtGui.QApplication.translate("MainWindow", "Home", None, QtGui.QApplication.UnicodeUTF8))
        self.actionFileClose.setText(QtGui.QApplication.translate("MainWindow", "C&lose", None, QtGui.QApplication.UnicodeUTF8))
        self.actionFileClose.setIconText(QtGui.QApplication.translate("MainWindow", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSearch.setIconText(QtGui.QApplication.translate("MainWindow", "Search", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setIconText(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAboutQt.setIconText(QtGui.QApplication.translate("MainWindow", "About Qt", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNewWindow.setIconText(QtGui.QApplication.translate("MainWindow", "Window", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNewWindow.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+N", None, QtGui.QApplication.UnicodeUTF8))

from PyQt4 import QAxContainer
import mainwindow_rc
