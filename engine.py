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
import logging
import pprint
import logging.handlers
import tempfile
import traceback
import datetime
from sgtk import TankError
from distutils.version import LooseVersion

LOG_CHANNEL = "sgtk.tk-flame"

class FlameEngine(sgtk.platform.Engine):
    """
    The engine class. This wraps around a series of callbacks in Flame (so called hooks).
    The Flame engine is a bit different than other engines.
    
    Because Flame doesn't have an API, we cannot call Flame, but Flame will call out 
    to the toolkit code. This means that the normal register_command approach won't 
    work inside of Flame - instead, the engine introduces a different scheme of callbacks
    that apps can register to ensure that they cen do stuff.
    
    For apps, the main entry points are register_export_hook and register_batch_hook.
    For more information, see below.
    """
    
    # the name of the folder in the engine which we should register
    # with Flame to trigger various hooks to run.
    FLAME_HOOKS_FOLDER = "flame_hooks"
    
    # our default log file to write to
    SGTK_LOG_FILE = "tk-flame.log"
    
    # a 'plan B' safe log file that we call fall back on in case
    # the default log file cannot be accessed
    SGTK_LOG_FILE_SAFE = "/tmp/tk-flame.log"
    
    # define constants for the various modes the engine can execute in
    (ENGINE_MODE_DCC, ENGINE_MODE_PRELAUNCH, ENGINE_MODE_BACKBURNER) = range(3)
    
    def __init__(self, *args, **kwargs):
        """
        Overridden constructor where we init some things which 
        need to be defined very early on in the engine startup.
        """

        # to support use cases where the flame engine isn't started via
        # the multi-launchapp chain, make sure that hooks that the engine
        # implements are registered.
        flame_hooks_folder = os.path.join(self.disk_location, self.FLAME_HOOKS_FOLDER)
        sgtk.util.append_path_to_env_var("DL_PYTHON_HOOK_PATH", flame_hooks_folder)
        self.log_debug("Added to hook path: %s" % flame_hooks_folder)

        # set the current engine mode. The mode contains information about
        # how the engine was started - it can be executed either before the 
        # actual DCC starts up (pre-launch), in the DCC itself or on the 
        # backburner farm. This means that there are three distinct bootstrap
        # scripts which can launch the engine (all contained within the engine itself).
        # these bootstrap scripts all set an environment variable called
        # TOOLKIT_FLAME_ENGINE_MODE which defines the desired engine mode.
        engine_mode_str = self._ensure_envvar("TOOLKIT_FLAME_ENGINE_MODE")
        if engine_mode_str == "PRE_LAUNCH":
            self._engine_mode = self.ENGINE_MODE_PRELAUNCH
        elif engine_mode_str == "BACKBURNER":
            self._engine_mode = self.ENGINE_MODE_BACKBURNER
        elif engine_mode_str == "DCC":
            self._engine_mode = self.ENGINE_MODE_DCC
        else:
            raise TankError("Unknown launch mode '%s' defined in "
                            "environment variable TOOLKIT_FLAME_ENGINE_MODE!" % engine_mode_str)

        super(FlameEngine, self).__init__(*args, **kwargs)

        # Set this up at first so we can turn on logging asap
        self._install_root = self._ensure_envvar("TOOLKIT_FLAME_INSTALL_ROOT")

        # We can't initialize logging until the engine's base class has been initialized to access
        # settings and we can't initialize it until we know the install root. Unfortunately,
        # this means that anything going wrong before this won't be reportable in the logs.
        self._initialize_logging(self._install_root)
        self.log_debug("Flame install root is '%s'" % self._install_root)

        self._python_executable_path = self._ensure_envvar("TOOLKIT_FLAME_PYTHON_BINARY")
        self.log_debug("This engine is running python interpreter '%s'" % self._python_executable_path)

        self._flame_version = {
            "full": self._ensure_envvar("TOOLKIT_FLAME_VERSION"),
            "major": self._ensure_envvar("TOOLKIT_FLAME_MINOR_VERSION"),
            "minor": self._ensure_envvar("TOOLKIT_FLAME_MINOR_VERSION")
        }
        self.log_debug("This engine is running with Flame version '%s'" % self._flame_version)

    def _ensure_envvar(self, env_var_name):
        """
        Ensure's an environment variable is set.
        """
        if env_var_name not in os.environ:
            raise TankError("Cannot find environment variable '%s'" % env_var_name)
        return os.environ.get(env_var_name)

    def pre_app_init(self):
        """
        Engine construction/setup done before any apps are initialized
        """
        # set up a custom exception trap for the engine.
        # it will log the exception and if possible also
        # display it in a UI
        sys.excepthook = sgtk_exception_trap
        
        # now start the proper init
        self.log_debug("%s: Initializing..." % self)        
        
        # maintain a list of export options
        self._registered_export_instances = {}
        self._export_sessions = {}
        self._registered_batch_instances = []
        
        if self.has_ui:
            # tell QT to interpret C strings as utf-8
            # Note - Since Flame is a PySide only environment, we import it directly
            # rather than going through the sgtk wrappers.             
            from PySide import QtGui, QtCore
            utf8 = QtCore.QTextCodec.codecForName("utf-8")
            QtCore.QTextCodec.setCodecForCStrings(utf8)        

    def _initialize_logging(self, install_root):
        """
        Set up logging for the engine

        :param install_root: path to flame install root
        """
        # standard flame log file
        std_log_file = os.path.join(install_root, "log", self.SGTK_LOG_FILE)

        # test if we can write to the default log file
        try:
            fh = open(std_log_file, "at")
            fh.close()
            log_file = std_log_file
            using_safe_log_file = False
        except IOError:
            # cannot operate on file (usually related to permissions)
            # write to tmp instead.
            log_file = self.SGTK_LOG_FILE_SAFE
            using_safe_log_file = True

        # Set up a rotating logger with 4MiB max file size
        rotating = logging.handlers.RotatingFileHandler(log_file, maxBytes=4*1024*1024, backupCount=10)
        rotating.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] PID %(process)d: %(message)s"))
        # create a global logging object
        logger = logging.getLogger(LOG_CHANNEL)
        logger.propagate = False
        # clear any existing handlers
        logger.handlers = []
        logger.addHandler(rotating)
        if self.get_setting("debug_logging"):
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        # now that we have a logger, we can warn about a non-std log file :)
        if using_safe_log_file:
            logger.error("Cannot write to standard log file location %s! Please check "
                         "the filesystem permissions. As a fallback, logs will be "
                         "written to %s instead." % (std_log_file, log_file))

    def _get_commands_matching_setting(self, setting):
        """
        This expects a list of dictionaries in the form:
            {name: command-name, app_instance: instance-name }

        The app_instance value will match a particular app instance associated with
        the engine.  The name is the menu name of the command to run when the engine starts up.
        If name is '' then all commands from the given app instance are returned.

        :returns A list of tuples for all commands that match the given setting.
                 Each tuple will be in the form (instance_name, command_name, callback)
        """
        # return a dictionary grouping all the commands by instance name
        commands_by_instance = {}
        for (name, value) in self.commands.iteritems():
            app_instance = value["properties"].get("app")
            if app_instance is None:
                continue
            instance_name = app_instance.instance_name
            commands_by_instance.setdefault(instance_name, []).append((name, value["callback"]))

        # go through the values from the setting and return any matching commands
        ret_value = []
        setting_value = self.get_setting(setting, [])
        for command in setting_value:
            command_name = command["name"]
            instance_name = command["app_instance"]
            instance_commands = commands_by_instance.get(instance_name)

            if instance_commands is None:
                self.log_warning(
                    "Error reading the '%s' configuration settings\n"
                    "The requested command '%s' from app '%s' isn't loaded.\n"
                    "Please make sure that you have the app installed" % (setting, command_name, instance_name))
                continue

            for (name, callback) in instance_commands:
                # add the command if the name from the settings is '' or the name matches
                if not command_name or (command_name == name):
                    ret_value.append((instance_name, name, callback))

        return ret_value

    def post_app_init(self):
        """
        Do any initialization after apps have been loaded
        """
        self.log_debug("%s: Running post app init..." % self)

        try:
            full_version_str = self.flame_version
            self.log_user_attribute_metric("Flame version", full_version_str)
        except:
            # ignore all errors. ex: using a core that doesn't support metrics
            pass

        # only run the startup commands when in DCC mode
        if self._engine_mode != self.ENGINE_MODE_DCC:
            return

        # run any commands registered via run_at_startup
        commands_to_start = self._get_commands_matching_setting("run_at_startup")
        for (instance_name, command_name, callback) in commands_to_start:
            self.log_debug("Running at startup: (%s, %s)" % (instance_name, command_name))
            callback()


    def destroy_engine(self):
        """
        Called when the engine is being destroyed
        """
        self.log_debug("%s: Destroying..." % self)

    @property
    def python_executable(self):
        """
        Returns the python executable associated with this engine
        
        :returns: path to python, e.g. '/usr/discreet/python/2016.0.0.322/bin/python'
        """
        return self._python_executable_path
    
    @property
    def preset_version(self):
        """
        Returns the preset version required for the currently executing 
        version of Flame. Preset xml files in Flame all have a version number 
        to denote which generation of the file format they implement. If you are using
        an old preset with a new version of Flame, a warning message appears. 
        
        :returns: Preset version, as string, e.g. '5'
        """  
        if self._flame_version is None:
            raise TankError("Cannot determine preset version - No Flame DCC version specified!")
        
        if self.is_version_less_than("2016.1"):
            # for version 2016 before ext 1, export preset is v5
            return "5" 
        elif self.is_version_less_than("2017"):
            # flame 2016 extension 1 and above.
            return "6"
        else:
            # flame 2017 and above
            #
            # Note: Flame 2017 uses preset 7, however further adjustments to the actual
            #       preset format used is required in individual apps - for the time being,
            #       the preset version is held at v6, ensuring that app apps operate correctly,
            #       but generating a warning message at startup.
            #
            return "7"

    @property
    def export_presets_root(self):
        """
        The location where flame export presets are located

        :returns: Path as string
        """
        if self.is_version_less_than("2017"):
            # flame 2016 presets structure
            return os.path.join(
                self.install_root,
                "presets",
                self.flame_version,
                "export",
                "presets"
            )
        else:
            # flame 2017+ presets structure (note the extra flame folder)
            return os.path.join(
                self.install_root,
                "presets",
                self.flame_version,
                "export",
                "presets",
                "flame"
            )

    def is_version_less_than(self, version_str):
        """
        Compares the given version string with the current 
        flame version and returns False if the given version is 
        greater than the current version.
        
        Example: 
        
        - Flame: '2016.1.0.278', version str: '2016.1' => False
        - Flame: '2016',  version str: '2016.1' => True
        
        :param version_str: Version to run comparison against
        """
        curr_version = self._flame_version["full"]
        return LooseVersion(curr_version) < LooseVersion(version_str)

    @property
    def flame_major_version(self):
        """
        Returns Flame's major version number as a string.
        
        :returns: String (e.g. '2016')
        """
        return self._flame_version["major"]
    
    @property
    def flame_minor_version(self):
        """
        Returns Flame's minor version number as a string.
        
        :returns: String (e.g. '2')
        """
        return self._flame_version["minor"]
    
    @property
    def flame_version(self):
        """
        Returns Flame's full version number as a string.
        
        :returns: String (e.g. '2016.1.0.278')
        """
        return self._flame_version["full"]

    @property
    def install_root(self):
        """
        The location where flame is installed.

        This may be '/usr/discreet', '/opt/Autodesk' etc.

        :returns: Path as string
        """
        return self._install_root

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
            # Note - Since Flame is a PySide only environment, we import it directly
            # rather than going through the sgtk wrappers.             
            from PySide import QtGui, QtCore
            if QtCore.QCoreApplication.instance():
                # there is an active application
                has_ui = True
        except:
            pass
        
        return has_ui

    def show_panel(self, panel_id, title, bundle, widget_class, *args, **kwargs):
        """
        Override the base show_panel to create a non-modal dialog that will stay on
        top of the Flame interface
        """
        if not self.has_ui:
            self.log_error("Sorry, this environment does not support UI display! Cannot show "
                           "the requested panel '%s'." % title)
            return None
        
        # Note - Since Flame is a PySide only environment, we import it directly
        # rather than going through the sgtk wrappers.         
        from PySide import QtGui, QtCore

        # create the dialog:
        dialog, widget = self._create_dialog_with_widget(title, bundle, widget_class, *args, **kwargs)
        dialog.setWindowFlags(
            dialog.windowFlags() |
            QtCore.Qt.WindowStaysOnTopHint &
            ~QtCore.Qt.WindowCloseButtonHint
        )
        
        # show the dialog        
        dialog.show()
        
        # lastly, return the instantiated widget
        return widget

    def log_debug(self, msg):
        """
        Log a debug message
        
        :param msg: The debug message to log
        """
        logging.getLogger(LOG_CHANNEL).debug(msg)        
 
    def log_info(self, msg):
        """
        Log some info
        
        :param msg: The info message to log
        """
        logging.getLogger(LOG_CHANNEL).info(msg)
 
    def log_warning(self, msg):
        """
        Log a warning
        
        :param msg: The warning message to log
        """
        logging.getLogger(LOG_CHANNEL).warning(msg)        
 
    def log_error(self, msg):
        """
        Log an error
        
        :param msg: The error message to log
        """        
        logging.getLogger(LOG_CHANNEL).error(msg)

    ################################################################################################################
    # Engine Bootstrap
    #
    
    def pre_dcc_launch_phase(self):
        """
        Special bootstrap method used to set up the Flame environment.
        This is designed to execute before Flame has launched, as part of the 
        bootstrapping process.

        This method assumes that it is being executed inside a Flame python
        and is called from the app_launcher script which ensures such an environment.
        
        The bootstrapper will first import the wiretap API and setup other settings.
        
        It then attempts to execute the pre-DCC project creation process, utilizing
        both wiretap and QT (setup project UI) for this.
        
        Finally, it will return the command line args to pass to Flame as it is being
        launched.
        
        :returns: arguments to pass to the app launch process
        """
        if self.get_setting("debug_logging"):
            # enable Flame hooks debug
            os.environ["DL_DEBUG_PYTHON_HOOKS"] = "1"
        
        # see if we can launch into batch mode. We only do this when in a 
        # shot context and if there is a published batch file in Shotgun
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
                if os.path.exists(batch_file_path):
                    self.log_debug("Setting auto startup file '%s'" % batch_file_path)
                    os.environ["DL_BATCH_START_WITH_SETUP"] = batch_file_path
        
        # add Flame hooks for this engine
        flame_hooks_folder = os.path.join(self.disk_location, self.FLAME_HOOKS_FOLDER)
        sgtk.util.append_path_to_env_var("DL_PYTHON_HOOK_PATH", flame_hooks_folder)
        self.log_debug("Added to hook path: %s" % flame_hooks_folder)
                
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
        if self._engine_mode in (self.ENGINE_MODE_DCC, self.ENGINE_MODE_BACKBURNER):
            # We are running the engine inside of the Flame Application.
            # alternatively, we are running the engine in backburner
            #
            # in both these states, no special QT init is necessary. 
            # Defer to default implementation which looks for pyside and 
            # gracefully fails in case that isn't found.
            self.log_debug("Initializing default PySide for in-DCC / backburner use")
            return super(FlameEngine, self)._define_qt_base()
        
        else:
            # we are running the engine outside of Flame.
            # This is special - no QApplication is running at this point -
            # a state akin to running apps inside the shell engine. 
            # We assume that in pre-launch mode, PySide is available since
            # we are running within the Flame python.
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
    # Any apps which are interested in registering custom exporters with Flame should use the methods
    # below. The register_export_hook() is called by apps in order to create a menu entry
    # on the Flame export menu. The remaining methods are used to call out from the actual Flame hook
    # to the relevant app code.
    #
    
    def register_export_hook(self, menu_caption, callbacks):
        """
        Allows an app to register an interest in one of the Flame export hooks.
        
        This is one of the interaction entry points in the system and this is how apps
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
        and info reflects the info parameter passed from Flame (varies for different callbacks).
        
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
        Creates a session object which represents a single export session in Flame.
        
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
        
        Dispatch method called from the various Flame hooks. 
        This method will ensure that the Flame callbacks will be 
        dispatched to the appropriate registered app callbacks.
        
        :param callback_name: Name of the Flame callback method
        :param session_id: Unique session identifier
        :param info: Metadata dictionary from Flame
        """
        self.log_debug("Flame engine export callback dispatch for %s" % callback_name)
        self.log_debug("Info parameters passed from Flame: %s" % pprint.pformat(info))
        
        if session_id not in self._export_sessions:
            self.log_debug("Ignoring request for unknown session %s..." % session_id)
            return
        
        # get the preset
        preset_name = self._export_sessions[session_id]
        tk_callbacks = self._registered_export_instances[preset_name]
        
        # call the callback in the preset
        if callback_name in tk_callbacks:
            # the app has registered interest in this!
            self.log_debug("Executing callback %s" % tk_callbacks[callback_name])
            tk_callbacks[callback_name](session_id, info)
        
    
    ################################################################################################################
    # batch callbacks handling
    #
    # Any apps which are interested in register custom batch exporters with Flame should use the methods
    # below. The register_batch_hook() is called by apps in order to register an interest in pre and post
    # export callbacks when in batch mode. The Flame engine will ensure that the app's callbacks will get 
    # called at the right time.
    #
    
    def register_batch_hook(self, callbacks):
        """
        Allows an app to register an interest in one of the Flame batch hooks.
        
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
        
        Dispatch method called from the various Flame hooks. 
        This method will ensure that the Flame callbacks will be 
        dispatched to the appropriate registered app callbacks.
        
        :param callback_name: Name of the Flame callback method
        :param session_id: Unique session identifier
        :param info: Metadata dictionary from Flame
        """
        self.log_debug("Flame engine batch callback dispatch for %s" % callback_name)
        self.log_debug("Info parameters passed from Flame: %s" % pprint.pformat(info))

        # dispatch to all callbacks
        for registered_batch_instance in self._registered_batch_instances:
            self.log_debug("Checking %s" % registered_batch_instance)
            if callback_name in registered_batch_instance:
                # the app has registered interest in this!
                self.log_debug("Executing callback %s" % registered_batch_instance[callback_name])
                registered_batch_instance[callback_name](info)
        

    
    
    ################################################################################################################
    # backburner integration
    #
    
    def get_server_hostname(self):
        """
        Return the hostname for the server which hosts this Flame setup.
        This is an accessor into the engine hook settings, allowing apps
        to query which host the closest Flame server is running on.
        
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

        backburner_job_cmd = os.path.join(self._install_root, "backburner", "cmdjob")

        # pass some args - most importantly tell it to run on the local host
        # looks like : chars are not valid so replace those
        backburner_args = []
        
        # run as current user, not as root
        backburner_args.append("-userRights")

        # increase the max task length to 600 minutes
        backburner_args.append("-timeout:600")

        # add basic job info
        # backburner does not do any kind of sanitaion itself, so ensure that job
        # info doesn't contain any strange characters etc
        
        # remove any non-trivial characters
        sanitized_job_name = re.sub('[^0-9a-zA-Z_\-,\. ]+', '_', job_name)        
        sanitized_job_desc = re.sub('[^0-9a-zA-Z_\-,\. ]+', '_', description)
        
        # if the job name contains too many characters, backburner submission fails
        if len(sanitized_job_name) > 70:    
            sanitized_job_name = "%s..." % sanitized_job_name[:67]
        if len(sanitized_job_desc) > 70:    
            sanitized_job_desc = "%s..." % sanitized_job_desc[:67]
        
        # there is a convention in flame to append a time stamp to jobs
        # e.g. 'Export - XXX_YYY_ZZZ (10.02.04)
        sanitized_job_name += datetime.datetime.now().strftime(" (%H.%M.%S)")
        
        backburner_args.append("-jobName:\"%s\"" % sanitized_job_name)
        backburner_args.append("-description:\"%s\"" % sanitized_job_desc)

        bb_manager = self.get_setting("backburner_manager")
        if bb_manager:
            # there is an external backburner manager specified.
            # this is only supported on 2016.1 and above
            if self.is_version_less_than("2016.1"):            
                self.log_warning("Backburner manager specifically set but this "
                                 "is only supported on Flame 2016.1 and above.")
            else:
                backburner_args.append("-manager:\"%s\"" % bb_manager)

        if run_after_job_id:
            backburner_args.append("-dependencies:%s" % run_after_job_id) # run after another job

        # call the bootstrap script
        backburner_bootstrap = os.path.join(self.disk_location, "python", "startup", "backburner.py")
        
        # assemble full cmd
        farm_cmd = "%s '%s'" % (self.python_executable, backburner_bootstrap)
        
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
        data["install_root"] = self._install_root
        data["flame_version"] = self._flame_version
        
        fh = open(session_file, "wb")
        pickle.dump(data, fh)
        fh.close()
        
        full_cmd = "%s %s %s %s" % (backburner_job_cmd, " ".join(backburner_args), farm_cmd, session_file)

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
        This is standard on all Flame installations.
        
        :param binary_name: Name of desired binary
        :returns: Absolute path as a string  
        """
        if sys.platform == "darwin":
            if int(self.flame_major_version) <= 2017:
                wtc_path = "/Library/WebServer/CGI-Executables/WiretapCentral"
            else:
                wtc_path = "/Library/WebServer/Documents/WiretapCentral/cgi-bin"
        elif sys.platform == "linux2":
            if int(self.flame_major_version) <= 2017:
                wtc_path = "/var/www/cgi-bin/WiretapCentral"
            else:
                wtc_path = "/var/www/html/WiretapCentral/cgi-bin"
        else:    
            raise TankError("Your operating system does not support wiretap central!")
        
        path = os.path.join(wtc_path, binary_name)
        if not os.path.exists(path):
            raise TankError("Cannot find binary '%s'!" % path)
        
        return path

    def get_ffmpeg_path(self):
        """
        Returns the path to the ffmpeg executable that ships with Flame.
        
        :returns: Absolute path as a string
        """
        return self.__get_wiretap_central_binary("ffmpeg")
                
    def get_read_frame_path(self):
        """
        Returns the path to the read_frame utility that ships with Flame.
        
        :returns: Absolute path as a string
        """
        return self.__get_wiretap_central_binary("read_frame")    

        
        
