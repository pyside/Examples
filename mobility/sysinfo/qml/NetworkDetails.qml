import QtQuick 1.1
import com.nokia.meego 1.0
import com.nokia.extras 1.1

Sheet {

    id: sheet

    property string networkMode: ""

    acceptButtonText: "Close"
    rejectButtonText: ""

    title: Label {
        text: "Details for network mode " + sheet.networkMode
    }

    content: Flickable {
        anchors.fill: parent
        anchors.margins: UiConstants.DefaultMargin
        contentWidth: col.width
        contentHeight: col.height
        flickableDirection: Flickable.VerticalFlick

        Column {
            id: col

            anchors.top: parent.top
//            anchors.left: parent.left
//            anchors.right: parent.right
            spacing: 10

            Label {
                text: "Network status: " + sysinfo.networkStatus(networkMode)
            }

            Label {
                text: "Network name: " + sysinfo.networkName(networkMode)
            }

            Label {
                text: "Interface name: " + sysinfo.networkInterfaceName(networkMode)
            }

            Label {
                text: "MAC Address: " + sysinfo.networkMacAddress(networkMode)
            }

            Row {
                anchors.left: col.left
                anchors.right: col.right

                spacing: 10
                Label {
                    text: "Signal strength:"
                }

                ProgressBar {
                    width: 600
                    minimumValue: -1
                    maximumValue: 100
                    value: sysinfo.networkSignalStrength(networkMode)
                }
            }
        }
    }
}
