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
import re
import sys
import uuid
import sgtk
import socket
import pickle
import tempfile
from sgtk import TankError

class FlameEngine(sgtk.platform.Engine):
    """
    The engine class
    """
    
    # the name of the folder in the engine which we should register
    # with flame to trigger various hooks to run.
    FLAME_HOOKS_FOLDER = "flame_hooks"
    
    def pre_app_init(self):
        """
        Engine construction/setup done before any apps are initialized
        """        
        self.log_debug("%s: Initializing..." % self)        
        
        # maintain a list of export options
        self._registered_export_instances = {}
        self._export_sessions = {}
        self._registered_batch_instances = []
        
        if self.has_ui:
            # tell QT to interpret C strings as utf-8
            from PySide import QtGui, QtCore
            utf8 = QtCore.QTextCodec.codecForName("utf-8")
            QtCore.QTextCodec.setCodecForCStrings(utf8)        
        
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
        # check if there is a UI. With Flame, we may run the engine in bootstrap
        # mode or on the farm - in this case, there is no access to UI. If inside the
        # DCC UI environment, pyside support is available.
        has_ui = False
        try:
            from PySide import QtGui, QtCore
            if QtCore.QCoreApplication.instance():
                # there is an active application
                has_ui = True
        except:
            pass
        
        return has_ui
    
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
    # Engine Bootstrap
    #
    
    def bootstrap(self):
        """
        Special bootstrap method used to set up the flame environment.
        This is designed to execute before flame has launched, as part of the 
        bootstrapping process.

        This method assumes that it is being executed inside a flame python
        and is called from the app_launcher script which ensures such an environment.
        
        The bootstrapper will first import the wiretap API and setup other settings.
        
        It then attempts to execute the pre-DCC project creation process, utilizing
        both wiretap and QT (setup project UI) for this.
        
        Finally, it will return the command line args to pass to flame as it is being
        launched.
        
        :returns: arguments to pass to the app launch process
        """
        if self.get_setting("debug_logging"):
            # enable flame hooks debug
            os.environ["DL_DEBUG_PYTHON_HOOKS"] = "1"
        
        # special logic for flare - see if we can load up a batch file
        if self.instance_name == "tk-flare":
            
            self.log_debug("Launching flare!")
        
            # For flare, try to see if we can seed the session with a particular batch file.
            # we do this by passing a special environment to the flare startup.
            # 
            # For now, hard code the logic of how to detect which batch file to load up.
            # TODO: in the future, we may want to expose this in a hook - but it is arguably
            # pretty advanced customization :)
            #
            # Current logic: Find the latest batch publish belonging to the context
            
            if self.context.entity:
                # we have a current context to lock on to!
        
                # try to see if we can find the latest batch publish
                publish_type = sgtk.util.get_published_file_entity_type(self.sgtk)
                
                if publish_type == "PublishedFile":
                    type_link_field = "published_file_type.PublishedFileType.code"
                else:
                    type_link_field = "tank_type.TankType.code"
                
                sg_data = self.shotgun.find_one(publish_type, 
                                                [[type_link_field, "is", self.get_setting("flame_batch_publish_type")],
                                                 ["entity", "is", self.context.entity]],
                                                ["path"],
                                                order=[{"field_name": "created_at", "direction": "desc"}])
                
                if sg_data:
                    # we have a batch file published for this context!
                    batch_file_path = sg_data["path"]["local_path"]
                    self.log_debug("Setting flare auto startup file '%s'" % batch_file_path)
                    os.environ["DL_BATCH_START_WITH_SETUP"] = batch_file_path
        
        
        # add flame hooks for this engine
        flame_hooks_folder = os.path.join(self.disk_location, self.FLAME_HOOKS_FOLDER)
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
            
            if sys.platform == "linux2":
                wiretap_path = os.path.join(self.disk_location, "resources", "wiretap", "linux")                
            
            elif sys.platform == "darwin":
                wiretap_path = os.path.join(self.disk_location, "resources", "wiretap", "macosx")
            
            else:
                raise TankError("Unsupported operating system! Cannot load wiretap API!")
            
            self.log_debug("The wiretap API for the current session would be here: %s" % wiretap_path)            
        
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
    
    def _define_qt_base(self):
        """
        Define QT behaviour. Subclassed from base class.
        """
        if "TK_ENGINE_BOOTSTRAP" not in os.environ:
            # we are running the engine inside of the Flame Application.
            # in this state, no special QT init is necesssary. Defer
            # to default implementation
            return super(FlameEngine, self)._define_qt_base()
        
        else:
            # we are running the engine outside of flame.
            # initialize QT.
            from PySide import QtCore, QtGui
            import PySide
    
            # a simple dialog proxy that pushes the window forward
            class ProxyDialogPySide(QtGui.QDialog):
                def show(self):
                    QtGui.QDialog.show(self)
                    self.activateWindow()
                    self.raise_()
    
                def exec_(self):
                    self.activateWindow()
                    self.raise_()
                    # the trick of activating + raising does not seem to be enough for
                    # modal dialogs. So force put them on top as well.
                    self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | self.windowFlags())
                    return QtGui.QDialog.exec_(self)
                    
            base = {}
            base["qt_core"] = QtCore
            base["qt_gui"] = QtGui
            base["dialog_base"] = ProxyDialogPySide
            self.log_debug("Successfully initialized PySide '%s' located in %s." 
                           % (PySide.__version__, PySide.__file__))
            
            return base
    
    
    
    ################################################################################################################
    # export callbacks handling
    #
    # Any apps which are interested in register custom exporters with flame should use the methods
    # below. The register_export_hook() is called by apps in order to create a menu entry
    # on the flame export menu. The remaining methods are used to call out from the actual flame hook
    # to the relevant app code.
    #
    
    def register_export_hook(self, menu_caption, callbacks):
        """
        Allows an app to register an interest in one of the flame export hooks.
        
        This one of the interaction entry points in the system and this is how apps
        typically have their business logic executed. At app init, an app typically
        calls this method with a syntax like this:
        
            # set up callback map
            callbacks = {}
            callbacks["preCustomExport"] = self.pre_custom_export
            callbacks["preExportAsset"] = self.adjust_path
            callbacks["postExportAsset"] = self.register_post_asset_job
            
            # register with the engine
            self.engine.register_export_hook("Menu Caption", callbacks)
 
        The engine will keep track of things automatically, and whenever the user
        clicks the "Menu Caption" entry on the menu, the corresponding chain of callbacks
        will be called.
        
        All methods should have the following method signature:
        
            def export_callback(self, session_id, info)
            
        Where session_id is a unique session identifier (typically only used in advanced scenarios)
        and info reflects the info passed from Flame (varies for different callbacks).
        
        For information which export can currently be registered against, see the
        flame_hooks/exportHook.py file.
        
        :param menu_caption: Text to appear on the Flame export menu
        :param callbacks: Dictionary of callbacks, see above for details.
        """
        if menu_caption in self._registered_export_instances:
            raise TankError("There is already a menu export preset named '%s'! " 
                            "Please ensure your preset names are unique" % menu_caption)
    
        self.log_debug("Registered export preset '%s' with engine." % menu_caption)
        self._registered_export_instances[menu_caption] = callbacks
    
    
    def get_export_presets(self):
        """
        Internal engine method. Do not use outside of the engine.
        Returns all export presets registered by apps.
        
        :returns: List of preset titles
        """
        return self._registered_export_instances.keys()

    
    def create_export_session(self, preset_name):
        """
        Internal engine method. Do not use outside of the engine.
        Start a new export session.
        Creates a session object which represents a single export session in flame.
        
        :param preset_name: The name of the preset which should be executed.
        :returns: session id string which is later passed into various methods
        """
        if preset_name not in self._registered_export_instances:
            raise TankError("The export preset '%s' is not registered with the current engine. "
                            "Current presets are: %s" % (preset_name, self._registered_export_instances.keys()))
        
        session_id = "tk_%s" % uuid.uuid4().hex
        
        # set up an export session
        self._export_sessions[session_id] = preset_name
        
        return session_id


    def trigger_export_callback(self, callback_name, session_id, info):
        """
        Internal engine method. Do not use outside of the engine.
        
        Dispatch method called from the various flame hooks. 
        This method will ensure that the flame callbacks will be 
        dispatched to the appropriate registered app callbacks.
        
        :param callback_name: Name of the flame callback method
        :param session_id: Unique session identifier
        :param info: Metadata dictionary from Flame
        """
        self.log_debug("Flame engine export callback dispatch for %s" % callback_name)
        if session_id not in self._export_sessions:
            self.log_debug("Ignoring request for unknown session %s..." % session_id)
            return
        
        # get the preset
        preset_name = self._export_sessions[session_id]
        callbacks = self._registered_export_instances[preset_name]
        
        # call the callback in the preset
        if callback_name in callbacks:
            # the app has registered interest in this!
            self.log_debug("Executing callback %s" % callbacks[callback_name])
            callbacks[callback_name](session_id, info)
        
    
    ################################################################################################################
    # batch callbacks handling
    #
    # Any apps which are interested in register custom batch exporters with flame should use the methods
    # below. The register_batch_hook() is called by apps in order to register an interest in pre and post
    # export callbacks when in batch mode. The flame engine will ensure that the app's callbacks will get 
    # called at the right time.
    #
    
    def register_batch_hook(self, callbacks):
        """
        Allows an app to register an interest in one of the flame batch hooks.
        
        This one of the interaction entry points in the system and this is how apps
        typically have their business logic executed. At app init, an app typically
        calls this method with a syntax like this:
        
            # set up callback map
            callbacks = {}
            callbacks["batchExportBegin"] = self.before_export
            callbacks["batchExportEnd"] = self.after_export
            
            # register with the engine
            self.engine.register_batch_hook(callbacks)
 
        The engine will keep track of things automatically, and whenever a batch render executes, 
        the corresponding chain of callbacks will be called.
        
        All methods should have the following method signature:
        
            def export_callback(self, info)
            
        For information which export can currently be registered against, see the
        flame_hooks/batchHook.py file.
        
        :param callbacks: Dictionary of callbacks, see above for details.
        """
        self.log_debug("Registered batch callbacks with engine: %s" % callbacks)
        self._registered_batch_instances.append(callbacks)
        
    def trigger_batch_callback(self, callback_name, info):
        """
        Internal engine method. Do not use outside of the engine.
        
        Dispatch method called from the various flame hooks. 
        This method will ensure that the flame callbacks will be 
        dispatched to the appropriate registered app callbacks.
        
        :param callback_name: Name of the flame callback method
        :param session_id: Unique session identifier
        :param info: Metadata dictionary from Flame
        """
        self.log_debug("Flame engine batch callback dispatch for %s" % callback_name)

        # dispatch to all callbacks
        
        for registered_batch_instance in self._registered_batch_instances:
            self.log_debug("checking %s" % registered_batch_instance)
            if callback_name in registered_batch_instance:
                # the app has registered interest in this!
                self.log_debug("Executing callback %s" % registered_batch_instance[callback_name])
                registered_batch_instance[callback_name](info)
        

    
    
    ################################################################################################################
    # backburner integration
    #
    
    def get_server_hostname(self):
        """
        Return the hostname for the server which hosts this flame setup.
        This is an accessor into the engine hook settings, allowing apps
        to query which host the closest flame server is running on.
        
        :returns: hostname string 
        """
        return self.execute_hook_method("project_startup_hook", "get_server_hostname")
    
    def get_backburner_tmp(self):
        """
        Return a location on disk, guaranteed to exist
        where temporary data can be put in such a way that
        it will be accessible for all backburner jobs, regardless of 
        which host they execute on.
        
        :returns: path
        """
        return self.get_setting("backburner_shared_tmp")
        
    def create_local_backburner_job(self, job_name, description, run_after_job_id, app, method_name, args):
        """
        Run a method in the local backburner queue.
        
        :param job_name: Name of the backburner job
        :param description: Description of the backburner job
        :param run_after_job_id: None if the backburner job should execute arbitrarily. If you 
                                 want to set the job up so that it executes after another known task, pass
                                 the backburner id here. This is typically used in conjunction with a postExportAsset
                                 hook where the export task runs on backburner. In this case, the hook will return
                                 the backburner id. By passing that id into this method, you can create a job which 
                                 only executes after the main export task has completed.
        :param app: App to remotely call up
        :param method_name: Name of method to remotely execute
        :param args: dictionary or args (**argv style) to pass to method at remote execution
        """
        
        # the backburner executable
        BACKBURNER_JOB_CMD = "/usr/discreet/backburner/cmdjob"

        # pass some args - most importantly tell it to run on the local host
        # looks like : chars are not valid so replace those
        backburner_args = []
        
        # run as current user, not as root
        backburner_args.append("-userRights")
        
        # add basic job info
        # backburner does not do any kind of sanitaion itself, so ensure that job
        # info doesn't contain any strange characters etc
        backburner_args.append("-jobName:\"%s\"" % re.sub('[^0-9a-zA-Z_\-,\. ]+', '_', job_name))
        backburner_args.append("-description:\"%s\"" % re.sub('[^0-9a-zA-Z_\-,\. ]+', '_', description))

        if run_after_job_id:
            backburner_args.append("-dependencies:%s" % run_after_job_id) # run after another job

        # call the bootstrap script
        backburner_bootstrap = os.path.join(self.disk_location, "python", "startup", "backburner.py")
        farm_cmd = "%s %s" % ("/usr/discreet/Python-2.6.9/bin/python", backburner_bootstrap)
        
        # now we need to capture all of the environment and everything in a file
        # (thanks backburner!) so that we can replay it later when the task wakes up
        session_file = os.path.join(self.get_backburner_tmp(), "tk_backburner_%s.pickle" % uuid.uuid4().hex)

        data = {}
        data["engine_instance"] = self.instance_name
        data["serialized_context"] = sgtk.context.serialize(self.context)
        data["app_instance"] = app.instance_name
        data["method_to_execute"] = method_name
        data["args"] = args
        data["sgtk_core_location"] = os.path.dirname(sgtk.__path__[0])
        
        fh = open(session_file, "wb")
        pickle.dump(data, fh)
        fh.close()
        
        full_cmd = "%s %s %s %s" % (BACKBURNER_JOB_CMD, " ".join(backburner_args), farm_cmd, session_file)

        self.log_debug("Starting backburner job '%s'" % job_name)
        self.log_debug("Command line: %s" % full_cmd)
        self.log_debug("App: %s" % app)
        self.log_debug("Method: %s with args %s" % (method_name, args))

        # kick it off        
        if os.system(full_cmd) != 0:
            raise TankError("Shotgun backburner job could not be created. Please see log for details.")


    ################################################################################################################
    # accessors to various core settings and functions                
                
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

    def get_default_clip_start_frame(self):
        """
        Returns the value of the per-user setting default TC.
        Returns 0 if this cannot be established.
        
        :returns: default offset for clips, in frames
        """
        
        # look for this file:
        # /usr/discreet/user/{USER}/status/EditingUICurrent.pref
        # There will be an entry on the following form:
        # 15 DefaultTCStart, 1800000.000000 50 fps
        
        user_name = self.execute_hook_method("project_startup_hook", "get_user")
        path = "/usr/discreet/user/%s/status/EditingUICurrent.pref" % user_name
        default_tc_start = 0
        
        if not os.path.exists(path):
            self.log_warning("Cannot find the preferences file %s. Will assume zero time code offset." % path )
        else:
            fh = open(path, "rt")
            try:
                for line in fh.readlines():
                    if "DefaultTCStart" in line:
                        (_, data) = line.split(", ")
                        # data: "1800000.000000 50 fps"
                        offset_str = data.split(" ")[0]
                        # offset_str: "1800000.000000"
                        default_tc_start = int(float(offset_str))
            except Exception, e:
                self.log_warning("Could not read DefaultTCStart token from file '%s'. "
                                 "Will assume zero offset. Error Reported: %s" (path, e))
            finally:
                fh.close()
        
        return default_tc_start  
        
        
