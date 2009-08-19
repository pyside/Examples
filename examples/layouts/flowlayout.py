#!/usr/bin/env python

"""PySide port of the layouts/flowlayout example from Qt v4.x"""

import sys
from PySide import QtCore, QtGui


class Window(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        flowLayout = FlowLayout()
        flowLayout.addWidget(QtGui.QPushButton(self.tr("Short")))
        flowLayout.addWidget(QtGui.QPushButton(self.tr("Longer")))
        flowLayout.addWidget(QtGui.QPushButton(self.tr("Different text")))
        flowLayout.addWidget(QtGui.QPushButton(self.tr("More text")))
        flowLayout.addWidget(QtGui.QPushButton(self.tr("Even longer button text")))
        self.setLayout(flowLayout)

        self.setWindowTitle(self.tr("Flow Layout"))


class FlowLayout(QtGui.QLayout):
    def __init__(self, parent=None, margin=0, spacing=-1):
        QtGui.QLayout.__init__(self, parent)

        if parent is not None:
            self.setMargin(margin)
        self.setSpacing(spacing)

        self.itemList = []

    def addItem(self, item):
        self.itemList.append(item)

    def count(self):
        return len(self.itemList)

    def itemAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList[index]

    def takeAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList.pop(index)

    def expandingDirections(self):
        return QtCore.Qt.Orientations(QtCore.Qt.Orientation(0))

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self.doLayout(QtCore.QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect):
        QtGui.QLayout.setGeometry(self, rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QtCore.QSize()

        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())

        size += QtCore.QSize(2 * self.margin(), 2 * self.margin())
        return size

    def doLayout(self, rect, testOnly):
        x = rect.x()
        y = rect.y()
        lineHeight = 0

        for item in self.itemList:
            nextX = x + item.sizeHint().width() + self.spacing()
            if nextX - self.spacing() > rect.right() and lineHeight > 0:
                x = rect.x()
                y = y + lineHeight + self.spacing()
                nextX = x + item.sizeHint().width() + self.spacing()
                lineHeight = 0

            if not testOnly:
                item.setGeometry(QtCore.QRect(QtCore.QPoint(x, y), item.sizeHint()))

            x = nextX
            lineHeight = max(lineHeight, item.sizeHint().height())

        return y + lineHeight - rect.y()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mainWin = Window()
    mainWin.show()
    sys.exit(app.exec_())
