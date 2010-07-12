# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'subscriberdialog.ui'
#
# Created: Thu Jul  8 17:19:26 2010
#      by: PySide uic UI code generator
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_SubscriberDialog(object):
    def setupUi(self, SubscriberDialog):
        SubscriberDialog.setObjectName("SubscriberDialog")
        SubscriberDialog.resize(400, 320)
        self.verticalLayout = QtGui.QVBoxLayout(SubscriberDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(SubscriberDialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.basePath = QtGui.QLineEdit(SubscriberDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.basePath.sizePolicy().hasHeightForWidth())
        self.basePath.setSizePolicy(sizePolicy)
        self.basePath.setObjectName("basePath")
        self.horizontalLayout.addWidget(self.basePath)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.connectButton = QtGui.QPushButton(SubscriberDialog)
        self.connectButton.setObjectName("connectButton")
        self.verticalLayout.addWidget(self.connectButton)
        self.buttonBox = QtGui.QDialogButtonBox(SubscriberDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(SubscriberDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), SubscriberDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), SubscriberDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SubscriberDialog)
        SubscriberDialog.setTabOrder(self.basePath, self.connectButton)
        SubscriberDialog.setTabOrder(self.connectButton, self.buttonBox)

    def retranslateUi(self, SubscriberDialog):
        SubscriberDialog.setWindowTitle(QtGui.QApplication.translate("SubscriberDialog", "Subscriber", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("SubscriberDialog", "Base path:", None, QtGui.QApplication.UnicodeUTF8))
        self.basePath.setText(QtGui.QApplication.translate("SubscriberDialog", "/example", None, QtGui.QApplication.UnicodeUTF8))
        self.connectButton.setText(QtGui.QApplication.translate("SubscriberDialog", "Connect", None, QtGui.QApplication.UnicodeUTF8))

