
import QtQuick 1.1
import com.nokia.meego 1.0

Button {
    text: ""

    property int holdTime: 800 // Hold time in msecs

    signal held
    signal clickedWithoutHold // Replace the original clicked signal, which keeps being emitted.

    onPressedChanged: {
        if (pressed) {
            // Start counting
            holdTimer.wasTriggered = false;
            holdTimer.start();
        } else {
            // Just stop the timer
            holdTimer.restart();
            holdTimer.stop();
        }

        if (!pressed && !holdTimer.wasTriggered) {
            // Replaces the clicked signal
            clickedWithoutHold();
            holdTimer.restart();
            holdTimer.stop();
        }
    }

    Timer {
        property bool wasTriggered: false
        id: holdTimer
        interval: holdTime
        running: false
        repeat: false
        onTriggered: {
            wasTriggered = true
            held();
            restart();
            stop();
        }
    }
}
