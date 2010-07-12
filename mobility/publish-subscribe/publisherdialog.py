#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#
# Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
# All rights reserved.
# Contact: Nokia Corporation (qt-info@nokia.com)
#
# This file is a port of the Qt Mobility Examples
#
# $QT_BEGIN_LICENSE:BSD$
# You may use this file under the terms of the BSD license as follows:
#
# "Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#   * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in
#     the documentation and/or other materials provided with the
#     distribution.
#   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
#     the names of its contributors may be used to endorse or promote
#     products derived from this software without specific prior written
#     permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
# $QT_END_LICENSE$
#
###############################################################################

from PySide.QtCore import QEvent, Signal
from PySide.QtGui import QDialog, QDialogButtonBox
from QtMobility.PublishSubscribe import QValueSpace, QValueSpacePublisher

try:
    from PySide import QtMaemo5
    USE_MAEMO_5 = True
    from publisherdialog_hor_ui import Ui_PublisherDialog
except:
    USE_MAEMO_5 = False
    from publisherdialog_ui import Ui_PublisherDialog



class PublisherDialog(QDialog):

    if USE_MAEMO_5:
        switchRequested = Signal()

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_PublisherDialog()
        self.ui.setupUi(self)
        self.publisher = None

        if USE_MAEMO_5:
            switchButton = self.ui.buttonBox.addButton(self.tr('Switch'), QDialogButtonBox.ActionRole)
            switchButton.clicked.connect(self.switchRequested)

        self.ui.connectButton.clicked.connect(self.createNewObject)
        self.ui.intValue.valueChanged.connect(self.intValueChanged)
        self.ui.unsetIntButton.clicked.connect(self.unsetIntValue)
        self.ui.setStringButton.clicked.connect(self.setStringValue)
        self.ui.setByteArrayButton.clicked.connect(self.setByteArrayValue)

        self.createNewObject()

    def changeEvent(self, e):
        QDialog.changeEvent(self, e)
        if e.type() == QEvent.LanguageChange:
            self.ui.retranslateUi(self)

    def intValueChanged(self, value):
        self.publisher.setValue('intValue', value);

    def unsetIntValue(self):
        self.publisher.resetValue('intValue')

    def setStringValue(self):
        self.publisher.setValue('stringValue', self.ui.stringValue.text())

    def setByteArrayValue(self):
        self.publisher.setValue('byteArrayValue', self.ui.byteArrayValue.text())

    def createNewObject(self):
        if self.publisher:
            del self.publisher

        self.publisher = QValueSpacePublisher(QValueSpace.WritableLayer, self.ui.basePath.text())
        if self.publisher.isConnected():
            self.ui.setters.setEnabled(True)
            self.intValueChanged(self.ui.intValue.value())
            self.setStringValue()
            self.setByteArrayValue()
        else:
            self.ui.setters.setEnabled(False)

