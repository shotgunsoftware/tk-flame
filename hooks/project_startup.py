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
import re

HookBaseClass = sgtk.get_hook_baseclass()

class ProjectStartupActions(HookBaseClass):
    """
    Toolkit hook to control the behavior of how new projects are created.
    
    As part of the toolkit Flame launch process, a new flame project is automatically
    created if it doesn't already exist. Toolkit will then jump directly into that project
    as part of the launch process. 
    
    This hooks allows a project to customize the behaviour for new projects and jumping into 
    projects:
    
    - The user which should be used when launching Flame and starting the project
    - The naming of a new project
    - The project parameters used with new projects
    - The storage volume to store a new project on
    - The workspace to use when launching the project
    
    It is possible to introspect Shotgun inside this hook, making it straight
    forward to make this entire process driven from field values within Shotgun.
    
    - The engine instance can be fetched via self.parent
    - A shotgun API handle is available via engine_obj.shotgun.
    - The project id can be retrieved via engine_obj.context.project["id"]
    """
    
    def get_project(self):
        """
        Return the project name that should be used for the current context.
        Please note that flame doesn't allow all types of characters in Project names.
        
        The flame engine will try to find this project in Flame and start it.
        If it doesn't exist, it will be automatically created.
        
        :returns: project name string 
        """
        engine = self.parent
        
        if engine.context.project is None:
            raise TankError("Context does not have a project!")
        
        project_name = engine.context.project["name"]
        
        # sanity check the project name, convert to alphanumeric.
        # flame is restrictive with special characters, so adopt 
        # a conservative approach
        sanitized_project_name = re.sub(r'\W+', '_', project_name)
        
        return sanitized_project_name
            
    def get_project_settings(self):
        """
        Returns project settings for when creating new projects.
        
        The following parameters need to be supplied:
        
         - FrameWidth
         - FrameHeight
         - FrameDepth
         - AspectRatio
         - FrameRate
         - ProxyEnable
         - ProxyWidthHint
         - ProxyDepthMode
         - ProxyMinFrameSize
         - ProxyAbove8bits
         - ProxyQuality
         - FieldDominance
        
        :returns: dictionary of standard wiretap style project setup parameters.
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
        When a new project is created, this allows to control
        which volume should be associated with the new project.
        
        The return value needs to be one of the strings passed in 
        via the volumes parameter.
        
        :param volumes: List of existing volumes (list of string)
        :returns: One of the volumes in the list (str)
        """
        return volumes[0]
    
    def get_workspace(self):
        """
        Return the name of the workspace to use when opening a project.
        The system will create it if it doesn't already exist.
        
        If None is return, flame will create a default workspace according
        to its standard workspace creation logic.
        
        :returns: A flame workspace Name or None for a default workspace
        """
        return None

    def get_user(self):
        """
        Return the name of the flame user to be used when launching this project.
        
        :returns: A user name as a string
        """
        engine = self.parent

        # Grab information about the environment we are running in
        shotgun_user = sgtk.util.get_current_user(engine.sgtk)

        if shotgun_user is None:
            user_name = "unknown"
        else:
            user_name = shotgun_user["name"] 

        return user_name
        
