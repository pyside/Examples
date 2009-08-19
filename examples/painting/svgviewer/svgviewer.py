#!/usr/bin/env python

"""PyQt4 port of the painting/svgviewer example from Qt v4.x"""

from PyQt4 import QtCore, QtGui, QtOpenGL, QtSvg

import svgviewer_rc


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.currentPath = QtCore.QString()

        self.view = SvgView()

        fileMenu = QtGui.QMenu(self.tr("&File"), self)
        openAction = fileMenu.addAction(self.tr("&Open..."))
        openAction.setShortcut(QtGui.QKeySequence(self.tr("Ctrl+O")))
        quitAction = fileMenu.addAction(self.tr("E&xit"))
        quitAction.setShortcut(QtGui.QKeySequence(self.tr("Ctrl+Q")))

        self.menuBar().addMenu(fileMenu)

        viewMenu = QtGui.QMenu(self.tr("&View"), self)
        self.backgroundAction = viewMenu.addAction(self.tr("&Background"))
        self.backgroundAction.setEnabled(False)
        self.backgroundAction.setCheckable(True)
        self.backgroundAction.setChecked(False)
        self.backgroundAction.toggled.connect(self.view.setViewBackground)

        self.outlineAction = viewMenu.addAction(self.tr("&Outline"))
        self.outlineAction.setEnabled(False)
        self.outlineAction.setCheckable(True)
        self.outlineAction.setChecked(True)
        self.outlineAction.toggled.connect(self.view.setViewOutline)

        self.menuBar().addMenu(viewMenu)

        rendererMenu = QtGui.QMenu(self.tr("&Renderer"), self)
        self.nativeAction = rendererMenu.addAction(self.tr("&Native"))
        self.nativeAction.setCheckable(True)
        self.nativeAction.setChecked(True)

        if QtOpenGL.QGLFormat.hasOpenGL():
            self.glAction = rendererMenu.addAction(self.tr("&OpenGL"))
            self.glAction.setCheckable(True)

        self.imageAction = rendererMenu.addAction(self.tr("&Image"))
        self.imageAction.setCheckable(True)

        if QtOpenGL.QGLFormat.hasOpenGL():
            rendererMenu.addSeparator()
            self.highQualityAntialiasingAction = rendererMenu.addAction(self.tr("&High Quality Antialiasing"))
            self.highQualityAntialiasingAction.setEnabled(False)
            self.highQualityAntialiasingAction.setCheckable(True)
            self.highQualityAntialiasingAction.setChecked(False)
            self.highQualityAntialiasingAction.toggled.connect(self.view.setHighQualityAntialiasing)

        rendererGroup = QtGui.QActionGroup(self)
        rendererGroup.addAction(self.nativeAction)

        if QtOpenGL.QGLFormat.hasOpenGL():
            rendererGroup.addAction(self.glAction)

        rendererGroup.addAction(self.imageAction)

        self.menuBar().addMenu(rendererMenu)

        openAction.triggered.connect(self.openFile)
        quitAction.triggered.connect(QtGui.qApp.quit)
        rendererGroup.triggered.connect(self.setRenderer)

        self.setCentralWidget(self.view)
        self.setWindowTitle(self.tr("SVG Viewer"))

    def openFile(self, path=''):
        path = QtCore.QString(path)
        if path.isEmpty():
            fileName = QtGui.QFileDialog.getOpenFileName(self,
                    self.tr("Open SVG File"), self.currentPath,
                    "SVG files (*.svg *.svgz *.svg.gz)")
        else:
            fileName = path

        if not fileName.isEmpty():
            svg_file = QtCore.QFile(fileName)
            if not svg_file.exists():
                QtGui.QMessageBox.critical(self, self.tr("Open SVG File"),
                        QtCore.QString("Could not open file '%1'.").arg(fileName))

                self.outlineAction.setEnabled(False)
                self.backgroundAction.setEnabled(False)
                return

            self.view.openFile(svg_file)

            if not fileName.startsWith(":/"):
                self.currentPath = fileName
                self.setWindowTitle(self.tr("%1 - SVGViewer").arg(self.currentPath))

            self.outlineAction.setEnabled(True)
            self.backgroundAction.setEnabled(True)

            self.resize(self.view.sizeHint() + QtCore.QSize(80, 80 + self.menuBar().height()))

    def setRenderer(self, action):
        if action == self.nativeAction:
            self.view.setRenderer(SvgView.Native)
        elif action == self.glAction:
            if QtOpenGL.QGLFormat.hasOpenGL():
                self.highQualityAntialiasingAction.setEnabled(True)
                self.view.setRenderer(SvgView.OpenGL)
        elif action == self.imageAction:
            self.view.setRenderer(SvgView.Image)


