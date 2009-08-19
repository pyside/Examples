#!/bin/env python

############################################################################
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
############################################################################

import sys
from PySide import QtCore, QtGui, QtSql

import connection


class TableEditor(QtGui.QDialog):
    def __init__(self, tableName, parent = None):
        QtGui.QDialog.__init__(self, parent)
        
        self.model = QtSql.QSqlTableModel(self)
        self.model.setTable(tableName)
        self.model.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.model.select()
        
        self.model.setHeaderData(0, QtCore.Qt.Horizontal,
                                 QtCore.QVariant(self.tr("ID")))
        self.model.setHeaderData(1, QtCore.Qt.Horizontal,
                                 QtCore.QVariant(self.tr("First name")))
        self.model.setHeaderData(2, QtCore.Qt.Horizontal,
                                 QtCore.QVariant(self.tr("Last name")))
        
        view = QtGui.QTableView()
        view.setModel(self.model)
        
        self.submitButton = QtGui.QPushButton(self.tr("Submit"))
        self.submitButton.setDefault(True)
        self.revertButton = QtGui.QPushButton(self.tr("&Revert"))
        self.quitButton = QtGui.QPushButton(self.tr("Quit"))
        
        self.connect(self.submitButton, QtCore.SIGNAL("clicked()"), self.submit)
        self.connect(self.revertButton, QtCore.SIGNAL("clicked()"), 
                     self.model.revertAll)
        self.connect(self.quitButton, QtCore.SIGNAL("clicked()"), self.close)
        
        buttonLayout = QtGui.QVBoxLayout()
        buttonLayout.addWidget(self.submitButton)
        buttonLayout.addWidget(self.revertButton)
        buttonLayout.addWidget(self.quitButton)
        buttonLayout.addStretch(1)
        
        mainLayout = QtGui.QHBoxLayout()
        mainLayout.addWidget(view)
        mainLayout.addLayout(buttonLayout)
        self.setLayout(mainLayout)
        
        self.setWindowTitle(self.tr("Cached Table"))
        
    def submit(self):
        self.model.database().transaction()
        if self.model.submitAll():
            self.model.database().commit()
        else:
            self.model.database().rollback()
            QtGui.QMessageBox.warning(self, self.tr("Cached Table"),
                        self.tr("The database reported an error: %1")
                                .arg(self.model.lastError().text()))

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    if not connection.createConnection():
        sys.exit(1)
    editor = TableEditor("person")
    editor.show()
    sys.exit(editor.exec_())
