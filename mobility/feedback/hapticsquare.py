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

from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtDeclarative import *
from QtMobility.Feedback import *

class EffectPlayer(QObject):

    def __init__(self, parent=None):
        QObject.__init__(self, parent)

        self.m_rumble = QFeedbackHapticsEffect()
        self.m_rumble.setAttackIntensity(0.1)
        self.m_rumble.setAttackTime(250)
        self.m_rumble.setIntensity(1)
        self.m_rumble.setDuration(1000)
        self.m_rumble.setFadeTime(250)
        self.m_rumble.setFadeIntensity(0.1)

        self.m_ocean = QFeedbackHapticsEffect()
        self.m_ocean.setAttackIntensity(0.1)
        self.m_ocean.setAttackTime(450)
        self.m_ocean.setIntensity(0.8)
        self.m_ocean.setDuration(6000)
        self.m_ocean.setFadeTime(900)
        self.m_ocean.setFadeIntensity(0.05)
        self.m_ocean.setPeriod(1500)

    @Slot()
    def playRumble(self):
        print "Starting rumble effect"
        self.m_rumble.start()

    @Slot()
    def playOcean(self):
       if self.m_ocean.state() == QFeedbackEffect.Stopped:
         self.m_ocean.start()
         print "Ocean start"
       else:
         self.m_ocean.stop()
         print "Ocean stop"

    @Slot()
    def playButtonClick(self):
        QFeedbackEffect.playThemeEffect(QFeedbackEffect.ThemeBasicButton)
        print "Play button click"

    @Slot()
    def playNegativeEffect(self):
        QFeedbackEffect.playThemeEffect(QFeedbackEffect.ThemeNegativeTacticon)
        print "Play negative button click"


def main():
    app = QApplication([])
    view = QDeclarativeView()
    player = EffectPlayer()
    context = view.rootContext()
    context.setContextProperty("effectPlayer", player)

    url = QUrl('main.qml')
    view.setSource(url)
    view.showFullScreen()

    app.exec_()


if __name__ == '__main__':
    main()



