#!/usr/bin/env python

"""PySide port of the tools/codecs example from Qt v4.x"""

import sys
from PySide import QtCore, QtGui


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.textEdit = QtGui.QTextEdit()
        self.textEdit.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.setCentralWidget(self.textEdit)
        self.codecs = []
        self.findCodecs()
        self.previewForm = PreviewForm(self)
        self.previewForm.setCodecList(self.codecs)
        self.saveAsActs = []
        self.createActions()
        self.createMenus()
        self.setWindowTitle(self.tr("Codecs"))
        self.resize(500, 400)
    
    def open(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self)
        if not fileName.isEmpty():
            inFile = QtCore.QFile(fileName)
            if not inFile.open(QtCore.QFile.ReadOnly):
                QtGui.QMessageBox.warning(self, self.tr("Codecs"),
                                          self.tr("Cannot read file %1:\n%2")
                                          .arg(fileName).arg(inFile.errorString()))
                return
            data = inFile.readAll()
            self.previewForm.setEncodedData(data)
            if self.previewForm.exec_():
                self.textEdit.setPlainText(self.previewForm.decodedString())
                
    def save(self):
        fileName = QtGui.QFileDialog.getSaveFileName(self)
        if not fileName.isEmpty():
            outFile = QtCore.QFile(fileName)
            if not outFile.open(QtCore.QFile.WriteOnly):
                QtGui.QMessageBox.warning(self, self.tr("Codecs"),
                                          self.tr("Cannot write file %1:\n%2")
                                          .arg(fileName).arg(outFile.errorString()))
                return
            action = self.sender()
            codecName = action.data().toByteArray()
            out = QtCore.QTextStream(outFile)
            out.setCodec(codecName.data())
            out << self.textEdit.toPlainText()
            
    def about(self):
        QtGui.QMessageBox.about(self, self.tr("About Codecs"), self.tr(
                                "The <b>Codecs</b> example demonstrates how to "
                                "read and write files using various encodings."))
            
    def aboutToShowSaveAsMenu(self):
        currentText = self.textEdit.toPlainText()
        for action in self.saveAsActs:
            codecName = action.data().toByteArray()
            codec = QtCore.QTextCodec.codecForName(codecName)
            action.setVisible(codec and codec.canEncode(currentText))
            
    def findCodecs(self):
        codecMap = []
        iso8859RegExp = QtCore.QRegExp("ISO[- ]8859-([0-9]+).*")
        for mib in QtCore.QTextCodec.availableMibs():
            codec = QtCore.QTextCodec.codecForMib(mib)
            sortKey = codec.name().toUpper().data()
            rank = 0
            if sortKey.startswith("UTF-8"):
                rank = 1
            elif sortKey.startswith("UTF-16"):
                rank = 2
            elif iso8859RegExp.exactMatch(sortKey):
                if iso8859RegExp.cap(1).size() == 1:
                    rank = 3
                else:
                    rank = 4
            else:
                rank = 5
            codecMap.append((str(rank) + sortKey, codec))
        codecMap.sort()
        self.codecs = [item[-1] for item in codecMap]
        
    def createActions(self):
        self.openAct = QtGui.QAction(self.tr("&Open..."), self)
        self.openAct.setShortcut(self.tr("Ctrl+O"))
        self.connect(self.openAct, QtCore.SIGNAL("triggered()"), self.open)
        for codec in self.codecs:
            text = self.tr("%1...").arg(QtCore.QString(codec.name()))
            action = QtGui.QAction(text, self)
            action.setData(QtCore.QVariant(codec.name()))
            self.connect(action, QtCore.SIGNAL("triggered()"), self.save)
            self.saveAsActs.append(action)

        self.exitAct = QtGui.QAction(self.tr("E&xit"), self)
        self.exitAct.setShortcut(self.tr("Ctrl+Q"))
        self.connect(self.exitAct, QtCore.SIGNAL("triggered()"),
                     self, QtCore.SLOT("close()"))
        self.aboutAct = QtGui.QAction(self.tr("&About"), self)
        self.connect(self.aboutAct, QtCore.SIGNAL("triggered()"),
                     self.about)
        self.aboutQtAct = QtGui.QAction(self.tr("About &Qt"), self)
        self.connect(self.aboutQtAct, QtCore.SIGNAL("triggered()"),
                     QtGui.qApp, QtCore.SLOT("aboutQt()"))
        
    def createMenus(self):
        self.saveAsMenu = QtGui.QMenu(self.tr("&Save As"), self)
        for action in self.saveAsActs:
            self.saveAsMenu.addAction(action)

        self.connect(self.saveAsMenu, QtCore.SIGNAL("aboutToShow()"),
                     self.aboutToShowSaveAsMenu)
        self.fileMenu = QtGui.QMenu(self.tr("&File"), self)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addMenu(self.saveAsMenu)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)
        self.helpMenu = QtGui.QMenu(self.tr("&Help"), self)
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)
        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.helpMenu)


class PreviewForm(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        
        self.encodingComboBox = QtGui.QComboBox()
        self.encodingLabel = QtGui.QLabel(self.tr("&Encoding:"))
        self.encodingLabel.setBuddy(self.encodingComboBox)
        
        self.textEdit = QtGui.QTextEdit()
        self.textEdit.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.textEdit.setReadOnly(True)
        
        self.okButton = QtGui.QPushButton(self.tr("OK"))
        self.cancelButton = QtGui.QPushButton(self.tr("Cancel"))
        self.okButton.setDefault(True)
        
        self.connect(self.encodingComboBox, QtCore.SIGNAL("activated(int)"),
                     self.updateTextEdit)
        self.connect(self.okButton, QtCore.SIGNAL("clicked()"),
                     self, QtCore.SLOT("accept()"))
        self.connect(self.cancelButton, QtCore.SIGNAL("clicked()"),
                     self, QtCore.SLOT("reject()"))
        
        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(self.okButton)
        buttonLayout.addWidget(self.cancelButton)
        
        mainLayout = QtGui.QGridLayout()
        mainLayout.addWidget(self.encodingLabel, 0, 0)
        mainLayout.addWidget(self.encodingComboBox, 0, 1)
        mainLayout.addWidget(self.textEdit, 1, 0, 1, 2)
        mainLayout.addLayout(buttonLayout, 2, 0, 1, 2)
        self.setLayout(mainLayout)
        
        self.setWindowTitle(self.tr("Choose Encoding"))
        self.resize(400, 300)
        
    def setCodecList(self, codecs):
        self.encodingComboBox.clear()
        for codec in codecs:
            self.encodingComboBox.addItem(QtCore.QString(codec.name()),
                                          QtCore.QVariant(codec.mibEnum()))
            
    def setEncodedData(self, data):
        self.encodedData = data
        self.updateTextEdit()
    
    def decodedString(self):
        return self.decodedStr
    
    def updateTextEdit(self):
        mib,ok = self.encodingComboBox.itemData(self.encodingComboBox.currentIndex()).toInt()
        codec = QtCore.QTextCodec.codecForMib(mib)
        
        data = QtCore.QTextStream(self.encodedData)
        data.setAutoDetectUnicode(False)
        data.setCodec(codec)
        
        self.decodedStr = data.readAll()
        self.textEdit.setPlainText(self.decodedStr)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
