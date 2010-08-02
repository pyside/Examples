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

from PySide.QtCore import Qt, QEvent, Signal
from PySide.QtGui import QListWidget, QListWidgetItem
from PySide.QtGui import QTableWidget, QTableWidgetItem
from PySide.QtGui import QDesktopWidget, QDialog, QDialogButtonBox
from QtMobility.PublishSubscribe import QValueSpaceSubscriber

try:
    from PySide import QtMaemo5
    USE_MAEMO_5 = True
    from subscriberdialog_hor_ui import Ui_SubscriberDialog
except:
    USE_MAEMO_5 = False
    from subscriberdialog_ui import Ui_SubscriberDialog


class SubscriberDialog(QDialog):

    if USE_MAEMO_5:
        switchRequested = Signal()

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_SubscriberDialog()
        self.ui.setupUi(self)

        self.subscriber = None
        self.tableWidget = None
        self.listWidget = None

        if USE_MAEMO_5:
            switchButton = self.ui.buttonBox.addButton(self.tr('Switch'), QDialogButtonBox.ActionRole)
            switchButton.clicked.connect(self.switchRequested)

            self.tableWidget = self.ui.tableWidget
            headerLabels = ('Key', 'Value', 'Type')
            self.tableWidget.setColumnCount(3)
            self.tableWidget.setHorizontalHeaderLabels(headerLabels)
            horizontalHeader = self.tableWidget.horizontalHeader()
            horizontalHeader.setStretchLastSection(True)
            verticalHeader = self.tableWidget.verticalHeader()
            verticalHeader.setVisible(False)
            self.tableWidget.setColumnWidth(0, 200)
            self.tableWidget.setColumnWidth(1, 400)
        else:
            desktopWidget = QDesktopWidget()
            if desktopWidget.availableGeometry().width() < 400:
                # Screen is too small to fit a table widget without scrolling, use a list widget instead.
                self.listWidget = QListWidget()
                self.listWidget.setAlternatingRowColors(True)
                self.ui.verticalLayout.insertWidget(2, self.listWidget)
            else:
                self.tableWidget = QTableWidget()
                headerLabels = ('Key', 'Value', 'Type')
                self.tableWidget.setColumnCount(3)
                self.tableWidget.setHorizontalHeaderLabels(headerLabels)
                horizontalHeader = self.tableWidget.horizontalHeader()
                horizontalHeader.setStretchLastSection(True)
                self.tableWidget.verticalHeader()
                self.setVisible(False)
                self.ui.verticalLayout.insertWidget(2, self.tableWidget)

        self.ui.connectButton.clicked.connect(self.changeSubscriberPath)
        self.changeSubscriberPath()

        # if the default path does not exist reset it to /
        value = self.subscriber.value()
        subPaths = self.subscriber.subPaths()
        if not value and not subPaths:
            self.ui.basePath.setText('/')
            self.changeSubscriberPath()

    def changeEvent(self, e):
        QDialog.changeEvent(self, e)
        if e.type() == QEvent.LanguageChange:
            self.ui.retranslateUi(self)

    def changeSubscriberPath(self):
        if self.listWidget:
            self.listWidget.clear()
        elif self.tableWidget:
            self.tableWidget.clearContents()

        if not self.subscriber:
            self.subscriber = QValueSpaceSubscriber(self.ui.basePath.text(), self)
        else:
            self.subscriber.setPath(self.ui.basePath.text())

        self.subscriber.contentsChanged.connect(self.subscriberChanged)
        self.subscriber.connectNotify("contentsChanged()")
        self.subscriberChanged()

    def subscriberChanged(self):
        subPaths = self.subscriber.subPaths()

        if self.listWidget:
            self.listWidget.clear()
        elif self.tableWidget:
            self.tableWidget.clearContents()
            self.tableWidget.setRowCount(len(subPaths))

        for i in xrange(len(subPaths)):
            v = self.subscriber.value(subPaths[i])
            if self.listWidget:
                item = QListWidgetItem('%s (%s)\n%s' % (subPaths[i], str(type(v)), str(v)))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.listWidget.addItem(item)
            elif self.tableWidget:
                pathItem = QTableWidgetItem(subPaths[i])
                pathItem.setFlags(pathItem.flags() & ~Qt.ItemIsEditable)
                valueItem = QTableWidgetItem(str(v))
                valueItem.setFlags(pathItem.flags() & ~Qt.ItemIsEditable)
                typeItem = QTableWidgetItem(str(type(v)))
                typeItem.setFlags(pathItem.flags() & ~Qt.ItemIsEditable)

                self.tableWidget.setItem(i, 0, pathItem)
                self.tableWidget.setItem(i, 1, valueItem)
                self.tableWidget.setItem(i, 2, typeItem)

