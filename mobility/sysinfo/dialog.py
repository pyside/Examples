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
from QtMobility.SystemInfo import SystemInfo, SystemDeviceInfo, SystemDisplayInfo, SystemStorageInfo, SystemNetworkInfo, SystemScreenSaver

from dialog_rc import Ui_Dialog

class Dialog(QWidget, Ui_Dialog):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.systemInfo = None
        self.di = None
        self.ni = None
        self.sti = None
        self.saver = None

        self.setupUi(self)
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

        if e.type() == QEvent.LanguageChange:
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

        self.systemInfo = SystemInfo(self)
        self.curLanguageLineEdit.setText(self.systemInfo.currentLanguage())

        self.languagesComboBox.clear()
        self.languagesComboBox.insertItems(0, self.systemInfo.availableLanguages())
        self.countryCodeLabel.setText(self.systemInfo.currentCountryCode())

    def setupDevice(self):
        del self.di

        self.di = SystemDeviceInfo(self)
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
        if self.di.currentPowerState() == SystemDeviceInfo.BatteryPower:
            self.radioButton_2.setChecked(True)
        elif self.di.currentPowerState() == SystemDeviceInfo.WallPower:
            self.radioButton_3.setChecked(True)
        elif self.di.currentPowerState() == SystemDeviceInfo.WallPowerChargingBattery:
            self.radioButton_4.setChecked(True)
        else:
            self.radioButton.setChecked(True)

        methods = self.di.inputMethodType()
        inputs = []
        if methods & SystemDeviceInfo.Keys:
            inputs.append("Keys")
        if methods & SystemDeviceInfo.Keypad:
            inputs.append("Keypad")
        if methods & SystemDeviceInfo.Keyboard:
            inputs.append("Keyboard")
        if methods & SystemDeviceInfo.SingleTouch:
            inputs.append("Touch Screen")
        if methods & SystemDeviceInfo.MultiTouch:
            inputs.append("Multi touch")
        if methods & SystemDeviceInfo.Mouse:
            inputs.append("Mouse")

        self.inputMethodLabel.setText(" ".join(inputs))
        bLabel = "Off"
        if self.di.currentBluetoothPowerState():
            bLabel = "On"

        self.bluetoothPowerLabel.setText(bLabel)
        self.di.bluetoothStateChanged.connect(self.bluetoothChanged)

    def updateDeviceLockedState(self):
        if self.di:
            self.deviceLockPushButton.setChecked(self.di.isDeviceLocked())

    def onProfileChanged(self, p):
        self.updateProfile()


    def setupDisplay(self):
        di = SystemDisplayInfo()
        self.brightnessLabel.setText(str(di.displayBrightness(0)))
        self.colorDepthLabel.setText(str(di.colorDepth((0))))

        orientation = di.getOrientation(0);
        if orientation == SystemDisplayInfo.Landscape:
            orientStr="Landscape"
        elif orientation == SystemDisplayInfo.Portrait:
            orientStr="Portrait"
        elif orientation == SystemDisplayInfo.InvertedLandscape:
            orientStr="Inverted Landscape";
        elif orientation == SystemDisplayInfo.InvertedPortrait:
            orientStr="Inverted Portrait";
        else:
            orientStr = "Orientation unknown"

        self.orientationLabel.setText(orientStr)
        self.contrastLabel.setText(str(di.contrast((0))))
        self.dpiWidthLabel.setText(str(di.getDPIWidth(0)))
        self.dpiHeightLabel.setText(str(di.getDPIHeight((0))))
        self.physicalHeightLabel.setText(str(di.physicalHeight(0)))
        self.physicalWidthLabel.setText(str(di.physicalWidth((0))))

    def setupStorage(self):
        if not self.sti:
            self.sti = SystemStorageInfo(self)
            self.storageTreeWidget.header().setResizeMode(QHeaderView.ResizeToContents)
            self.sti.logicalDrivesChanged.connect(self.storageChanged)
        self.updateStorage();

    def updateStorage(self):
        self.storageTreeWidget.clear()

        vols = self.sti.logicalDrives()
        for volName in vols:
            volType = self.sti.typeForDrive(volName)
            if volType == SystemStorageInfo.InternalDrive:
                typeName =  "Internal"
            elif volType == SystemStorageInfo.RemovableDrive:
                typeName = "Removable"
            elif volType == SystemStorageInfo.CdromDrive:
                typeName =  "Cdrom"
            elif volType == SystemStorageInfo.RemoteDrive:
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
        self.ni = SystemNetworkInfo(self)
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
        reIndex = index
        self.displayNetworkStatus(self.ni.networkStatus(reIndex))
        self.macAddressLabel.setText(self.ni.macAddress(reIndex))
        strength = self.ni.networkSignalStrength(reIndex)
        if strength < 0:
            strength = 0
        self.signalLevelProgressBar.setValue(strength)
        self.InterfaceLabel.setText(self.ni.interfaceForMode(reIndex).humanReadableName())
        self.operatorNameLabel.setText(self.ni.networkName(reIndex))

    def getVersion(self, index):
        version = SystemInfo.Version()
        if index == 0:
            self.versionLineEdit.setText("")
        elif index == 1:
            version = SystemInfo.Os
        elif index == 2:
            version = SystemInfo.QtCore;
        elif index == 3:
            version = SystemInfo.Firmware

        si = SystemInfo()
        self.versionLineEdit.setText(si.version(version))

    def getFeature(self, index):
        if index == 0:
            return
        elif index == 1:
           feature = SystemInfo.BluetoothFeature
        elif index == 2:
            feature = SystemInfo.CameraFeature
        elif index == 3:
            feature = SystemInfo.FmradioFeature
        elif index == 4:
            feature = SystemInfo.IrFeature;
        elif index == 5:
            feature = SystemInfo.LedFeature
        elif index == 6:
            feature = SystemInfo.MemcardFeature
        elif index == 7:
            feature = SystemInfo.UsbFeature
        elif index == 8:
            feature = SystemInfo.VibFeature
        elif index == 9:
            feature = SystemInfo.WlanFeature
        elif index == 10:
            feature = SystemInfo.SimFeature
        elif index == 11:
            feature = SystemInfo.LocationFeature
        elif index == 12:
            feature = SystemInfo.VideoOutFeature
        elif index == 13:
            feature = SystemInfo.HapticsFeature

        si = SystemInfo()
        text = "false"
        if si.hasFeatureSupported(feature):
            text = "true"
        self.featuresLineEdit.setText(text)

    def setupSaver(self):
        if not self.saver:
            self.saver = SystemScreenSaver(self)

        saverEnabled = self.saver.screenSaverInhibited()
        self.saverInhibitedCheckBox.clicked.connect(self.setSaverEnabled)
        self.saverInhibitedCheckBox.setChecked(saverEnabled)

    def setSaverEnabled(self, b):
        if b:
            if not self.saver:
                self.saver = SystemScreenSaver(self)
            if self.saver.setScreenSaverInhibit():
                pass
        else:
            del self.saver
            self.saver = None


    def updateBatteryStatus(self, level):
        self.batteryLevelBar.setValue(level)

    def updatePowerState(self, newState):
        if newState == SystemDeviceInfo.BatteryPower:
            self.radioButton_2.setChecked(True)
        elif newState == SystemDeviceInfo.WallPower:
            self.radioButton_3.setChecked(True)
        elif newState == SystemDeviceInfo.WallPowerChargingBattery:
            self.radioButton_4.setChecked(True)
        elif newState == SystemDeviceInfo.NoBatteryLevel:
            self.radioButton.setChecked(True);

    def displayBatteryStatus(self, status):
        if status == SystemDeviceInfo.BatteryCritical:
            msg = " Battery is Critical (4% or less), please save your work or plug in the charger."
            QMessageBox.critical(self, "SystemInfo", msg)
        elif status == SystemDeviceInfo.BatteryVeryLow:
            msg = "Battery is Very Low (10%), please plug in the charger soon"
            QMessageBox.warning(self, "SystemInfo", msg);
        elif status == SystemDeviceInfo.BatteryLow:
            msg = "Battery is Low (40% or less)";
            QMessageBox.information(self, "SystemInfo", msg)
        elif status == SystemDeviceInfo.BatteryNormal:
            msg = "Battery is Normal (greater than 40%)";
            QMessageBox.information(self, "SystemInfo", msg)

    def networkSignalStrengthChanged(self, mode, strength):
        if mode == SystemNetworkInfo.WlanMode:
            if self.netStatusComboBox.currentText() == "Wlan":
                self.signalLevelProgressBar.setValue(strength)

        if mode == SystemNetworkInfo.EthernetMode:
            if self.netStatusComboBox.currentText() == "Ethernet":
                self.signalLevelProgressBar.setValue(strength)

        if mode == SystemNetworkInfo.GsmMode:
            if self.netStatusComboBox.currentText() == "Gsm":
                self.signalLevelProgressBar.setValue(strength)

        if mode == SystemNetworkInfo.CdmaMode:
            if self.netStatusComboBox.currentText() == "Cdma":
                self.signalLevelProgressBar.setValue(strength)

        if mode == SystemNetworkInfo.WcdmaMode:
            if self.netStatusComboBox.currentText() == "Wcdma":
                self.signalLevelProgressBar.setValue(strength)

    def networkNameChanged(self, mode, text):
        if mode == SystemNetworkInfo.WlanMode:
            if self.netStatusComboBox.currentText() == "Wlan":
                self.operatorNameLabel.setText(text);

        if mode == SystemNetworkInfo.EthernetMode:
            if self.netStatusComboBox.currentText() == "Ethernet":
                self.operatorNameLabel.setText(text)

        if mode == SystemNetworkInfo.GsmMode:
            if self.netStatusComboBox.currentText() == "Gsm":
                self.operatorNameLabel.setText(text)

        if mode == SystemNetworkInfo.CdmaMode:
            if self.netStatusComboBox.currentText() == "Cdma":
                self.operatorNameLabel.setText(text)

        if mode == SystemNetworkInfo.WcdmaMode:
            if self.netStatusComboBox.currentText() == "Wcdma":
                self.operatorNameLabel.setText(text)


    def networkStatusChanged(self, mode, status):
        if mode == SystemNetworkInfo.WlanMode:
            if self.netStatusComboBox.currentText() == "Wlan":
                self.displayNetworkStatus(status)

        if mode == SystemNetworkInfo.EthernetMode:
            if self.netStatusComboBox.currentText() == "Ethernet":
                self.displayNetworkStatus(status)

        if mode == SystemNetworkInfo.GsmMode:
            if self.netStatusComboBox.currentText() == "Gsm":
                self.displayNetworkStatus(status)

        if mode == SystemNetworkInfo.CdmaMode:
            if self.netStatusComboBox.currentText() == "Cdma":
                self.displayNetworkStatus(status)

        if mode == SystemNetworkInfo.WcdmaMode:
            if self.netStatusComboBox.currentText() == "Wcdma":
                self.displayNetworkStatus(status)

    def networkModeChanged(self, mode):
        if mode == SystemNetworkInfo.WlanMode:
            self.primaryModeLabel.setText("Wlan")

        if mode == SystemNetworkInfo.EthernetMode:
            self.primaryModeLabel.setText("Ethernet")

        if mode == SystemNetworkInfo.GsmMode:
            self.primaryModeLabel.setText("Gsm")

        if mode == SystemNetworkInfo.CdmaMode:
            self.primaryModeLabel.setText("Cdma")

        if mode == SystemNetworkInfo.WcdmaMode:
            self.primaryModeLabel.setText("Wcdma")

        if mode == SystemNetworkInfo.UnknownMode:
            self.primaryModeLabel.setText("None")


    def displayNetworkStatus(self, status):
        if status == SystemNetworkInfo.UndefinedStatus:
            stat = "Undefined"
        if status == SystemNetworkInfo.NoNetworkAvailable:
            stat = "No Network Available"
        if status == SystemNetworkInfo.EmergencyOnly:
            stat = "Emergency Only"
        if status == SystemNetworkInfo.Searching:
            stat = "Searching or Connecting"
        if status == SystemNetworkInfo.Busy:
            stat = "Busy"
        if status == SystemNetworkInfo.Connected:
            stat = "Connected"
        if status == SystemNetworkInfo.HomeNetwork:
            stat = "Home Network"
        if status == SystemNetworkInfo.Denied:
            stat = "Denied"
        if status == SystemNetworkInfo.Roaming:
            stat = "Roaming"
        self.cellNetworkStatusLabel.setText(stat)

    def updateProfile(self):
        if self.di:
            current = self.di.currentProfile()
            if current == SystemDeviceInfo.UnknownProfile:
                profilestring = "Unknown"
            elif current == SystemDeviceInfo.SilentProfile:
                profilestring = "Silent"
            elif current == SystemDeviceInfo.NormalProfile:
                profilestring = "Normal"
            elif current == SystemDeviceInfo.LoudProfile:
                profilestring = "Loud"
            elif current == SystemDeviceInfo.VibProfile:
                profilestring = "Vibrate"
            elif current == SystemDeviceInfo.OfflineProfile:
                profilestring = "Offline";
            elif current == SystemDeviceInfo.PowersaveProfile:
                profilestring = "Powersave";
            elif current ==  SystemDeviceInfo.CustomProfile:
                profilestring = "custom";

        self.profileLabel.setText(profilestring);

    def updateSimStatus(self):
        if self.di:
            status = self.di.simStatus()
            if status == SystemDeviceInfo.SimLocked:
                simstring = "Sim Locked";
            elif status == SystemDeviceInfo.SimNotAvailable:
                simstring = "Sim not available";
            elif status == SystemDeviceInfo.SingleSimAvailable:
                simstring = "Single Sim Available";
            elif status == SystemDeviceInfo.DualSimAvailable:
                simstring = "Dual Sim available";
            else:
                simstring = ""

            self.simStatusLabel.setText(simstring)

    def storageChanged(self, added):
        self.setupStorage()

    def bluetoothChanged(self, b):
        if b:
            text = "On"
        else:
            text = "Off"
        self.bluetoothPowerLabel.setText(text)

