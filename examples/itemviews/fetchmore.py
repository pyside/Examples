#!/usr/bin/python

# Fetch More Example
# Ported to PyQt4 by Darryl Wallace, 2009 - wallacdj@gmail.com

from PySide import QtCore, QtGui


class FileListModel(QtCore.QAbstractListModel):
    #numberPopulated = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super(FileListModel, self).__init__(parent)

        self.fileCount = 0    
        self.fileList = []

    def rowCount(self, parent=QtCore.QModelIndex()):
        return self.fileCount

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return QtCore.QVariant()

        if index.row() >= len(self.fileList) or index.row() < 0:
            return QtCore.QVariant()

        if role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(self.fileList[index.row()])
        elif role == QtCore.Qt.BackgroundRole:
            batch = (index.row() / 100) % 2
            if batch == 0:
                return QtCore.QVariant(QtGui.qApp.palette().base())
            else:
                return QtCore.QVariant(QtGui.qApp.palette().alternateBase())

        return QtCore.QVariant()

    def canFetchMore(self, index):
        return self.fileCount < len(self.fileList)

    def fetchMore(self, index):
        remainder = len(self.fileList) - self.fileCount
        itemsToFetch = min(100, remainder)

        self.beginInsertRows(QtCore.QModelIndex(), self.fileCount,
                self.fileCount + itemsToFetch)

        self.fileCount += itemsToFetch

        self.endInsertRows()

        self.emit(QtCore.SIGNAL('numberPopulated'), itemsToFetch)

    def setDirPath(self, path):
        dir = QtCore.QDir(path)

        self.fileList = list(dir.entryList())
        self.fileCount = 0
        self.reset()


class Window(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        model = FileListModel(self)
        model.setDirPath(QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.PrefixPath))

        label = QtGui.QLabel(self.tr("Directory"))
        lineEdit = QtGui.QLineEdit()
        label.setBuddy(lineEdit)

        view = QtGui.QListView()
        view.setModel(model)

        self.logViewer = QtGui.QTextBrowser()
        self.logViewer.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred))

        QtCore.QObject.connect(lineEdit, QtCore.SIGNAL('textChanged(const QString&)'), model.setDirPath)
        QtCore.QObject.connect(lineEdit, QtCore.SIGNAL('textChanged(const QString&)'), self.logViewer, QtCore.SLOT('clear()'))
        QtCore.QObject.connect(model, QtCore.SIGNAL('numberPopulated'), self.updateLog)

        layout = QtGui.QGridLayout()
        layout.addWidget(label, 0, 0)
        layout.addWidget(lineEdit, 0, 1)
        layout.addWidget(view, 1, 0, 1, 2)
        layout.addWidget(self.logViewer, 2, 0, 1, 2)

        self.setLayout(layout)
        self.setWindowTitle(self.tr("Fetch More Example"))

    def updateLog(self, number):
        self.logViewer.append(self.tr("%1 items added.").arg(number))


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)

    window = Window()
    window.show()

    sys.exit(app.exec_())
