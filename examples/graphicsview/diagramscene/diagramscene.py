#!/usr/bin/env python

import sys
import math
from PySide import QtCore, QtGui

import diagramscene_rc


class Arrow(QtGui.QGraphicsLineItem):
    def __init__(self, startItem, endItem, parent=None, scene=None):
        QtGui.QGraphicsLineItem.__init__(self, parent, scene)

        self.myStartItem = startItem
        self.myEndItem = endItem
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
        self.myColor = QtCore.Qt.black
        self.setPen(QtGui.QPen(self.myColor, 2, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
        self.arrowHead = QtGui.QPolygonF()

    def setColor(self, color):
        self.myColor = color

    def boundingRect(self):
        extra = (self.pen().width() + 20) / 2.0
        p1 = self.line().p1()
        p2 = self.line().p2()
        return QtCore.QRectF(p1, QtCore.QSizeF(p2.x() - p1.x(), p2.y() - p1.y())).normalized().adjusted(-extra, -extra, extra, extra)

    def shape(self):
        path = QtGui.QGraphicsLineItem.shape(self)
        path.addPolygon(self.arrowHead)
        return path

    def updatePosition(self):
        line = QtCore.QLineF(self.mapFromItem(self.myStartItem, 0, 0), self.mapFromItem(self.myEndItem, 0, 0))
        self.setLine(line)

    def paint(self, painter, option, widget=None):
        if (self.myStartItem.collidesWithItem(self.myEndItem)):
            return

        myStartItem = self.myStartItem
        myEndItem = self.myEndItem
        myColor = self.myColor
        myPen = self.pen()
        myPen.setColor(self.myColor)
        arrowSize = 20.0
        painter.setPen(myPen)
        painter.setBrush(self.myColor)

        centerLine = QtCore.QLineF(myStartItem.pos(), myEndItem.pos())
        endPolygon = myEndItem.polygon()
        p1 = endPolygon[0] + myEndItem.pos()

        intersectPoint = QtCore.QPointF()
        for i in endPolygon:
            p2 = i + myEndItem.pos()
            polyLine = QtCore.QLineF(p1, p2)
            (intersectType, intersectPoint) = polyLine.intersect(centerLine)
            if intersectType == QtCore.QLineF.BoundedIntersection:
                break
            p1 = p2

        self.setLine(QtCore.QLineF(intersectPoint, myStartItem.pos()))
        line = self.line()

        angle = math.acos(line.dx() / line.length())
        if line.dy() >= 0:
            angle = (math.pi * 2.0) - angle

        arrowP1 = line.p1() + QtCore.QPointF(math.sin(angle + math.pi / 3.0) * arrowSize,
                                        math.cos(angle + math.pi / 3) * arrowSize)
        arrowP2 = line.p1() + QtCore.QPointF(math.sin(angle + math.pi - math.pi / 3.0) * arrowSize,
                                        math.cos(angle + math.pi - math.pi / 3.0) * arrowSize)

        self.arrowHead.clear()
        for point in [line.p1(), arrowP1, arrowP2]:
            self.arrowHead.append(point)

        painter.drawLine(line)
        painter.drawPolygon(self.arrowHead)
        if self.isSelected():
            painter.setPen(QtGui.QPen(myColor, 1, QtCore.Qt.DashLine))
            myLine = QtCore.QLineF(line)
            myLine.translate(0, 4.0)
            painter.drawLine(myLine)
            myLine.translate(0,-8.0)
            painter.drawLine(myLine)


class DiagramTextItem(QtGui.QGraphicsTextItem):
    def __init__(self, parent=None, scene=None):
        QtGui.QGraphicsTextItem.__init__(self, parent, scene)

        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)

    def itemChange(self, change, value):
        if (change == QtGui.QGraphicsItem.ItemSelectedChange):
            self.emit(QtCore.SIGNAL("selectedChange"), self)
        return value

    def focusOutEvent(self, event):
        self.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.emit(QtCore.SIGNAL("lostFocus"), self)
        QtGui.QGraphicsTextItem.focusOutEvent(self, event)

    def mousePressEvent(self, event):
        self.scene().clearSelection()
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        QtGui.QGraphicsTextItem.mousePressEvent(self, event)
        self.setSelected(True)

    def mouseMoveEvent(self, event):
        if self.textInteractionFlags() & QtCore.Qt.TextEditable:
            QtGui.QGraphicsTextItem.mouseMoveEvent(self, event)
        else:
            QtGui.QGraphicsItem.mouseMoveEvent(self, event)

    def mouseDoubleClickEvent(self, event):
        self.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction) == False
        mouseEvent = QtGui.QGraphicsSceneMouseEvent(QtCore.QEvent.GraphicsSceneMousePress)
        mouseEvent.setAccepted(True)
        mouseEvent.setPos(event.pos())
        mouseEvent.setScenePos(event.scenePos())
        mouseEvent.setScreenPos(event.screenPos())
        mouseEvent.setButtonDownPos(QtCore.Qt.LeftButton,
            event.buttonDownPos(QtCore.Qt.LeftButton))
        mouseEvent.setButtonDownScreenPos(QtCore.Qt.LeftButton,
            event.buttonDownScreenPos(QtCore.Qt.LeftButton))
        mouseEvent.setButtonDownScenePos(QtCore.Qt.LeftButton,
            event.buttonDownScenePos(QtCore.Qt.LeftButton))
        mouseEvent.setWidget(event.widget())

        QtGui.QGraphicsTextItem.mousePressEvent(self, mouseEvent)

        mouseEvent = None


