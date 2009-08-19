#!/usr/bin/env python

#############################################################################
##
## Copyright (C) 2005-2005 Trolltech AS. All rights reserved.
##
## This file is part of the example classes of the Qt Toolkit.
##
## This file may be used under the terms of the GNU General Public
## License version 2.0 as published by the Free Software Foundation
## and appearing in the file LICENSE.GPL included in the packaging of
## this file.  Please review the following information to ensure GNU
## General Public Licensing requirements will be met:
## http://www.trolltech.com/products/qt/opensource.html
##
## If you are unsure which license is appropriate for your use, please
## review the following information:
## http://www.trolltech.com/products/qt/licensing.html or contact the
## sales department at sales@trolltech.com.
##
## This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
## WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
##
#############################################################################

import sys
from PySide import QtCore, QtGui


class IconSizeSpinBox(QtGui.QSpinBox):
    def valueFromText(self, text):
        regExp = QtCore.QRegExp(self.tr("(\\d+)(\\s*[xx]\\s*\\d+)?"))

        if regExp.exactMatch(text):
            return regExp.cap(1).toInt()
        else:
            return 0

    def textFromValue(self, value):
        return self.tr("%1 x %1").arg(value)


class ImageDelegate(QtGui.QItemDelegate):
    def createEditor(self, parent, option, index):
        comboBox = QtGui.QComboBox(parent)
        if index.column() == 1:
            comboBox.addItem(self.tr("Normal"))
            comboBox.addItem(self.tr("Active"))
            comboBox.addItem(self.tr("Disabled"))
        elif index.column() == 2:
            comboBox.addItem(self.tr("Off"))
            comboBox.addItem(self.tr("On"))

        self.connect(comboBox, QtCore.SIGNAL("activated(int)"), self.emitCommitData)

        return comboBox

    def setEditorData(self, editor, index):
        comboBox = editor
        if not comboBox:
            return

        pos = comboBox.findText(index.model().data(index).toString(),
                                QtCore.Qt.MatchExactly)
        comboBox.setCurrentIndex(pos)

    def setModelData(self, editor, model, index):
        comboBox = editor
        if not comboBox:
            return

        model.setData(index, QtCore.QVariant(comboBox.currentText()))

    def emitCommitData(self):
        self.emit(QtCore.SIGNAL("commitData(QWidget *)"), self.sender())


