from QtMobility.Location import *
from PySide.QtGui import *
import sys

from satellitedialog import *

app = QApplication(sys.argv)

dialog = SatelliteDialog(None,
		    30,
		    SatelliteDialog.ExitOnCancel,
		    SatelliteDialog.OrderByPrnNumber,
		    SatelliteDialog.ScaleToMaxPossible)

posSource = QGeoPositionInfoSource.createDefaultSource(None)
satSource = QGeoSatelliteInfoSource.createDefaultSource(None)

if posSource == None or satSource == None:
	QMessageBox.critical(None, "SatelliteDialog", "This examples requires a valid location source and no valid location sources are available on this platform.")
	sys.exit(-1)

posSource.setUpdateInterval(5000)
dialog.connectSources(posSource, satSource)

posSource.startUpdates()
satSource.startUpdates()

dialog.show()

result = app.exec_()

posSource.stopUpdates();
satSource.stopUpdates();
