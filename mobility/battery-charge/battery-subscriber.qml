/****************************************************************************
**
** Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
** All rights reserved.
** Contact: Nokia Corporation (qt-info@nokia.com)
**
** This file is part of the Qt Mobility Components.
**
** $QT_BEGIN_LICENSE:BSD$
** You may use this file under the terms of the BSD license as follows:
**
** "Redistribution and use in source and binary forms, with or without
** modification, are permitted provided that the following conditions are
** met:
**   * Redistributions of source code must retain the above copyright
**     notice, this list of conditions and the following disclaimer.
**   * Redistributions in binary form must reproduce the above copyright
**     notice, this list of conditions and the following disclaimer in
**     the documentation and/or other materials provided with the
**     distribution.
**   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
**     the names of its contributors may be used to endorse or promote
**     products derived from this software without specific prior written
**     permission.
**
** THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
** "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
** LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
** A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
** OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
** SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
** LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
** DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
** THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
** (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
** OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
** $QT_END_LICENSE$
**
****************************************************************************/

import Qt 4.7
//! [4]
import QtMobility.publishsubscribe 1.0
//! [4]
//import Qt.labs.particles 1.0

Rectangle {
    color: "white"
    width: 100
    height: 230

    Rectangle {
        x: 20
        y: 10
        width: 60
        height: 10
        color: "black"
    }

    Rectangle {
        x: 10
        y: 20
        width: 80
        height: 200
        color: "black"
    }

    Rectangle {
        //! [1]
        id: visualCharge
        x: 12
        y: 22 + 196 - height
        width: 76
        height: 196 * batteryCharge.value / 100
        clip: true
        color: "green"
        //! [1]

        states: [
        //! [3]
        State {
            name: "charging"
            when: batteryCharging.value
            PropertyChanges {
                target: bubbles
                count: batteryCharge.value / 5
                emissionRate: 5
            }
        },
        //! [3]
        //! [2]
        State {
            name: "low"
            when: batteryCharge.value < 25 && !batteryCharging.value
            PropertyChanges {
                target: visualCharge
                color: "red"
            }
        }
        //! [2]
        ]

        transitions: [
        Transition {
            from: "*"
            to: "low"
            reversible: true
            ColorAnimation {
                duration: 200
            }
        }
        ]
    }

    //! [0]
    ValueSpaceSubscriber {
        id: batteryCharge
        path: "/power/battery/charge"
    }
    ValueSpaceSubscriber {
        id: batteryCharging
        path: "/power/battery/charging"
    }
    //! [0]
}
