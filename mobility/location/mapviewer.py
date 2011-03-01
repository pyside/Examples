
import sys
from collections import deque

from PySide.QtCore import QTimer, Qt, QRect, QPoint, Signal, QObject, QRectF, QPointF
from PySide.QtCore import QTime
from PySide.QtGui import QApplication, QMessageBox, QMainWindow, qApp
from PySide.QtGui import QGraphicsView, QGraphicsScene, QWidget, QGridLayout
from PySide.QtGui import QPainter, QPen, QColor, QPixmap, QBrush
from PySide.QtGui import QSlider, QFormLayout, QVBoxLayout, QHBoxLayout
from PySide.QtGui import QLineEdit, QToolButton, QPushButton, QRadioButton
from PySide.QtGui import QAction, QMenu
from PySide.QtNetwork import QNetworkConfigurationManager, QNetworkConfiguration
from PySide.QtNetwork import QNetworkSession

from QtMobility.Location import QGeoServiceProvider, QGraphicsGeoMap, QGeoMapPolylineObject
from QtMobility.Location import QGeoCoordinate, QGeoMapRectangleObject, QGeoMapPixmapObject
from QtMobility.Location import QGeoMapPolygonObject, QGeoMapCircleObject, QGeoMapTextObject
from QtMobility.Location import QGeoMapRouteObject, QGeoRouteRequest

MARKER_HEIGHT = 36
MARKER_WIDTH = 25
MARKER_PIN_LEN = 10

ENABLE_KINETIC_PANNING = True
KINETIC_PANNING_HALFLIFE = 300.0
PAN_SPEED_NORMAL = 0.3
PAN_SPEED_FAST = 1.0
KINETIC_PAN_SPEED_THRESHOLD = 0.005
KINETIC_PANNING_RESOLUTION = 30
HOLD_TIME_THRESHOLD = 500

class MouseHistoryEntry(object):

    def __init__(self, position=None, time=None):
        self.position = position
        self.time = time

class MapWidget(QGraphicsGeoMap):

    coordQueryResult = Signal(QGeoCoordinate)

    def __init__(self, manager):
        QGraphicsGeoMap.__init__(self, manager)

        self.coordQueryState = False
        self.panActive = False
        self.kineticTimer = QTimer()
        self.lastCircle = None
        self.lastMoveTime = None
        self.kineticPanSpeed = None
        self.panDecellerate = True
        self.remainingPan = QPointF()

        self.mouseHistory = deque([MouseHistoryEntry() for i in range(5)])

        self.kineticTimer.timeout.connect(self.kineticTimerEvent)
        self.kineticTimer.setInterval(KINETIC_PANNING_RESOLUTION)

    def setMouseClickCoordQuery(self, state):
        self.coordQueryState = state

    def mousePressEvent(self, event):
        self.setFocus()

        if event.button() == Qt.LeftButton:
            if event.modifiers() & Qt.ControlModifier:
                pass
            else:
                if self.coordQueryState:
                    self.coordQueryResult.emit(self.screenPositionToCoordinate(event.lastPos()))
                    return

                self.panActive = True

                self.kineticTimer.stop()
                self.kineticPanSpeed = QPointF()
                self.lastMoveTime = QTime.currentTime()

        event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.panActive:
                self.panActive = False

                if not ENABLE_KINETIC_PANNING or self.lastMoveTime.msecsTo(QTime.currentTime()) > HOLD_TIME_THRESHOLD:
                    return

                self.kineticPanSpeed = QPointF()
                entriesConsidered = 0

                currentTime = QTime.currentTime()

                for entry in self.mouseHistory:
                    if not entry.time:
                        continue

                    if entry.time.msecsTo(currentTime) < HOLD_TIME_THRESHOLD:
                        self.kineticPanSpeed += entry.position
                        entriesConsidered += 1

                if entriesConsidered > 0:
                    self.kineticPanSpeed /= entriesConsidered

                self.lastMoveTime = currentTime

                self.kineticTimer.start()
                self.panDecellerate = True

        event.accept()

    def mouseMoveEvent(self, event):
        if event.modifiers() & Qt.ControlModifier:
            if self.lastCircle:
                self.lastCircle.setCenter(self.screenPositionToCoordinate(event.pos()))
        elif self.panActive:
            currentTime = QTime.currentTime()
            deltaTime = self.lastMoveTime.msecsTo(currentTime)

            delta = event.lastPos() - event.pos()

            if deltaTime > 0:
                self.kineticPanSpeed = delta / deltaTime

                self.mouseHistory.popleft()
                self.mouseHistory.append(MouseHistoryEntry(self.kineticPanSpeed, currentTime))

            self.panFloatWrapper(delta)

        event.accept()

    def kineticTimerEvent(self):

        currentTime = QTime.currentTime()

        deltaTime = self.lastMoveTime.msecsTo(currentTime)
        self.lastMoveTime = currentTime

        if self.panDecellerate:
            self.kineticPanSpeed *= pow(0.5, float(deltaTime / KINETIC_PANNING_HALFLIFE))

        scaledSpeed = self.kineticPanSpeed * deltaTime

        if self.kineticPanSpeed.manhattanLength() < KINETIC_PAN_SPEED_THRESHOLD:
            self.kineticTimer.stop()
            return
        self.panFloatWrapper(scaledSpeed)

    def panFloatWrapper(self, delta):

        self.remainingPan += delta
        move = self.remainingPan.toPoint()
        self.pan(move.x(), move.y())
        self.remainingPan -= move

    def mouseDoubleClickEvent(self, event):

        self.setFocus()

        self.pan(event.lastPos().x() - self.size().width() / 2.0, event.lastPos().y() - self.size().height() / 2.0)

        if self.zoomLevel() < self.maximumZoomLevel():
            self.setZoomLevel(self.zoomLevel() + 1)

        event.accept()

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Minus:
            if self.zoomLevel() > self.minimumZoomLevel():
                self.setZoomLevel(self.zoomLevel() - 1)
        elif event.key() == Qt.Key_Plus:
            if self.zoomLevel() < self.maximumZoomLevel():
                self.setZoomLevel(self.zoomLevel() + 1)
        elif event.key() == Qt.Key_T:
            if self.mapType() == QGraphicsGeoMap.StreetMap:
                self.setMapType(QGraphicsGeoMap.SatelliteMapDay)
            elif self.mapType() == QGraphicsGeoMap.SatelliteMapDay:
                self.setMapType(QGraphicsGeoMap.StreetMap)

        event.accept()

    def wheelEvent(self, event):

        if event.delta() > 0:
            if self.zoomLevel() < self.maximumZoomLevel():
                self.setZoomLevel(self.zoomLevel() + 1)
        else:
            if self.zoomLevel() > self.minimumZoomLevel():
                self.setZoomLevel(self.zoomLevel() - 1)

        event.accept()

