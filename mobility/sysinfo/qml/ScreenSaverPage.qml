import QtQuick 1.1
import com.nokia.meego 1.0

Page {
    id: screenSaverTab
    orientationLock: PageOrientation.LockLandscape
    anchors.margins: UiConstants.DefaultMargin

    RadioButton { text: "Screen saver inhibited"; checked: sysinfo.screenSaverInhibited }
}
