"""
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
"""

from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtDeclarative import *
from QtMobility.MultimediaKit import QAudioDeviceInfo, QAudio, QAudioFormat

def sampletoString(sampleType):
    result = "Unknown"
    if sampleType == QAudioFormat.SignedInt:
        result = "SignedInt"
    elif sampleType == QAudioFormat.UnSignedInt:
        result = "UnSignedInt"
    elif sampleType == QAudioFormat.Float:
        result = "Float"

    return result

def stringToSample(sampleType):
    if sampleType == "SignedInt":
        return QAudioFormat.SignedInt
    elif sampleType == "UnSignedInt":
        return QAudioFormat.UnSignedInt
    elif sampleType == "Float":
        return QAudioFormat.Float

def byteOrdertoString(endian):
    result = "Unknown"
    if endian == QAudioFormat.LittleEndian:
        result = "LittleEndian"
    elif endian == QAudioFormat.BigEndian:
        result = "BigEndian"

    return result

def stringToByteOrder(endian):
    if endian == "LittleEndian":
        return QAudioFormat.LittleEndian
    elif endian == "BigEndian":
        return QAudioFormat.BigEndian

class AudioTest(QObject):
    modeHasChanged = Signal("QVariantList")
    newResult = Signal(str)
    newNearest = Signal("QVariantList")

    def __init__(self, parent=None):
        QObject.__init__(self, parent)

        self.deviceInfo = QAudioDeviceInfo()
        self.settings = QAudioFormat()
        self.mode = QAudio.Mode()
        self._availableDevices = {}
        self._availableCodecs = {}
        self._availableFreqs = {}
        self._availableChannels = {}
        self._availableTypes = {}
        self._availableSizes = {}
        self._availableEnds = {}

        self.mode = QAudio.AudioOutput

    @Slot()
    def test(self):
        # tries to set all the settings picked.
        if not self.deviceInfo.isNull():
            if self.deviceInfo.isFormatSupported(self.settings):
                self.newResult.emit("Success")
                '''
                self.testResult.setText(self.tr("Success"))
                self.nearestFreq.setText("")
                self.nearestChannel.setText("")
                self.nearestCodec.setText("")
                self.nearestSampleSize.setText("")
                self.nearestSampleType.setText("")
                self.nearestEndian.setText("")
                '''
            else:
                nearest = self.deviceInfo.nearestFormat(self.settings)
                self.newResult.emit("Failed")
                newValues = []
                newValues.append("") # keep the same positions as newLabels list
                newValues.append(nearest.codec()) # codec - 1
                newValues.append(str(nearest.frequency())) # freq - 2
                newValues.append(str(nearest.channels())) # channel - 3
                newValues.append(sampletoString(nearest.sampleType())) # type - 4
                newValues.append(str(nearest.sampleSize())) # size - 5
                newValues.append(byteOrdertoString(nearest.byteOrder())) # end - 6
                self.newNearest.emit(newValues)
        else:
            self.newResult.emit("No Device")

    @Slot(str)
    def modeChanged(self, idx):
        # mode has changed
        if idx == "Input":
            mode = QAudio.AudioInput
        else:
            mode = QAudio.AudioOutput

        self._availableDevices = {}
        for deviceInfo in QAudioDeviceInfo.availableDevices(mode):
            self._availableDevices[deviceInfo.deviceName()] = deviceInfo

        firstDevice = QAudioDeviceInfo.availableDevices(mode)[0].deviceName()
        self.deviceChanged(firstDevice)

    @Slot(str)
    def deviceChanged(self, idx):
        if len(self._availableDevices) == 0:
            return
        newLabels = []
        newLabels.append(idx) # device - 0

        # device has changed
        self.deviceInfo = self._availableDevices[idx]

        codecz = self.deviceInfo.supportedCodecs()
        self._availableCodecs = {}
        for codec in codecz:
            self._availableCodecs[codec] = codec
        if len(codecz):
            self.settings.setCodec(codecz[0])
            newLabels.append(codecz[0]) # codec - 1

        freqz = self.deviceInfo.supportedFrequencies()
        self._availableFreqs = {}
        for freq in freqz:
            self._availableFreqs[str(freq)] = freq
        if len(freqz):
            self.settings.setFrequency(freqz[0])
            newLabels.append(str(freqz[0])) # freq - 2

        chz = self.deviceInfo.supportedChannels()
        self._availableChannels = {}
        for ch in chz:
            self._availableChannels[str(ch)] = ch
        # Add false to create failed condition!
        self._availableChannels["FAIL"] = -1
        if len(chz):
            self.settings.setChannels(chz[0])
            newLabels.append(str(chz[0])) # channel - 3


        sampleTypes = self.deviceInfo.supportedSampleTypes()
        self._availableTypes = {}
        for sample in sampleTypes:
            self._availableTypes[sampletoString(sample)] = sample
        if len(sampleTypes):
            self.settings.setSampleType(sampleTypes[0])
            newLabels.append(sampletoString(sampleTypes[0])) # type - 4

        sampleSizes = self.deviceInfo.supportedSampleSizes()
        self._availableSizes = {}
        for sample in sampleSizes:
            self._availableSizes[str(sample)] = sample
        if len(sampleSizes):
            self.settings.setSampleSize(sampleSizes[0])
            newLabels.append(str(sampleSizes[0])) # size - 5

        endianz = self.deviceInfo.supportedByteOrders()
        self._availableEnds = {}
        for endian in endianz:
            self._availableEnds[byteOrdertoString(endian)] = endian
        if len(endianz):
            self.settings.setByteOrder(endianz[0])
            newLabels.append(byteOrdertoString(endianz[0])) # end - 6

        # Update all the buttons
        self.modeHasChanged.emit(newLabels)

    @Slot(str)
    def codecChanged(self, idx):
        self.settings.setCodec(self._availableCodecs[idx])

    @Slot(str)
    def freqChanged(self, idx):
        # freq has changed
        self.settings.setFrequency(int(self._availableFreqs[idx]))

    @Slot(str)
    def channelChanged(self, idx):
        self.settings.setChannels(int(self._availableChannels[idx]))

    @Slot(str)
    def sizeChanged(self, idx):
        self.settings.setSampleSize(int(self._availableSizes[idx]))

    @Slot(str)
    def typeChanged(self, idx):
        sampleType = stringToSample(self._availableTypes[idx])
        if sampleType == QAudioFormat.SignedInt:
            self.settings.setSampleType(QAudioFormat.SignedInt)
        elif sampleType == QAudioFormat.UnSignedInt:
            self.settings.setSampleType(QAudioFormat.UnSignedInt)
        elif sampleType == QAudioFormat.Float:
            self.settings.setSampleType(QAudioFormat.Float)

    @Slot(str)
    def endChanged(self, idx):
        endian = stringToByteOrder(self._availableEnds[idx])
        if endian == QAudioFormat.LittleEndian:
            self.settings.setByteOrder(QAudioFormat.LittleEndian)
        elif endian == QAudioFormat.BigEndian:
            self.settings.setByteOrder(QAudioFormat.BigEndian)

    @Property("QStringList", constant=True)
    def availableDevices(self):
        return self._availableDevices.keys()

    @Property("QStringList", constant=True)
    def availableCodecs(self):
        return self._availableCodecs.keys()

    @Property("QStringList", constant=True)
    def availableFreqs(self):
        return self._availableFreqs.keys()

    @Property("QStringList", constant=True)
    def availableChannels(self):
        return self._availableChannels.keys()

    @Property("QStringList", constant=True)
    def availableTypes(self):
        return self._availableTypes.keys()

    @Property("QStringList", constant=True)
    def availableSizes(self):
        return self._availableSizes.keys()

    @Property("QStringList", constant=True)
    def availableEnds(self):
        return self._availableEnds.keys()


def main():
    app = QApplication([])
    view = QDeclarativeView()
    player = AudioTest()
    context = view.rootContext()
    context.setContextProperty("audioPlayer", player)

    url = QUrl('main.qml')
    view.setSource(url)
    view.showFullScreen()

    player.modeChanged("Input")
    app.exec_()


if __name__ == '__main__':
    main()



