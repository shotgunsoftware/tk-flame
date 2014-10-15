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
Wiretap connection with the local flame to carry out common setup operations
"""

import sgtk
from sgtk import TankError

# helper exception class to trap all the C style errors
# that are potentially coming from the wiretap API.
class WiretapError(TankError):
    pass

# note: this is one of those C style library wrappers
# where each method internally is prefixed with 
# WireTap, hence the dropping of the namespace.
from libwiretapPythonClientAPI import *

class WiretapHandler(object):
    """
    Wiretap functionality
    """
    
    #########################################################################################################
    # public methods
    
    def __init__(self):
        """
        Construction
        """
        self._engine = sgtk.platform.current_bundle()
        
        self._engine.log_debug("Initializing wiretap...")
        WireTapClientInit()
        
        # Instantiate a server handle
        host_name = self._engine.execute_hook_method("project_startup_hook", "get_server_hostname")
        self._server = WireTapServerHandle("%s:IFFFS" % host_name)
        self._engine.log_debug("Connected to wiretap host '%s'..." % host_name)
    
    def close(self):
        """
        Closes the wiretap connection
        """
        # Make sure to always uninitialize WireTap services in case of
        # exception, otherwise wiretap server will refuse all the 
        # following connections.
        self._server = None
        WireTapClientUninit()
        self._engine.log_debug("Uninitialized wiretap...")
        
    def prepare_and_load_project(self):
        """
        Load and prepare the project represented by the current context
        
        :returns: arguments to pass to the Flame lauch command line
        """
        
        user_name = self._engine.execute_hook_method("project_startup_hook", "get_user")
        self._ensure_user_exists(user_name)

        project_name = self._engine.execute_hook_method("project_startup_hook", "get_project")
        self._ensure_project_exists(project_name)
        
        workspace_name = self._engine.execute_hook_method("project_startup_hook", "get_workspace")
        if workspace_name:
            self._engine.log_debug("Using a custom workspace '%s'" % workspace_name)
            # an explicit workspace is used. Ensure it exists
            self._ensure_workspace_exists(project_name, workspace_name)
            # and pass it to the startup
            app_args = "--start-project='%s' --start-user='%s' --create-workspace --start-workspace='%s'" % (project_name, 
                                                                                                             user_name, 
                                                                                                             workspace_name)
        else:
            # use flame's default workspace
            self._engine.log_debug("Using the flame default workspace")
            app_args = "--start-project='%s' --start-user='%s' --create-workspace" % (project_name, user_name)
        
        return app_args
    
    
    
    #########################################################################################################
    # internals
        
    def _ensure_user_exists(self, user_name):
        """
        Ensures the given user exists
        
        :param user_name: Name of the user to look for
        """
        
        if not self._child_node_exists("/users", user_name, "USER"):
            # Create the new user
            users = WireTapNodeHandle(self._server, "/users")
       
            user_node = WireTapNodeHandle()
            if not users.createNode(user_name, "USER", user_node):
                raise WiretapError("Unable to create user %s: %s" % (user_name, users.lastError()))
 
            self._engine.log_debug("User %s succesfully created" % user_name)

    def _ensure_workspace_exists(self, project_name, workspace_name):
        """
        Ensures that the given workspace exists
        
        :param project_name: Project to look in
        :param workspace_name: Workspace name to look for        
        """
        
        if not self._child_node_exists("/projects/%s" % project_name, workspace_name, "WORKSPACE"):
            project = WireTapNodeHandle(self._server, "/projects/%s" % project_name)
       
            workspace_node = WireTapNodeHandle()
            if not project.createNode(workspace_name, "WORKSPACE", workspace_node):
                raise WiretapError("Unable to create workspace %s in "
                                   "project %s: %s" % (workspace_name, project_name, project.lastError()) )
 
        self._engine.log_debug("Workspace %s successfully created" % workspace_name)
 
    def _ensure_project_exists(self, project_name):
        """
        Ensures that the given project exists
        
        :param project_name: Project name to look for
        """
        if not self._child_node_exists("/projects", project_name, "PROJECT"):

            # first decide which volume to create the project on.
            # get a list of volumes and pass it to a hook which will 
            # return the volume to use
            volumes = self._get_volumes()
            
            if len(volumes) == 0:
                raise TankError("Cannot create new project! There are no volumes defined for this Flame!")
            
            # call out to the hook to determine which volume to use
            volume_name = self._engine.execute_hook_method("project_startup_hook", "get_volume", volumes=volumes)
            
            # sanity check :)
            if volume_name not in volumes:
                raise TankError("Volume '%s' specified in hook does not exist in "
                                "list of current volumes '%s'" % (volume_name, volumes))
            
            # resolve this as an object
            volume = WireTapNodeHandle(self._server, "/volumes/%s" % volume_name)
            
            # create the project
            project_node = WireTapNodeHandle()
            if not volume.createNode(project_name, "PROJECT", project_node):
                raise WiretapError("Unable to create project %s: %s" %  (project_name, volume.lastError()))
 
            # create project settings
            # first get settings from the toolkit hook
            settings = self._engine.execute_hook_method("project_startup_hook", "get_project_settings") 

            self._engine.log_debug("A new project '%s' will be created." % project_name)
            self._engine.log_debug("The following settings will be used:")
            for (k,v) in settings.iteritems():
                self._engine.log_debug("%s: %s" % (k, v))

            # create xml structure
            xml  = "<Project>"
            xml += "<Description>%s</Description>"             % "Created by Shotgun Pipeline Toolkit"
            xml += "<FrameWidth>%s</FrameWidth>"               % settings.get("FrameWidth")
            xml += "<FrameHeight>%s</FrameHeight>"             % settings.get("FrameHeight")
            xml += "<FrameDepth>%s</FrameDepth>"               % settings.get("FrameDepth")
            xml += "<AspectRatio>%s</AspectRatio>"             % settings.get("AspectRatio")
            xml += "<FrameRate>%s</FrameRate>"                 % settings.get("FrameRate")
            xml += "<ProxyEnable>%s</ProxyEnable>"             % settings.get("ProxyEnable")
            xml += "<ProxyWidthHint>%s</ProxyWidthHint>"       % settings.get("ProxyWidthHint")
            xml += "<ProxyDepthMode>%s</ProxyDepthMode>"       % settings.get("ProxyDepthMode")
            xml += "<ProxyMinFrameSize>%s</ProxyMinFrameSize>" % settings.get("ProxyMinFrameSize")
            xml += "<ProxyAbove8bits>%s</ProxyAbove8bits>"     % settings.get("ProxyAbove8bits")
            xml += "<ProxyQuality>%s</ProxyQuality>"           % settings.get("ProxyQuality")
            xml += "<FieldDominance>%s</FieldDominance>"       % settings.get("FieldDominance")
            xml += "</Project>"
    
            # Set the project meta data
            if not project_node.setMetaData("XML", xml):
                raise WiretapError("Error setting metadata for %s: %s" % (project_name, project_node.lastError()))
               
            self._engine.log_debug( "Project successfully created.")
         

    def _get_volumes(self):
        """
        Return a list of volumes available
        
        :returns: List of volume names
        """
        root = WireTapNodeHandle(self._server, "/volumes")
        num_children = WireTapInt(0)
        if not root.getNumChildren(num_children):
            raise WiretapError("Unable to obtain number of volumes: %s" % root.lastError())
        
        volumes = []
        
        # iterate over children, look for the given node
        child_obj = WireTapNodeHandle()
        for child_idx in range(num_children):
            
            # get the child
            if not root.getChild(child_idx, child_obj):
                raise WiretapError("Unable to get child: %s" % parent.lastError())
    
            node_name = WireTapStr()
            
            if not child_obj.getDisplayName(node_name):
                raise WiretapError("Unable to get child name: %s" % child_obj.lastError())
 
            volumes.append(node_name.c_str())
        
        return volumes

    def _child_node_exists(self, parent_path, child_name, child_type):
        """
        Helper method. Check if a wiretap node exists.
        
        :param parent_path: Parent node to scan
        :param child_name: Name of child node to look for
        :param child_type: Type of child node to look for
        :returns: True if node exists, false otherwise.
        """ 
        # get the parent
        parent = WireTapNodeHandle(self._server, parent_path)
        
        # get number of children
        num_children = WireTapInt(0)
        if not parent.getNumChildren(num_children):
            raise WiretapError("Unable to obtain number of children for %s: %s" % (parent_path, parent.lastError()))
                            
        # iterate over children, look for the given node
        child_obj = WireTapNodeHandle()
        for child_idx in range(num_children):
            
            # get the child
            if not parent.getChild(child_idx, child_obj):
                raise WiretapError("Unable to get child: %s" % parent.lastError())
    
            node_name = WireTapStr()
            node_type = WireTapStr()
            
            if not child_obj.getDisplayName(node_name):
                raise WiretapError("Unable to get child name: %s" % child_obj.lastError())
            if not child_obj.getNodeTypeStr(node_type):
                raise WiretapError("Unable to obtain child type: %s" % child_obj.lastError())
 
            if node_name.c_str() == child_name and node_type.c_str() == child_type:
                return True
       
        return False
