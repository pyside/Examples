#!/usr/bin/env python

import sys

from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtDeclarative import *
from QtMobility.Gallery import QDocumentGallery, QGalleryProperty, QGalleryQueryRequest

class DocumentPropertiesWidget(QObject):

    def __init__(self, fileInfo, gallery, parent=None):
        QObject.__init__(self, parent)

        self.parent = parent
        self.request = QGalleryQueryRequest(gallery, self)
        self.request.setFilter(QDocumentGallery.filePath.equals(fileInfo))
        self.resultSet = None

        self.propertyKeys = []
        self.dialogContent = []
        self.propertyLabels = {}

        propertyNames = [
                QDocumentGallery.fileName,
                QDocumentGallery.mimeType,
                QDocumentGallery.path,
                QDocumentGallery.fileSize,
                QDocumentGallery.lastModified,
                QDocumentGallery.lastAccessed
        ]

        labels = [
                self.tr('File Name'),
                self.tr('Type'),
                self.tr('Path'),
                self.tr('Size'),
                self.tr('Modified'),
                self.tr('Accessed')
        ]

        self.requestProperties(QDocumentGallery.File, propertyNames, labels)

    def itemsInserted(self, index, count):
        self.resultSet.fetch(0)

        self.metaDataChanged(index, count, [])

        if index == 0 and str(self.request.rootType()) == str(QDocumentGallery.File):
            itemType = self.resultSet.itemType()

            if str(itemType) == str(QDocumentGallery.Audio):
                QTimer.singleShot(0, self.requestAudioProperties)
            elif str(itemType) == str(QDocumentGallery.Document):
                QTimer.singleShot(0, self.requestDocumentProperties)
            elif str(itemType) == str(QDocumentGallery.Image):
                QTimer.singleShot(0, self.requestImageProperties)
            elif str(itemType) == str(QDocumentGallery.Video):
                QTimer.singleShot(0, self.requestVideoProperties)


    def itemsRemoved(self, index, count):
        self.metaDataChanged(index, count, [])

    def metaDataChanged(self, index, count, keys):
        if index == 0:
            if not keys:
                for i, key in enumerate(self.propertyKeys):
                    self.updateValue(i, self.resultSet.propertyKey(str(key)))
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
                QDocumentGallery.duration
        ]

        labels = [
                self.tr('Title'),
                self.tr('Artist'),
                self.tr('Album'),
                self.tr('Album Artist'),
                self.tr('Genre'),
                self.tr('Duration')
        ]

        self.requestProperties(QDocumentGallery.Audio, propertyNames, labels)

    def requestDocumentProperties(self):
        propertyNames = [
                QDocumentGallery.title,
                QDocumentGallery.author,
                QDocumentGallery.pageCount
        ]

        labels = [
                self.tr('Title'),
                self.tr('Author'),
                self.tr('Page Count')
        ]

        self.requestProperties(QDocumentGallery.Document, propertyNames, labels)

    def requestImageProperties(self):
        propertyNames = [
                QDocumentGallery.title,
                QDocumentGallery.width,
                QDocumentGallery.height,
        ]

        labels = [
                self.tr('Title'),
                self.tr('Width'),
                self.tr('Height'),
        ]

        self.requestProperties(QDocumentGallery.Image, propertyNames, labels)

    def requestVideoProperties(self):
        propertyNames = [
                QDocumentGallery.title,
                QDocumentGallery.width,
                QDocumentGallery.height,
                QDocumentGallery.duration
        ]

        labels = [
                self.tr('Title'),
                self.tr('Width'),
                self.tr('Height'),
                self.tr('Duration')
        ]

        self.requestProperties(QDocumentGallery.Video, propertyNames, labels)

    def requestProperties(self, itemType, propertyNames, labels):
        currentPropertyNames = self.request.propertyNames()

        self.request.setRootType(str(itemType))
        self.request.setPropertyNames(map(str, currentPropertyNames + propertyNames))
        self.request.execute()

        self.resultSet = self.request.resultSet()

        if self.resultSet:
            self.resultSet.itemsInserted.connect(self.itemsInserted)
            self.resultSet.itemsRemoved.connect(self.itemsRemoved)
            self.resultSet.metaDataChanged.connect(self.metaDataChanged)

            for i, propertyName in enumerate(currentPropertyNames):
                self.propertyKeys[i] = propertyName

            for i, propertyName in enumerate(propertyNames):
                self.insertRow(i, propertyName, labels[i])

            if self.resultSet.itemCount():
                self.itemsInserted(0, self.resultSet.itemCount())

    def insertRow(self, index, propertyName, label):
        propertyKey = self.resultSet.propertyKey(str(propertyName))

        propertyType = self.resultSet.propertyType(propertyKey)
        propertyAttributes = self.resultSet.propertyAttributes(propertyKey)

        self.dialogContent.insert(index, label)
        self.propertyKeys.insert(index, propertyName)
        self.propertyLabels[str(propertyName)] = label

    def updateValue(self, widgetIndex, propertyKey):
        propertyAttributes = self.resultSet.propertyAttributes(propertyKey)

        value = self.resultSet.metaData(propertyKey)

        data = ""
        if isinstance(value, float) or isinstance(value, int):
            data = str(value)
        elif isinstance(value, QDate):
            data = value.toString()
        elif isinstance(value, QTime):
            data = value.toString()
        elif isinstance(value, QDateTime):
            data = value.toString()
        elif isinstance(value, list):
            data = str('; '.join(value))
        elif isinstance(value, QImage) or isinstance(value, QPixmap):
            data = "Image not supported yet!"
        else:
            data = value

        self.dialogContent[widgetIndex] = self.propertyLabels[str(self.propertyKeys[widgetIndex])] + ": " + data
        self.parent.updateDialog.emit()

