import QtQuick 1.1
import com.nokia.meego 1.0

Page {
    id: generalPage
    orientationLock: PageOrientation.LockLandscape
    anchors.margins: UiConstants.DefaultMargin

    Column {
        anchors.fill: parent
        spacing: 25
        Row {
            spacing: 20
            Label { text: "Current language:" }
            Label { id: currentLanguage; text: sysinfo.currentLanguage }
        }
        Row {
            spacing: 20
            Label { text: "Current country:" }
            Label { id: currentCountry; text: "currentCountry" }
        }
        Row {
            spacing: 20
            Label { text: "Available languages:"; anchors.verticalCenter: parent.verticalCenter }
            Button {
                id: languageButton
                text: "Select a language"
                onClicked: {
                    pageStack.push(Qt.createComponent("AvailableLanguages.qml"))
                }
            }
        }
        Row {
            spacing: 20
            Label { text: "Version"; anchors.verticalCenter: parent.verticalCenter }
            Button {
                id: versionButton
                text: "Select version"
                onClicked: pageStack.push(Qt.createComponent("AvailableVersions.qml"))

            }
            TextField {
                text: ""
            }
        }

        Row {
            spacing: 20
            Label { text: "Feature supported"; anchors.verticalCenter: parent.verticalCenter }
            Button {
                id: featureButton
                text: "Select feature"
                onClicked: pageStack.push(Qt.createComponent("AvailableFeatures.qml"))
            }
            TextField {
                text: ""
            }
        }
    }
}
