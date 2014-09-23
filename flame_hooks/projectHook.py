# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.


# Hook called when the user loads a project in the application.
# projectName : Name of the loaded project -- String.
def projectChanged(projectName):
   pass


# Hook called when application is fully initialized
#
# projectName: the project that was loaded -- String
def appInitialized( projectName ):
    """
    Try to start up the flame engine at this point
    """
    import sgtk
    import os
    
    # todo - add exception handling
    print "Starting up toolkit engine..."
    engine_name = os.environ.get("TOOLKIT_ENGINE_NAME") 
    context = sgtk.context.deserialize(os.environ.get("TOOLKIT_CONTEXT"))
    e = sgtk.platform.start_engine(engine_name, context.sgtk, context)
    print "toolkit engine running! %s" % e 
    

# Hook called after a project has been saved
#
# projectName: the project that was saved -- String
# saveTime   : time to save the project (in seconds) -- Float
# isAutoSave : true if save was automatically initiated,
#              false if user initiated -- Bool
def projectSaved( projectName, saveTime, isAutoSave ):
   pass











