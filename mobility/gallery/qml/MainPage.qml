

import QtQuick 1.1
import com.nokia.meego 1.0

Page {
    id: mainPage
    anchors.margins: UiConstants.DefaultMargin
    anchors.fill: parent
    orientationLock: PageOrientation.LockLandscape

    Dialog {
        anchors.fill: parent
        id: dlg
        content: Item {
            id: name
            height: 350
            width: parent.width
            ListView {
                clip: true
                id: fileInfoView
                anchors.fill: parent
                model: fileBrowser.fileInfo
                delegate: Label {
                    color: "white"
                    text: modelData
                }
            }
        }
    }
 
    ListView {
        id: mainList
        anchors.fill: parent
        anchors.centerIn: parent
        model: VisualDataModel {
            id: visualData
            model: dirModel
            rootIndex: curIndex

            delegate: Button {
                width: mainList.width
                text: filePath
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        if (model.hasModelChildren) {
                            mainList.model.rootIndex = mainList.model.modelIndex(index)
                        } else {
                            fileBrowser.fileSelected(filePath);
                            dlg.open()
                        }
                    }
                }
            }
        }
    }

    tools: ToolBarLayout {
        id: mainTools
        ToolButton {
            text: "Documents"
            onClicked: {
                mainList.model.rootIndex = fileBrowser.browseDocuments
            }
        }
        ToolButton {
            text: "Audio"
            onClicked: {
                mainList.model.rootIndex = fileBrowser.browseAudio
            }
        }
        ToolButton {
            text: "Images"
            onClicked: {
                mainList.model.rootIndex = fileBrowser.browseImages
            }
        }
        ToolButton {
            text: "Video"
            onClicked: {
                mainList.model.rootIndex = fileBrowser.browseVideos
            }
        }
    }
}
