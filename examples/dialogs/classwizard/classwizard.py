#!/usr/bin/env python

from PyQt4 import QtCore, QtGui

import classwizard_rc


class ClassWizard(QtGui.QWizard):
    def __init__(self, parent=None):
        super(ClassWizard, self).__init__(parent)

        self.addPage(IntroPage())
        self.addPage(ClassInfoPage())
        self.addPage(CodeStylePage())
        self.addPage(OutputFilesPage())
        self.addPage(ConclusionPage())

        self.setPixmap(QtGui.QWizard.BannerPixmap,
                QtGui.QPixmap(":/images/banner.png"))
        self.setPixmap(QtGui.QWizard.BackgroundPixmap,
                QtGui.QPixmap(":/images/background.png"))

        self.setWindowTitle(self.tr("Class Wizard"))

    def accept(self):
        className = self.field("className").toByteArray()
        baseClass = self.field("baseClass").toByteArray()
        macroName = self.field("macroName").toByteArray()
        baseInclude = self.field("baseInclude").toByteArray()

        outputDir = self.field("outputDir").toString()
        header = self.field("header").toString()
        implementation = self.field("implementation").toString()

        block = QtCore.QByteArray()

        if self.field("comment").toBool():
            block += "/*\n"
            block += "    " + header.toAscii() + "\n"
            block += "*/\n"
            block += "\n"

        if self.field("protect").toBool():
            block += "#ifndef " + macroName + "\n"
            block += "#define " + macroName + "\n"
            block += "\n"

        if self.field("includeBase").toBool():
            block += "#include " + baseInclude + "\n"
            block += "\n"

        block += "class " + className
        if not baseClass.isEmpty():
            block += " : public " + baseClass

        block += "\n"
        block += "{\n"

        if self.field("qobjectMacro").toBool():
            block += "    Q_OBJECT\n"
            block += "\n"

        block += "public:\n"

        if self.field("qobjectCtor").toBool():
            block += "    " + className + "(QObject *parent = 0);\n"
        elif self.field("qwidgetCtor").toBool():
            block += "    " + className + "(QWidget *parent = 0);\n"
        elif self.field("defaultCtor").toBool():
            block += "    " + className + "();\n"

            if self.field("copyCtor").toBool():
                block += "    " + className + "(const " + className + " &other);\n"
                block += "\n"
                block += "    " + className + " &operator=" + "(const " + className + " &other);\n"

        block += "};\n"

        if self.field("protect").toBool():
            block += "\n"
            block += "#endif\n"

        headerFile = QtCore.QFile(outputDir + "/" + header)

        if not headerFile.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(None, self.tr("Class Wizard"),
                    self.tr("Cannot write file %1:\n%2").arg(headerFile.fileName()).arg(headerFile.errorString()));
            return

        headerFile.write(block)

        block.clear()

        if self.field("comment").toBool():
            block += "/*\n"
            block += "    " + implementation.toAscii() + "\n"
            block += "*/\n"
            block += "\n"

        block += "#include \"" + header.toAscii() + "\"\n"
        block += "\n"

        if self.field("qobjectCtor").toBool():
            block += className + "::" + className + "(QObject *parent)\n"
            block += "    : " + baseClass + "(parent)\n"
            block += "{\n"
            block += "}\n"
        elif self.field("qwidgetCtor").toBool():
            block += className + "::" + className + "(QWidget *parent)\n"
            block += "    : " + baseClass + "(parent)\n"
            block += "{\n"
            block += "}\n"
        elif self.field("defaultCtor").toBool():
            block += className + "::" + className + "()\n"
            block += "{\n"
            block += "    // missing code\n"
            block += "}\n"

            if self.field("copyCtor").toBool():
                block += "\n"
                block += className + "::" + className + "(const " + className + " &other)\n"
                block += "{\n"
                block += "    *this = other;\n"
                block += "}\n"
                block += "\n"
                block += className + " &" + className + "::operator=(const " + className + " &other)\n"
                block += "{\n"

                if not baseClass.isEmpty():
                    block += "    " + baseClass + "::operator=(other);\n"

                block += "    // missing code\n"
                block += "    return *this;\n"
                block += "}\n"

        implementationFile = QtCore.QFile(outputDir + "/" + implementation)

        if not implementationFile.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(None, self.tr("Class Wizard"),
                    self.tr("Cannot write file %1:\n%2").arg(implementationFile.fileName()).arg(implementationFile.errorString()));
            return

        implementationFile.write(block)

        super(ClassWizard, self).accept()


