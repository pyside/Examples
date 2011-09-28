#!/usr/bin/python

import sys
import os

from PySide import QtCore
from PySide import QtGui
from PySide import QtDeclarative
from PySide import QtOpenGL
from QtMobility.SystemInfo import QSystemInfo, QSystemDeviceInfo, QSystemDisplayInfo, QSystemStorageInfo, QSystemNetworkInfo, QSystemScreenSaver


class SystemInfoModel(QtCore.QObject):
    changed = QtCore.Signal()

    def __init__(self):
        super(SystemInfoModel, self).__init__()
        self.systemInfo = QSystemInfo(self)
        self.setupGeneral()
        self.setupDevice()
        self.setupDisplay()
        self.setupStorage()
        self.setupNetwork()
        self.setupScreenSaver()

    @QtCore.Property(str, notify=changed)
    def currentLanguage(self):
        return self._currentLanguage

    @QtCore.Property("QStringList", notify=changed)
    def availableLanguages(self):
        return self._availableLanguages

    @QtCore.Property(int, notify=changed)
    def displayBrightness(self):
        return self._displayBrightness

    @QtCore.Property(int, notify=changed)
    def colorDepth(self):
        return self._colorDepth

    @QtCore.Property(str, notify=changed)
    def imei(self):
        return self._imei

    @QtCore.Property(str, notify=changed)
    def imsi(self):
        return self._imsi

    @QtCore.Property(str, notify=changed)
    def manufacturer(self):
        return self._manufacturer

    @QtCore.Property(str, notify=changed)
    def product(self):
        return self._product

    @QtCore.Property(str, notify=changed)
    def model(self):
        return self._model

    @QtCore.Property(str, notify=changed)
    def profile(self):
        return self._profile

    @QtCore.Property(str, notify=changed)
    def inputMethod(self):
        return self._inputMethod

    @QtCore.Property(bool, notify=changed)
    def deviceLock(self):
        return self._deviceLock

    @QtCore.Property(str, notify=changed)
    def simStatus(self):
        return self._simStatus

    @QtCore.Property(bool, notify=changed)
    def bluetoothState(self):
        return self._bluetoothState

    @QtCore.Property("QStringList", notify=changed)
    def volumeNames(self):
        return self._volumeNames

    @QtCore.Property("QStringList", notify=changed)
    def networksNames(self):
        return ["Wlan", "Ethernet", "Gsm", "Cdma", "Wcdma"]

    @QtCore.Property(bool, notify=changed)
    def screenSaverInhibited(self):
        return self._screenSaverInhibited

    def setupGeneral(self):
        self._currentLanguage = self.systemInfo.currentLanguage()
        self._availableLanguages = self.systemInfo.availableLanguages()

    def setupDevice(self):
        self.deviceInfo = QSystemDeviceInfo(self)
        self._batteryLevel = self.deviceInfo.batteryLevel()
        self.deviceInfo.batteryLevelChanged.connect(self.updateBatteryStatus)
        self.deviceInfo.batteryStatusChanged.connect(self.displayBatteryStatus)
        self.deviceInfo.powerStateChanged.connect(self.updatePowerState)
        self._imei = self.deviceInfo.imei()
        self._imsi = self.deviceInfo.imsi()
        self._manufacturer = self.deviceInfo.manufacturer()
        self._model = self.deviceInfo.model()
        self._product = self.deviceInfo.productName()
        self._deviceLock = self.deviceInfo.isDeviceLocked()

        methods = self.deviceInfo.inputMethodType()
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

        self._inputMethod = " ".join(inputs)
        self.updateSimStatus()
        self.updateProfile()

        self._bluetoothState = self.deviceInfo.currentBluetoothPowerState()
        self.deviceInfo.bluetoothStateChanged.connect(self.updateBluetoothState)

    def setupDisplay(self):
        self.displayInfo = QSystemDisplayInfo()
        self._displayBrightness = self.displayInfo.displayBrightness(0)
        self._colorDepth = self.displayInfo.colorDepth(0)

    def setupStorage(self):
        self.storageInfo = QSystemStorageInfo()
        self._volumeNames = self.storageInfo.logicalDrives()

    @QtCore.Slot(str, result=str)
    def storageType(self, volumeName):
        names = {
            QSystemStorageInfo.InternalDrive: "Internal",
            QSystemStorageInfo.RemovableDrive: "Removable",
            QSystemStorageInfo.CdromDrive: "CD-Rom",
            QSystemStorageInfo.RemoteDrive: "Network",
        }

        volType = self.storageInfo.typeForDrive(volumeName)

        return names.get(volType, "Unknown")

    @QtCore.Slot(str, result=str)
    def totalStorageSize(self, volumeName):
        return self.convert_bytes(self.storageInfo.totalDiskSpace(volumeName))

    @QtCore.Slot(str, result=str)
    def availableStorageSize(self, volumeName):
        return self.convert_bytes(self.storageInfo.availableDiskSpace(volumeName))

    def convert_bytes(self, bytes):
        # From http://www.5dollarwhitebox.org/drupal/node/84
        bytes = float(bytes)
        if bytes >= 1099511627776:
            terabytes = bytes / 1099511627776
            size = '%.2fT' % terabytes
        elif bytes >= 1073741824:
            gigabytes = bytes / 1073741824
            size = '%.2fG' % gigabytes
        elif bytes >= 1048576:
            megabytes = bytes / 1048576
            size = '%.2fM' % megabytes
        elif bytes >= 1024:
            kilobytes = bytes / 1024
            size = '%.2fK' % kilobytes
        else:
            size = '%.2fb' % bytes
        return size

    def setupNetwork(self):
        self.networkInfo = QSystemNetworkInfo()

    def modeEnumForName(self, name):
        try:
            mode = getattr(QSystemNetworkInfo, name.capitalize() + "Mode")
        except AttributeError as e:
            print e
            return None

        return mode

    @QtCore.Slot(str, result=str)
    def networkStatus(self, modeName):
        mode = self.modeEnumForName(modeName)
        status = self.networkInfo.networkStatus(mode)
        statusName = str(status).split('.')[-1]
        # Split the CamelCase enum name
        import re
        return re.sub(r'([a-z])([A-Z])', r'\1 \2', statusName)

    @QtCore.Slot(str, result=str)
    def networkName(self, modeName):
        mode = self.modeEnumForName(modeName)
        name = self.networkInfo.networkName(mode)
        return name if name else "<Unknown>"

    @QtCore.Slot(str, result=str)
    def networkInterfaceName(self, modeName):
        mode = self.modeEnumForName(modeName)
        name = self.networkInfo.interfaceForMode(mode).humanReadableName()
        return name if name else "<Unknown>"

    @QtCore.Slot(str, result=str)
    def networkMacAddress(self, modeName):
        mode = self.modeEnumForName(modeName)
        mac = self.networkInfo.macAddress(mode)
        return mac if mac else "<Unknown>"

    @QtCore.Slot(str, result=int)
    def networkSignalStrength(self, modeName):
        mode = self.modeEnumForName(modeName)
        return self.networkInfo.networkSignalStrength(mode)

    @QtCore.Slot(result=str)
    def cellId(self):
        cell = self.networkInfo.cellId()
        return str(cell) if cell != -1 else "<Unavailable>"

    @QtCore.Slot(result=str)
    def locationAreaCode(self):
        code = self.networkInfo.locationAreaCode()
        return str(code) if code != -1 else "<Unavailable>"

    @QtCore.Slot(result=str)
    def currentMCC(self):
        code = self.networkInfo.currentMobileCountryCode()
        return code if code else "<Unavailable>"

    @QtCore.Slot(result=str)
    def currentMNC(self):
        code = self.networkInfo.currentMobileNetworkCode()
        return code if code else "<Unavailable>"

    @QtCore.Slot(result=str)
    def homeMCC(self):
        code = self.networkInfo.homeMobileCountryCode()
        return code if code else "<Unavailable>"

    @QtCore.Slot(result=str)
    def homeMNC(self):
        code = self.networkInfo.homeMobileNetworkCode()
        return code if code else "<Unavailable>"

    def setupScreenSaver(self):
        self.saverInfo = QSystemScreenSaver(self)
        self._screenSaverInhibited = self.saverInfo.screenSaverInhibited()

    def updateBluetoothState(self, on):
        self._bluetoothState = on
        self.changed.emit()

    def updateBatteryStatus(self, status):
        self._batteryLevel = status
        self.emit(QtCore.SIGNAL('changed()'))

    def displayBatteryStatus(self, status):
        pass

    def updatePowerState(self, newState):
        pass

    def updateSimStatus(self):
        if self.deviceInfo:
            status = self.deviceInfo.simStatus()
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

            self._simStatus = simstring


    def updateProfile(self):
        if self.deviceInfo:
            current = self.deviceInfo.currentProfile()
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

            self._profile = profilestring

class SystemInfoUI(QtCore.QObject):
    def __init__(self):
        super(SystemInfoUI, self).__init__()
        self.view = QtDeclarative.QDeclarativeView()
        self.rc = self.view.rootContext()

        self.model = SystemInfoModel()
        self.rc.setContextProperty('sysinfo', self.model)

        self.view.setSource('main.qml')

        if "-no-fs" in sys.argv:
            self.view.show()
        else:
            self.view.showFullScreen()

        self.systemInfo = QSystemInfo(self)

if __name__ == "__main__":
    app = QtGui.QApplication([])
    ui = SystemInfoUI()
    app.exec_()
