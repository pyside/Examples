#!/usr/bin/env python

from PySide import QtCore, QtGui
import sys


class ComplexWizard(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)

        self.history = []

        self.cancelButton = QtGui.QPushButton(self.tr("Cancel"))
        self.backButton = QtGui.QPushButton(self.tr("< &Back"))
        self.nextButton = QtGui.QPushButton(self.tr("Next >"))
        self.finishButton = QtGui.QPushButton(self.tr("&Finish"))

        self.connect(self.cancelButton, QtCore.SIGNAL("clicked()"), self.reject)
        self.connect(self.backButton, QtCore.SIGNAL("clicked()"), self.backButtonClicked)
        self.connect(self.nextButton, QtCore.SIGNAL("clicked()"), self.nextButtonClicked)
        self.connect(self.finishButton, QtCore.SIGNAL("clicked()"), self.accept)

        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(self.cancelButton)
        buttonLayout.addWidget(self.backButton)
        buttonLayout.addWidget(self.nextButton)
        buttonLayout.addWidget(self.finishButton)

        self.mainLayout = QtGui.QVBoxLayout()
        self.mainLayout.addLayout(buttonLayout)
        self.setLayout(self.mainLayout)

    def historyPages(self):
        return self.history

    def setFirstPage(self, page):
        page.resetPage()
        self.history.append(page)
        self.switchPage(None)

    def backButtonClicked(self):
        oldpage = self.history.pop()
        oldpage.resetPage()
        self.switchPage(oldpage)

    def nextButtonClicked(self):
        oldpage = self.history[-1]
        newpage = oldpage.nextPage()
        newpage.resetPage()
        self.history.append(newpage)
        self.switchPage(oldpage)

    def completeStateChanged(self):
        currentpage = self.history[-1]
        if currentpage.isLastPage():
            self.finishButton.setEnabled(currentpage.isComplete())
        else:
            self.nextButton.setEnabled(currentpage.isComplete())

    def switchPage(self, oldPage):
        if oldPage is not None:
            oldPage.hide()
            self.mainLayout.removeWidget(oldPage)
            self.disconnect(oldPage, QtCore.SIGNAL("completeStateChanged())"),
                            self.completeStateChanged)

        newpage = self.history[-1]
        self.mainLayout.insertWidget(0, newpage)
        newpage.show()
        newpage.setFocus()
        self.connect(newpage, QtCore.SIGNAL("completeStateChanged()"),
                     self.completeStateChanged)

        self.backButton.setEnabled(len(self.history) != 1)
        if newpage.isLastPage():
            self.nextButton.setEnabled(False)
            self.finishButton.setDefault(True)
        else:
            self.nextButton.setDefault(True)
            self.finishButton.setEnabled(False)

        self.completeStateChanged()


class WizardPage(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.hide()

    def resetPage(self):
        pass

    def nextPage(self):
        return None

    def isLastPage(self):
        return False

    def isComplete(self):
        return True


class LicenseWizard(ComplexWizard):
    def __init__(self, parent=None):
        ComplexWizard.__init__(self, parent)

        self.titlePage = TitlePage(self)
        self.evaluatePage = EvaluatePage(self)
        self.registerPage = RegisterPage(self)
        self.detailsPage = DetailsPage(self)
        self.finishPage = FinishPage(self)

        self.setFirstPage(self.titlePage)

        self.setWindowTitle(self.tr("Complex Wizard"))
        self.resize(480, 200)


class LicenseWizardPage(WizardPage):
    def __init__(self, wizard):
        WizardPage.__init__(self, wizard)

        self.wizard = wizard


class TitlePage(LicenseWizardPage):
    def __init__(self, wizard):
        LicenseWizardPage.__init__(self, wizard)

        self.topLabel = QtGui.QLabel(self.tr(
                            "<center><font color=\"blue\" size=\"5\"><b><i>"
                            "Super Product One</i></b></font></center>"))

        self.registerRadioButton = QtGui.QRadioButton(self.tr("&Register your copy"))
        self.evaluateRadioButton = QtGui.QRadioButton(self.tr("&Evaluate our product"))
        self.setFocusProxy(self.registerRadioButton)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.topLabel)
        layout.addSpacing(10)
        layout.addWidget(self.registerRadioButton)
        layout.addWidget(self.evaluateRadioButton)
        layout.addStretch(1)
        self.setLayout(layout)

    def resetPage(self):
        self.registerRadioButton.setChecked(True)

    def nextPage(self):
        if self.evaluateRadioButton.isChecked():
            return self.wizard.evaluatePage
        else:
            return self.wizard.registerPage


