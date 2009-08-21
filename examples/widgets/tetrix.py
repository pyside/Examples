#!/usr/bin/env python

"""PySide port of the widgets/tetrix example from Qt v4.x"""

import sys
import random
from PySide import QtCore, QtGui


class TetrixWindow(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)

        self.board = TetrixBoard(self)

        self.nextPieceLabel = QtGui.QLabel()
        self.nextPieceLabel.setFrameStyle(QtGui.QFrame.Box | QtGui.QFrame.Raised)
        self.nextPieceLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.board.setNextPieceLabel(self.nextPieceLabel)

        self.scoreLcd = QtGui.QLCDNumber(5)
        self.scoreLcd.setSegmentStyle(QtGui.QLCDNumber.Filled)
        self.levelLcd = QtGui.QLCDNumber(2)
        self.levelLcd.setSegmentStyle(QtGui.QLCDNumber.Filled)
        self.linesLcd = QtGui.QLCDNumber(5)
        self.linesLcd.setSegmentStyle(QtGui.QLCDNumber.Filled)

        self.startButton = QtGui.QPushButton(self.tr("&Start"))
        self.startButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.quitButton = QtGui.QPushButton(self.tr("&Quit"))
        self.quitButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pauseButton = QtGui.QPushButton(self.tr("&Pause"))
        self.pauseButton.setFocusPolicy(QtCore.Qt.NoFocus)

        self.connect(self.startButton, QtCore.SIGNAL("clicked()"),
                     self.board.start)
        self.connect(self.pauseButton, QtCore.SIGNAL("clicked()"),
                     self.board.pause)
        self.connect(self.quitButton, QtCore.SIGNAL("clicked()"),
                     QtGui.qApp, QtCore.SLOT("quit()"))
        self.connect(self.board, QtCore.SIGNAL("scoreChanged(int)"),
                     self.scoreLcd, QtCore.SLOT("display(int)"))
        self.connect(self.board, QtCore.SIGNAL("levelChanged(int)"),
                     self.levelLcd, QtCore.SLOT("display(int)"))
        self.connect(self.board, QtCore.SIGNAL("linesRemovedChanged(int)"),
                     self.linesLcd, QtCore.SLOT("display(int)"))

        layout = QtGui.QGridLayout()
        layout.addWidget(self.createLabel(self.tr("NEXT")), 0, 0)
        layout.addWidget(self.nextPieceLabel, 1, 0)
        layout.addWidget(self.createLabel(self.tr("LEVEL")), 2, 0)
        layout.addWidget(self.levelLcd, 3, 0)
        layout.addWidget(self.startButton, 4, 0)
        layout.addWidget(self.board, 0, 1, 6, 1)
        layout.addWidget(self.createLabel(self.tr("SCORE")), 0, 2)
        layout.addWidget(self.scoreLcd, 1, 2)
        layout.addWidget(self.createLabel(self.tr("LINES REMOVED")), 2, 2)
        layout.addWidget(self.linesLcd, 3, 2)
        layout.addWidget(self.quitButton, 4, 2)
        layout.addWidget(self.pauseButton, 5, 2)
        self.setLayout(layout)

        self.setWindowTitle(self.tr("Tetrix"))
        self.resize(550, 370)

    def createLabel(self, text):
        lbl = QtGui.QLabel(text)
        lbl.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom)
        return lbl


