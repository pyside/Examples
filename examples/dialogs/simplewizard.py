#!/usr/bin/env python

"""PySide port of the dialogs/simplewizard example from Qt v4.x"""

import sys
from PySide import QtCore, QtGui


class SimpleWizard(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)

        self.history = []
        self.numPages = 0
        
        self.cancelButton = QtGui.QPushButton(self.tr("Cancel"))
        self.backButton = QtGui.QPushButton(self.tr("< &Back"))
        self.nextButton = QtGui.QPushButton(self.tr("Next >"))
        self.finishButton = QtGui.QPushButton(self.tr("&Finish"))
    
        self.connect(self.cancelButton, QtCore.SIGNAL("clicked()"), self, QtCore.SLOT("reject()"))
        self.connect(self.backButton, QtCore.SIGNAL("clicked()"), self.backButtonClicked)
        self.connect(self.nextButton, QtCore.SIGNAL("clicked()"), self.nextButtonClicked)
        self.connect(self.finishButton, QtCore.SIGNAL("clicked()"), self, QtCore.SLOT("accept()"))
    
        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(self.cancelButton)
        buttonLayout.addWidget(self.backButton)
        buttonLayout.addWidget(self.nextButton)
        buttonLayout.addWidget(self.finishButton)
    
        self.mainLayout = QtGui.QVBoxLayout()
        self.mainLayout.addLayout(buttonLayout)
        self.setLayout(self.mainLayout)

    def setButtonEnabled(self, enable):
        if len(self.history) == self.numPages:
            self.finishButton.setEnabled(enable)
        else:
            self.nextButton.setEnabled(enable)

    def setNumPages(self, n):
        self.numPages = n
        self.history.append(self.createPage(0))
        self.switchPage(0)

    def backButtonClicked(self):
        self.nextButton.setEnabled(True)
        self.finishButton.setEnabled(True)
    
        oldPage = self.history.pop()
        self.switchPage(oldPage)
        del oldPage

    def nextButtonClicked(self):
        self.nextButton.setEnabled(True)
        self.finishButton.setEnabled(len(self.history) == self.numPages - 1)
    
        oldPage = self.history[-1]
        self.history.append(self.createPage(len(self.history)))
        self.switchPage(oldPage)

    def switchPage(self, oldPage):
        if oldPage:
            oldPage.hide()
            self.mainLayout.removeWidget(oldPage)

        newPage = self.history[-1]
        self.mainLayout.insertWidget(0, newPage)
        newPage.show()
        newPage.setFocus()
    
        self.backButton.setEnabled(len(self.history) != 1)
        if len(self.history) == self.numPages:
            self.nextButton.setEnabled(False)
            self.finishButton.setDefault(True)
        else:
            self.nextButton.setDefault(True)
            self.finishButton.setEnabled(False)

        self.setWindowTitle(self.tr("Simple Wizard - Step %1 of %2")
                                    .arg(len(self.history)).arg(self.numPages))
                       

