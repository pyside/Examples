import QtQuick 1.1
import com.nokia.meego 1.0

Page {
    id: devicePage
    orientationLock: PageOrientation.LockLandscape
    Flickable {
        id: flickableDevice
        anchors.fill: parent
        flickableDirection: Flickable.VerticalFlick
        contentHeight: columnDevice.height + toolBarLayout.height
        contentWidth: flickableDevice.width
        Column {
            id: columnDevice
            anchors.top: parent.top
            anchors.topMargin: 20
            anchors.left: parent.left
            anchors.leftMargin: 20
            spacing: 25
            ProgressBar {
                id: progressBar
                minimumValue: 0
                maximumValue: 100
                value: 10
                width: parent.width
            }
            Label { text: "Power state" }
            ButtonColumn {
                RadioButton { text: "Unknown power" }
                RadioButton { text: "Battery power" }
                RadioButton { text: "Wall power" }
                RadioButton { text: "Wall Power charging Battery" }
                spacing: 10
            }
            Row { 
                Label { text: "IMEI: "  }
                Label { id: labelIMEI; text: sysinfo.imei }
            }
            Row {
                Label { text: "IMSI: " }
                Label { id: labelIMSI; text: sysinfo.imsi }
            }
            Row {
                Label { text: "Manufacturer: " }
                Label { id: labelManufacturer; text: sysinfo.manufacturer }
            }
            Row {
                Label { text: "Model: " }
                Label { id: labelModel; text: sysinfo.model }
            }
            Row {
                Label { text: "Product: " }
                Label { id: labelProduct; text: sysinfo.product }
            }
            Row {
                Button { id: buttonLock; iconSource: "../general_unlock.png"; checked: sysinfo.deviceLock }
                Label { text: "Device lock"; anchors.verticalCenter: parent.verticalCenter }
            }
            Row {
                Label { text: "Current profile: " }
                Label { id: labelProfile; text: sysinfo.profile }
            }
            Row {
                Label { text: "Input method " }
                Label { id: labelInputMethod; text: sysinfo.inputMethod }
            }
            RadioButton { text: "Bluetooth on"; checked: sysinfo.bluetoothState }
        }
    }
    ScrollDecorator {
        flickableItem: flickableDevice
    }
}
