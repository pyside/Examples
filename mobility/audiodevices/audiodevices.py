"""
 Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
 All rights reserved.
 Contact: Nokia Corporation (qt-info@nokia.com)

 This file is part of the examples of the Qt Toolkit.

 $QT_BEGIN_LICENSE:LGPL$
 Commercial Usage
 Licensees holding valid Qt Commercial licenses may use this file in
 accordance with the Qt Solutions Commercial License Agreement provided
 with the Software or, alternatively, in accordance with the terms
 contained in a written agreement between you and Nokia.

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

 GNU General Public License Usage
 Alternatively, this file may be used under the terms of the GNU
 General Public License version 3.0 as published by the Free Software
 Foundation and appearing in the file LICENSE.GPL included in the
 packaging of this file.  Please review the following information to
 ensure the GNU General Public License version 3.0 requirements will be
 met: http://www.gnu.org/copyleft/gpl.html.

 Please note Third Party Software included with Qt Solutions may impose
 additional restrictions and it is the user's responsibility to ensure
 that they have met the licensing requirements of the GPL, LGPL, or Qt
 Solutions Commercial license and the relevant license of the Third
 Party Software they are using.

 If you are unsure which license is appropriate for your use, please
 contact the sales department at qt-sales@nokia.com.
 $QT_END_LICENSE$
"""

from audiodevicesbase import Ui_AudioDevicesBase
from PySide.QtGui import QMainWindow, QTableWidgetItem
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

class AudioDevicesBase(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)


