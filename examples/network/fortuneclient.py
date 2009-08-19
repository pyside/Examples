#!/usr/bin/env python

"""PyQt4 port of the network/fortuneclient example from Qt v4.x"""

from PyQt4 import QtCore, QtGui, QtNetwork


class Client(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Client, self).__init__(parent)

        self.blockSize = 0
        self.currentFortune = QtCore.QString()

        hostLabel = QtGui.QLabel(self.tr("&Server name:"))
        portLabel = QtGui.QLabel(self.tr("S&erver port:"))

        self.hostLineEdit = QtGui.QLineEdit("Localhost")
        self.portLineEdit = QtGui.QLineEdit()
        self.portLineEdit.setValidator(QtGui.QIntValidator(1, 65535, self))

        hostLabel.setBuddy(self.hostLineEdit)
        portLabel.setBuddy(self.portLineEdit)

        self.statusLabel = QtGui.QLabel(self.tr("This examples requires that "
                                                "you run the Fortune Server "
                                                "example as well."))

        self.getFortuneButton = QtGui.QPushButton(self.tr("Get Fortune"))
        self.getFortuneButton.setDefault(True)
        self.getFortuneButton.setEnabled(False)

        quitButton = QtGui.QPushButton(self.tr("Quit"))

        buttonBox = QtGui.QDialogButtonBox()
        buttonBox.addButton(self.getFortuneButton,
                QtGui.QDialogButtonBox.ActionRole)
        buttonBox.addButton(quitButton, QtGui.QDialogButtonBox.RejectRole)

        self.tcpSocket = QtNetwork.QTcpSocket(self)

        self.hostLineEdit.textChanged.connect(self.enableGetFortuneButton)
        self.portLineEdit.textChanged.connect(self.enableGetFortuneButton)
        self.getFortuneButton.clicked.connect(self.requestNewFortune)
        quitButton.clicked.connect(self.close)
        self.tcpSocket.readyRead.connect(self.readFortune)
        self.tcpSocket.error.connect(self.displayError)

        mainLayout = QtGui.QGridLayout()
        mainLayout.addWidget(hostLabel, 0, 0)
        mainLayout.addWidget(self.hostLineEdit, 0, 1)
        mainLayout.addWidget(portLabel, 1, 0)
        mainLayout.addWidget(self.portLineEdit, 1, 1)
        mainLayout.addWidget(self.statusLabel, 2, 0, 1, 2)
        mainLayout.addWidget(buttonBox, 3, 0, 1, 2)
        self.setLayout(mainLayout)

        self.setWindowTitle(self.tr("Fortune Client"))
        self.portLineEdit.setFocus()

    def requestNewFortune(self):
        self.getFortuneButton.setEnabled(False)
        self.blockSize = 0
        self.tcpSocket.abort()
        self.tcpSocket.connectToHost(self.hostLineEdit.text(),
                self.portLineEdit.text().toInt()[0])

    def readFortune(self):
        instr = QtCore.QDataStream(self.tcpSocket)
        instr.setVersion(QtCore.QDataStream.Qt_4_0)

        if self.blockSize == 0:
            if self.tcpSocket.bytesAvailable() < 2:
                return

            self.blockSize = instr.readUInt16()

        if self.tcpSocket.bytesAvailable() < self.blockSize:
            return

        nextFortune = QtCore.QString()
        instr >> nextFortune

        if nextFortune == self.currentFortune:
            QtCore.QTimer.singleShot(0, self.requestNewFortune)
            return

        self.currentFortune = nextFortune
        self.statusLabel.setText(self.currentFortune)
        self.getFortuneButton.setEnabled(True)

    def displayError(self, socketError):
        if socketError == QtNetwork.QAbstractSocket.RemoteHostClosedError:
            pass
        elif socketError == QtNetwork.QAbstractSocket.HostNotFoundError:
            QtGui.QMessageBox.information(self, self.tr("Fortune Client"),
                    self.tr("The host was not found. Please check the host "
                            "name and port settings."))
        elif socketError == QtNetwork.QAbstractSocket.ConnectionRefusedError:
            QtGui.QMessageBox.information(self, self.tr("Fortune Client"),
                    self.tr("The connection was refused by the peer. Make "
                            "sure the fortune server is running, and check "
                            "that the host name and port settings are "
                            "correct."))
        else:
            QtGui.QMessageBox.information(self, self.tr("Fortune Client"),
                    self.tr("The following error occurred: %1.").arg(self.tcpSocket.errorString()))

        self.getFortuneButton.setEnabled(True)

    def enableGetFortuneButton(self):
        self.getFortuneButton.setEnabled(
                not self.hostLineEdit.text().isEmpty() and
                not self.portLineEdit.text().isEmpty())


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    client = Client()
    client.show()
    sys.exit(client.exec_())