class MainWindow(QMainWindow):
    """docstring for MainWindow"""
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.serviceProvider = 0
        self.popupMenu = None
        self.mapControlButtons = []
        self.mapControlTypes = []
        self.markerObjects = []
        self.setWindowTitle(self.tr('Map Viewer Demo'))

        self.routingManager = None
        self.mapManager = None
        self.mapWidget = None
        self.markerIcon = None
        self.slider = None

        manager = QNetworkConfigurationManager()

        canStartIAP = manager.capabilities() & QNetworkConfigurationManager.CanStartAndStopInterfaces

        configuration = manager.defaultConfiguration()

        if not configuration.isValid or (not canStartIAP and configuration.starte() != QNetworkConfiguration.Active):
            QMessageBox.information(self, self.tr('Map Viewer Demo'),
                                    self.tr('Available Access Points not found.'))
            return

        self.session = QNetworkSession(configuration, self)
        self.session.opened.connect(self.networkSessionOpened)
        self.session.error.connect(self.error)

        self.session.open()
        self.session.waitForOpened()

        self.setProvider('nokia')
        self.setupUi()

    def networkSessionOpened(self):
        pass

    def sliderValueChanged(self, value):
        self.mapWidget.setZoomLevel(value)

    def mapZoomLevelChanged(self, level):
        self.slider.setSliderPosition(int(level))

    def mapTypeChanged(self, newType):
        index = self.mapControlTypes.index(newType)
        if index != -1:
            self.mapControButtons[index].setChecked(True)

    def mapTypeToggled(self, checked):
        if checked:
            button = self.sender()
            index = self.mapControlButtons.index(button)
            if index != -1:
                print index, self.mapControlTypes[index]
                self.mapWidget.setMapType(self.mapControlTypes[index])

    def updateCoords(self, coords):
        if not coords.isValid():
            return

        self.latitudeEdit.setText('%f' % coords.latitude())
        self.longitudeEdit.setText('%f' % coords.longitude())

    def setCoordsClicked(self):
        lat = float(self.latitudeEdit.text())
        lon = float(self.longitudeEdit.text())
        self.mapWidget.setCenter(QGeoCoordinate(lat, lon))

    def setProvider(self, providerId):
        self.serviceProvider = QGeoServiceProvider(providerId)
        if self.serviceProvider.error() != QGeoServiceProvider.NoError:
            QMessageBox.information(self, self.tr('MapViewer Example'),
                                    self.tr('Unable to dinf the %s geoservices plugin.' % providerId))

            qApp.quit()
            return

        self.mapManager = self.serviceProvider.mappingManager()
        self.routingManager = self.serviceProvider.routingManager()

    def error(self, error):
        if error == QNetworkSession.UnknownSessionError:
            msgBox = QMessageBox(self.parent())
            msgBox.setText('This application requires network access to function.')
            msgBox.setInformativeText('Press Cancel to quit the application.')
            msgBox.setStandardButtons(QMessageBox.Retry | QMessageBox.Cancel)
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setDefaultButton(QMessageBox.Retry)
            ret = msgBox.exec_()
            if ret == QMessageBox.Retry:
                QTimer.singleShot(0, self.session.open)
            elif ret == QMessageBox.Cancel:
                self.close()
        elif error == QNetworkSession.SessionAbortedError:
            msgBox = QMessageBox(self.parent())
            msgBox.setText('Out of range of network')
            msgBox.setInformativeText('Move back into range and press Retry, or press Cancel to quit the application')
            msgBox.setStandardButtons(QMessageBox.Retry | QMessageBox.Cancel)
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setDefaultButton(QMessageBox.Retry)
            ret = msgBox.exec_()
            if ret == QMessageBox.Retry:
                QTimer.singleShot(0, self.session.open)
            elif ret == QMessageBox.Cancel:
                self.close()


    def setupUi(self):

        scene = QGraphicsScene(self)
        self.view = QGraphicsView(scene, self)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVisible(True)
        self.view.setInteractive(True)

        self.createPixmapIcon()

        self.mapWidget = MapWidget(self.mapManager)
        scene.addItem(self.mapWidget)
        self.mapWidget.setCenter(QGeoCoordinate(-8.1, -34.95))
        self.mapWidget.setZoomLevel(5)

        #...
        self.slider = QSlider(Qt.Vertical, self)
        self.slider.setTickInterval(1)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.setMaximum(self.mapManager.maximumZoomLevel())
        self.slider.setMinimum(self.mapManager.minimumZoomLevel())

        self.slider.valueChanged[int].connect(self.sliderValueChanged)
        self.mapWidget.zoomLevelChanged[float].connect(self.mapZoomLevelChanged)

        mapControlLayout = QVBoxLayout()

        self.mapWidget.mapTypeChanged.connect(self.mapTypeChanged)

        for mapType in self.mapWidget.supportedMapTypes():
            radio = QRadioButton(self)
            if mapType == QGraphicsGeoMap.StreetMap:
                radio.setText('Street')
            elif mapType == QGraphicsGeoMap.SatelliteMapDay:
                radio.setText('Sattelite')
            elif mapType == QGraphicsGeoMap.SatelliteMapNight:
                radio.setText('Sattelite - Night')
            elif mapType == QGraphicsGeoMap.TerrainMap:
                radio.setText('Terrain')

            if mapType == self.mapWidget.mapType():
                radio.setChecked(True)

            radio.toggled[bool].connect(self.mapTypeToggled)

            self.mapControlButtons.append(radio)
            self.mapControlTypes.append(mapType)
            mapControlLayout.addWidget(radio)

        self.latitudeEdit = QLineEdit()
        self.longitudeEdit = QLineEdit()

        formLayout = QFormLayout()
        formLayout.addRow('Latitude', self.latitudeEdit)
        formLayout.addRow('Longitude', self.longitudeEdit)

        self.captureCoordsButton = QToolButton()
        self.captureCoordsButton.setText('Capture coordinates')
        self.captureCoordsButton.setCheckable(True)

        self.captureCoordsButton.toggled[bool].connect(
                self.mapWidget.setMouseClickCoordQuery)
        self.mapWidget.coordQueryResult.connect(self.updateCoords)

        self.setCoordsButton = QPushButton()
        self.setCoordsButton.setText('Set coordinates')
        self.setCoordsButton.clicked.connect(self.setCoordsClicked)

        buttonLayout = QHBoxLayout()

        buttonLayout.addWidget(self.captureCoordsButton)
        buttonLayout.addWidget(self.setCoordsButton)

        coordControlLayout = QVBoxLayout()
        coordControlLayout.addLayout(formLayout)
        coordControlLayout.addLayout(buttonLayout)

        widget = QWidget(self)
        layout = QGridLayout()
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 0)

        topLayout = QGridLayout()
        bottomLayout = QGridLayout()

        topLayout.setColumnStretch(0, 0)
        topLayout.setColumnStretch(1, 1)

        bottomLayout.setColumnStretch(0, 0)
        bottomLayout.setColumnStretch(1, 1)

        topLayout.addWidget(self.slider, 0, 0)
        topLayout.addWidget(self.view, 0, 1)

        bottomLayout.addLayout(mapControlLayout, 0, 0)
        bottomLayout.addLayout(coordControlLayout, 0, 1)

        layout.addLayout(topLayout, 0, 0)
        layout.addLayout(bottomLayout, 1, 0)

        self.layout = layout
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.view.setContextMenuPolicy(Qt.CustomContextMenu)

        self.view.customContextMenuRequested.connect(self.customContextMenuRequest)

    def createPixmapIcon(self):
        self.markerIcon = QPixmap(MARKER_WIDTH, MARKER_HEIGHT)
        self.markerIcon.fill(Qt.transparent)

        painter = QPainter(self.markerIcon)

        p1 = QPoint(MARKER_WIDTH / 2, MARKER_HEIGHT - 1)
        p2 = QPoint(MARKER_WIDTH / 2, MARKER_HEIGHT - 1 - MARKER_PIN_LEN)
        pen = QPen(Qt.black)
        pen.setWidth(2)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.drawLine(p1, p2)
        ellipse = QRect(0, 0, MARKER_WIDTH - 1, MARKER_HEIGHT - 1)
        pen.setWidth(1)
        painter.setPen(pen)
        color = QColor(Qt.green)
        color.setAlpha(127)
        brush = QBrush(color)
        painter.setBrush(brush)
        painter.drawEllipse(ellipse)

    def resizeEvent(self, event):
        self.view.setSceneRect(QRectF(QPointF(0.0, 0.0), self.view.size()))
        self.mapWidget.resize(self.view.size())

    def showEvent(self, event):
        self.view.setSceneRect(QRectF(QPointF(0.0, 0.0), self.view.size()))
        self.mapWidget.resize(self.view.size())

    def createMenus(self):
        self.popupMenu = QMenu(self)

        # Markers
        subMenuItem = QMenu(self.tr('Marker'), self)
        self.popupMenu.addMenu(subMenuItem)

        menuItem = QAction(self.tr('Set marker'), self)
        subMenuItem.addAction(menuItem)
        menuItem.triggered[bool].connect(self.drawPixmap)

        menuItem = QAction(self.tr('Remove marker'), self)
        subMenuItem.addAction(menuItem)
        menuItem.triggered[bool].connect(self.removePixmaps)

        menuItem = QAction(self.tr('Select objects'), self)
        subMenuItem.addAction(menuItem)
        menuItem.triggered[bool].connect(self.selectObjects)

        # Draw
        subMenuItem = QMenu(self.tr('Draw'), self)
        self.popupMenu.addMenu(subMenuItem)

        menuItem = QAction(self.tr('Rectangle'), self)
        subMenuItem.addAction(menuItem)
        menuItem.triggered[bool].connect(self.drawRect)

        menuItem = QAction(self.tr('Polyline'), self)
        subMenuItem.addAction(menuItem)
        menuItem.triggered[bool].connect(self.drawPolyline)

        menuItem = QAction(self.tr('Polygon'), self)
        subMenuItem.addAction(menuItem)
        menuItem.triggered[bool].connect(self.drawPolygon)

        menuItem = QAction(self.tr('Circle'), self)
        subMenuItem.addAction(menuItem)
        menuItem.triggered[bool].connect(self.drawCircle)

        menuItem = QAction(self.tr('Text'), self)
        subMenuItem.addAction(menuItem)
        menuItem.triggered[bool].connect(self.drawText)

        # Routing
        subMenuItem = QMenu(self.tr('Route'), self)
        self.popupMenu.addMenu(subMenuItem)

        menuItem = QAction(self.tr('Calculate route'), self)
        subMenuItem.addAction(menuItem)
        menuItem.triggered[bool].connect(self.calculateRoute)

    def selectObjects(self):
        for obj in self.mapWidget.mapObjects():
            obj.setSelected(False)

        if len(self.markerObjects) < 2:
            return

        bottomRight = self.markerObjects.pop()
        topLeft = self.markerObjects.pop()

        self.mapWidget.removeMapObject(topLeft)
        self.mapWidget.removeMapObject(bottomRight)

        selectedObjects = self.mapWidget.mapObjectsInScreenRect(
                    QRectF(self.mapWidget.coordinateToScreenPosition(topLeft.coordinate()),
                           self.mapWidget.coordinateToScreenPosition(bottomRight.coordinate()))
                )

        for obj in selectedObjects:
            obj.setSelected(True)

    def drawRect(self):
        if len(self.markerObjects) < 2:
            return

        p1, p2 = self.markerObjects[:2]

        pen = QPen(Qt.white)
        pen.setWidth(2)
        pen.setCosmetic(True)
        fill = QColor(Qt.black)
        fill.setAlpha(65)
        rectangle = QGeoMapRectangleObject(p1.coordinate(), p2.coordinate())
        rectangle.setPen(pen)
        rectangle.setBrush(QBrush(fill))
        self.mapWidget.addMapObject(rectangle)

    def drawPolyline(self):
        path = [mark.coordinate() for mark in self.markerObjects]

        pen = QPen(Qt.white)
        pen.setWidth(2)
        pen.setCosmetic(True)
        polyline = QGeoMapPolylineObject()
        polyline.setPen(pen)
        polyline.setPath(path)

        self.mapWidget.addMapObject(polyline)

    def drawPolygon(self):
        path = [mark.coordinate() for mark in self.markerObjects]

        pen = QPen(Qt.white)
        pen.setWidth(2)
        pen.setCosmetic(True)
        polygon = QGeoMapPolygonObject()
        polygon.setPen(pen)
        fill = QColor(Qt.black)
        fill.setAlpha(65)
        polygon.setBrush(QBrush(fill))
        polygon.setPath(path)

        self.mapWidget.addMapObject(polygon)

    def drawCircle(self):

        if not len(self.markerObjects):
            return

        p1 = self.markerObjects[0]
        center = p1.coordinate()

        radius = 3000 # Meters

        if len(self.markerObjects) >= 2:
            radius = center.distanceTo(self.markerObjects[1].coordinate())

        pen = QPen(Qt.white)
        pen.setWidth(2)
        pen.setCosmetic(True)
        circle = QGeoMapCircleObject(center, radius)
        circle.setPen(pen)
        fill = QColor(Qt.black)
        fill.setAlpha(65)
        circle.setBrush(QBrush(fill))

        self.mapWidget.addMapObject(circle)

    def drawText(self):

        if not len(self.markerObjects):
            return

        start = self.markerObjects[0].coordinate()

        text = QGeoMapTextObject(start, 'Text')

        fill = QColor(Qt.black)
        text.setBrush(fill)
        self.mapWidget.addMapObject(text)

    def calculateRoute(self):
        if len(self.markerObjects) < 2:
            return

        waypoints = [x.coordinate() for x in self.markerObjects[:2]]

        request = QGeoRouteRequest(waypoints)
        self.routeReply = self.routingManager.calculateRoute(request)
        self.routeReply.finished.connect(self.routeFinished)

    def routeFinished(self):

        if not self.routeReply.routes():
            return

        route = QGeoMapRouteObject(self.routeReply.routes()[0])
        routeColor = QColor(Qt.blue)
        routeColor.setAlpha(127)
        pen = QPen(routeColor)
        pen.setWidth(7)
        pen.setCosmetic(True)
        pen.setCapStyle(Qt.RoundCap)
        route.setPen(pen)
        self.mapWidget.addMapObject(route)

    def drawPixmap(self):
        marker = QGeoMapPixmapObject(self.mapWidget.screenPositionToCoordinate(self.lastClicked),
                                    QPoint(-(MARKER_WIDTH / 2), -MARKER_HEIGHT), self.markerIcon)
        self.mapWidget.addMapObject(marker)
        self.markerObjects.append(marker)

    def removePixmaps(self):
        for i in range(len(self.markerObjects)):
            marker = self.markerObjects.pop()

            self.mapWidget.removeMapObject(marker)
            marker.deleteLater()

    def customContextMenuRequest(self, point):
        self.lastClicked = point
        if self.focusWidget() == self.view:
            if not self.popupMenu:
                self.createMenus()

            self.popupMenu.popup(self.view.mapToGlobal(self.lastClicked))

def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.showMaximized()

    return app.exec_()

if __name__ == '__main__':
    main()