class IntroPage(QtGui.QWizardPage):
    def __init__(self, parent=None):
        super(IntroPage, self).__init__(parent)

        self.setTitle(self.tr("Introduction"))
        self.setPixmap(QtGui.QWizard.WatermarkPixmap,
                QtGui.QPixmap(":/images/watermark1.png"))

        label = QtGui.QLabel(self.tr("This wizard will generate a skeleton "
                                     "C++ class definition, including a few "
                                     "functions. You simply need to specify "
                                     "the class name and set a few options to "
                                     "produce a header file and an "
                                     "implementation file for your new C++ "
                                     "class."))
        label.setWordWrap(True)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)


class ClassInfoPage(QtGui.QWizardPage):
    def __init__(self, parent=None):
        super(ClassInfoPage, self).__init__(parent)

        self.setTitle(self.tr("Class Information"))
        self.setSubTitle(self.tr("Specify basic information about the class "
                                 "for which you want to generate skeleton "
                                 "source code files."))
        self.setPixmap(QtGui.QWizard.LogoPixmap,
                QtGui.QPixmap(":/images/logo1.png"))

        classNameLabel = QtGui.QLabel(self.tr("&Class name:"))
        classNameLineEdit = QtGui.QLineEdit()
        classNameLabel.setBuddy(classNameLineEdit)

        baseClassLabel = QtGui.QLabel(self.tr("B&ase class:"))
        baseClassLineEdit = QtGui.QLineEdit()
        baseClassLabel.setBuddy(baseClassLineEdit)

        qobjectMacroCheckBox = QtGui.QCheckBox(self.tr("Generate Q_OBJECT &macro"))

        groupBox = QtGui.QGroupBox(self.tr("C&onstructor"))

        qobjectCtorRadioButton = QtGui.QRadioButton(self.tr("&QObject-style constructor"))
        qwidgetCtorRadioButton = QtGui.QRadioButton(self.tr("Q&Widget-style constructor"))
        defaultCtorRadioButton = QtGui.QRadioButton(self.tr("&Default constructor"))
        copyCtorCheckBox = QtGui.QCheckBox(self.tr("&Generate copy constructor and operator="))

        defaultCtorRadioButton.setChecked(True)

        defaultCtorRadioButton.toggled.connect(copyCtorCheckBox.setEnabled)

        self.registerField("className*", classNameLineEdit)
        self.registerField("baseClass", baseClassLineEdit)
        self.registerField("qobjectMacro", qobjectMacroCheckBox)
        self.registerField("qobjectCtor", qobjectCtorRadioButton)
        self.registerField("qwidgetCtor", qwidgetCtorRadioButton)
        self.registerField("defaultCtor", defaultCtorRadioButton)
        self.registerField("copyCtor", copyCtorCheckBox)

        groupBoxLayout = QtGui.QVBoxLayout()
        groupBoxLayout.addWidget(qobjectCtorRadioButton)
        groupBoxLayout.addWidget(qwidgetCtorRadioButton)
        groupBoxLayout.addWidget(defaultCtorRadioButton)
        groupBoxLayout.addWidget(copyCtorCheckBox)
        groupBox.setLayout(groupBoxLayout)

        layout = QtGui.QGridLayout()
        layout.addWidget(classNameLabel, 0, 0)
        layout.addWidget(classNameLineEdit, 0, 1)
        layout.addWidget(baseClassLabel, 1, 0)
        layout.addWidget(baseClassLineEdit, 1, 1)
        layout.addWidget(qobjectMacroCheckBox, 2, 0, 1, 2)
        layout.addWidget(groupBox, 3, 0, 1, 2)
        self.setLayout(layout)


