

import QtQuick 1.1
import com.nokia.meego 1.0

Page {
    id: mainPage
    anchors.margins: rootWindow.pageMargin

    Button {
        id: play
        text: "Play!"
        anchors.fill: parent
        onClicked: player.play()
    }
}
