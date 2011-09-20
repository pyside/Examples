'''
 Copyright (C) 2011 Nokia Corporation and/or its subsidiary(-ies).
 All rights reserved.
 Contact: Nokia Corporation (qt-info@nokia.com)

 This file is part of the Qt Mobility Components.

 $QT_BEGIN_LICENSE:LGPL$
 No Commercial Usage
 This file contains pre-release code and may not be distributed.
 You may use this file in accordance with the terms and conditions
 contained in the Technology Preview License Agreement accompanying
 this package.

 GNU Lesser General Public License Usage
 Alternatively, this file may be used under the terms of the GNU Lesser
 General Public License version 2.1 as published by the Free Software
 Foundation and appearing in the file LICENSE.LGPL included in the
 packaging of this file.  Please review the following information to
 ensure the GNU Lesser General Public License version 2.1 requirements
 will be met: http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html.

 In addition, as a special exception, Nokia gives you certain additional
 rights.  These rights are described in the Nokia Qt LGPL Exception
 version 1.1, included in the file LGPL_EXCEPTION.txt in this package.

 If you have questions regarding the use of this file, please contact
 Nokia at qt-info@nokia.com.
'''

import os
import sys

from PySide.QtCore import QObject, Signal, Slot, Property, QUrl, qWarning
from PySide.QtGui import QApplication
from PySide.QtDeclarative import QDeclarativeView
from QtMobility.ServiceFramework import QServiceManager


class ServiceManager(QObject):

    def __init__(self):
        QObject.__init__(self)

        self._services = []
        self._errorMessage = ""
        self._emailEnabled = False
        self._addressEnabled = True

        self.manager = QServiceManager(self)

        self.reloadServicesList()

    def reloadServicesList(self):
        self._services = []
        for service in self.manager.findServices():
            self._services.append(service)
        self.onServicesChanged.emit()

    onServicesChanged = Signal()

    @Property("QStringList", notify=onServicesChanged)
    def servicesNames(self):
        return self._services

    @Slot(str, int, result="QStringList")
    def serviceImplementations(self, serviceName, serviceIndex):
        print "Interfaces implemented by ", serviceName

        self._implementations = []
        for descriptor in self.manager.findInterfaces(serviceName):
            impSpec = "%s %d.%d" % (descriptor.interfaceName(),
                                    descriptor.majorVersion(),
                                    descriptor.minorVersion())

            if not serviceName:
                impSpec += " (" + descriptor.serviceName() + ")"

            default = self.manager.interfaceDefault(descriptor.interfaceName())
            if descriptor == default:
                impSpec += " (default)"

            self._implementations.append((impSpec, descriptor))
        return [x[0] for x in self._implementations]

    @Slot(str, int, str, int, result="QStringList")
    def implementationDetails(self, implementationSpec, implementationIndex,
                                    serviceName, serviceIndex):

        selectedImplementation = self._implementations[implementationIndex][1]
        implementationRef = self.manager.loadInterface(selectedImplementation)
        attributes = []

        if not implementationRef:
            return ["(Error loading service plugin)"]

        metaObject = implementationRef.metaObject()

        for i in range(metaObject.methodCount()):
            method = metaObject.method(i)
            attributes.append("[METHOD] " + method.signature())

        for i in range(metaObject.propertyCount()):
            p = metaObject.property(i)
            attributes.append("[PROPERTY] " + p.name())

        return attributes if attributes else ["(no attributes found)"]

    @Slot(int)
    def setDefault(self, index):
        descriptor = self._implementations[index][1]

        if descriptor.isValid():
            if self.manager.setInterfaceDefault(descriptor):
                pass

def main():
    app = QApplication([])
    view = QDeclarativeView()
    manager = ServiceManager()
    context = view.rootContext()
    context.setContextProperty("manager", manager)

    url = QUrl('main.qml')
    view.setSource(url)
    view.showFullScreen()

    app.exec_()


if __name__ == '__main__':
    main()


