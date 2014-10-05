# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

import sys
import traceback

def sgtk_exception_trap(ex_cls, ex, tb):
    """
    Standard exception trap override.
    Attempts to display exceptions as QMessagebox popups
    """
    
    # careful about infinite loops here - 
    # MUST NOT RAISE EXCEPTIONS :)
    
    # assemble message
    error_message = "Critical: Could not format error message."
    try:
        tb_str = "\n".join(traceback.format_tb(tb))
        error_message = "A general Shotgun error message was reported:\n%s\n\nError Type: %s\n\nTraceback:\n%s" % (ex, ex_cls, tb_str)
    except:
        pass

    # now output it    
    try:
        from PySide import QtGui, QtCore
        if QtCore.QCoreApplication.instance():
            # there is a qapplication running - so pop up a message!
            QtGui.QMessageBox.critical(None, "Shotgun General Error", error_message)
    except:
        pass
    
    # in addition to the ui popup, also defer to the default mechanism
    sys.__excepthook__(type, value, tb)
        
def appInitialized(projectName):
    """
    Hook called when application is fully initialized.
    
    :param projectName: String containing the name of the project that was loaded
    """
    
    # attempt to start the flame engine if it hasn't already been started.
    
    import sgtk
    import traceback
    import os    
    
    if sgtk.platform.current_engine():
        # there is already an engine running.
        # TODO: later on, allow for switching of engines as projects 
        #       are being switched. For now, issue a warning
        
        from PySide import QtGui     
        QtGui.QMessageBox.warning(None,
                                  "No project switching!",
                                  "The Shotgun integration does not currently support project switching.\n"
                                  "Even if you switch projects, any Shotgun specific configuration will\n"
                                  "remain connected to the initially loaded project.")
    
    else:
        # no engine running - so start one!
        
        # first override the default exception hook with a more elaborate one which displays an
        # error message.
        sys.excepthook = sgtk_exception_trap
        
        # now attempt to launch the engine
        engine_name = os.environ.get("TOOLKIT_ENGINE_NAME") 
        context = sgtk.context.deserialize(os.environ.get("TOOLKIT_CONTEXT"))
        sgtk.platform.start_engine(engine_name, context.sgtk, context)
            