class ClassWizard(SimpleWizard):
    def __init__(self, parent=None):
        SimpleWizard.__init__(self, parent)

        self.setNumPages(3)

    def createPage(self, index):
        if index == 0:
            self.firstPage = FirstPage(self)
            return self.firstPage
        elif index == 1:
            self.secondPage = SecondPage(self)
            return self.secondPage
        elif index == 2:
            self.thirdPage = ThirdPage(self)
            return self.thirdPage

        return 0

    def accept(self):
        className = self.firstPage.classNameLineEdit.text().toAscii()
        baseClass = self.firstPage.baseClassLineEdit.text().toAscii()
        qobjectMacro = self.firstPage.qobjectMacroCheckBox.isChecked()
        qobjectCtor = self.firstPage.qobjectCtorRadioButton.isChecked()
        qwidgetCtor = self.firstPage.qwidgetCtorRadioButton.isChecked()
        defaultCtor = self.firstPage.defaultCtorRadioButton.isChecked()
        copyCtor = self.firstPage.copyCtorCheckBox.isChecked()
    
        comment = self.secondPage.commentCheckBox.isChecked()
        protect = self.secondPage.protectCheckBox.isChecked()
        macroName = self.secondPage.macroNameLineEdit.text().toAscii()
        includeBase = self.secondPage.includeBaseCheckBox.isChecked()
        baseInclude = self.secondPage.baseIncludeLineEdit.text().toAscii()
    
        outputDir = QtCore.QString(self.thirdPage.outputDirLineEdit.text())
        header = QtCore.QString(self.thirdPage.headerLineEdit.text())
        implementation = QtCore.QString(self.thirdPage.implementationLineEdit.text())
    
        block = QtCore.QByteArray()
    
        if comment:
            block += "/*\n"
            block += "    " + header.toAscii() + "\n"
            block += "*/\n"
            block += "\n"

        if protect:
            block += "#ifndef " + macroName + "\n"
            block += "#define " + macroName + "\n"
            block += "\n"

        if includeBase:
            block += "#include " + baseInclude + "\n"
            block += "\n"

        block += "class " + className
        if  not baseClass.isEmpty():
            block += " : public " + baseClass
        block += "\n"
        block += "{\n"
    
        # qmake ignore Q_OBJECT
    
        if qobjectMacro:
            block += "    Q_OBJECT\n"
            block += "\n"

        block += "public:\n"
    
        if qobjectCtor:
            block += "    " + className + "(QObject *parent);\n"
        elif qwidgetCtor:
            block += "    " + className + "(QWidget *parent);\n"
        elif defaultCtor:
            block += "    " + className + "();\n"
            if copyCtor:
                block += "    " + className + "(const " + className + " &other);\n"
                block += "\n"
                block += "    " + className + " &operator=" + "(const " + className + " &other);\n"

        block += "};\n"
    
        if protect:
            block += "\n"
            block += "#endif\n"

        headerFile = QtCore.QFile(outputDir + "/" + header)
        if  not headerFile.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, self.tr("Simple Wizard"),
                                      self.tr("Cannot write file %1:\n%2")
                                              .arg(headerFile.fileName())
                                              .arg(headerFile.errorString()))
            return

        headerFile.write(block)
    
        block.clear()
    
        if comment:
            block += "/*\n"
            block += "    " + implementation.toAscii() + "\n"
            block += "*/\n"
            block += "\n"

        block += "#include \"" + header.toAscii() + "\"\n"
        block += "\n"
    
        if qobjectCtor:
            block += className + "::" + className + "(QObject *parent)\n"
            block += "    : " + baseClass + "(parent)\n"
            block += "{\n"
            block += "}\n"
        elif qwidgetCtor:
            block += className + "::" + className + "(QWidget *parent)\n"
            block += "    : " + baseClass + "(parent)\n"
            block += "{\n"
            block += "}\n"
        elif defaultCtor:
            block += className + "::" + className + "()\n"
            block += "{\n"
            block += "    // missing code\n"
            block += "}\n"
    
            if copyCtor:
                block += "\n"
                block += className + "::" + className + "(const " + className + " &other)\n"
                block += "{\n"
                block += "    *this = other;\n"
                block += "}\n"
                block += "\n"
                block += className + " &" + className + "::operator=(const " + className + " &other)\n"
                block += "{\n"
                if  not baseClass.isEmpty():
                    block += "    " + baseClass + "::operator=(other);\n"
                block += "    // missing code\n"
                block += "    return *this;\n"
                block += "}\n"

        implementationFile = QtCore.QFile(outputDir + "/" + implementation)
        if  not implementationFile.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, self.tr("Simple Wizard"),
                                      self.tr("Cannot write file %1:\n%2")
                                              .arg(implementationFile.fileName())
                                              .arg(implementationFile.errorString()))
            return

        implementationFile.write(block)
    
        QtGui.QDialog.accept(self)
        

