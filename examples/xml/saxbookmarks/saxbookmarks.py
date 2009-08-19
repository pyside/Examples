############################################################################
##
## Copyright (C) 2004-2005 Trolltech AS. All rights reserved.
##
## This file is part of the example classes of the Qt Toolkit.
##
## This file may be used under the terms of the GNU General Public
## License version 2.0 as published by the Free Software Foundation
## and appearing in the file LICENSE.GPL included in the packaging of
## this file.  Please review the following information to ensure GNU
## General Public Licensing requirements will be met:
## http://www.trolltech.com/products/qt/opensource.html
##
## If you are unsure which license is appropriate for your use, please
## review the following information:
## http://www.trolltech.com/products/qt/licensing.html or contact the
## sales department at sales@trolltech.com.
##
## This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
## WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
##
############################################################################

from PyQt4 import QtCore, QtGui, QtXml


class XbelGenerator(object):
    def __init__(self, treeWidget):
        self.treeWidget = treeWidget
        self.out = QtCore.QTextStream()

    def write(self, device):
        self.out.setDevice(device)
        self.out.setCodec("UTF-8")
        self.out << "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n" \
                 << "<!DOCTYPE xbel>\n" \
                 << "<xbel version=\"1.0\">\n"

        for i in range(self.treeWidget.topLevelItemCount()):
            self.generateItem(self.treeWidget.topLevelItem(i), 1)

        self.out << "</xbel>\n"
        return True

    def indent(self, depth):
        IndentSize = 4

        return QtCore.QString(IndentSize * depth, QtCore.QChar(' '))

    def escapedText(self, txt):
        result = txt
        result.replace("&", "&amp;")
        result.replace("<", "&lt;")
        result.replace(">", "&gt;")
        return result

    def escapedAttribute(self, txt):
        result = self.escapedText(txt)
        result.replace("\"", "&quot;")
        result.prepend("\"")
        result.append("\"")
        return result

    def generateItem(self, item, depth):
        tagName = item.data(0, QtCore.Qt.UserRole).toString()
        if tagName == "folder":
            folded = (not self.treeWidget.isItemExpanded(item))
            self.out << self.indent(depth) << "<folder folded=\""
            if folded:
                self.out << "yes"
            else:
                self.out << "no"
            self.out << "\">\n"\
                     << self.indent(depth + 1) << "<title>" \
                     << self.escapedText(item.text(0)) \
                     << "</title>\n"

            for i in range(item.childCount()):
                self.generateItem(item.child(i), depth + 1)

            self.out << self.indent(depth) << "</folder>\n"
        elif tagName == "bookmark":
            self.out << self.indent(depth) << "<bookmark"
            if not item.text(1).isEmpty():
                self.out << " href=" \
                         << self.escapedAttribute(item.text(1))
            self.out << ">\n" \
                     << self.indent(depth + 1) << "<title>" \
                     << self.escapedText(item.text(0)) \
                     << "</title>\n" \
                     << self.indent(depth) << "</bookmark>\n"
        elif tagName == "separator":
            self.out << self.indent(depth) << "<separator/>\n"


