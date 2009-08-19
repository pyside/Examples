#!/usr/bin/env python

"""PySide port of the network/fortuneserver example from Qt v4.x"""

import sys
import random
from PySide import QtCore, QtGui, QtNetwork


class Server(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)

        self.statusLabel = QtGui.QLabel()
        self.quitButton = QtGui.QPushButton(self.tr("Quit"))
        self.quitButton.setAutoDefault(False)

        self.tcpServer = QtNetwork.QTcpServer(self)
        if not self.tcpServer.listen():
            QtGui.QMessageBox.critical(self, self.tr("Fortune Server"),
                                       self.tr("Unable to start the server: %1.")
                                       .arg(self.tcpServer.errorString()))
            self.close()
            return

        self.statusLabel.setText(self.tr("The server is running on port %1.\n"
                                         "Run the Fortune Client example now.")
                                         .arg(self.tcpServer.serverPort()))

        self.fortunes = QtCore.QStringList()
        (self.fortunes << self.tr("You've been leading a dog's life. Stay off the furniture.")
                       << self.tr("You've got to think about tomorrow.")
                       << self.tr("You will be surprised by a loud noise.")
                       << self.tr("You will feel hungry again in another hour.")
                       << self.tr("You might have mail.")
                       << self.tr("You cannot kill time without injuring eternity.")
                       << self.tr("Computers are not intelligent. They only think they are."))

        self.connect(self.quitButton, QtCore.SIGNAL("clicked()"), self, QtCore.SLOT("close()"))
        self.connect(self.tcpServer, QtCore.SIGNAL("newConnection()"), self.sendFortune)

        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(self.quitButton)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.statusLabel)
        mainLayout.addLayout(buttonLayout)
        self.setLayout(mainLayout)

        self.setWindowTitle(self.tr("Fortune Server"))

    def sendFortune(self):
        block = QtCore.QByteArray()
        out = QtCore.QDataStream(block, QtCore.QIODevice.WriteOnly)
        out.setVersion(QtCore.QDataStream.Qt_4_0)
        out.writeUInt16(0)
        out << self.fortunes[random.randint(0, self.fortunes.count() - 1)]
        out.device().seek(0)
        out.writeUInt16(block.size() - 2)

        clientConnection = self.tcpServer.nextPendingConnection()
        self.connect(clientConnection, QtCore.SIGNAL("disconnected()"),
                     clientConnection, QtCore.SLOT("deleteLater()"))

        clientConnection.write(block)
        clientConnection.disconnectFromHost()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    server = Server()
    random.seed(None)
    sys.exit(server.exec_())
