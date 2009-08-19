#!/usr/bin/env python

#############################################################################
##
## Copyright (C) 2004-2005 Trolltech AS. All rights reserved.
##
## This file is part of the example classes of the Qt Toolkit.
##
## This file may be used under the terms of the GNU General Public
## License version 2.0 as published by the Free Software Foundation
## and appearing in the file LICENSE.GPL included in the packaging of
## this file.  Please review the following information to ensure GNU
## General Public Licensing requirements will be met:
## http/www.trolltech.com/products/qt/opensource.html
##
## If you are unsure which license is appropriate for your use, please
## review the following information:
## http/www.trolltech.com/products/qt/licensing.html or contact the
## sales department at sales@trolltech.com.
##
## This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
## WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
##
#############################################################################

import sys
from PySide import QtCore, QtGui

import movie_rc


class MoviePlayer(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.movieScreen = QtGui.QLabel()
        self.movieScreen.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.movieScreen.setBackgroundRole(QtGui.QPalette.Base)
        self.movieScreen.setText(self.tr("Use the Eject button to select a movie."))
        self.movieScreen.setAlignment(QtCore.Qt.AlignCenter)
        self.movieScreen.setWordWrap(True)

        self.currentMovieDirectory = "movies"

        self.createSliders()
        self.createCheckBox()
        self.createButtons()

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.movieScreen)
        mainLayout.addWidget(self.scaleMovieCheckbox)
        mainLayout.addLayout(self.slidersLayout)
        mainLayout.addLayout(self.buttonsLayout)
        self.setLayout(mainLayout)

        self.speedSlider.setDisabled(True)
        self.scaleMovieCheckbox.setDisabled(True)
        self.playButton.setDisabled(True)
        self.stopButton.setDisabled(True)

        self.resize(400, 400)
        self.setWindowTitle(self.tr("Movie Player"))

    def browse(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self, self.tr("Select a Movie"), self.currentMovieDirectory, self.tr("Movies (*.gif *.mng)"))

        if not fileName.isEmpty():
            index = fileName.length() - fileName.lastIndexOf("/")

            if index >= 0:
                currentMovieDirectory = fileName
                currentMovieDirectory.chop(index)

            if self.movieScreen.movie() and self.movieScreen.movie().state() != QtGui.QMovie.NotRunning:
                self.movieScreen.movie().stop()

            movie = QtGui.QMovie("trolltech.gif", QtCore.QByteArray(), self)
            movie.setCacheMode(QtGui.QMovie.CacheAll)

            movie.setSpeed(100)
            self.speedSlider.setValue(100)
            self.connect(self.speedSlider, QtCore.SIGNAL("valueChanged(int)"), movie, QtCore.SLOT("setSpeed(int)"))

            self.movieScreen.setMovie(movie)

            supportsFrames = (movie.frameCount() > 0)

            if supportsFrames:
                self.frameSlider.setMaximum(movie.frameCount()-1)
                self.connect(movie, QtCore.SIGNAL("frameChanged(int)"), self.frameSlider, QtCore.SLOT("setValue(int)"))

            self.frameSlider.setVisible(supportsFrames)
            self.frameLabel.setVisible(supportsFrames)

            self.speedSlider.setDisabled(False)
            self.scaleMovieCheckbox.setDisabled(False)
            self.playButton.setDisabled(False)
            self.stopButton.setDisabled(False)

            movie.start()

    def start(self):
        movie = self.movieScreen.movie()

        if movie.state() == QtGui.QMovie.NotRunning:
            movie.start()
        else:
            movie.setPaused(not (movie.state() == QtGui.QMovie.Paused))

    def stop(self):
        movie = self.movieScreen.movie()

        if not (movie.state() == QtGui.QMovie.NotRunning):
            movie.stop()

    def goToFrame(self, frame):
        self.movieScreen.movie().jumpToFrame(frame)

    def scaleMovie(self):
        self.movieScreen.setScaledContents(self.scaleMovieCheckbox.isChecked())

    def createSliders(self):
        self.frameSlider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.frameSlider.setTickPosition(QtGui.QSlider.TicksBelow)
        self.frameSlider.setTickInterval(1)
        self.connect(self.frameSlider, QtCore.SIGNAL("valueChanged(int)"), self.goToFrame)
        self.frameSlider.setVisible(False)

        self.frameLabel = QtGui.QLabel(self.tr("Jump to frame"))
        self.frameLabel.setVisible(False)

        self.speedSlider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.speedSlider.setMaximum(1000)
        self.speedSlider.setTickInterval(50)
        self.speedSlider.setTickPosition(QtGui.QSlider.TicksBelow)
        self.speedSlider.setMinimum(50)

        speedLabel = QtGui.QLabel(self.tr("Set speed"))

        self.slidersLayout = QtGui.QGridLayout()
        self.slidersLayout.addWidget(self.frameLabel, 0, 0)
        self.slidersLayout.addWidget(self.frameSlider, 0, 1)
        self.slidersLayout.addWidget(speedLabel, 1, 0)
        self.slidersLayout.addWidget(self.speedSlider, 1, 1)

    def createCheckBox(self):
        self.scaleMovieCheckbox = QtGui.QCheckBox(self.tr("Scale movie"))
        self.connect(self.scaleMovieCheckbox, QtCore.SIGNAL("clicked()"), self.scaleMovie)

    def createButtons(self):
        self.browseButton = QtGui.QToolButton()
        self.browseButton.setToolTip(self.tr("Eject/Open File..."))
        self.browseButton.setIcon(QtGui.QIcon(":/icons/eject.png"))
        self.browseButton.setIconSize(QtCore.QSize(32, 32))
        self.connect(self.browseButton, QtCore.SIGNAL("clicked()"), self.browse)

        self.playButton = QtGui.QToolButton()
        self.playButton.setToolTip(self.tr("Play/Pause"))
        self.playButton.setIcon(QtGui.QIcon(":/icons/play-pause.png"))
        self.playButton.setIconSize(QtCore.QSize(49, 32))
        self.connect(self.playButton, QtCore.SIGNAL("clicked()"), self.start)

        self.stopButton = QtGui.QToolButton()
        self.stopButton.setToolTip(self.tr("Stop"))
        self.stopButton.setIcon(QtGui.QIcon(":/icons/stop.png"))
        self.stopButton.setIconSize(QtCore.QSize(32, 32))
        self.connect(self.stopButton, QtCore.SIGNAL("clicked()"), self.stop)

        self.quitButton = QtGui.QToolButton()
        self.quitButton.setToolTip(self.tr("Quit"))
        self.quitButton.setIcon(QtGui.QIcon(":/icons/quit.png"))
        self.quitButton.setIconSize(QtCore.QSize(32, 32))
        self.connect(self.quitButton, QtCore.SIGNAL("clicked()"), self, QtCore.SLOT("close()"))

        self.buttonsLayout = QtGui.QHBoxLayout()
        self.buttonsLayout.addStretch()
        self.buttonsLayout.addWidget(self.playButton)
        self.buttonsLayout.addWidget(self.stopButton)
        self.buttonsLayout.addWidget(self.browseButton)
        self.buttonsLayout.addWidget(self.quitButton)
        self.buttonsLayout.addStretch()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    player = MoviePlayer()
    player.show()
    sys.exit(app.exec_())
