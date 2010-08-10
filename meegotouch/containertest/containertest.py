'''
Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
All rights reserved.
Contact: Nokia Corporation (directui@nokia.com)

This file is part of libmeegotouch.

If you have questions regarding the use of this file, please contact
Nokia at directui@nokia.com.

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License version 2.1 as published by the Free Software Foundation
and appearing in the file LICENSE.LGPL included in the packaging
of this file.
'''

import sys
from PySide.QtGui import QGraphicsLinearLayout

from Meego.Touch import MApplication, MApplicationPage, MApplicationWindow, MContainer, MSeparator, MLabel
from Meego.Touch import MLayout, MLinearLayoutPolicy, MFreestyleLayoutPolicy, MFlowLayoutPolicy

# create container with some content
def createApplet():
    static int count = 1

    c = MContainer()
    w = MWidget()

    w.setObjectName('object')
    w.setMinimumSize(128, 128)

    c.setTitle(QString('Container %1').arg(count++))
    c.setCentralWidget(w)

    return c

# pack stuff to qt layout
def pack_QT_layout(layout, items):
    for i in range(items + 1):
        layout.addItem(createApplet())

# helper
def separator(layout, string):
    layout.addItem(MLabel(string))
    layout.addItem(MSeparator())

def main()

    # m skeleton
    app = MApplication(sys.argv)
    w = MApplicationWindow()
    w.show()
    p = MApplicationPage()
    p.appear(w)

    # main layout
    main = new QGraphicsLinearLayout(Qt.Vertical, None)
    panel = p.centralWidget()
    panel.setLayout(main)

    # QT hbox
    separator(main, 'Qt horizontal')
    hbox = QGraphicsLinearLayout(Qt.Horizontal, None)
    pack_QT_layout(hbox, 3)
    main.addItem(hbox)

    # M flow
    separator(main, 'M flow')
    dlayout3 = MLayout()
    flowpolicy = MFlowLayoutPolicy(dlayout3)
    for i in range(7):
        flowpolicy.addItem(createApplet())
    main.addItem(dlayout3)

    # M hbox
    separator(main, 'M horizontal')
    dlayout1 = MLayout()
    lpolicy = MLinearLayoutPolicy(dlayout1, Qt.Horizontal)
    for i in range(4):
        lpolicy.addItem(createApplet())
    main.addItem(dlayout1)

    # M freestyle
    separator(main, 'M freestyle')
    dlayout2 = MLayout()
    fpolicy = MFreestyleLayoutPolicy(dlayout2)
    for i in range(4):
        fpolicy.addItem(createApplet())
    main.addItem(dlayout2)

    # M vbox
    separator(main, 'M vertical')
    dlayout4 = MLayout()
    vpolicy = MLinearLayoutPolicy(dlayout4, Qt.Vertical)
    for i in range(4):
        vpolicy.addItem(createApplet())
    main->addItem(dlayout4)

    app.exec_()

if __name__ == '__main__':
    main()