class AudioTest(AudioDevicesBase, Ui_AudioDevicesBase):
    def __init__(self, parent=None):
        AudioDevicesBase.__init__(self, parent)

        self.deviceInfo = QAudioDeviceInfo()
        self.settings = QAudioFormat()
        self.mode = QAudio.Mode()

        self.mode = QAudio.AudioOutput
        self.testButton.clicked.connect(self.test)
        self.modeBox.activated[int].connect(self.modeChanged)
        self.deviceBox.activated[int].connect(self.deviceChanged)
        self.frequencyBox.activated[int].connect(self.freqChanged)
        self.channelsBox.activated[int].connect(self.channelChanged)
        self.codecsBox.activated[int].connect(self.codecChanged)
        self.sampleSizesBox.activated[int].connect(self.sampleSizeChanged)
        self.sampleTypesBox.activated[int].connect(self.sampleTypeChanged)
        self.endianBox.activated[int].connect(self.endianChanged)
        self.populateTableButton.clicked.connect(self.populateTable)
        self.modeBox.setCurrentIndex(0)
        self.modeChanged(0)
        self.deviceBox.setCurrentIndex(0)
        self.deviceChanged(0)

    def test(self):
        # tries to set all the settings picked.
        self.testResult.clear()
        if not self.deviceInfo.isNull():
            if self.deviceInfo.isFormatSupported(self.settings):
                self.testResult.setText(self.tr("Success"))
                self.nearestFreq.setText("")
                self.nearestChannel.setText("")
                self.nearestCodec.setText("")
                self.nearestSampleSize.setText("")
                self.nearestSampleType.setText("")
                self.nearestEndian.setText("")
            else:
                nearest = self.deviceInfo.nearestFormat(self.settings)
                self.testResult.setText(self.tr("Failed"))
                self.nearestFreq.setText(str(nearest.frequency()))
                self.nearestChannel.setText(str(nearest.channels()))
                self.nearestCodec.setText(nearest.codec())
                self.nearestSampleSize.setText(str(nearest.sampleSize()))
                self.nearestSampleType.setText(sampletoString(nearest.sampleType()))
                self. nearestEndian.setText(byteOrdertoString(nearest.byteOrder()))
        else:
            self.testResult.setText(self.tr("No Device"))

    def modeChanged(self, idx):
        self.testResult.clear();
        # mode has changed
        if idx == 0:
            mode = QAudio.AudioInput
        else:
            mode = QAudio.AudioOutput

        self.deviceBox.clear()
        for deviceInfo in QAudioDeviceInfo.availableDevices(mode):
            self.deviceBox.addItem(deviceInfo.deviceName(), deviceInfo)

        self.deviceBox.setCurrentIndex(0)
        self.deviceChanged(0)

    def deviceChanged(self, idx):
        self.testResult.clear()
        if self.deviceBox.count() == 0:
            return

        # device has changed
        self.deviceInfo = self.deviceBox.itemData(idx)
        self.frequencyBox.clear()
        freqz = self.deviceInfo.supportedFrequencies()
        for freq in freqz:
            self.frequencyBox.addItem(str(freq))
        if len(freqz):
            self.settings.setFrequency(freqz[0])

        self.channelsBox.clear();
        chz = self.deviceInfo.supportedChannels()
        for ch in chz:
            self.channelsBox.addItem(str(ch))
        if len(chz):
            self.settings.setChannels(chz[0])

        self.codecsBox.clear()
        codecz = self.deviceInfo.supportedCodecs()
        for codec in codecz:
            self.codecsBox.addItem(codec)
        if len(codecz):
            self.settings.setCodec(codecz[0])

        # Add false to create failed condition!
        self.codecsBox.addItem("audio/test");

        self.sampleSizesBox.clear()
        sampleSizez = self.deviceInfo.supportedSampleSizes()
        for sample in sampleSizez:
            self.sampleSizesBox.addItem(str(sample))
        if len(sampleSizez):
            self.settings.setSampleSize(sampleSizez[0])

        self.sampleTypesBox.clear()
        sampleTypez = self.deviceInfo.supportedSampleTypes()
        for sample in sampleTypez:
            self.sampleTypesBox.addItem(sampletoString(sample))
        if len(sampleTypez):
            self.settings.setSampleType(sampleTypez[0])

        self.endianBox.clear();
        endianz = self.deviceInfo.supportedByteOrders()
        for endian in endianz:
            self.endianBox.addItem(byteOrdertoString(endian))
        if len(endianz):
            self.settings.setByteOrder(endianz[0])

        self.allFormatsTable.clearContents()

    def populateTable(self):
        row = 0
        format = QAudioFormat()
        for codec in self.deviceInfo.supportedCodecs():
            format.setCodec(codec)
            for frequency in self.deviceInfo.supportedFrequencies():
                format.setFrequency(frequency)
                for channels in self.deviceInfo.supportedChannels():
                    format.setChannels(channels)
                    for sampleType in self.deviceInfo.supportedSampleTypes():
                        format.setSampleType(sampleType)
                        for sampleSize in self.deviceInfo.supportedSampleSizes():
                            format.setSampleSize(sampleSize)
                            for endian in self.deviceInfo.supportedByteOrders():
                                format.setByteOrder(endian)
                                if self.deviceInfo.isFormatSupported(format):
                                    self.allFormatsTable.setRowCount(row + 1);

                                    codecItem = QTableWidgetItem(format.codec())
                                    self.allFormatsTable.setItem(row, 0, codecItem)

                                    frequencyItem = QTableWidgetItem(str(format.frequency()))
                                    self.allFormatsTable.setItem(row, 1, frequencyItem)

                                    channelsItem = QTableWidgetItem(str(format.channels()))
                                    self.allFormatsTable.setItem(row, 2, channelsItem)

                                    sampleTypeItem = QTableWidgetItem(sampletoString(format.sampleType()))
                                    self.allFormatsTable.setItem(row, 3, sampleTypeItem)

                                    sampleSizeItem = QTableWidgetItem(str(format.sampleSize()))
                                    self.allFormatsTable.setItem(row, 4, sampleSizeItem)

                                    byteOrderItem = QTableWidgetItem(byteOrdertoString(format.byteOrder()))
                                    self.allFormatsTable.setItem(row, 5, byteOrderItem)
                                    row += 1

    def freqChanged(self, idx):
        # freq has changed
        self.settings.setFrequency(int(self.frequencyBox.itemText(idx)))

    def channelChanged(self, idx):
        self.settings.setChannels(int(self.channelsBox.itemText(idx)))

    def codecChanged(self, idx):
        self.settings.setCodec(self.codecsBox.itemText(idx))

    def sampleSizeChanged(self, idx):
        self.settings.setSampleSize(int(self.sampleSizesBox.itemText(idx)))

    def sampleTypeChanged(self, idx):
        sampleType = stringToSample(self.sampleTypesBox.itemText(idx))
        if sampleType == QAudioFormat.SignedInt:
            self.settings.setSampleType(QAudioFormat.SignedInt)
        elif sampleType == QAudioFormat.UnSignedInt:
            self.settings.setSampleType(QAudioFormat.UnSignedInt)
        elif sampleType == QAudioFormat.Float:
            self.settings.setSampleType(QAudioFormat.Float)

    def endianChanged(self, idx):
        endian = stringToByteOrder(self.endianBox.itemText(idx))
        if endian == QAudioFormat.LittleEndian:
            self.settings.setByteOrder(QAudioFormat.LittleEndian)
        elif endian == QAudioFormat.BigEndian:
            self.settings.setByteOrder(QAudioFormat.BigEndian)
