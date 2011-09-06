
import sys

from PySide.QtCore import QIODevice, QByteArray, QTimer
from PySide.QtGui import QWidget, QMainWindow, QVBoxLayout, QPushButton
from PySide.QtGui import QComboBox, QApplication
from QtMobility.MultimediaKit import QAudioFormat, QAudio, QAudioDeviceInfo
from QtMobility.MultimediaKit import QAudioOutput
import struct

from math import sin, pi

from generator import Generator

DURATION_SECONDS = 1
TONE_FREQUENCY_HZ = 600
DATA_FREQUENCY_HZ = 44100
BUFFER_SIZE = 32768

PUSH_MODE_LABEL = 'Enable push mode'
PULL_MODE_LABEL = 'Enable pull mode'
SUSPEND_LABEL = 'Suspend playback'
RESUME_LABEL = 'Resume playback'

class AudioTest(QMainWindow):

    def __init__(self, filename=None):
        QMainWindow.__init__(self)
        self.pullTimer = QTimer(self)

        # Owned by layout
        self.modeButton = None
        self.suspendResumeButton = None
        self.deviceBox = None

        self.device = QAudioDeviceInfo.defaultOutputDevice()
        self.generator = None
        self.audioOutput = None
        self.output = None
        self.fmt = QAudioFormat()
        self.pullMode = False
        self.buf = QByteArray(BUFFER_SIZE, 0)
        self.dump = filename

        self.initializeWindow()
        self.initializeAudio()

    def initializeWindow(self):
        window = QWidget()
        layout = QVBoxLayout()

        self.deviceBox = QComboBox(self)
        for info in QAudioDeviceInfo.availableDevices(QAudio.AudioOutput):
            self.deviceBox.addItem(info.deviceName(), info)

        self.deviceBox.activated[int].connect(self.deviceChanged)
        layout.addWidget(self.deviceBox)

        self.modeButton = QPushButton(self)
        self.modeButton.setText(PUSH_MODE_LABEL)
        self.modeButton.clicked.connect(self.toggleMode)
        layout.addWidget(self.modeButton)

        self.suspendResumeButton = QPushButton(self)
        self.suspendResumeButton.setText(SUSPEND_LABEL)
        self.suspendResumeButton.clicked.connect(self.toggleSuspendResume)
        layout.addWidget(self.suspendResumeButton)

        window.setLayout(layout)
        self.setCentralWidget(window)
        window.show()

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

    # Slots
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

    def toggleMode(self):
        self.pullTimer.stop()
        self.audioOutput.stop()

        if self.pullMode:
            self.modeButton.setText(PULL_MODE_LABEL)
            self.output = self.audioOutput.start()
            self.pullMode = False
            self.pullTimer.start(5)
        else:
            self.modeButton.setText(PUSH_MODE_LABEL)
            self.pullMode = True
            self.audioOutput.start(self.generator)

        self.suspendResumeButton.setText(SUSPEND_LABEL)

    def toggleSuspendResume(self):
        if self.audioOutput.state() == QAudio.SuspendedState:
            print 'Status: Suspended, resuming'
            self.audioOutput.resume()
            self.suspendResumeButton.setText(SUSPEND_LABEL)
        elif self.audioOutput.state() == QAudio.ActiveState:
            print 'Status: Active, suspending'
            self.audioOutput.suspend()
            self.suspendResumeButton.setText(RESUME_LABEL)
        elif self.audioOutput.state() == QAudio.StoppedState:
            print 'Status: Stopped, resuming'
            self.audioOutput.resume()
            self.suspendResumeButton.setText(SUSPEND_LABEL)
        elif self.audioOutput.state() == QAudio.IdleState:
            print 'Status: Idle'

    def stateChanged(self, state):
        print 'State changed: ', state

    def deviceChanged(self, index):
        self.pullTimer.stop()
        self.generator.stop()
        self.audioOutput.stop()
        self.audioOutput.disconnect(self)
        self.device = self.deviceBox.itemData(index)
        self.createAudioOutput()


def main():

    app = QApplication(sys.argv)
    app.setApplicationName('Audio Output Test')

    try:
        filename = sys.argv[1]
    except IndexError:
        filename = None

    window = AudioTest(filename=filename)
    window.show()

    return app.exec_()


if __name__ == '__main__':
    sys.exit(main())
