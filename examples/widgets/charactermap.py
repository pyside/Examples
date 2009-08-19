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

import sys
from PySide import QtCore, QtGui


class CharacterWidget(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)

        self.displayFont = QtGui.QFont()
        self.lastKey = -1
        self.setMouseTracking(True)

    def updateFont(self, fontFamily):
        self.displayFont.setFamily(fontFamily)
        self.displayFont.setPixelSize(16)
        self.update()

    def updateStyle(self, fontStyle):
        fontDatabase = QtGui.QFontDatabase()
        self.displayFont = fontDatabase.font(self.displayFont.family(),
                                             fontStyle, 12)
        self.displayFont.setPixelSize(16)
        self.update()

    def sizeHint(self):
        return QtCore.QSize(32*24, (65536/32)*24)

    def mouseMoveEvent(self, event):
        widgetPosition = self.mapFromGlobal(event.globalPos())
        key = (widgetPosition.y()/24)*32 + widgetPosition.x()/24
        QtGui.QToolTip.showText(event.globalPos(), QtCore.QString.number(key), self)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.lastKey = (event.y()/24)*32 + event.x()/24
            if QtCore.QChar(self.lastKey).category() != QtCore.QChar.NoCategory:
                self.emit(QtCore.SIGNAL("characterSelected(const QString &)"), QtCore.QString(QtCore.QChar(self.lastKey)))
            self.update()
        else:
            QtGui.QWidget.mousePressEvent(self, event)

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.fillRect(event.rect(), QtCore.Qt.white)
        painter.setFont(self.displayFont)

        redrawRect = event.rect()
        beginRow = redrawRect.top()/24
        endRow = redrawRect.bottom()/24
        beginColumn = redrawRect.left()/24
        endColumn = redrawRect.right()/24

        painter.setPen(QtCore.Qt.gray)
        for row in range(beginRow, endRow + 1):
            for column in range(beginColumn, endColumn + 1):
                painter.drawRect(column*24, row*24, 24, 24)

        fontMetrics = QtGui.QFontMetrics(self.displayFont)
        painter.setPen(QtCore.Qt.black)
        for row in range(beginRow, endRow + 1):
            for column in range(beginColumn, endColumn + 1):
                key = row*32 + column
                painter.setClipRect(column*24, row*24, 24, 24)

                if key == self.lastKey:
                    painter.fillRect(column*24, row*24, 24, 24, QtCore.Qt.red)

                painter.drawText(column*24 + 12 - fontMetrics.width(QtCore.QChar(key))/2,
                                 row*24 + 4 + fontMetrics.ascent(),
                                 QtCore.QString(QtCore.QChar(key)))


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)

        centralWidget = QtGui.QWidget()

        fontLabel = QtGui.QLabel(self.tr("Font:"))
        self.fontCombo = QtGui.QComboBox()
        styleLabel = QtGui.QLabel(self.tr("Style:"))
        self.styleCombo = QtGui.QComboBox()

        self.scrollArea = QtGui.QScrollArea()
        self.characterWidget = CharacterWidget()
        self.scrollArea.setWidget(self.characterWidget)

        self.findFonts()
        self.findStyles()

        self.lineEdit = QtGui.QLineEdit()
        clipboardButton = QtGui.QPushButton(self.tr("&To clipboard"))

        self.clipboard = QtGui.QApplication.clipboard()

        self.connect(self.fontCombo, QtCore.SIGNAL("activated(const QString &)"),
                     self.findStyles)
        self.connect(self.fontCombo, QtCore.SIGNAL("activated(const QString &)"),
                     self.characterWidget.updateFont)
        self.connect(self.styleCombo, QtCore.SIGNAL("activated(const QString &)"),
                     self.characterWidget.updateStyle)
        self.connect(self.characterWidget, QtCore.SIGNAL("characterSelected(const QString &)"),
                     self.insertCharacter)
        self.connect(clipboardButton, QtCore.SIGNAL("clicked()"), self.updateClipboard)

        controlsLayout = QtGui.QHBoxLayout()
        controlsLayout.addWidget(fontLabel)
        controlsLayout.addWidget(self.fontCombo, 1)
        controlsLayout.addWidget(styleLabel)
        controlsLayout.addWidget(self.styleCombo, 1)
        controlsLayout.addStretch(1)

        lineLayout = QtGui.QHBoxLayout()
        lineLayout.addWidget(self.lineEdit, 1)
        lineLayout.addSpacing(12)
        lineLayout.addWidget(clipboardButton)

        centralLayout = QtGui.QVBoxLayout()
        centralLayout.addLayout(controlsLayout)
        centralLayout.addWidget(self.scrollArea, 1)
        centralLayout.addSpacing(4)
        centralLayout.addLayout(lineLayout)
        centralWidget.setLayout(centralLayout)

        self.setCentralWidget(centralWidget)
        self.setWindowTitle(self.tr("Character Map"))

    def findFonts(self):
        fontDatabase = QtGui.QFontDatabase()
        self.fontCombo.clear()

        for family in fontDatabase.families():
            self.fontCombo.addItem(family)

    def findStyles(self):
        fontDatabase = QtGui.QFontDatabase()
        currentItem = self.styleCombo.currentText()
        self.styleCombo.clear()

        for style in fontDatabase.styles(self.fontCombo.currentText()):
            self.styleCombo.addItem(style)

        index = self.styleCombo.findText(currentItem)
        if index == -1:
            self.styleCombo.setCurrentIndex(0)
        else:
            self.styleCombo.setCurrentIndex(index)

        self.characterWidget.updateStyle(self.styleCombo.currentText())

    def insertCharacter(self, character):
        self.lineEdit.insert(character)

    def updateClipboard(self):
        self.clipboard.setText(self.lineEdit.text(), QtGui.QClipboard.Clipboard)
        self.clipboard.setText(self.lineEdit.text(), QtGui.QClipboard.Selection)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
