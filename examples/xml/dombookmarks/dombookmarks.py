#!/usr/bin/env python

"""PyQt4 port of the xml/dombookmarks example from Qt v4.x"""

from PyQt4 import QtCore, QtGui, QtXml


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.xbelTree = XbelTree()
        self.setCentralWidget(self.xbelTree)

        self.createActions()
        self.createMenus()

        self.statusBar().showMessage(self.tr("Ready"))

        self.setWindowTitle(self.tr("DOM Bookmarks"))
        self.resize(480, 320)

    def open(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self,
                self.tr("Open Bookmark File"), QtCore.QDir.currentPath(),
                self.tr("XBEL Files (*.xbel *.xml)"))

        if fileName.isEmpty():
            return

        inFile = QtCore.QFile(fileName)
        if not inFile.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, self.tr("DOM Bookmarks"),
                    self.tr("Cannot read file %1:\n%2.").arg(fileName).arg(inFile.errorString()))
            return

        if self.xbelTree.read(inFile):
            self.statusBar().showMessage(self.tr("File loaded"), 2000)

    def saveAs(self):
        fileName = QtGui.QFileDialog.getSaveFileName(self,
                self.tr("Save Bookmark File"), QtCore.QDir.currentPath(),
                self.tr("XBEL Files (*.xbel *.xml)"))

        if fileName.isEmpty():
            return

        outFile = QtCore.QFile(fileName)
        if not outFile.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, self.tr("DOM Bookmarks"),
                    self.tr("Cannot write file %1:\n%2.").arg(fileName).arg(outFile.errorString()))
            return

        if self.xbelTree.write(outFile):
            self.statusBar().showMessage(self.tr("File saved"), 2000)

    def about(self):
       QtGui.QMessageBox.about(self, self.tr("About DOM Bookmarks"),
            self.tr("The <b>DOM Bookmarks</b> example demonstrates how to use "
                    "Qt's DOM classes to read and write XML documents."))

    def createActions(self):
        self.openAct = QtGui.QAction(self.tr("&Open..."), self)
        self.openAct.setShortcut(self.tr("Ctrl+O"))
        self.openAct.triggered.connect(self.open)

        self.saveAsAct = QtGui.QAction(self.tr("&Save As..."), self)
        self.saveAsAct.setShortcut(self.tr("Ctrl+S"))
        self.saveAsAct.triggered.connect(self.saveAs)

        self.exitAct = QtGui.QAction(self.tr("E&xit"), self)
        self.exitAct.setShortcut(self.tr("Ctrl+Q"))
        self.exitAct.triggered.connect(self.close)

        self.aboutAct = QtGui.QAction(self.tr("&About"), self)
        self.aboutAct.triggered.connect(self.about)

        self.aboutQtAct = QtGui.QAction(self.tr("About &Qt"), self)
        self.aboutQtAct.triggered.connect(QtGui.qApp.aboutQt)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu(self.tr("&File"))
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAsAct)
        self.fileMenu.addAction(self.exitAct)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu(self.tr("&Help"))
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)


class XbelTree(QtGui.QTreeWidget):
    def __init__(self, parent=None):
        super(XbelTree, self).__init__(parent)

        labels = QtCore.QStringList()
        labels << self.tr("Title") << self.tr("Location")

        self.header().setResizeMode(QtGui.QHeaderView.Stretch)
        self.setHeaderLabels(labels)

        self.domDocument = QtXml.QDomDocument()

        self.domElementForItem = {}

        self.folderIcon = QtGui.QIcon()
        self.bookmarkIcon = QtGui.QIcon()

        self.folderIcon.addPixmap(self.style().standardPixmap(QtGui.QStyle.SP_DirClosedIcon),
                QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.folderIcon.addPixmap(self.style().standardPixmap(QtGui.QStyle.SP_DirOpenIcon),
                QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.bookmarkIcon.addPixmap(self.style().standardPixmap(QtGui.QStyle.SP_FileIcon))

    def read(self, device):     
        ok, errorStr, errorLine, errorColumn = self.domDocument.setContent(device, True)
        if not ok:
            QtGui.QMessageBox.information(self.window(),
                    self.tr("DOM Bookmarks"),
                    self.tr("Parse error at line %1, column %2:\n%3").arg(errorLine).arg(errorColumn).arg(errorStr))
            return False

        root = self.domDocument.documentElement()
        if root.tagName() != "xbel":
            QtGui.QMessageBox.information(self.window(),
                    self.tr("DOM Bookmarks"),
                    self.tr("The file is not an XBEL file."))
            return False
        elif root.hasAttribute("version") and root.attribute("version") != "1.0":
            QtGui.QMessageBox.information(self.window(),
                    self.tr("DOM Bookmarks"),
                    self.tr("The file is not an XBEL version 1.0 file."))
            return False

        self.clear()

        # It might not be connected.
        try:
            self.itemChanged.disconnect(self.updateDomElement)
        except:
            pass

        child = root.firstChildElement("folder")
        while not child.isNull():
            self.parseFolderElement(child)
            child = child.nextSiblingElement("folder")

        self.itemChanged.connect(self.updateDomElement)

        return True

    def write(self, device):
        indentSize = 4

        out = QtCore.QTextStream(device)
        self.domDocument.save(out, indentSize)
        return True

    def updateDomElement(self, item, column):
        element = self.domElementForItem.get(id(item))
        if not element.isNull():
            if column == 0:
                oldTitleElement = element.firstChildElement("title")
                newTitleElement = self.domDocument.createElement("title")

                newTitleText = self.domDocument.createTextNode(item.text(0))
                newTitleElement.appendChild(newTitleText)

                element.replaceChild(newTitleElement, oldTitleElement)
            else:
                if element.tagName() == "bookmark":
                    element.setAttribute("href", item.text(1))

    def parseFolderElement(self, element, parentItem=None):
        item = self.createItem(element, parentItem)

        title = element.firstChildElement("title").text()
        if title.isEmpty():
            title = QtCore.QObject.tr("Folder")

        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
        item.setIcon(0, self.folderIcon)
        item.setText(0, title)

        folded = (element.attribute("folded") != "no")
        self.setItemExpanded(item, not folded)

        child = element.firstChildElement()
        while not child.isNull():
            if child.tagName() == "folder":
                self.parseFolderElement(child, item)
            elif child.tagName() == "bookmark":
                childItem = self.createItem(child, item)

                title = child.firstChildElement("title").text()
                if title.isEmpty():
                    title = QtCore.QObject.tr("Folder")

                childItem.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
                childItem.setIcon(0, self.bookmarkIcon)
                childItem.setText(0, title)
                childItem.setText(1, child.attribute("href"))
            elif child.tagName() == "separator":
                childItem = self.createItem(child, item)
                childItem.setFlags(item.flags() & ~(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable))
                childItem.setText(0, QtCore.QString(30 * "\xB7"))

            child = child.nextSiblingElement()

    def createItem(self, element, parentItem=None):
        item = QtGui.QTreeWidgetItem()

        if parentItem is not None:
            item = QtGui.QTreeWidgetItem(parentItem)
        else:
            item = QtGui.QTreeWidgetItem(self)

        self.domElementForItem[id(item)] = element
        return item


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    mainWin.open()
    sys.exit(app.exec_())
