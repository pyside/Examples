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

from PySide.QtCore import QEvent
from PySide.QtGui import QDialog
from batterypublisher_ui import Ui_BatteryPublisher
from QtMobility import PublishSubscribe

class BatteryPublisher(QDialog):

    def __init__(self):
        QDialog.__init__(self)
        self.ui = Ui_BatteryPublisher()
        self.ui.setupUi(self)

        self.publisher = PublishSubscribe.QValueSpacePublisher('/power/battery')
        self.ui.batteryCharge.valueChanged.connect(self.chargeChanged)
        self.ui.charging.toggled.connect(self.chargingToggled)

        self.chargeTimer = 0

        self.chargeChanged(self.ui.batteryCharge.value())

    def changeEvent(self, e):
        QDialog.changeEvent(self, e)
        if e.type() == QEvent.LanguageChange:
            self.ui.retranslateUi(self)

    def timerEvent(self, e):
        newCharge = self.ui.batteryCharge.value() + 1
        self.ui.batteryCharge.setValue(newCharge)
        if newCharge >= 100:
            self.ui.charging.setChecked(False)

    def chargeChanged(self, newCharge):
        self.publisher.setValue('charge', newCharge)

    def chargingToggled(self, charging):
        self.ui.batteryCharge.setEnabled(not charging)
        self.publisher.setValue('charging', charging)
        if charging:
            self.chargeTimer = self.startTimer(2000)
        else:
            self.killTimer(self.chargeTimer)

