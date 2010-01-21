#!/usr/bin/env python

#############################################################################
##
## Copyright (C) 2009 Nokia Corporation and/or its subsidiary(-ies).
## Contact: Qt Software Information (qt-info@nokia.com)
##
## This file is part of the example classes of the Qt Toolkit.
##
#############################################################################

from PySide import QtCore, QtGui


class SortedDict(dict):
    class Iterator(object):
        def __init__(self, sorted_dict):
            self._dict = sorted_dict
            self._keys = sorted(self._dict.keys())
            self._nr_items = len(self._keys)
            self._idx = 0

        def __iter__(self):
            return self

        def next(self):
            if self._idx >= self._nr_items:
                raise StopIteration

            key = self._keys[self._idx]
            value = self._dict[key]
            self._idx += 1

            return key, value

    def __iter__(self):
        return SortedDict.Iterator(self)

    iterkeys = __iter__


class AddressBook(QtGui.QWidget):
    def __init__(self, parent=None):
        super(AddressBook, self).__init__(parent)

        self.contacts = SortedDict()
        self.oldName = QtCore.QString()
        self.oldAddress = QtCore.QString()

        nameLabel = QtGui.QLabel(self.tr("Name:"))
        self.nameLine = QtGui.QLineEdit()
        self.nameLine.setReadOnly(True)

        addressLabel = QtGui.QLabel(self.tr("Address:"))
        self.addressText = QtGui.QTextEdit()
        self.addressText.setReadOnly(True)

        self.addButton = QtGui.QPushButton(self.tr("&Add"))
        self.addButton.show()
        self.submitButton = QtGui.QPushButton(self.tr("&Submit"))
        self.submitButton.hide()
        self.cancelButton = QtGui.QPushButton(self.tr("&Cancel"))
        self.cancelButton.hide()
        self.nextButton = QtGui.QPushButton(self.tr("&Next"))
        self.nextButton.setEnabled(False)
        self.previousButton = QtGui.QPushButton(self.tr("&Previous"))
        self.previousButton.setEnabled(False)

        self.connect(self.addButton,QtCore.SIGNAL("clicked()"),self.addContact)
        self.connect(self.submitButton,QtCore.SIGNAL("clicked()"),self.submitContact)
        self.connect(self.cancelButton,QtCore.SIGNAL("clicked()"),self.cancel)
        self.connect(self.nextButton,QtCore.SIGNAL("clicked()"), self.next)
        self.connect(self.previousButton,QtCore.SIGNAL("clicked()"),self.previous)

        buttonLayout1 = QtGui.QVBoxLayout()
        buttonLayout1.addWidget(self.addButton, QtCore.Qt.AlignTop)
        buttonLayout1.addWidget(self.submitButton)
        buttonLayout1.addWidget(self.cancelButton)
        buttonLayout1.addStretch()

        buttonLayout2 = QtGui.QHBoxLayout()
        buttonLayout2.addWidget(self.previousButton)
        buttonLayout2.addWidget(self.nextButton)

        mainLayout = QtGui.QGridLayout()
        mainLayout.addWidget(nameLabel, 0, 0)
        mainLayout.addWidget(self.nameLine, 0, 1)
        mainLayout.addWidget(addressLabel, 1, 0, QtCore.Qt.AlignTop)
        mainLayout.addWidget(self.addressText, 1, 1)
        mainLayout.addLayout(buttonLayout1, 1, 2)
        mainLayout.addLayout(buttonLayout2, 3, 1)

        self.setLayout(mainLayout)
        self.setWindowTitle(self.tr("Simple Address Book"))

    def addContact(self):
        self.oldName = self.nameLine.text()
        self.oldAddress = self.addressText.toPlainText()

        self.nameLine.clear()
        self.addressText.clear()

        self.nameLine.setReadOnly(False)
        self.nameLine.setFocus(QtCore.Qt.OtherFocusReason)
        self.addressText.setReadOnly(False)

        self.addButton.setEnabled(False)
        self.nextButton.setEnabled(False)
        self.previousButton.setEnabled(False)
        self.submitButton.show()
        self.cancelButton.show()

    def submitContact(self):
        name = self.nameLine.text()
        address = self.addressText.toPlainText()

        if name == "" or address == "":
            QtGui.QMessageBox.information(self, self.tr("Empty Field"),
                    self.tr("Please enter a name and address."))
            return

        if name not in self.contacts:
            self.contacts[name] = address
            QtGui.QMessageBox.information(self, self.tr("Add Successful"),
                    self.tr("\"%1\" has been added to your address book.").arg(name))
        else:
            QtGui.QMessageBox.information(self, self.tr("Add Unsuccessful"),
                    self.tr("Sorry, \"%1\" is already in your address book.").arg(name))
            return

        if not self.contacts:
            self.nameLine.clear()
            self.addressText.clear()

        self.nameLine.setReadOnly(True)
        self.addressText.setReadOnly(True)
        self.addButton.setEnabled(True)

        number = len(self.contacts)
        self.nextButton.setEnabled(number > 1)
        self.previousButton.setEnabled(number > 1)

        self.submitButton.hide()
        self.cancelButton.hide()

    def cancel(self):
        self.nameLine.setText(self.oldName)
        self.addressText.setText(self.oldAddress)

        if not self.contacts:
            self.nameLine.clear()
            self.addressText.clear()

        self.nameLine.setReadOnly(True)
        self.addressText.setReadOnly(True)
        self.addButton.setEnabled(True)

        number = len(self.contacts)
        self.nextButton.setEnabled(number > 1)
        self.previousButton.setEnabled(number > 1)

        self.submitButton.hide()
        self.cancelButton.hide()

    def next(self):
        name = self.nameLine.text()
        it = iter(self.contacts)

        try:
            while True:
                this_name, _ = it.next()

                if this_name == name:
                    next_name, next_address = it.next()
                    break
        except StopIteration:
            next_name, next_address = iter(self.contacts).next()

        self.nameLine.setText(next_name)
        self.addressText.setText(next_address)

    def previous(self):
        name = self.nameLine.text()

        prev_name = prev_address = None
        for this_name, this_address in self.contacts:
            if this_name == name:
                break

            prev_name = this_name
            prev_address = this_address
        else:
            self.nameLine.clear()
            self.addressText.clear()
            return

        if prev_name is None:
            for prev_name, prev_address in self.contacts:
                pass

        self.nameLine.setText(prev_name)
        self.addressText.setText(prev_address)


if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)

    addressBook = AddressBook()
    addressBook.show()

    sys.exit(app.exec_())
