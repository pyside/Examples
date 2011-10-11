'''
 Copyright (C) 2011 Nokia Corporation and/or its subsidiary(-ies).
 All rights reserved.
 Contact: Nokia Corporation (qt-info@nokia.com)

 This file is part of the Qt Mobility Components.

 $QT_BEGIN_LICENSE:LGPL$
 No Commercial Usage
 This file contains pre-release code and may not be distributed.
 You may use this file in accordance with the terms and conditions
 contained in the Technology Preview License Agreement accompanying
 this package.

 GNU Lesser General Public License Usage
 Alternatively, this file may be used under the terms of the GNU Lesser
 General Public License version 2.1 as published by the Free Software
 Foundation and appearing in the file LICENSE.LGPL included in the
 packaging of this file.  Please review the following information to
 ensure the GNU Lesser General Public License version 2.1 requirements
 will be met: http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html.

 In addition, as a special exception, Nokia gives you certain additional
 rights.  These rights are described in the Nokia Qt LGPL Exception
 version 1.1, included in the file LGPL_EXCEPTION.txt in this package.

 If you have questions regarding the use of this file, please contact
 Nokia at qt-info@nokia.com.
'''

import os
import sys

from PySide.QtCore import QObject, Signal, Slot, Property, QUrl, qWarning
from PySide.QtCore import QAbstractItemModel, QDate, QDateTime, QTime
from PySide.QtGui import QApplication
from PySide.QtDeclarative import QDeclarativeView
from QtMobility.Organizer import QOrganizerManager, QOrganizerItemSortOrder
from QtMobility.Organizer import QOrganizerTodo, QOrganizerTodoTime
from QtMobility.Organizer import QOrganizerItemFilter, QOrganizerItemDetailFilter
from QtMobility.Organizer import QOrganizerItemPriority, QOrganizerTodoProgress
from QtMobility.Organizer import QOrganizerItemType


class TodoManager(QObject):

    def __init__(self):
        QObject.__init__(self)

        self.manager = QOrganizerManager("memory")
        self._todos = [] # FIXME Use a model instead of a string list as model
        self._todo = None # Current todo being edited or created

        self.reload()

    @Slot()
    def reload(self):
        self._todos = []

        sortOrder = QOrganizerItemSortOrder()
        sortOrder.setDetailDefinitionName(QOrganizerTodoTime.DefinitionName,
                                          QOrganizerTodoTime.FieldDueDateTime)

        todoFilter = QOrganizerItemFilter()

        items = self.manager.items(todoFilter, [sortOrder])

        todos = []
        for item in items:
            if item.type() == QOrganizerItemType.TypeTodo:
                todo = QOrganizerTodo(item)

                display = todo.startDateTime().toString("yy/MM/dd hh:mm") +\
                        "-" + todo.dueDateTime().toString("yy/MM/dd hh:mm") +\
                        "\n" + todo.displayLabel()

                todos.append((display, todo))

        self._todos = todos
        self.todosChanged.emit()

    @Slot()
    def deleteCurrent(self):
        self.manager.removeItem(self._todo.id())
        self.reload()

    currentTodoChanged = Signal()

    @Slot()
    def editNewTodo(self):
        """Sets the current todo to a newly created todo"""
        newTodo = QOrganizerTodo()
        newTodo.setPriority(QOrganizerItemPriority.HighPriority)
        newTodo.setStatus(QOrganizerTodoProgress.StatusNotStarted)
        currentDateTime = QDateTime(QDate.currentDate(), QTime.currentTime())
        newTodo.setStartDateTime(currentDateTime)
        newTodo.setDueDateTime(currentDateTime.addSecs(60*60))

        self._todo = newTodo
        self._todo.isNewTodo = True
        self.currentTodoChanged.emit()

    @Property(bool, notify=currentTodoChanged)
    def isNewTodo(self):
        return self._todo.isNewTodo if self._todo else True

    @Slot(int)
    def editExistingTodo(self, index):
        self._todo = self._todos[index][1]
        self._todo.isNewTodo = False
        self.currentTodoChanged.emit()

    @Slot()
    def saveTodo(self):
        self.manager.saveItem(self._todo)
        self._todo = None
        self.reload()

    todosChanged = Signal()
    @Property("QStringList", notify=todosChanged)
    def todos(self):
        return [x[0] for x in self._todos]

    @todos.setter
    def setTodo(self, value):
        self._todos = value
        self.todosChanged.emit()

    # Subject
    currentTodoSubjectChanged = Signal()

    @Property(str, notify=currentTodoSubjectChanged)
    def todoSubject(self):
        return self._todo.displayLabel()

    @todoSubject.setter
    def setTodoSubject(self, value):
        self._todo.setDisplayLabel(value)
        self.currentTodoSubjectChanged.emit()

    # Dates and times
    def datetimeToStrList(self, datetime):
        date = datetime.date()
        time = datetime.time()
        return (("%02d "*5) % (date.year(), date.month(), date.day(),
                        time.hour(), time.minute())).split()