class EvaluatePage(LicenseWizardPage):
    def __init__(self, wizard):
        LicenseWizardPage.__init__(self, wizard)

        self.topLabel = QtGui.QLabel(self.tr(
                                    "<center><b>Evaluate Super Product One"
                                    "</b></center>"))

        self.nameLabel = QtGui.QLabel(self.tr("&Name:"))
        self.nameLineEdit = QtGui.QLineEdit()
        self.nameLabel.setBuddy(self.nameLineEdit)
        self.setFocusProxy(self.nameLineEdit)

        self.emailLabel = QtGui.QLabel(self.tr("&Email address:"))
        self.emailLineEdit = QtGui.QLineEdit()
        self.emailLabel.setBuddy(self.emailLineEdit)

        self.bottomLabel = QtGui.QLabel(self.tr(
                                    "Please fill in both fields.\nThis will "
                                    "entitle you to a 30-day evaluation."))

        self.connect(self.nameLineEdit, QtCore.SIGNAL("textChanged(QString)"),
                     self, QtCore.SIGNAL("completeStateChanged()"))
        self.connect(self.emailLineEdit, QtCore.SIGNAL("textChanged(QString)"),
                     self, QtCore.SIGNAL("completeStateChanged()"))

        layout = QtGui.QGridLayout()
        layout.addWidget(self.topLabel, 0, 0, 1, 2)
        layout.setRowMinimumHeight(1, 10)
        layout.addWidget(self.nameLabel, 2, 0)
        layout.addWidget(self.nameLineEdit, 2, 1)
        layout.addWidget(self.emailLabel, 3, 0)
        layout.addWidget(self.emailLineEdit, 3, 1)
        layout.setRowMinimumHeight(4, 10)
        layout.addWidget(self.bottomLabel, 5, 0, 1, 2)
        layout.setRowStretch(6, 1)
        self.setLayout(layout)

    def resetPage(self):
        self.nameLineEdit.clear()
        self.emailLineEdit.clear()

    def nextPage(self):
        return self.wizard.finishPage

    def isComplete(self):
        return ( not self.nameLineEdit.text().isEmpty() and not self.emailLineEdit.text().isEmpty() )


class RegisterPage(LicenseWizardPage):
    def __init__(self, wizard):
        LicenseWizardPage.__init__(self, wizard)

        self.topLabel = QtGui.QLabel(self.tr(
                            "<center><b>Register your copy of Super Product "
                            "One</b></center>"))

        self.nameLabel = QtGui.QLabel(self.tr("&Name:"))
        self.nameLineEdit = QtGui.QLineEdit()
        self.nameLabel.setBuddy(self.nameLineEdit)
        self.setFocusProxy(self.nameLineEdit)

        self.upgradeKeyLabel = QtGui.QLabel(self.tr("&Upgrade key:"))
        self.upgradeKeyLineEdit = QtGui.QLineEdit()
        self.upgradeKeyLabel.setBuddy(self.upgradeKeyLineEdit)

        self.bottomLabel = QtGui.QLabel(self.tr(
                            "If you have an upgrade key, please fill in "
                            "the appropriate field."))

        self.connect(self.nameLineEdit, QtCore.SIGNAL("textChanged(QString)"),
                     self, QtCore.SIGNAL("completeStateChanged()"))

        layout = QtGui.QGridLayout()
        layout.addWidget(self.topLabel, 0, 0, 1, 2)
        layout.setRowMinimumHeight(1, 10)
        layout.addWidget(self.nameLabel, 2, 0)
        layout.addWidget(self.nameLineEdit, 2, 1)
        layout.addWidget(self.upgradeKeyLabel, 3, 0)
        layout.addWidget(self.upgradeKeyLineEdit, 3, 1)
        layout.setRowMinimumHeight(4, 10)
        layout.addWidget(self.bottomLabel, 5, 0, 1, 2)
        layout.setRowStretch(6, 1)
        self.setLayout(layout)

    def resetPage(self):
        self.nameLineEdit.clear()
        self.upgradeKeyLineEdit.clear()

    def nextPage(self):
        if self.upgradeKeyLineEdit.text().isEmpty():
            return self.wizard.detailsPage
        else:
            return self.wizard.finishPage

    def isComplete(self):
        return ( not self.nameLineEdit.text().isEmpty() )