class DiagramItem(QtGui.QGraphicsPolygonItem):
    Step, Conditional, StartEnd, Io = range(4)

    def __init__(self, diagramType, contextMenu, parent=None, scene=None):
        QtGui.QGraphicsPolygonItem.__init__(self, parent, scene)

        self.diagramType = diagramType
        self.contextMenu = contextMenu

        path = QtGui.QPainterPath()
        if self.diagramType == self.StartEnd:
            path.moveTo(200, 50)
            path.arcTo(150, 0, 50, 50, 0, 90)
            path.arcTo(50, 0, 50, 50, 90, 90)
            path.arcTo(50, 50, 50, 50, 180, 90)
            path.arcTo(150, 50, 50, 50, 270, 90)
            path.lineTo(200, 25)
            myPolygon = path.toFillPolygon()
        elif self.diagramType == self.Conditional:
            myPolygon = QtGui.QPolygonF([
                    QtCore.QPointF(-100, 0), QtCore.QPointF(0, 100),
                    QtCore.QPointF(100, 0), QtCore.QPointF(0, -100),
                    QtCore.QPointF(-100, 0)])
        elif self.diagramType == self.Step:
            myPolygon = QtGui.QPolygonF([
                    QtCore.QPointF(-100, -100), QtCore.QPointF(100, -100),
                    QtCore.QPointF(100, 100), QtCore.QPointF(-100, 100),
                    QtCore.QPointF(-100, -100)])
        else:
            myPolygon = QtGui.QPolygonF([
                    QtCore.QPointF(-120, -80), QtCore.QPointF(-70, 80),
                    QtCore.QPointF(120, 80), QtCore.QPointF(70, -80),
                    QtCore.QPointF(-120, -80)])
        self.setPolygon(myPolygon)
        self.myPolygon = myPolygon

        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
        self.arrows = []

    def image(self):
        pixmap = QtGui.QPixmap(250, 250)
        pixmap.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(pixmap)
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 8))
        painter.translate(125, 125)
        painter.drawPolyline(self.myPolygon)
        return pixmap

    def removeArrow(self, arrow):
        if arrow in self.arrows:
            self.arrows.remove(arrow)

    def removeArrows(self):
        for arrow in self.arrows:
            arrow.startItem().removeArrow(arrow)
            arrow.endItem().removeArrow(arrow)
            self.scene().removeItem(arrow)

    def addArrow(self, arrow):
        self.arrows.append(arrow)

    def contextMenuEvent(self, event):
        self.scene().clearSelection()
        self.setSelected(True)

    def itemChange(self, change, value):
        if change == QtGui.QGraphicsItem.ItemPositionChange:
            for arrow in self.arrows:
                arrow.updatePosition()
        return QtCore.QVariant(value)


