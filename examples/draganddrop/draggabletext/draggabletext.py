#!/usr/bin/env python

"""***************************************************************************
**
** Copyright (C) 2005-2005 Trolltech AS. All rights reserved.
**
** This file is part of the example classes of the Qt Toolkit.
**
** This file may be used under the terms of the GNU General Public
** License version 2.0 as published by the Free Software Foundation
** and appearing in the file LICENSE.GPL included in the packaging of
** this file.  Please review the following information to ensure GNU
** General Public Licensing requirements will be met:
** http://www.trolltech.com/products/qt/opensource.html
**
** If you are unsure which license is appropriate for your use, please
** review the following information:
** http://www.trolltech.com/products/qt/licensing.html or contact the
** sales department at sales@trolltech.com.
**
** This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
** WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
**
***************************************************************************"""

import sys
from PySide import QtCore, QtGui

import draggabletext_rc


class DragLabel(QtGui.QLabel):
    def __init__(self, text, parent=None):
        QtGui.QLabel.__init__(self, text, parent)

        self.setFrameShape(QtGui.QFrame.Panel)
        self.setFrameShadow(QtGui.QFrame.Raised)

    def mousePressEvent(self, event):
        plainText = self.text() # for quoting purposes

        mimeData = QtCore.QMimeData()
        mimeData.setText(plainText)

        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(event.pos() - self.rect().topLeft())

        dropAction = drag.exec_(QtCore.Qt.CopyAction | QtCore.Qt.MoveAction)

        if dropAction == QtCore.Qt.MoveAction:
            self.close()
            self.update()


class DragWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        dictionaryFile = QtCore.QFile(":/dictionary/words.txt")
        dictionaryFile.open(QtCore.QIODevice.ReadOnly)
        inputStream = QtCore.QTextStream(dictionaryFile)

        x = 5
        y = 5

        while not inputStream.atEnd():
            word = QtCore.QString()
            inputStream >> word
            if not word.isEmpty():
                wordLabel = DragLabel(word, self)
                wordLabel.move(x, y)
                wordLabel.show()
                x += wordLabel.width() + 2
                if x >= 195:
                    x = 5
                    y += wordLabel.height() + 2

        newPalette = self.palette()
        newPalette.setColor(QtGui.QPalette.Background, QtCore.Qt.white)
        self.setPalette(newPalette)

        self.setAcceptDrops(True)
        self.setMinimumSize(400, max(200, y))
        self.setWindowTitle(self.tr("Draggable Text"))

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasText():
            pieces = event.mimeData().text().split(QtCore.QRegExp("\\s+"),
                                 QtCore.QString.SkipEmptyParts)
            position = event.pos()

            for piece in pieces:
                newLabel = DragLabel(piece, self)
                newLabel.move(position)
                newLabel.show()

                position += QtCore.QPoint(newLabel.width(), 0)

            if event.source() in self.children():
                event.setDropAction(QtCore.Qt.MoveAction)
                event.accept()
            else:
                event.acceptProposedAction()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = DragWidget()
    window.show()
    sys.exit(app.exec_())
