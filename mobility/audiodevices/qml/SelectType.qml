
import QtQuick 1.1
import com.nokia.meego 1.0

Page {
    id: selectDevice
    anchors.margins: UiConstants.DefaultMargin
    orientationLock: PageOrientation.LockLandscape

    ListView {
        anchors.fill: parent
        anchors.centerIn: parent
        model: audioPlayer.availableTypes
        delegate: Button {
            text: modelData
            onClicked: {
                audioPlayer.typeChanged(modelData)
                typeBut.text = modelData
                cleanupNearest()
                pageStack.pop()
            }
        }
    }

    tools: ToolBarLayout {
        id: mainTools
        ToolButton {
            text: "Cancel"
            onClicked: {
                pageStack.pop()
            }
        }
    }
}