class FileBrowser(QObject):

    def __init__(self, parent=None):
        QObject.__init__(self, parent)

        self.curModelIndex = []
        self.gallery = QDocumentGallery(self)
        self.fileSystemModel = QFileSystemModel(self)

        self.rootPath = QDesktopServices.storageLocation(QDesktopServices.HomeLocation)
        self.fileSystemModel.setRootPath(self.rootPath)

        self.fileSystemModel.setFilter(QDir.AllEntries | QDir.NoDotAndDotDot | QDir.AllDirs)
        self.curModelIndex = self.fileSystemModel.index(QDesktopServices.storageLocation(QDesktopServices.DocumentsLocation))
        self.dialogContent = ""

    @Property("QModelIndex", constant=True)
    def browseAudio(self):
        self.curModelIndex = self.fileSystemModel.index(QDesktopServices.storageLocation(QDesktopServices.MusicLocation))
        return self.curModelIndex

    @Property("QModelIndex", constant=True)
    def browseDocuments(self):
        self.curModelIndex = self.fileSystemModel.index(QDesktopServices.storageLocation(QDesktopServices.DocumentsLocation))
        return self.curModelIndex

    @Property("QModelIndex", constant=True)
    def browseImages(self):
        self.curModelIndex = self.fileSystemModel.index(QDesktopServices.storageLocation(QDesktopServices.PicturesLocation))
        return self.curModelIndex

    @Property("QModelIndex", constant=True)
    def browseVideos(self):
        self.curModelIndex = self.fileSystemModel.index(QDesktopServices.storageLocation(QDesktopServices.MoviesLocation))
        return self.curModelIndex

    updateDialog = Signal()

    @Property("QStringList", constant=False, notify=updateDialog)
    def fileInfo(self):
        return self.dialogContent

    @Slot(str)
    def fileSelected(self, fileName):
        self.documentProperties = DocumentPropertiesWidget(fileName, self.gallery, self)
        self.dialogContent = self.documentProperties.dialogContent

def main():
    app = QApplication([])
    view = QDeclarativeView()
    filebrowser = FileBrowser()
    context = view.rootContext()
    context.setContextProperty("fileBrowser", filebrowser)

    url = QUrl('main.qml')
    view.rootContext().setContextProperty("dirModel", filebrowser.fileSystemModel)
    view.rootContext().setContextProperty("curIndex", filebrowser.curModelIndex)
    view.setSource(url)
    view.showFullScreen()

    app.exec_()


if __name__ == '__main__':
    main()
