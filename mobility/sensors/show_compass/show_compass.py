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

class CompassFilter(QCompassFilter):
    stamp = 0

    def filter(self, reading):
        diff = reading.timestamp() - self.stamp
        stamp = reading.timestamp()
        print "Compass heading: %.2f" % reading.azimuth(), " calibration: %.2f" % reading.calibrationLevel(), " (%.2f ms since last, " % (diff / 1000), "%.2f Hz)" % (1000000.0 / diff)
        return True

if __name__ == "__main__":
    app = QCoreApplication(sys.argv)
    if "-r" in sys.argv:
        rate_place = sys.argv.index("-r")
    else:
        rate_place = -1
    rate_val = 0
    if (rate_place != -1):
        rate_val = int(sys.argv[rate_place + 1])
    sensor = QCompass()
    if (rate_val > 0):
        sensor.setDataRate(rate_val)

    filter = CompassFilter()
    sensor.addFilter(filter)
    sensor.start()
    if not sensor.isActive():
        qWarning("Compasssensor didn't start!")
    else:
        app.exec_()