class XbelHandler(QtXml.QXmlDefaultHandler):
    def __init__(self, treeWidget):
        super(XbelHandler, self).__init__()

        self.treeWidget = treeWidget
        self.folderIcon = QtGui.QIcon()
        self.bookmarkIcon = QtGui.QIcon()
        self.currentText = QtCore.QString()
        self.errorStr = QtCore.QString()

        self.item = None
        self.metXbelTag = False

        style = self.treeWidget.style()

        self.folderIcon.addPixmap(style.standardPixmap(QtGui.QStyle.SP_DirClosedIcon),
                QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.folderIcon.addPixmap(style.standardPixmap(QtGui.QStyle.SP_DirOpenIcon),
                QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.bookmarkIcon.addPixmap(style.standardPixmap(QtGui.QStyle.SP_FileIcon))

    def startElement(self, namespaceURI, localName, qName, attributes):
        if not self.metXbelTag and qName != "xbel":
            self.errorStr = QtGui.qApp.tr("The file is not an XBEL file.")
            return False

        if qName == "xbel":
            version = attributes.value("version")
            if not version.isEmpty() and version != "1.0":
                self.errorStr = QtGui.qApp.tr("The File is not an XBEL version 1.0 file.")
                return False
            self.metXbelTag = True
        elif qName == "folder":
            self.item = self.createChildItem(qName)
            self.item.setFlags(self.item.flags() | QtCore.Qt.ItemIsEditable)
            self.item.setIcon(0, self.folderIcon)
            self.item.setText(0, QtGui.qApp.tr("Folder"))
            folded = (attributes.value("folded") != "no")
            self.treeWidget.setItemExpanded(self.item, (not folded))
        elif qName == "bookmark":
            self.item = self.createChildItem(qName)
            self.item.setFlags(self.item.flags() | QtCore.Qt.ItemIsEditable)
            self.item.setIcon(0, self.bookmarkIcon)
            self.item.setText(0, QtGui.qApp.tr("Unkown title"))
            self.item.setText(1, attributes.value("href"))
        elif qName == "separator":
            self.item = self.createChildItem(qName)
            self.item.setFlags(self.item.flags() & ~QtCore.Qt.ItemIsSelectable)
            self.item.setText(0, QtCore.QString(30, QtCore.QChar(0xB7)))

        self.currentText.clear()
        return True

    def endElement(self, namespaceURI, localName, qName):
        if qName == "title":
            if self.item:
                self.item.setText(0, self.currentText)
        elif qName == "folder" or qName == "bookmark" or qName == "separator":
            self.item = self.item.parent()

        return True

    def characters(self, txt):
        self.currentText += txt
        return True

    def fatalError(self, exception):
        QtGui.QMessageBox.information(self.treeWidget.window(),
                QtGui.qApp.tr("SAX Bookmarks"),
                QtGui.qApp.tr("Parse error at line %1, column %2:\n%3").arg(exception.lineNumber()).arg(exception.columnNumber()).arg(exception.message()))
        return False

    def errorString(self):
        return self.errorStr

    def createChildItem(self, tagName):
        if self.item:
            childItem = QtGui.QTreeWidgetItem(self.item)
        else:
            childItem = QtGui.QTreeWidgetItem(self.treeWidget)

        childItem.setData(0, QtCore.Qt.UserRole, QtCore.QVariant(tagName))
        return childItem


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        labels = QtCore.QStringList()
        labels << self.tr("Title") << self.tr("Location")

        self.treeWidget = QtGui.QTreeWidget()
        self.treeWidget.header().setResizeMode(QtGui.QHeaderView.Stretch)
        self.treeWidget.setHeaderLabels(labels)
        self.setCentralWidget(self.treeWidget)

        self.createActions()
        self.createMenus()

        self.statusBar().showMessage(self.tr("Ready"))

        self.setWindowTitle(self.tr("SAX Bookmarks"))
        self.resize(480, 320)

    def open(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self,
                self.tr("Open Bookmark File"), QtCore.QDir.currentPath(),
                self.tr("XBEL Files (*.xbel *.xml)"))

        if fileName.isEmpty():
            return

        self.treeWidget.clear()

        handler = XbelHandler(self.treeWidget)
        reader = QtXml.QXmlSimpleReader()
        reader.setContentHandler(handler)
        reader.setErrorHandler(handler)

        file = QtCore.QFile(fileName)
        if not file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, self.tr("SAX Bookmarks"),
                    self.tr("Cannot read file %1:\n%2.").arg(fileName).arg(file.errorString()))
            return

        xmlInputSource = QtXml.QXmlInputSource(file)
        if reader.parse(xmlInputSource):
            self.statusBar().showMessage(self.tr("File loaded"), 2000)

    def saveAs(self):
        fileName = QtGui.QFileDialog.getSaveFileName(self,
                self.tr("Save Bookmark File"), QtCore.QDir.currentPath(),
                self.tr("XBEL Files (*.xbel *.xml)"))

        if fileName.isEmpty():
            return

        file = QtCore.QFile(fileName)
        if not file.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, self.tr("SAX Bookmarks"),
                    self.tr("Cannot write file %1:\n%2.").arg(fileName).arg(file.errorString()))
            return

        generator = XbelGenerator(self.treeWidget)
        if generator.write(file):
            self.statusBar().showMessage(self.tr("File saved"), 2000)

    def about(self):
         QtGui.QMessageBox.about(self, self.tr("About SAX Bookmarks"),
                self.tr("The <b>SAX Bookmarks</b> example demonstrates how to "
                        "use Qt's SAX classes to read XML documents and how "
                        "to generate XML by hand."))

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


if __name__ == "__main__":

    import sys

    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    mainWin.open()
    sys.exit(app.exec_())
