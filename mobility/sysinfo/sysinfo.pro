QT       += network

TARGET = qsysinfo
TEMPLATE = app


SOURCES += main.cpp\
        dialog.cpp

HEADERS  += dialog.h
RESOURCES = examples.qrc

INCLUDEPATH += ../../src/systeminfo

include(../examples.pri)
CONFIG += mobility
MOBILITY = systeminfo

CONFIG += console

win32 {
    FORMS += dialog.ui
}

unix: {
    linux-*: {
        maemo* {
            FORMS += dialog_landscape.ui
        } else {
            FORMS += dialog.ui
        }
    }
    
    mac: {
        FORMS += dialog.ui
    }
}

symbian {
    TARGET.CAPABILITY = LocalServices NetworkServices ReadUserData UserEnvironment Location  ReadDeviceData
    TARGET.UID3 = 0x2002ac7e
    FORMS    += dialog_s60.ui
}
