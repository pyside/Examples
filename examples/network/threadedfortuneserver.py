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

import random

from PyQt4 import QtCore, QtGui, QtNetwork


class FortuneThread(QtCore.QThread):
    error = QtCore.pyqtSignal(QtNetwork.QTcpSocket.SocketError)

    def __init__(self, socketDescriptor, fortune, parent):
        super(FortuneThread, self).__init__(parent)

        self.socketDescriptor = socketDescriptor
        self.text = fortune

    def run(self):
        tcpSocket = QtNetwork.QTcpSocket()
        if not tcpSocket.setSocketDescriptor(self.socketDescriptor):
            self.error.emit(tcpSocket.error())
            return

        block = QtCore.QByteArray()
        outstr = QtCore.QDataStream(block, QtCore.QIODevice.WriteOnly)
        outstr.setVersion(QtCore.QDataStream.Qt_4_0)
        outstr.writeUInt16(0)
        outstr << self.text
        outstr.device().seek(0)
        outstr.writeUInt16(block.count() - 2)

        tcpSocket.write(block)
        tcpSocket.disconnectFromHost()
        tcpSocket.waitForDisconnected()


class FortuneServer(QtNetwork.QTcpServer):
    def __init__(self, parent=None):
        super(FortuneServer, self).__init__(parent)

        self.fortunes = [
                self.tr("You've been leading a dog's life. Stay off the furniture."),
                self.tr("You've got to think about tomorrow."),
                self.tr("You will be surprised by a loud noise."),
                self.tr("You will feel hungry again in another hour."),
                self.tr("You might have mail."),
                self.tr("You cannot kill time without injuring eternity."),
                self.tr("Computers are not intelligent. They only think they are.")]

    def incomingConnection(self, socketDescriptor):
        fortune = self.fortunes[random.randint(0, len(self.fortunes) - 1)]
        thread = FortuneThread(socketDescriptor, fortune, self)
        thread.finished.connect(thread.deleteLater)
        thread.start()


class Dialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)

        self.server = FortuneServer()

        statusLabel = QtGui.QLabel()
        quitButton = QtGui.QPushButton(self.tr("Quit"))
        quitButton.setAutoDefault(False)

        if not self.server.listen():
            QtGui.QMessageBox.critical(self,
                    self.tr("Threaded Fortune Server"),
                    self.tr("Unable to start the server: %1.".arg(self.server.errorString())))
            self.close()
            return

        statusLabel.setText(self.tr("The server is running on port %1.\n"
                                    "Run the Fortune Client example now.").arg(self.server.serverPort()))

        quitButton.clicked.connect(self.close)

        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(quitButton)
        buttonLayout.addStretch(1)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(statusLabel)
        mainLayout.addLayout(buttonLayout)
        self.setLayout(mainLayout)

        self.setWindowTitle(self.tr("Threaded Fortune Server"))


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    dialog = Dialog()
    dialog.show()
    sys.exit(dialog.exec_())
