from QtMobility.Location import *
from PySide.QtGui import *
from PySide.QtCore import *

class SatelliteWidget (QWidget):
    numBars = 32
    gapWidth = 1
    barWidth = 3
    spanWidth = gapWidth + barWidth
    borderOffset = 4
    legendTextOffset = 5


    def __init__(self, parent, ordering, scaling):
        QWidget.__init__(self, parent)

        self._ordering = ordering
        self._scaling = scaling

        painter = QPainter(self)
        self.textHeight =  20 #painter.fontMetrics().height()
        self.legendHeight = SatelliteWidget.borderOffset + self.textHeight + 2

        self.inViewColor = QColor(192, 192, 255);
        self.inUseColor = QColor(64, 64, 255);
        self.satellitesInView = []
        self.satellitesInUse = []
        self.satellites = []

        self.ordering = property(self.getOrdering, self.setOrdering)
        self.strengthScaling = property(self.getStrengthScaling, self.setStrengthScaling)

    def getOrdering(self):
        return self._ordering

    def setOrdering(self, ordering):
        if (ordering != self._ordering):
            self._ordering = ordering;
            self.updateSatelliteList()

    def getStrengthScaling(self):
        return self.scaling

    def setStrengthScaling(self, scaling):
        if scaling != self.scaling:
            self.scaling = scaling
            self.updateSatelliteList()

    def clearSatellites(self):
        self.satellitesInView = []
        self.satellitesInUse = []
        self.updateSatelliteList()

    def satellitesInViewUpdated(self, satellites):
        self.satellitesInView = satellites
        self.satellitesInView.sort(lambda s1, s2 : s1.prnNumber() < s2.prnNumber())
        self.updateSatelliteList()

    def satellitesInUseUpdated(self, satellites):
        self.satellitesInUse = satellites
        self.satellitesInUse.sort(lambda s1, s2 : s1.prnNumber() < s2.prnNumber())
        self.updateSatelliteList()

    def updateSatelliteList(self):
        self.satellites = []

        if len(self.satellitesInUse) == 0 and len(self.satellitesInView) == 0:
            self.update()
            return

        for satellite in self.satellitesInUse:
            if satellite.signalStrength() != 0:
                self.satellites.append((satellite, True))

        for satellite in self.satellitesInView:
            if satellite.signalStrength() == 0:
                continue

            if satellite not in self.satellitesInUse:
                self.satellites.append((satellite, False))

        if self._ordering == SatelliteDialog.OrderByPrnNumber:
            self.satellites.sort(lambda p1, p2 : p1[0].prnNumber() < p2[0].prnNumber())
            self.maximumSignalStrength = 0
            for satellite in self.satellites:
                if satellite[0].signalStrength() > self.maximumSignalStrength:
                    self.maximumSignalStrength = satellite[0].signalStrength()
        else:
            self.satellites.sort(lambda p1, p2 : p1[0].signalStrength() < p2[0].signalStrength())
            self.maximumSignalStrength = self.satellites[-1][0].signalStrength()

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        satBounds = QRect(self.rect().x() + self.borderOffset,
                          self.rect().y() + self.borderOffset,
                          self.rect().width() - 2 * self.borderOffset,
                          self.rect().height() - self.legendHeight - 2 * self.borderOffset)


        painter.setPen(QApplication.palette().color(QPalette.WindowText))
        painter.setBrush(QApplication.palette().color(QPalette.Base))
        painter.drawRect(satBounds)

        for i in range(0, len(self.satellites)):
            self.paintSatellite(painter, satBounds, i)

        legendBounds = QRect(self.rect().x() + self.borderOffset,
                             self.rect().height() - self.legendHeight,
                             self.rect().width() - 2 * self.borderOffset,
                             self.legendHeight);
        self.paintLegend(painter, legendBounds);

    def paintSatellite(self, painter, bounds, index):
        bars = self.numBars
        if self._ordering == SatelliteDialog.OrderBySignalStrength:
            bars = len(satellites)

        pixelsPerUnit = bounds.width() / float(bars * self.spanWidth + self.gapWidth)
        spanPixels = pixelsPerUnit * self.spanWidth
        gapPixels = pixelsPerUnit * self.gapWidth
        barPixels = pixelsPerUnit * self.barWidth

        painter.setPen(QApplication.palette().color(QPalette.WindowText))
        if not self.satellites[index][1]:
            painter.setBrush(self.inViewColor)
        else:
            painter.setBrush(self.inUseColor)

        maximum = 100
        if self._scaling == SatelliteDialog.ScaleToMaxAvailable:
            maximum = self.maximumSignalStrength

        i = index;
        if self._ordering == SatelliteDialog.OrderByPrnNumber:
            i = self.satellites[index][0].prnNumber() - 1

        height = (self.satellites[index][0].signalStrength() / float(maximum)) * bounds.height()

        r = QRectF(bounds.x() + gapPixels + i * spanPixels, bounds.y() + bounds.height() - 1 - height, barPixels, height);
        painter.drawRect(r);

    def paintLegend(self, painter, bounds):
        halfWidth = bounds.width() / 2.0

        keyX = bounds.x() + 1
        textX = keyX + self.legendHeight + 2 + self.legendTextOffset
        y = bounds.y() + 1
        keyWidth = self.legendHeight - 2 - self.borderOffset
        textWidth = halfWidth  - self.legendHeight - 3 - self.legendTextOffset
        height = self.legendHeight - 2 - self.borderOffset

        viewKeyRect = QRectF(keyX, y, keyWidth, height)
        viewTextRect = QRectF(textX, y, textWidth, height)
        useKeyRect = QRectF(keyX + halfWidth, y, keyWidth, height)
        useTextRect = QRectF(textX + halfWidth, y, textWidth, height)

        painter.setPen(QApplication.palette().color(QPalette.WindowText))

        painter.setBrush(self.inViewColor)
        painter.drawRect(viewKeyRect)

        painter.setBrush(self.inUseColor);
        painter.drawRect(useKeyRect);

        #painter.setPen(QApplication.palette().color(QPalette.Text))
        painter.setPen(QColor(255,255,255))
        painter.drawText(viewTextRect, Qt.AlignLeft, self.tr("In View"))
        painter.drawText(useTextRect, Qt.AlignLeft, self.tr("In Use"))

    def sizeHint(self):
        return QSize(self.parentWidget().width(), self.parentWidget().width() / 2 + self.legendHeight);


