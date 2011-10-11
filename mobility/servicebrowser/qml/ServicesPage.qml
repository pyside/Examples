

import QtQuick 1.1
import com.nokia.meego 1.0
import com.nokia.extras 1.1

Page {
    id: servicePage
    anchors.margins: UiConstants.DefaultMargin
    //orientationLock: PageOrientation.LockPortrait

    Label {
        id: titleLabel
        anchors.top: parent.top
        anchors.horizontalCenter: parent.horizontalCenter
        text: "Services available"
    }

    Flickable {
        anchors.top: titleLabel.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        width: parent.width
        contentHeight: servicesButtons.height

        ButtonColumn {
            id: servicesButtons
            width: parent.width
            anchors.horizontalCenter: parent.horizontalCenter
            Repeater {
                model: manager.servicesNames
                Button {
                    text: modelData
                    onClicked: {
                        console.log("Selecting service")
                        pageStack.push(Qt.createComponent("ServiceImplementations.qml"),
                                                            { serviceName: modelData,
                                                              serviceIndex: index })
                    }
                }
            }
        }
    }

    /*tools: ToolBarLayout {
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
    }*/

}
