# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'subscriberdialog_hor.ui'
#
# Created: Thu Jul  8 17:19:15 2010
#      by: PySide uic UI code generator
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_SubscriberDialog(object):
    def setupUi(self, SubscriberDialog):
        SubscriberDialog.setObjectName("SubscriberDialog")
        SubscriberDialog.resize(453, 339)
        self.verticalLayout = QtGui.QVBoxLayout(SubscriberDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(SubscriberDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
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
        self.connectButton = QtGui.QPushButton(SubscriberDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.connectButton.sizePolicy().hasHeightForWidth())
        self.connectButton.setSizePolicy(sizePolicy)
        self.connectButton.setObjectName("connectButton")
        self.horizontalLayout.addWidget(self.connectButton)
        self.buttonBox = QtGui.QDialogButtonBox(SubscriberDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tableWidget = QtGui.QTableWidget(SubscriberDialog)
        self.tableWidget.setMinimumSize(QtCore.QSize(0, 300))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)

        self.retranslateUi(SubscriberDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), SubscriberDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), SubscriberDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SubscriberDialog)
        SubscriberDialog.setTabOrder(self.basePath, self.connectButton)
        SubscriberDialog.setTabOrder(self.connectButton, self.buttonBox)
        SubscriberDialog.setTabOrder(self.buttonBox, self.tableWidget)

    def retranslateUi(self, SubscriberDialog):
        SubscriberDialog.setWindowTitle(QtGui.QApplication.translate("SubscriberDialog", "Subscriber", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("SubscriberDialog", "Base path:", None, QtGui.QApplication.UnicodeUTF8))
        self.basePath.setText(QtGui.QApplication.translate("SubscriberDialog", "/example", None, QtGui.QApplication.UnicodeUTF8))
        self.connectButton.setText(QtGui.QApplication.translate("SubscriberDialog", "Connect", None, QtGui.QApplication.UnicodeUTF8))

