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

    def _currentLanguage(self): return self.__currentLanguage
    def _displayBrightness(self): return self.__displayBrightness
    def _colorDepth(self): return self.__colorDepth
    def _imsi(self): return self.__imsi
    def _imei(self): return self.__imei
    def _manufacturer(self): return self.__manufacturer
    def _product(self): return self.__product
    def _model(self): return self.__model
    def _profile(self): return self.__profile
    def _inputMethod(self): return self.__inputMethod
    def _bluetoothPower(self): return self.__bluetoothPower
    def _availableLanguages(self): return self.__availableLanguages
    def _deviceLock(self): return self.__deviceLock

    #@QtCore.Property(str, notify=changed)
    #def currentLanguage(self):
        #return self.__currentLanguage

    currentLanguage = QtCore.Property(str, _currentLanguage, notify=changed)
    displayBrightness = QtCore.Property(int, _displayBrightness, notify=changed)
    colorDepth = QtCore.Property(int, _colorDepth, notify=changed)
    imei = QtCore.Property(str, _imei, notify=changed)
    imsi = QtCore.Property(str, _imsi, notify=changed)
    manufacturer = QtCore.Property(str, _manufacturer, notify=changed)
    product = QtCore.Property(str, _product, notify=changed)
    model = QtCore.Property(str, _model, notify=changed)
    profile = QtCore.Property(str, _profile, notify=changed)
    inputMethod = QtCore.Property(str, _inputMethod, notify=changed)
    deviceLock = QtCore.Property(bool, _deviceLock, notify=changed)
    availableLanguages = QtCore.Property("QStringList", _availableLanguages, notify=changed)

    def setupAll(self):
        self.setupGeneral()
        self.setupDevice()
        self.setupDisplay()

    def setupGeneral(self):
        self.systemInfo = QSystemInfo(self)

        self.__currentLanguage = self.systemInfo.currentLanguage()
        self.__availableLanguages = self.systemInfo.availableLanguages()
        print self.__availableLanguages
        self.emit(QtCore.SIGNAL('changed()'))

    def setupDevice(self):
        self.di = QSystemDeviceInfo(self)
        self.__batteryLevel = self.di.batteryLevel()
        self.di.batteryLevelChanged.connect(self.updateBatteryStatus)
        self.di.batteryStatusChanged.connect(self.displayBatteryStatus)
        self.di.powerStateChanged.connect(self.updatePowerState)
        self.__imei = self.di.imei()
        self.__imsi = self.di.imsi()
        self.__manufacturer = self.di.manufacturer()
        self.__model = self.di.model()
        self.__product = self.di.productName()
        self.__deviceLock = self.di.isDeviceLocked()

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

        self.__inputMethod = " ".join(inputs)
        self.updateSimStatus()
        self.updateProfile()

        #self.di.currentProfileChanged.connect(self.onProfileChanged)

        self.emit(QtCore.SIGNAL('changed()'))
    
    def setupDisplay(self):
        self.di = QSystemDisplayInfo()
        self.__displayBrightness = self.di.displayBrightness(0)
        self.__colorDepth = self.di.colorDepth(0)
        self.emit(QtCore.SIGNAL('changed()'))

    
    def updateBatteryStatus(self, status):
        self.__batteryLevel = status
        self.emit(QtCore.SIGNAL('changed()'))

    def displayBatteryStatus(self, status):
        pass

    def updatePowerState(self, newState):
        pass


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

            self.__simStatus = simstring


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

            self.__profile = profilestring

class SystemInfoUI(QtCore.QObject):
    def __init__(self):
        super(SystemInfoUI, self).__init__()
        self.view = QtDeclarative.QDeclarativeView()
        self.glw = QtOpenGL.QGLWidget()
        self.view.setViewport(self.glw)
        
        #self.view.setSource(os.path.join('qml','main.qml'))
        self.view.setSource('main.qml')
        self.rc = self.view.rootContext()
        self.model = SystemInfoModel()
        self.model.setupAll()
        self.rc.setContextProperty('dataModel', self.model)
        self.view.showFullScreen()
        self.systemInfo = QSystemInfo(self)
   
    
if __name__ == "__main__":
    app = QtGui.QApplication([])
    ui = SystemInfoUI()
    app.exec_()
