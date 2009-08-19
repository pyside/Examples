#!/usr/bin/env python

"""PySide port of the layouts/basiclayout example from Qt v4.x"""

import sys
from PySide import QtCore, QtGui


class Dialog(QtGui.QDialog):
    NumGridRows = 3
    NumButtons = 4
    
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        
        self.buttons = []
        self.labels = []
        self.lineEdits = []
        
        self.createMenu()
        self.createHorizontalGroupBox()
        self.createGridGroupBox()
        
        self.bigEditor = QtGui.QTextEdit()
        self.bigEditor.setPlainText(self.tr("This widget takes up all the remaining "
                                            "space in the top-level layout."))
        
        self.okButton = QtGui.QPushButton(self.tr("OK"))
        self.cancelButton = QtGui.QPushButton(self.tr("Cancel"))
        self.okButton.setDefault(True)
        
        self.connect(self.okButton, QtCore.SIGNAL("clicked()"),
                     self, QtCore.SLOT("accept()"))
        self.connect(self.cancelButton, QtCore.SIGNAL("clicked()"),
                     self, QtCore.SLOT("reject()"))
        
        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(self.okButton)
        buttonLayout.addWidget(self.cancelButton)
        
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.setMenuBar(self.menuBar)
        mainLayout.addWidget(self.horizontalGroupBox)
        mainLayout.addWidget(self.gridGroupBox)
        mainLayout.addWidget(self.bigEditor)
        mainLayout.addLayout(buttonLayout)
        self.setLayout(mainLayout)
        
        self.setWindowTitle(self.tr("Basic Layouts"))
        
    def createMenu(self):
        self.menuBar = QtGui.QMenuBar()
        
        self.fileMenu = QtGui.QMenu(self.tr("&File"), self)
        self.exitAction = self.fileMenu.addAction(self.tr("E&xit"))
        self.menuBar.addMenu(self.fileMenu)
        
        self.connect(self.exitAction, QtCore.SIGNAL("triggered()"),
                     self, QtCore.SLOT("accept()"))
        
    def createHorizontalGroupBox(self):
        self.horizontalGroupBox = QtGui.QGroupBox(self.tr("Horizontal layout"))
        layout = QtGui.QHBoxLayout()
        
        for i in range(Dialog.NumButtons):
            self.buttons.append(QtGui.QPushButton(self.tr("Button %1").arg(i + 1)))
            layout.addWidget(self.buttons[i])
        
        self.horizontalGroupBox.setLayout(layout)
        
    def createGridGroupBox(self):
        self.gridGroupBox = QtGui.QGroupBox(self.tr("Grid layout"))
        layout = QtGui.QGridLayout()
        
        for i in range(Dialog.NumGridRows):
            self.labels.append(QtGui.QLabel(self.tr("Line %1:").arg(i + 1)))
            self.lineEdits.append(QtGui.QLineEdit())
            layout.addWidget(self.labels[i], i, 0)
            layout.addWidget(self.lineEdits[i], i, 1)
        
        self.smallEditor = QtGui.QTextEdit()
        self.smallEditor.setPlainText(self.tr("This widget takes up about two "
                                              "thirds of the grid layout."))

        layout.addWidget(self.smallEditor, 0, 2, 3, 1)
        
        layout.setColumnStretch(1, 10)
        layout.setColumnStretch(2, 20)
        self.gridGroupBox.setLayout(layout)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    dialog = Dialog()
    sys.exit(dialog.exec_())
