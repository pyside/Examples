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

from PySide.QtGui import QMessageBox, QWidget, QHeaderView, QTreeWidgetItem
from PySide.QtCore import QTimer, QEvent
from QtMobility.SystemInfo import QSystemInfo, QSystemDeviceInfo, QSystemDisplayInfo, QSystemStorageInfo, QSystemNetworkInfo, QSystemScreenSaver

from dialog_rc import Ui_Dialog

class Dialog(QWidget, Ui_Dialog):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.systemInfo = None
        self.di = None
        self.ni = None
        self.sti = None
        self.saver = None
        self.uiCreated = False

        self.setupUi(self)

        self.uiCreated = True
        self.setupGeneral()

        self.tabWidget.currentChanged.connect(self.tabChanged)
        self.versionComboBox.activated[int].connect(self.getVersion)
        self.featureComboBox.activated[int].connect(self.getFeature)


        self.updateDeviceLockedState()
        timer = QTimer(self)
        timer.timeout.connect(self.updateDeviceLockedState)
        timer.start(1000)


    def changeEvent(self, e):
        QWidget.changeEvent(self, e)

        if e.type() == QEvent.LanguageChange and self.uiCreated:
            self.retranslateUi(self)

    def tabChanged(self, index):
        if index == 0:
            self.setupGeneral()
        elif index == 1:
            self.setupDevice()
        elif index == 2:
            self.setupDisplay()
        elif index == 3:
            self.setupStorage()
        elif index == 4:
            self.setupNetwork()
        elif index == 5:
            self.setupSaver()

    def setupGeneral(self):
        del self.systemInfo

        self.systemInfo = QSystemInfo(self)
        self.curLanguageLineEdit.setText(self.systemInfo.currentLanguage())

        self.languagesComboBox.clear()
        self.languagesComboBox.insertItems(0, self.systemInfo.availableLanguages())
        self.countryCodeLabel.setText(self.systemInfo.currentCountryCode())

    def setupDevice(self):
        del self.di

        self.di = QSystemDeviceInfo(self)
        self.batteryLevelBar.setValue(self.di.batteryLevel())
        self.di.batteryLevelChanged.connect(self.updateBatteryStatus)
        self.di.batteryStatusChanged.connect(self.displayBatteryStatus)
        self.di.powerStateChanged.connect(self.updatePowerState)
        self.ImeiLabel.setText(self.di.imei())
        self.imsiLabel.setText(self.di.imsi())
        self.manufacturerLabel.setText(self.di.manufacturer())
        self.modelLabel.setText(self.di.model())
        self.productLabel.setText(self.di.productName())
        self.deviceLockPushButton.setChecked(self.di.isDeviceLocked())

        self.updateSimStatus()
        self.updateProfile()

        self.di.currentProfileChanged.connect(self.onProfileChanged)
        if self.di.currentPowerState() == QSystemDeviceInfo.BatteryPower:
            self.radioButton_2.setChecked(True)
        elif self.di.currentPowerState() == QSystemDeviceInfo.WallPower:
            self.radioButton_3.setChecked(True)
        elif self.di.currentPowerState() == QSystemDeviceInfo.WallPowerChargingBattery:
            self.radioButton_4.setChecked(True)
        else:
            self.radioButton.setChecked(True)

        methods = self.di.inputMethodType()
        inputs = []
        if methods & QSystemDeviceInfo.Keys:
            inputs.append("Keys")
        if methods & QSystemDeviceInfo.Keypad:
            inputs.append("Keypad")
        if methods & QSystemDeviceInfo.Keyboard:
            inputs.append("Keyboard")
        if methods & QSystemDeviceInfo.SingleTouch:
            inputs.append("Touch Screen")
        if methods & QSystemDeviceInfo.MultiTouch:
            inputs.append("Multi touch")
        if methods & QSystemDeviceInfo.Mouse:
            inputs.append("Mouse")

        self.inputMethodLabel.setText(" ".join(inputs))

    def updateDeviceLockedState(self):
        if self.di:
            self.deviceLockPushButton.setChecked(self.di.isDeviceLocked())

    def onProfileChanged(self, p):
        self.updateProfile()


    def setupDisplay(self):
        di = QSystemDisplayInfo()
        self.brightnessLabel.setText(str(di.displayBrightness(0)))
        self.colorDepthLabel.setText(str(di.colorDepth((0))))

    def setupStorage(self):
        if not self.sti:
            self.sti = QSystemStorageInfo(self)
            self.storageTreeWidget.header().setResizeMode(QHeaderView.ResizeToContents)
        self.updateStorage();

    def updateStorage(self):
        self.storageTreeWidget.clear()

        vols = self.sti.logicalDrives()
        for volName in vols:
            volType = self.sti.typeForDrive(volName)
            if volType == QSystemStorageInfo.InternalDrive:
                typeName =  "Internal"
            elif volType == QSystemStorageInfo.RemovableDrive:
                typeName = "Removable"
            elif volType == QSystemStorageInfo.CdromDrive:
                typeName =  "Cdrom"
            elif volType == QSystemStorageInfo.RemoteDrive:
                typeName =  "Network"
            items = []
            items.append(volName);
            items.append(typeName);
            items.append(str(self.sti.totalDiskSpace(volName)))
            items.append(str(self.sti.availableDiskSpace(volName)))
            item = QTreeWidgetItem(items)
            self.storageTreeWidget.addTopLevelItem(item)


    def setupNetwork(self):
        del self.ni
        self.ni = QSystemNetworkInfo(self)
        self.netStatusComboBox.activated[int].connect(self.netStatusComboActivated)
        self.ni.networkSignalStrengthChanged.connect(self.networkSignalStrengthChanged)
        self.ni.networkNameChanged.connect(self.networkNameChanged)
        self.ni.networkStatusChanged.connect(self.networkStatusChanged)
        self.ni.networkModeChanged.connect(self.networkModeChanged)
        self.cellIdLabel.setText(str(self.ni.cellId()))
        self.locationAreaCodeLabel.setText(str(self.ni.locationAreaCode()))
        self.currentMMCLabel.setText(self.ni.currentMobileCountryCode())
        self.currentMNCLabel.setText(self.ni.currentMobileNetworkCode())
        self.homeMMCLabel.setText(self.ni.homeMobileCountryCode())
        self.homeMNCLabel.setText(self.ni.homeMobileNetworkCode())
        self.networkModeChanged(self.ni.currentMode())

    def netStatusComboActivated(self, index):
        status = ""
        reIndex = QSystemNetworkInfo.NetworkMode(index)
        self.displayNetworkStatus(self.ni.networkStatus(reIndex))
        self.macAddressLabel.setText(self.ni.macAddress(reIndex))
        strength = self.ni.networkSignalStrength(reIndex)
        if strength < 0:
            strength = 0
        self.signalLevelProgressBar.setValue(strength)
        self.InterfaceLabel.setText(self.ni.interfaceForMode(reIndex).humanReadableName())
        self.operatorNameLabel.setText(self.ni.networkName(reIndex))

    def getVersion(self, index):
        version = QSystemInfo.Version()
        if index == 0:
            self.versionLineEdit.setText("")
        elif index == 1:
            version = QSystemInfo.Os
        elif index == 2:
            version = QSystemInfo.QtCore;
        elif index == 3:
            version = QSystemInfo.Firmware

        si = QSystemInfo()
        self.versionLineEdit.setText(si.version(version))

    def getFeature(self, index):
        if index == 0:
            return
        elif index == 1:
           feature = QSystemInfo.BluetoothFeature
        elif index == 2:
            feature = QSystemInfo.CameraFeature
        elif index == 3:
            feature = QSystemInfo.FmradioFeature
        elif index == 4:
            feature = QSystemInfo.IrFeature;
        elif index == 5:
            feature = QSystemInfo.LedFeature
        elif index == 6:
            feature = QSystemInfo.MemcardFeature
        elif index == 7:
            feature = QSystemInfo.UsbFeature
        elif index == 8:
            feature = QSystemInfo.VibFeature
        elif index == 9:
            feature = QSystemInfo.WlanFeature
        elif index == 10:
            feature = QSystemInfo.SimFeature
        elif index == 11:
            feature = QSystemInfo.LocationFeature
        elif index == 12:
            feature = QSystemInfo.VideoOutFeature
        elif index == 13:
            feature = QSystemInfo.HapticsFeature

        si = QSystemInfo()
        text = "false"
        if si.hasFeatureSupported(feature):
            text = "true"
        self.featuresLineEdit.setText(text)

    def setupSaver(self):
        if not self.saver:
            self.saver = QSystemScreenSaver(self)

        saverEnabled = self.saver.screenSaverInhibited()
        self.saverInhibitedCheckBox.clicked.connect(self.setSaverEnabled)
        self.saverInhibitedCheckBox.setChecked(saverEnabled)

    def setSaverEnabled(self, b):
        if b:
            if not self.saver:
                self.saver = QSystemScreenSaver(self)
            if self.saver.setScreenSaverInhibit():
                pass
        else:
            del self.saver
            self.saver = None


    def updateBatteryStatus(self, level):
        self.batteryLevelBar.setValue(level)

    def updatePowerState(self, newState):
        if newState == QSystemDeviceInfo.BatteryPower:
            self.radioButton_2.setChecked(True)
        elif newState == QSystemDeviceInfo.WallPower:
            self.radioButton_3.setChecked(True)
        elif newState == QSystemDeviceInfo.WallPowerChargingBattery:
            self.radioButton_4.setChecked(True)
        elif newState == QSystemDeviceInfo.NoBatteryLevel:
            self.radioButton.setChecked(True);

    def displayBatteryStatus(self, status):
        if status == QSystemDeviceInfo.BatteryCritical:
            msg = " Battery is Critical (4% or less), please save your work or plug in the charger."
            QMessageBox.critical(self, "QSystemInfo", msg)
        elif status == QSystemDeviceInfo.BatteryVeryLow:
            msg = "Battery is Very Low (10%), please plug in the charger soon"
            QMessageBox.warning(self, "QSystemInfo", msg);
        elif status == QSystemDeviceInfo.BatteryLow:
            msg = "Battery is Low (40% or less)";
            QMessageBox.information(self, "QSystemInfo", msg)
        elif status == QSystemDeviceInfo.BatteryNormal:
            msg = "Battery is Normal (greater than 40%)";
            QMessageBox.information(self, "QSystemInfo", msg)

    def networkSignalStrengthChanged(self, mode, strength):
        if mode == QSystemNetworkInfo.WlanMode:
            if self.netStatusComboBox.currentText() == "Wlan":
                self.signalLevelProgressBar.setValue(strength)

        if mode == QSystemNetworkInfo.EthernetMode:
            if self.netStatusComboBox.currentText() == "Ethernet":
                self.signalLevelProgressBar.setValue(strength)

        if mode == QSystemNetworkInfo.GsmMode:
            if self.netStatusComboBox.currentText() == "Gsm":
                self.signalLevelProgressBar.setValue(strength)

        if mode == QSystemNetworkInfo.CdmaMode:
            if self.netStatusComboBox.currentText() == "Cdma":
                self.signalLevelProgressBar.setValue(strength)

        if mode == QSystemNetworkInfo.WcdmaMode:
            if self.netStatusComboBox.currentText() == "Wcdma":
                self.signalLevelProgressBar.setValue(strength)

    def networkNameChanged(self, mode, text):
        if mode == QSystemNetworkInfo.WlanMode:
            if self.netStatusComboBox.currentText() == "Wlan":
                self.operatorNameLabel.setText(text);

        if mode == QSystemNetworkInfo.EthernetMode:
            if self.netStatusComboBox.currentText() == "Ethernet":
                self.operatorNameLabel.setText(text)

        if mode == QSystemNetworkInfo.GsmMode:
            if self.netStatusComboBox.currentText() == "Gsm":
                self.operatorNameLabel.setText(text)

        if mode == QSystemNetworkInfo.CdmaMode:
            if self.netStatusComboBox.currentText() == "Cdma":
                self.operatorNameLabel.setText(text)

        if mode == QSystemNetworkInfo.WcdmaMode:
            if self.netStatusComboBox.currentText() == "Wcdma":
                self.operatorNameLabel.setText(text)


    def networkStatusChanged(self, mode, status):
        if mode == QSystemNetworkInfo.WlanMode:
            if self.netStatusComboBox.currentText() == "Wlan":
                self.displayNetworkStatus(status)

        if mode == QSystemNetworkInfo.EthernetMode:
            if self.netStatusComboBox.currentText() == "Ethernet":
                self.displayNetworkStatus(status)

        if mode == QSystemNetworkInfo.GsmMode:
            if self.netStatusComboBox.currentText() == "Gsm":
                self.displayNetworkStatus(status)

        if mode == QSystemNetworkInfo.CdmaMode:
            if self.netStatusComboBox.currentText() == "Cdma":
                self.displayNetworkStatus(status)

        if mode == QSystemNetworkInfo.WcdmaMode:
            if self.netStatusComboBox.currentText() == "Wcdma":
                self.displayNetworkStatus(status)

    def networkModeChanged(self, mode):
        if mode == QSystemNetworkInfo.WlanMode:
            self.primaryModeLabel.setText("Wlan")

        if mode == QSystemNetworkInfo.EthernetMode:
            self.primaryModeLabel.setText("Ethernet")

        if mode == QSystemNetworkInfo.GsmMode:
            self.primaryModeLabel.setText("Gsm")

        if mode == QSystemNetworkInfo.CdmaMode:
            self.primaryModeLabel.setText("Cdma")

        if mode == QSystemNetworkInfo.WcdmaMode:
            self.primaryModeLabel.setText("Wcdma")

        if mode == QSystemNetworkInfo.UnknownMode:
            self.primaryModeLabel.setText("None")


    def displayNetworkStatus(self, status):
        if status == QSystemNetworkInfo.UndefinedStatus:
            stat = "Undefined"
        if status == QSystemNetworkInfo.NoNetworkAvailable:
            stat = "No Network Available"
        if status == QSystemNetworkInfo.EmergencyOnly:
            stat = "Emergency Only"
        if status == QSystemNetworkInfo.Searching:
            stat = "Searching or Connecting"
        if status == QSystemNetworkInfo.Busy:
            stat = "Busy"
        if status == QSystemNetworkInfo.Connected:
            stat = "Connected"
        if status == QSystemNetworkInfo.HomeNetwork:
            stat = "Home Network"
        if status == QSystemNetworkInfo.Denied:
            stat = "Denied"
        if status == QSystemNetworkInfo.Roaming:
            stat = "Roaming"
        self.cellNetworkStatusLabel.setText(stat)

    def updateProfile(self):
        if self.di:
            current = self.di.currentProfile()
            if current == QSystemDeviceInfo.UnknownProfile:
                profilestring = "Unknown"
            elif current == QSystemDeviceInfo.SilentProfile:
                profilestring = "Silent"
            elif current == QSystemDeviceInfo.NormalProfile:
                profilestring = "Normal"
            elif current == QSystemDeviceInfo.LoudProfile:
                profilestring = "Loud"
            elif current == QSystemDeviceInfo.VibProfile:
                profilestring = "Vibrate"
            elif current == QSystemDeviceInfo.OfflineProfile:
                profilestring = "Offline";
            elif current == QSystemDeviceInfo.PowersaveProfile:
                profilestring = "Powersave";
            elif current ==  QSystemDeviceInfo.CustomProfile:
                profilestring = "custom";

        self.profileLabel.setText(profilestring);

    def updateSimStatus(self):
        if self.di:
            status = self.di.simStatus()
            if status == QSystemDeviceInfo.SimLocked:
                simstring = "Sim Locked";
            elif status == QSystemDeviceInfo.SimNotAvailable:
                simstring = "Sim not available";
            elif status == QSystemDeviceInfo.SingleSimAvailable:
                simstring = "Single Sim Available";
            elif status == QSystemDeviceInfo.DualSimAvailable:
                simstring = "Dual Sim available";
            else:
                simstring = ""

            self.simStatusLabel.setText(simstring)

    def bluetoothChanged(self, b):
        if b:
            text = "On"
        else:
            text = "Off"
        self.bluetoothPowerLabel.setText(text)

