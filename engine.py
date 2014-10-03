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
        
        # check if there is a UI. With Flame, we may run the engine in bootstrap
        # mode or on the farm - in this case, there is no access to UI. If inside the
        # DCC UI environment, pyside support is available.
        try:
            import PySide
            self._has_ui = True
        except:
            self._has_ui = False
        
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
    
    @property
    def has_ui(self):
        """
        Property to determine if the current environment has access to a UI or not
        """
        return self._has_ui
        
    
    
    ################################################################################################################
    # Bootstrap code
    # NOTE! This is executed *outside* of Flame, prior to launch.
    
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
            flame_hooks_folder = os.path.join(app_obj.disk_location, self.FLAME_HOOKS_FOLDER)
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
    
    
    ################################################################################################################
    # standard engine interface
                
    def log_debug(self, msg):
        """
        Log a debug message
        
        :param msg: The debug message to log
        """
        if self.get_setting("debug_logging", False):
            print "Shotgun Debug: %s" % msg
 
    def log_info(self, msg):
        """
        Log some info
        
        :param msg: The info message to log
        """
        print "Shotgun Info: %s" % msg
 
    def log_warning(self, msg):
        """
        Log a warning
        
        :param msg: The warning message to log
        """        
        print "Shotgun Warning: %s" % msg
 
    def log_error(self, msg):
        """
        Log an error
        
        :param msg: The error message to log
        """        
        print "Shotgun Error: %s" % msg


    ################################################################################################################
    # wiretap accessors                
                
    def __get_wiretap_central_binary(self, binary_name):
        """
        Returns the path to a binary in the wiretap central binary collection.
        This is standard on all flame installations.
        
        :param binary_name: Name of desired binary
        :returns: Absolute path as a string  
        """
        if sys.platform == "darwin":
            wtc_path = "/Library/WebServer/CGI-Executables/WiretapCentral"
        elif sys.platform == "linux2":
            wtc_path = "/var/www/cgi-bin/WiretapCentral"
        else:    
            raise TankError("Your operating system does not support wiretap central!")
        
        path = os.path.join(wtc_path, binary_name)
        if not os.path.exists(path):
            raise TankError("Cannot find binary '%s'!" % path)
        
        return path

    def get_ffmpeg_path(self):
        """
        Returns the path to the ffmpeg executable that ships with flame.
        
        :returns: Absolute path as a string
        """
        return self.__get_wiretap_central_binary("ffmpeg")
                
    def get_read_frame_path(self):
        """
        Returns the path to the read_frame utility that ships with flame.
        
        :returns: Absolute path as a string
        """
        return self.__get_wiretap_central_binary("read_frame")    
