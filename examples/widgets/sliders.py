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

import sys
from PySide import QtCore, QtGui


class SlidersGroup(QtGui.QGroupBox):
    def __init__(self, orientation, title, parent=None):
        QtGui.QGroupBox.__init__(self, title, parent)

        self.slider = QtGui.QSlider(orientation)
        self.slider.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.slider.setTickPosition(QtGui.QSlider.TicksBothSides)
        self.slider.setTickInterval(10)
        self.slider.setSingleStep(1)
    
        self.scrollBar = QtGui.QScrollBar(orientation)
        self.scrollBar.setFocusPolicy(QtCore.Qt.StrongFocus)
    
        self.dial = QtGui.QDial()
        self.dial.setFocusPolicy(QtCore.Qt.StrongFocus)
    
        self.connect(self.slider, QtCore.SIGNAL("valueChanged(int)"),
                     self.scrollBar, QtCore.SLOT("setValue(int)"))
        self.connect(self.scrollBar, QtCore.SIGNAL("valueChanged(int)"),
                     self.dial, QtCore.SLOT("setValue(int)"))
        self.connect(self.dial, QtCore.SIGNAL("valueChanged(int)"),
                     self.slider, QtCore.SLOT("setValue(int)"))
        self.connect(self.dial, QtCore.SIGNAL("valueChanged(int)"),
                     self, QtCore.SIGNAL("valueChanged(int)"))
    
        if orientation == QtCore.Qt.Horizontal:
            direction = QtGui.QBoxLayout.TopToBottom
        else:
            direction = QtGui.QBoxLayout.LeftToRight
    
        slidersLayout = QtGui.QBoxLayout(direction)
        slidersLayout.addWidget(self.slider)
        slidersLayout.addWidget(self.scrollBar)
        slidersLayout.addWidget(self.dial)
        self.setLayout(slidersLayout)    
    
    def setValue(self, value):    
        self.slider.setValue(value)    
    
    def setMinimum(self, value):    
        self.slider.setMinimum(value)
        self.scrollBar.setMinimum(value)
        self.dial.setMinimum(value)    
    
    def setMaximum(self, value):    
        self.slider.setMaximum(value)
        self.scrollBar.setMaximum(value)
        self.dial.setMaximum(value)    
    
    def invertAppearance(self, invert):
        self.slider.setInvertedAppearance(invert)
        self.scrollBar.setInvertedAppearance(invert)
        self.dial.setInvertedAppearance(invert)    
    
    def invertKeyBindings(self, invert):
        self.slider.setInvertedControls(invert)
        self.scrollBar.setInvertedControls(invert)
        self.dial.setInvertedControls(invert)


class Sliders(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        self.horizontalSliders = SlidersGroup(QtCore.Qt.Horizontal, QtCore.QString(self.tr("Horizontal")))
        self.verticalSliders = SlidersGroup(QtCore.Qt.Vertical, QtCore.QString(self.tr("Vertical")))

        self.stackedWidget = QtGui.QStackedWidget()
        self.stackedWidget.addWidget(self.horizontalSliders)
        self.stackedWidget.addWidget(self.verticalSliders)
    
        self.createControls(self.tr("Controls"))
    
        self.connect(self.horizontalSliders, QtCore.SIGNAL("valueChanged(int)"),
                     self.verticalSliders.setValue)
        self.connect(self.verticalSliders, QtCore.SIGNAL("valueChanged(int)"),
                     self.valueSpinBox, QtCore.SLOT("setValue(int)"))
        self.connect(self.valueSpinBox, QtCore.SIGNAL("valueChanged(int)"),
                     self.horizontalSliders.setValue)
    
        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.controlsGroup)
        layout.addWidget(self.stackedWidget)
        self.setLayout(layout)
    
        self.minimumSpinBox.setValue(0)
        self.maximumSpinBox.setValue(20)
        self.valueSpinBox.setValue(5)
    
        self.setWindowTitle(self.tr("Sliders"))
    
    def createControls(self, title):
        self.controlsGroup = QtGui.QGroupBox(title)
    
        minimumLabel = QtGui.QLabel(self.tr("Minimum value:"))
        maximumLabel = QtGui.QLabel(self.tr("Maximum value:"))
        valueLabel = QtGui.QLabel(self.tr("Current value:"))
    
        invertedAppearance = QtGui.QCheckBox(self.tr("Inverted appearance"))
        invertedKeyBindings = QtGui.QCheckBox(self.tr("Inverted key bindings"))
    
        self.minimumSpinBox = QtGui.QSpinBox()
        self.minimumSpinBox.setRange(-100, 100)
        self.minimumSpinBox.setSingleStep(1)
    
        self.maximumSpinBox = QtGui.QSpinBox()
        self.maximumSpinBox.setRange(-100, 100)
        self.maximumSpinBox.setSingleStep(1)
    
        self.valueSpinBox = QtGui.QSpinBox()
        self.valueSpinBox.setRange(-100, 100)
        self.valueSpinBox.setSingleStep(1)
    
        orientationCombo = QtGui.QComboBox()
        orientationCombo.addItem(self.tr("Horizontal slider-like widgets"))
        orientationCombo.addItem(self.tr("Vertical slider-like widgets"))
    
        self.connect(orientationCombo, QtCore.SIGNAL("activated(int)"),
                     self.stackedWidget, QtCore.SLOT("setCurrentIndex(int)"))
        self.connect(self.minimumSpinBox, QtCore.SIGNAL("valueChanged(int)"),
                     self.horizontalSliders.setMinimum)
        self.connect(self.minimumSpinBox, QtCore.SIGNAL("valueChanged(int)"),
                     self.verticalSliders.setMinimum)
        self.connect(self.maximumSpinBox, QtCore.SIGNAL("valueChanged(int)"),
                     self.horizontalSliders.setMaximum)
        self.connect(self.maximumSpinBox, QtCore.SIGNAL("valueChanged(int)"),
                     self.verticalSliders.setMaximum)
        self.connect(invertedAppearance, QtCore.SIGNAL("toggled(bool)"),
                     self.horizontalSliders.invertAppearance)
        self.connect(invertedAppearance, QtCore.SIGNAL("toggled(bool)"),
                     self.verticalSliders.invertAppearance)
        self.connect(invertedKeyBindings, QtCore.SIGNAL("toggled(bool)"),
                     self.horizontalSliders.invertKeyBindings)
        self.connect(invertedKeyBindings, QtCore.SIGNAL("toggled(bool)"),
                     self.verticalSliders.invertKeyBindings)

        controlsLayout = QtGui.QGridLayout()
        controlsLayout.addWidget(minimumLabel, 0, 0)
        controlsLayout.addWidget(maximumLabel, 1, 0)
        controlsLayout.addWidget(valueLabel, 2, 0)
        controlsLayout.addWidget(self.minimumSpinBox, 0, 1)
        controlsLayout.addWidget(self.maximumSpinBox, 1, 1)
        controlsLayout.addWidget(self.valueSpinBox, 2, 1)
        controlsLayout.addWidget(invertedAppearance, 0, 2)
        controlsLayout.addWidget(invertedKeyBindings, 1, 2)
        controlsLayout.addWidget(orientationCombo, 3, 0, 1, 3)
        self.controlsGroup.setLayout(controlsLayout)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    sliders = Sliders()
    sliders.show()
    sys.exit(app.exec_())
