#!/usr/bin/env python

"""PyQt4 port of the tools/settingseditor example from Qt v4.x"""

import sys

from PyQt4 import QtCore, QtGui


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.settingsTree = SettingsTree()
        self.setCentralWidget(self.settingsTree)

        self.locationDialog = None

        self.createActions()
        self.createMenus()

        self.autoRefreshAct.setChecked(True)
        self.fallbacksAct.setChecked(True)

        self.setWindowTitle(self.tr("Settings Editor"))
        self.resize(500, 600)

    def openSettings(self):
        if self.locationDialog is None:
            self.locationDialog = LocationDialog(self)

        if self.locationDialog.exec_():
            settings = QtCore.QSettings(self.locationDialog.format(),
                                        self.locationDialog.scope(),
                                        self.locationDialog.organization(),
                                        self.locationDialog.application())
            self.setSettingsObject(settings)
            self.fallbacksAct.setEnabled(True)

    def openIniFile(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self,
                self.tr("Open INI File"), "",
                self.tr("INI Files (*.ini *.conf)"))

        if not fileName.isEmpty():
            settings = QtCore.QSettings(fileName, QtCore.QSettings.IniFormat)
            self.setSettingsObject(settings)
            self.fallbacksAct.setEnabled(False)

    def openPropertyList(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self,
                self.tr("Open Property List"), "",
                self.tr("Property List Files (*.plist)"))

        if not fileName.isEmpty():
            settings = QtCore.QSettings(fileName, QtCore.QSettings.NativeFormat)
            self.setSettingsObject(settings)
            self.fallbacksAct.setEnabled(False)

    def openRegistryPath(self):
        path = QtGui.QInputDialog.getText(self, self.tr("Open Registry Path"),
                self.tr("Enter the path in the Windows registry:"),
                QtGui.QLineEdit.Normal, "HKEY_CURRENT_USER\\")

        if not path.isEmpty():
            settings = QtCore.QSettings(path, QtCore.QSettings.NativeFormat)
            self.setSettingsObject(settings)
            self.fallbacksAct.setEnabled(False)

    def about(self):
        QtGui.QMessageBox.about(self, self.tr("About Settings Editor"),
                self.tr("The <b>Settings Editor</b> example shows how to "
                        "access application settings using Qt."))

    def createActions(self):
        self.openSettingsAct = QtGui.QAction(self.tr("&Open Application Settings..."), self)
        self.openSettingsAct.setShortcut(self.tr("Ctrl+O"))
        self.openSettingsAct.triggered.connect(self.openSettings)

        self.openIniFileAct = QtGui.QAction(self.tr("Open I&NI File..."), self)
        self.openIniFileAct.setShortcut(self.tr("Ctrl+N"))
        self.openIniFileAct.triggered.connect(self.openIniFile)

        self.openPropertyListAct = QtGui.QAction(self.tr("Open Mac &Property List..."), self)
        self.openPropertyListAct.setShortcut(self.tr("Ctrl+P"))
        self.openPropertyListAct.triggered.connect(self.openPropertyList)
        if sys.platform != 'darwin':
            self.openPropertyListAct.setEnabled(False)

        self.openRegistryPathAct = QtGui.QAction(self.tr("Open Windows &Registry Path..."), self)
        self.openRegistryPathAct.setShortcut(self.tr("Ctrl+G"))
        self.openRegistryPathAct.triggered.connect(self.openRegistryPath)
        if sys.platform != 'win32':
            self.openRegistryPathAct.setEnabled(False)

        self.refreshAct = QtGui.QAction(self.tr("&Refresh"), self)
        self.refreshAct.setShortcut(self.tr("Ctrl+R"))
        self.refreshAct.setEnabled(False)
        self.refreshAct.triggered.connect(self.settingsTree.refresh)

        self.exitAct = QtGui.QAction(self.tr("E&xit"), self)
        self.exitAct.setShortcut(self.tr("Ctrl+Q"))
        self.exitAct.triggered.connect(self.close)

        self.autoRefreshAct = QtGui.QAction(self.tr("&Auto-Refresh"), self)
        self.autoRefreshAct.setShortcut(self.tr("Ctrl+A"))
        self.autoRefreshAct.setCheckable(True)
        self.autoRefreshAct.setEnabled(False)
        self.autoRefreshAct.triggered.connect(self.settingsTree.setAutoRefresh)
        self.autoRefreshAct.triggered.connect(self.refreshAct.setDisabled)

        self.fallbacksAct = QtGui.QAction(self.tr("&Fallbacks"), self)
        self.fallbacksAct.setShortcut(self.tr("Ctrl+F"))
        self.fallbacksAct.setCheckable(True)
        self.fallbacksAct.setEnabled(False)
        self.fallbacksAct.triggered.connect(self.settingsTree.setFallbacksEnabled)

        self.aboutAct = QtGui.QAction(self.tr("&About"), self)
        self.aboutAct.triggered.connect(self.about)

        self.aboutQtAct = QtGui.QAction(self.tr("About &Qt"), self)
        self.aboutQtAct.triggered.connect(QtGui.qApp.aboutQt)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu(self.tr("&File"))
        self.fileMenu.addAction(self.openSettingsAct)
        self.fileMenu.addAction(self.openIniFileAct)
        self.fileMenu.addAction(self.openPropertyListAct)
        self.fileMenu.addAction(self.openRegistryPathAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.refreshAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.optionsMenu = self.menuBar().addMenu(self.tr("&Options"))
        self.optionsMenu.addAction(self.autoRefreshAct)
        self.optionsMenu.addAction(self.fallbacksAct)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu(self.tr("&Help"))
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

    def setSettingsObject(self, settings):
        settings.setFallbacksEnabled(self.fallbacksAct.isChecked())
        self.settingsTree.setSettingsObject(settings)

        self.refreshAct.setEnabled(True)
        self.autoRefreshAct.setEnabled(True)

        niceName = settings.fileName()
        niceName.replace("\\", "/")
        pos = niceName.lastIndexOf("/")
        if pos != -1:
            niceName.remove(0, pos + 1)

        if not settings.isWritable():
            niceName = self.tr("%1 (read only)").arg(niceName)

        self.setWindowTitle(self.tr("%1 - %2")
                            .arg(niceName).arg(self.tr("Settings Editor")))


class LocationDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(LocationDialog, self).__init__(parent)

        self.formatComboBox = QtGui.QComboBox()
        self.formatComboBox.addItem(self.tr("Native"))
        self.formatComboBox.addItem(self.tr("INI"))

        self.scopeComboBox = QtGui.QComboBox()
        self.scopeComboBox.addItem(self.tr("User"))
        self.scopeComboBox.addItem(self.tr("System"))

        self.organizationComboBox = QtGui.QComboBox()
        self.organizationComboBox.addItem(self.tr("Trolltech"))
        self.organizationComboBox.setEditable(True)

        self.applicationComboBox = QtGui.QComboBox()
        self.applicationComboBox.addItem(self.tr("Any"))
        self.applicationComboBox.addItem(self.tr("Application Example"))
        self.applicationComboBox.addItem(self.tr("Assistant"))
        self.applicationComboBox.addItem(self.tr("Designer"))
        self.applicationComboBox.addItem(self.tr("Linguist"))
        self.applicationComboBox.setEditable(True)
        self.applicationComboBox.setCurrentIndex(3)

        formatLabel = QtGui.QLabel(self.tr("&Format:"))
        formatLabel.setBuddy(self.formatComboBox)

        scopeLabel = QtGui.QLabel(self.tr("&Scope:"))
        scopeLabel.setBuddy(self.scopeComboBox)

        organizationLabel = QtGui.QLabel(self.tr("&Organization:"))
        organizationLabel.setBuddy(self.organizationComboBox)

        applicationLabel = QtGui.QLabel(self.tr("&Application:"))
        applicationLabel.setBuddy(self.applicationComboBox)

        self.locationsGroupBox = QtGui.QGroupBox(self.tr("Setting Locations"))

        labels = QtCore.QStringList()
        labels << self.tr("Location") << self.tr("Access")

        self.locationsTable = QtGui.QTableWidget()
        self.locationsTable.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.locationsTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.locationsTable.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.locationsTable.setColumnCount(2)
        self.locationsTable.setHorizontalHeaderLabels(labels)
        self.locationsTable.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.Stretch)
        self.locationsTable.horizontalHeader().resizeSection(1, 180)

        self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)

        self.formatComboBox.activated.connect(self.updateLocationsTable)
        self.scopeComboBox.activated.connect(self.updateLocationsTable)
        self.organizationComboBox.lineEdit().editingFinished.connect(self.updateLocationsTable)
        self.applicationComboBox.lineEdit().editingFinished.connect(self.updateLocationsTable)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        locationsLayout = QtGui.QVBoxLayout()
        locationsLayout.addWidget(self.locationsTable)
        self.locationsGroupBox.setLayout(locationsLayout)

        mainLayout = QtGui.QGridLayout()
        mainLayout.addWidget(formatLabel, 0, 0)
        mainLayout.addWidget(self.formatComboBox, 0, 1)
        mainLayout.addWidget(scopeLabel, 1, 0)
        mainLayout.addWidget(self.scopeComboBox, 1, 1)
        mainLayout.addWidget(organizationLabel, 2, 0)
        mainLayout.addWidget(self.organizationComboBox, 2, 1)
        mainLayout.addWidget(applicationLabel, 3, 0)
        mainLayout.addWidget(self.applicationComboBox, 3, 1)
        mainLayout.addWidget(self.locationsGroupBox, 4, 0, 1, 2)
        mainLayout.addWidget(self.buttonBox, 5, 0, 1, 2)
        self.setLayout(mainLayout)

        self.updateLocationsTable()

        self.setWindowTitle(self.tr("Open Application Settings"))
        self.resize(650, 400)

    def format(self):
        if self.formatComboBox.currentIndex() == 0:
            return QtCore.QSettings.NativeFormat
        else:
            return QtCore.QSettings.IniFormat

    def scope(self):
        if self.scopeComboBox.currentIndex() == 0:
            return QtCore.QSettings.UserScope
        else:
            return QtCore.QSettings.SystemScope

    def organization(self):
        return self.organizationComboBox.currentText()

    def application(self):
        if self.applicationComboBox.currentText() == self.tr("Any"):
            return QtCore.QString("")
        else:
            return self.applicationComboBox.currentText()

    def updateLocationsTable(self):
        self.locationsTable.setUpdatesEnabled(False)
        self.locationsTable.setRowCount(0)

        for i in range(2):
            if i == 0:
                if self.scope() == QtCore.QSettings.SystemScope:
                    continue

                actualScope = QtCore.QSettings.UserScope
            else:
                actualScope = QtCore.QSettings.SystemScope

            for j in range(2):
                if j == 0:
                    if self.application().isEmpty():
                        continue

                    actualApplication = self.application()
                else:
                    actualApplication = QtCore.QString()

                settings = QtCore.QSettings(self.format(), actualScope,
                        self.organization(), actualApplication)

                row = self.locationsTable.rowCount()
                self.locationsTable.setRowCount(row + 1)

                item0 = QtGui.QTableWidgetItem()
                item0.setText(settings.fileName())

                item1 = QtGui.QTableWidgetItem()
                disable = (settings.childKeys().isEmpty() and settings.childGroups().isEmpty())

                if row == 0:
                    if settings.isWritable():
                        item1.setText(self.tr("Read-write"))
                        disable = False
                    else:
                        item1.setText(self.tr("Read-only"))
                    self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setDisabled(disable)
                else:
                    item1.setText(self.tr("Read-only fallback"))

                if disable:
                    item0.setFlags(item0.flags() & ~QtCore.Qt.ItemIsEnabled)
                    item1.setFlags(item1.flags() & ~QtCore.Qt.ItemIsEnabled)

                self.locationsTable.setItem(row, 0, item0)
                self.locationsTable.setItem(row, 1, item1)

        self.locationsTable.setUpdatesEnabled(True)


