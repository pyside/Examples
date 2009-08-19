#!/usr/bin/env python

"""PyQt4 port of the network/http example from Qt v4.x"""

from PyQt4 import QtCore, QtGui, QtNetwork


class HttpWindow(QtGui.QDialog):
    def __init__(self, parent=None):
        super(HttpWindow, self).__init__(parent)

        self.outFile = None
        self.httpGetId = 0
        self.httpRequestAborted = False

        self.urlLineEdit = QtGui.QLineEdit("https://")

        urlLabel = QtGui.QLabel(self.tr("&URL:"))
        urlLabel.setBuddy(self.urlLineEdit)
        self.statusLabel = QtGui.QLabel(self.tr("Please enter the URL of a "
                                                "file you want to download."))

        self.downloadButton = QtGui.QPushButton(self.tr("Download"))
        self.downloadButton.setDefault(True)
        self.quitButton = QtGui.QPushButton(self.tr("Quit"))
        self.quitButton.setAutoDefault(False)

        buttonBox = QtGui.QDialogButtonBox()
        buttonBox.addButton(self.downloadButton,
                QtGui.QDialogButtonBox.ActionRole)
        buttonBox.addButton(self.quitButton, QtGui.QDialogButtonBox.RejectRole)

        self.progressDialog = QtGui.QProgressDialog(self)

        self.http = QtNetwork.QHttp(self)

        self.urlLineEdit.textChanged.connect(self.enableDownloadButton)
        self.http.requestFinished.connect(self.httpRequestFinished)
        self.http.dataReadProgress.connect(self.updateDataReadProgress)
        self.http.responseHeaderReceived.connect(self.readResponseHeader)
        self.http.authenticationRequired.connect(self.slotAuthenticationRequired)
        self.http.sslErrors.connect(self.sslErrors)
        self.progressDialog.canceled.connect(self.cancelDownload)
        self.downloadButton.clicked.connect(self.downloadFile)
        self.quitButton.clicked.connect(self.close)

        topLayout = QtGui.QHBoxLayout()
        topLayout.addWidget(urlLabel)
        topLayout.addWidget(self.urlLineEdit)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addLayout(topLayout)
        mainLayout.addWidget(self.statusLabel)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.setWindowTitle(self.tr("HTTP"))
        self.urlLineEdit.setFocus()

    def downloadFile(self):
        url = QtCore.QUrl(self.urlLineEdit.text())
        fileInfo = QtCore.QFileInfo(url.path())
        fileName = QtCore.QString(fileInfo.fileName())

        if fileName.isEmpty():
            fileName = "index.html"

        if QtCore.QFile.exists(fileName):
            ret = QtGui.QMessageBox.question(self, self.tr("HTTP"),
                    self.tr("There already exists a file called %1 in the "
                            "current directory.").arg(fileName),
                    QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel,
                    QtGui.QMessageBox.Cancel)

            if ret == QtGui.QMessageBox.Cancel:
                return

            QtCore.QFile.remove(fileName)

        self.outFile = QtCore.QFile(fileName)
        if not self.outFile.open(QtCore.QIODevice.WriteOnly):
            QtGui.QMessageBox.information(self, self.tr("HTTP"),
                    self.tr("Unable to save the file %1: %2.").arg(fileName).arg(self.outFile.errorString()))
            self.outFile = None
            return

        if url.scheme().toLower() == 'https':
            mode = QtNetwork.QHttp.ConnectionModeHttps
        else:
            mode = QtNetwork.QHttp.ConnectionModeHttp

        port = url.port()

        if port == -1:
            port = 0

        self.http.setHost(url.host(), mode, port)

        if not url.userName().isEmpty():
            self.http.setUser(url.userName(), url.password())

        self.httpRequestAborted = False
        path = QtCore.QUrl.toPercentEncoding(url.path(), "!$&'()*+,;=:@/")
        if path.isEmpty():
            path = "/"
        self.httpGetId = self.http.get(path, self.outFile)

        self.progressDialog.setWindowTitle(self.tr("HTTP"))
        self.progressDialog.setLabelText(self.tr("Downloading %1.").arg(fileName))
        self.downloadButton.setEnabled(False)

    def cancelDownload(self):
        self.statusLabel.setText(self.tr("Download canceled."))
        self.httpRequestAborted = True
        self.http.abort()
        self.downloadButton.setEnabled(True)

    def httpRequestFinished(self, requestId, error):
        if requestId != self.httpGetId:
            return

        if self.httpRequestAborted:
            if self.outFile is not None:
                self.outFile.close()
                self.outFile.remove()
                self.outFile = None

            self.progressDialog.hide()
            return

        self.progressDialog.hide()
        self.outFile.close()

        if error:
            self.outFile.remove()
            QtGui.QMessageBox.information(self, self.tr("HTTP"),
                    self.tr("Download failed: %1.").arg(self.http.errorString()))
        else:
            fileName = QtCore.QFileInfo(QtCore.QUrl(self.urlLineEdit.text()).path()).fileName()
            self.statusLabel.setText(self.tr("Downloaded %1 to current directory.").arg(fileName))

        self.downloadButton.setEnabled(True)
        self.outFile = None

    def readResponseHeader(self, responseHeader):
        # Check for genuine error conditions.
        if responseHeader.statusCode() not in (200, 300, 301, 302, 303, 307):
            QtGui.QMessageBox.information(self, self.tr("HTTP"),
                                          self.tr("Download failed: %1.")
                                          .arg(responseHeader.reasonPhrase()))
            self.httpRequestAborted = True
            self.progressDialog.hide()
            self.http.abort()

    def updateDataReadProgress(self, bytesRead, totalBytes):
        if self.httpRequestAborted:
            return

        self.progressDialog.setMaximum(totalBytes)
        self.progressDialog.setValue(bytesRead)

    def enableDownloadButton(self):
        self.downloadButton.setEnabled(not self.urlLineEdit.text().isEmpty())

    def slotAuthenticationRequired(self, hostName, _, authenticator):
        import os
        from PyQt4 import uic

        ui = os.path.join(os.path.dirname(__file__), 'authenticationdialog.ui')
        dlg = uic.loadUi(ui)
        dlg.adjustSize()
        dlg.siteDescription.setText(self.tr("%1 at %2").arg(authenticator.realm()).arg(hostName))

        if dlg.exec_() == QtGui.QDialog.Accepted:
            authenticator.setUser(dlg.userEdit.text())
            authenticator.setPassword(dlg.passwordEdit.text())

    def sslErrors(self, errors):
        errorString = ", ".join([str(error.errorString()) for error in errors])

        ret = QtGui.QMessageBox.warning(self, self.tr("HTTP Example"),
                self.tr("One or more SSL errors has occurred: %1").arg(errorString),
                QtGui.QMessageBox.Ignore | QtGui.QMessageBox.Abort)

        if ret == QtGui.QMessageBox.Ignore:
            self.http.ignoreSslErrors()


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    httpWin = HttpWindow()
    httpWin.show()
    sys.exit(httpWin.exec_())
