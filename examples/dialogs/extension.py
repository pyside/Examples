#!/usr/bin/env python

"""PySide port of the dialogs/extension example from Qt v4.x"""

import sys
from PySide import QtCore, QtGui


class FindDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)

        self.label = QtGui.QLabel(self.tr("Find &what:"))
        self.lineEdit = QtGui.QLineEdit()
        self.label.setBuddy(self.lineEdit)

        self.caseCheckBox = QtGui.QCheckBox(self.tr("Match &case"))
        self.fromStartCheckBox = QtGui.QCheckBox(self.tr("Search from &start"))
        self.fromStartCheckBox.setChecked(True)

        self.findButton = QtGui.QPushButton(self.tr("&Find"))
        self.findButton.setDefault(True)

        self.closeButton = QtGui.QPushButton(self.tr("Close"))

        self.moreButton = QtGui.QPushButton(self.tr("&More"))
        self.moreButton.setCheckable(True)
        self.moreButton.setAutoDefault(False)

        self.extension = QtGui.QWidget()

        self.wholeWordsCheckBox = QtGui.QCheckBox(self.tr("&Whole words"))
        self.backwardCheckBox = QtGui.QCheckBox(self.tr("Search &backward"))
        self.searchSelectionCheckBox = QtGui.QCheckBox(self.tr("Search se&lection"))

        self.connect(self.closeButton, QtCore.SIGNAL("clicked()"),
                     self, QtCore.SLOT("close()"))
        self.connect(self.moreButton, QtCore.SIGNAL("toggled(bool)"),
                     self.extension, QtCore.SLOT("setVisible(bool)"))

        extensionLayout = QtGui.QVBoxLayout()
        extensionLayout.setMargin(0)
        extensionLayout.addWidget(self.wholeWordsCheckBox)
        extensionLayout.addWidget(self.backwardCheckBox)
        extensionLayout.addWidget(self.searchSelectionCheckBox)
        self.extension.setLayout(extensionLayout)

        topLeftLayout = QtGui.QHBoxLayout()
        topLeftLayout.addWidget(self.label)
        topLeftLayout.addWidget(self.lineEdit)

        leftLayout = QtGui.QVBoxLayout()
        leftLayout.addLayout(topLeftLayout)
        leftLayout.addWidget(self.caseCheckBox)
        leftLayout.addWidget(self.fromStartCheckBox)
        leftLayout.addStretch(1)

        rightLayout = QtGui.QVBoxLayout()
        rightLayout.addWidget(self.findButton)
        rightLayout.addWidget(self.closeButton)
        rightLayout.addWidget(self.moreButton)
        rightLayout.addStretch(1)

        mainLayout = QtGui.QGridLayout()
        mainLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        mainLayout.addLayout(leftLayout, 0, 0)
        mainLayout.addLayout(rightLayout, 0, 1)
        mainLayout.addWidget(self.extension, 1, 0, 1, 2)
        self.setLayout(mainLayout)

        self.setWindowTitle(self.tr("Extension"))
        self.extension.hide()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    dialog = FindDialog()
    sys.exit(dialog.exec_())
