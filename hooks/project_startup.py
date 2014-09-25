# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

"""
Hook that handles logic and automation around automatic Flame project setup 
"""
import sgtk
from sgtk import TankError
import os

HookBaseClass = sgtk.get_hook_baseclass()

class ProjectStartupActions(HookBaseClass):
    
    
    def get_project(self):
        """
        Return the project name
        """
        engine = self.parent
        
        if engine.context.project is None:
            raise TankError("Context does not have a project!")
        
        project_name = engine.context.project["name"]
        
        # spaces don't seem to be supported
        # TODO: probably more aggressive cleanup needed here)
        project_name = project_name.replace(" ", "_")
        
        return project_name
            
    def get_project_settings(self):
        """
        Returns project settings
        """
        settings = {}
        settings["FrameWidth"] = "1280"
        settings["FrameHeight"] = "1080"
        settings["FrameDepth"] = "16-bit fp"
        settings["AspectRatio"] = "1.7778"
        settings["FrameRate"] = "29.9699"
        settings["ProxyEnable"] = "29.9699"
        settings["ProxyWidthHint"] = "0.2"
        settings["ProxyDepthMode"] = "8-bit"
        settings["ProxyMinFrameSize"] = "720"
        settings["ProxyAbove8bits"] = "false"
        settings["ProxyQuality"] = "medium"
        settings["FieldDominance"] = "PROGRESSIVE"

        return settings
        
            
    def get_volume(self, volumes):
        """
        Return the volume to use
        """
        return volumes[0]
    
    def get_workspace(self):
        """
        Return the name of the workspace to use when opening a project.
        The system will create it if it doesn't already exist.
        
        """
        return "my-workspace"

    def get_user(self):
        """
        Execute a given action. The data sent to this be method will
        represent one of the actions enumerated by the generate_actions method.
        
        :param name: Action name string representing one of the items returned by generate_actions.
        :param params: Params data, as specified by generate_actions.
        :param sg_publish_data: Shotgun data dictionary with all the standard publish fields.
        :returns: No return value expected.
        """
        engine = self.parent

        # Grab information about the environment we are running in
        shotgun_user = sgtk.util.get_current_user(engine.sgtk)

        if shotgun_user is None:
            user_name = "unknown"
        else:
            user_name = shotgun_user["name"] 

        return user_name
        
                        
        