#    @Slot(result="QStringList")
    @Property("QStringList", notify=currentTodoChanged)
    def todoStartDateTime(self):
        return self.datetimeToStrList(self._todo.startDateTime())

    @Slot(int, int, int)
    def setTodoStartDate(self, year, month, day):
        orig_time = self._todo.startDateTime().time()
        date = QDate(year, month, day)
        datetime = QDateTime(date, orig_time)

        self._todo.setStartDateTime(datetime)
        self.currentTodoChanged.emit()

    @Slot(int, int)
    def setTodoStartTime(self, hour, minute):
        orig_date = self._todo.startDateTime().date()
        time = QTime(hour, minute)
        datetime = QDateTime(orig_date, time)

        self._todo.setStartDateTime(datetime)
        self.currentTodoChanged.emit()

    @Property("QStringList", notify=currentTodoChanged)
    def todoDueDateTime(self):
        return self.datetimeToStrList(self._todo.dueDateTime())

    @Slot(int, int, int)
    def setTodoDueDate(self, year, month, day):
        orig_time = self._todo.dueDateTime().time()
        date = QDate(year, month, day)
        datetime = QDateTime(date, orig_time)

        self._todo.setDueDateTime(datetime)

        self.currentTodoChanged.emit()

    @Slot(int, int)
    def setTodoDueTime(self, hour, minute):
        orig_date = self._todo.dueDateTime().date()
        time = QTime(hour, minute)
        datetime = QDateTime(orig_date, time)

        self._todo.setDueDateTime(datetime)

        self.currentTodoChanged.emit()

    # Status

    Status = [
            QOrganizerTodoProgress.StatusNotStarted,
            QOrganizerTodoProgress.StatusInProgress,
            QOrganizerTodoProgress.StatusComplete,
    ]

    @Property(int, notify=currentTodoChanged)
    def todoStatus(self):
        status = self._todo.status()
        try:
            index = self.Status.index(status)
            return index
        except ValueError:
            return 0

    @todoStatus.setter
    def setTodoStatus(self, value):
        try:
            self._todo.setStatus(self.Status[value])
            self.currentTodoChanged.emit()
        except IndexError:
            pass # Fail silently...

    # Priority

    Priority = [
        QOrganizerItemPriority.UnknownPriority,
        QOrganizerItemPriority.HighestPriority,
        QOrganizerItemPriority.ExtremelyHighPriority,
        QOrganizerItemPriority.VeryHighPriority,
        QOrganizerItemPriority.HighPriority,
        QOrganizerItemPriority.MediumPriority,
        QOrganizerItemPriority.LowPriority,
        QOrganizerItemPriority.VeryLowPriority,
        QOrganizerItemPriority.ExtremelyLowPriority,
        QOrganizerItemPriority.LowestPriority,
    ]

    @Property(int, notify=currentTodoChanged)
    def todoPriority(self):
        priority = self._todo.priority()
        try:
            index = self.Priority.index(priority)
            return index
        except ValueError:
            return 0

    @todoPriority.setter
    def setTodoPriority(self, value):
        try:
            self._todo.setPriority(self.Priority[value])
            self.currentTodoChanged.emit()
        except IndexError:
            pass # Fail silently...


def main():
    app = QApplication([])
    view = QDeclarativeView()
    manager = TodoManager()
    context = view.rootContext()
    context.setContextProperty("manager", manager)

    url = QUrl('main.qml')
    view.setSource(url)

    if "-no-fs" not in sys.argv:
        view.showFullScreen()
    else:
        view.show()

    app.exec_()


if __name__ == '__main__':
    main()


