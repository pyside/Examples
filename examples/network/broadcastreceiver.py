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

from PySide import QtCore, QtGui, QtNetwork


class Receiver(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Receiver, self).__init__(parent)

        self.statusLabel = QtGui.QLabel("Listening for broadcasted messages")
        quitButton = QtGui.QPushButton("&Quit")

        self.udpSocket = QtNetwork.QUdpSocket(self)
        self.udpSocket.bind(45454)

        self.udpSocket.readyRead.connect(self.processPendingDatagrams)
        quitButton.clicked.connect(self.close)

        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(quitButton)
        buttonLayout.addStretch(1)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.statusLabel)
        mainLayout.addLayout(buttonLayout)
        self.setLayout(mainLayout)

        self.setWindowTitle("Broadcast Receiver")

    def processPendingDatagrams(self):
        while self.udpSocket.hasPendingDatagrams():
            datagram, host, port = self.udpSocket.readDatagram(
                self.udpSocket.pendingDatagramSize())

            try:
                # Python v3.
                datagram = str(datagram, encoding='ascii')
            except TypeError:
                # Python v2.
                pass

            self.statusLabel.setText("Received datagram: \"%s\"" % datagram)


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    receiver = Receiver()
    receiver.show()
    sys.exit(receiver.exec_())
