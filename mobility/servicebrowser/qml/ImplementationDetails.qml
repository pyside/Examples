
import QtQuick 1.1
import com.nokia.meego 1.0
import com.nokia.extras 1.1

Page {

    property string implementationSpec: ""
    property int implementationIndex: -1
    property string serviceName: ""
    property int serviceIndex: -1

    id: implementationDetails
    anchors.margins: UiConstants.DefaultMargin
    //orientationLock: PageOrientation.LockPortrait

    Label {
        id: titleLabel
        anchors.top: parent.top
        width: parent.width
        anchors.horizontalCenter: parent.horizontalCenter
        text: "Implementation: " + implementationSpec
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
                model: manager.implementationDetails(implementationSpec, implementationIndex,
                                                    serviceName, serviceIndex);
                Button {
                    width: parent.width
                    text: modelData
                    onClicked: {
                        console.log("Selecting service")
                        //manager.selectService(index)
                    }
                }
            }
        }
    }

    tools: ToolBarLayout {
        id: implementationPageTools
        ToolButton {
            text: "Back"
            onClicked: {
                pageStack.pop();
            }
        }
    }

}
