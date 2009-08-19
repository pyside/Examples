#!/usr/bin/env python

"""PySide port of the network/fortuneclient example from Qt v4.x"""

import sys
from PySide import QtCore, QtGui, QtNetwork


class Client(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)

        self.hostLabel = QtGui.QLabel(self.tr("&Server name:"))
        self.portLabel = QtGui.QLabel(self.tr("S&erver port:"))
    
        self.hostLineEdit = QtGui.QLineEdit("Localhost")
        self.portLineEdit = QtGui.QLineEdit()
        self.portLineEdit.setValidator(QtGui.QIntValidator(1, 65535, self))
    
        self.hostLabel.setBuddy(self.hostLineEdit)
        self.portLabel.setBuddy(self.portLineEdit)
    
        self.statusLabel = QtGui.QLabel(self.tr("This examples requires that you run "
                                                "the Fortune Server example as well."))
    
        self.getFortuneButton = QtGui.QPushButton(self.tr("Get Fortune"))
        self.getFortuneButton.setDefault(True)
        self.getFortuneButton.setEnabled(False)
    
        self.quitButton = QtGui.QPushButton(self.tr("Quit"))
    
        self.timerId = -1
        self.blockSize = 0
        self.currentFortune = QtCore.QString()
        self.tcpSocket = QtNetwork.QTcpSocket(self)
    
        self.connect(self.hostLineEdit, QtCore.SIGNAL("textChanged(const QString &)"), self.enableGetFortuneButton)
        self.connect(self.portLineEdit, QtCore.SIGNAL("textChanged(const QString &)"), self.enableGetFortuneButton)
        self.connect(self.getFortuneButton, QtCore.SIGNAL("clicked()"), self.requestNewFortune)
        self.connect(self.quitButton, QtCore.SIGNAL("clicked()"), self, QtCore.SLOT("close()"))
        self.connect(self.tcpSocket, QtCore.SIGNAL("readyRead()"), self.readFortune)
        self.connect(self.tcpSocket, QtCore.SIGNAL("error(QAbstractSocket::SocketError)"), self.displayError)
    
        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(self.getFortuneButton)
        buttonLayout.addWidget(self.quitButton)
    
        mainLayout = QtGui.QGridLayout()
        mainLayout.addWidget(self.hostLabel, 0, 0)
        mainLayout.addWidget(self.hostLineEdit, 0, 1)
        mainLayout.addWidget(self.portLabel, 1, 0)
        mainLayout.addWidget(self.portLineEdit, 1, 1)
        mainLayout.addWidget(self.statusLabel, 2, 0, 1, 2)
        mainLayout.addLayout(buttonLayout, 3, 0, 1, 2)
        self.setLayout(mainLayout)
    
        self.setWindowTitle(self.tr("Fortune Client"))
        self.portLineEdit.setFocus()
    
    def requestNewFortune(self):
        self.getFortuneButton.setEnabled(False)
        self.blockSize = 0
        self.tcpSocket.abort()
        self.tcpSocket.connectToHost(self.hostLineEdit.text(), self.portLineEdit.text().toInt()[0])
    
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
            self.timerId = self.startTimer(10)
            return
    
        self.currentFortune = nextFortune
        self.statusLabel.setText(self.currentFortune)
        self.getFortuneButton.setEnabled(True)
    
    def timerEvent(self, event):
        if event.timerId() == self.timerId:
            self.killTimer(self.timerId)
            self.timerId = -1
            
            self.requestNewFortune()
            
    def displayError(self, socketError):
        if socketError ==  QtNetwork.QAbstractSocket.RemoteHostClosedError:
            pass
        elif socketError ==  QtNetwork.QAbstractSocket.HostNotFoundError:
            QtGui.QMessageBox.information(self, self.tr("Fortune Client"), self.tr(
                                          "The host was not found. Please check the "
                                          "host name and port settings."))
        elif socketError ==  QtNetwork.QAbstractSocket.ConnectionRefusedError:
            QtGui.QMessageBox.information(self, self.tr("Fortune Client"), self.tr(
                                          "The connection was refused by the peer. "
                                          "Make sure the fortune server is running,\n"
                                          "and check that the host name and port "
                                          "settings are correct."))
        else:
            QtGui.QMessageBox.information(self, self.tr("Fortune Client"),
                                          self.tr("The following error occurred: %1.")
                                          .arg(self.tcpSocket.errorString()))
    
        self.getFortuneButton.setEnabled(True)
    
    def enableGetFortuneButton(self):
        self.getFortuneButton.setEnabled(not self.hostLineEdit.text().isEmpty() and
                                         not self.portLineEdit.text().isEmpty())


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    client = Client()
    sys.exit(client.exec_())
