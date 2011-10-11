
import struct
from math import sin, pi

from PySide.QtCore import QIODevice, QByteArray, QTimer
from QtMobility.MultimediaKit import QAudioFormat, QAudio, QAudioDeviceInfo

signed8 = struct.Struct('>b')
unsigned8 = struct.Struct('>B')

bigSigned16 = struct.Struct('>h')
bigUnsigned16 = struct.Struct('>H')

littleSigned16 = struct.Struct('<h')
littleUnsigned16 = struct.Struct('<H')


class Generator(QIODevice):

    def __init__(self, fmt, durationUs, frequency, parent, filename=None):
        QIODevice.__init__(self, parent)
        self.pos = 0
        self.buf = []

        self.generateData(fmt, durationUs, frequency)
        if filename:
            self.dump(filename, fmt)

    def dump(self, filename, fmt):

        import wave

        handle = wave.open(filename, 'wb')

        handle.setnchannels(fmt.channels())
        handle.setsampwidth(fmt.sampleSize()/8)
        handle.setframerate(fmt.sampleRate())
        handle.writeframes(''.join(self.buf))

        handle.close()

    def start(self):
        self.open(QIODevice.ReadOnly)

    def stop(self):
        self.pos = 0
        self.close()

    def readData(self, size):
        total = 0
        data = []

        while size - total > 0:
            chunk = min(len(self.buf) - self.pos, size - total)
            data.extend(self.buf[self.pos:self.pos + chunk])
            self.pos = (self.pos + chunk) % len(self.buf)
            total += chunk

        return ''.join(data)

    def writeData(self, data, maxLen):
        return 0

    def bytesAvailable(self):
        return len(self.buf) + QIODevice.bytesAvailable(self)

    def generateData(self, fmt, durationUs, frequency):
        channelBytes = fmt.sampleSize() / 8
        sampleBytes = fmt.channels() * channelBytes

        seconds = durationUs / 1000000
        length = fmt.frequency() * sampleBytes * seconds

        assert length % sampleBytes == 0

        self.buf = [''] * length

        sampleIndex = 0

        for i in range(0, length, channelBytes):
            position = float(sampleIndex % fmt.frequency()) / fmt.frequency()
            x = sin(2 * pi * frequency * position)

            for channel in range(fmt.channels()):
                if fmt.sampleSize() == 8:
                    value = ((1.0 + x) / 2 * 255) % 255

                    if fmt.sampleType() == QAudioFormat.UnSignedInt:
                        data = unsigned8.pack(value)
                    else: #Signed
                        data = signed8.pack(value - 127)

                    self.buf[i + channel * channelBytes] = data

                elif fmt.sampleSize() == 16:
                    value = ((1.0 + x) / 2 * 65535) % 65535

                    if fmt.sampleType() == QAudioFormat.UnSignedInt:
                        if fmt.byteOrder() == QAudioFormat.LittleEndian:
                            data = littleUnsigned16.pack(value)
                        else:
                            data = bigUnsigned16.pack(value)
                    else:
                        value -= 32767

                        if fmt.byteOrder() == QAudioFormat.LittleEndian:
                            data = littleSigned16.pack(value)
                        else:
                            data = bigSigned16.pack(value)

                    self.buf[i + channel * channelBytes] = data[0]
                    self.buf[i + channel * channelBytes + 1] = data[1]

            sampleIndex += 1



