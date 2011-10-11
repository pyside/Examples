
import QtQuick 1.1
import com.nokia.meego 1.0
import com.nokia.extras 1.1

Page {

    property string serviceName: ""
    property int serviceIndex: -1

    id: serviceImplementations
    anchors.margins: UiConstants.DefaultMargin
    //orientationLock: PageOrientation.LockPortrait

    Label {
        id: titleLabel
        anchors.top: parent.top
        anchors.horizontalCenter: parent.horizontalCenter
        text: "Service: " + serviceName
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
                id: buttonRepeater
                model: manager.serviceImplementations(serviceName, serviceIndex)

                HoldButton {
                    text: modelData
                    // TODO Getting some "Unable to assing undefined value" at this line when
                    // setting model to a different list (line 73), but the example is working
                    // so far.
                    width: parent.width

                    onHeld: {
                        setDefaultDialog.titleText = "Change default implementation";
                        setDefaultDialog.message = "Set " + modelData + " as default?";
                        setDefaultDialog.index = index;
                        setDefaultDialog.open();
                    }

                    onClickedWithoutHold: {
                        pageStack.push(Qt.createComponent("ImplementationDetails.qml"),
                                    { implementationSpec: modelData,
                                        implementationIndex: index,
                                        serviceName: serviceName,
                                        serviceIndex: serviceIndex
                                    });

                    }
                }
            }
        }
    }

    QueryDialog {
        property int index: -1

        id: setDefaultDialog
        acceptButtonText: "Yes"
        rejectButtonText: "No"

        onAccepted: {
            console.log("Accepted");
            manager.setDefault(index);
            buttonRepeater.model = manager.serviceImplementations(serviceName, serviceIndex)
        }

        onRejected: {
            console.log("Rejected");
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
