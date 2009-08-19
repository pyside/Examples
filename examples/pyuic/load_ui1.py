#!/usr/bin/env python

import sys

from PyQt4 import QtGui, uic


app = QtGui.QApplication(sys.argv)
widget = uic.loadUi('demo.ui')
widget.show()
sys.exit(app.exec_())