def sgtk_exception_trap(ex_cls, ex, tb):
    """
    UI Popup and logging exception trap override.
    
    This method is used to override the default exception reporting behaviour
    inside the embedded Flame python interpreter to make errors more visible 
    to the user.
    
    It attempts to create a QT messagebox with a formatted error message to
    alert the user that something has gong wrong. In addition to this, the
    default exception handling is also carried out and the exception is also
    written to the log.
    
    Note that this is a global object and not an engine-relative thing, so that
    the exception handler will operate correctly even if the engine instance no
    longer exists.
    """
    # careful about infinite loops here - we mustn't raise exceptions.
    
    # like in other environments and scripts, for TankErrors, we assume that the 
    # error message is already a nice descriptive, crafted message and try to present
    # this in a user friendly fashion
    # 
    # for other exception types, we give a full call stack.
    
    error_message = "Critical: Could not format error message."
    
    try:
        traceback_str = "\n".join(traceback.format_tb(tb))
        if ex_cls == TankError:
            # for TankErrors, we don't show the whole stack trace
            error_message = "A Shotgun error was reported:\n\n%s" % ex
        else:    
            error_message = "A Shotgun error was reported:\n\n%s (%s)\n\nTraceback:\n%s" % (ex, ex_cls, traceback_str)
    except:
        pass

    # now try to output it
    try:
        # Note - Since Flame is a PySide only environment, we import it directly
        # rather than going through the sgtk wrappers.         
        from PySide import QtGui, QtCore
        if QtCore.QCoreApplication.instance():
            # there is an application running - so pop up a message!
            QtGui.QMessageBox.critical(None, "Shotgun General Error", error_message)
    except:
        pass
    
    # and try to log it
    try:        
        error_message = "An exception was raised:\n\n%s (%s)\n\nTraceback:\n%s" % (ex, ex_cls, traceback_str)
        logging.getLogger(LOG_CHANNEL).error(error_message)
    except:
        pass
    
    # in addition to the ui popup, also defer to the default mechanism
    sys.__excepthook__(type, ex, tb)