class FirstPage(QtGui.QWidget):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)

        self.topLabel = QtGui.QLabel(self.tr("<center><b>Class information</b></center>"
                                             "<p>This wizard will generate a skeleton class "
                                             "definition and member function definitions."))
        self.topLabel.setWordWrap(False)
    
        self.classNameLabel = QtGui.QLabel(self.tr("Class &name:"))
        self.classNameLineEdit = QtGui.QLineEdit()
        self.classNameLabel.setBuddy(self.classNameLineEdit)
        self.setFocusProxy(self.classNameLineEdit)
    
        self.baseClassLabel = QtGui.QLabel(self.tr("&Base class:"))
        self.baseClassLineEdit = QtGui.QLineEdit()
        self.baseClassLabel.setBuddy(self.baseClassLineEdit)
    
        self.qobjectMacroCheckBox = QtGui.QCheckBox(self.tr("&Generate Q_OBJECT macro"))
    
        self.groupBox = QtGui.QGroupBox(self.tr("&Constructor"))
    
        self.qobjectCtorRadioButton = QtGui.QRadioButton(self.tr("&QObject-style constructor"))
        self.qwidgetCtorRadioButton = QtGui.QRadioButton(self.tr("Q&Widget-style constructor"))
        self.defaultCtorRadioButton = QtGui.QRadioButton(self.tr("&Default constructor"))
        self.copyCtorCheckBox = QtGui.QCheckBox(self.tr("&Also generate copy constructor "
                                                        "and assignment operator"))
    
        self.defaultCtorRadioButton.setChecked(True)
    
        self.connect(self.classNameLineEdit, QtCore.SIGNAL("textChanged(const QString &)"),
                self.classNameChanged)
        self.connect(self.defaultCtorRadioButton, QtCore.SIGNAL("toggled(bool)"),
                self.copyCtorCheckBox, QtCore.SLOT("setEnabled(bool)"))
    
        parent.setButtonEnabled(False)
    
        groupBoxLayout = QtGui.QVBoxLayout()
        groupBoxLayout.addWidget(self.qobjectCtorRadioButton)
        groupBoxLayout.addWidget(self.qwidgetCtorRadioButton)
        groupBoxLayout.addWidget(self.defaultCtorRadioButton)
        groupBoxLayout.addWidget(self.copyCtorCheckBox)
        self.groupBox.setLayout(groupBoxLayout)
    
        layout = QtGui.QGridLayout()
        layout.addWidget(self.topLabel, 0, 0, 1, 2)
        layout.setRowMinimumHeight(1, 10)
        layout.addWidget(self.classNameLabel, 2, 0)
        layout.addWidget(self.classNameLineEdit, 2, 1)
        layout.addWidget(self.baseClassLabel, 3, 0)
        layout.addWidget(self.baseClassLineEdit, 3, 1)
        layout.addWidget(self.qobjectMacroCheckBox, 4, 0, 1, 2)
        layout.addWidget(self.groupBox, 5, 0, 1, 2)
        layout.setRowStretch(6, 1)
        self.setLayout(layout)

    def classNameChanged(self):
        wizard = self.parent()
        wizard.setButtonEnabled(not self.classNameLineEdit.text().isEmpty())

        
