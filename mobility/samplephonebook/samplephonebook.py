'''
Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
All rights reserved.
Contact: Nokia Corporation (qt-info@nokia.com)
Ported by PySide team (pyside@openbossa.org)

This file is part of the Qt Mobility Components.

$QT_BEGIN_LICENSE:BSD$
You may use this file under the terms of the BSD license as follows:

"Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:
  * Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.
  * Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in
    the documentation and/or other materials provided with the
    distribution.
  * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
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
'''

import sys

from PySide.QtCore import *
from PySide.QtGui import *

from QtMobility.Contacts import *
from QtMobility.Versit import *

MAX_AVATAR_DISPLAY_SIZE = 120;

class ContactListPage(QWidget):
    showEditorPage = Signal(int)
    #should use QContactManager - using object due to a bug in PySide
    managerChanged = Signal(object)
    clearFilter = Signal()

    def __init__(self, mainWindow = None, parent = None):
        QWidget.__init__(self, parent)

        self.manager = 0;
        self.availableManagers = {}
        self.idToListIndex = {}
        self.initialisedManagers = {}

        self.backendsCombo = QComboBox()
        availableMgrs = QContactManager.availableManagers()
        availableMgrs.remove("invalid")
        for managerName in availableMgrs:
            params = {}
            managerUri = QContactManager.buildUri(managerName, params)
            self.availableManagers[managerName] =  managerUri

        self.backendsCombo.addItems(availableMgrs)
        self.backendsCombo.currentIndexChanged.connect(self.backendSelected)

        bookLayout = QVBoxLayout()
        backendLayout = QFormLayout()
        backendLayout.addRow("Store:", self.backendsCombo)
        bookLayout.addLayout(backendLayout)

        self.contactsList = QListWidget()
        bookLayout.addWidget(self.contactsList)

        # Action buttons at the bottom
        btnLayout1 = QHBoxLayout()

        addBtn = QPushButton("&Add")
        addBtn.clicked.connect(self.addClicked)
        btnLayout1.addWidget(addBtn)

        editBtn = QPushButton("&Edit")
        editBtn.clicked.connect(self.editClicked)
        btnLayout1.addWidget(editBtn)

        deleteBtn = QPushButton("&Delete")
        deleteBtn.clicked.connect(self.deleteClicked)
        btnLayout1.addWidget(deleteBtn)

        bookLayout.addLayout(btnLayout1)

        self.setLayout(bookLayout)

        if mainWindow:
            optionsMenu = QMenu("&Contacts", self)
            mainWindow.menuBar().addMenu(optionsMenu)

            importAction = QAction(self)
            importAction.setText("&Import contacts...")
            importAction.triggered.connect(self.importClicked)
            optionsMenu.addAction(importAction)
            exportAction = QAction(self)
            exportAction.setText("&Export contacts...")
            exportAction.triggered.connect(self.exportClicked)
            optionsMenu.addAction(exportAction)
            optionsMenu.addSeparator()

            exitAction = QAction(self);
            exitAction.setText("E&xit")
            exitAction.triggered.connect(qApp.quit)
            optionsMenu.addAction(exitAction)

        # force update to backend.
        QTimer.singleShot(0, self.backendSelected)

    def __del__(self):
        self.initialisedManagers = self.initialisedManagers.values()
        while self.initialisedManagers:
            deleteMe = self.initialisedManagers.pop(0)
            del deleteMe

    def backendSelected(self):
        managerUri = self.availableManagers[self.backendsCombo.currentText()]

        # first, check to see if they reselected the same backend.
        if self.manager and self.manager.managerUri() == managerUri:
            return

        # the change is real.  update.
        if self.initialisedManagers.has_key(managerUri):
            self.manager = self.initialisedManagers[managerUri]
        else:
            self.manager = QContactManager.fromUri(managerUri)
            if self.manager.error():
                QMessageBox.information(self, "Failed!", "Failed to open store!\n(error code %s)"%self.manager.error())
                del self.manager
                self.manager = 0
                return
            self.initialisedManagers[managerUri] = self.manager

        # signal that the manager has changed.
        self.managerChanged.emit(self.manager)

        # and... rebuild the list.
        self.rebuildList()

    def rebuildList(self):
        self.contactsList.clear()
        self.idToListIndex.clear()
        self.contacts = self.manager.contacts()
        for contact in self.contacts:
            currItem = QListWidgetItem()
            currItem.setData(Qt.DisplayRole, contact.displayLabel())
            currItem.setData(Qt.UserRole, contact.localId()) # also store the id of the contact.
            self.idToListIndex[contact.localId()] = self.contactsList.count()
            self.contactsList.addItem(currItem)

    def addClicked(self):
        if self.manager:
            self.showEditorPage.emit(0)

    def editClicked(self):
        if self.contactsList.currentItem():
            self.showEditorPage.emit(self.contactsList.currentItem().data(Qt.UserRole))
        # else, nothing selected; ignore.

    def filterClicked(self):
        if self.manager:
            self.showFilterPage.emit(self.currentFilter)

    def deleteClicked(self):
        if not self.manager:
            qWarning("No manager selected; cannot delete.")
            return

        if not self.contactsList.currentItem():
            qWarning("Nothing to delete.")
            return

        contactId = self.contactsList.currentItem().data(Qt.UserRole)
        success = self.manager.removeContact(contactId)

        if success:
            item = self.contactsList.takeItem(self.contactsList.currentRow())
            del item
        else:
            QMessageBox.information(self, "Failed!", "Failed to delete contact!")

    def importClicked(self):
        if not self.manager:
            qWarning() << "No manager selected; cannot import"
            return

        fileName = QFileDialog.getOpenFileName(self, "Select vCard file", ".", "vCard files (*.vcf)")
        openfile = QFile(fileName[0])
        openfile.open(QIODevice.ReadOnly)
        if openfile.isReadable():
            reader = QVersitReader()
            reader.setDevice(openfile)
            if reader.startReading() and reader.waitForFinished():
                importer = QVersitContactImporter()
                if importer.importDocuments(reader.results()):
                    contacts = importer.contacts()
                    #it = contacts.begin()
                    #while it != contacts.end():
                    prunedcontacts = []
                    for it in contacts:
                        prunedcontacts.append(self.manager.compatibleContact(it))
                    self.manager.saveContacts(prunedcontacts)
                    self.rebuildList()

    def exportClicked(self):
        if not self.manager:
            qWarning() << "No manager selected; cannot export"
            return

        fileName = QFileDialog.getSaveFileName(self, "Save vCard", "./contacts.vcf", "vCards (*.vcf)")
        openfile = QFile(fileName[0])
        openfile.open(QIODevice.WriteOnly)
        if openfile.isWritable():
            exporter = QVersitContactExporter()
            if exporter.exportContacts(self.contacts, QVersitDocument.VCard30Type):
                documents = exporter.documents()
                writer = QVersitWriter()
                writer.setDevice(openfile)
                writer.startWriting(documents)
                writer.waitForFinished()

