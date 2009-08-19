#!/usr/bin/env python

"""PyQt4 port of the network/ftp example from Qt v4.x"""

from PyQt4 import QtCore, QtGui, QtNetwork

import ftp_rc


class FtpWindow(QtGui.QDialog):
    def __init__(self, parent=None):
        super(FtpWindow, self).__init__(parent)

        self.isDirectory = {}
        self.currentPath = QtCore.QString()
        self.ftp = None
        self.outFile = None

        ftpServerLabel = QtGui.QLabel(self.tr("Ftp &server:"))
        self.ftpServerLineEdit = QtGui.QLineEdit("ftp.trolltech.com")
        ftpServerLabel.setBuddy(self.ftpServerLineEdit)

        self.statusLabel = QtGui.QLabel(self.tr("Please enter the name of an FTP server."))

        self.fileList = QtGui.QTreeWidget()
        self.fileList.setEnabled(False)
        self.fileList.setRootIsDecorated(False)
        self.fileList.setHeaderLabels(QtCore.QStringList() << self.tr("Name") << self.tr("Size") << self.tr("Owner") << self.tr("Group") << self.tr("Time"))
        self.fileList.header().setStretchLastSection(False)

        self.connectButton = QtGui.QPushButton(self.tr("Connect"))
        self.connectButton.setDefault(True)

        self.cdToParentButton = QtGui.QPushButton()
        self.cdToParentButton.setIcon(QtGui.QIcon(":/images/cdtoparent.png"))
        self.cdToParentButton.setEnabled(False)

        self.downloadButton = QtGui.QPushButton(self.tr("Download"))
        self.downloadButton.setEnabled(False)

        self.quitButton = QtGui.QPushButton(self.tr("Quit"))

        buttonBox = QtGui.QDialogButtonBox()
        buttonBox.addButton(self.downloadButton,
                QtGui.QDialogButtonBox.ActionRole)
        buttonBox.addButton(self.quitButton, QtGui.QDialogButtonBox.RejectRole)

        self.progressDialog = QtGui.QProgressDialog(self)

        self.fileList.itemActivated.connect(self.processItem)
        self.fileList.currentItemChanged.connect(self.enableDownloadButton)
        self.progressDialog.canceled.connect(self.cancelDownload)
        self.connectButton.clicked.connect(self.connectOrDisconnect)
        self.cdToParentButton.clicked.connect(self.cdToParent)
        self.downloadButton.clicked.connect(self.downloadFile)
        self.quitButton.clicked.connect(self.close)

        topLayout = QtGui.QHBoxLayout()
        topLayout.addWidget(ftpServerLabel)
        topLayout.addWidget(self.ftpServerLineEdit)
        topLayout.addWidget(self.cdToParentButton)
        topLayout.addWidget(self.connectButton)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addLayout(topLayout)
        mainLayout.addWidget(self.fileList)
        mainLayout.addWidget(self.statusLabel)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.setWindowTitle(self.tr("FTP"))

    def sizeHint(self):
        return QtCore.QSize(500, 300)

    def connectOrDisconnect(self):
        if self.ftp:
            self.ftp.abort()
            self.ftp.deleteLater()
            self.ftp = None

            self.fileList.setEnabled(False)
            self.cdToParentButton.setEnabled(False)
            self.downloadButton.setEnabled(False)
            self.connectButton.setEnabled(True)
            self.connectButton.setText(self.tr("Connect"))
            self.setCursor(QtCore.Qt.ArrowCursor)

            return

        self.setCursor(QtCore.Qt.WaitCursor)

        self.ftp = QtNetwork.QFtp(self)
        self.ftp.commandFinished.connect(self.ftpCommandFinished)
        self.ftp.listInfo.connect(self.addToList)
        self.ftp.dataTransferProgress.connect(self.updateDataTransferProgress)

        self.fileList.clear()
        self.currentPath.clear()
        self.isDirectory.clear()

        url = QtCore.QUrl(self.ftpServerLineEdit.text())
        if not url.isValid() or url.scheme().toLower() != 'ftp':
            self.ftp.connectToHost(self.ftpServerLineEdit.text(), 21)
            self.ftp.login()
        else:
            self.ftp.connectToHost(url.host(), url.port(21))

            if not url.userName().isEmpty():
                self.ftp.login(QtCore.QUrl.fromPercentEncoding(url.userName().toLatin1()), url.password())
            else:
                self.ftp.login()

            if not url.path().isEmpty():
                self.ftp.cd(url.path())

        self.fileList.setEnabled(True)
        self.connectButton.setEnabled(False)
        self.connectButton.setText(self.tr("Disconnect"))
        self.statusLabel.setText(self.tr("Connecting to FTP server %1...")
                             .arg(self.ftpServerLineEdit.text()))

    def downloadFile(self):
        fileName = self.fileList.currentItem().text(0)

        if QtCore.QFile.exists(fileName):
            QtGui.QMessageBox.information(self, self.tr("FTP"),
                    self.tr("There already exists a file called %1 in the "
                            "current directory.").arg(fileName))
            return

        self.outFile = QtCore.QFile(fileName)
        if not self.outFile.open(QtCore.QIODevice.WriteOnly):
            QtGui.QMessageBox.information(self, self.tr("FTP"),
                    self.tr("Unable to save the file %1: %2.").arg(fileName).arg(self.outFile.errorString()))
            self.outFile = None
            return

        self.ftp.get(self.fileList.currentItem().text(0), self.outFile)

        self.progressDialog.setLabelText(self.tr("Downloading %1...").arg(fileName))
        self.downloadButton.setEnabled(False)
        self.progressDialog.exec_()

    def cancelDownload(self):
        self.ftp.abort()

    def ftpCommandFinished(self, _, error):
        self.setCursor(QtCore.Qt.ArrowCursor)

        if self.ftp.currentCommand() == QtNetwork.QFtp.ConnectToHost:
            if error:
                QtGui.QMessageBox.information(self, self.tr("FTP"),
                        self.tr("Unable to connect to the FTP server at %1. "
                                "Please check that the host name is correct.").arg(self.ftpServerLineEdit.text()))
                self.connectOrDisconnect()
                return

            self.statusLabel.setText(self.tr("Logged onto %1.").arg(self.ftpServerLineEdit.text()))
            self.fileList.setFocus()
            self.downloadButton.setDefault(True)
            self.connectButton.setEnabled(True)
            return

        if self.ftp.currentCommand() == QtNetwork.QFtp.Login:
            self.ftp.list()

        if self.ftp.currentCommand() == QtNetwork.QFtp.Get:
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
            self.progressDialog.hide()
        elif self.ftp.currentCommand() == QtNetwork.QFtp.List:
            if not self.isDirectory:
                self.fileList.addTopLevelItem(QtGui.QTreeWidgetItem([self.tr("<empty>")]))
                self.fileList.setEnabled(False)

    def addToList(self, urlInfo):
        item = QtGui.QTreeWidgetItem()
        item.setText(0, urlInfo.name())
        item.setText(1, QtCore.QString.number(urlInfo.size()))
        item.setText(2, urlInfo.owner())
        item.setText(3, urlInfo.group())
        item.setText(4, urlInfo.lastModified().toString("MMM dd yyyy"))

        if urlInfo.isDir():
            icon = QtGui.QIcon(":/images/dir.png")
        else:
            icon = QtGui.QIcon(":/images/file.png")
        item.setIcon(0, icon)

        self.isDirectory[urlInfo.name()] = urlInfo.isDir()
        self.fileList.addTopLevelItem(item)
        if not self.fileList.currentItem():
            self.fileList.setCurrentItem(self.fileList.topLevelItem(0))
            self.fileList.setEnabled(True)

    def processItem(self, item):
        name = item.text(0)
        if self.isDirectory.get(name):
            self.fileList.clear()
            self.isDirectory.clear()
            self.currentPath += "/" + name
            self.ftp.cd(name)
            self.ftp.list()
            self.cdToParentButton.setEnabled(True)
            self.setCursor(QtCore.Qt.WaitCursor)

    def cdToParent(self):
        self.setCursor(QtCore.Qt.WaitCursor)
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

    def enableDownloadButton(self):
        current = self.fileList.currentItem()
        if current:
            currentFile = current.text(0)
            self.downloadButton.setEnabled(not self.isDirectory.get(currentFile))
        else:
            self.downloadButton.setEnabled(False)


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    ftpWin = FtpWindow()
    ftpWin.show()
    sys.exit(ftpWin.exec_())