class SettingsTree(QtGui.QTreeWidget):
    def __init__(self, parent=None):
        super(SettingsTree, self).__init__(parent)

        self.setItemDelegate(VariantDelegate(self))

        labels = QtCore.QStringList()
        labels << self.tr("Setting") << self.tr("Type") << self.tr("Value")
        self.setHeaderLabels(labels)
        self.header().setResizeMode(0, QtGui.QHeaderView.Stretch)
        self.header().setResizeMode(2, QtGui.QHeaderView.Stretch)

        self.settings = None
        self.refreshTimer = QtCore.QTimer()
        self.refreshTimer.setInterval(2000)
        self.autoRefresh = False

        self.groupIcon = QtGui.QIcon()
        self.groupIcon.addPixmap(self.style().standardPixmap(QtGui.QStyle.SP_DirClosedIcon),
                QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.groupIcon.addPixmap(self.style().standardPixmap(QtGui.QStyle.SP_DirOpenIcon),
                QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.keyIcon = QtGui.QIcon()
        self.keyIcon.addPixmap(self.style().standardPixmap(QtGui.QStyle.SP_FileIcon))

        self.refreshTimer.timeout.connect(self.maybeRefresh)

    def setSettingsObject(self, settings):
        self.settings = settings
        self.clear()

        if self.settings is not None:
            self.settings.setParent(self)
            self.refresh()
            if self.autoRefresh:
                self.refreshTimer.start()
        else:
            self.refreshTimer.stop()

    def sizeHint(self):
        return QtCore.QSize(800, 600)

    def setAutoRefresh(self, autoRefresh):
        self.autoRefresh = autoRefresh

        if self.settings is not None:
            if self.autoRefresh:
                self.maybeRefresh()
                self.refreshTimer.start()
            else:
                self.refreshTimer.stop()

    def setFallbacksEnabled(self, enabled):
        if self.settings is not None:
            self.settings.setFallbacksEnabled(enabled)
            self.refresh()

    def maybeRefresh(self):
        if self.state() != QtGui.QAbstractItemView.EditingState:
            self.refresh()

    def refresh(self):
        if self.settings is None:
            return

        # The signal might not be connected.
        try:
            self.itemChanged.disconnect(self.updateSetting)
        except:
            pass

        self.settings.sync()
        self.updateChildItems(None)

        self.itemChanged.connect(self.updateSetting)

    def event(self, event):
        if event.type() == QtCore.QEvent.WindowActivate:
            if self.isActiveWindow() and self.autoRefresh:
                self.maybeRefresh()

        return super(SettingsTree, self).event(event)

    def updateSetting(self, item):
        key = item.text(0)
        ancestor = item.parent()

        while ancestor:
            key.prepend(ancestor.text(0) + "/")
            ancestor = ancestor.parent()

        d = item.data(2, QtCore.Qt.UserRole)
        self.settings.setValue(key, item.data(2, QtCore.Qt.UserRole))

        if self.autoRefresh:
            self.refresh()

    def updateChildItems(self, parent):
        dividerIndex = 0

        for group in self.settings.childGroups():
            childIndex = self.findChild(parent, group, dividerIndex)
            if childIndex != -1:
                child = self.childAt(parent, childIndex)
                child.setText(1, "")
                child.setText(2, "")
                child.setData(2, QtCore.Qt.UserRole, QtCore.QVariant())
                self.moveItemForward(parent, childIndex, dividerIndex)
            else:
                child = self.createItem(group, parent, dividerIndex)

            child.setIcon(0, self.groupIcon)
            dividerIndex += 1

            self.settings.beginGroup(group)
            self.updateChildItems(child)
            self.settings.endGroup()

        for key in self.settings.childKeys():
            childIndex = self.findChild(parent, key, 0)
            if childIndex == -1 or childIndex >= dividerIndex:
                if childIndex != -1:
                    child = self.childAt(parent, childIndex)
                    for i in range(child.childCount()):
                        self.deleteItem(child, i)
                    self.moveItemForward(parent, childIndex, dividerIndex)
                else:
                    child = self.createItem(key, parent, dividerIndex)
                child.setIcon(0, self.keyIcon)
                dividerIndex += 1
            else:
                child = self.childAt(parent, childIndex)

            value = self.settings.value(key)
            if value.type() == QtCore.QVariant.Invalid:
                child.setText(1, "Invalid")
            else:
                child.setText(1, value.typeName())
            child.setText(2, VariantDelegate.displayText(value))
            child.setData(2, QtCore.Qt.UserRole, value)

        while dividerIndex < self.childCount(parent):
            self.deleteItem(parent, dividerIndex)

    def createItem(self, text, parent, index):
        after = None

        if index != 0:
            after = self.childAt(parent, index - 1)

        if parent is not None:
            item = QtGui.QTreeWidgetItem(parent, after)
        else:
            item = QtGui.QTreeWidgetItem(self, after)

        item.setText(0, text)
        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
        return item

    def deleteItem(self, parent, index):
        if parent is not None:
            item = parent.takeChild(index)
        else:
            item = self.takeTopLevelItem(index)
        del item

    def childAt(self, parent, index):
        if parent is not None:
            return parent.child(index)
        else:
            return self.topLevelItem(index)

    def childCount(self, parent):
        if parent is not None:
            return parent.childCount()
        else:
            return self.topLevelItemCount()

    def findChild(self, parent, text, startIndex):
        for i in range(self.childCount(parent)):
            if self.childAt(parent, i).text(0) == text:
                return i
        return -1

    def moveItemForward(self, parent, oldIndex, newIndex):
        for int in range(oldIndex - newIndex):
            self.deleteItem(parent, newIndex)


class VariantDelegate(QtGui.QItemDelegate):
    def __init__(self, parent=None):
        super(VariantDelegate, self).__init__(parent)

        self.boolExp = QtCore.QRegExp()
        self.boolExp.setPattern("true|false")
        self.boolExp.setCaseSensitivity(QtCore.Qt.CaseInsensitive)

        self.byteArrayExp = QtCore.QRegExp()
        self.byteArrayExp.setPattern("[\\x00-\\xff]*")

        self.charExp = QtCore.QRegExp()
        self.charExp.setPattern(".")

        self.colorExp = QtCore.QRegExp()
        self.colorExp.setPattern("\\(([0-9]*),([0-9]*),([0-9]*),([0-9]*)\\)")

        self.doubleExp = QtCore.QRegExp()
        self.doubleExp.setPattern("")

        self.pointExp = QtCore.QRegExp()
        self.pointExp.setPattern("\\((-?[0-9]*),(-?[0-9]*)\\)")

        self.rectExp = QtCore.QRegExp()
        self.rectExp.setPattern("\\((-?[0-9]*),(-?[0-9]*),(-?[0-9]*),(-?[0-9]*)\\)")

        self.signedIntegerExp = QtCore.QRegExp()
        self.signedIntegerExp.setPattern("-?[0-9]*")

        self.sizeExp = QtCore.QRegExp(self.pointExp)

        self.unsignedIntegerExp = QtCore.QRegExp()
        self.unsignedIntegerExp.setPattern("[0-9]*")

        self.dateExp = QtCore.QRegExp()
        self.dateExp.setPattern("([0-9]{,4})-([0-9]{,2})-([0-9]{,2})")

        self.timeExp = QtCore.QRegExp()
        self.timeExp.setPattern("([0-9]{,2}):([0-9]{,2}):([0-9]{,2})")

        self.dateTimeExp = QtCore.QRegExp()
        self.dateTimeExp.setPattern(self.dateExp.pattern() + "T" + self.timeExp.pattern())

    def paint(self, painter, option, index):
        if index.column() == 2:
            value = index.model().data(index, QtCore.Qt.UserRole)
            if not self.isSupportedType(value.type()):
                myOption = QtGui.QStyleOptionViewItem(option)
                myOption.state &= ~QtGui.QStyle.State_Enabled
                super(VariantDelegate, self).paint(painter, myOption, index)
                return

        super(VariantDelegate, self).paint(painter, option, index)

    def createEditor(self, parent, option, index):
        if index.column() != 2:
            return None

        originalValue = index.model().data(index, QtCore.Qt.UserRole)
        if not self.isSupportedType(originalValue.type()):
            return None

        lineEdit = QtGui.QLineEdit(parent)
        lineEdit.setFrame(False)

        valueType = originalValue.type()
        if valueType == QtCore.QVariant.Bool:
            regExp = self.boolExp
        elif valueType == QtCore.QVariant.ByteArray:
            regExp = self.byteArrayExp
        elif valueType == QtCore.QVariant.Char:
            regExp = self.charExp
        elif valueType == QtCore.QVariant.Color:
            regExp = self.colorExp
        elif valueType == QtCore.QVariant.Date:
            regExp = self.dateExp
        elif valueType == QtCore.QVariant.DateTime:
            regExp = self.dateTimeExp
        elif valueType == QtCore.QVariant.Double:
            regExp = self.doubleExp
        elif valueType in (QtCore.QVariant.Int, QtCore.QVariant.LongLong):
            regExp = self.signedIntegerExp
        elif valueType == QtCore.QVariant.Point:
            regExp = self.pointExp
        elif valueType == QtCore.QVariant.Rect:
            regExp = self.rectExp
        elif valueType == QtCore.QVariant.Size:
            regExp = self.sizeExp
        elif valueType == QtCore.QVariant.Time:
            regExp = self.timeExp
        elif valueType in (QtCore.QVariant.UInt, QtCore.QVariant.ULongLong):
            regExp = self.unsignedIntegerExp
        else:
            regExp = QtCore.QRegExp()

        if not regExp.isEmpty():
            validator = QtGui.QRegExpValidator(regExp, lineEdit)
            lineEdit.setValidator(validator)

        return lineEdit

    def setEditorData(self, editor, index):
        value = index.model().data(index, QtCore.Qt.UserRole)
        if editor is not None:
            editor.setText(self.displayText(value))

    def setModelData(self, editor, model, index):
        if not editor.isModified():
            return

        text = QtCore.QString(editor.text())
        validator = editor.validator()
        if validator is not None:
            state, pos = validator.validate(text, 0)
            if state != QtGui.QValidator.Acceptable:
                return

        originalValue = index.model().data(index, QtCore.Qt.UserRole)

        valueType = originalValue.type()
        if valueType == QtCore.QVariant.Char:
            value = QtCore.QVariant(text.at(0))
        elif valueType == QtCore.QVariant.Color:
            self.colorExp.exactMatch(text)
            value = QtCore.QVariant(QtGui.QColor(min(self.colorExp.cap(1).toInt(), 255),
                                                 min(self.colorExp.cap(2).toInt(), 255),
                                                 min(self.colorExp.cap(3).toInt(), 255),
                                                 min(self.colorExp.cap(4).toInt(), 255)))
        elif valueType == QtCore.QVariant.Date:
            date = QtCore.QDate.fromString(text, QtCore.Qt.ISODate)
            if not date.isValid():
                return
            value = QtCore.QVariant(date)
        elif valueType == QtCore.QVariant.DateTime:
            dateTime = QtCore.QDateTime.fromString(text, QtCore.Qt.ISODate)
            if not dateTime.isValid():
                return
            value = QtCore.QVariant(dateTime)
        elif valueType == QtCore.QVariant.Point:
            self.pointExp.exactMatch(text)
            value = QtCore.QVariant(QtCore.QPoint(self.pointExp.cap(1).toInt(),
                                                  self.pointExp.cap(2).toInt()))
        elif valueType == QtCore.QVariant.Rect:
            self.rectExp.exactMatch(text)
            value = QtCore.QVariant(QtCore.QRect(self.rectExp.cap(1).toInt(),
                                                 self.rectExp.cap(2).toInt(),
                                                 self.rectExp.cap(3).toInt(),
                                                 self.rectExp.cap(4).toInt()))
        elif valueType == QtCore.QVariant.Size:
            self.sizeExp.exactMatch(text)
            value = QtCore.QVariant(QtCore.QSize(self.sizeExp.cap(1).toInt(),
                                                 self.sizeExp.cap(2).toInt()))
        elif valueType == QtCore.QVariant.StringList:
            value = QtCore.QVariant(text.split(","))
        elif valueType == QtCore.QVariant.Time:
            time = QtCore.QTime.fromString(text, QtCore.Qt.ISODate)
            if not time.isValid():
                return
            value = QtCore.QVariant(time)
        else:
            value = QtCore.QVariant(text)
            value.convert(originalValue.type())

        model.setData(index, QtCore.QVariant(self.displayText(value)),
                QtCore.Qt.DisplayRole)
        model.setData(index, value, QtCore.Qt.UserRole)

    @staticmethod
    def isSupportedType(valueType):
        return valueType in (QtCore.QVariant.Bool, QtCore.QVariant.ByteArray,
                QtCore.QVariant.Char, QtCore.QVariant.Color,
                QtCore.QVariant.Date, QtCore.QVariant.DateTime,
                QtCore.QVariant.Double, QtCore.QVariant.Int,
                QtCore.QVariant.LongLong, QtCore.QVariant.Point,
                QtCore.QVariant.Rect, QtCore.QVariant.Size,
                QtCore.QVariant.String, QtCore.QVariant.StringList,
                QtCore.QVariant.Time, QtCore.QVariant.UInt,
                QtCore.QVariant.ULongLong)

    @staticmethod
    def displayText(value):
        valueType = value.type()
        if valueType == QtCore.QVariant.Bool:
            return value.toString()
        elif valueType == QtCore.QVariant.ByteArray:
            return value.toString()
        elif valueType == QtCore.QVariant.Char:
            return value.toString()
        elif valueType == QtCore.QVariant.Double:
            return value.toString()
        elif valueType == QtCore.QVariant.Int:
            return value.toString()
        elif valueType == QtCore.QVariant.LongLong:
            return value.toString()
        elif valueType == QtCore.QVariant.String:
            return value.toString()
        elif valueType == QtCore.QVariant.UInt:
            return value.toString()
        elif valueType == QtCore.QVariant.ULongLong:
            return value.toString()
        elif valueType == QtCore.QVariant.Color:
            color = QColor(value)
            return (QtCore.QString("(%1,%2,%3,%4)")
                    .arg(color.red()).arg(color.green())
                    .arg(color.blue()).arg(color.alpha()))
        elif valueType == QtCore.QVariant.Date:
            return value.toDate().toString(QtCore.Qt.ISODate)
        elif valueType == QtCore.QVariant.DateTime:
            return value.toDateTime().toString(QtCore.Qt.ISODate)
        elif valueType == QtCore.QVariant.Invalid:
            return "<Invalid>"
        elif valueType == QtCore.QVariant.Point:
            point = value.toPoint()
            return QtCore.QString("(%1,%2)").arg(point.x()).arg(point.y())
        elif valueType == QtCore.QVariant.Rect:
            rect = value.toRect()
            return (QtCore.QString("(%1,%2,%3,%4)")
                    .arg(rect.x()).arg(rect.y())
                    .arg(rect.width()).arg(rect.height()))
        elif valueType == QtCore.QVariant.Size:
            size = value.toSize()
            return QtCore.QString("(%1,%2)").arg(size.width()).arg(size.height())
        elif valueType == QtCore.QVariant.StringList:
            return value.toStringList().join(",")
        elif valueType == QtCore.QVariant.Time:
            return value.toTime().toString(QtCore.Qt.ISODate)

        return QtCore.QString("<%1>").arg(value.typeName())


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
