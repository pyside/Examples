#!/usr/bin/env python

"""PyQt4 port of the layouts/basiclayout example from Qt v4.x"""

from PyQt4 import QtCore, QtGui


class Dialog(QtGui.QDialog):
    NumGridRows = 3
    NumButtons = 4

    def __init__(self):
        super(Dialog, self).__init__()

        self.createMenu()
        self.createHorizontalGroupBox()
        self.createGridGroupBox()
        self.createFormGroupBox()

        bigEditor = QtGui.QTextEdit()
        bigEditor.setPlainText(self.tr("This widget takes up all the "
                                       "remaining space in the top-level "
                                       "layout."))

        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.setMenuBar(self.menuBar)
        mainLayout.addWidget(self.horizontalGroupBox)
        mainLayout.addWidget(self.gridGroupBox)
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(bigEditor)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.setWindowTitle(self.tr("Basic Layouts"))

    def createMenu(self):
        self.menuBar = QtGui.QMenuBar()

        self.fileMenu = QtGui.QMenu(self.tr("&File"), self)
        self.exitAction = self.fileMenu.addAction(self.tr("E&xit"))
        self.menuBar.addMenu(self.fileMenu)

        self.exitAction.triggered.connect(self.accept)

    def createHorizontalGroupBox(self):
        self.horizontalGroupBox = QtGui.QGroupBox(self.tr("Horizontal layout"))
        layout = QtGui.QHBoxLayout()

        for i in range(Dialog.NumButtons):
            button = QtGui.QPushButton(self.tr("Button %1").arg(i + 1))
            layout.addWidget(button)

        self.horizontalGroupBox.setLayout(layout)

    def createGridGroupBox(self):
        self.gridGroupBox = QtGui.QGroupBox(self.tr("Grid layout"))
        layout = QtGui.QGridLayout()

        for i in range(Dialog.NumGridRows):
            label = QtGui.QLabel(self.tr("Line %1:").arg(i + 1))
            lineEdit = QtGui.QLineEdit()
            layout.addWidget(label, i + 1, 0)
            layout.addWidget(lineEdit, i + 1, 1)

        self.smallEditor = QtGui.QTextEdit()
        self.smallEditor.setPlainText(self.tr("This widget takes up about two "
                                              "thirds of the grid layout."))

        layout.addWidget(self.smallEditor, 0, 2, 4, 1)

        layout.setColumnStretch(1, 10)
        layout.setColumnStretch(2, 20)
        self.gridGroupBox.setLayout(layout)

    def createFormGroupBox(self):
        self.formGroupBox = QtGui.QGroupBox(self.tr("Form layout"))
        layout = QtGui.QFormLayout()
        layout.addRow(QtGui.QLabel(self.tr("Line 1:")), QtGui.QLineEdit())
        layout.addRow(QtGui.QLabel(self.tr("Line 2, long text:")),
                QtGui.QComboBox())
        layout.addRow(QtGui.QLabel(self.tr("Line 3:")), QtGui.QSpinBox())
        self.formGroupBox.setLayout(layout)


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    dialog = Dialog()
    sys.exit(dialog.exec_())
