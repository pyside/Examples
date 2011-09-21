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
from QtMobility.Contacts import QContactManager, QContactPhoneNumber, QContact
from QtMobility.Contacts import QContactAddress, QContactEmailAddress, QContactType
from QtMobility.Contacts import QContactName


class MyContactManager(QObject):

    def __init__(self):
        QObject.__init__(self)

        self._availableManagers = {}
        self._contacts = []

        self.initialisedManagers = {}
        self.manager = None
        self.contactId = 0

        self._errorMessage = ""
        self._emailEnabled = False
        self._addressEnabled = True

        availableMgrs = QContactManager.availableManagers()
        availableMgrs.remove("invalid")
        for managerName in availableMgrs:
            params = {}
            managerUri = QContactManager.buildUri(managerName, params)
            self._availableManagers[managerName] =  managerUri

        self.selectManager(self.availableManagers[0])

    # Email Enabled property
    onErrorMessageChanged = Signal()

    @Property(str, notify=onErrorMessageChanged)
    def errorMessage(self):
        return self._errorMessage

    @errorMessage.setter
    def setErrorMessage(self, value):
        self._errorMessage = value
        self.onErrorMessageChanged.emit()

    # Email Enabled property
    onEmailEnabledChanged = Signal()

    @Property("bool", notify=onEmailEnabledChanged)
    def emailEnabled(self):
        return self._emailEnabled

    @emailEnabled.setter
    def setEmailEnabled(self, value):
        self._emailEnabled = value
        self.onEmailEnabledChanged.emit()

    # Address Enabled property
    onAddressEnabledChanged = Signal()

    @Property("bool", notify=onAddressEnabledChanged)
    def addressEnabled(self):
        return self._addressEnabled

    @addressEnabled.setter
    def setAddressEnabled(self, value):
        self._addressEnabled = value
        self.onAddressEnabledChanged.emit()

    @Property("QStringList", constant=True)
    def availableManagers(self):
        return self._availableManagers.keys()

    # List of contacts changed property
    onContactsChanged = Signal()

    @Property("QStringList", notify=onContactsChanged)
    def contactsNames(self):
        return [x[0] for x in self._contacts]

    onSelectedContactChanged = Signal()

    def emitContactsChanged(self):
        self.onContactsChanged.emit()

    @Property("QStringList", notify=onSelectedContactChanged)
    def contactData(self):
        if not self.contactId:
            print "Trying to get data while no contact selected..."
            return ["", "", "", ""]

        print "Getting existing contact data"

        contact = self.manager.contact(self.contactId)

        name = self.manager.synthesizedContactDisplayLabel(contact)
        phone = contact.detail(QContactPhoneNumber.DefinitionName).value(QContactPhoneNumber.FieldNumber)

        if self.emailEnabled:
            emailObj = contact.detail(QContactEmailAddress.DefinitionName)
            email = emailObj.value(QContactEmailAddress.FieldEmailAddress)
        else:
            email = ""

        if self.addressEnabled:
            addressObj = contact.detail(QContactAddress.DefinitionName)
            address = addressObj.value(QContactAddress.FieldStreet)
        else:
            address = ""

        return name, phone, email, address

    @Slot(int)
    def selectContact(self, idx):
        if idx == -1:
            self.contactId = 0
        else:
            self.contactId = self._contacts[idx][1]

    @Slot(str)
    def selectManager(self, name):
        managerUri = self._availableManagers[name]

        # first, check to see if they reselected the same backend.
        if self.manager and self.manager.managerUri() == managerUri:
            return

        # the change is real.  update.
        if self.initialisedManagers.has_key(managerUri):
            self.manager = self.initialisedManagers[managerUri]
        else:
            self.manager = QContactManager.fromUri(managerUri)
            if self.manager.error():
                print "Failed to open store...."
                del self.manager
                self.manager = None
                return
            self.initialisedManagers[managerUri] = self.manager

        defs = self.manager.detailDefinitions(QContactType.TypeContact)

        self.emailEnabled = bool(defs["EmailAddress"])
        self.addressEnabled = bool(defs["Address"])

        self.updateContactList()

    def updateContactList(self):
        self._contacts = []

        for contact in self.manager.contacts():
            name = self.manager.synthesizedContactDisplayLabel(contact)
            self._contacts.append((name, contact.localId()))
            self.emitContactsChanged()

    saveEmptyName = Signal()

    @Slot(str, str, str, str, result=bool)
    def saveContact(self, name, phone, email, address):
        if not self.manager:
            qWarning("No manager selected, cannot save")
            return

        if self.contactId:
            print "Updating existing contact"
            contact = self.manager.contact(self.contactId)
        else:
            print "Creating new contact"
            contact = QContact()

        if not name:
            self.errorMessage = "Name must not be empty!"
            return False

        # Name
        if name != self.manager.synthesizedContactDisplayLabel(contact):
            saveNameField = self.nameField()
            if saveNameField:
                nm = QContactName(contact.detail(QContactName().DefinitionName))
                nm.setValue(saveNameField, name)
                contact.saveDetail(nm)

        # Phone
        phoneObj = QContactPhoneNumber(contact.detail(QContactPhoneNumber.DefinitionName))
        phoneObj.setNumber(phone)
        contact.saveDetail(phoneObj)

        # Email
        if self.emailEnabled:
            emailObj = QContactEmailAddress(contact.detail(QContactEmailAddress.DefinitionName))
            emailObj.setEmailAddress(email)
            contact.saveDetail(emailObj)

        # Address
        if self.addressEnabled:
            addressObj = QContactAddress(contact.detail(QContactAddress.DefinitionName))
            addressObj.setStreet(address)
            contact.saveDetail(addressObj)

        contact = self.manager.compatibleContact(contact)
        success = self.manager.saveContact(contact)
        if not success:
            qWarning("Failed to save contact")

        self.updateContactList()

        return True


    def nameField(self):
        # return the field which the name data should be saved in.
        if not self.manager:
            return ""

        defs = self.manager.detailDefinitions(QContactType.TypeContact)
        nameDef = defs[QContactName.DefinitionName]
        if QContactName.FieldCustomLabel in nameDef.fields():
            return QContactName.FieldCustomLabel
        elif QContactName.FieldFirstName in nameDef.fields():
            return QContactName.FieldFirstName
        else:
            return ""

def main():
    app = QApplication([])
    view = QDeclarativeView()
    manager = MyContactManager()
    context = view.rootContext()
    context.setContextProperty("manager", manager)

    url = QUrl('main.qml')
    view.setSource(url)
    view.showFullScreen()

    app.exec_()


if __name__ == '__main__':
    main()



