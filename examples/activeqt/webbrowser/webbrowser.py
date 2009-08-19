#############################################################################
## Copyright (C) 1992-2006 Trolltech ASA. All rights reserved.
##
## This file is part of the example classes of the Qt Toolkit.
##
## Licensees holding a valid Qt License Agreement may use this file in
## accordance with the rights, responsibilities and obligations
## contained therein.  Please consult your licensing agreement or
## contact sales@trolltech.com if any conditions of this licensing
## agreement are not clear to you.
##
## Further information about Qt licensing is available at:
## http://www.trolltech.com/products/qt/licensing.html or by
## contacting info@trolltech.com.
##
## This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
## WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
##
#############################################################################

import sys

from PyQt4 import QtCore, QtGui, QAxContainer

from ui_mainwindow import Ui_MainWindow


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    # Maintain the list of browser windows so that they do not get garbage
    # collected.
    _window_list = []

    def __init__(self):
        super(MainWindow, self).__init__()

        MainWindow._window_list.append(self)

        self.setupUi(self)

        # Qt Designer (at least to v4.2.1) can't handle arbitrary widgets in a
        # QToolBar - even though uic can, and they are in the original .ui
        # file.  Therefore we manually add the problematic widgets.
        self.lblAddress = QtGui.QLabel("Address", self.tbAddress)
        self.tbAddress.insertWidget(self.actionGo, self.lblAddress)
        self.addressEdit = QtGui.QLineEdit(self.tbAddress)
        self.tbAddress.insertWidget(self.actionGo, self.addressEdit)

        self.addressEdit.returnPressed.connect(self.actionGo.trigger)
        QtCore.QObject.connect(self.actionBack, QtCore.SIGNAL('triggered()'),
                self.WebBrowser, QtCore.SLOT('GoBack()'))
        QtCore.QObject.connect(self.actionForward, QtCore.SIGNAL('triggered()'),
                self.WebBrowser, QtCore.SLOT('GoForward()'))
        QtCore.QObject.connect(self.actionStop, QtCore.SIGNAL('triggered()'),
                self.WebBrowser, QtCore.SLOT('Stop()'))
        QtCore.QObject.connect(self.actionRefresh, QtCore.SIGNAL('triggered()'),
                self.WebBrowser, QtCore.SLOT('Refresh()'))
        QtCore.QObject.connect(self.actionHome, QtCore.SIGNAL('triggered()'),
                self.WebBrowser, QtCore.SLOT('GoHome()'))
        QtCore.QObject.connect(self.actionSearch, QtCore.SIGNAL('triggered()'),
                self.WebBrowser, QtCore.SLOT('GoSearch()'))

        self.pb = QtGui.QProgressBar(self.statusBar())
        self.pb.setTextVisible(False)
        self.pb.hide()
        self.statusBar().addPermanentWidget(self.pb)

        self.WebBrowser.dynamicCall('GoHome()')

    def closeEvent(self, e):
        MainWindow._window_list.remove(self)
        e.accept()

    def on_WebBrowser_TitleChange(self, title):
        self.setWindowTitle("Qt WebBrowser - " + title)

    def on_WebBrowser_ProgressChange(self, a, b):
        if a <= 0 or b <= 0:
            self.pb.hide()
            return

        self.pb.show()
        self.pb.setRange(0, b)
        self.pb.setValue(a)

    def on_WebBrowser_CommandStateChange(self, cmd, on):
        if cmd == 1:
            self.actionForward.setEnabled(on)
        elif cmd == 2:
            self.actionBack.setEnabled(on)

    def on_WebBrowser_BeforeNavigate(self):
        self.actionStop.setEnabled(True)

    def on_WebBrowser_NavigateComplete(self, _):
        self.actionStop.setEnabled(False)

    @QtCore.pyqtSlot()
    def on_actionGo_triggered(self):
        self.WebBrowser.dynamicCall('Navigate(const QString&)',
                QtCore.QVariant(self.addressEdit.text()))

    @QtCore.pyqtSlot()
    def on_actionNewWindow_triggered(self):
        window = MainWindow()
        window.show()
        if self.addressEdit.text().isEmpty():
            return;

        window.addressEdit.setText(self.addressEdit.text())
        window.actionStop.setEnabled(True)
        window.on_actionGo_triggered()

    @QtCore.pyqtSlot()
    def on_actionAbout_triggered(self):
        QtGui.QMessageBox.about(self, self.tr("About WebBrowser"),
                self.tr("This Example has been created using the ActiveQt integration into Qt Designer.\n"
                        "It demonstrates the use of QAxWidget to embed the Internet Explorer ActiveX\n"
                        "control into a Qt application."))

    @QtCore.pyqtSlot()
    def on_actionAboutQt_triggered(self):
        QtGui.QMessageBox.aboutQt(self, self.tr("About Qt"))


if __name__ == "__main__":
    a = QtGui.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(a.exec_())
