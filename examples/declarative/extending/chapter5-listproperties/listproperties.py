#!/usr/bin/python

# Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
# All rights reserved.
# Contact: PySide Team (pyside@openbossa.org)
#
# This file is part of the examples of PySide: Python for Qt.
#
# You may use this file under the terms of the BSD license as follows:
#
# "Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#   * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in
#     the documentation and/or other materials provided with the
#     distribution.
#   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
#     the names of its contributors may be used to endorse or promote
#     products derived from this software without specific prior written
#     permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."

import sys
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtDeclarative import *


class PieSlice (QDeclarativeItem):

    def __init__(self, parent=None):
        QDeclarativeItem.__init__(self, parent)
        # need to disable this flag to draw inside a QDeclarativeItem
        self.setFlag(QGraphicsItem.ItemHasNoContents, False)
        self._color = QColor()
        self._fromAngle = 0
        self._angleSpan = 0

    def getColor(self):
        return self._color

    def setColor(self, value):
        self._color = value

    def getFromAngle(self):
        return self._angle

    def setFromAngle(self, value):
        self._fromAngle = value

    def getAngleSpan(self):
        return self._angleSpan

    def setAngleSpan(self, value):
        self._angleSpan = value

    color = Property(QColor, getColor, setColor)
    fromAngle = Property(int, getFromAngle, setFromAngle)
    angleSpan = Property(int, getAngleSpan, setAngleSpan)

    def paint(self, painter, options, widget):
        pen = QPen(self._color, 2)
        painter.setPen(pen)
        painter.setRenderHints(QPainter.Antialiasing, True)
        painter.drawPie(
            self.boundingRect(), self._fromAngle * 16, self._angleSpan * 16)


class PieChart (QDeclarativeItem):

    def __init__(self, parent=None):
        QDeclarativeItem.__init__(self, parent)
        self._name = u''
        self._slices = []

    def getName(self):
        return self._name

    def setName(self, value):
        self._name = value

    name = Property(unicode, getName, setName)

    def appendSlice(self, _slice):
        _slice.setParentItem(self)
        self._slices.append(_slice)

    slices = ListProperty(PieSlice, appendSlice)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    qmlRegisterType(PieChart, 'Charts', 1, 0, 'PieChart')
    qmlRegisterType(PieSlice, "Charts", 1, 0, "PieSlice")

    view = QDeclarativeView()
    view.setSource(QUrl.fromLocalFile('app.qml'))
    view.show()
    sys.exit(app.exec_())
