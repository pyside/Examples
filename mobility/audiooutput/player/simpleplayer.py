
import os
import sys

from PySide.QtCore import QUrl
from PySide.QtGui import QApplication, QPushButton, QMainWindow
from QtMobility.MultimediaKit import QMediaPlayer

class AudioTest(QMainWindow):


    def __init__(self, filename):
        QMainWindow.__init__(self)

        self.playButton = QPushButton('Play!')
        self.source = QUrl.fromLocalFile(filename)
        self.player = QMediaPlayer()

        self.player.setMedia(self.source)

        self.playButton.clicked.connect(self.play)

        self.setCentralWidget(self.playButton)
        self.playButton.show()

    def play(self):
        self.player.play()

def main():

    app = QApplication([])
    app.setApplicationName('Simple Audio player')

    window = AudioTest(os.path.abspath(sys.argv[1]))
    window.show()

    return app.exec_()

if __name__ == '__main__':
    main()
