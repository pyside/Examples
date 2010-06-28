'''
Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
All rights reserved.
Contact: Nokia Corporation (qt-info@nokia.com)
Ported by PySide team (pyside@openbossa.org)

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

import sys

from PySide.QtCore import *
from QtMobility.Sensors import *

class AccelerometerFilter(QAccelerometerFilter):
    stamp = 0

    def filter(self, reading):
        diff = reading.timestamp() - self.stamp
        self.stamp = reading.timestamp()
	if diff:
            print "Acceleration: %.2f x" % reading.x(), " %.2f y" % reading.y(), " %.2f z m/s^2" % reading.z(), " %.2f ms since last, " % (diff / 1000), " %.2f Hz" % (1000000.0 / diff)
        return False # don't store the reading in the sensor

def main():
    app = QCoreApplication(sys.argv)
    if "-r" in  sys.argv:
        rate_place = sys.argv.index("-r")
    else:
        rate_place = -1
    rate_val = 0
    if (rate_place != -1):
        rate_val = int(sys.argv[rate_place + 1])

    sensor = QAccelerometer()
    if rate_val > 0:
        sensor.setDataRate(rate_val)

    filter = AccelerometerFilter()
    sensor.addFilter(filter)
    sensor.start()
    if not sensor.isActive():
        qWarning("Accelerometersensor didn't start!")
        return 1

    return app.exec_()

if __name__ == "__main__":
    main()