class SvgView(QtGui.QGraphicsView):
    Native, OpenGL, Image = range(3)

    def __init__(self, parent=None):
        super(SvgView, self).__init__(parent)

        self.renderer = SvgView.Native
        self.svgItem = None
        self.backgroundItem = None
        self.outlineItem = None
        self.image = QtGui.QImage()

        self.setScene(QtGui.QGraphicsScene(self))
        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)

        # Prepare background check-board pattern.
        tilePixmap = QtGui.QPixmap(64, 64)
        tilePixmap.fill(QtCore.Qt.white)
        tilePainter = QtGui.QPainter(tilePixmap)
        color = QtGui.QColor(220, 220, 220)
        tilePainter.fillRect(0, 0, 32, 32, color)
        tilePainter.fillRect(32, 32, 32, 32, color)
        tilePainter.end()

        self.setBackgroundBrush(QtGui.QBrush(tilePixmap))

    def drawBackground(self, p, rect):
        p.save()
        p.resetTransform()
        p.drawTiledPixmap(self.viewport().rect(),
                self.backgroundBrush().texture())
        p.restore()

    def openFile(self, svg_file):
        if not svg_file.exists():
            return

        s = self.scene()

        if self.backgroundItem:
            drawBackground = self.backgroundItem.isVisible()
        else:
            drawBackground = False

        if self.outlineItem:
            drawOutline = self.outlineItem.isVisible()
        else:
            drawOutline = True

        s.clear()
        self.resetTransform()

        self.svgItem = QtSvg.QGraphicsSvgItem(svg_file.fileName())
        self.svgItem.setFlags(QtGui.QGraphicsItem.ItemClipsToShape)
        self.svgItem.setCacheMode(QtGui.QGraphicsItem.NoCache)
        self.svgItem.setZValue(0)

        self.backgroundItem = QtGui.QGraphicsRectItem(self.svgItem.boundingRect())
        self.backgroundItem.setBrush(QtCore.Qt.white)
        self.backgroundItem.setPen(QtGui.QPen(QtCore.Qt.NoPen))
        self.backgroundItem.setVisible(drawBackground)
        self.backgroundItem.setZValue(-1)

        self.outlineItem = QtGui.QGraphicsRectItem(self.svgItem.boundingRect())
        outline = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.DashLine)
        outline.setCosmetic(True)
        self.outlineItem.setPen(outline)
        self.outlineItem.setBrush(QtGui.QBrush(QtCore.Qt.NoBrush))
        self.outlineItem.setVisible(drawOutline)
        self.outlineItem.setZValue(1)

        s.addItem(self.backgroundItem)
        s.addItem(self.svgItem)
        s.addItem(self.outlineItem)

        s.setSceneRect(self.outlineItem.boundingRect().adjusted(-10, -10, 10, 10))

    def setRenderer(self, renderer):
        self.renderer = renderer

        if self.renderer == SvgView.OpenGL:
            if QtOpenGL.QGLFormat.hasOpenGL():
                self.setViewport(QtOpenGL.QGLWidget(QtOpenGL.QGLFormat(QtOpenGL.QGL.SampleBuffers)))
        else:
            self.setViewport(QtGui.QWidget())

    def setHighQualityAntialiasing(self, highQualityAntialiasing):
        if QtOpenGL.QGLFormat.hasOpenGL():
            self.setRenderHint(QtGui.QPainter.HighQualityAntialiasing,
                    highQualityAntialiasing)

    def setViewBackground(self, enable):
        if self.backgroundItem:
            self.backgroundItem.setVisible(enable)

    def setViewOutline(self, enable):
        if self.outlineItem:
            self.outlineItem.setVisible(enable)

    def paintEvent(self, event):
        if self.renderer == SvgView.Image:
            if self.image.size() != self.viewport().size():
                self.image = QtGui.QImage(self.viewport().size(),
                        QtGui.QImage.Format_ARGB32_Premultiplied)

            imagePainter = QtGui.QPainter(self.image)
            QtGui.QGraphicsView.render(imagePainter)
            imagePainter.end()

            p = QtGui.QPainter(self.viewport())
            p.drawImage(0, 0, self.image)
        else:
            super(SvgView, self).paintEvent(event)

    def wheelEvent(self, event):
        factor = QtCore.qPow(1.2, event.delta() / 240.0)
        self.scale(factor, factor)
        event.accept()


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)

    window = MainWindow()
    if len(sys.argv) == 2:
        window.openFile(sys.argv[1])
    else:
        window.openFile(':/files/bubbles.svg')
    window.show()
    sys.exit(app.exec_())