class TetrixBoard(QtGui.QFrame):
    BoardWidth = 10
    BoardHeight = 22

    def __init__(self, parent):
        QtGui.QFrame.__init__(self, parent)

        self.timer = QtCore.QBasicTimer()
        self.isWaitingAfterLine = False
        self.curPiece = TetrixPiece()
        self.nextPiece = TetrixPiece()
        self.curX = 0
        self.curY = 0
        self.nextPieceLabel = None
        self.numLinesRemoved = 0
        self.numPiecesDropped = 0
        self.score = 0
        self.level = 0
        self.board = None

        self.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Sunken)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.isStarted = False
        self.isPaused = False
        self.clearBoard()

        self.nextPiece.setRandomShape()

    def shapeAt(self, x, y):
        return self.board[(y * TetrixBoard.BoardWidth) + x]

    def setShapeAt(self, x, y, shape):
        self.board[(y * TetrixBoard.BoardWidth) + x] = shape   

    def timeoutTime(self):
        return 1000 / (1 + self.level)

    def squareWidth(self):
        return self.contentsRect().width() / TetrixBoard.BoardWidth

    def squareHeight(self):
        return self.contentsRect().height() / TetrixBoard.BoardHeight

    def setNextPieceLabel(self, label):
        self.nextPieceLabel = label

    def sizeHint(self):
        return QtCore.QSize(TetrixBoard.BoardWidth * 15 + self.frameWidth() * 2,
                            TetrixBoard.BoardHeight * 15 + self.frameWidth() * 2)

    def minimumSizeHint(self):
        return QtCore.QSize(TetrixBoard.BoardWidth * 5 + self.frameWidth() * 2,
                            TetrixBoard.BoardHeight * 5 + self.frameWidth() * 2)

    def start(self):
        if self.isPaused:
            return

        self.isStarted = True
        self.isWaitingAfterLine = False
        self.numLinesRemoved = 0
        self.numPiecesDropped = 0
        self.score = 0
        self.level = 1
        self.clearBoard()

        self.emit(QtCore.SIGNAL("linesRemovedChanged(int)"), self.numLinesRemoved)
        self.emit(QtCore.SIGNAL("scoreChanged(int)"), self.score)
        self.emit(QtCore.SIGNAL("levelChanged(int)"), self.level)

        self.newPiece()
        self.timer.start(self.timeoutTime(), self)

    def pause(self):
        if not self.isStarted:
            return

        self.isPaused = not self.isPaused
        if self.isPaused:
            self.timer.stop()
        else:
            self.timer.start(self.timeoutTime(), self)

        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        rect = self.contentsRect()

        self.drawFrame(painter)

        if self.isPaused:
            painter.drawText(rect, QtCore.Qt.AlignCenter, self.tr("Pause"))
            return

        boardTop = rect.bottom() - TetrixBoard.BoardHeight * self.squareHeight()

        for i in range(TetrixBoard.BoardHeight):
            for j in range(TetrixBoard.BoardWidth):
                shape = self.shapeAt(j, TetrixBoard.BoardHeight - i - 1)
                if shape != TetrixShape.NoShape:
                    self.drawSquare(painter,
                                    rect.left() + j * self.squareWidth(),
                                    boardTop + i * self.squareHeight(), shape)

        if self.curPiece.shape() != TetrixShape.NoShape:
            for i in range(4):
                x = self.curX + self.curPiece.x(i)
                y = self.curY - self.curPiece.y(i)
                self.drawSquare(painter,
                                rect.left() + x * self.squareWidth(),
                                boardTop + (TetrixBoard.BoardHeight - y - 1) * self.squareHeight(),
                                self.curPiece.shape())

    def keyPressEvent(self, event):
        if not self.isStarted or self.isPaused or self.curPiece.shape() == TetrixShape.NoShape:
            QtGui.QWidget.keyPressEvent(self, event)
            return

        key = event.key()
        if key == QtCore.Qt.Key_Left:
            self.tryMove(self.curPiece, self.curX - 1, self.curY)
        elif key == QtCore.Qt.Key_Right:
            self.tryMove(self.curPiece, self.curX + 1, self.curY)
        elif key == QtCore.Qt.Key_Down:
            self.tryMove(self.curPiece.rotatedRight(), self.curX, self.curY)
        elif key == QtCore.Qt.Key_Up:
            self.tryMove(self.curPiece.rotatedLeft(), self.curX, self.curY)
        elif key == QtCore.Qt.Key_Space:
            self.dropDown()
        elif key == QtCore.Qt.Key_D:
            self.oneLineDown()
        else:
            QtGui.QWidget.keyPressEvent(self, event)

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            if self.isWaitingAfterLine:
                self.isWaitingAfterLine = False
                self.newPiece()
                self.timer.start(self.timeoutTime(), self)
            else:
                self.oneLineDown()
        else:
            QtGui.QFrame.timerEvent(self, event)

    def clearBoard(self):
        self.board = [TetrixShape.NoShape for i in range(TetrixBoard.BoardHeight * TetrixBoard.BoardWidth)]

    def dropDown(self):
        dropHeight = 0
        newY = self.curY
        while newY > 0:
            if not self.tryMove(self.curPiece, self.curX, newY - 1):
                break
            newY -= 1
            dropHeight += 1

        self.pieceDropped(dropHeight)

    def oneLineDown(self):
        if not self.tryMove(self.curPiece, self.curX, self.curY - 1):
            self.pieceDropped(0)

    def pieceDropped(self, dropHeight):
        for i in range(4):
            x = self.curX + self.curPiece.x(i)
            y = self.curY - self.curPiece.y(i)
            self.setShapeAt(x, y, self.curPiece.shape())

        self.numPiecesDropped += 1
        if self.numPiecesDropped % 25 == 0:
            self.level += 1
            self.timer.start(self.timeoutTime(), self)
            self.emit(QtCore.SIGNAL("levelChanged(int)"), self.level)

        self.score += dropHeight + 7
        self.emit(QtCore.SIGNAL("scoreChanged(int)"), self.score)
        self.removeFullLines()

        if not self.isWaitingAfterLine:
            self.newPiece()

    def removeFullLines(self):
        numFullLines = 0

        for i in range(TetrixBoard.BoardHeight - 1, -1, -1):
            lineIsFull = True

            for j in range(TetrixBoard.BoardWidth):
                if self.shapeAt(j, i) == TetrixShape.NoShape:
                    lineIsFull = False
                    break

            if lineIsFull:
                numFullLines += 1
                for k in range(TetrixBoard.BoardHeight - 1):
                    for j in range(TetrixBoard.BoardWidth):
                        self.setShapeAt(j, k, self.shapeAt(j, k + 1))

                for j in range(TetrixBoard.BoardWidth):
                    self.setShapeAt(j, TetrixBoard.BoardHeight - 1, TetrixShape.NoShape)

        if numFullLines > 0:
            self.numLinesRemoved += numFullLines
            self.score += 10 * numFullLines
            self.emit(QtCore.SIGNAL("linesRemovedChanged(int)"), self.numLinesRemoved)
            self.emit(QtCore.SIGNAL("scoreChanged(int)"), self.score)

            self.timer.start(500, self)
            self.isWaitingAfterLine = True
            self.curPiece.setShape(TetrixShape.NoShape)
            self.update()

    def newPiece(self):
        self.curPiece = self.nextPiece
        self.nextPiece.setRandomShape()
        self.showNextPiece()
        self.curX = TetrixBoard.BoardWidth / 2 + 1
        self.curY = TetrixBoard.BoardHeight - 1 + self.curPiece.minY()

        if not self.tryMove(self.curPiece, self.curX, self.curY):
            self.curPiece.setShape(TetrixShape.NoShape)
            self.timer.stop()
            self.isStarted = False

    def showNextPiece(self):
        if self.nextPieceLabel is not None:
            return

        dx = self.nextPiece.maxX() - self.nextPiece.minX() + 1
        dy = self.nextPiece.maxY() - self.nextPiece.minY() + 1

        pixmap = QtGui.QPixmap(dx * self.squareWidth(), dy * self.squareHeight())
        painter = QtGui.QPainter(pixmap)
        painter.fillRect(pixmap.rect(), self.nextPieceLabel.palette().background())

        for int in range(4):
            x = self.nextPiece.x(i) - self.nextPiece.minX()
            y = self.nextPiece.y(i) - self.nextPiece.minY()
            self.drawSquare(painter, x * self.squareWidth(),
                            y * self.squareHeight(), self.nextPiece.shape())

        self.nextPieceLabel.setPixmap(pixmap)

    def tryMove(self, newPiece, newX, newY):
        for i in range(4):
            x = newX + newPiece.x(i)
            y = newY - newPiece.y(i)
            if x < 0 or x >= TetrixBoard.BoardWidth or y < 0 or y >= TetrixBoard.BoardHeight:
                return False
            if self.shapeAt(x, y) != TetrixShape.NoShape:
                return False

        self.curPiece = newPiece
        self.curX = newX
        self.curY = newY
        self.update()
        return True

    def drawSquare(self, painter, x, y, shape):
        colorTable = [0x000000, 0xCC6666, 0x66CC66, 0x6666CC,
                      0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00]

        color = QtGui.QColor(colorTable[shape])
        painter.fillRect(x + 1, y + 1,
                         self.squareWidth() - 2, self.squareHeight() - 2,
                         color)

        painter.setPen(color.lighter())
        painter.drawLine(x, y + self.squareHeight() - 1, x, y)
        painter.drawLine(x, y, x + self.squareWidth() - 1, y)

        painter.setPen(color.darker())
        painter.drawLine(x + 1, y + self.squareHeight() - 1,
                         x + self.squareWidth() - 1, y + self.squareHeight() - 1)
        painter.drawLine(x + self.squareWidth() - 1, y + self.squareHeight() - 1,
                         x + self.squareWidth() - 1, y + 1)


