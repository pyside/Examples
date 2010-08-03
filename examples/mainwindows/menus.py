#!/usr/bin/env python

############################################################################
# 
#  Copyright (C) 2004-2005 Trolltech AS. All rights reserved.
# 
#  This file is part of the example classes of the Qt Toolkit.
# 
#  This file may be used under the terms of the GNU General Public
#  License version 2.0 as published by the Free Software Foundation
#  and appearing in the file LICENSE.GPL included in the packaging of
#  self file.  Please review the following information to ensure GNU
#  General Public Licensing requirements will be met:
#  http://www.trolltech.com/products/qt/opensource.html
# 
#  If you are unsure which license is appropriate for your use, please
#  review the following information:
#  http://www.trolltech.com/products/qt/licensing.html or contact the
#  sales department at sales@trolltech.com.
# 
#  This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
#  WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
# 
############################################################################

from PySide import QtCore, QtGui


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        widget = QtGui.QWidget()
        self.setCentralWidget(widget)

        topFiller = QtGui.QWidget()
        topFiller.setSizePolicy(QtGui.QSizePolicy.Expanding,
                QtGui.QSizePolicy.Expanding)

        self.infoLabel = QtGui.QLabel(
                "<i>Choose a menu option, or right-click to invoke a context menu</i>")
        self.infoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.infoLabel.setFrameStyle(QtGui.QFrame.StyledPanel | QtGui.QFrame.Sunken)

        bottomFiller = QtGui.QWidget()
        bottomFiller.setSizePolicy(QtGui.QSizePolicy.Expanding,
                QtGui.QSizePolicy.Expanding)

        vbox = QtGui.QVBoxLayout()
        vbox.setMargin(5)
        vbox.addWidget(topFiller)
        vbox.addWidget(self.infoLabel)
        vbox.addWidget(bottomFiller)
        widget.setLayout(vbox)

        self.createActions()
        self.createMenus()

        message = "A context menu is available by right-clicking"
        self.statusBar().showMessage(message)

        self.setWindowTitle("Menus")
        self.setMinimumSize(160,160)
        self.resize(480,320)

    def contextMenuEvent(self, event):
        menu = QtGui.QMenu(self)
        menu.addAction(self.cutAct)
        menu.addAction(self.copyAct)
        menu.addAction(self.pasteAct)
        menu.exec_(event.globalPos())

    def newFile(self):
        self.infoLabel.setText("Invoked <b>File|New</b>")

    def open(self):
        self.infoLabel.setText("Invoked <b>File|Open</b>")
        	
    def save(self):
        self.infoLabel.setText("Invoked <b>File|Save</b>")

    def print_(self):
        self.infoLabel.setText("Invoked <b>File|Print</b>")

    def undo(self):
        self.infoLabel.setText("Invoked <b>Edit|Undo</b>")

    def redo(self):
        self.infoLabel.setText("Invoked <b>Edit|Redo</b>")

    def cut(self):
        self.infoLabel.setText("Invoked <b>Edit|Cut</b>")

    def copy(self):
        self.infoLabel.setText("Invoked <b>Edit|Copy</b>")

    def paste(self):
        self.infoLabel.setText("Invoked <b>Edit|Paste</b>")

    def bold(self):
        self.infoLabel.setText("Invoked <b>Edit|Format|Bold</b>")

    def italic(self):
        self.infoLabel.setText("Invoked <b>Edit|Format|Italic</b>")

    def leftAlign(self):
        self.infoLabel.setText("Invoked <b>Edit|Format|Left Align</b>")

    def rightAlign(self):
        self.infoLabel.setText("Invoked <b>Edit|Format|Right Align</b>")

    def justify(self):
        self.infoLabel.setText("Invoked <b>Edit|Format|Justify</b>")

    def center(self):
        self.infoLabel.setText("Invoked <b>Edit|Format|Center</b>")

    def setLineSpacing(self):
        self.infoLabel.setText("Invoked <b>Edit|Format|Set Line Spacing</b>")

    def setParagraphSpacing(self):
        self.infoLabel.setText("Invoked <b>Edit|Format|Set Paragraph Spacing</b>")

    def about(self):
        self.infoLabel.setText("Invoked <b>Help|About</b>")
        QtGui.QMessageBox.about(self, "About Menu",
                "The <b>Menu</b> example shows how to create menu-bar menus "
                "and context menus.")

    def aboutQt(self):
        self.infoLabel.setText("Invoked <b>Help|About Qt</b>")

    def createActions(self):
        self.newAct = QtGui.QAction("&New", self)
        self.newAct.setShortcut(QtGui.QKeySequence.New)
        self.newAct.setStatusTip("Create a new file")
        self.newAct.triggered.connect(self.newFile)

        self.openAct = QtGui.QAction("&Open...", self)
        self.openAct.setShortcut(QtGui.QKeySequence.Open)
        self.openAct.setStatusTip("Open an existing file")
        self.openAct.triggered.connect(self.open)

        self.saveAct = QtGui.QAction("&Save", self)
        self.saveAct.setShortcut(QtGui.QKeySequence.Save)
        self.saveAct.setStatusTip("Save the document to disk")
        self.saveAct.triggered.connect(self.save)

        self.printAct = QtGui.QAction("&Print...", self)
        self.printAct.setShortcut(QtGui.QKeySequence.Print)
        self.printAct.setStatusTip("Print the document")
        self.printAct.triggered.connect(self.print_)

        self.exitAct = QtGui.QAction("E&xit", self)
        self.exitAct.setShortcut("Ctrl+Q")
        self.exitAct.setStatusTip("Exit the application")
        self.exitAct.triggered.connect(self.close)

        self.undoAct = QtGui.QAction("&Undo", self)
        self.undoAct.setShortcut(QtGui.QKeySequence.Undo)
        self.undoAct.setStatusTip("Undo the last operation")
        self.undoAct.triggered.connect(self.undo)

        self.redoAct = QtGui.QAction("&Redo", self)
        self.redoAct.setShortcut(QtGui.QKeySequence.Redo)
        self.redoAct.setStatusTip("Redo the last operation")
        self.redoAct.triggered.connect(self.redo)

        self.cutAct = QtGui.QAction("Cu&t", self)
        self.cutAct.setShortcut(QtGui.QKeySequence.Cut)
        self.cutAct.setStatusTip("Cut the current selection's contents to the clipboard")
        self.cutAct.triggered.connect(self.cut)

        self.copyAct = QtGui.QAction("&Copy", self)
        self.copyAct.setShortcut(QtGui.QKeySequence.Copy)
        self.copyAct.setStatusTip("Copy the current selection's contents to the clipboard")
        self.copyAct.triggered.connect(self.copy)

        self.pasteAct = QtGui.QAction("&Paste", self)
        self.pasteAct.setShortcut(QtGui.QKeySequence.Paste)
        self.pasteAct.setStatusTip("Paste the clipboard's contents into the current selection")
        self.pasteAct.triggered.connect(self.paste)

        self.boldAct = QtGui.QAction("&Bold", self)
        self.boldAct.setCheckable(True)
        self.boldAct.setShortcut("Ctrl+B")
        self.boldAct.setStatusTip("Make the text bold")
        self.boldAct.triggered.connect(self.bold)

        boldFont = self.boldAct.font()
        boldFont.setBold(True)
        self.boldAct.setFont(boldFont)

        self.italicAct = QtGui.QAction("&Italic", self)
        self.italicAct.setCheckable(True)
        self.italicAct.setShortcut("Ctrl+I")
        self.italicAct.setStatusTip("Make the text italic")
        self.italicAct.triggered.connect(self.italic)

        italicFont = self.italicAct.font()
        italicFont.setItalic(True)
        self.italicAct.setFont(italicFont)

        self.setLineSpacingAct = QtGui.QAction("Set &Line Spacing...", self)
        self.setLineSpacingAct.setStatusTip("Change the gap between the lines of a paragraph")
        self.setLineSpacingAct.triggered.connect(self.setLineSpacing)

        self.setParagraphSpacingAct = QtGui.QAction("Set &Paragraph Spacing...", self)
        self.setParagraphSpacingAct.setStatusTip("Change the gap between paragraphs")
        self.setParagraphSpacingAct.triggered.connect(self.setParagraphSpacing)

        self.aboutAct = QtGui.QAction("&About", self)
        self.aboutAct.setStatusTip("Show the application's About box")
        self.aboutAct.triggered.connect(self.about)

        self.aboutQtAct = QtGui.QAction("About &Qt", self)
        self.aboutQtAct.setStatusTip("Show the Qt library's About box")
        self.aboutQtAct.triggered.connect(self.aboutQt)
        self.aboutQtAct.triggered.connect(QtGui.qApp.aboutQt)

        self.leftAlignAct = QtGui.QAction("&Left Align", self)
        self.leftAlignAct.setCheckable(True)
        self.leftAlignAct.setShortcut("Ctrl+L")
        self.leftAlignAct.setStatusTip("Left align the selected text")
        self.leftAlignAct.triggered.connect(self.leftAlign)

        self.rightAlignAct = QtGui.QAction("&Right Align", self)
        self.rightAlignAct.setCheckable(True)
        self.rightAlignAct.setShortcut("Ctrl+R")
        self.rightAlignAct.setStatusTip("Right align the selected text")
        self.rightAlignAct.triggered.connect(self.rightAlign)

        self.justifyAct = QtGui.QAction("&Justify", self)
        self.justifyAct.setCheckable(True)
        self.justifyAct.setShortcut("Ctrl+J")
        self.justifyAct.setStatusTip("Justify the selected text")
        self.justifyAct.triggered.connect(self.justify)

        self.centerAct = QtGui.QAction("&Center", self)
        self.centerAct.setCheckable(True)
        self.centerAct.setShortcut("Ctrl+C")
        self.centerAct.setStatusTip("Center the selected text")
        self.centerAct.triggered.connect(self.center)

        self.alignmentGroup = QtGui.QActionGroup(self)
        self.alignmentGroup.addAction(self.leftAlignAct)
        self.alignmentGroup.addAction(self.rightAlignAct)
        self.alignmentGroup.addAction(self.justifyAct)
        self.alignmentGroup.addAction(self.centerAct)
        self.leftAlignAct.setChecked(True)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.printAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.undoAct)
        self.editMenu.addAction(self.redoAct)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.cutAct)
        self.editMenu.addAction(self.copyAct)
        self.editMenu.addAction(self.pasteAct)
        self.editMenu.addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

        self.formatMenu = self.editMenu.addMenu("&Format")
        self.formatMenu.addAction(self.boldAct)
        self.formatMenu.addAction(self.italicAct)
        self.formatMenu.addSeparator().setText("Alignment")
        self.formatMenu.addAction(self.leftAlignAct)
        self.formatMenu.addAction(self.rightAlignAct)
        self.formatMenu.addAction(self.justifyAct)
        self.formatMenu.addAction(self.centerAct)
        self.formatMenu.addSeparator()
        self.formatMenu.addAction(self.setLineSpacingAct)
        self.formatMenu.addAction(self.setParagraphSpacingAct)


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
