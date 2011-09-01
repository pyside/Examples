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

from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtDeclarative import *
from QtMobility.MultimediaKit import *

class Player(QObject):

    def __init__(self, filename, parent=None):
        QObject.__init__(self, parent)

        self.source = QUrl.fromLocalFile(os.path.abspath(filename))
        self.player = QMediaPlayer()
        self.player.setMedia(self.source)

    @Slot()
    def play(self):
        self.player.play()

def main():
    app = QApplication([])
    view = QDeclarativeView()
    player = Player(sys.argv[1])
    context = view.rootContext()
    context.setContextProperty("player", player)

    url = QUrl('main.qml')
    view.setSource(url)
    view.showFullScreen()

    app.exec_()


if __name__ == '__main__':
    main()



