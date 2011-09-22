import QtQuick 1.1
import com.nokia.meego 1.0

Page {
    id: tabBarPage
    anchors.margins: UiConstants.DefaultMargin
    orientationLock: PageOrientation.LockLandscape

    tools: ToolBarLayout {
        id: toolBarLayout
        ButtonRow {
            platformStyle: TabButtonStyle { }
            TabButton { text: "General";  tab: generalTab }
            TabButton { text: "Device";  tab: deviceTab }
            TabButton { text: "Display";  tab: displayTab }
            TabButton { text: "Storage";  tab: storageTab }
            TabButton { text: "Network";  tab: networkTab }
            TabButton { text: "Screen saver";  tab: screenSaverTab }
        }
    }
    TabGroup {
        anchors.fill: parent
        currentTab: generalTab
        GeneralPage { id: generalTab }
        DevicePage { id: deviceTab }
        DisplayPage { id: displayTab }
        StoragePage { id: storageTab }
        NetworkPage { id: networkTab }
        ScreenSaverPage { id: screenSaverTab }
    }
}
