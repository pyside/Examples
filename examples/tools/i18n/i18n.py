#!/usr/bin/env python

#############################################################################
##
## Copyright (C) 2004-2005 Trolltech AS. All rights reserved.
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

from PyQt4 import QtCore, QtGui

import i18n_rc


class LanguageChooser(QtGui.QDialog):
    def __init__(self, parent=None):
        super(LanguageChooser, self).__init__(parent,
                QtCore.Qt.WindowStaysOnTopHint)

        self.qmFileForCheckBoxMap = {}
        self.mainWindowForCheckBoxMap = {} 

        groupBox = QtGui.QGroupBox("Languages")

        groupBoxLayout = QtGui.QGridLayout()

        qmFiles = self.findQmFiles()

        for i, qmf in enumerate(qmFiles):
            checkBox = QtGui.QCheckBox(self.languageName(qmf))
            self.qmFileForCheckBoxMap[checkBox] = qmf
            checkBox.toggled.connect(self.checkBoxToggled)
            groupBoxLayout.addWidget(checkBox, i / 2, i % 2)

        groupBox.setLayout(groupBoxLayout)

        buttonBox = QtGui.QDialogButtonBox()

        showAllButton = buttonBox.addButton("Show All",
                QtGui.QDialogButtonBox.ActionRole)
        hideAllButton = buttonBox.addButton("Hide All",
                QtGui.QDialogButtonBox.ActionRole)

        showAllButton.clicked.connect(self.showAll)
        hideAllButton.clicked.connect(self.hideAll)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(groupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        if hasattr(QtGui, 'qt_mac_set_menubar_merge'):
            QtGui.qt_mac_set_menubar_merge(False)

        self.setWindowTitle("I18N")

    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.Close:
            if isinstance(object, MainWindow):
                window = object

                for checkBox, w in self.mainWindowForCheckBoxMap.items():
                    if w is window:
                        break
                else:
                    checkBox = None

                if checkBox:
                    checkBox.setChecked(False)

        return QtGui.QWidget.eventFilter(self, object, event)

    def closeEvent(self, event):
        QtGui.qApp.quit()

    def checkBoxToggled(self):
        checkBox = self.sender()
        window = self.mainWindowForCheckBoxMap.get(checkBox)

        if not window:
            translator = QtCore.QTranslator()
            translator.load(self.qmFileForCheckBoxMap[checkBox])
            QtGui.qApp.installTranslator(translator)

            # Because we will be installing an event filter for the main window
            # it is important that this instance isn't garbage collected before
            # the main window when the program terminates.  We ensure this by
            # making the main window a child of this one.
            window = MainWindow(self)
            window.setPalette(QtGui.QPalette(self.colorForLanguage(checkBox.text())))

            window.installEventFilter(self)
            self.mainWindowForCheckBoxMap[checkBox] = window

        window.setVisible(checkBox.isChecked())

    def showAll(self):
        for checkBox in self.qmFileForCheckBoxMap.keys():
            checkBox.setChecked(True)

    def hideAll(self):
        for checkBox in self.qmFileForCheckBoxMap.keys():
            checkBox.setChecked(False)

    def findQmFiles(self):
        trans_dir = QtCore.QDir(":/translations")
        fileNames = trans_dir.entryList(QtCore.QStringList("*.qm"),
                QtCore.QDir.Files, QtCore.QDir.Name)

        for i in fileNames:
            fileNames.replaceInStrings(i, trans_dir.filePath(i))

        return fileNames

    def languageName(self, qmFile):
        translator = QtCore.QTranslator() 
        translator.load(qmFile)

        return translator.translate("MainWindow", "English")

    def colorForLanguage(self, language):
        hashValue = hash(language)
        red = 156 + (hashValue & 0x3F)
        green = 156 + ((hashValue >> 6) & 0x3F)
        blue = 156 + ((hashValue >> 12) & 0x3F)
        return QtGui.QColor(red, green, blue)


class MainWindow(QtGui.QMainWindow):
    listEntries = [QtCore.QT_TRANSLATE_NOOP("MainWindow", "First"),
                   QtCore.QT_TRANSLATE_NOOP("MainWindow", "Second"),
                   QtCore.QT_TRANSLATE_NOOP("MainWindow", "Third")]

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.centralWidget = QtGui.QWidget()
        self.setCentralWidget(self.centralWidget)

        self.createGroupBox()

        listWidget = QtGui.QListWidget()

        for le in MainWindow.listEntries:
            listWidget.addItem(self.tr(le))

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.groupBox)
        mainLayout.addWidget(listWidget)
        self.centralWidget.setLayout(mainLayout)

        exitAction = QtGui.QAction(self.tr("E&xit"), self)
        exitAction.triggered.connect(QtGui.qApp.quit)

        fileMenu = self.menuBar().addMenu(self.tr("&File"))
        fileMenu.setPalette(QtGui.QPalette(QtCore.Qt.red))
        fileMenu.addAction(exitAction)

        self.setWindowTitle(self.tr("Language: %1").arg(self.tr("English")))
        self.statusBar().showMessage(self.tr("Internationalization Example"))

        if self.tr("LTR") == "RTL":
            self.setLayoutDirection(QtCore.Qt.RightToLeft)

    def createGroupBox(self):
        self.groupBox = QtGui.QGroupBox(self.tr("View"))
        perspectiveRadioButton = QtGui.QRadioButton(self.tr("Perspective"))
        isometricRadioButton = QtGui.QRadioButton(self.tr("Isometric"))
        obliqueRadioButton = QtGui.QRadioButton(self.tr("Oblique"))
        perspectiveRadioButton.setChecked(True)

        self.groupBoxLayout = QtGui.QVBoxLayout()
        self.groupBoxLayout.addWidget(perspectiveRadioButton)
        self.groupBoxLayout.addWidget(isometricRadioButton)
        self.groupBoxLayout.addWidget(obliqueRadioButton)
        self.groupBox.setLayout(self.groupBoxLayout)


if __name__ == "__main__":

    import sys

    app = QtGui.QApplication(sys.argv)
    chooser = LanguageChooser()
    chooser.show()
    sys.exit(app.exec_())
