#!/usr/bin/env python

import sys

from PyQt4 import QtCore, QtGui, uic


app = QtGui.QApplication(sys.argv)
form_class, base_class = uic.loadUiType('demo.ui')


class DemoImpl(QtGui.QDialog, form_class):
    def __init__(self, *args):
        super(DemoImpl, self).__init__(*args)

        self.setupUi(self)
    
    @QtCore.pyqtSlot()
    def on_button1_clicked(self):
        for s in "This is a demo".split(" "):
            self.list.addItem(s)


form = DemoImpl()
form.show()
sys.exit(app.exec_())
