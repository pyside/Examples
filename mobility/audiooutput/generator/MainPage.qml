

import QtQuick 1.1
import com.nokia.meego 1.0
import com.nokia.extras 1.1

Page {
    id: mainPage
    anchors.margins: rootWindow.pageMargin
    anchors.fill: parent

        Flow {
            anchors.fill: parent

            Flickable {
                width: deviceButtons.width
                height: screen.displayHeight
                contentHeight: deviceButtons.height
                ButtonColumn {
                    id: deviceButtons
                    Repeater {
                        model: deviceModel
                        Button {
                            text: modelData
                            onClicked: {
                                player.deviceChanged(index)
                            }
                        }
                    }
                }
            }

            Column {
                CheckBox {
                    anchors.left: parent.left
                    id: play
                    checked: true
                    text: "Play when checked"
                    onClicked: { player.toggleSuspendResume() }

                    Connections {
                        target: player
                        onPlaybackResumed: {
                            play.checked = true
                        }
                    }
                }

                CheckBox {
                    anchors.left: parent.left
                    id: pushpull
                    checked: true
                    text: "Pull mode when checked"
                    onClicked: { player.toggleMode() }
                }
            }
        }
}
