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

import sgtk
from sgtk import TankError

class FlameEngine(sgtk.platform.Engine):
    """
    The engine class
    """
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
        
#     @property
#     def has_ui(self):
#         """
#         Detect and return if mari is not running in terminal mode
#         """        
#         # todo: detect batch mode
#         return True
# 
#     def log_debug(self, msg):
#         """
#         Log a debug message
#         :param msg:    The debug message to log
#         """
#         if not hasattr(self, "_debug_logging"):
#             self._debug_logging = self.get_setting("debug_logging", False)
#         if self._debug_logging:
#             print 'Shotgun Debug: %s' % msg
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

