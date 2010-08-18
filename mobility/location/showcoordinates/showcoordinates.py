from PySide.QtCore import *
from QtMobility.Location import *
import sys

class ShowCoordinates:
    def __init__(self):
        self.source = QGeoPositionInfoSource.createDefaultSource(None)
        if self.source is not None:
            self.source.setUpdateInterval(5000)
            self.source.positionUpdated.connect(self.positionUpdated)
            self.source.startUpdates()
            print "Waiting for a fix..."


    def positionUpdated(self, update):
        print "position:"
        print "%s, %s" % (update.coordinate().latitude(), update.coordinate().longitude())


if __name__ == "__main__":

    app = QCoreApplication([])
    reader = ShowCoordinates()
    sys.exit(app.exec_())


