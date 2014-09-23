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
import os

FLAME_HOOKS_FOLDER = "flame_hooks"

def bootstrap(engine_instance_name, context):
    """
    Entry point for starting this engine.
    This is typically called from something like tk-multi-launchapp
    prior to starting up the DCC, but could be initialized in other ways too.
    
    :param tk: Tk API instance
    :param engine_instance_name: the name of the engine instance in the environment to launch
    :param context: The context to launch
    """
    
    # first create a version of the flame engine!
    # this is so that we can introspect it and extract and validate settings
    #
    # todo: add get_engine() method (or similar) to core
    current_engine = sgtk.platform.current_engine()
    sgtk.platform.engine.set_current_engine(None)
    
    flame_engine = sgtk.platform.start_engine(engine_instance_name, context.sgtk, context)
    
    
    if flame_engine.get_setting("debug_logging"):
        # enable flame hooks debug
        os.environ["DL_DEBUG_PYTHON_HOOKS"] = "1"
        
    flame_engine.log_debug("Started flame engine for introspection: %s" % flame_engine)
        
    # add flame hooks for this engine
    flame_hooks_folder = os.path.join(flame_engine.disk_location, FLAME_HOOKS_FOLDER)
    sgtk.util.append_path_to_env_var("DL_PYTHON_HOOK_PATH", flame_hooks_folder)
    flame_engine.log_debug("Added to hook path: %s" % flame_hooks_folder)
    
    # go through and add flame hooks for all apps registered with this engine    
    for app_obj in flame_engine.apps.values():        
        flame_hooks_folder = os.path.join(app_obj.disk_location, FLAME_HOOKS_FOLDER)
        if os.path.exists(flame_hooks_folder):
            sgtk.util.append_path_to_env_var("DL_PYTHON_HOOK_PATH", flame_hooks_folder)
            flame_engine.log_debug("Added to hook path: %s" % flame_hooks_folder)
    
    # deallocate the engine
    flame_engine.destroy()
    
    # put the currently running engine back again
    sgtk.platform.engine.set_current_engine(current_engine)
    
    # serialize engine parameters. Once flame has started, the project hook 
    # will run and start up the engine (again) inside of flame.
    os.environ["TOOLKIT_ENGINE_NAME"] = engine_instance_name
    os.environ["TOOLKIT_CONTEXT"] = sgtk.context.serialize(context)
