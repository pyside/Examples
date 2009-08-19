#!/usr/bin/env python

# This example launches Qt Designer after setting up the environment to point
# at the example plugins.
#
# Copyright (c) 2007 Phil Thompson


import sys
import os.path

from PyQt4 import QtCore, QtGui


# Set a specified environment variable with a directory name.
def setEnvironment(env, var_name, dir_name):
    # Convert the relative directory name to an absolute one.
    dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), dir_name)

    # Remove any existing value so that we have a controlled environment.
    idx = env.indexOf(QtCore.QRegExp("^%s=.*" % var_name, QtCore.Qt.CaseInsensitive))

    if idx >= 0:
        env.removeAt(idx)

    env << "%s=%s" % (var_name, dir)


app = QtGui.QApplication(sys.argv)

QtGui.QMessageBox.information(None, "PyQt Designer Plugins",
        "<p>This example will start Qt Designer when you click the <b>OK</b> "
        "button.</p>"
        "<p>Before doing so it sets the <tt>PYQTDESIGNERPATH</tt> environment "
        "variable to the <tt>python</tt> directory that is part of this "
        "example.  This directory contains all the example Python plugin "
        "modules.</p>"
        "<p>It also sets the <tt>PYTHONPATH</tt> environment variable to the "
        "<tt>widgets</tt> directory that is also part of this example.  This "
        "directory contains the Python modules that implement the example "
        "custom widgets.</p>"
        "<p>All of the example custom widgets should then appear in "
        "Designer's widget box in the <b>PyQt Examples</b> group.</p>")

# Tell Qt Designer where it can find the directory containing the plugins and
# Python where it can find the widgets.
env = QtCore.QProcess.systemEnvironment()
setEnvironment(env, "PYQTDESIGNERPATH", "python")
setEnvironment(env, "PYTHONPATH", "widgets")

# Start Designer.
designer = QtCore.QProcess()
designer.setEnvironment(env)

designer_bin = QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.BinariesPath)

if sys.platform == "darwin":
    designer_bin.append("/Designer.app/Contents/MacOS/Designer")
else:
    designer_bin.append("/designer")

designer.start(designer_bin)
designer.waitForFinished(-1)

sys.exit(designer.exitCode())