class DiagramScene(QtGui.QGraphicsScene):
    InsertItem, InsertLine, InsertText, MoveItem  = range(4)

    def __init__(self, itemMenu, parent=None):
        QtGui.QGraphicsScene.__init__(self, parent)

        self.myItemMenu = itemMenu
        self.myMode = self.MoveItem
        self.myItemType = DiagramItem.Step
        self.line = None
        self.textItem = None
        self.myItemColor = QtCore.Qt.white
        self.myTextColor = QtCore.Qt.black
        self.myLineColor = QtCore.Qt.black
        self.myFont = QtGui.QFont()

    def setLineColor(self, color):
        self.myLineColor = color
        if self.isItemChange(Arrow):
            item = self.selectedItems()[0]
            item.setColor(self.myLineColor)
            self.update()

    def setTextColor(self, color):
        self.myTextColor = color
        if self.isItemChange(DiagramTextItem):
            item = self.selectedItems()[0]
            item.setDefaultTextColor(myTextColor)

    def setItemColor(self, color):
        self.myItemColor = color
        if self.isItemChange(DiagramItem):
            item = self.selectedItems()[0]
            item.setBrush(self.myItemColor)

    def setFont(self, font):
        self.myFont = font
        if self.isItemChange(DiagramTextItem):
            item = self.selectedItems()[0]
            item.setFont(self.myFont)

    def setMode(self, mode):
        self.myMode = mode

    def setItemType(self, type):
        self.myItemType = type

    def editorLostFocus(self, item):
        cursor = item.textCursor()
        cursor.clearSelection()
        item.setTextCursor(cursor)
        if item.toPlainText().isEmpty():
            self.removeItem(item)
            item.deleteLater()

    def mousePressEvent(self, mouseEvent):
        if (mouseEvent.button() != QtCore.Qt.LeftButton):
            return

        if self.myMode == self.InsertItem:
            item = DiagramItem(self.myItemType, self.myItemMenu)
            item.setBrush(self.myItemColor)
            self.addItem(item)
            item.setPos(mouseEvent.scenePos())
            self.emit(QtCore.SIGNAL("itemInserted"), item)
        elif self.myMode == self.InsertLine:
            self.line = QtGui.QGraphicsLineItem(QtCore.QLineF(mouseEvent.scenePos(),
                                        mouseEvent.scenePos()))
            self.line.setPen(QtGui.QPen(self.myLineColor, 2))
            self.addItem(self.line)
        elif self.myMode == self.InsertText:
            textItem = DiagramTextItem()
            textItem.setFont(self.myFont)
            textItem.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
            textItem.setZValue(1000.0)
            self.connect(textItem, QtCore.SIGNAL("lostFocus"),
                    self.editorLostFocus)
            self.connect(textItem, QtCore.SIGNAL("selectedChange"),
                    self, QtCore.SIGNAL("itemSelected(QGraphicsItem *)"))
            self.addItem(textItem)
            textItem.setDefaultTextColor(self.myTextColor)
            textItem.setPos(mouseEvent.scenePos())
            self.emit(QtCore.SIGNAL("textInserted"), textItem)

        QtGui.QGraphicsScene.mousePressEvent(self, mouseEvent)

    def mouseMoveEvent(self, mouseEvent):
        if self.myMode == self.InsertLine and self.line:
            newLine = QtCore.QLineF(self.line.line().p1(), mouseEvent.scenePos())
            self.line.setLine(newLine)
        elif self.myMode == self.MoveItem:
            QtGui.QGraphicsScene.mouseMoveEvent(self, mouseEvent)

    def mouseReleaseEvent(self, mouseEvent):
        if (self.line and self.myMode == self.InsertLine):
            startItems = self.items(self.line.line().p1())
            if len(startItems) and startItems[0] == self.line:
                startItems.pop(0)
            endItems = self.items(self.line.line().p2())
            if len(endItems) and endItems[0] == self.line:
                endItems.pop(0)

            self.removeItem(self.line)
            self.line = None

            if len(startItems) and len(endItems) and \
                    isinstance(startItems[0], DiagramItem) and \
                    isinstance(endItems[0], DiagramItem) and \
                    startItems[0] != endItems[0]:
                startItem = startItems[0]
                endItem = endItems[0]
                arrow = Arrow(startItem, endItem)
                arrow.setColor(self.myLineColor)
                startItem.addArrow(arrow)
                endItem.addArrow(arrow)
                arrow.setZValue(-1000.0)
                self.addItem(arrow)
                arrow.updatePosition()

        self.line = None
        QtGui.QGraphicsScene.mouseReleaseEvent(self, mouseEvent)

    def isItemChange(self, type):
        for item in self.selectedItems():
            if isinstance(item, type):
                return True
        return False


