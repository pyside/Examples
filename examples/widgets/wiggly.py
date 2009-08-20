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


class WigglyWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        self.setBackgroundRole(QtGui.QPalette.Midlight)
        
        newFont = self.font()
        newFont.setPointSize(newFont.pointSize() + 20)
        self.setFont(newFont)

        self.timer = QtCore.QBasicTimer()
        self.text = QtCore.QString("Hello World !")
        
        self.step = 0;
        self.timer.start(60, self)   
        
    def paintEvent(self, event):
        sineTable = [0, 38, 71, 92, 100, 92, 71, 38, 0, -38, -71, -92, -100, -92, -71, -38]

        metrics = QtGui.QFontMetrics(self.font())
        x = (self.width() - metrics.width(self.text)) / 2
        y = (self.height() + metrics.ascent() - metrics.descent()) / 2
        color = QtGui.QColor()

        painter = QtGui.QPainter(self)
        
        for i in xrange(self.text.size()):
            index = (self.step + i) % 16
            color.setHsv((15 - index) * 16, 255, 191)
            painter.setPen(color)
            painter.drawText(x, y - ((sineTable[index] * metrics.height()) / 400), QtCore.QString(self.text[i]))
            x += metrics.width(self.text[i])
    
    def setText(self, newText):
        self.text = QtCore.QString(newText)

    def timerEvent(self, event):
        if (event.timerId() == self.timer.timerId()):
            self.step = self.step + 1
            self.update()
        else:
            QtGui.QWidget.timerEvent(event)


class Dialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        
        wigglyWidget = WigglyWidget()
        lineEdit = QtGui.QLineEdit()

        layout = QtGui.QVBoxLayout()
        layout.addWidget(wigglyWidget)
        layout.addWidget(lineEdit)
        self.setLayout(layout)

        self.connect(lineEdit, QtCore.SIGNAL("textChanged(QString)"), wigglyWidget.setText)

        lineEdit.setText(self.tr("Hello world!"))

        self.setWindowTitle(self.tr("Wiggly"))
        self.resize(360, 145)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    dialog = Dialog()
    dialog.show();
    sys.exit(dialog.exec_())    