class IconPreviewArea(QtGui.QWidget):
    NumModes = 3
    NumStates = 2
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)

        mainLayout = QtGui.QGridLayout()
        self.setLayout(mainLayout)

        self.icon = QtGui.QIcon()
        self.size = QtCore.QSize()
        self.stateLabels = []
        self.modeLabels = []
        self.pixmapLabels = []

        self.stateLabels.append(self.createHeaderLabel(self.tr("Off")))
        self.stateLabels.append(self.createHeaderLabel(self.tr("On")))

        self.modeLabels.append(self.createHeaderLabel(self.tr("Normal")))
        self.modeLabels.append(self.createHeaderLabel(self.tr("Active")))
        self.modeLabels.append(self.createHeaderLabel(self.tr("Disabled")))

        for j in range(IconPreviewArea.NumStates):
            mainLayout.addWidget(self.stateLabels[j], j + 1, 0)

        for i in range(IconPreviewArea.NumModes):
            mainLayout.addWidget(self.modeLabels[i], 0, i + 1)

            self.pixmapLabels.append([])
            for j in range(IconPreviewArea.NumStates):
                self.pixmapLabels[i].append(self.createPixmapLabel())
                mainLayout.addWidget(self.pixmapLabels[i][j], j + 1, i + 1)

    def setIcon(self, icon):
        self.icon = icon
        self.updatePixmapLabels()

    def setSize(self, size):
        if size != self.size:
            self.size = size
            self.updatePixmapLabels()

    def createHeaderLabel(self, text):
        label = QtGui.QLabel(self.tr("<b>%1</b>").arg(text))
        label.setAlignment(QtCore.Qt.AlignCenter)
        return label

    def createPixmapLabel(self):
        label = QtGui.QLabel()
        label.setEnabled(False)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setFrameShape(QtGui.QFrame.Box)
        label.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        label.setBackgroundRole(QtGui.QPalette.Base)
        label.setMinimumSize(132, 132)
        return label

    def updatePixmapLabels(self):
        for i in range(IconPreviewArea.NumModes):
            if i == 0:
                mode = QtGui.QIcon.Normal
            elif i == 1:
                mode = QtGui.QIcon.Active
            else:
                mode = QtGui.QIcon.Disabled

            for j in range(IconPreviewArea.NumStates):
                state = {True: QtGui.QIcon.Off, False: QtGui.QIcon.On}[j == 0]
                pixmap = self.icon.pixmap(self.size, mode, state)
                self.pixmapLabels[i][j].setPixmap(pixmap)
                self.pixmapLabels[i][j].setEnabled(not pixmap.isNull())


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)

        self.centralWidget = QtGui.QWidget()
        self.setCentralWidget(self.centralWidget)

        self.createPreviewGroupBox()
        self.createImagesGroupBox()
        self.createIconSizeGroupBox()

        self.createActions()
        self.createMenus()
        self.createContextMenu()

        mainLayout = QtGui.QGridLayout()
        mainLayout.addWidget(self.imagesGroupBox, 0, 0)
        mainLayout.addWidget(self.iconSizeGroupBox, 1, 0)
        mainLayout.addWidget(self.previewGroupBox, 0, 1, 2, 1)
        self.centralWidget.setLayout(mainLayout)

        self.setWindowTitle(self.tr("Icons"))
        self.checkCurrentStyle()
        self.otherRadioButton.click()

        self.resize(860, 400)

    def about(self):
        QtGui.QMessageBox.about(self, self.tr("About Icons"), self.tr(
            "The <b>Icons</b> example illustrates how Qt renders an icon in "
            "different modes (active, normal, and disabled) and states (on "
            "and off) based on a set of images."))

    def changeStyle(self, checked):
        if not checked:
            return

        action = self.sender()
        style = QtGui.QStyleFactory.create(action.data().toString())
        QtGui.QApplication.setStyle(style)

        self.smallRadioButton.setText(self.tr("Small (%1 x %1)")
                .arg(style.pixelMetric(QtGui.QStyle.PM_SmallIconSize)))
        self.largeRadioButton.setText(self.tr("Large (%1 x %1)")
                .arg(style.pixelMetric(QtGui.QStyle.PM_LargeIconSize)))
        self.toolBarRadioButton.setText(self.tr("Toolbars (%1 x %1)")
                .arg(style.pixelMetric(QtGui.QStyle.PM_ToolBarIconSize)))
        self.listViewRadioButton.setText(self.tr("List views (%1 x %1)")
                .arg(style.pixelMetric(QtGui.QStyle.PM_ListViewIconSize)))
        self.iconViewRadioButton.setText(self.tr("Icon views (%1 x %1)")
                .arg(style.pixelMetric(QtGui.QStyle.PM_IconViewIconSize)))

        self.changeSize()

    def changeSize(self):
        if self.otherRadioButton.isChecked():
            extent = self.otherSpinBox.value()
        else:
            if self.smallRadioButton.isChecked():
                metric = QtGui.QStyle.PM_SmallIconSize
            elif self.largeRadioButton.isChecked():
                metric = QtGui.QStyle.PM_LargeIconSize
            elif self.toolBarRadioButton.isChecked():
                metric = QtGui.QStyle.PM_ToolBarIconSize
            elif self.listViewRadioButton.isChecked():
                metric = QtGui.QStyle.PM_ListViewIconSize
            else:
                metric = QtGui.QStyle.PM_IconViewIconSize

            extent = QtGui.QApplication.style().pixelMetric(metric)

        self.previewArea.setSize(QtCore.QSize(extent, extent))
        self.otherSpinBox.setEnabled(self.otherRadioButton.isChecked())

    def changeIcon(self):
        icon = QtGui.QIcon()

        for row in range(self.imagesTable.rowCount()):
            item0 = self.imagesTable.item(row, 0)
            item1 = self.imagesTable.item(row, 1)
            item2 = self.imagesTable.item(row, 2)

            if item0.checkState() == QtCore.Qt.Checked:
                if item1.text() == self.tr("Normal"):
                    mode = QtGui.QIcon.Normal
                elif item1.text() == self.tr("Active"):
                    mode = QtGui.QIcon.Active
                else:
                    mode = QtGui.QIcon.Disabled

                if item2.text() == self.tr("On"):
                    state = QtGui.QIcon.On
                else:
                    state = QtGui.QIcon.Off

                fileName = item0.data(QtCore.Qt.UserRole).toString()
                image = QtGui.QImage(fileName)
                if not image.isNull():
                    icon.addPixmap(QtGui.QPixmap.fromImage(image), mode, state)

        self.previewArea.setIcon(icon)

    def addImage(self):
        fileNames = QtGui.QFileDialog.getOpenFileNames(
                        self, self.tr("Open Images"), "",
                        self.tr("Images (*.png *.xpm *.jpg);;All Files (*)"))

        if not fileNames.isEmpty():
            for fileName in fileNames:
                row = self.imagesTable.rowCount()
                self.imagesTable.setRowCount(row + 1)

                imageName = QtCore.QFileInfo(fileName).baseName()
                item0 = QtGui.QTableWidgetItem(imageName)
                item0.setData(QtCore.Qt.UserRole, QtCore.QVariant(fileName))
                item0.setFlags(item0.flags() & ~QtCore.Qt.ItemIsEditable)

                item1 = QtGui.QTableWidgetItem(self.tr("Normal"))
                item2 = QtGui.QTableWidgetItem(self.tr("Off"))

                if self.guessModeStateAct.isChecked():
                    if fileName.contains("_act"):
                        item1.setText(self.tr("Active"))
                    elif fileName.contains("_dis"):
                        item1.setText(self.tr("Disabled"))

                    if fileName.contains("_on"):
                        item2.setText(self.tr("On"))

                self.imagesTable.setItem(row, 0, item0)
                self.imagesTable.setItem(row, 1, item1)
                self.imagesTable.setItem(row, 2, item2)
                self.imagesTable.openPersistentEditor(item1)
                self.imagesTable.openPersistentEditor(item2)

                item0.setCheckState(QtCore.Qt.Checked)

    def removeAllImages(self):
        self.imagesTable.setRowCount(0)
        self.changeIcon()

    def createPreviewGroupBox(self):
        self.previewGroupBox = QtGui.QGroupBox(self.tr("Preview"))

        self.previewArea = IconPreviewArea()

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.previewArea)
        self.previewGroupBox.setLayout(layout)

    def createImagesGroupBox(self):
        self.imagesGroupBox = QtGui.QGroupBox(self.tr("Images"))
        self.imagesGroupBox.setSizePolicy(QtGui.QSizePolicy.Expanding,
                                          QtGui.QSizePolicy.Expanding)

        labels = QtCore.QStringList()
        labels << self.tr("Image") << self.tr("Mode") << self.tr("State")

        self.imagesTable = QtGui.QTableWidget()
        self.imagesTable.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Ignored)
        self.imagesTable.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.imagesTable.setColumnCount(3)
        self.imagesTable.setHorizontalHeaderLabels(labels)
        self.imagesTable.setItemDelegate(ImageDelegate(self))

        self.imagesTable.horizontalHeader().resizeSection(0, 160)
        self.imagesTable.horizontalHeader().resizeSection(1, 80)
        self.imagesTable.horizontalHeader().resizeSection(2, 80)
        self.imagesTable.verticalHeader().hide()

        self.connect(self.imagesTable, QtCore.SIGNAL("itemChanged(QTableWidgetItem *)"),
                     self.changeIcon)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.imagesTable)
        self.imagesGroupBox.setLayout(layout)

    def createIconSizeGroupBox(self):
        self.iconSizeGroupBox = QtGui.QGroupBox(self.tr("Icon Size"))

        self.smallRadioButton = QtGui.QRadioButton()
        self.largeRadioButton = QtGui.QRadioButton()
        self.toolBarRadioButton = QtGui.QRadioButton()
        self.listViewRadioButton = QtGui.QRadioButton()
        self.iconViewRadioButton = QtGui.QRadioButton()
        self.otherRadioButton = QtGui.QRadioButton(self.tr("Other:"))

        self.otherSpinBox = IconSizeSpinBox()
        self.otherSpinBox.setRange(8, 128)
        self.otherSpinBox.setValue(64)

        self.connect(self.toolBarRadioButton, QtCore.SIGNAL("toggled(bool)"),
                     self.changeSize)
        self.connect(self.listViewRadioButton, QtCore.SIGNAL("toggled(bool)"),
                     self.changeSize)
        self.connect(self.iconViewRadioButton, QtCore.SIGNAL("toggled(bool)"),
                     self.changeSize)
        self.connect(self.smallRadioButton, QtCore.SIGNAL("toggled(bool)"),
                     self.changeSize)
        self.connect(self.largeRadioButton, QtCore.SIGNAL("toggled(bool)"),
                     self.changeSize)
        self.connect(self.otherRadioButton, QtCore.SIGNAL("toggled(bool)"),
                     self.changeSize)
        self.connect(self.otherSpinBox, QtCore.SIGNAL("valueChanged(int)"),
                     self.changeSize)

        otherSizeLayout = QtGui.QHBoxLayout()
        otherSizeLayout.addWidget(self.otherRadioButton)
        otherSizeLayout.addWidget(self.otherSpinBox)

        layout = QtGui.QGridLayout()
        layout.addWidget(self.smallRadioButton, 0, 0)
        layout.addWidget(self.largeRadioButton, 1, 0)
        layout.addWidget(self.toolBarRadioButton, 2, 0)
        layout.addWidget(self.listViewRadioButton, 0, 1)
        layout.addWidget(self.iconViewRadioButton, 1, 1)
        layout.addLayout(otherSizeLayout, 2, 1)
        self.iconSizeGroupBox.setLayout(layout)

    def createActions(self):
        self.addImageAct = QtGui.QAction(self.tr("&Add Image..."), self)
        self.addImageAct.setShortcut(self.tr("Ctrl+A"))
        self.connect(self.addImageAct, QtCore.SIGNAL("triggered()"),
                     self.addImage)

        self.removeAllImagesAct = QtGui.QAction(self.tr("&Remove All Images"), self)
        self.removeAllImagesAct.setShortcut(self.tr("Ctrl+R"))
        self.connect(self.removeAllImagesAct, QtCore.SIGNAL("triggered()"),
                     self.removeAllImages)

        self.exitAct = QtGui.QAction(self.tr("&Quit"), self)
        self.exitAct.setShortcut(self.tr("Ctrl+Q"))
        self.connect(self.exitAct, QtCore.SIGNAL("triggered()"),
                     self, QtCore.SLOT("close()"))

        self.styleActionGroup = QtGui.QActionGroup(self)
        for styleName in QtGui.QStyleFactory.keys():
            action = QtGui.QAction(self.styleActionGroup)
            action.setText(self.tr("%1 Style").arg(styleName))
            action.setData(QtCore.QVariant(styleName))
            action.setCheckable(True)
            self.connect(action, QtCore.SIGNAL("triggered(bool)"), self.changeStyle)

        self.guessModeStateAct = QtGui.QAction(self.tr("&Guess Image Mode/State"), self)
        self.guessModeStateAct.setCheckable(True)
        self.guessModeStateAct.setChecked(True)

        self.aboutAct = QtGui.QAction(self.tr("&About"), self)
        self.connect(self.aboutAct, QtCore.SIGNAL("triggered()"), self.about)

        self.aboutQtAct = QtGui.QAction(self.tr("About &Qt"), self)
        self.connect(self.aboutQtAct, QtCore.SIGNAL("triggered()"),
                     QtGui.qApp, QtCore.SLOT("aboutQt()"))

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu(self.tr("&File"))
        self.fileMenu.addAction(self.addImageAct)
        self.fileMenu.addAction(self.removeAllImagesAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.viewMenu = self.menuBar().addMenu(self.tr("&View"))
        for action in self.styleActionGroup.actions():
            self.viewMenu.addAction(action)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.guessModeStateAct)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu(self.tr("&Help"))
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

    def createContextMenu(self):
        self.imagesTable.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.imagesTable.addAction(self.addImageAct)
        self.imagesTable.addAction(self.removeAllImagesAct)

    def checkCurrentStyle(self):
        for action in self.styleActionGroup.actions():
            styleName = action.data().toString()
            candidate = QtGui.QStyleFactory.create(styleName)

            if candidate.metaObject().className() == QtGui.QApplication.style().metaObject().className():
                action.trigger()
                return


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
