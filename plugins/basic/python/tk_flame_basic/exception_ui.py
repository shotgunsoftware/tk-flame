# Copyright (c) 2014 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import traceback
from PySide import QtGui, QtCore

def show_exception_in_ui():
    """
    Shows exception in a UI messagebox.
    To be executed from inside an except clause.
    """
    error_message = "A Shotgun error was reported:\n\n%s" % traceback.format_exc()

    # now try to output it
    try:
        # Note - Since Flame is a PySide only environment, we import it directly
        # rather than going through the sgtk wrappers.
        if QtCore.QCoreApplication.instance():
            # there is an application running - so pop up a message!
            QtGui.QMessageBox.critical(None, "Shotgun General Error", error_message)
        else:
            print error_message
    except Exception, e:
        print "Could not report Shotgun error! (%s)" % e
        print error_message

    # and log it
    import sgtk
    logger = sgtk.LogManager.get_logger(__name__)
    logger.error(error_message)

