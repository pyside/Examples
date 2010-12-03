
import sys
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtDeclarative import *

class PieChart (QDeclarativeItem):

    def __init__(self, parent = None):
        QDeclarativeItem.__init__(self, parent)
        # need to disable this flag to draw inside a QDeclarativeItem
        self.setFlag(QGraphicsItem.ItemHasNoContents, False)
        self._name = u''
        self._color = QColor()

    def paint(self, painter, options, widget):
        pen = QPen(self._color, 2)
        painter.setPen(pen);
        painter.setRenderHints(QPainter.Antialiasing, True);
        painter.drawPie(self.boundingRect(), 90 * 16, 290 * 16);

    def getColor(self):
        return self._color

    def setColor(self, value):
        if value != self._color:
            self._color = value
            self.update()
            self.colorChanged.emit()

    def getName(self):
        return self._name

    def setName(self, value):
        self._name = value

    colorChanged = Signal()
    color = Property(QColor, getColor, setColor, notify=colorChanged)
    name = Property(unicode, getName, setName)

    chartCleared = Signal()

    @Slot() # This should be something like @Invokable
    def clearChart(self):
        self.setColor(Qt.transparent)
        self.update()
        self.chartCleared.emit()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    qmlRegisterType(PieChart, 'Charts', 1, 0, 'PieChart');

    view = QDeclarativeView()
    view.setSource(QUrl.fromLocalFile('app.qml'))
    view.show()
    sys.exit(app.exec_())
