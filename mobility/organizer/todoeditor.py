"""

 Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
 All rights reserved.
 Contact: Nokia Corporation (qt-info@nokia.com)

 This file is part of the Qt Mobility Components.

 $QT_BEGIN_LICENSE:BSD$
 You may use this file under the terms of the BSD license as follows:

 "Redistribution and use in source and binary forms, with or without
 modification, are permitted provided that the following conditions are
 met:
    Redistributions of source code must retain the above copyright
     notice, this list of conditions and the following disclaimer.
    Redistributions in binary form must reproduce the above copyright
     notice, this list of conditions and the following disclaimer in
     the documentation and/or other materials provided with the
     distribution.
    Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
     the names of its contributors may be used to endorse or promote
     products derived from this software without specific prior written
     permission.

 THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
 $QT_END_LICENSE$
"""

from PySide.QtCore import *
from PySide.QtGui import *
from QtMobility.Organizer import *


class TodoEditor(QWidget):
    #signals
    # See bug 657
    #editingFinished = Signal(QOrganizerTodo)
    editingFinished = Signal()

    def __init__(self, parent = None):
        QWidget.__init__(self, parent = None)
        
        self.todo = None
        self.startDateEdit = None
        self.dueDateEdit = None
        self.statusCombo = None
        self.priorityCombo = None
        self.alarmCombo = None
        self.subjectLineEdit = None
        self.descriptionTextEdit = None
        self.doneButton = None
        
        self.setupGui()

    def editTodo(self, newTodo):
        self.todo = newTodo
        self.subjectLineEdit.setText(self.todo.displayLabel())
        self.startDateEdit.setDateTime(self.todo.startDateTime())
        self.dueDateEdit.setDateTime(self.todo.dueDateTime())
        self.priorityCombo.setCurrentIndex(
            self.priorityCombo.findData(self.todo.priority()))
        self.statusCombo.setCurrentIndex(
            self.statusCombo.findData(self.todo.status()))
        self.descriptionTextEdit.setText(self.todo.description())
        if len(self.todo.details(QOrganizerItemVisualReminder.DefinitionName)) != 0:
            reminder = QOrganizerItemVisualReminder(self.todo.detail(QOrganizerItemVisualReminder.DefinitionName))
            seconds = reminder.secondsBeforeStart()
            self.alarmCombo.setCurrentIndex(seconds/(15*60))
        else:
            self.alarmCombo.setCurrentIndex(0)

    def updateSubject(self):
        self.todo.setDisplayLabel(self.subjectLineEdit.text())

    def updateDescription(self):
        self.todo.setDescription(self.descriptionTextEdit.toPlainText())

    def updateDates(self):
        startTime = self.startDateEdit.dateTime()
        dueDateTime = self.dueDateEdit.dateTime()

        self.todo.setStartDateTime(startTime)
        self.todo.setDueDateTime(dueDateTime)
        self.updateAlarm(self.alarmCombo.currentIndex())

    def updateStatus(self, index):
        status = self.statusCombo.itemData(index)
        self.todo.setStatus(QOrganizerTodoProgress.Status(index))

    def updatePriority(self, index):
        priority = self.priorityCombo.itemData(index)
        self.todo.setPriority(QOrganizerItemPriority.Priority(index))
 
    def updateAlarm(self, index):
        seconds = index * (15*60)
        dueDate = self.todo.dueDateTime()
        oldReminder = self.todo.detail(QOrganizerItemVisualReminder.DefinitionName)
        self.todo.removeDetail(oldReminder)
        if seconds == 0:
            return
        reminder = QOrganizerItemVisualReminder()
        reminder.setSecondsBeforeStart(int(seconds))
        self.todo.saveDetail(reminder)

    def finishEditing(self):
        # See bug 657
        #self.editingFinished.emit(self.todo)
        
        self.finishedTodo = self.todo
        self.editingFinished.emit()

    def setupGui(self):
        self.startDateEdit = QDateTimeEdit()
        self.dueDateEdit = QDateTimeEdit()
        self.subjectLineEdit = QLineEdit()
        self.descriptionTextEdit = QTextEdit()
        self.doneButton = QPushButton(self.tr("Done"))
        self.setupCombos()
    
        self.startDateEdit.editingFinished.connect(self.updateDates)
        self.dueDateEdit.editingFinished.connect(self.updateDates)
        self.subjectLineEdit.editingFinished.connect(self.updateSubject)
        self.descriptionTextEdit.textChanged.connect(self.updateDescription)
        self.statusCombo.activated[int].connect(self.updateStatus)
        self.priorityCombo.activated[int].connect(self.updatePriority)
        self.alarmCombo.activated[int].connect(self.updateAlarm)
        self.doneButton.clicked.connect(self.finishEditing)
    
        layout = QVBoxLayout()
        layout.addWidget(QLabel(self.tr("Subject:")))
        layout.addWidget(self.subjectLineEdit)
        layout.addWidget(QLabel(self.tr("Start Date:")))
        layout.addWidget(self.startDateEdit)
        layout.addWidget(QLabel(self.tr("Due Date:")))
        layout.addWidget(self.dueDateEdit)
        layout.addWidget(QLabel(self.tr("Status:")))
        layout.addWidget(self.statusCombo)
        layout.addWidget(QLabel(self.tr("Priority:")))
        layout.addWidget(self.priorityCombo)
        layout.addWidget(QLabel(self.tr("Alarm:")))
        layout.addWidget(self.alarmCombo)
        layout.addWidget(QLabel(self.tr("Description")))
        layout.addWidget(self.descriptionTextEdit)
        layout.addWidget(self.doneButton)
    
        self.setLayout(layout)

    def setupCombos(self):
        self.priorityCombo =  QComboBox()
        self.priorityCombo.addItem("Unknown", QOrganizerItemPriority.UnknownPriority)
        self.priorityCombo.addItem("Highest", QOrganizerItemPriority.HighestPriority)
        self.priorityCombo.addItem("Extremely high",
            QOrganizerItemPriority.ExtremelyHighPriority)
        self.priorityCombo.addItem("Very high",
            QOrganizerItemPriority.VeryHighPriority)
        self.priorityCombo.addItem("High", QOrganizerItemPriority.HighPriority)
        self.priorityCombo.addItem("Medium", QOrganizerItemPriority.MediumPriority)
        self.priorityCombo.addItem("Low", QOrganizerItemPriority.LowPriority)
        self.priorityCombo.addItem("Very low", QOrganizerItemPriority.VeryLowPriority)
        self.priorityCombo.addItem("Extremely low",
            QOrganizerItemPriority.ExtremelyLowPriority)
        self.priorityCombo.addItem("Lowest", QOrganizerItemPriority.LowestPriority)
        
        self.statusCombo =  QComboBox()
        self.statusCombo.addItem("Not started",
            QOrganizerTodoProgress.StatusNotStarted)
        self.statusCombo.addItem("In progress", QOrganizerTodoProgress.StatusInProgress)
        self.statusCombo.addItem("Complete",
            QOrganizerTodoProgress.StatusComplete)
    
        self.alarmCombo = QComboBox()
        self.alarmCombo.addItems(["None",  "15 minutes",  "30 minutes",  "45 minutes", "1 hour"])

