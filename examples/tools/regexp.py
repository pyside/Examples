#!/usr/bin/env python

"""PySide port of the tools/regexp example from Qt v4.x"""

import sys
from PySide import QtCore, QtGui


class RegExpDialog(QtGui.QDialog):
    MaxCaptures = 6
    
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        
        self.patternComboBox = QtGui.QComboBox()
        self.patternComboBox.setEditable(True)
        self.patternComboBox.setSizePolicy(QtGui.QSizePolicy.Expanding,
                                           QtGui.QSizePolicy.Preferred)
        
        self.patternLabel = QtGui.QLabel(self.tr("&Pattern:"))
        self.patternLabel.setBuddy(self.patternComboBox)
        
        self.escapedPatternLineEdit = QtGui.QLineEdit()
        self.escapedPatternLineEdit.setReadOnly(True)
        palette = self.escapedPatternLineEdit.palette()
        palette.setBrush(QtGui.QPalette.Base, 
                         palette.brush(QtGui.QPalette.Disabled, QtGui.QPalette.Base))
        self.escapedPatternLineEdit.setPalette(palette)
        self.escapedPatternLabel = QtGui.QLabel(self.tr("&Escaped Pattern:"))
        self.escapedPatternLabel.setBuddy(self.escapedPatternLineEdit)
        
        self.textComboBox = QtGui.QComboBox()
        self.textComboBox.setEditable(True)
        self.textComboBox.setSizePolicy(QtGui.QSizePolicy.Expanding,
                                        QtGui.QSizePolicy.Preferred)
        self.textLabel = QtGui.QLabel(self.tr("&Text:"))
        self.textLabel.setBuddy(self.textComboBox)
        
        self.caseSensitiveCheckBox = QtGui.QCheckBox(self.tr("Case &Sensitive"))
        self.caseSensitiveCheckBox.setChecked(True)
        self.minimalCheckBox = QtGui.QCheckBox(self.tr("&Minimal"))
        self.wildcardCheckBox = QtGui.QCheckBox(self.tr("&Wildcard"))
        
        self.indexLabel = QtGui.QLabel(self.tr("Index of Match:"))
        self.indexEdit = QtGui.QLineEdit()
        self.indexEdit.setReadOnly(True)
        
        self.matchedLengthLabel = QtGui.QLabel(self.tr("Matched Length:"))
        self.matchedLengthEdit = QtGui.QLineEdit()
        self.matchedLengthEdit.setReadOnly(True)
        
        self.captureLabels = []
        self.captureEdits = []
        for i in range(self.MaxCaptures):
            self.captureLabels.append(QtGui.QLabel(self.tr("Capture %1:").arg(i)))
            self.captureEdits.append(QtGui.QLineEdit())
            self.captureEdits[i].setReadOnly(True)
        self.captureLabels[0].setText(self.tr("Match:"))
        
        checkBoxLayout = QtGui.QHBoxLayout()
        checkBoxLayout.addWidget(self.caseSensitiveCheckBox)
        checkBoxLayout.addWidget(self.minimalCheckBox)
        checkBoxLayout.addWidget(self.wildcardCheckBox)
        checkBoxLayout.addStretch(1)
        
        mainLayout = QtGui.QGridLayout()
        mainLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        mainLayout.addWidget(self.patternLabel, 0, 0)
        mainLayout.addWidget(self.patternComboBox, 0, 1)
        mainLayout.addWidget(self.escapedPatternLabel, 1, 0)
        mainLayout.addWidget(self.escapedPatternLineEdit, 1, 1)
        mainLayout.addWidget(self.textLabel, 2, 0)
        mainLayout.addWidget(self.textComboBox, 2, 1)
        mainLayout.addLayout(checkBoxLayout, 3, 0, 1, 2)
        mainLayout.addWidget(self.indexLabel, 4, 0)
        mainLayout.addWidget(self.indexEdit, 4, 1)
        mainLayout.addWidget(self.matchedLengthLabel, 5, 0)
        mainLayout.addWidget(self.matchedLengthEdit, 5, 1)
        for i in range(self.MaxCaptures):
            mainLayout.addWidget(self.captureLabels[i], 6 + i, 0)
            mainLayout.addWidget(self.captureEdits[i], 6 + i, 1)
        self.setLayout(mainLayout)
        
        self.connect(self.patternComboBox,
                     QtCore.SIGNAL("editTextChanged(const QString &)"), self.refresh)
        self.connect(self.textComboBox,
                     QtCore.SIGNAL("editTextChanged(const QString &)"), self.refresh)
        self.connect(self.caseSensitiveCheckBox,
                     QtCore.SIGNAL("toggled(bool)"), self.refresh)
        self.connect(self.minimalCheckBox,
                     QtCore.SIGNAL("toggled(bool)"), self.refresh)
        self.connect(self.wildcardCheckBox,
                     QtCore.SIGNAL("toggled(bool)"), self.refresh)

        self.patternComboBox.addItem(self.tr("([A-Za-z_])([A-Za-z_0-9]*)"))
        self.textComboBox.addItem(self.tr("(10 + delta4)* 32"))
        
        self.setWindowTitle(self.tr("RegExp"))
        self.refresh()

    def refresh(self):
        pattern = self.patternComboBox.currentText()
        text = self.textComboBox.currentText()
        escaped = self.patternComboBox.currentText()
        
        escaped = escaped.replace("\\", "\\\\")
        escaped = "\"" + escaped + "\""
        self.escapedPatternLineEdit.setText(escaped)
        
        rx = QtCore.QRegExp(pattern)
        cs = QtCore.Qt.CaseInsensitive
        if self.caseSensitiveCheckBox.isChecked():
            cs = QtCore.Qt.CaseSensitive
        rx.setCaseSensitivity(cs)
        rx.setMinimal(self.minimalCheckBox.isChecked())
        if self.wildcardCheckBox.isChecked():
            syntax = QtCore.QRegExp.Wildcard
        else:
            syntax = QtCore.QRegExp.RegExp
        rx.setPatternSyntax(syntax)
        
        palette = self.patternComboBox.palette()
        if rx.isValid():
            palette.setColor(QtGui.QPalette.Text,
                             self.textComboBox.palette().color(QtGui.QPalette.Text))
        else:
            palette.setColor(QtGui.QPalette.Text, QtCore.Qt.red)
        self.patternComboBox.setPalette(palette)
        
        self.indexEdit.setText(QtCore.QString.number(rx.indexIn(text)))
        self.matchedLengthEdit.setText(
            QtCore.QString.number(rx.matchedLength()))

        for i in range(self.MaxCaptures):
            self.captureLabels[i].setEnabled(i <= rx.numCaptures())
            self.captureEdits[i].setEnabled(i <= rx.numCaptures())
            self.captureEdits[i].setText(rx.cap(i))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    dialog = RegExpDialog()
    sys.exit(dialog.exec_())
