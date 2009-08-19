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

import math

from PyQt4 import QtCore, QtGui


class Button(QtGui.QToolButton):
    def __init__(self, text, parent=None):
        super(Button, self).__init__(parent)

        self.setSizePolicy(QtGui.QSizePolicy.Expanding,
                QtGui.QSizePolicy.Preferred)
        self.setText(text)

    def sizeHint(self):
        size = super(Button, self).sizeHint()
        size.setHeight(size.height() + 20)
        size.setWidth(max(size.width(), size.height()))
        return size


class Calculator(QtGui.QDialog):
    NumDigitButtons = 10
    
    def __init__(self, parent=None):
        super(Calculator, self).__init__(parent)

        self.pendingAdditiveOperator = QtCore.QString()
        self.pendingMultiplicativeOperator = QtCore.QString()

        self.sumInMemory = 0.0
        self.sumSoFar = 0.0
        self.factorSoFar = 0.0
        self.waitingForOperand = True

        self.display = QtGui.QLineEdit("0")
        self.display.setReadOnly(True)
        self.display.setAlignment(QtCore.Qt.AlignRight)
        self.display.setMaxLength(15)

        font = self.display.font()
        font.setPointSize(font.pointSize() + 8)
        self.display.setFont(font)

        self.digitButtons = []
        
        for i in range(Calculator.NumDigitButtons):
            self.digitButtons.append(self.createButton(QtCore.QString.number(i),
                    self.digitClicked))

        self.pointButton = self.createButton(self.tr("."), self.pointClicked)
        self.changeSignButton = self.createButton(self.tr("\261"),
                self.changeSignClicked)

        self.backspaceButton = self.createButton(self.tr("Backspace"),
                self.backspaceClicked)
        self.clearButton = self.createButton(self.tr("Clear"), self.clear)
        self.clearAllButton = self.createButton(self.tr("Clear All"),
                self.clearAll)

        self.clearMemoryButton = self.createButton(self.tr("MC"),
                self.clearMemory)
        self.readMemoryButton = self.createButton(self.tr("MR"),
                self.readMemory)
        self.setMemoryButton = self.createButton(self.tr("MS"), self.setMemory)
        self.addToMemoryButton = self.createButton(self.tr("M+"),
                self.addToMemory)

        self.divisionButton = self.createButton(self.tr("\367"),
                self.multiplicativeOperatorClicked)
        self.timesButton = self.createButton(self.tr("\327"),
                self.multiplicativeOperatorClicked)
        self.minusButton = self.createButton(self.tr("-"),
                self.additiveOperatorClicked)
        self.plusButton = self.createButton(self.tr("+"),
                self.additiveOperatorClicked)

        self.squareRootButton = self.createButton(self.tr("Sqrt"),
                self.unaryOperatorClicked)
        self.powerButton = self.createButton(self.tr("x\262"),
                self.unaryOperatorClicked)
        self.reciprocalButton = self.createButton(self.tr("1/x"),
                self.unaryOperatorClicked)
        self.equalButton = self.createButton(self.tr("="), self.equalClicked)

        mainLayout = QtGui.QGridLayout()
        mainLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)

        mainLayout.addWidget(self.display, 0, 0, 1, 6)
        mainLayout.addWidget(self.backspaceButton, 1, 0, 1, 2)
        mainLayout.addWidget(self.clearButton, 1, 2, 1, 2)
        mainLayout.addWidget(self.clearAllButton, 1, 4, 1, 2)

        mainLayout.addWidget(self.clearMemoryButton, 2, 0)
        mainLayout.addWidget(self.readMemoryButton, 3, 0)
        mainLayout.addWidget(self.setMemoryButton, 4, 0)
        mainLayout.addWidget(self.addToMemoryButton, 5, 0)

        for i in range(1, Calculator.NumDigitButtons):
            row = ((9 - i) / 3) + 2
            column = ((i - 1) % 3) + 1
            mainLayout.addWidget(self.digitButtons[i], row, column)

        mainLayout.addWidget(self.digitButtons[0], 5, 1)
        mainLayout.addWidget(self.pointButton, 5, 2)
        mainLayout.addWidget(self.changeSignButton, 5, 3)

        mainLayout.addWidget(self.divisionButton, 2, 4)
        mainLayout.addWidget(self.timesButton, 3, 4)
        mainLayout.addWidget(self.minusButton, 4, 4)
        mainLayout.addWidget(self.plusButton, 5, 4)

        mainLayout.addWidget(self.squareRootButton, 2, 5)
        mainLayout.addWidget(self.powerButton, 3, 5)
        mainLayout.addWidget(self.reciprocalButton, 4, 5)
        mainLayout.addWidget(self.equalButton, 5, 5)
        self.setLayout(mainLayout)

        self.setWindowTitle(self.tr("Calculator"))

    def digitClicked(self):
        clickedButton = self.sender()
        digitValue, _ = clickedButton.text().toInt()

        if self.display.text() == "0" and digitValue == 0.0:
            return

        if self.waitingForOperand:
            self.display.clear()
            self.waitingForOperand = False

        self.display.setText(self.display.text() + QtCore.QString.number(digitValue))

    def unaryOperatorClicked(self):
        clickedButton = self.sender()
        clickedOperator = clickedButton.text()
        operand, _ = self.display.text().toDouble()

        if clickedOperator == self.tr("Sqrt"):
            if operand < 0.0:
                self.abortOperation()
                return

            result = math.sqrt(operand)
        elif clickedOperator == self.tr("x\262"):
            result = math.pow(operand, 2.0)
        elif clickedOperator == self.tr("1/x"):
            if operand == 0.0:
                self.abortOperation()
                return

            result = 1.0 / operand

        self.display.setText(QtCore.QString.number(result))
        self.waitingForOperand = True

    def additiveOperatorClicked(self):
        clickedButton = self.sender()
        clickedOperator = clickedButton.text()
        operand, _ = self.display.text().toDouble()

        if not self.pendingMultiplicativeOperator.isEmpty():
            if not self.calculate(operand, self.pendingMultiplicativeOperator):
                self.abortOperation()
                return

            self.display.setText(QtCore.QString.number(self.factorSoFar))
            operand = self.factorSoFar
            self.factorSoFar = 0.0
            self.pendingMultiplicativeOperator.clear()

        if not self.pendingAdditiveOperator.isEmpty():
            if not self.calculate(operand, self.pendingAdditiveOperator):
                self.abortOperation()
                return

            self.display.setText(QtCore.QString.number(self.sumSoFar))
        else:
            self.sumSoFar = operand

        self.pendingAdditiveOperator = clickedOperator
        self.waitingForOperand = True

    def multiplicativeOperatorClicked(self):
        clickedButton = self.sender()
        clickedOperator = clickedButton.text()
        operand, success = self.display.text().toDouble()

        if not self.pendingMultiplicativeOperator.isEmpty():
            if not self.calculate(operand, self.pendingMultiplicativeOperator):
                self.abortOperation()
                return

            self.display.setText(QtCore.QString.number(self.factorSoFar))
        else:
            self.factorSoFar = operand

        self.pendingMultiplicativeOperator = clickedOperator
        self.waitingForOperand = True

    def equalClicked(self):
        operand, _ = self.display.text().toDouble()

        if not self.pendingMultiplicativeOperator.isEmpty():
            if not self.calculate(operand, self.pendingMultiplicativeOperator):
                self.abortOperation()
                return

            operand = self.factorSoFar
            self.factorSoFar = 0.0
            self.pendingMultiplicativeOperator.clear()

        if not self.pendingAdditiveOperator.isEmpty():
            if not self.calculate(operand, self.pendingAdditiveOperator):
                self.abortOperation()
                return

            self.pendingAdditiveOperator.clear()
        else:
            self.sumSoFar = operand

        self.display.setText(QtCore.QString.number(self.sumSoFar))
        self.sumSoFar = 0.0
        self.waitingForOperand = True

    def pointClicked(self):
        if self.waitingForOperand:
            self.display.setText("0")

        if not self.display.text().contains("."):
            self.display.setText(self.display.text() + self.tr("."))

        self.waitingForOperand = False

    def changeSignClicked(self):
        text = self.display.text()
        value, _ = text.toDouble()

        if value > 0.0:
            text.prepend(self.tr("-"))
        elif value < 0.0:
            text.remove(0, 1)

        self.display.setText(text)

    def backspaceClicked(self):
        if self.waitingForOperand:
            return

        text = self.display.text()
        text.chop(1)
        if text.isEmpty():
            text = "0"
            self.waitingForOperand = True

        self.display.setText(text)

    def clear(self):
        if self.waitingForOperand:
            return

        self.display.setText("0")
        self.waitingForOperand = True

    def clearAll(self):
        self.sumSoFar = 0.0
        self.factorSoFar = 0.0
        self.pendingAdditiveOperator.clear()
        self.pendingMultiplicativeOperator.clear()
        self.display.setText("0")
        self.waitingForOperand = True

    def clearMemory(self):
        self.sumInMemory = 0.0

    def readMemory(self):
        self.display.setText(QtCore.QString.number(self.sumInMemory))
        self.waitingForOperand = True

    def setMemory(self):
        self.equalClicked()
        self.sumInMemory, _ = self.display.text().toDouble()

    def addToMemory(self):
        self.equalClicked()
        value, _ = self.display.text().toDouble()
        self.sumInMemory += value

    def createButton(self, text, member):
        button = Button(text)
        button.clicked.connect(member)
        return button

    def abortOperation(self):
        self.clearAll()
        self.display.setText(self.tr("####"))

    def calculate(self, rightOperand, pendingOperator):
        if pendingOperator == self.tr("+"):
            self.sumSoFar += rightOperand
        elif pendingOperator == self.tr("-"):
            self.sumSoFar -= rightOperand
        elif pendingOperator == self.tr("\327"):
            self.factorSoFar *= rightOperand
        elif pendingOperator == self.tr("\367"):
            if rightOperand == 0.0:
                return False

            self.factorSoFar /= rightOperand

        return True


if __name__ == "__main__":

    import sys

    app = QtGui.QApplication(sys.argv)
    calc = Calculator()
    sys.exit(calc.exec_())