class ContactEditor(QWidget):
    showListPage = Signal()

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.manager = 0
        self.contactId = 0

        self.nameEdit = QLineEdit()
        self.phoneEdit = QLineEdit()
        self.emailEdit = QLineEdit()
        self.addrEdit = QLineEdit()
        self.avatarBtn = QPushButton("Set picture")
        self.clearAvatarBtn = QPushButton("Clear")
        self.avatarView = QLabel()
        self.avatarBtn.clicked.connect(self.avatarClicked)
        self.clearAvatarBtn.clicked.connect(self.clearAvatarClicked)

        detailsLayout = QFormLayout()
        nameLabel = QLabel("Name")
        phoneLabel = QLabel("Phone")
        emailLabel = QLabel("Email")
        addressLabel = QLabel("Address")
        avatarLabel = QLabel("Picture")
        avatarBtnLayout = QHBoxLayout()
        avatarBtnLayout.addWidget(self.avatarBtn)
        avatarBtnLayout.addWidget(self.clearAvatarBtn)
        if QApplication.desktop().availableGeometry().width() < 360:
            # Narrow screen: put label on separate line to textbox
            detailsLayout.addRow(nameLabel)
            detailsLayout.addRow(self.nameEdit)
            detailsLayout.addRow(phoneLabel)
            detailsLayout.addRow(self.phoneEdit)
            detailsLayout.addRow(emailLabel)
            detailsLayout.addRow(self.emailEdit)
            detailsLayout.addRow(addressLabel)
            detailsLayout.addRow(self.addrEdit)
            detailsLayout.addRow(avatarLabel)
            detailsLayout.addRow(avatarBtnLayout)
            detailsLayout.addRow(self.avatarView)
        else:
            # Wide screen: put label on same line as textbox
            detailsLayout.addRow(nameLabel, self.nameEdit)
            detailsLayout.addRow(phoneLabel, self.phoneEdit)
            detailsLayout.addRow(emailLabel, self.emailEdit)
            detailsLayout.addRow(addressLabel, self.addrEdit)
            detailsLayout.addRow(avatarLabel, avatarBtnLayout)
            detailsLayout.addRow("", self.avatarView)

        detailsLayout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        detailsLayout.setSizeConstraint(QLayout.SetMinAndMaxSize)

        detailsScrollArea = QScrollArea()
        detailsScrollArea.setWidgetResizable(True)
        detailsContainer = QWidget(detailsScrollArea)
        detailsContainer.setLayout(detailsLayout)
        detailsScrollArea.setWidget(detailsContainer)

        editLayout = QVBoxLayout()
        editLayout.addWidget(detailsScrollArea)

        self.saveBtn = QPushButton("&Save")
        self.saveBtn.setDefault(True)
        self.saveBtn.clicked.connect(self.saveClicked)
        self.cancelBtn = QPushButton("&Cancel")
        self.cancelBtn.clicked.connect(self.cancelClicked)
        btnLayout = QHBoxLayout()
        btnLayout.addWidget(self.saveBtn)
        btnLayout.addWidget(self.cancelBtn)
        editLayout.addLayout(btnLayout)

        self.setLayout(editLayout)

    def setCurrentContact(self, manager, currentId):
        self.manager = manager
        self.contactId = currentId
        self.newAvatarPath = ""

        # Clear UI
        self.nameEdit.clear()
        self.phoneEdit.clear()
        self.emailEdit.clear()
        self.addrEdit.clear()

        if manager == 0:
            self.saveBtn.setEnabled(False)
            return

        # enable the UI.
        self.saveBtn.setEnabled(True)

        # otherwise, build from the contact details.
        curr = QContact()

        # Disable fields & buttons according to what the backend supports
        #TODO: remove ()
        defs = self.manager.detailDefinitions(QContactType().TypeContact)

        #name
        if self.contactId != 0:
            curr = self.manager.contact(self.contactId)
            self.nameEdit.setText(self.manager.synthesizedContactDisplayLabel(curr))

        # phonenumber
        #TODO: remove ()
        phn = curr.detail(QContactPhoneNumber().DefinitionName)
        self.phoneEdit.setText(phn.value(QContactPhoneNumber().FieldNumber))

        # email
        if defs["EmailAddress"]:
            #TODO: remove ()
            em = curr.detail(QContactEmailAddress().DefinitionName)
            self.emailEdit.setText(em.value(QContactEmailAddress().FieldEmailAddress))
            self.emailEdit.setReadOnly(False)
        else:
            self.emailEdit.setText("<not supported>")
            self.emailEdit.setReadOnly(True)

        # address
        if defs["Address"]:
            #TODO: remove ()
            adr = curr.detail(QContactAddress().DefinitionName)
            self.addrEdit.setText(adr.value(QContactAddress().FieldStreet)) # ugly hack.
            self.addrEdit.setReadOnly(False)
        else:
            self.addrEdit.setText("<not supported>")
            self.addrEdit.setReadOnly(true)

        # avatar viewer
        #TODO: remove ()
        if QContactAvatar().DefinitionName in defs or QContactThumbnail().DefinitionName in defs:
            self.avatarBtn.setEnabled(True)
            #TODO: remove ()
            av = QContactAvatar(curr.detail(QContactAvatar().DefinitionName))
            thumb = QContactThumbnail(curr.detail(QContactThumbnail().DefinitionName))
            self.avatarView.clear()
            self.newAvatarPath = av.imageUrl().toLocalFile()
            self.thumbnail = thumb.thumbnail()
            if self.thumbnail.isNull():
                if not self.newAvatarPath:
                    self.avatarView.clear()
                    self.clearAvatarBtn.setDisabled(True)
                else:
                    self.setAvatarPixmap(QPixmap(av.imageUrl().toLocalFile()))
                    self.thumbnail = QImage(av.imageUrl().toLocalFile())
            else:
                self.setAvatarPixmap(QPixmap.fromImage(self.thumbnail))
        else:
            self.avatarBtn.setDisabled(True)
            self.clearAvatarBtn.setDisabled(True)

    def nameField(self):
        # return the field which the name data should be saved in.
        if not self.manager:
            return ""

        #TODO: remove ()
        defs = self.manager.detailDefinitions(QContactType().TypeContact)
        nameDef = defs[QContactName().DefinitionName]
        if QContactName().FieldCustomLabel in nameDef.fields():
            return QContactName().FieldCustomLabel
        elif QContactName().FieldFirstName in nameDef.fields():
            return QContactName().FieldFirstName
        else:
            return ""

    def setAvatarPixmap(self, pixmap):
        if pixmap.isNull():
            return
        scaled = pixmap.scaled(QSize(MAX_AVATAR_DISPLAY_SIZE, MAX_AVATAR_DISPLAY_SIZE), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.avatarView.setPixmap(scaled)
        self.avatarView.setMaximumSize(scaled.size())
        self.clearAvatarBtn.setEnabled(True)

    def clearAvatarClicked(self):
        self.avatarView.clear()
        self.thumbnail = QImage()
        self.newAvatarPath = ""
        self.clearAvatarBtn.setDisabled(True)

    def avatarClicked(self):
    # put up a file dialog, and update the new avatar path.
        fileName = QFileDialog.getOpenFileName(self, "Select Contact Picture", ".", "Image Files (*.png *.jpg *.bmp)");

        if fileName:
            self.newAvatarPath = fileName[0]
            self.thumbnail = QImage(self.newAvatarPath)
            self.setAvatarPixmap(QPixmap.fromImage(self.thumbnail))

    def saveClicked(self):
        if not self.manager:
            qWarning("No manager selected; cannot save.")
        else:
            if self.contactId != 0:
                curr = self.manager.contact(self.contactId)
            else:
                curr = QContact()

            if not self.nameEdit.text():
                QMessageBox.information(self, "Failed!", "You must give a name for the contact!")
                return

            if self.nameEdit.text() != self.manager.synthesizedContactDisplayLabel(curr):
                # if the name has changed (ie, is different to the synthed label) then save it as a custom label.
                saveNameField = self.nameField()
                if saveNameField:
                    # TODO: remove this "cast" to QContactName and ()
                    nm = QContactName(curr.detail(QContactName().DefinitionName))
                    nm.setValue(saveNameField, self.nameEdit.text())
                    curr.saveDetail(nm)

            # TODO: remove this "cast" to QContactPhoneNumber and ()
            phn = QContactPhoneNumber(curr.detail(QContactPhoneNumber().DefinitionName))
            phn.setNumber(self.phoneEdit.text())
            curr.saveDetail(phn)

            if not self.emailEdit.isReadOnly():
                # TODO: remove this "cast" to QContactEmailAddress and ()
                em = QContactEmailAddress(curr.detail(QContactEmailAddress().DefinitionName))
                em.setEmailAddress(self.emailEdit.text())
                curr.saveDetail(em)

            if not self.addrEdit.isReadOnly():
                # TODO: remove this "cast" to QContactAddress and ()
                adr = QContactAddress(curr.detail(QContactAddress().DefinitionName))
                adr.setStreet(self.addrEdit.text())
                curr.saveDetail(adr)

            if self.avatarBtn.isEnabled():
                # TODO: remove this "cast" to QContactAvatar and ()
                av = QContactAvatar(curr.detail(QContactAvatar().DefinitionName))
                av.setImageUrl(QUrl(self.newAvatarPath))
                curr.saveDetail(av)

                # TODO: remove this "cast" to QContactThumbnail and ()
                thumb = QContactThumbnail(curr.detail(QContactThumbnail().DefinitionName))
                img = QImage(self.thumbnail)
                thumb.setThumbnail(img)
                curr.saveDetail(thumb)

            curr = self.manager.compatibleContact(curr)
            success = self.manager.saveContact(curr)
            if not success:
                QMessageBox.information("Failed!", "Failed to save contact!\n(error code %1)"%self.manager.error())

        self.showListPage.emit()

    def cancelClicked(self):
        self.showListPage.emit()

class PhoneBook(QMainWindow):

    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)

        self.manager = 0
        centralWidget = QWidget(self)

        self.editorPage = ContactEditor(centralWidget)
        self.editorPage.showListPage.connect(self.activateList)

        self.listPage = ContactListPage(self, centralWidget)
        self.listPage.showEditorPage.connect(self.activateEditor)
        self.listPage.managerChanged.connect(self.managerChanged)

        self.stackedWidget = QStackedWidget(centralWidget)
        self.stackedWidget.addWidget(self.listPage)
        self.stackedWidget.addWidget(self.editorPage)
        self.stackedWidget.setCurrentIndex(0)

        centralLayout = QVBoxLayout()
        centralLayout.addWidget(self.stackedWidget)
        centralWidget.setLayout(centralLayout)

        self.setCentralWidget(centralWidget)

    def activateEditor(self, contactId):
        self.editorPage.setCurrentContact(self.manager, contactId)
        self.stackedWidget.setCurrentIndex(1) # list = 0, editor = 1, find = 2.

    def activateList(self, filtr):
        self.currentFilter = filtr
        activateList() # call base now.

    def activateList(self):
        self.listPage.rebuildList()
        self.stackedWidget.setCurrentIndex(0) # list = 0, editor = 1, find = 2.

    def managerChanged(self, manager):
        self.manager = manager
        self.editorPage.setCurrentContact(self.manager, 0) # must reset the manager of the editor.

def main():
    app = QApplication(sys.argv)

    phoneBook = PhoneBook()
    phoneBook.show()

    app.exec_()

if __name__ == "__main__":
    main()
