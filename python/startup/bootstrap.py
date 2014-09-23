# Copyright (c) 2014 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.


import tank
import os

FLAME_HOOKS_FOLDER = "flame_hooks"

def bootstrap(tk, engine_instance_name, context):
    """
    Entry point for starting this engine.
    This is typically called from something like tk-multi-launchapp
    prior to starting up the DCC, but could be initialized in other ways too.
    
    :param tk: Tk API instance
    :param engine_instance_name: the name of the engine instance in the environment to launch
    :param context: The context to launch
    """
    
    # for now, force enable debug. later on, read from engine settings    
    os.environ["DL_DEBUG_PYTHON_HOOKS"] = "1"
        
    # add flame hooks for this engine
    # note - this is currently using some private core methods - replace with official ones!
    engine_path = tank.platform.get_engine_path(engine_instance_name, tk, context)
    flame_hooks_folder = os.path.join(engine_path, FLAME_HOOKS_FOLDER)
    tank.util.append_path_to_env_var("DL_PYTHON_HOOK_PATH", flame_hooks_folder)
    
    # go through and add flame hooks for all apps registered with this engine
    # note - this is currently using some private core methods - replace with official ones!
    env = tank.platform.engine.get_environment_from_context(tk, context)    
    for app in env.get_apps(engine_instance_name):
        descriptor = env.get_app_descriptor(engine_instance_name, app)
        flame_hooks_folder = os.path.join(descriptor.get_path(), FLAME_HOOKS_FOLDER)
        print flame_hooks_folder
        if os.path.exists(flame_hooks_folder):
            tank.util.append_path_to_env_var("DL_PYTHON_HOOK_PATH", flame_hooks_folder)
    
