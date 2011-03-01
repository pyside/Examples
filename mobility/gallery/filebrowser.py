#!/usr/bin/env python

import sys

from PySide.QtCore import Qt, QDir, QDate, QTime, QDateTime, QTimer
from PySide.QtGui import QApplication, QDesktopServices, QFileSystemModel
from PySide.QtGui import QListView, QMainWindow, QWidget, QLineEdit
from PySide.QtGui import QDoubleSpinBox, QSpinBox, QDateTimeEdit, QLabel
from PySide.QtGui import QImage, QPixmap, QFormLayout
from QtMobility.Gallery import QDocumentGallery, QGalleryProperty, QGalleryQueryRequest

class DocumentPropertiesWidget(QWidget):

    def __init__(self, fileInfo, gallery, parent=None, flags=Qt.Widget):
        QWidget.__init__(self, parent, flags)

        self.setLayout(QFormLayout(parent=self))
        self.request = QGalleryQueryRequest(gallery, self)
        self.request.setFilter(QDocumentGallery.filePath.equals(fileInfo.absoluteFilePath()))
        self.resultSet = None

        self.propertyKeys = []
        self.widgets = []

        propertyNames = [
                QDocumentGallery.fileName,
                QDocumentGallery.mimeType,
                QDocumentGallery.path,
                QDocumentGallery.fileSize,
                QDocumentGallery.lastModified,
                QDocumentGallery.lastAccessed,
        ]

        labels = [
                self.tr('File Name'),
                self.tr('Type'),
                self.tr('Path'),
                self.tr('Size'),
                self.tr('Modified'),
                self.tr('Accessed'),
        ]

        self.requestProperties(QDocumentGallery.File, propertyNames, labels)

    def itemsInserted(self, index, count):
        self.resultSet.fetch(0)

        self.metaDataChanged(index, count, [])

        if index == 0 and self.request.rootType() == QDocumentGallery.File:
            itemType = self.resultSet.itemType()

            if itemType == QDocumentGallery.Audio:
                QTimer.singleShot(0, self.requestAudioProperties)
            elif itemType == QDocumentGallery.Document:
                QTimer.singleShot(0, self.requestDocumentProperties)
            elif itemType == QDocumentGallery.Image:
                QTimer.singleShot(0, self.requestImageProperties)
            elif itemType == QDocumentGallery.Video:
                QTimer.singleShot(0, self.requestVideoProperties)


    def itemsRemoved(self, index, count):
        self.metaDataChanged(index, count, [])

    def metaDataChanged(self, index, count, keys):
        if index == 0:
            if not keys:
                for i, key in enumerate(self.propertyKeys):
                    self.updateValue(i, key)
            else:
                for key in keys:
                    i = self.propertyKeys.index(key)
                    if i >= 0:
                        self.updateValue(i, key)

    def requestAudioProperties(self):
        propertyNames = [
                QDocumentGallery.title,
                QDocumentGallery.artist,
                QDocumentGallery.albumTitle,
                QDocumentGallery.albumArtist,
                QDocumentGallery.genre,
                QDocumentGallery.duration,
        ]

        labels = [
                self.tr('Title'),
                self.tr('Artist'),
                self.tr('Album'),
                self.tr('Album Artist'),
                self.tr('Genre'),
                self.tr('Duration'),
        ]

        self.requestProperties(QDocumentGallery.Audio, propertyNames, labels)

    def requestDocumentProperties(self):
        propertyNames = [
                QDocumentGallery.title,
                QDocumentGallery.author,
                QDocumentGallery.pageCount,
        ]

        labels = [
                self.tr('Title'),
                self.tr('Author'),
                self.tr('Page Count'),
        ]

        self.requestProperties(QDocumentGallery.Document, propertyNames, labels)

    def requestImageProperties(self):
        propertyNames = [
                QDocumentGallery.title,
                QDocumentGallery.width,
                QDocumentGallery.height,
                QDocumentGallery.keywords,
        ]

        labels = [
                self.tr('Title'),
                self.tr('Width'),
                self.tr('Height'),
                self.tr('Keywords'),
        ]

        self.requestProperties(QDocumentGallery.Image, propertyNames, labels)

    def requestVideoProperties(self):
        propertyNames = [
                QDocumentGallery.title,
                QDocumentGallery.width,
                QDocumentGallery.height,
                QDocumentGallery.duration,
        ]

        labels = [
                self.tr('Title'),
                self.tr('Width'),
                self.tr('Height'),
                self.tr('Duration'),
        ]

        self.requestProperties(QDocumentGallery.Video, propertyNames, labels)

    def requestProperties(self, itemType, propertyNames, labels):
        currentPropertyNames = self.request.propertyNames()

        self.request.setRootType(str(itemType))
        self.request.setPropertyNames(map(str, propertyNames + currentPropertyNames))
        self.request.execute()

        self.resultSet = self.request.resultSet()

        if self.resultSet:
            self.resultSet.itemsInserted.connect(self.itemsInserted)
            self.resultSet.itemsRemoved.connect(self.itemsRemoved)
            self.resultSet.metaDataChanged.connect(self.metaDataChanged)

            for i, propertyName in enumerate(currentPropertyNames):
                self.propertyKeys[i] = self.resultSet.propertyKey(propertyName)

            for i, propertyName in enumerate(propertyNames):
                self.insertRow(i, propertyName, labels[i])

            if self.resultSet.itemCount():
                self.itemsInserted(0, self.resultSet.itemCount())

    def insertRow(self, index, propertyName, label):
        propertyKey = self.resultSet.propertyKey(str(propertyName))

        propertyType = self.resultSet.propertyType(propertyKey)
        propertyAttributes = self.resultSet.propertyAttributes(propertyKey)

        widget = None

        if propertyAttributes & QGalleryProperty.CanWrite:
            if propertyType == str:
                widget = QLineEdit()
            elif propertyType == float:
                widget = QDoubleSpinBox()
            elif propertyType == int:
                widget = QSpinBox()
            elif propertyType == QDateTime:
                widget = QDateTimeEdit()
            else:
                widget = QLabel()
        elif propertyAttributes & QGalleryProperty.CanRead:
            widget = QLabel()

        self.propertyKeys.insert(index, propertyKey)
        self.widgets.insert(index, widget)

        self.layout().insertRow(index, label, widget)

    def updateValue(self, widgetIndex, propertyKey):
        propertyAttributes = self.resultSet.propertyAttributes(propertyKey)

        widget = self.widgets[widgetIndex]
        value = self.resultSet.metaData(propertyKey)

        if propertyAttributes & QGalleryProperty.CanWrite:
            if isinstance(value, str):
                widget.setText(value)
            elif isinstance(value, float) or isinstance(value, int):
                widget.setValue(value)
            elif isinstance(value, QDate):
                widget.setDate(value)
            elif isinstance(value, QTime):
                widget.setTime(value)
            elif isinstance(value, QDateTime):
                widget.setDateTime(value)
            elif isinstance(value, QImage) or isinstance(value, QPixmap):
                widget.setPixmap(value)
            elif isinstance(value, list):
                widget.setText('; '.join(value))
            else:
                widget.setText(value)
        elif propertyAttributes & QGalleryProperty.CanRead:
            if isinstance(value, list):
                widget.setText('; '.join(value))
            else:
                widget.setText(value)

