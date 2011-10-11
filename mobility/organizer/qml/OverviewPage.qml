
import QtQuick 1.1
import com.nokia.meego 1.0
import com.nokia.extras 1.1

Page {
    id: overviewPage
    anchors.margins: UiConstants.DefaultMargin
    orientationLock: PageOrientation.LockPortrait

    Label {
        anchors.centerIn: parent
        text: "No tasks"
        visible: manager.todos.length == 0
    }

    Flickable {
        anchors.fill: parent
        clip: true

        flickableDirection: Flickable.VerticalFlick
        contentHeight: todoButtons.height
        contentWidth: todoButtons.width

        ButtonColumn {
            id: todoButtons

            // On N9 it seems that displayWidth keeps pointing to the larger
            // side of the screen, even in portrait mode...
            width: screen.displayHeight - 2 * UiConstants.DefaultMargin

            Repeater {
                model: manager.todos
                Button {
                    text: modelData
                    onClicked: {
                        manager.editExistingTodo(index)
                        pageStack.push(Qt.createComponent("TodoEdit.qml"))
                    }
                }
            }
        }
    }

    tools: ToolBarLayout {
        id: mainTools
        ToolButton {
            text: "Add Task"
            onClicked: {
                manager.editNewTodo() // Prepare new todo info
                pageStack.push(Qt.createComponent("TodoEdit.qml"))
            }
        }
    }

}
