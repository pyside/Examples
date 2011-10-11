import QtQuick 1.1
import com.nokia.meego 1.0

Page {
    id: displayPage
    anchors.margins: UiConstants.DefaultMargin
    orientationLock: PageOrientation.LockLandscape
    Flickable {
        id: flickableDisplay
        anchors.fill: parent
        flickableDirection: Flickable.VerticalFlick
        contentHeight: columnDisplay.height + toolBarLayout.height
        contentWidth: flickableDisplay.width
        Column {
            id: columnDisplay
            anchors.top: parent.top
            anchors.topMargin: 20
            anchors.left: parent.left
            anchors.leftMargin: 20
            spacing: 25
            Row {
                Label { text: "Brightness: "  }
                Label { id: labelBrightness; text: sysinfo.displayBrightness }
            }
            Row {
                Label { text: "Color depth: " }
                Label { id: labelColorDepth; text: sysinfo.colorDepth }
            }
/*          Row {
                Label { text: "Orientation: " }
                Label { id: labelOrientation; text: "" }
            }
            Row {
                Label { text: "Contrast: " }
                Label { id: labelContrast; text: "" }
            }
            Row {
                Label { text: "DPI Width: " }
                Label { id: labelDPIWidth; text: "" }
            }
            Row {
                Label { text: "DPI Height: " }
                Label { id: labelDPIHeight; text: "" }
            }
            Row {
                Label { text: "Physical Width:  " }
                Label { id: labelPhysicalWidth; text: "" }
            }
            Row {
                Label { text: "Physical Height: " }
                Label { id: labelPhysicalHeight; text: "" }
            }*/
        }
    }
    ScrollDecorator {
        flickableItem: flickableDisplay
    }
}
