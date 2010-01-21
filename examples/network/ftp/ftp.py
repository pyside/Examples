#!/usr/bin/env python

"""PySide port of the network/ftp example from Qt v4.x"""

import sys
from PySide import QtCore, QtGui, QtNetwork

import ftp_rc


class FtpWindow(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
    
        self.ftpServerLabel = QtGui.QLabel(self.tr("Ftp &server:"))
        self.ftpServerLineEdit = QtGui.QLineEdit("ftp.trolltech.com")
        self.ftpServerLabel.setBuddy(self.ftpServerLineEdit)
    
        self.statusLabel = QtGui.QLabel(self.tr("Please enter the name of an FTP server."))
    
        self.fileList = QtGui.QListWidget()
    
        self.connectButton = QtGui.QPushButton(self.tr("Connect"))
        self.connectButton.setDefault(True)
    
        self.downloadButton = QtGui.QPushButton(self.tr("Download"))
        self.downloadButton.setEnabled(False)
        
        self.cdToParentButton = QtGui.QPushButton()
        self.cdToParentButton.setIcon(QtGui.QIcon(":/images/cdtoparent.png"))
        self.cdToParentButton.setEnabled(False)
    
        self.quitButton = QtGui.QPushButton(self.tr("Quit"))
    
        self.isDirectory = {}
        self.currentPath = QtCore.QString()
        self.ftp = QtNetwork.QFtp(self)
        self.outFile = None
    
        self.progressDialog = QtGui.QProgressDialog(self)
    
        self.connect(self.ftpServerLineEdit, QtCore.SIGNAL("textChanged(QString &)"),
                     self.enableConnectButton)
        self.connect(self.fileList, QtCore.SIGNAL("itemDoubleClicked(QListWidgetItem *)"),
                     self.processItem)
        self.connect(self.fileList, QtCore.SIGNAL("itemEntered(QListWidgetItem *)"),
                     self.processItem)
        self.connect(self.fileList, QtCore.SIGNAL("itemSelectionChanged()"), self.enableDownloadButton)
        self.connect(self.ftp, QtCore.SIGNAL("commandFinished(int, bool)"), self.ftpCommandFinished)
        self.connect(self.ftp, QtCore.SIGNAL("listInfo(const QUrlInfo &)"), self.addToList)
        self.connect(self.ftp, QtCore.SIGNAL("dataTransferProgress(qint64, qint64)"),
                     self.updateDataTransferProgress)
        self.connect(self.progressDialog, QtCore.SIGNAL("canceled()"), self.cancelDownload)
        self.connect(self.connectButton, QtCore.SIGNAL("clicked()"), self.connectToFtpServer)
        self.connect(self.cdToParentButton, QtCore.SIGNAL("clicked()"), self.cdToParent)
        self.connect(self.downloadButton, QtCore.SIGNAL("clicked()"), self.downloadFile)
        self.connect(self.quitButton, QtCore.SIGNAL("clicked()"), self, QtCore.SLOT("close()"))
    
        topLayout = QtGui.QHBoxLayout()
        topLayout.addWidget(self.ftpServerLabel)
        topLayout.addWidget(self.ftpServerLineEdit)
        topLayout.addWidget(self.cdToParentButton)
    
        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(self.downloadButton)
        buttonLayout.addWidget(self.connectButton)
        buttonLayout.addWidget(self.quitButton)
    
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addLayout(topLayout)
        mainLayout.addWidget(self.fileList)
        mainLayout.addWidget(self.statusLabel)
        mainLayout.addLayout(buttonLayout)
        self.setLayout(mainLayout)
    
        self.setWindowTitle(self.tr("FTP"))

    def connectToFtpServer(self):
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        self.ftp.connectToHost(self.ftpServerLineEdit.text())
        self.ftp.login()
        self.ftp.list()
        self.statusLabel.setText(self.tr("Connecting to FTP server %1...")
                             .arg(self.ftpServerLineEdit.text()))
    
    def downloadFile(self):
        fileName = QtCore.QString(self.fileList.currentItem().text())
    
        if QtCore.QFile.fileExists(fileName):
            QtGui.QMessageBox.information(self, self.tr("FTP"), self.tr(
                                          "There already exists a file called %1 "
                                          "in the current directory.").arg(fileName))
            return
    
        self.outFile = QtCore.QFile(fileName)
        if  not self.outFile.open(QtCore.QIODevice.WriteOnly):
            QtGui.QMessageBox.information(self, self.tr("FTP"),
                                          self.tr("Unable to save the file %1: %2.")
                                          .arg(fileName).arg(self.outFile.errorString()))
            self.outFile = None
            return
    
        self.ftp.get(self.fileList.currentItem().text(), self.outFile)
    
        self.progressDialog.setLabelText(self.tr("Downloading %1...").arg(fileName))
        self.progressDialog.show()
        self.downloadButton.setEnabled(False)
    
    def cancelDownload(self):
        self.ftp.abort()
    
    def ftpCommandFinished(self, int, error):
        if self.ftp.currentCommand() == QtNetwork.QFtp.ConnectToHost:
            if error:
                QtGui.QApplication.restoreOverrideCursor()
                QtGui.QMessageBox.information(self, self.tr("FTP"), self.tr(
                                              "Unable to connect to the FTP server "
                                              "at %1. Please check that the host "
                                              "name is correct.")
                                              .arg(self.ftpServerLineEdit.text()))
                return
    
            self.statusLabel.setText(self.tr("Logged onto %1.")
                                 .arg(self.ftpServerLineEdit.text()))
            self.fileList.setFocus()
            self.connectButton.setEnabled(False)
            self.downloadButton.setDefault(True)
            return
    
        if self.ftp.currentCommand() == QtNetwork.QFtp.Get:
            QtGui.QApplication.restoreOverrideCursor()
            if error:
                self.statusLabel.setText(self.tr("Canceled download of %1.")
                                                 .arg(self.outFile.fileName()))
                self.outFile.close()
                self.outFile.remove()
            else:
                self.statusLabel.setText(self.tr("Downloaded %1 to current directory.")
                                                 .arg(self.outFile.fileName()))
                self.outFile.close()
    
            self.outFile = None
            self.enableDownloadButton()
        elif self.ftp.currentCommand() == QtNetwork.QFtp.List:
            QtGui.QApplication.restoreOverrideCursor()
            if not self.isDirectory:
                self.fileList.addItem(self.tr("<empty>"))
                self.fileList.setEnabled(False)
    
    def addToList(self, urlInfo):
        item = QtGui.QListWidgetItem()
        item.setText(urlInfo.name())
        if urlInfo.isDir():
            icon = QtGui.QIcon(":/images/dir.png")
        else:
            icon = QtGui.QIcon(":/images/file.png")
        item.setIcon(icon)
        
        self.isDirectory[unicode(urlInfo.name())] = urlInfo.isDir()
        self.fileList.addItem(item)
        if not self.fileList.currentItem():
            self.fileList.setCurrentItem(self.fileList.item(0))
            self.fileList.setEnabled(True)
    
    def processItem(self, item):
        name = unicode(item.text())
        if self.isDirectory.get(name):
            self.fileList.clear()
            self.isDirectory.clear()
            self.currentPath += "/" + name
            self.ftp.cd(name)
            self.ftp.list()
            self.cdToParentButton.setEnabled(True)
            QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
            return
    
    def cdToParent(self):
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        self.fileList.clear()
        self.isDirectory.clear()
        self.currentPath = self.currentPath.left(self.currentPath.lastIndexOf('/'))
        if self.currentPath.isEmpty():
            self.cdToParentButton.setEnabled(False)
            self.ftp.cd("/")
        else:
            self.ftp.cd(self.currentPath)
    
        self.ftp.list()
    
    def updateDataTransferProgress(self, readBytes, totalBytes):
        self.progressDialog.setMaximum(totalBytes)
        self.progressDialog.setValue(readBytes)
    
    def enableConnectButton(self):
        self.connectButton.setEnabled(not self.ftpServerLineEdit.text().isEmpty())
    
    def enableDownloadButton(self):
        current = self.fileList.currentItem()
        if current:
            currentFile = QtCore.QString(current.text())
            self.downloadButton.setEnabled(not self.isDirectory.get(currentFile))
        else:
            self.downloadButton.setEnabled(False)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ftpWin = FtpWindow()
    sys.exit(ftpWin.exec_())
