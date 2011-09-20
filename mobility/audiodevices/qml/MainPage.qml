

import QtQuick 1.1
import com.nokia.meego 1.0

Page {
    id: mainPage
    anchors.margins: UiConstants.DefaultMargin
    orientationLock: PageOrientation.LockLandscape

    function cleanupNearest() {
        codecLabel.text = "None"
        freqLabel.text = "None"
        channelLabel.text = "None"
        typeLabel.text = "None"
        sizeLabel.text = "None"
        endLabel.text = "None"
        resultLabel.text = ""
    }

    Item {
        id: commonButtons
        anchors.top: parent.top
        height: modeBut.height + actualLab.height + testBut.height + 64

        Menu {
            id: modeMenu
            // visualParent is needed to specify the grayed out area.
            visualParent: pageStack
            MenuLayout {
                MenuItem {text: "Input"; onClicked: { modeBut.text = "Input"; audioPlayer.modeChanged("Input"); cleanupNearest() } }
                MenuItem {text: "Output"; onClicked: { modeBut.text = "Output"; audioPlayer.modeChanged("Output"); cleanupNearest() }}
            }
        }

        Column {
            spacing: 20

            Row {
                spacing: 24

                Label {
                    anchors.verticalCenter: modeBut.verticalCenter
                    text : "Mode:"
                }
                Button {
                    id: modeBut
                    text: "Input"
                    onClicked: {
                        modeMenu.open()
                    }
                }

                Label {
                    anchors.verticalCenter: deviceBut.verticalCenter
                    text : "Device:"
                }
                Button {
                    id: deviceBut
                    text: ""
                    onClicked: {
                        pageStack.push(Qt.createComponent("SelectDevice.qml"))
                    }
                    Component.onCompleted: {
                        audioPlayer.modeHasChanged.connect(setDevice)
                    }
                    function setDevice(newName) {
                        deviceBut.text = newName[0]
                    }
                }
            }

            Row {
                spacing: 24
                //anchors.horizontalCenter: parent.horizontalCenter
                Label {
                    anchors.verticalCenter: testBut.verticalCenter
                    text: "TIP: To fail use Channel FAIL."
                }
                Button {
                    id: testBut
                    text: "Click to test"
                    onClicked: {
                        audioPlayer.test();
                    }
                }
                Label {
                    anchors.verticalCenter: testBut.verticalCenter
                    id: resultLabel
                    font.bold: true
                    text: ""
                    Component.onCompleted: {
                        audioPlayer.newResult.connect(setResult)
                    }
                    function setResult(newName) {
                        resultLabel.text = newName
                    }
                }
            }

            Row {
                spacing: 180
                anchors.horizontalCenter: parent.horizontalCenter
                Label {
                    id: actualLab
                    font.bold: true
                    text: "Actual setting"
                }
                Label {
                    font.bold: true
                    text: "Nearest setting"
                }
            }
        } //Column
    } //Item

    Flickable {
        width: 854; height: parent.height - commonButtons.height
        anchors.top: commonButtons.bottom
        contentWidth: pageSt.width; contentHeight: firstCol.height
        clip: true

        PageStack {
            id: pageSt
            Grid {
                id: firstCol
                columns: 3
                spacing: 24

                Label {
                    text : "Codec:"
                }
                Button {
                    id: codecBut
                    text: ""
                    onClicked: {
                        pageStack.push(Qt.createComponent("SelectCodec.qml"))
                    }
                    Component.onCompleted: {
                        audioPlayer.modeHasChanged.connect(setCodec)
                    }
                    function setCodec(newName) {
                        codecBut.text = newName[1]
                    }
                }
                Label {
                    id: codecLabel
                    text: "None"
                    Component.onCompleted: {
                        audioPlayer.newNearest.connect(setCodec)
                    }
                    function setCodec(newName) {
                        codecLabel.text = newName[1]
                    }
                }

                Label {
                    text : "Frequency:"
                }
                Button {
                    id: freqBut
                    text: "source.rec"
                    onClicked: {
                        pageStack.push(Qt.createComponent("SelectFreq.qml"))
                    }
                    Component.onCompleted: {
                        audioPlayer.modeHasChanged.connect(setFreq)
                    }
                    function setFreq(newName) {
                        freqBut.text = newName[2]
                    }
                }
                Label {
                    id: freqLabel
                    text: "None"
                    Component.onCompleted: {
                        audioPlayer.newNearest.connect(setFreq)
                    }
                    function setFreq(newName) {
                        freqLabel.text = newName[2]
                    }
                }

                Label {
                    text : "Channel:"
                }
                Button {
                    id: channelBut
                    text: "source.rec"
                    onClicked: {
                        pageStack.push(Qt.createComponent("SelectChannel.qml"))
                    }
                    Component.onCompleted: {
                        audioPlayer.modeHasChanged.connect(setChannel)
                    }
                    function setChannel(newName) {
                        channelBut.text = newName[3]
                    }
                }
                Label {
                    id: channelLabel
                    text: "None"
                    Component.onCompleted: {
                        audioPlayer.newNearest.connect(setChannel)
                    }
                    function setChannel(newName) {
                        channelLabel.text = newName[3]
                    }
                }

                Label {
                    text : "Sample type:"
                }
                Button {
                    id: typeBut
                    text: "source.rec"
                    onClicked: {
                        pageStack.push(Qt.createComponent("SelectType.qml"))
                    }
                    Component.onCompleted: {
                        audioPlayer.modeHasChanged.connect(setType)
                    }
                    function setType(newName) {
                        typeBut.text = newName[4]
                    }
                }
                Label {
                    id: typeLabel
                    text: "None"
                    Component.onCompleted: {
                        audioPlayer.newNearest.connect(setType)
                    }
                    function setType(newName) {
                        typeLabel.text = newName[4]
                    }
                }

                Label {
                    text : "Sample size:"
                }
                Button {
                    id: sizeBut
                    text: "source.rec"
                    onClicked: {
                        pageStack.push(Qt.createComponent("SelectSize.qml"))
                    }
                    Component.onCompleted: {
                        audioPlayer.modeHasChanged.connect(setSize)
                    }
                    function setSize(newName) {
                        sizeBut.text = newName[5]
                    }
                }
                Label {
                    id: sizeLabel
                    text: "None"
                    Component.onCompleted: {
                        audioPlayer.newNearest.connect(setSize)
                    }
                    function setSize(newName) {
                        sizeLabel.text = newName[5]
                    }
                }

                Label {
                    text : "Endianess:"
                }
                Button {
                    id: endBut
                    text: "source.rec"
                    onClicked: {
                        pageStack.push(Qt.createComponent("SelectEnd.qml"))
                    }
                    Component.onCompleted: {
                        audioPlayer.modeHasChanged.connect(setEnd)
                    }
                    function setEnd(newName) {
                        endBut.text = newName[6]
                    }
                }
                Label {
                    id: endLabel
                    text: "None"
                    Component.onCompleted: {
                        audioPlayer.newNearest.connect(setEnd)
                    }
                    function setEnd(newName) {
                        endLabel.text = newName[6]
                    }
                }
            } //Grid
        } //PageStack
    } //Flickable
}
