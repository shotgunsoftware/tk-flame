# Copyright (c) 2014 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.


import sgtk
from sgtk import TankError
import os
import re
import sys

def bootstrap(engine_instance_name, context, app_path, app_args):
    """
    Entry point for starting this engine.
    This is typically called from something like tk-multi-launchapp
    prior to starting up the DCC, but could be initialized in other ways too.
    
    This method needs to be able to execute from any python version, with 
    or without QT installed. Since it will typically be executed from within
    the multi-launch-app, it will be running in the python that was used to 
    start the engine where the multi-launch-app is running (typically 
    tk-shell/tk-desktop/tk-shotgun). 

    The purpose of this script is to prepare the launch process for flame,
    return the executable that the launch app should actually execute. This 
    process consists of an additional step for Flame because part of the app
    launch process happens outside of flame. We therefore rewrite the launch
    arguments as part of this method. For example
    
    input: app_path: /usr/discreet/flame_2015.2/bin/startApplication
           app_args: ""
    
    output: app_path: /mnt/software/shotgun/my_project/install/engines/app-store/tk-flame/v1.2.3/launch_app
            app_args: /usr/discreet/flame_2015.2/bin/startApplication --extra args
    
    :param engine_instance_name: the name of the engine instance in the environment to launch
    :param context: The context to launch
    :param app_path: The path to the DCC to start
    :param app_args: External args to pass to the DCC 

    :returns: (app_path, app_args)
    """
    
    # do a quick check to ensure that we are running 2015.2 or later
    re_match = re.search("/fla[mr]e[^_]*_([^/]+)/", app_path)
    if not re_match:
        raise TankError("Cannot extract Flame version number from the path '%s'!" % app_path)
    version_str = re_match.group(1)
    # Examples:
    # 2015.2
    # 2016
    # 2015.2.pr99
    chunks = version_str.split(".")
    major_ver = int(chunks[0])
    if len(chunks) > 1:
        minor_ver = int(chunks[1])
    else:
        minor_ver = 0
    
    if major_ver < 2015:
        raise TankError("In order to run the Shotgun integration, you need at least Flame 2015, extension 2!")
    
    if major_ver == 2015 and minor_ver < 2:
        raise TankError("In order to run the Shotgun integration, you need at least Flame 2015, extension 2!")
    
    this_folder = os.path.abspath(os.path.dirname(__file__))
    engine_root = os.path.abspath(os.path.join(this_folder, "..", ".."))
    launch_script = os.path.join(engine_root, "app_launcher") 
    
    # update the environment prior to launch
    os.environ["TOOLKIT_ENGINE_NAME"] = engine_instance_name
    os.environ["TOOLKIT_CONTEXT"] = sgtk.context.serialize(context)
    
    # also, in order to ensure that qt is working correctly inside of
    # the flame python interpreter, we need to hint the library order
    # by adjusting the LD_LIBRARY_PATH. Note that this cannot be done
    # inside an executing script as the dynamic loader sets up the load
    # order prior to the execution of any payload. This is why we need to 
    # set this before we run the app launch script.
    if sys.platform == "darwin":
        sgtk.util.prepend_path_to_env_var("DYLD_FRAMEWORK_PATH", "/usr/discreet/lib64/2015.2/framework")
    elif sys.platform == "linux2":
        sgtk.util.prepend_path_to_env_var("LD_LIBRARY_PATH", "/usr/discreet/Python-2.6.9/lib")
        sgtk.util.prepend_path_to_env_var("LD_LIBRARY_PATH", "/usr/discreet/lib64/2015.2")
    
    # finally, reroute the executable and args
    new_app_path = launch_script
    new_app_args = "%s %s" % (app_path, app_args)
        
    return (new_app_path, new_app_args) 
