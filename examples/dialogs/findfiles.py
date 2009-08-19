#!/usr/bin/env python

"""PySide port of the dialogs/findfiles example from Qt v4.x"""

import sys
from PySide import QtCore, QtGui


class Window(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.browseButton = self.createButton(self.tr("&Browse..."), self.browse)
        self.findButton = self.createButton(self.tr("&Find"), self.find)
        self.quitButton = self.createButton(self.tr("&Quit"), QtCore.SLOT("close()"))
    
        self.fileComboBox = self.createComboBox(self.tr("*"))
        self.textComboBox = self.createComboBox()
        self.directoryComboBox = self.createComboBox(QtCore.QDir.currentPath())
    
        self.fileLabel = QtGui.QLabel(self.tr("Named:"))
        self.textLabel = QtGui.QLabel(self.tr("Containing text:"))
        self.directoryLabel = QtGui.QLabel(self.tr("In directory:"))
        self.filesFoundLabel = QtGui.QLabel()
    
        self.createFilesTable()
    
        buttonsLayout = QtGui.QHBoxLayout()
        buttonsLayout.addStretch()
        buttonsLayout.addWidget(self.findButton)
        buttonsLayout.addWidget(self.quitButton)
    
        mainLayout = QtGui.QGridLayout()
        mainLayout.addWidget(self.fileLabel, 0, 0)
        mainLayout.addWidget(self.fileComboBox, 0, 1, 1, 2)
        mainLayout.addWidget(self.textLabel, 1, 0)
        mainLayout.addWidget(self.textComboBox, 1, 1, 1, 2)
        mainLayout.addWidget(self.directoryLabel, 2, 0)
        mainLayout.addWidget(self.directoryComboBox, 2, 1)
        mainLayout.addWidget(self.browseButton, 2, 2)
        mainLayout.addWidget(self.filesTable, 3, 0, 1, 3)
        mainLayout.addWidget(self.filesFoundLabel, 4, 0)
        mainLayout.addLayout(buttonsLayout, 5, 0, 1, 3)
        self.setLayout(mainLayout)
    
        self.setWindowTitle(self.tr("Find Files"))
        self.resize(700, 300)
    
    def browse(self):
        directory = QtGui.QFileDialog.getExistingDirectory(self, self.tr("Find Files"),
                                                           QtCore.QDir.currentPath())
        self.directoryComboBox.addItem(directory)
        self.directoryComboBox.setCurrentIndex(self.directoryComboBox.currentIndex() + 1)
    
    def find(self):
        self.filesTable.setRowCount(0)
    
        fileName = QtCore.QString(self.fileComboBox.currentText())
        text = QtCore.QString(self.textComboBox.currentText())
        path = QtCore.QString(self.directoryComboBox.currentText())
    
        directory = QtCore.QDir(path)
        files = QtCore.QStringList()
        if fileName.isEmpty():
            fileName = "*"
        files = directory.entryList(QtCore.QStringList(fileName),
                                    QtCore.QDir.Files | QtCore.QDir.NoSymLinks)
    
        if not text.isEmpty():
            files = self.findFiles(directory, files, text)
        self.showFiles(directory, files)
    
    def findFiles(self, directory, files, text):
        progressDialog = QtGui.QProgressDialog(self)
        
        progressDialog.setCancelButtonText(self.tr("&Cancel"))
        progressDialog.setRange(0, files.count())
        progressDialog.setWindowTitle(self.tr("Find Files"))
    
        foundFiles = QtCore.QStringList()
    
        for i in range(files.count()):
            progressDialog.setValue(i)
            progressDialog.setLabelText(self.tr("Searching file number %1 of %2...")
                                                .arg(i).arg(files.count()))
            QtGui.qApp.processEvents()
    
            if progressDialog.wasCanceled():
                break
    
            inFile = QtCore.QFile(directory.absoluteFilePath(files[i]))
    
            if inFile.open(QtCore.QIODevice.ReadOnly):
                line = QtCore.QString()
                stream = QtCore.QTextStream(inFile)
                while not stream.atEnd():
                    if progressDialog.wasCanceled():
                        break
                    line = stream.readLine()
                    if line.contains(text):
                        foundFiles << files[i]
                        break
        
        progressDialog.close()
        
        return foundFiles
    
    def showFiles(self, directory, files):
        for i in range(files.count()):
            file = QtCore.QFile(directory.absoluteFilePath(files[i]))
            size = QtCore.QFileInfo(file).size()
    
            fileNameItem = QtGui.QTableWidgetItem(files[i])
            fileNameItem.setFlags(QtCore.Qt.ItemIsEnabled)
            sizeItem = QtGui.QTableWidgetItem(QtCore.QString("%1 KB").arg(int((size + 1023) / 1024)))
            sizeItem.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
            sizeItem.setFlags(QtCore.Qt.ItemIsEnabled)
    
            row = self.filesTable.rowCount()
            self.filesTable.insertRow(row)
            self.filesTable.setItem(row, 0, fileNameItem)
            self.filesTable.setItem(row, 1, sizeItem)
    
        self.filesFoundLabel.setText(self.tr("%1 file(s) found").arg(files.count()))
    
    def createButton(self, text, member):
        button = QtGui.QPushButton(text)
        self.connect(button, QtCore.SIGNAL("clicked()"), member)
        return button
    
    def createComboBox(self, text=""):
        comboBox = QtGui.QComboBox()
        comboBox.setEditable(True)
        comboBox.addItem(text)
        comboBox.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        return comboBox
    
    def createFilesTable(self):
        self.filesTable = QtGui.QTableWidget(0, 2)
        labels = QtCore.QStringList()
        labels << self.tr("File Name") << self.tr("Size")
        self.filesTable.setHorizontalHeaderLabels(labels)
        self.filesTable.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.Stretch)
        self.filesTable.verticalHeader().hide()
        self.filesTable.setShowGrid(False)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
