
import sys
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtDeclarative import *

class PieSlice (QDeclarativeItem):

    def __init__(self, parent = None):
        QDeclarativeItem.__init__(self, parent)
        # need to disable this flag to draw inside a QDeclarativeItem
        self.setFlag(QGraphicsItem.ItemHasNoContents, False)
        self._color = QColor()

    def getColor(self):
        return self._color

    def setColor(self, value):
        self._color = value

    color = Property(QColor, getColor, setColor)

    def paint(self, painter, options, widget):
        pen = QPen(self._color, 2)
        painter.setPen(pen);
        painter.setRenderHints(QPainter.Antialiasing, True);
        painter.drawPie(self.boundingRect(), 90 * 16, 290 * 16);

class PieChart (QDeclarativeItem):

    def __init__(self, parent = None):
        QDeclarativeItem.__init__(self, parent)
        self._name = u''
        self._pieSlice = None

    def getName(self):
        return self._name

    def setName(self, value):
        self._name = value

    name = Property(unicode, getName, setName)

    def getPieSlice(self):
        return self._pieSlice

    def setPieSlice(self, value):
        self._pieSlice = value
        self._pieSlice.setParentItem(self)

    pieSlice = Property(PieSlice, getPieSlice, setPieSlice)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    qmlRegisterType(PieChart, 'Charts', 1, 0, 'PieChart');
    qmlRegisterType(PieSlice, "Charts", 1, 0, "PieSlice");

    view = QDeclarativeView()
    view.setSource(QUrl.fromLocalFile('app.qml'))
    view.show()
    sys.exit(app.exec_())
