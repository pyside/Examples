
import QtQuick 1.1
import com.nokia.meego 1.0

Page {
    id: selectBackend
    anchors.margins: UiConstants.DefaultMargin
    orientationLock: PageOrientation.LockPortrait


    ListView {
        anchors.fill: parent
        anchors.centerIn: parent
        model: manager.availableManagers
        delegate: Button {
            text: modelData
            onClicked: {
                manager.selectManager(modelData)
                pageStack.pop()
            }
        }
    }

    tools: ToolBarLayout {
        id: mainTools
        ToolButton {
            text: "Select"
            onClicked: {
                console.log("Selected new backend")
                pageStack.pop()
            }
        }
        ToolButton {
            text: "Cancel"
            onClicked: {
                console.log("Cancel edit/add")
                pageStack.pop()
            }
        }
    }
}
