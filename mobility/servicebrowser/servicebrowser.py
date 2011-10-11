"""
 Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
 All rights reserved.
 Contact: Nokia Corporation (qt-info@nokia.com)

 This file is part of the Qt Mobility Components.

 $QT_BEGIN_LICENSE:BSD$
 You may use this file under the terms of the BSD license as follows:

 "Redistribution and use in source and binary forms, with or without
 modification, are permitted provided that the following conditions are
 met:
    Redistributions of source code must retain the above copyright
     notice, this list of conditions and the following disclaimer.
    Redistributions in binary form must reproduce the above copyright
     notice, this list of conditions and the following disclaimer in
     the documentation and/or other materials provided with the
     distribution.
    Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
     the names of its contributors may be used to endorse or promote
     products derived from this software without specific prior written
     permission.

 THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
 $QT_END_LICENSE$
"""


from PySide.QtGui import QWidget, QListWidgetItem, QListWidget, QRadioButton, QGroupBox, QPushButton, QButtonGroup, QVBoxLayout, QLabel, QStackedLayout, QComboBox, QGridLayout
from PySide.QtCore import QCoreApplication, Qt
from QtMobility.ServiceFramework import QServiceManager, QServiceInterfaceDescriptor

class ServiceBrowser(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.serviceManager = QServiceManager(self)
        self.registerExampleServices()
        self.initWidgets()
        self.reloadServicesList()
        self.setWindowTitle(self.tr("Services Browser"))

    def __del__(self):
        self.unregisterExampleServices()

    def currentInterfaceImplChanged(self, current, previous):
        if not current:
            return

        descriptor = current.data(Qt.UserRole)
        self.reloadAttributesList()
        self.reloadAttributesRadioButtonText()
        if descriptor.isValid():
            self.defaultInterfaceButton.setText(self.tr("Set as default implementation for %s" % str(descriptor.interfaceName())))
        self.defaultInterfaceButton.setEnabled(True)

    def reloadServicesList(self):
        self.servicesListWidget.clear()
        services = self.serviceManager.findServices()
        for serv in services:
            self.servicesListWidget.addItem(serv)

        self.servicesListWidget.addItem(self.showAllServicesItem)
        self._services = services

    def reloadInterfaceImplementationsList(self):
        serviceName = None
        allServices = self.servicesListWidget.currentItem().text() == self.showAllServicesItem.text()
        if self.servicesListWidget.currentItem() and not allServices:
            serviceName = self.servicesListWidget.currentItem().text()
            self.interfacesGroup.setTitle(self.tr("Interfaces implemented by %s" % str(serviceName)))
        else:
            self.interfacesGroup.setTitle(self.tr("All interface implementations"))

        descriptors = self.serviceManager.findInterfaces(serviceName)
        self.attributesListWidget.clear()
        self.interfacesListWidget.clear()
        self._i = []
        for desc in descriptors:
            text = "%s %d.%d" % (desc.interfaceName(), desc.majorVersion(), desc.minorVersion())

            if not serviceName:
                text += " (" + desc.serviceName() + ")"

            defaultInterfaceImpl = self.serviceManager.interfaceDefault(desc.interfaceName())
            if desc == defaultInterfaceImpl:
                text += self.tr(" (default)")

            item = QListWidgetItem(text)
            item.setData(Qt.UserRole, desc)
            item._data = desc
            self.interfacesListWidget.addItem(item)

        self.defaultInterfaceButton.setEnabled(False)

    def reloadAttributesList(self):
        item = self.interfacesListWidget.currentItem()
        if not item:
            return

        selectedImpl = item.data(Qt.UserRole)
        implementationRef = None
        if self.selectedImplRadioButton.isChecked():
            implementationRef = self.serviceManager.loadInterface(selectedImpl)
        else:
            implementationRef = self.serviceManager.loadInterface(selectedImpl.interfaceName())

        self.attributesListWidget.clear()
        if not implementationRef:
            self.attributesListWidget.addItem(self.tr("(Error loading service plugin)"))
            return

        metaObject = implementationRef.metaObject()
        self.attributesGroup.setTitle(self.tr("Invokable attributes for %s class" % metaObject.className()))
        for i in range(metaObject.methodCount()):
            method = metaObject.method(i)
            self.attributesListWidget.addItem("[METHOD] " + method.signature())

        for i in range(metaObject.propertyCount()):
            p = metaObject.property(i)
            self.attributesListWidget.addItem("[PROPERTY] " + p.name())

    def setDefaultInterfaceImplementation(self):
        item = self.interfacesListWidget.currentItem()
        if not item:
            return

        descriptor = item.data(Qt.UserRole)
        if descriptor.isValid():
            if self.serviceManager.setInterfaceDefault(descriptor):
                currentIndex = self.interfacesListWidget.row(item)
                self.reloadInterfaceImplementationsList()
                self.interfacesListWidget.setCurrentRow(currentIndex)
            else:
                print "Unable to set default service for interface:",  descriptor.interfaceName()

    def registerExampleServices(self):
        exampleXmlFiles = ["filemanagerservice.xml", "bluetoothtransferservice.xml"]
        for fileName in exampleXmlFiles:
            path = "./xmldata/" + fileName
            self.serviceManager.addService(path)

    def unregisterExampleServices(self):
        self.serviceManager.removeService("FileManagerService")
        self.serviceManager.removeService("BluetoothTransferService")

    def reloadAttributesRadioButtonText(self):
        item = self.interfacesListWidget.currentItem()
        if not item:
            return

        selectedImpl = item.data(Qt.UserRole)
        defaultImpl = self.serviceManager.interfaceDefault(selectedImpl.interfaceName())
        self.defaultImplRadioButton.setText(self.tr("Default implementation for %s\n(currently provided by %s)" % (str(defaultImpl.interfaceName()), str(defaultImpl.serviceName()))))

    def initWidgets(self):
        self.showAllServicesItem = QListWidgetItem(self.tr("(All registered services)"))
        self.servicesListWidget = QListWidget()
        self.interfacesListWidget = QListWidget()
        self.interfacesListWidget.addItem(self.tr("(Select a service)"))
        self.attributesListWidget = QListWidget()
        self.attributesListWidget.addItem(self.tr("(Select an interface implementation)"))
        self.interfacesListWidget.setMinimumWidth(450)
        self.servicesListWidget.currentItemChanged.connect(self.reloadInterfaceImplementationsList)
        self.interfacesListWidget.currentItemChanged.connect(self.currentInterfaceImplChanged)
        self.defaultInterfaceButton = QPushButton(self.tr("Set as default implementation"))
        self.defaultInterfaceButton.setEnabled(False)
        self.defaultInterfaceButton.clicked.connect(self.setDefaultInterfaceImplementation)
        self.selectedImplRadioButton = QRadioButton(self.tr("Selected interface implementation"))
        self.defaultImplRadioButton = QRadioButton(self.tr("Default implementation"))
        self.selectedImplRadioButton.setChecked(True)
        self.radioButtons = QButtonGroup(self)
        self.radioButtons.addButton(self.selectedImplRadioButton)
        self.radioButtons.addButton(self.defaultImplRadioButton)
        self.radioButtons.buttonClicked.connect(self.reloadAttributesList)

        self.servicesGroup = QGroupBox(self.tr("Show services for:"))
        servicesLayout = QVBoxLayout()
        servicesLayout.addWidget(self.servicesListWidget)
        self.servicesGroup.setLayout(servicesLayout)

        self.interfacesGroup = QGroupBox(self.tr("Interface implementations"))
        interfacesLayout = QVBoxLayout()
        interfacesLayout.addWidget(self.interfacesListWidget)
        interfacesLayout.addWidget(self.defaultInterfaceButton)
        self.interfacesGroup.setLayout(interfacesLayout)

        self.attributesGroup = QGroupBox(self.tr("Invokable attributes"))
        attributesLayout = QVBoxLayout()
        self.attributesGroup.setLayout(attributesLayout)
        attributesLayout.addWidget(self.attributesListWidget)
        attributesLayout.addWidget(QLabel(self.tr("Show attributes for:")))
        attributesLayout.addWidget(self.selectedImplRadioButton)
        attributesLayout.addWidget(self.defaultImplRadioButton)

        self.attributesGroup.setLayout(attributesLayout)

        layout = QGridLayout()
        layout.addWidget(self.servicesGroup, 0, 0)
        layout.addWidget(self.attributesGroup, 0, 1, 2, 1)
        layout.addWidget(self.interfacesGroup, 1, 0)

        self.setLayout(layout)
