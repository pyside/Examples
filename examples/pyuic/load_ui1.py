#!/usr/bin/env python
import sys

from PySide import QtGui, uic


app = QtGui.QApplication(sys.argv)
widget = uic.loadUi("demo.ui")
widget.show()
app.exec_()
