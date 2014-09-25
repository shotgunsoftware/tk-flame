# Copyright (c) 2014 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

"""
A Toolkit engine for Flame
"""

import os
import sys
import sgtk
from sgtk import TankError

class FlameEngine(sgtk.platform.Engine):
    """
    The engine class
    """
    
    FLAME_HOOKS_FOLDER = "flame_hooks"
    
    def pre_app_init(self):
        """
        Engine construction/setup done before any apps are initialized
        """        
        self.log_debug("%s: Initializing..." % self)        
        
    def post_app_init(self):
        """
        Do any initialization after apps have been loaded
        """
        self.log_debug("%s: Running post app init..." % self)

    def destroy_engine(self):
        """
        Called when the engine is being destroyed
        """
        self.log_debug("%s: Destroying..." % self)
        
    def bootstrap(self):
        """
        Special bootstrap method used to set up the flame environment.
        This is designed to execute before flame has launched, as part of the 
        bootstrapping process.
        
        :returns: arguments to pass to the app launch process
        """
        if self.get_setting("debug_logging"):
            # enable flame hooks debug
            os.environ["DL_DEBUG_PYTHON_HOOKS"] = "1"
        
        # add flame hooks for this engine
        flame_hooks_folder = os.path.join(self.disk_location, self.FLAME_HOOKS_FOLDER)
        sgtk.util.append_path_to_env_var("DL_PYTHON_HOOK_PATH", flame_hooks_folder)
        self.log_debug("Added to hook path: %s" % flame_hooks_folder)
        
        # go through and add flame hooks for all apps registered with this engine    
        for app_obj in self.apps.values():        
            flame_hooks_folder = os.path.join(self.disk_location, self.FLAME_HOOKS_FOLDER)
            if os.path.exists(flame_hooks_folder):
                sgtk.util.append_path_to_env_var("DL_PYTHON_HOOK_PATH", flame_hooks_folder)
                self.log_debug("Added to hook path: %s" % flame_hooks_folder)
        
        # add and validate the wiretap API
        # first, see if the wiretap API already exists - in that case, we use that version
        try:
            import libwiretapPythonClientAPI
            self.log_debug("Wiretap API was already in the pythonpath. "
                           "Will not try to add one in from the engine.")
        except:
            self.log_debug("Wiretap API not detected. Will add it to the pythonpath.")
            wiretap_path = os.path.join(self.disk_location, 
                                        "resources", 
                                        "wiretap_%s_py%s%s" % (sys.platform, sys.version_info[0], sys.version_info[1]))
            
            self.log_debug("The wiretap API for the current session would be here: %s" % wiretap_path)
            
            if not os.path.exists(wiretap_path):
                raise TankError("The flame engine does not support the version of python (%s) "
                                "you are currently running!" % sys.version)
        
            sys.path.append(wiretap_path)
            import libwiretapPythonClientAPI
        
        self.log_debug("Using wiretap API %s from %s" % (libwiretapPythonClientAPI, libwiretapPythonClientAPI.__file__))
        
        # now that we have a wiretap library, call out and initialize the project 
        # automatically
        tk_flame = self.import_module("tk_flame")
        wiretap_handler = tk_flame.WiretapHandler()
        
        try:
            app_args = wiretap_handler.prepare_and_load_project()
        finally:
            wiretap_handler.close()
        
        return app_args
        
        
        
        
        
        
        
        
#     @property
#     def has_ui(self):
#         """
#         Detect and return if mari is not running in terminal mode
#         """        
#         # todo: detect batch mode
#         return True
# 
    def log_debug(self, msg):
        """
        Log a debug message
        :param msg:    The debug message to log
        """
        if self.get_setting("debug_logging", False):
            print "Shotgun Debug: %s" % msg
# 
#     def log_info(self, msg):
#         """
#         Log some info
#         :param msg:    The info message to log
#         """
#         print 'Shotgun Info: %s' % msg
# 
#     def log_warning(self, msg):
#         """
#         Log a warning
#         :param msg:    The warning message to log
#         """        
#         msg = 'Shotgun Warning: %s' % msg
#         print msg
# 
#     def log_error(self, msg):
#         """
#         Log an error
#         :param msg:    The error message to log
#         """        
#         msg = 'Shotgun Error: %s' % msg
#         print msg

