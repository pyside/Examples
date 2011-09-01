

import QtQuick 1.1
import com.nokia.meego 1.0

Page {
    id: mainPage
    anchors.margins: rootWindow.pageMargin

    Flow {
        anchors.top: parent.top
        anchors.right: parent.right
        anchors.left: parent.left
        anchors.margins: 10

        spacing: 10

        Button {
            id: rumble
            text: "Rumble"
            onClicked: effectPlayer.playRumble()
        }

        Button {
            id: ocean
            text: "Ocean"
            onClicked: effectPlayer.playOcean()
        }

        Button {
            id: buttonClick
            text: "Button Click"
            onClicked: effectPlayer.playButtonClick()
        }

        Button {
            id: negativeEffect
            text: "Negative Effect"
            onClicked: effectPlayer.playNegativeEffect()
        }
    }

}
