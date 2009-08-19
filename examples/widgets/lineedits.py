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


class Window(QtGui.QWidget):
    def __init__(self):
        super(Window, self).__init__()

        echoGroup = QtGui.QGroupBox(self.tr("Echo"))

        echoLabel = QtGui.QLabel(self.tr("Mode:"))
        echoComboBox = QtGui.QComboBox()
        echoComboBox.addItem(self.tr("Normal"))
        echoComboBox.addItem(self.tr("Password"))
        echoComboBox.addItem(self.tr("PasswordEchoOnEdit"))
        echoComboBox.addItem(self.tr("No Echo"))

        self.echoLineEdit = QtGui.QLineEdit()
        self.echoLineEdit.setFocus()

        validatorGroup = QtGui.QGroupBox(self.tr("Validator"))

        validatorLabel = QtGui.QLabel(self.tr("Type:"))
        validatorComboBox = QtGui.QComboBox()
        validatorComboBox.addItem(self.tr("No validator"))
        validatorComboBox.addItem(self.tr("Integer validator"))
        validatorComboBox.addItem(self.tr("Double validator"))

        self.validatorLineEdit = QtGui.QLineEdit()

        alignmentGroup = QtGui.QGroupBox(self.tr("Alignment"))

        alignmentLabel = QtGui.QLabel(self.tr("Type:"))
        alignmentComboBox = QtGui.QComboBox()
        alignmentComboBox.addItem(self.tr("Left"))
        alignmentComboBox.addItem(self.tr("Centered"))
        alignmentComboBox.addItem(self.tr("Right"))

        self.alignmentLineEdit = QtGui.QLineEdit()

        inputMaskGroup = QtGui.QGroupBox(self.tr("Input mask"))

        inputMaskLabel = QtGui.QLabel(self.tr("Type:"))
        inputMaskComboBox = QtGui.QComboBox()
        inputMaskComboBox.addItem(self.tr("No mask"))
        inputMaskComboBox.addItem(self.tr("Phone number"))
        inputMaskComboBox.addItem(self.tr("ISO date"))
        inputMaskComboBox.addItem(self.tr("License key"))

        self.inputMaskLineEdit = QtGui.QLineEdit()

        accessGroup = QtGui.QGroupBox(self.tr("Access"))

        accessLabel = QtGui.QLabel(self.tr("Read-only:"))
        accessComboBox = QtGui.QComboBox()
        accessComboBox.addItem(self.tr("False"))
        accessComboBox.addItem(self.tr("True"))

        self.accessLineEdit = QtGui.QLineEdit()

        echoComboBox.activated.connect(self.echoChanged)
        validatorComboBox.activated.connect(self.validatorChanged)
        alignmentComboBox.activated.connect(self.alignmentChanged)
        inputMaskComboBox.activated.connect(self.inputMaskChanged)
        accessComboBox.activated.connect(self.accessChanged)

        echoLayout = QtGui.QGridLayout()
        echoLayout.addWidget(echoLabel, 0, 0)
        echoLayout.addWidget(echoComboBox, 0, 1)
        echoLayout.addWidget(self.echoLineEdit, 1, 0, 1, 2)
        echoGroup.setLayout(echoLayout)

        validatorLayout = QtGui.QGridLayout()
        validatorLayout.addWidget(validatorLabel, 0, 0)
        validatorLayout.addWidget(validatorComboBox, 0, 1)
        validatorLayout.addWidget(self.validatorLineEdit, 1, 0, 1, 2)
        validatorGroup.setLayout(validatorLayout)

        alignmentLayout = QtGui.QGridLayout()
        alignmentLayout.addWidget(alignmentLabel, 0, 0)
        alignmentLayout.addWidget(alignmentComboBox, 0, 1)
        alignmentLayout.addWidget(self.alignmentLineEdit, 1, 0, 1, 2)
        alignmentGroup. setLayout(alignmentLayout)

        inputMaskLayout = QtGui.QGridLayout()
        inputMaskLayout.addWidget(inputMaskLabel, 0, 0)
        inputMaskLayout.addWidget(inputMaskComboBox, 0, 1)
        inputMaskLayout.addWidget(self.inputMaskLineEdit, 1, 0, 1, 2)
        inputMaskGroup.setLayout(inputMaskLayout)

        accessLayout = QtGui.QGridLayout()
        accessLayout.addWidget(accessLabel, 0, 0)
        accessLayout.addWidget(accessComboBox, 0, 1)
        accessLayout.addWidget(self.accessLineEdit, 1, 0, 1, 2)
        accessGroup.setLayout(accessLayout)

        layout = QtGui.QGridLayout()
        layout.addWidget(echoGroup, 0, 0)
        layout.addWidget(validatorGroup, 1, 0)
        layout.addWidget(alignmentGroup, 2, 0)
        layout.addWidget(inputMaskGroup, 0, 1)
        layout.addWidget(accessGroup, 1, 1)
        self.setLayout(layout)

        self.setWindowTitle(self.tr("Line Edits"))

    def echoChanged(self, index):
        if index == 0:
            self.echoLineEdit.setEchoMode(QtGui.QLineEdit.Normal)
        elif index == 1:
            self.echoLineEdit.setEchoMode(QtGui.QLineEdit.Password)
        elif index == 2:
            self.echoLineEdit.setEchoMode(QtGui.QLineEdit.PasswordEchoOnEdit)
        elif index == 3:
    	    self.echoLineEdit.setEchoMode(QtGui.QLineEdit.NoEcho)

    def validatorChanged(self, index):
        if index == 0:
            self.validatorLineEdit.setValidator(0)
        elif index == 1:
            self.validatorLineEdit.setValidator(QtGui.QIntValidator(self.validatorLineEdit))
        elif index == 2:
            self.validatorLineEdit.setValidator(QtGui.QDoubleValidator(-999.0, 999.0, 2, self.validatorLineEdit))

        self.validatorLineEdit.clear()

    def alignmentChanged(self, index):
        if index == 0:
            self.alignmentLineEdit.setAlignment(QtCore.Qt.AlignLeft)
        elif index == 1:
            self.alignmentLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        elif index == 2:
    	    self.alignmentLineEdit.setAlignment(QtCore.Qt.AlignRight)

    def inputMaskChanged(self, index):
        if index == 0:
            self.inputMaskLineEdit.setInputMask("")
        elif index == 1:
            self.inputMaskLineEdit.setInputMask("+99 99 99 99 99;_")
        elif index == 2:
            self.inputMaskLineEdit.setInputMask("0000-00-00")
            self.inputMaskLineEdit.setText("00000000")
            self.inputMaskLineEdit.setCursorPosition(0)
        elif index == 3:
            self.inputMaskLineEdit.setInputMask(">AAAAA-AAAAA-AAAAA-AAAAA-AAAAA;#")

    def accessChanged(self, index):
        if index == 0:
            self.accessLineEdit.setReadOnly(False)
        elif index == 1:
            self.accessLineEdit.setReadOnly(True)


if __name__ == "__main__":

    import sys

    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
