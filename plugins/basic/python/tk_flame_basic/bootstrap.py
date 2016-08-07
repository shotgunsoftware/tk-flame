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
import re
import sys
from PySide import QtGui, QtCore
from sgtk_plugin_basic import manifest

from .welcome_dialog import WelcomeDialog

g_toolkit_init_complete = False

def bootstrap_flame(plugin_root, project_name):
    """
    Main entry point for Shotgun boostrap.
    Executed whenever a project is being started.

    :param plugin_root: Root folder for the plugin
    :param project_name: Name of the flame project that is being launched.
    """
    global g_toolkit_init_complete

    if not g_toolkit_init_complete:
        # import toolkit
        import sgtk

        # initialize logging to disk
        sgtk.LogManager().initialize_base_file_handler("tk-flame")
        sgtk.LogManager().global_debug = manifest.debug_logging
        g_toolkit_init_complete = True

        if manifest.log_to_stdout:
            sgtk.LogManager().initialize_custom_handler()

    else:
        # toolkit already present
        import sgtk

    # kick off logging
    logger = sgtk.LogManager.get_logger(__name__)
    logger.debug("Flame sgtk project hook waking up!")
    logger.debug("Manifest: %s" % manifest.BUILD_INFO)

    # turn off previous running engines
    if sgtk.platform.current_engine():
        logger.debug("Engine already running - shutting it down...")
        sgtk.platform.current_engine().destroy()
        logger.debug("... previous engine shutdown complete")

    # check if we are exiting out to the project select screen
    if project_name == "":
        logger.debug("exited out to the project selection screen.")
        # don't try to start up an engine for this case.
        return


    # check if we are already logged in
    authenticator = sgtk.authentication.ShotgunAuthenticator()
    if authenticator.get_default_user() is None:

        logger.debug("We are not logged in - pop up UI to tell user about shotgun.")

        # we were not authenticated - in this case tell user about shotgun
        welcome_ui = WelcomeDialog()
        status = welcome_ui.exec_()

        if status == welcome_ui.NEW_SITE:
            # navigate to site register page and bail
            QtGui.QDesktopServices.openUrl(QtCore.QUrl("https://www.shotgunsoftware.com/signup"))
            return

        elif status == welcome_ui.LEARN_MORE:
            # navigate to home page and bail
            QtGui.QDesktopServices.openUrl(QtCore.QUrl("https://www.shotgunsoftware.com"))
            return

    # authenticate and log in
    user = authenticator.get_user()
    sg = user.create_sg_connection()

    logger.debug("Logged in to Shotgun! %s" % user)




    # see if a project exists
    logger.debug(
        "Checking if a project '%s' exists on %s..." % (project_name, sg.base_url)
    )
    proj = sg.find_one(
        "Project",
        [["tank_name", "is", project_name]]
    )

    if proj is None:

        logger.debug("No associated project found - launching site level engine to prompt.")

        # no project match - in this case pop up the UI where the user can manage projects
        engine = _bootstrap_flame_engine(user, entity=None)

        # start up app
        project_create_app = engine.apps["tk-flame-projectcreate"]
        proj = project_create_app.show_modal(project_name)

        logger.debug("Project create app returned project %s" % proj)

        # kill engine
        engine.destroy()

        if proj is None:
            # user didn't want to create project for this one
            logger.debug("Early exit. No associated shotgun project.")
            return

    logger.debug("Starting up actual integration for proj %s" % proj)
    engine = _bootstrap_flame_engine(user, entity=proj)

    logger.debug("Adding custom actions")
    engine.register_command("wintermute.shotgunstudio.com", callback)
    engine.register_command("Log out", callback)



def callback():

    print "CALLBACK"


def _bootstrap_flame_engine(user, entity):
    import sgtk

    # start up toolkit via the manager
    mgr = sgtk.bootstrap.ToolkitManager(user)

    # add our local baked cache to the search path
    this_dir = os.path.abspath(os.path.dirname(__file__))
    plugin_root_dir = os.path.abspath(os.path.join(this_dir, "..", ".."))
    mgr.bundle_cache_fallback_paths = [os.path.join(plugin_root_dir, "bundle_cache")]

    # define our entry point
    mgr.entry_point = manifest.entry_point

    # Set up our config:
    #
    # The config is stored in the plugin for the time being.
    # In the future, it should be moved out into a separate
    # repository so that updates can be pushed out automatically.
    #
    mgr.base_configuration = manifest.base_configuration

    # flag to the engine that it operates in its main mode
    os.environ["TOOLKIT_FLAME_ENGINE_MODE"] = "DCC"

    engine = mgr.bootstrap_engine("tk-flame", entity=entity)

    # clean up operational state
    del os.environ["TOOLKIT_FLAME_ENGINE_MODE"]

    # figure out our flame version
    (install_root, major_ver, minor_ver, version_str) = _determine_flame_version()

    # pass the python executable from the bootstrap to the engine
    python_binary = "%s/python/%s/bin/python" % (install_root, version_str)
    engine.set_python_executable(python_binary)

    # set the install root
    engine.set_install_root(install_root)

    # and the version number
    engine.set_version_info(str(major_ver), str(minor_ver), version_str)

    return engine

def _determine_flame_version():
    """
    Returns the version string for the given Flame path

    <INSTALL_ROOT>/flameassist_2015.2/bin/startApplication        --> (<INTALL_ROOT>, 2015, 2, "2015.2")
    <INSTALL_ROOT>/flameassist_2015.3/bin/startApplication        --> (<INTALL_ROOT>, 2015, 3, "2015.3")
    <INSTALL_ROOT>/flameassist_2016.0.0.322/bin/startApplication  --> (<INTALL_ROOT>, 2016, 0, "2016.0.0.322")
    <INSTALL_ROOT>/flameassist_2015.2.pr99/bin/startApplication   --> (<INTALL_ROOT>, 2015, 2, "2015.2.pr99")
    <INSTALL_ROOT>/flame_2016.pr50/bin/start_Flame                --> (<INTALL_ROOT>, 2016, 0, "2016.pr50")

    If the minor or major version cannot be extracted, it will be set to zero.

    :returns: (install_root, major (int), minor (int), full_str)
    """
    import sgtk
    logger = sgtk.LogManager.get_logger(__name__)

    # sys.executable returns
    # /usr/discreet/flame_2017/bin/flame.app/Contents/MacOS/flame
    # /usr/discreet/flame_2017.pr65/...
    flame_executable_path = sys.executable

    logger.debug("Analysing executable path '%s' to determine flame properties..." % flame_executable_path)

    re_match = re.search("(^.*)/fla[mr]e[^_]*_([^/]+)/bin", flame_executable_path)
    install_root = re_match.group(1)
    version_str = re_match.group(2)

    logger.debug("Flame install root is '%s'" % install_root)
    logger.debug("Flame version is '%s'" % version_str)

    # Examples:
    # 2015.2
    # 2016
    # 2016.pr99
    # 2015.2.pr99

    major_ver = 0
    minor_ver = 0

    chunks = version_str.split(".")
    if len(chunks) > 0:
        if chunks[0].isdigit():
            major_ver = int(chunks[0])

    if len(chunks) > 1:
        if chunks[1].isdigit():
            minor_ver = int(chunks[1])

    return install_root, major_ver, minor_ver, version_str


