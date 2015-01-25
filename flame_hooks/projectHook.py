# Copyright (c) 2014 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

        
def appInitialized(projectName):
    """
    Hook called when application is fully initialized.
    
    :param projectName: String containing the name of the project that was loaded
    """
    
    # attempt to start the flame engine if it hasn't already been started.
    
    import sgtk
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
        engine_name = os.environ.get("TOOLKIT_ENGINE_NAME") 
        context = sgtk.context.deserialize(os.environ.get("TOOLKIT_CONTEXT"))
        
        # set a special environment variable to help hint to the engine
        # that we are running a backburner job
        os.environ["TK_FLAME_ENGINE_MODE"] = "DCC"
        e = sgtk.platform.start_engine(engine_name, context.sgtk, context)
        del os.environ["TK_FLAME_ENGINE_MODE"]
        
        # pass the python executable from the bootstrap to the engine 
        python_executable = os.environ.get("TOOLKIT_FLAME_PYTHON_BINARY")
        if not python_executable:
            e.log_error("Cannot find environment variable TOOLKIT_FLAME_PYTHON_BINARY - this is set "
                        "during the sgtk bootstrap of Flame.")
        else:
            e.set_python_executable(python_executable)
        
        
