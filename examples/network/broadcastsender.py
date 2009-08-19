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

import sys
from PySide import QtCore, QtGui, QtNetwork


class Sender(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        
        self.statusLabel = QtGui.QLabel(self.tr("Ready to broadcast datagramms on port 45454"))
        self.startButton = QtGui.QPushButton(self.tr("&Start"))
        self.quitButton = QtGui.QPushButton(self.tr("&Quit"))
        self.timer = QtCore.QTimer(self)
        self.udpSocket = QtNetwork.QUdpSocket(self)
        self.messageNo = 1
        
        self.connect(self.startButton, QtCore.SIGNAL("clicked()"),
                     self.startBroadcasting)
        self.connect(self.quitButton, QtCore.SIGNAL("clicked()"),
                     self, QtCore.SLOT("close()"))
        self.connect(self.timer, QtCore.SIGNAL("timeout()"), 
                     self.broadcastDatagramm)
        
        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(self.startButton)
        buttonLayout.addWidget(self.quitButton)
        
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.statusLabel)
        mainLayout.addLayout(buttonLayout)
        self.setLayout(mainLayout)
        
        self.setWindowTitle(self.tr("Broadcast Sender"))

    def startBroadcasting(self):
        self.startButton.setEnabled(False)
        self.timer.start(1000)
        
    def broadcastDatagramm(self):
        self.statusLabel.setText(self.tr("Now broadcasting datagram %1").arg(self.messageNo))
        datagram = "Broadcast message %d" % self.messageNo
        self.udpSocket.writeDatagram(datagram, QtNetwork.QHostAddress(QtNetwork.QHostAddress.Broadcast), 45454)
        self.messageNo += 1


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    sender = Sender()
    sender.show()
    sys.exit(sender.exec_())
