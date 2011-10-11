import QtQuick 1.1
import com.nokia.meego 1.0

Page {

    id: page
    orientationLock: PageOrientation.LockLandscape
    anchors.margins: UiConstants.DefaultMargin

    Flickable {
        id: flickNetwork
        anchors.fill: parent
        flickableDirection: Flickable.VerticalFlick
        contentHeight: colNetwork.height + toolBarLayout.height
        contentWidth: flickNetwork.width

        Column {
            id: colNetwork
            spacing: 20

            ButtonColumn {
                id: columnNetworks
                //anchors.top: parent.top
                //width: parent.width

                Repeater {
                    model: sysinfo.networksNames
                    Button {
                        text: modelData
                        onClicked: {
                            console.log("Getting info for" + modelData);
                            var component = Qt.createComponent("NetworkDetails.qml");
                            if (component.status == Component.Ready) {
                                var networkSheet = component.createObject(page,
                                        {
                                            "networkMode": modelData
                                        });
                                networkSheet.open();
                            } else {
                                console.log("Component not ready");
                            }
                        }
                    }
                }
            }

            // Cell ID stuff
            Label {
                text: "Cell ID: " + sysinfo.cellId()
            }

            Label {
                text: "Location Area Code: " + sysinfo.locationAreaCode()
            }

            Label {
                text: "Current Mobile Country Code: " + sysinfo.currentMCC()
            }

            Label {
                text: "Current Mobile Network Code: " + sysinfo.currentMNC()
            }

            Label {
                text: "Home Mobile Country Code: " + sysinfo.homeMCC()
            }

            Label {
                text: "Home Mobile Network Code: " + sysinfo.homeMNC()
            }

        }

    }

}
