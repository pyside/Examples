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
                Label { id: labelIMEI; text: dataModel.imei }
            }
            Row {
                Label { text: "IMSI: " }
                Label { id: labelIMSI; text: dataModel.imsi }
            }
            Row {
                Label { text: "Manufacturer: " }
                Label { id: labelManufacturer; text: dataModel.manufacturer }
            }
            Row {
                Label { text: "Model: " }
                Label { id: labelModel; text: dataModel.model }
            }
            Row {
                Label { text: "Product: " }
                Label { id: labelProduct; text: dataModel.product }
            }
            Row {
                Button { id: buttonLock; iconSource: "../general_unlock.png"; checked: dataModel.deviceLock }
                Label { text: "Device lock"; anchors.verticalCenter: parent.verticalCenter }
            }
            Row {
                Label { text: "Current profile: " }
                Label { id: labelProfile; text: dataModel.profile }
            }
            Row {
                Label { text: "Input method " }
                Label { id: labelInputMethod; text: dataModel.inputMethod }
            }
            RadioButton { text: "Bluetooth on"; checked: dataModel.bluetoothState }
        }
    }
    ScrollDecorator {
        flickableItem: flickableColumn
    }
}
