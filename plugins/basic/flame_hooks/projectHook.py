# Copyright (c) 2014 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

# Note! This file implements the projectHook interface from Flame 2015.2

import os
import sys


# figure out our location
this_dir = os.path.abspath(os.path.dirname(__file__))
plugin_root_dir = os.path.abspath(os.path.join(this_dir, ".."))

# add python module to path
python_path = os.path.join(plugin_root_dir, "python")
sys.path.append(python_path)

# add bundle cache module to path
python_path = os.path.join(plugin_root_dir, "bundle_cache", "python")
sys.path.append(python_path)

# import manifest that handles config and paths
from sgtk_plugin_basic import manifest
from tk_flame_basic import exception_ui, bootstrap

if manifest.debug_logging:
    # turn on flame debug
    os.environ["DL_DEBUG_PYTHON_HOOKS"] = "1"

# Hook called when the user loads a project in the application.
# projectName : Name of the loaded project -- String.
def projectChanged(projectName):
    try:
        bootstrap.bootstrap_flame(plugin_root_dir, projectName)
    except Exception, e:
        exception_ui.show_exception_in_ui()