class SatelliteDialog(QDialog):
    # ExitBehaviour
    ExitOnFixOrCancel = 0
    ExitOnCancel = 1

    # Ordering
    OrderBySignalStrength = 0
    OrderByPrnNumber = 1

    # StrengthScaling
    ScaleToMaxAvailable = 0
    ScaleToMaxPossible = 1

    def __init__(self, parent,
                 noSatelliteTimeoutSeconds = 30,
                 exitBehaviour = ExitOnFixOrCancel,
                 ordering = OrderBySignalStrength,
                 scaling = ScaleToMaxPossible):
        QDialog.__init__(self, parent)

        self.noSatelliteTimeoutSeconds = noSatelliteTimeoutSeconds
        self.exitBehaviour = exitBehaviour
        self.ordering = ordering
        self.scaling = scaling

        self.noSatelliteTimer = QTimer(self);
        self.noSatelliteTimer.setInterval(self.noSatelliteTimeoutSeconds * 1000)
        self.noSatelliteTimer.setSingleShot(True)

        self.noSatelliteTimer.timeout.connect(self.noSatelliteTimeout)

        self.satelliteWidget = SatelliteWidget(self, ordering, scaling)

        titleLabel = QLabel(self.tr("Satellite Signal Strength"))
        titleLabel.setAlignment(Qt.AlignCenter | Qt.AlignBottom)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(titleLabel)
        mainLayout.addWidget(self.satelliteWidget)

        switchAction = QAction(self)
        switchAction.setText(self.tr("Switch"))
        switchAction.setSoftKeyRole(QAction.PositiveSoftKey)

        switchAction.triggered.connect(self.switchButtonClicked)
        self.addAction(switchAction)

        cancelAction = QAction(self)
        cancelAction.setText(self.tr("Cancel"))
        cancelAction.setSoftKeyRole(QAction.NegativeSoftKey)

        cancelAction.triggered.connect(self.reject)
        self.addAction(cancelAction)

        menuBar = QMenuBar(self)
        menuBar.addAction(switchAction)
        menuBar.addAction(cancelAction)

        self.setLayout(mainLayout)

        self.setWindowTitle(self.tr("Waiting for GPS fix"));

        self.setModal(True);

    def connectSources(self, posSource, satSource):
        posSource.positionUpdated.connect(self.positionUpdated)
        satSource.satellitesInViewUpdated.connect(self.satellitesInViewUpdated)
        satSource.satellitesInUseUpdated.connect(self.satellitesInUseUpdated)

    def switchButtonClicked(self):
        o = self.ordering()
        if o == SatelliteDialog.OrderByPrnNumber:
            self.setOrdering(SatelliteDialog.OrderBySignalStrength)
        elif (o == SatelliteDialog.OrderBySignalStrength):
            self.setOrdering(SatelliteDialog.OrderByPrnNumber)

    def ordering(self):
        return self.satelliteWidget.ordering()

    def setOrdering(self, ordering):
        self.satelliteWidget.setOrdering(ordering)

    def strengthScaling(self):
        return self.satelliteWidget.strengthScaling()

    def setStrengthScaling(self, scaling):
        self.satelliteWidget.setStrengthScaling(scaling)

    def noSatelliteTimeout(self):
        self.satelliteWidget.clearSatellites()

    def positionUpdated(self, pos):
        if self.exitBehaviour == SatelliteDialog.ExitOnFixOrCancel:
            accept()

    def satellitesInViewUpdated(self, satellites):
        self.noSatelliteTimer.stop()
        self.satelliteWidget.satellitesInViewUpdated(satellites)
        self.noSatelliteTimer.start()

    def satellitesInUseUpdated(self, satellites):
        self.noSatelliteTimer.stop();
        self.satelliteWidget.satellitesInUseUpdated(satellites)
        self.noSatelliteTimer.start()
