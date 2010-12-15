import sys
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtDeclarative import *

class PersonModel (QAbstractListModel):

    MyRole = Qt.UserRole + 1

    def __init__(self, parent = None):
        QAbstractListModel.__init__(self, parent)
        self.setRoleNames({
            PersonModel.MyRole : 'modelData',
            Qt.DisplayRole : 'display' # Qt asserts if you don't define a display role
            })
        self._data = []

    def rowCount(self, index):
        return len(self._data)

    def data(self, index, role):
        d = self._data[index.row()]

        if role == Qt.DisplayRole:
            return d['name']
        elif role == Qt.DecorationRole:
            return Qt.black
        elif role == PersonModel.MyRole:
            return d['myrole']
        return None

    def populate(self):
        self._data.append({'name':'Qt', 'myrole':'role1'})
        self._data.append({'name':'PySide', 'myrole':'role2'})

if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = QDeclarativeView()

    myModel = PersonModel()
    myModel.populate()

    view.rootContext().setContextProperty("myModel", myModel)
    view.setSource('view.qml')
    view.show()

    app.exec_()


