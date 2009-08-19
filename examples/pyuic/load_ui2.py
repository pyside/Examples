#!/usr/bin/env python

import sys

from PyQt4 import QtCore, QtGui, uic


class DemoImpl(QtGui.QDialog):
    def __init__(self, *args):
        super(DemoImpl, self).__init__(*args)

        uic.loadUi('demo.ui', self)

    @QtCore.pyqtSlot()
    def on_button1_clicked(self):
        for s in "This is a demo".split(" "):
            self.list.addItem(s)


app = QtGui.QApplication(sys.argv)
widget = DemoImpl()
widget.show()
sys.exit(app.exec_())