class Window(QWidget):

    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
            
        self.todoEditor = None
        self.listWidget = None
        self.stackedWidget = None
        self.TodoButton = None
        self.deletTodoButton = None
        self.calendarWidget = None

        self.setupGui()
        self.manager = QOrganizerManager("memory")
        self.setWindowTitle(self.tr("ToDo Example"))
        self.refreshList()


    def editNewTodo(self):
        newTodo = QOrganizerTodo()
        newTodo.setPriority(QOrganizerItemPriority.HighPriority)
        newTodo.setStatus(QOrganizerTodoProgress.StatusNotStarted)
        currentDateTime = QDateTime(self.calendarWidget.selectedDate(), QTime.currentTime())
        newTodo.setStartDateTime(currentDateTime)
        newTodo.setDueDateTime(currentDateTime.addSecs(60*60))
    
        self.todoEditor.editTodo(newTodo)
    
        self.stackedWidget.setCurrentWidget(self.todoEditor)
    
   
    def editTodo(self, item):
        if isinstance(item.data(Qt.UserRole), QOrganizerTodo):
            self.todo = item.data(Qt.UserRole)
            self.todoEditor.editTodo(self.todo)
            self.stackedWidget.setCurrentWidget(self.todoEditor)
    
    def saveTodo(self):
        self.manager.saveItem(self.todoEditor.finishedTodo)
        self.stackedWidget.setCurrentIndex(0)
        self.refreshList()


    def refreshList(self):
        self.listWidget.clear()

        sortOrder = QOrganizerItemSortOrder()
        sortOrder.setDetailDefinitionName(QOrganizerTodoTime.DefinitionName,
            QOrganizerTodoTime.FieldDueDateTime)
    
        items = self.manager.items(QOrganizerItemFilter(), [sortOrder])
        if len(items) == 0:
            QListWidgetItem("<No Todos>", self.listWidget)
        
        for item in items: 
            if (item.type() == QOrganizerItemType.TypeTodo): 
                self.todo = QOrganizerTodo(item)
                if (self.todo.startDateTime() > QDateTime(self.calendarWidget.selectedDate(), QTime(23,59))) or (self.todo.dueDateTime() < QDateTime(self.calendarWidget.selectedDate(), QTime(0, 0))):
                    continue
    
                display = self.todo.startDateTime().toString("yy/MM/dd hh:mm") + "-" + self.todo.dueDateTime().toString("yy/MM/dd hh:mm") + " - "+ self.todo.displayLabel()
    
                listItem = QListWidgetItem(display, self.listWidget)
                listItem.setData(Qt.UserRole, self.todo)
    

    def deleteTodo(self):
        items = self.listWidget.selectedItems()
        if items:
            item = items[0].data(Qt.UserRole)
            if isinstance(item, QOrganizerTodo):
                theTodo = item
                self.manager.removeItem(theTodo.id())
                self.refreshList()
        
    

    def setupGui(self):
        self.todoEditor =  TodoEditor()
    
        self.listWidget =  QListWidget()
        self.stackedWidget =  QStackedWidget()
        self.newTodoButton =  QPushButton(self.tr("New Todo"))
        self.deletTodoButton =  QPushButton(self.tr("Delete Todo"))
        self.calendarWidget =  QCalendarWidget()
        
        self.newTodoButton.clicked.connect(self.editNewTodo)
        # See bug 657
        #self.todoEditor.editingFinished[QOrganizerTodo].connect(self.saveTodo)
        self.todoEditor.editingFinished.connect(self.saveTodo)
        self.listWidget.itemDoubleClicked[QListWidgetItem].connect(self.editTodo)
        self.calendarWidget.selectionChanged.connect(self.refreshList)
        self.deletTodoButton.clicked.connect(self.deleteTodo)
        
        mainLayout =  QVBoxLayout()
        mainLayout.addWidget(self.calendarWidget)
        mainLayout.addWidget(self.listWidget)
        buttonLayout =  QHBoxLayout()
        buttonLayout.addWidget(self.newTodoButton)
        buttonLayout.addWidget(self.deletTodoButton)
        mainLayout.addLayout(buttonLayout)
        frontPage =  QWidget()
        frontPage.setLayout(mainLayout)
        self.stackedWidget.addWidget(frontPage)
        self.stackedWidget.addWidget(self.todoEditor)
        layout =  QGridLayout()
        layout.addWidget(self.stackedWidget)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication([])
    w = Window()
    w.show()
    app.exec_()