InsertTextButton = 10

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.createActions()
        self.createMenus()
        self.createToolBox()

        scene = DiagramScene(self.itemMenu)
        scene.setSceneRect(QtCore.QRectF(0, 0, 5000, 5000))
        self.connect(scene, QtCore.SIGNAL("itemInserted"), self.itemInserted)
        self.connect(scene, QtCore.SIGNAL("textInserted(QGraphicsTextItem *)"),
                self.textInserted)
        self.connect(scene, QtCore.SIGNAL("itemSelected(QGraphicsItem *)"),
                self.itemSelected)
        self.scene = scene

        self.createToolbars()

        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.toolBox)
        self.view = QtGui.QGraphicsView(self.scene)
        self.view.setRenderHints(QtGui.QPainter.Antialiasing)
        layout.addWidget(self.view)

        self.widget = QtGui.QWidget()
        self.widget.setLayout(layout)

        self.setCentralWidget(self.widget)
        self.setWindowTitle("Diagramscene")

    ## slots
    def backgroundButtonGroupClicked(self, button):
        buttons = self.backgroundButtonGroup.buttons()
        for myButton in buttons:
            if myButton != button:
                button.setChecked(False)

        text = button.text()
        if text == "Blue Grid":
            self.scene.setBackgroundBrush(QtGui.QBrush(QtGui.QPixmap(":/images/background1.png")))
        elif text == "White Grid":
            self.scene.setBackgroundBrush(QtGui.QBrush(QtGui.QPixmap(":/images/background2.png")))
        elif text == "Gray Grid":
            self.scene.setBackgroundBrush(QtGui.QBrush(QtGui.QPixmap(":/images/background3.png")))
        else:
            self.scene.setBackgroundBrush(QtGui.QBrush(QtGui.QPixmap(":/images/background4.png")))

        self.scene.update()
        self.view.update()

    def buttonGroupClicked(self, id):
        buttons = self.buttonGroup.buttons()
        for button in buttons:
            if self.buttonGroup.button(id) != button:
                button.setChecked(False)

        if id == InsertTextButton:
            self.scene.setMode(DiagramScene.InsertText)
        else:
            self.scene.setItemType(id)
            self.scene.setMode(DiagramScene.InsertItem)

    def deleteItem(self):
        for item in self.scene.selectedItems():
            if isinstance(item, DiagramItem):
                item.removeArrows()
            self.scene.removeItem(item)

    def pointerGroupClicked(self, i):
        self.scene.setMode(self.pointerTypeGroup.checkedId())

    def bringToFront(self):
        if scene.selectedItems().isEmpty():
            return

        selectedItem = self.scene.selectedItems().first()
        overlapItems = selectedItem.collidingItems()

        zValue = 0
        for item in overlapItems:
            if (item.zValue() >= zValue and
                isinstance(item, DiagramItem)):
                zValue = item.zValue() + 0.1
        selectedItem.setZValue(zValue)

    def sendToBack(self):
        if scene.selectedItems().isEmpty():
            return

        selectedItem = self.scene.selectedItems().first()
        overlapItems = selectedItem.collidingItems()

        zValue = 0
        for item in overlapItems:
            if (item.zValue() <= zValue and
                isinstance(item, DiagramItem)):
                zValue = item.zValue() - 0.1
        selectedItem.setZValue(zValue)

    def itemInserted(self, item):
        self.scene.setMode(self.pointerTypeGroup.checkedId())
        self.buttonGroup.button(item.diagramType).setChecked(False)

    def textInserted(self, item):
        self.buttonGroup.button(InsertTextButton).setChecked(False)
        self.scene.setMode(pointerTypeGroup.checkedId())

    def currentFontChanged(self, font):
        self.handleFontChange()

    def fontSizeChanged(self, font):
        self.handleFontChange()

    def sceneScaleChanged(self, scale):
        newScale = scale.left(scale.indexOf("%")).toDouble()[0] / 100.0
        oldMatrix = self.view.matrix()
        self.view.resetMatrix()
        self.view.translate(oldMatrix.dx(), oldMatrix.dy())
        self.view.scale(newScale, newScale)

    def textColorChanged(self):
        self.textAction = self.sender()
        self.fontColorToolButton.setIcon(self.createColorToolButtonIcon(
                    ":/images/textpointer.png",
                    QtGui.QColor(self.textAction.data())))
        self.textButtonTriggered()

    def itemColorChanged(self):
        self.fillAction = self.sender()
        self.fillColorToolButton.setIcon(self.createColorToolButtonIcon(
                    ":/images/floodfill.png",
                    QtGui.QColor(self.fillAction.data())))
        self.fillButtonTriggered()

    def lineColorChanged(self):
        self.lineAction = self.sender()
        self.lineColorToolButton.setIcon(self.createColorToolButtonIcon(
                    ":/images/linecolor.png",
                    QtGui.QColor(self.lineAction.data())))
        self.lineButtonTriggered()

    def textButtonTriggered(self):
        self.scene.setTextColor(QtGui.QColor(self.textAction.data()))

    def fillButtonTriggered(self):
        self.scene.setItemColor(QtGui.QColor(self.fillAction.data()))

    def lineButtonTriggered(self):
        self.scene.setLineColor(QtGui.QColor(self.lineAction.data()))

    def handleFontChange(self):
        font = self.fontCombo.currentFont()
        font.setPointSize(self.fontSizeCombo.currentText().toInt()[0])
        if self.boldAction.isChecked():
            font.setWeight = QtGui.QFont.Bold
        else:
            font.setWeight = QtGui.QFont.Normal
        font.setItalic(self.italicAction.isChecked())
        font.setUnderline(self.underlineAction.isChecked())

        self.scene.setFont(font)

    def itemSelected(self, item):
        font = item.font()
        color = item.defaultTextColor()
        self.fontCombo.setCurrentFont(font)
        self.fontSizeCombo.setEditText(QString.number(font.pointSize()))
        self.boldAction.setChecked(font.weight() == QtGui.QFont.Bold)
        self.italicAction.setChecked(font.italic())
        self.underlineAction.setChecked(font.underline())

    def about(self):
        QtGui.QMessageBox.about(self, ("About Diagram Scene"),
                        ("The <b>Diagram Scene</b> example shows use of the graphics framework."))

    def createToolBox(self):
        buttonGroup = QtGui.QButtonGroup()
        self.buttonGroup = buttonGroup
        buttonGroup.setExclusive(False) #Exclusivity is handled in the slot
        self.connect(buttonGroup, QtCore.SIGNAL("buttonClicked(int)"), self.buttonGroupClicked)
        layout = QtGui.QGridLayout()
        layout.addWidget(self.createCellWidget("Conditional",
                                DiagramItem.Conditional), 0, 0)
        layout.addWidget(self.createCellWidget("Process",
                        DiagramItem.Step),0, 1)
        layout.addWidget(self.createCellWidget("Input/Output",
                        DiagramItem.Io), 1, 0)

        textButton = QtGui.QToolButton()
        textButton.setCheckable(True)
        buttonGroup.addButton(textButton, InsertTextButton)
        textButton.setIcon(QtGui.QIcon(QtGui.QPixmap(":/images/textpointer.png")
                            .scaled(30, 30)))

        textButton.setIconSize(QtCore.QSize(50, 50))
        textLayout = QtGui.QGridLayout()
        textLayout.addWidget(textButton, 0, 0, QtCore.Qt.AlignHCenter)
        textLayout.addWidget(QtGui.QLabel("Text"), 1, 0, QtCore.Qt.AlignCenter)
        textWidget = QtGui.QWidget()
        textWidget.setLayout(textLayout)
        layout.addWidget(textWidget, 1, 1)

        layout.setRowStretch(3, 10)
        layout.setColumnStretch(2, 10)

        itemWidget = QtGui.QWidget()
        itemWidget.setLayout(layout)

        self.backgroundButtonGroup = QtGui.QButtonGroup()
        self.connect(self.backgroundButtonGroup, QtCore.SIGNAL("buttonClicked(QAbstractButton *)"),
                self.backgroundButtonGroupClicked)

        backgroundLayout = QtGui.QGridLayout()
        backgroundLayout.addWidget(self.createBackgroundCellWidget("Blue Grid",
                    ":/images/background1.png"), 0, 0)
        backgroundLayout.addWidget(self.createBackgroundCellWidget("White Grid",
                    ":/images/background2.png"), 0, 1)
        backgroundLayout.addWidget(self.createBackgroundCellWidget("Gray Grid",
                        ":/images/background3.png"), 1, 0)
        backgroundLayout.addWidget(self.createBackgroundCellWidget("No Grid",
                    ":/images/background4.png"), 1, 1)

        backgroundLayout.setRowStretch(2, 10)
        backgroundLayout.setColumnStretch(2, 10)

        backgroundWidget = QtGui.QWidget()
        backgroundWidget.setLayout(backgroundLayout)


        toolBox = QtGui.QToolBox()
        toolBox.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Ignored))
        toolBox.setMinimumWidth(itemWidget.sizeHint().width())
        toolBox.addItem(itemWidget, "Basic Flowchart Shapes")
        toolBox.addItem(backgroundWidget, "Backgrounds")
        self.toolBox = toolBox

    def createActions(self):
        toFrontAction = QtGui.QAction(QtGui.QIcon(":/images/bringtofront.png"),
                                    "Bring to &Front", self)
        toFrontAction.setShortcut("Ctrl+F")
        toFrontAction.setStatusTip("Bring item to front")
        self.connect(toFrontAction, QtCore.SIGNAL("triggered()"),
                self.bringToFront)
        self.toFrontAction = toFrontAction

        sendBackAction = QtGui.QAction(QtGui.QIcon(":/images/sendtoback.png"),
                                    "Send to &Back", self)
        sendBackAction.setShortcut("Ctrl+B")
        sendBackAction.setStatusTip("Send item to back")
        self.connect(sendBackAction, QtCore.SIGNAL("triggered()"),
                self.sendToBack)
        self.sendBackAction = sendBackAction

        deleteAction = QtGui.QAction(QtGui.QIcon(":/images/delete.png"),
                                "&Delete", self)
        deleteAction.setShortcut("Delete")
        deleteAction.setStatusTip("Delete item from diagram")
        self.connect(deleteAction, QtCore.SIGNAL("triggered()"),
                self.deleteItem)
        self.deleteAction = deleteAction

        exitAction = QtGui.QAction("E&xit", self)
        exitAction.setShortcut("Ctrl+X")
        exitAction.setStatusTip("Quit Scenediagram example")
        self.connect(exitAction, QtCore.SIGNAL("triggered()"), self, QtCore.SLOT("close()"))
        self.exitAction = exitAction

        boldAction = QtGui.QAction("Bold", self)
        boldAction.setCheckable(True)
        pixmap = QtGui.QPixmap(":/images/bold.png")
        boldAction.setIcon(QtGui.QIcon(pixmap))
        boldAction.setShortcut("Ctrl+B")
        self.connect(boldAction, QtCore.SIGNAL("triggered()"),
                self.handleFontChange)
        self.boldAction = boldAction

        italicAction = QtGui.QAction(QtGui.QIcon(":/images/italic.png"),
                                "Italic", self)
        italicAction.setCheckable(True)
        italicAction.setShortcut("Ctrl+I")
        self.connect(italicAction, QtCore.SIGNAL("triggered()"),
                self.handleFontChange)
        self.italicAction = italicAction

        underlineAction = QtGui.QAction(QtGui.QIcon(":/images/underline.png"),
                                    "Underline", self)
        underlineAction.setCheckable(True)
        underlineAction.setShortcut("Ctrl+U")
        self.connect(underlineAction, QtCore.SIGNAL("triggered()"),
                self.handleFontChange)
        self.underlineAction = underlineAction

        aboutAction = QtGui.QAction("A&bout", self)
        aboutAction.setShortcut("Ctrl+B")
        self.connect(aboutAction, QtCore.SIGNAL("triggered()"),
                self.about)
        self.aboutAction = aboutAction

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.exitAction)

        self.itemMenu = self.menuBar().addMenu("&Item")
        self.itemMenu.addAction(self.deleteAction)
        self.itemMenu.addSeparator()
        self.itemMenu.addAction(self.toFrontAction)
        self.itemMenu.addAction(self.sendBackAction)

        self.aboutMenu = self.menuBar().addMenu("&Help")
        self.aboutMenu.addAction(self.aboutAction)

    def createToolbars(self):
        self.editToolBar = self.addToolBar("Edit")
        self.editToolBar.addAction(self.deleteAction)
        self.editToolBar.addAction(self.toFrontAction)
        self.editToolBar.addAction(self.sendBackAction)

        fontCombo = QtGui.QFontComboBox()
        self.connect(fontCombo, QtCore.SIGNAL("currentFontChanged(const QFont &)"),
                self.currentFontChanged)
        self.fontCombo = fontCombo

        fontSizeCombo = QtGui.QComboBox()
        fontSizeCombo.setEditable(True)
        for i in range(8, 30, 2):
            fontSizeCombo.addItem(QtCore.QString().setNum(i))
        validator = QtGui.QIntValidator(2, 64, self)
        fontSizeCombo.setValidator(validator)
        self.connect(fontSizeCombo, QtCore.SIGNAL("currentIndexChanged(const QString &)"),
                self.fontSizeChanged)
        self.fontSizeCombo = fontSizeCombo

        fontColorToolButton = QtGui.QToolButton()
        fontColorToolButton.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
        fontColorToolButton.setMenu(self.createColorMenu(self.textColorChanged,
                                                    QtCore.Qt.black))
        textAction = fontColorToolButton.menu().defaultAction()
        fontColorToolButton.setIcon(self.createColorToolButtonIcon(
        ":/images/textpointer.png", QtCore.Qt.black))
        fontColorToolButton.setAutoFillBackground(True)
        self.connect(fontColorToolButton, QtCore.SIGNAL("clicked()"),
                self.textButtonTriggered)
        self.textAction = textAction
        self.fontColorToolButton = fontColorToolButton

        fillColorToolButton = QtGui.QToolButton()
        fillColorToolButton.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
        fillColorToolButton.setMenu(self.createColorMenu(self.itemColorChanged,
                            QtCore.Qt.white))
        fillAction = fillColorToolButton.menu().defaultAction()
        fillColorToolButton.setIcon(self.createColorToolButtonIcon(
        ":/images/floodfill.png", QtCore.Qt.white))
        self.connect(fillColorToolButton, QtCore.SIGNAL("clicked()"),
                self.fillButtonTriggered)
        self.fillAction = fillAction
        self.fillColorToolButton = fillColorToolButton

        lineColorToolButton = QtGui.QToolButton()
        lineColorToolButton.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
        lineColorToolButton.setMenu(self.createColorMenu(self.lineColorChanged,
                                    QtCore.Qt.black))
        lineAction = lineColorToolButton.menu().defaultAction()
        lineColorToolButton.setIcon(self.createColorToolButtonIcon(
            ":/images/linecolor.png", QtCore.Qt.black))
        self.connect(lineColorToolButton, QtCore.SIGNAL("clicked()"),
                self.lineButtonTriggered)
        self.lineAction = lineAction
        self.lineColorToolButton = lineColorToolButton

        textToolBar = self.addToolBar("Font")
        textToolBar.addWidget(fontCombo)
        textToolBar.addWidget(fontSizeCombo)
        textToolBar.addAction(self.boldAction)
        textToolBar.addAction(self.italicAction)
        textToolBar.addAction(self.underlineAction)
        self.textToolBar = textToolBar

        colorToolBar = self.addToolBar("Color")
        colorToolBar.addWidget(fontColorToolButton)
        colorToolBar.addWidget(fillColorToolButton)
        colorToolBar.addWidget(lineColorToolButton)
        self.colorToolBar = colorToolBar

        pointerButton = QtGui.QToolButton()
        pointerButton.setCheckable(True)
        pointerButton.setChecked(True)
        pointerButton.setIcon(QtGui.QIcon(":/images/pointer.png"))
        linePointerButton = QtGui.QToolButton()
        linePointerButton.setCheckable(True)
        linePointerButton.setIcon(QtGui.QIcon(":/images/linepointer.png"))

        pointerTypeGroup = QtGui.QButtonGroup()
        pointerTypeGroup.addButton(pointerButton, int(DiagramScene.MoveItem))
        pointerTypeGroup.addButton(linePointerButton,
                                    int(DiagramScene.InsertLine))
        self.connect(pointerTypeGroup, QtCore.SIGNAL("buttonClicked(int)"),
                self.pointerGroupClicked)
        self.pointerTypeGroup = pointerTypeGroup

        sceneScaleCombo = QtGui.QComboBox()
        scales = ["50%", "75%", "100%", "125%", "150%"]
        sceneScaleCombo.addItems(scales)
        sceneScaleCombo.setCurrentIndex(2)
        self.connect(sceneScaleCombo, QtCore.SIGNAL("currentIndexChanged(const QString &)"), self.sceneScaleChanged)
        self.sceneScaleCombo = sceneScaleCombo

        pointerToolbar = self.addToolBar("Pointer type")
        pointerToolbar.addWidget(pointerButton)
        pointerToolbar.addWidget(linePointerButton)
        pointerToolbar.addWidget(sceneScaleCombo)
        self.pointerToolbar = pointerToolbar

    def createBackgroundCellWidget(self, text, image):
        button = QtGui.QToolButton()
        button.setText(text)
        button.setIcon(QtGui.QIcon(image))
        button.setIconSize(QtCore.QSize(50, 50))
        button.setCheckable(True)
        self.backgroundButtonGroup.addButton(button)

        layout = QtGui.QGridLayout()
        layout.addWidget(button, 0, 0, QtCore.Qt.AlignHCenter)
        layout.addWidget(QtGui.QLabel(text), 1, 0, QtCore.Qt.AlignCenter)

        widget = QtGui.QWidget()
        widget.setLayout(layout)

        return widget

    def createCellWidget(self, text, diagramType):
        item = DiagramItem(diagramType, self.itemMenu)
        icon = QtGui.QIcon(item.image())

        button = QtGui.QToolButton()
        button.setIcon(icon)
        button.setIconSize(QtCore.QSize(50, 50))
        button.setCheckable(True)
        self.buttonGroup.addButton(button, diagramType)

        layout = QtGui.QGridLayout()
        layout.addWidget(button, 0, 0, QtCore.Qt.AlignHCenter)
        layout.addWidget(QtGui.QLabel(text), 1, 0, QtCore.Qt.AlignCenter)

        widget = QtGui.QWidget()
        widget.setLayout(layout)

        return widget

    def createColorMenu(self, slot, defaultColor):
        colors = [QtCore.Qt.black, QtCore.Qt.white, QtCore.Qt.red, QtCore.Qt.blue, QtCore.Qt.yellow]
        names = ["black", "white", "red", "blue", "yellow"]

        colorMenu = QtGui.QMenu(self)
        for color, name in zip(colors, names):
            action = QtGui.QAction(name, self)
            #need to specifically create a QColor from "color", since the "color" is a GlobalColor
            # and not a QColor object
            action.setData(QtCore.QVariant(QtGui.QColor(color)))
            action.setIcon(self.createColorIcon(color))
            self.connect(action, QtCore.SIGNAL("triggered()"), slot)
            colorMenu.addAction(action)
            if color == defaultColor:
                colorMenu.setDefaultAction(action)
        return colorMenu

    def createColorToolButtonIcon(self, imageFile, color):
        pixmap = QtGui.QPixmap(50, 80)
        pixmap.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(pixmap)
        image = QtGui.QPixmap(imageFile)
        target = QtCore.QRect(0, 0, 50, 60)
        source = QtCore.QRect(0, 0, 42, 42)
        painter.fillRect(QtCore.QRect(0, 60, 50, 80), color)
        painter.drawPixmap(target, image, source)
        painter.end()
        return QtGui.QIcon(pixmap)

    def createColorIcon(self, color):
        pixmap = QtGui.QPixmap(20, 20)
        painter = QtGui.QPainter(pixmap)
        painter.setPen(QtCore.Qt.NoPen)
        painter.fillRect(QtCore.QRect(0, 0, 20, 20), color)
        painter.end()
        return QtGui.QIcon(pixmap)


if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.setGeometry(100, 100, 800, 500)
    mainWindow.show()

    sys.exit(app.exec_())
