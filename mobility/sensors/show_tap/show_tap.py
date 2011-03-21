'''
Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
All rights reserved.
Contact: Nokia Corporation (qt-info@nokia.com)
Ported by PySide team (pyside@openbossa.org)

This file is part of the Qt Mobility Components.

$QT_BEGIN_LICENSE:BSD$
You may use this file under the terms of the BSD license as follows:

"Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:
  * Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.
  * Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in
    the documentation and/or other materials provided with the
    distribution.
  * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
    the names of its contributors may be used to endorse or promote
    products derived from this software without specific prior written
    permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
$QT_END_LICENSE$
'''

import sys

from PySide.QtCore import *
from QtMobility.Sensors import *

class TapSensorFilter(QTapFilter):
    stamp = 0

    def filter(self, reading):
        diff = reading.timestamp() - self.stamp
        self.stamp = reading.timestamp()
        tapdir = reading.tapDirection()
        if tapdir == QTapReading.X:
            output = "X"
        elif tapdir == QTapReading.Y:
            output = "Y"
        elif tapdir == QTapReading.Z:
            output = "Z"
        elif tapdir == QTapReading.X_Pos:
            output = "X pos"
        elif tapdir == QTapReading.Y_Pos:
            output = "Y pos"
        elif tapdir == QTapReading.Z_Pos:
            output = "Z pos"
        elif tapdir == QTapReading.X_Neg:
            output = "X neg"
        elif tapdir == QTapReading.Y_Neg:
            output = "Y neg"
        elif tapdir == QTapReading.Z_Neg:
            output = "Z neg"
        elif tapdir == QTapReading.X_Both:
            output = "X (both)"
        elif tapdir == QTapReading.Y_Both:
            output = "Y (both)"
        elif tapdir == QTapReading.Z_Both:
            output = "Z (both)"
        elif tapdir == QTapReading.Undefined:
            output = "Undefined"
        else:
            output = "Invalid enum value"

        print "Tap: "
        if reading.isDoubleTap():
            print "Double "
        else:
            print "Single "
        print output
        print " (%.2f ms since last, " % (diff / 1000.0), "%.2f Hz)" % (1000000.0 / diff),
        return False # don't store the reading in the sensor

if __name__ == "__main__":
    app = QCoreApplication(sys.argv)
    rate_val = 0

    doublesensor = QTapSensor()
    doublesensor.connectToBackend()    
    if rate_val > 0:
        doublesensor.setDataRate(rate_val)

    filterSensor = TapSensorFilter()
    doublesensor.addFilter(filterSensor)
    doublesensor.setProperty("returnDoubleTapEvents", True)
    doublesensor.start()
    if not doublesensor.isActive():
        qWarning("Tapsensor (double) didn't start!")
        exit()

    singlesensor = QTapSensor()
    singlesensor.connectToBackend()
    if rate_val > 0:
        singlesensor.setDataRate(rate_val)

    filterSensor = TapSensorFilter()
    singlesensor.addFilter(filterSensor)
    singlesensor.setProperty("returnDoubleTapEvents", False)
    singlesensor.start()
    if not singlesensor.isActive():
        qWarning("Tapsensor (single) didn't start!")
        exit()

    app.exec_()
