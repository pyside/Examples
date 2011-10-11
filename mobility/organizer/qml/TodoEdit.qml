
import QtQuick 1.1
import com.nokia.meego 1.0
import com.nokia.extras 1.1

Page {
    id: editPage
    anchors.margins: UiConstants.DefaultMargin
    orientationLock: PageOrientation.LockPortrait

    property int todoId: -1

    Flickable {
        anchors.fill: parent
        contentHeight: editCol.height
        flickableDirection: Flickable.VerticalFlick

        Column {
            id: editCol

            width: parent.width
            anchors.horizontalCenter: parent.horizontalCenter
            spacing: 10

            Label {
                text: "Subject"
            }

            TextField {
                id: subjectField
                text: manager.todoSubject

                Keys.onReturnPressed: {
                    parent.focus = true;
                }
            }

            Label {
                text: "Start Date"
            }

            Column {
                spacing: 20
                Button {
                    id: selectStartDateButton
                    text: manager.todoStartDateTime[1] + "/" + manager.todoStartDateTime[2] + "/" + manager.todoStartDateTime[0]

                    onClicked: {
                        startDateSelector.day = manager.todoStartDateTime[2];
                        startDateSelector.month = manager.todoStartDateTime[1];
                        startDateSelector.year = manager.todoStartDateTime[0];
                        startDateSelector.open()
                    }

                    DatePickerDialog {
                        id: startDateSelector

                        onAccepted: {
                            manager.setTodoStartDate(year, month, day)
                        }
                    }
                }

                Button {
                    id: selectStartTimeButton
                    text: manager.todoStartDateTime[3]+ ":" + manager.todoStartDateTime[4]

                    onClicked: {
                        startTimeSelector.hour = manager.todoStartDateTime[3];
                        startTimeSelector.minute = manager.todoStartDateTime[4];
                        startTimeSelector.open()
                    }

                    TimePickerDialog {
                        id: startTimeSelector
                        fields: DateTime.Hours | DateTime.Minutes
                        acceptButtonText: "Confirm"
                        rejectButtonText: "Cancel"

                        onAccepted: {
                            manager.setTodoStartTime(hour, minute)
                        }

                    }
                }

            }

            Label {
                text: "Due Date"
            }

            Column {
                spacing: 20
                Button {
                    id: selectDueDateButton
                    text: manager.todoDueDateTime[1] + "/" + manager.todoDueDateTime[2] + "/" + manager.todoDueDateTime[0]

                    onClicked: {
                        dueDateSelector.day = manager.todoDueDateTime[2];
                        dueDateSelector.month = manager.todoDueDateTime[1];
                        dueDateSelector.year = manager.todoDueDateTime[0];
                        dueDateSelector.open()
                    }

                    DatePickerDialog {
                        id: dueDateSelector

                        onAccepted: {
                            manager.setTodoDueDate(year, month, day)
                        }
                    }
                }

                Button {
                    id: selectDueTimeButton
                    text: manager.todoDueDateTime[3]+ ":" + manager.todoDueDateTime[4]

                    onClicked: {
                        dueTimeSelector.hour = manager.todoDueDateTime[3];
                        dueTimeSelector.minute = manager.todoDueDateTime[4];
                        dueTimeSelector.open()
                    }

                    TimePickerDialog {
                        id: dueTimeSelector
                        fields: DateTime.Hours | DateTime.Minutes
                        acceptButtonText: "Confirm"
                        rejectButtonText: "Cancel"

                        onAccepted: {
                            manager.setTodoDueTime(hour, minute)
                        }
                    }
                }

            }

            Label {
                text: "Status"
            }

            Button {
                id: statusButton
                text: statusSelection.model.get(statusSelection.selectedIndex).name

                onClicked: {
                    statusSelection.open();
                }


                SelectionDialog {
                    id: statusSelection
                    titleText: "Select status"
                    selectedIndex: manager.todoStatus

                    model: ListModel {
                        ListElement { name: "Not started" }
                        ListElement { name: "In progress" }
                        ListElement { name: "Complete" }
                    }

                    onAccepted: {
                        manager.todoStatus = statusSelection.selectedIndex;
                    }
                }
            }

            Label {
                text: "Priority"
            }

            Button {
                id: priorityButton
                text: prioritySelection.model.get(prioritySelection.selectedIndex).name

                onClicked: {
                    prioritySelection.open();
                }


                SelectionDialog {
                    id: prioritySelection
                    titleText: "Select priority"
                    selectedIndex: manager.todoPriority

                    model: ListModel {
                        ListElement { name: "Unknown" }
                        ListElement { name: "Highest" }
                        ListElement { name: "Extremely high" }
                        ListElement { name: "Very high" }
                        ListElement { name: "High" }
                        ListElement { name: "Medium" }
                        ListElement { name: "Low" }
                        ListElement { name: "Very low" }
                        ListElement { name: "Extremely low" }
                        ListElement { name: "Lowest" }
                    }

                    onAccepted: {
                        manager.todoPriority = prioritySelection.selectedIndex;
                    }
                }
            }
        }
    }

    tools: ToolBarLayout {
        id: editTools
        ToolButton {
            text: "Save"
            onClicked: {
                console.log("Saving new task")
                manager.todoSubject = subjectField.text; // Other fields are handled by dialog.accept signal
                manager.saveTodo();
                pageStack.pop();
            }
        }
        ToolButton {
            text: "Delete"
            enabled: !manager.isNewTodo
            onClicked: {
                console.log("Deleting todo.");
                manager.deleteCurrent();
                pageStack.pop();
            }
        }
        ToolButton {
            text: "Cancel"
            onClicked: {
                console.log("Cancel task edit");
                console.log("Is new todo?" + manager.isNewTodo);
                manager.reload();
                pageStack.pop();
            }
        }
    }

}