class TetrixShape(object):
    NoShape = 0
    ZShape = 1
    SShape = 2
    LineShape = 3
    TShape = 4
    SquareShape = 5
    LShape = 6
    MirroredLShape = 7


class TetrixPiece(object):
    coordsTable = (
        ((0, 0),     (0, 0),     (0, 0),     (0, 0)),
        ((0, -1),    (0, 0),     (-1, 0),    (-1, 1)),
        ((0, -1),    (0, 0),     (1, 0),     (1, 1)),
        ((0, -1),    (0, 0),     (0, 1),     (0, 2)),
        ((-1, 0),    (0, 0),     (1, 0),     (0, 1)),
        ((0, 0),     (1, 0),     (0, 1),     (1, 1)),
        ((-1, -1),   (0, -1),    (0, 0),     (0, 1)),
        ((1, -1),    (0, -1),    (0, 0),     (0, 1))
    )

    def __init__(self):
        self.coords = [[0,0] for _ in range(4)]
        self.pieceShape = TetrixShape.NoShape

        self.setShape(TetrixShape.NoShape)

    def shape(self):
        return self.pieceShape

    def setShape(self, shape):
        table = TetrixPiece.coordsTable[shape]
        for i in range(4):
            for j in range(2):
                self.coords[i][j] = table[i][j]

        self.pieceShape = shape

    def setRandomShape(self):
        self.setShape(random.randint(1, 7))

    def x(self, index):
        return self.coords[index][0]

    def y(self, index):
        return self.coords[index][1]

    def setX(self, index, x):
        self.coords[index][0] = x

    def setY(self, index, y):
        self.coords[index][1] = y

    def minX(self):
        m = self.coords[0][0]
        for i in range(4):
            m = min(m, self.coords[i][0])

        return m

    def maxX(self):
        m = self.coords[0][0]
        for i in range(4):
            m = max(m, self.coords[i][0])

        return m

    def minY(self):
        m = self.coords[0][1]
        for i in range(4):
            m = min(m, self.coords[i][1])

        return m

    def maxY(self):
        m = self.coords[0][1]
        for i in range(4):
            m = max(m, self.coords[i][1])

        return m

    def rotatedLeft(self):
        if self.pieceShape == TetrixShape.SquareShape:
            return self

        result = TetrixPiece()
        result.pieceShape = self.pieceShape
        for i in range(4):
            result.setX(i, self.y(i))
            result.setY(i, -self.x(i))

        return result

    def rotatedRight(self):
        if self.pieceShape == TetrixShape.SquareShape:
            return self

        result = TetrixPiece()
        result.pieceShape = self.pieceShape
        for i in range(4):
            result.setX(i, -self.y(i))
            result.setY(i, self.x(i))

        return result


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = TetrixWindow()
    window.show()
    random.seed(None)
    sys.exit(app.exec_())
