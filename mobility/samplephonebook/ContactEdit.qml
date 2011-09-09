
import QtQuick 1.1
import com.nokia.meego 1.0

Page {
    id: contactEdit
    anchors.margins: UiConstants.DefaultMargin
    orientationLock: PageOrientation.LockPortrait


    Flickable {
        anchors.fill: parent
        contentHeight: textFields.height
        Column {
            id: textFields
            anchors.fill: parent
            Label {
                text: "Name"
            }
            TextField {
                id: fieldName
                anchors.left: parent.left
                anchors.right: parent.right
                text: manager.contactData[0]
            }
            Label {
                text: "Phone"
            }
            TextField {
                id: fieldPhone
                text: manager.contactData[1]
                anchors.left: parent.left
                anchors.right: parent.right
            }
            Label {
                text: "Email"
            }
            TextField {
                id: fieldEmail
                text: (manager.emailEnabled ? manager.contactData[2] : "<not supported>")
                readOnly: !manager.emailEnabled
                anchors.left: parent.left
                anchors.right: parent.right
            }
            Label {
                text: "Address"
            }
            TextField {
                id: fieldAddress
                text: (manager.addressEnabled ? manager.contactData[3] : "<not supported>")
                readOnly: !manager.addressEnabled
                anchors.left: parent.left
                anchors.right: parent.right
            }

        }
    }
    Dialog {
        id: errorDialog
        visualParent: contactEdit
        title: Item {
            id: titleField
            height: errorDialog.platformStyle.titleBarHeight
            width: parent.width
            Label {
                id: titleLabel
                anchors.verticalCenter: titleField.verticalCenter
                font.capitalization: Font.MixedCase
                color: "white"
                text: "Error"
            }
        }
        content:Item {
            id: name
            height: childrenRect.height
            Text {
                id: text
                font.pixelSize: 22
                color: "white"
                text: manager.errorMessage
            }
        }
        buttons: ButtonRow {
            platformStyle: ButtonStyle { }
            anchors.horizontalCenter: parent.horizontalCenter
            Button {id: b1; text: "Edit fields"; onClicked: errorDialog.accept()}
            Button {id: b2; text: "Cancel entry"; onClicked: errorDialog.reject()}
        }
    }

    tools: ToolBarLayout {
        id: mainTools
        ToolButton {
            text: "Save"
            onClicked: {
                console.log("Save contact");
                if (!manager.saveContact(fieldName.text, fieldPhone.text, fieldEmail.text, fieldAddress.text)) {
                    errorDialog.open();
                } else {
                    manager.selectContact(-1);
                    pageStack.pop();
                }
            }
        }
        ToolButton {
            text: "Cancel"
            onClicked: {
                console.log("Cancel edit/add")
                manager.selectContact(-1)
                pageStack.pop()
            }
        }
    }


}
