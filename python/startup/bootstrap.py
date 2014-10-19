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
import sys

def bootstrap(engine_instance_name, context):
    """
    Entry point for starting this engine.
    This is typically called from something like tk-multi-launchapp
    prior to starting up the DCC, but could be initialized in other ways too.
    
    NOTE! When this method is called, Flame is NOT running. This is part of the
          Flame launch sequence and used to prepare the environment and set up prior 
          to launch.
    
    :param engine_instance_name: the name of the engine instance in the environment to launch
    :param context: The context to launch

    :returns: arguments to pass when launching flame
    """
    
    # first create a version of the flame engine!
    # this is so that we can introspect it and extract and validate settings
    #
    # TODO: add get_engine() method (or similar) to core
    #
    # for now, stash the current engine.
    current_engine = sgtk.platform.current_engine()
    sgtk.platform.engine.set_current_engine(None)
    
    # start up flame engine
    # set a special environment varialbe to help hint to the engine
    # that when it is started this time, it is part of the bootstrap
    # and happening *outside* of flame
    os.environ["TK_ENGINE_BOOTSTRAP"] = "1"
    flame_engine = sgtk.platform.start_engine(engine_instance_name, context.sgtk, context)
    del os.environ["TK_ENGINE_BOOTSTRAP"]
    
    app_args = flame_engine.bootstrap()
    
    # deallocate the engine
    flame_engine.destroy()
    
    # put the currently running engine back again
    sgtk.platform.engine.set_current_engine(current_engine)
    
    # serialize engine parameters. Once flame has started, the project hook 
    # will run and start up the engine (again) inside of flame.
    os.environ["TOOLKIT_ENGINE_NAME"] = engine_instance_name
    os.environ["TOOLKIT_CONTEXT"] = sgtk.context.serialize(context)
    
    return app_args
