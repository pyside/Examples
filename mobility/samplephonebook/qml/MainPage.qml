

import QtQuick 1.1
import com.nokia.meego 1.0
import com.nokia.extras 1.1

Page {
    id: mainPage
    anchors.margins: UiConstants.DefaultMargin
    orientationLock: PageOrientation.LockPortrait

    Flickable {
        anchors.fill: parent

        ButtonColumn {
            Repeater {
                model: manager.contactsNames
                Button {
                    text: modelData
                    onClicked: {
                        console.log("Editing existing contact")
                        manager.selectContact(index)
                        pageStack.push(Qt.createComponent("ContactEdit.qml"))
                    }
                }
            }
        }
    }

    tools: ToolBarLayout {
        id: mainTools
        ToolButton {
            text: "Add..."
            onClicked: {
                console.log("Add new contact")
                pageStack.push(Qt.createComponent("ContactEdit.qml"))
            }
        }
        ToolButton {
            text: "Select backend..."
            onClicked: {
                pageStack.push(Qt.createComponent("SelectBackend.qml"))
            }
        }
    }

}