class CodeStylePage(QtGui.QWizardPage):
    def __init__(self, parent=None):
        super(CodeStylePage, self).__init__(parent)

        self.setTitle(self.tr("Code Style Options"))
        self.setSubTitle(self.tr("Choose the formatting of the generated code."))
        self.setPixmap(QtGui.QWizard.LogoPixmap,
                QtGui.QPixmap(":/images/logo2.png"))

        commentCheckBox = QtGui.QCheckBox(self.tr("&Start generated files "
                                                  "with a comment"))
        commentCheckBox.setChecked(True)

        protectCheckBox = QtGui.QCheckBox(self.tr("&Protect header file "
                                                  "against multiple "
                                                  "inclusions"))
        protectCheckBox.setChecked(True)

        macroNameLabel = QtGui.QLabel(self.tr("&Macro name:"))
        self.macroNameLineEdit = QtGui.QLineEdit()
        macroNameLabel.setBuddy(self.macroNameLineEdit)

        self.includeBaseCheckBox = QtGui.QCheckBox(self.tr("&Include base "
                                                           "class definition"))
        self.baseIncludeLabel = QtGui.QLabel(self.tr("Base class include:"))
        self.baseIncludeLineEdit = QtGui.QLineEdit()
        self.baseIncludeLabel.setBuddy(self.baseIncludeLineEdit)

        protectCheckBox.toggled.connect(macroNameLabel.setEnabled)
        protectCheckBox.toggled.connect(self.macroNameLineEdit.setEnabled)
        self.includeBaseCheckBox.toggled.connect(self.baseIncludeLabel.setEnabled)
        self.includeBaseCheckBox.toggled.connect(self.baseIncludeLineEdit.setEnabled)

        self.registerField("comment", commentCheckBox)
        self.registerField("protect", protectCheckBox)
        self.registerField("macroName", self.macroNameLineEdit)
        self.registerField("includeBase", self.includeBaseCheckBox)
        self.registerField("baseInclude", self.baseIncludeLineEdit)

        layout = QtGui.QGridLayout()
        layout.setColumnMinimumWidth(0, 20)
        layout.addWidget(commentCheckBox, 0, 0, 1, 3)
        layout.addWidget(protectCheckBox, 1, 0, 1, 3)
        layout.addWidget(macroNameLabel, 2, 1)
        layout.addWidget(self.macroNameLineEdit, 2, 2)
        layout.addWidget(self.includeBaseCheckBox, 3, 0, 1, 3)
        layout.addWidget(self.baseIncludeLabel, 4, 1)
        layout.addWidget(self.baseIncludeLineEdit, 4, 2)
        self.setLayout(layout)

    def initializePage(self):
        className = self.field("className").toString()
        self.macroNameLineEdit.setText(className.toUpper() + "_H")

        baseClass = self.field("baseClass").toString()

        self.includeBaseCheckBox.setChecked(not baseClass.isEmpty())
        self.includeBaseCheckBox.setEnabled(not baseClass.isEmpty())
        self.baseIncludeLabel.setEnabled(not baseClass.isEmpty())
        self.baseIncludeLineEdit.setEnabled(not baseClass.isEmpty())

        if baseClass.isEmpty():
            self.baseIncludeLineEdit.clear()
        elif QtCore.QRegExp("Q[A-Z].*").exactMatch(baseClass):
            self.baseIncludeLineEdit.setText("<" + baseClass + ">")
        else:
            self.baseIncludeLineEdit.setText("\"" + baseClass.toLower() + ".h\"")


class OutputFilesPage(QtGui.QWizardPage):
    def __init__(self, parent=None):
        super(OutputFilesPage, self).__init__(parent)

        self.setTitle(self.tr("Output Files"))
        self.setSubTitle(self.tr("Specify where you want the wizard to put "
                                 "the generated skeleton code."))
        self.setPixmap(QtGui.QWizard.LogoPixmap,
                QtGui.QPixmap(":/images/logo3.png"))

        outputDirLabel = QtGui.QLabel(self.tr("&Output directory:"))
        self.outputDirLineEdit = QtGui.QLineEdit()
        outputDirLabel.setBuddy(self.outputDirLineEdit)

        headerLabel = QtGui.QLabel(self.tr("&Header file name:"))
        self.headerLineEdit = QtGui.QLineEdit()
        headerLabel.setBuddy(self.headerLineEdit)

        implementationLabel = QtGui.QLabel(self.tr("&Implementation file name:"))
        self.implementationLineEdit = QtGui.QLineEdit()
        implementationLabel.setBuddy(self.implementationLineEdit)

        self.registerField("outputDir*", self.outputDirLineEdit)
        self.registerField("header*", self.headerLineEdit)
        self.registerField("implementation*", self.implementationLineEdit)

        layout = QtGui.QGridLayout()
        layout.addWidget(outputDirLabel, 0, 0)
        layout.addWidget(self.outputDirLineEdit, 0, 1)
        layout.addWidget(headerLabel, 1, 0)
        layout.addWidget(self.headerLineEdit, 1, 1)
        layout.addWidget(implementationLabel, 2, 0)
        layout.addWidget(self.implementationLineEdit, 2, 1)
        self.setLayout(layout)

    def initializePage(self):
        className = self.field("className").toString()
        self.headerLineEdit.setText(className.toLower() + ".h")
        self.implementationLineEdit.setText(className.toLower() + ".cpp")
        self.outputDirLineEdit.setText(QtCore.QDir.convertSeparators(QtCore.QDir.tempPath()))


class ConclusionPage(QtGui.QWizardPage):
    def __init__(self, parent=None):
        super(ConclusionPage, self).__init__(parent)

        self.setTitle(self.tr("Conclusion"))
        self.setPixmap(QtGui.QWizard.WatermarkPixmap,
                QtGui.QPixmap(":/images/watermark2.png"))

        self.label = QtGui.QLabel()
        self.label.setWordWrap(True)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

    def initializePage(self):
        finishText = self.wizard().buttonText(QtGui.QWizard.FinishButton)
        finishText.remove('&')
        self.label.setText(self.tr("Click %1 to generate the class skeleton.").arg(finishText));


if __name__ == "__main__":

    import sys

    app = QtGui.QApplication(sys.argv)
    wizard = ClassWizard()
    wizard.show()
    sys.exit(app.exec_())
