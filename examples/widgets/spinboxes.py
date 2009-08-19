#!/usr/bin/env python

#############################################################################
##
## Copyright (C) 2004-2005 Trolltech AS. All rights reserved.
##
## This file is part of the example classes of the Qt Toolkit.
##
## This file may be used under the terms of the GNU General Public
## License version 2.0 as published by the Free Software Foundation
## and appearing in the file LICENSE.GPL included in the packaging of
## this file.  Please review the following information to ensure GNU
## General Public Licensing requirements will be met:
## http://www.trolltech.com/products/qt/opensource.html
##
## If you are unsure which license is appropriate for your use, please
## review the following information:
## http://www.trolltech.com/products/qt/licensing.html or contact the
## sales department at sales@trolltech.com.
##
## This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
## WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
##
#############################################################################

from PyQt4 import QtCore, QtGui


class Window(QtGui.QWidget):
    def __init__(self):
        super(Window, self).__init__()

        self.createSpinBoxes()
        self.createDateTimeEdits()
        self.createDoubleSpinBoxes()

        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.spinBoxesGroup)
        layout.addWidget(self.editsGroup)
        layout.addWidget(self.doubleSpinBoxesGroup)
        self.setLayout(layout)

        self.setWindowTitle(self.tr("Spin Boxes"))

    def createSpinBoxes(self):
        self.spinBoxesGroup = QtGui.QGroupBox(self.tr("Spinboxes"))

        integerLabel = QtGui.QLabel(self.tr("Enter a value between %1 and %2:").arg(-20).arg(20))
        integerSpinBox = QtGui.QSpinBox()
        integerSpinBox.setRange(-20, 20)
        integerSpinBox.setSingleStep(1)
        integerSpinBox.setValue(0)

        zoomLabel = QtGui.QLabel(self.tr("Enter a zoom value between %1 and %2:").arg(0).arg(1000))
        zoomSpinBox = QtGui.QSpinBox()
        zoomSpinBox.setRange(0, 1000)
        zoomSpinBox.setSingleStep(10)
        zoomSpinBox.setSuffix("%")
        zoomSpinBox.setSpecialValueText(self.tr("Automatic"))
        zoomSpinBox.setValue(100)

        priceLabel = QtGui.QLabel(self.tr("Enter a price between %1 and %2:").arg(0).arg(999))
        priceSpinBox = QtGui.QSpinBox()
        priceSpinBox.setRange(0, 999)
        priceSpinBox.setSingleStep(1)
        priceSpinBox.setPrefix("$")
        priceSpinBox.setValue(99)

        spinBoxLayout = QtGui.QVBoxLayout()
        spinBoxLayout.addWidget(integerLabel)
        spinBoxLayout.addWidget(integerSpinBox)
        spinBoxLayout.addWidget(zoomLabel)
        spinBoxLayout.addWidget(zoomSpinBox)
        spinBoxLayout.addWidget(priceLabel)
        spinBoxLayout.addWidget(priceSpinBox)
        self.spinBoxesGroup.setLayout(spinBoxLayout)

    def createDateTimeEdits(self):
        self.editsGroup = QtGui.QGroupBox(self.tr("Date and time spin boxes"))

        dateLabel = QtGui.QLabel()
        dateEdit = QtGui.QDateEdit(QtCore.QDate.currentDate())
        dateEdit.setDateRange(QtCore.QDate(2005, 1, 1), QtCore.QDate(2010, 12, 31))
        dateLabel.setText(self.tr("Appointment date (between %0 and %1):")
                    .arg(dateEdit.minimumDate().toString(QtCore.Qt.ISODate))
                    .arg(dateEdit.maximumDate().toString(QtCore.Qt.ISODate)))

        timeLabel = QtGui.QLabel()
        timeEdit = QtGui.QTimeEdit(QtCore.QTime.currentTime())
        timeEdit.setTimeRange(QtCore.QTime(9, 0, 0, 0), QtCore.QTime(16, 30, 0, 0))
        timeLabel.setText(self.tr("Appointment time (between %0 and %1):")
                    .arg(timeEdit.minimumTime().toString(QtCore.Qt.ISODate))
                    .arg(timeEdit.maximumTime().toString(QtCore.Qt.ISODate)))

        self.meetingLabel = QtGui.QLabel()
        self.meetingEdit = QtGui.QDateTimeEdit(QtCore.QDateTime.currentDateTime())

        formatLabel = QtGui.QLabel(self.tr("Format string for the meeting date and time:"))

        formatComboBox = QtGui.QComboBox()
        formatComboBox.addItem("yyyy-MM-dd hh:mm:ss (zzz 'ms')")
        formatComboBox.addItem("hh:mm:ss MM/dd/yyyy")
        formatComboBox.addItem("hh:mm:ss dd/MM/yyyy")
        formatComboBox.addItem("hh:mm:ss")
        formatComboBox.addItem("hh:mm ap")

        formatComboBox.activated[str].connect(self.setFormatString)

        self.setFormatString(formatComboBox.currentText())

        editsLayout = QtGui.QVBoxLayout()
        editsLayout.addWidget(dateLabel)
        editsLayout.addWidget(dateEdit)
        editsLayout.addWidget(timeLabel)
        editsLayout.addWidget(timeEdit)
        editsLayout.addWidget(self.meetingLabel)
        editsLayout.addWidget(self.meetingEdit)
        editsLayout.addWidget(formatLabel)
        editsLayout.addWidget(formatComboBox)
        self.editsGroup.setLayout(editsLayout)

    def setFormatString(self, formatString):
        self.meetingEdit.setDisplayFormat(formatString)

        if self.meetingEdit.displayedSections() & QtGui.QDateTimeEdit.DateSections_Mask:
            self.meetingEdit.setDateRange(QtCore.QDate(2004, 11, 1), QtCore.QDate(2005, 11, 30))
            self.meetingLabel.setText(self.tr("Meeting date (between %0 and %1):")
                    .arg(self.meetingEdit.minimumDate().toString(QtCore.Qt.ISODate))
                    .arg(self.meetingEdit.maximumDate().toString(QtCore.Qt.ISODate)))
        else:
            self.meetingEdit.setTimeRange(QtCore.QTime(0, 7, 20, 0), QtCore.QTime(21, 0, 0, 0))
            self.meetingLabel.setText(self.tr("Meeting time (between %0 and %1):")
                    .arg(self.meetingEdit.minimumTime().toString(QtCore.Qt.ISODate))
                    .arg(self.meetingEdit.maximumTime().toString(QtCore.Qt.ISODate)))

    def createDoubleSpinBoxes(self):
        self.doubleSpinBoxesGroup = QtGui.QGroupBox(self.tr("Double precision spinboxes"))

        precisionLabel = QtGui.QLabel(self.tr("Number of decimal places to show:"))
        precisionSpinBox = QtGui.QSpinBox()
        precisionSpinBox.setRange(0, 100)
        precisionSpinBox.setValue(2)

        doubleLabel = QtGui.QLabel(self.tr("Enter a value between %1 and %2:").arg(-20).arg(20))
        self.doubleSpinBox = QtGui.QDoubleSpinBox()
        self.doubleSpinBox.setRange(-20.0, 20.0)
        self.doubleSpinBox.setSingleStep(1.0)
        self.doubleSpinBox.setValue(0.0)

        scaleLabel = QtGui.QLabel(self.tr("Enter a scale factor between %1 and %2:").arg(0).arg(1000.0))
        self.scaleSpinBox = QtGui.QDoubleSpinBox()
        self.scaleSpinBox.setRange(0.0, 1000.0)
        self.scaleSpinBox.setSingleStep(10.0)
        self.scaleSpinBox.setSuffix("%")
        self.scaleSpinBox.setSpecialValueText(self.tr("No scaling"))
        self.scaleSpinBox.setValue(100.0)

        priceLabel = QtGui.QLabel(self.tr("Enter a price between %1 and %2:").arg(0).arg(1000))
        self.priceSpinBox = QtGui.QDoubleSpinBox()
        self.priceSpinBox.setRange(0.0, 1000.0)
        self.priceSpinBox.setSingleStep(1.0)
        self.priceSpinBox.setPrefix("$")
        self.priceSpinBox.setValue(99.99)

        precisionSpinBox.valueChanged.connect(self.changePrecision)

        spinBoxLayout = QtGui.QVBoxLayout()
        spinBoxLayout.addWidget(precisionLabel)
        spinBoxLayout.addWidget(precisionSpinBox)
        spinBoxLayout.addWidget(doubleLabel)
        spinBoxLayout.addWidget(self.doubleSpinBox)
        spinBoxLayout.addWidget(scaleLabel)
        spinBoxLayout.addWidget(self.scaleSpinBox)
        spinBoxLayout.addWidget(priceLabel)
        spinBoxLayout.addWidget(self.priceSpinBox)
        self.doubleSpinBoxesGroup.setLayout(spinBoxLayout)

    def changePrecision(self, decimals):
        self.doubleSpinBox.setDecimals(decimals)
        self.scaleSpinBox.setDecimals(decimals)
        self.priceSpinBox.setDecimals(decimals)


if __name__ == "__main__":

    import sys

    app = QtGui.QApplication(sys.argv)    
    window = Window()
    window.show()    
    sys.exit(app.exec_())
