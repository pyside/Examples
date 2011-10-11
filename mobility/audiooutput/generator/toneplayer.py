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

from PySide.QtCore import QObject, QUrl, QTimer, QByteArray, Slot, Property, Signal
from PySide.QtGui import QApplication
from PySide.QtDeclarative import QDeclarativeView
from QtMobility.MultimediaKit import QAudioFormat, QAudioDeviceInfo, QAudioOutput, QAudio

from generator import Generator

PUSH_MODE_LABEL = 'Enable push mode'
PULL_MODE_LABEL = 'Enable pull mode'
SUSPEND_LABEL = 'Suspend playback'
RESUME_LABEL = 'Resume playback'

BUFFER_SIZE = 32768
DURATION_SECONDS = 1
TONE_FREQUENCY_HZ = 600
DATA_FREQUENCY_HZ = 44100


class TonePlayer(QObject):

    changed = Signal()

    def getStateLabel(self):
        print "Getting"
        return self._label

    def setStateLabel(self, value):
        print "Setting", value
        self._label = value
        self.changed.emit()

    stateLabel = Property(str, getStateLabel, setStateLabel, notify=changed)

    def __init__(self, devices=None, filename=None, parent=None):
        QObject.__init__(self, parent)

        self.pullTimer = QTimer(self)
        self.buf = QByteArray()
        self.devices = devices
        self.device = QAudioDeviceInfo.defaultOutputDevice()
        self.generator = None
        self.audioOutput = None
        self.output = None
        self.fmt = QAudioFormat()
        self.pullMode = False
        self.dump = filename
        self._label = SUSPEND_LABEL

        self.initializeAudio()

    def initializeAudio(self):
        self.pullTimer.timeout.connect(self.pullTimerExpired)

        self.pullMode = True

        self.fmt.setFrequency(DATA_FREQUENCY_HZ)
        self.fmt.setChannels(1)
        self.fmt.setSampleSize(16)
        self.fmt.setCodec('audio/pcm')
        self.fmt.setByteOrder(QAudioFormat.LittleEndian)
        self.fmt.setSampleType(QAudioFormat.SignedInt)

        info = QAudioDeviceInfo(QAudioDeviceInfo.defaultOutputDevice())
        if not info.isFormatSupported(self.fmt):
            print 'Default format not supported - trying to use nearest'
            self.fmt = info.nearestFormat(self.fmt)

        self.generator = Generator(self.fmt, DURATION_SECONDS * 1000000,
                                   TONE_FREQUENCY_HZ, self, self.dump)

        self.createAudioOutput()

    def createAudioOutput(self):
        self.audioOutput = QAudioOutput(self.device, self.fmt, self)
        self.audioOutput.notify.connect(self.notified)
        self.audioOutput.stateChanged.connect(self.stateChanged)
        self.generator.start()
        self.audioOutput.start(self.generator)

    @Slot()
    def toggleSuspendResume(self):
        if self.audioOutput.state() == QAudio.SuspendedState:
            print 'Status: Suspended, resuming'
            self.audioOutput.resume()
            self.stateLabel = SUSPEND_LABEL
        elif self.audioOutput.state() == QAudio.ActiveState:
            print 'Status: Active, suspending'
            self.audioOutput.suspend()
            self.stateLabel = RESUME_LABEL
        elif self.audioOutput.state() == QAudio.StoppedState:
            print 'Status: Stopped, resuming'
            self.audioOutput.resume()
            self.stateLabel = SUSPEND_LABEL
        elif self.audioOutput.state() == QAudio.IdleState:
            print 'Status: Idle'

    playbackResumed = Signal()

    @Slot()
    def toggleMode(self):
        self.pullTimer.stop()
        self.audioOutput.stop()

        if self.pullMode:
            print "Enabling push mode"
            self.output = self.audioOutput.start()
            self.pullMode = False
            self.pullTimer.start(5)
        else:
            print "Enabling pull mode"
            self.pullMode = True
            self.audioOutput.start(self.generator)
        self.playbackResumed.emit()

    @Slot(int)
    def deviceChanged(self, index):
        print "Device changed: index:", index
        print "Selected device name: ", self.devices[index].deviceName()
        self.pullTimer.stop()
        self.generator.stop()
        self.audioOutput.stop()
        self.audioOutput.disconnect(self)
        self.device = self.devices[index]
        self.createAudioOutput()

    def stateChanged(self, state):
        print 'State changed: ', state

    def notified(self):
        print 'Bytes free %d, elapsed usecs %d, processed usecs %d' % (
                self.audioOutput.bytesFree(),
                self.audioOutput.elapsedUSecs(),
                self.audioOutput.processedUSecs())

    def pullTimerExpired(self):
        if self.audioOutput.state() != QAudio.StoppedState:
            chunks = self.audioOutput.bytesFree() / self.audioOutput.periodSize()
            while chunks:
                data = self.generator.read(self.audioOutput.periodSize())
                self.output.write(data)
                if len(data) != self.audioOutput.periodSize():
                    break
                chunks -= 1


def main():
    app = QApplication([])
    app.setApplicationName('Audio Output Test')
    view = QDeclarativeView()

    devices = []
    for info in QAudioDeviceInfo.availableDevices(QAudio.AudioOutput):
        devices.append(info)

    player = TonePlayer(devices, sys.argv[1] if len(sys.argv) > 1 else None)

    context = view.rootContext()
    context.setContextProperty("player", player)
    context.setContextProperty("deviceModel", [x.deviceName() for x in devices])

    url = QUrl('main.qml')
    view.setSource(url)


    view.show()

    app.exec_()

if __name__ == '__main__':
    main()
