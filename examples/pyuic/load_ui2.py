#!/usr/bin/env python
import sys

from PySide import QtCore, QtGui, uic


class DemoImpl(QtGui.QDialog):
    def __init__(self, *args):
        QtGui.QWidget.__init__(self, *args)
        uic.loadUi("demo.ui", self)

    @QtCore.pyqtSignature("")
    def on_button1_clicked(self):
        for s in "This is a demo".split(" "):
            self.list.addItem(s)


app = QtGui.QApplication(sys.argv)
widget = DemoImpl()
widget.show()
app.exec_()
