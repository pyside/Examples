#!/usr/bin/env python

############################################################################
# 
#  Copyright (C) 2004-2005 Trolltech AS. All rights reserved.
# 
#  This file is part of the example classes of the Qt Toolkit.
# 
#  This file may be used under the terms of the GNU General Public
#  License version 2.0 as published by the Free Software Foundation
#  and appearing in the file LICENSE.GPL included in the packaging of
#  self file.  Please review the following information to ensure GNU
#  General Public Licensing requirements will be met:
#  http://www.trolltech.com/products/qt/opensource.html
# 
#  If you are unsure which license is appropriate for your use, please
#  review the following information:
#  http://www.trolltech.com/products/qt/licensing.html or contact the
#  sales department at sales@trolltech.com.
# 
#  This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
#  WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
# 
############################################################################

import sys
from PySide import QtCore, QtGui

import sdi_rc


class MainWindow(QtGui.QMainWindow):
    sequenceNumber = 1
    windowList = []

    def __init__(self, fileName=None, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        self.init()
        if fileName:
            self.loadFile(fileName)
        else:
            self.setCurrentFile(QtCore.QString())
        
    def closeEvent(self, event):
        if self.maybeSave():
            self.writeSettings()
            event.accept()
        else:
            event.ignore()
            
    def newFile(self):
        other = MainWindow()
        MainWindow.windowList.append(other)
        other.move(self.x()+40, self.y()+40)
        other.show()
            
    def open(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self)
        if not fileName.isEmpty():
            existing = self.findMainWindow(fileName)
            if existing:
                existing.show()
                existing.raise_()
                existing.activateWindow()
                return

            if self.isUntitled and self.textEdit.document().isEmpty() and not self.isWindowModified():
                self.loadFile(fileName)
            else:
                other = MainWindow(fileName)
                if other.isUntitled:
                    del other
                    return

                MainWindow.windowList.append(other)
                other.move(self.x() + 40, self.y() + 40)
                other.show()
        	
    def save(self):
        if self.isUntitled:
            return self.saveAs()
        else:
            return self.saveFile(self.curFile)

    def saveAs(self):
        fileName = QtGui.QFileDialog.getSaveFileName(self, self.tr("Save As"), 
                                                     self.curFile)
        if fileName.isEmpty():
            return False

        return self.saveFile(fileName)
                
    def about(self):
        QtGui.QMessageBox.about(self, self.tr("About SDI"),
            self.tr("The <b>SDI</b> example demonstrates how to write single "
                    "document interface applications using Qt."))
        
    def documentWasModified(self):
        self.setWindowModified(True)
        
    def init(self):
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.isUntitled = True
        self.textEdit = QtGui.QTextEdit()
        self.setCentralWidget(self.textEdit)
        
        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        
        self.readSettings()
        
        self.connect(self.textEdit.document(), QtCore.SIGNAL("contentsChanged()"), 
                     self.documentWasModified)
        
    def createActions(self):
        self.newAct = QtGui.QAction(QtGui.QIcon(":/images/new.png"),self.tr("&New"), self)
        self.newAct.setShortcut(self.tr("Ctrl+N"))
        self.newAct.setStatusTip(self.tr("Create a new file"))
        self.connect(self.newAct, QtCore.SIGNAL("triggered()"), self.newFile)

        self.openAct = QtGui.QAction(QtGui.QIcon(":/images/open.png"),self.tr("&Open..."), self)
        self.openAct.setShortcut(self.tr("Ctrl+O"))
        self.openAct.setStatusTip(self.tr("Open an existing file"))
        self.connect(self.openAct, QtCore.SIGNAL("triggered()"), self.open)

        self.saveAct = QtGui.QAction(QtGui.QIcon(":/images/save.png"),self.tr("&Save"), self)
        self.saveAct.setShortcut(self.tr("Ctrl+S"))
        self.saveAct.setStatusTip(self.tr("Save the document to disk"))
        self.connect(self.saveAct, QtCore.SIGNAL("triggered()"), self.save)

        self.saveAsAct = QtGui.QAction(self.tr("Save &As..."), self)
        self.saveAsAct.setStatusTip(self.tr("Save the document under a new name"))
        self.connect(self.saveAsAct, QtCore.SIGNAL("triggered()"), self.saveAs)

        self.closeAct = QtGui.QAction(self.tr("&Close"), self)
        self.closeAct.setShortcut(self.tr("Ctrl+W"))
        self.closeAct.setStatusTip(self.tr("Close this window"))
        self.connect(self.closeAct, QtCore.SIGNAL("triggered()"), self.close)

        self.exitAct = QtGui.QAction(self.tr("E&xit"), self)
        self.exitAct.setShortcut(self.tr("Ctrl+Q"))
        self.exitAct.setStatusTip(self.tr("Exit the application"))
        self.connect(self.exitAct, QtCore.SIGNAL("triggered()"), 
                     QtGui.qApp.closeAllWindows)
        
        self.cutAct = QtGui.QAction(QtGui.QIcon(":/images/cut.png"),self.tr("Cu&t"),
                                    self)
        self.cutAct.setShortcut(self.tr("Ctrl+X"))
        self.cutAct.setStatusTip(self.tr("Cut the current selection's "
                                         "contents to the clipboard"))
        self.connect(self.cutAct, QtCore.SIGNAL("triggered()"), self.textEdit.cut)

        self.copyAct = QtGui.QAction(QtGui.QIcon(":/images/copy.png"),self.tr("&Copy"),
                                     self)
        self.copyAct.setShortcut(self.tr("Ctrl+C"))
        self.copyAct.setStatusTip(self.tr("Copy the current selection's "
                                          "contents to the clipboard"))
        self.connect(self.copyAct, QtCore.SIGNAL("triggered()"), self.textEdit.copy)

        self.pasteAct = QtGui.QAction(QtGui.QIcon(":/images/paste.png"), 
                                      self.tr("&Paste"), self)
        self.pasteAct.setShortcut(self.tr("Ctrl+V"))
        self.pasteAct.setStatusTip(self.tr("Paste the clipboard's contents "
                                           "into the current selection"))
        self.connect(self.pasteAct, QtCore.SIGNAL("triggered()"), self.textEdit.paste)

        self.aboutAct = QtGui.QAction(self.tr("&About"), self)
        self.aboutAct.setStatusTip(self.tr("Show the application's About box"))
        self.connect(self.aboutAct, QtCore.SIGNAL("triggered()"), self.about)

        self.aboutQtAct = QtGui.QAction(self.tr("About &Qt"), self)
        self.aboutQtAct.setStatusTip(self.tr("Show the Qt library's About box"))
        self.connect(self.aboutQtAct, QtCore.SIGNAL("triggered()"), QtGui.qApp.aboutQt)

        self.cutAct.setEnabled(False)
        self.copyAct.setEnabled(False)
        self.connect(self.textEdit, QtCore.SIGNAL("copyAvailable(bool)"),
                self.cutAct.setEnabled)
        self.connect(self.textEdit, QtCore.SIGNAL("copyAvailable(bool)"),
                self.copyAct.setEnabled)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu(self.tr("&File"))
        self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.saveAsAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.closeAct)
        self.fileMenu.addAction(self.exitAct)

        self.editMenu = self.menuBar().addMenu(self.tr("&Edit"))
        self.editMenu.addAction(self.cutAct)
        self.editMenu.addAction(self.copyAct)
        self.editMenu.addAction(self.pasteAct)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu(self.tr("&Help"))
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

    def createToolBars(self):
        self.fileToolBar = self.addToolBar(self.tr("File"))
        self.fileToolBar.addAction(self.newAct)
        self.fileToolBar.addAction(self.openAct)
        self.fileToolBar.addAction(self.saveAct)
        
        self.editToolBar = self.addToolBar(self.tr("Edit"))
        self.editToolBar.addAction(self.cutAct)
        self.editToolBar.addAction(self.copyAct)
        self.editToolBar.addAction(self.pasteAct)
        
    def createStatusBar(self):
        self.statusBar().showMessage(self.tr("Ready"))
        
    def readSettings(self):
        settings = QtCore.QSettings("Trolltech", "SDI Example")
        pos = settings.value("pos", QtCore.QVariant(QtCore.QPoint(200, 200))).toPoint()
        size = settings.value("size", QtCore.QVariant(QtCore.QSize(400, 400))).toSize()
        self.resize(size)
        self.move(pos)
        
    def writeSettings(self):
        settings = QtCore.QSettings("Trolltech", "SDI Example")
        settings.setValue("pos", QtCore.QVariant(self.pos()))
        settings.setValue("size", QtCore.QVariant(self.size()))
        
    def maybeSave(self):
        if self.textEdit.document().isModified():
            ret = QtGui.QMessageBox.warning(self, self.tr("SDI"),
                    self.tr("The document has been modified.\n"
                            "Do you want to save your changes?"),
                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.Default,
                    QtGui.QMessageBox.No,
                    QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Escape)
            if ret == QtGui.QMessageBox.Yes:
                return save()
            elif ret == QtGui.QMessageBox.Cancel:
                return False
        return True
        
    def loadFile(self, fileName):
        file = QtCore.QFile(fileName)
        if not file.open( QtCore.QFile.ReadOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, self.tr("SDI"),
                    self.tr("Cannot read file %1:\n%2.").arg(fileName).arg(file.errorString()))
            return

        instr = QtCore.QTextStream(file)
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        self.textEdit.setPlainText(instr.readAll())
        QtGui.QApplication.restoreOverrideCursor()
        
        self.setCurrentFile(fileName)
        self.statusBar().showMessage(self.tr("File loaded"), 2000)
        
    def saveFile(self, fileName):
        file = QtCore.QFile(fileName)
        if not file.open( QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, self.tr("SDI"),
                    self.tr("Cannot write file %1:\n%2.").arg(fileName).arg(file.errorString()))
            return False

        outstr = QtCore.QTextStream(file)
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        outstr << self.textEdit.toPlainText()
        QtGui.QApplication.restoreOverrideCursor()
        
        self.setCurrentFile(fileName)
        self.statusBar().showMessage(self.tr("File saved"), 2000)
        return True
    
    def setCurrentFile(self, fileName):
        self.isUntitled = fileName.isEmpty()
        if self.isUntitled:
            self.curFile = self.tr("document%1.txt").arg(MainWindow.sequenceNumber)
            MainWindow.sequenceNumber += 1
        else:
            self.curFile = QtCore.QFileInfo(fileName).canonicalFilePath()
        
        self.textEdit.document().setModified(False)
        self.setWindowModified(False)
        self.setWindowTitle(self.tr("%1[*] - %2")
            .arg(self.strippedName(self.curFile)).arg(self.tr("SDI")))
        
    def strippedName(self, fullFileName):
        return QtCore.QFileInfo(fullFileName).fileName()
    
    def findMainWindow(self, fileName):
        canonicalFilePath = QtCore.QFileInfo(fileName).canonicalFilePath()
        
        for widget in QtGui.qApp.topLevelWidgets():
            if isinstance(widget, MainWindow) and widget.curFile == canonicalFilePath:
                return widget
        return 0

        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())
