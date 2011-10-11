import QtQuick 1.1
import com.nokia.meego 1.0

Page {
    id: availableLanguages
    anchors.margins: UiConstants.DefaultMargin
    orientationLock: PageOrientation.LockPortrait

    ListView {
        anchors.fill: parent
        anchors.centerIn: parent
        model: sysinfo.availableManagers
        delegate: Button {
            text: modelData
            onClicked: {
                languageButton.text = text
                pageStack.pop()
            }
        }
    }
}
