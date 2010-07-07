# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'batterypublisher.ui'
#
# Created: Wed Jul  7 11:34:58 2010
#      by: PySide uic UI code generator
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_BatteryPublisher(object):
    def setupUi(self, BatteryPublisher):
        BatteryPublisher.setObjectName("BatteryPublisher")
        BatteryPublisher.resize(400, 125)
        self.gridLayout = QtGui.QGridLayout(BatteryPublisher)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(BatteryPublisher)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(322, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(BatteryPublisher)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)
        self.batteryCharge = QtGui.QSlider(BatteryPublisher)
        self.batteryCharge.setMaximum(100)
        self.batteryCharge.setSingleStep(5)
        self.batteryCharge.setPageStep(25)
        self.batteryCharge.setProperty("value", 50)
        self.batteryCharge.setOrientation(QtCore.Qt.Horizontal)
        self.batteryCharge.setTickPosition(QtGui.QSlider.TicksBothSides)
        self.batteryCharge.setTickInterval(25)
        self.batteryCharge.setObjectName("batteryCharge")
        self.gridLayout.addWidget(self.batteryCharge, 1, 0, 1, 3)
        self.buttonBox = QtGui.QDialogButtonBox(BatteryPublisher)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 3)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 3, 0, 1, 3)
        self.charging = QtGui.QCheckBox(BatteryPublisher)
        self.charging.setObjectName("charging")
        self.gridLayout.addWidget(self.charging, 2, 0, 1, 3)

        self.retranslateUi(BatteryPublisher)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), BatteryPublisher.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), BatteryPublisher.reject)
        QtCore.QMetaObject.connectSlotsByName(BatteryPublisher)

    def retranslateUi(self, BatteryPublisher):
        BatteryPublisher.setWindowTitle(QtGui.QApplication.translate("BatteryPublisher", "Battery Publisher", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("BatteryPublisher", "Empty", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("BatteryPublisher", "Full", None, QtGui.QApplication.UnicodeUTF8))
        self.charging.setText(QtGui.QApplication.translate("BatteryPublisher", "Charging", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    BatteryPublisher = QtGui.QDialog()
    ui = Ui_BatteryPublisher()
    ui.setupUi(BatteryPublisher)
    BatteryPublisher.show()
    sys.exit(app.exec_())