class SecondPage(QtGui.QWidget):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)

        self.topLabel = QtGui.QLabel(self.tr("<center><b>Code style options</b></center>"))
    
        self.commentCheckBox = QtGui.QCheckBox(self.tr("&Start generated files with a comment"))
        self.commentCheckBox.setChecked(True)
        self.setFocusProxy(self.commentCheckBox)
    
        self.protectCheckBox = QtGui.QCheckBox(self.tr("&Protect header file against "
                                                       "multiple inclusions"))
        self.protectCheckBox.setChecked(True)
    
        self.macroNameLabel = QtGui.QLabel(self.tr("&Macro name:"))
        self.macroNameLineEdit = QtGui.QLineEdit()
        self.macroNameLabel.setBuddy(self.macroNameLineEdit)
    
        self.includeBaseCheckBox = QtGui.QCheckBox(self.tr("&Include base class definition"))
        self.baseIncludeLabel = QtGui.QLabel(self.tr("Base class include:"))
        self.baseIncludeLineEdit = QtGui.QLineEdit()
        self.baseIncludeLabel.setBuddy(self.baseIncludeLineEdit)
    
        className = QtCore.QString(parent.firstPage.classNameLineEdit.text())
        self.macroNameLineEdit.setText(className.toUpper() + "_H")
    
        baseClass = QtCore.QString(parent.firstPage.baseClassLineEdit.text())
        if baseClass.isEmpty():
            self.includeBaseCheckBox.setEnabled(False)
            self.baseIncludeLabel.setEnabled(False)
            self.baseIncludeLineEdit.setEnabled(False)
        else:
            self.includeBaseCheckBox.setChecked(True)
            if QtCore.QRegExp("Q[A-Z].*").exactMatch(baseClass):
                self.baseIncludeLineEdit.setText("<" + baseClass + ">")
            else:
                self.baseIncludeLineEdit.setText("\"" + baseClass.toLower() + ".h\"")

        self.connect(self.protectCheckBox, QtCore.SIGNAL("toggled(bool)"),
                self.macroNameLabel, QtCore.SLOT("setEnabled(bool)"))
        self.connect(self.protectCheckBox, QtCore.SIGNAL("toggled(bool)"),
                self.macroNameLineEdit, QtCore.SLOT("setEnabled(bool)"))
        self.connect(self.includeBaseCheckBox, QtCore.SIGNAL("toggled(bool)"),
                self.baseIncludeLabel, QtCore.SLOT("setEnabled(bool)"))
        self.connect(self.includeBaseCheckBox, QtCore.SIGNAL("toggled(bool)"),
                self.baseIncludeLineEdit, QtCore.SLOT("setEnabled(bool)"))
    
        layout = QtGui.QGridLayout()
        layout.setColumnMinimumWidth(0, 20)
        layout.addWidget(self.topLabel, 0, 0, 1, 3)
        layout.setRowMinimumHeight(1, 10)
        layout.addWidget(self.commentCheckBox, 2, 0, 1, 3)
        layout.addWidget(self.protectCheckBox, 3, 0, 1, 3)
        layout.addWidget(self.macroNameLabel, 4, 1)
        layout.addWidget(self.macroNameLineEdit, 4, 2)
        layout.addWidget(self.includeBaseCheckBox, 5, 0, 1, 3)
        layout.addWidget(self.baseIncludeLabel, 6, 1)
        layout.addWidget(self.baseIncludeLineEdit, 6, 2)
        layout.setRowStretch(7, 1)
        self.setLayout(layout)

        
class ThirdPage(QtGui.QWidget):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        
        self.topLabel = QtGui.QLabel(self.tr("<center><b>Output files</b></center>"))
    
        self.outputDirLabel = QtGui.QLabel(self.tr("&Output directory:"))
        self.outputDirLineEdit = QtGui.QLineEdit()
        self.outputDirLabel.setBuddy(self.outputDirLineEdit)
        self.setFocusProxy(self.outputDirLineEdit)
    
        self.headerLabel = QtGui.QLabel(self.tr("&Header file name:"))
        self.headerLineEdit = QtGui.QLineEdit()
        self.headerLabel.setBuddy(self.headerLineEdit)
    
        self.implementationLabel = QtGui.QLabel(self.tr("&Implementation file name:"))
        self.implementationLineEdit = QtGui.QLineEdit()
        self.implementationLabel.setBuddy(self.implementationLineEdit)
    
        className = QtCore.QString(parent.firstPage.classNameLineEdit.text())
        self.headerLineEdit.setText(className.toLower() + ".h")
        self.implementationLineEdit.setText(className.toLower() + ".cpp")
        self.outputDirLineEdit.setText(QtCore.QDir.convertSeparators(QtCore.QDir.homePath()))
    
        layout = QtGui.QGridLayout()
        layout.addWidget(self.topLabel, 0, 0, 1, 2)
        layout.setRowMinimumHeight(1, 10)
        layout.addWidget(self.outputDirLabel, 2, 0)
        layout.addWidget(self.outputDirLineEdit, 2, 1)
        layout.addWidget(self.headerLabel, 3, 0)
        layout.addWidget(self.headerLineEdit, 3, 1)
        layout.addWidget(self.implementationLabel, 4, 0)
        layout.addWidget(self.implementationLineEdit, 4, 1)
        layout.setRowStretch(5, 1)
        self.setLayout(layout)
        

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    wizard = ClassWizard()
    wizard.show()
    sys.exit(wizard.exec_())