class FileBrowser(QMainWindow):
    """Example file browsing widget. Based of the C++ example."""
    def __init__(self, parent=None, flags=Qt.Widget):
        super(FileBrowser, self).__init__(parent, flags)

        self.gallery = QDocumentGallery(self)
        self.fileSystemModel = QFileSystemModel(self)

        self.rootPath = QDesktopServices.storageLocation(QDesktopServices.HomeLocation)
        self.fileSystemModel.setRootPath(self.rootPath)

        self.view = QListView()
        self.view.setModel(self.fileSystemModel)
        self.view.activated.connect(self.activated)

        self.setCentralWidget(self.view)

        self.menuBar().addAction(self.tr("Documents"), self.browseDocuments)
        self.menuBar().addAction(self.tr("Audio"), self.browseAudio)
        self.menuBar().addAction(self.tr("Images"), self.browseImages)
        self.menuBar().addAction(self.tr("Videos"), self.browseVideos)

        self.browseDocuments()

    def activated(self, index):
        fileInfo = self.fileSystemModel.fileInfo(index)

        if fileInfo.isDir() and fileInfo.fileName() != '.':
            if fileInfo.fileName() == '..':
                parent = self.view.rootIndex().parent()

                fileInfo = self.fileSystemModel.fileInfo(parent)

                if fileInfo.absoluteFilePath() == self.rootPath:
                    self.fileSystemModel.setFilter(QDir.AllEntries | QDir.NoDotAndDotDot | QDir.AllDirs)

                self.view.setRootIndex(parent)

            else:
                self.fileSystemModel.setFilter(QDir.AllEntries | QDir.AllDirs)
                self.view.setRootIndex(index)

            self.setWindowTitle(fileInfo.fileName())
        else:
            if fileInfo.fileName() == '.':
                fileInfo = self.fileSystemModel.fileInfo(self.view.rootIndex())

            widget = DocumentPropertiesWidget(fileInfo, self.gallery, self)
            widget.setWindowFlags(self.window().windowFlags() | Qt.Dialog)
            widget.setAttribute(Qt.WA_DeleteOnClose)
            widget.setWindowModality(Qt.WindowModal)
            widget.show()

    def browseAudio(self):
        self.rootPath = QDesktopServices.storageLocation(QDesktopServices.MusicLocation)
        self.fileSystemModel.setFilter(QDir.AllEntries | QDir.NoDotAndDotDot | QDir.AllDirs)
        self.view.setRootIndex(self.fileSystemModel.index(self.rootPath))
        self.setWindowTitle(self.tr("Audio"))

    def browseDocuments(self):
        self.rootPath = QDesktopServices.storageLocation(QDesktopServices.DocumentsLocation)
        self.fileSystemModel.setFilter(QDir.AllEntries | QDir.NoDotAndDotDot | QDir.AllDirs)
        self.view.setRootIndex(self.fileSystemModel.index(self.rootPath))
        self.setWindowTitle(self.tr("Documents"))

    def browseImages(self):
        self.rootPath = QDesktopServices.storageLocation(QDesktopServices.PicturesLocation)
        self.fileSystemModel.setFilter(QDir.AllEntries | QDir.NoDotAndDotDot | QDir.AllDirs)
        self.view.setRootIndex(self.fileSystemModel.index(self.rootPath))
        self.setWindowTitle(self.tr("Images"))

    def browseVideos(self):
        self.rootPath = QDesktopServices.storageLocation(QDesktopServices.MoviesLocation)
        self.fileSystemModel.setFilter(QDir.AllEntries | QDir.NoDotAndDotDot | QDir.AllDirs)
        self.view.setRootIndex(self.fileSystemModel.index(self.rootPath))
        self.setWindowTitle(self.tr("Videos"))


def main():

    app = QApplication([])
    widget = FileBrowser()

    widget.show()

    return app.exec_()

if __name__ == '__main__':
    main()