class DetailsPage(LicenseWizardPage):
    def __init__(self, wizard):
        LicenseWizardPage.__init__(self, wizard)

        self.topLabel = QtGui.QLabel(self.tr("<center><b>Fill in your details</b></center>"))

        self.companyLabel = QtGui.QLabel(self.tr("&Company name:"))
        self.companyLineEdit = QtGui.QLineEdit()
        self.companyLabel.setBuddy(self.companyLineEdit)
        self.setFocusProxy(self.companyLineEdit)

        self.emailLabel = QtGui.QLabel(self.tr("&Email address:"))
        self.emailLineEdit = QtGui.QLineEdit()
        self.emailLabel.setBuddy(self.emailLineEdit)

        self.postalLabel = QtGui.QLabel(self.tr("&Postal address:"))
        self.postalLineEdit = QtGui.QLineEdit()
        self.postalLabel.setBuddy(self.postalLineEdit)

        self.connect(self.companyLineEdit, QtCore.SIGNAL("textChanged(QString)"),
                     self, QtCore.SIGNAL("completeStateChanged()"))
        self.connect(self.emailLineEdit, QtCore.SIGNAL("textChanged(QString)"),
                     self, QtCore.SIGNAL("completeStateChanged()"))
        self.connect(self.postalLineEdit, QtCore.SIGNAL("textChanged(QString)"),
                     self, QtCore.SIGNAL("completeStateChanged()"))

        layout = QtGui.QGridLayout()
        layout.addWidget(self.topLabel, 0, 0, 1, 2)
        layout.setRowMinimumHeight(1, 10)
        layout.addWidget(self.companyLabel, 2, 0)
        layout.addWidget(self.companyLineEdit, 2, 1)
        layout.addWidget(self.emailLabel, 3, 0)
        layout.addWidget(self.emailLineEdit, 3, 1)
        layout.addWidget(self.postalLabel, 4, 0)
        layout.addWidget(self.postalLineEdit, 4, 1)
        layout.setRowStretch(5, 1)
        self.setLayout(layout)

    def resetPage(self):
        self.companyLineEdit.clear()
        self.emailLineEdit.clear()
        self.postalLineEdit.clear()

    def nextPage(self):
        return self.wizard.finishPage

    def isComplete(self):
        return (not self.companyLineEdit.text().isEmpty() and 
                not self.emailLineEdit.text().isEmpty() and 
                not self.postalLineEdit.text().isEmpty())


class FinishPage(LicenseWizardPage):
    def __init__(self, wizard):
        LicenseWizardPage.__init__(self, wizard)

        self.topLabel = QtGui.QLabel(self.tr(
                                    "<center><b>Complete your registration"
                                    "</b></center>"))

        self.bottomLabel = QtGui.QLabel()
        self.bottomLabel.setWordWrap(True)

        self.agreeCheckBox = QtGui.QCheckBox(self.tr(
                                    "I agree to the terms and conditions of "
                                    "the license"))
        self.setFocusProxy(self.agreeCheckBox)

        self.connect(self.agreeCheckBox, QtCore.SIGNAL("toggled(bool)"),
                     self, QtCore.SIGNAL("completeStateChanged()"))

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.topLabel)
        layout.addSpacing(10)
        layout.addWidget(self.bottomLabel)
        layout.addWidget(self.agreeCheckBox)
        layout.addStretch(1)
        self.setLayout(layout)

    def resetPage(self):
        if self.wizard.evaluatePage in self.wizard.historyPages():
            licenseText = self.tr("Evaluation License Agreement: "
                        "You can use this software for 30 days and make one "
                        "back up, but you are not allowed to distribute it.")
        elif self.wizard.detailsPage in self.wizard.historyPages():
            licenseText = self.tr("First-Time License Agreement: "
                        "You can use this software subject to the license "
                        "you will receive by email.")
        else:
            licenseText = self.tr("Upgrade License Agreement: "
                        "This software is licensed under the terms of your "
                        "current license.")

        self.bottomLabel.setText(licenseText)
        self.agreeCheckBox.setChecked(False)

    def isLastPage(self):
        return True

    def isComplete(self):
        return self.agreeCheckBox.isChecked()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    wizard = LicenseWizard()
    sys.exit(wizard.exec_())
