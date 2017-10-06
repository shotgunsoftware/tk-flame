# Copyright (c) 2016 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import os
import sys

import sgtk
from sgtk import TankError
from sgtk.platform import SoftwareLauncher, SoftwareVersion, LaunchInformation


class FlameLauncher(SoftwareLauncher):
    """
    Handles launching Flame executables. Automatically starts up a tk-flame
    engine with the current context in the new session of Houdini.
    """

    # A lookup to map an executable name to a product. This is critical for
    # linux where the product does not show up in the path.
    EXECUTABLE_TO_PRODUCT = {
        "flame": "Flame",
        "flameassist": "Flame Assist",
        "flare": "Flare",
        "flamepremium": "Flame Premium",
    }

    # lookup for icons
    ICON_LOOKUP = {
        "Flame": "icon_256.png",
        "Flame Assist": "flame_assist_icon_256.png",
        "Flare": "flare_icon_256.png",
        "Flame Premium": "icon_256.png"
    }

    # Named regex strings to insert into the executable template paths when
    # matching against supplied versions and products. Similar to the glob
    # strings, these allow us to alter the regex matching for any of the
    # variable components of the path in one place
    COMPONENT_REGEX_LOOKUP = {
        "darwin": {
            "version": "\d.*",  # starts with a number followed by anything
            "product": "[ \w]+",  # spaces and word characters
            "app": ".*",  # spaces and word characters
        },
        "linux2": {
            "version": "\d.*",  # starts with a number followed by anything
            "executable": "[\w]+",  # word characters (a-z0-9)
        }
    }

    # This dictionary defines a list of executable template strings for each
    # of the supported operating systems. The templates are used for both
    # globbing and regex matches by replacing the named format placeholders
    # with an appropriate glob or regex string.
    EXECUTABLE_TEMPLATES = {
        "darwin": [
            # /Applications/Autodesk/Flame 2018/Flame 2018.app
            # /Applications/Autodesk/Flame 2017.1.pr70/Flame 2017.1.pr70.app
            # /Applications/Autodesk/Flame Assist 2017.1.pr70/Flame Assist 2017.1.pr70.app
            "/Applications/Autodesk/{product} {version}/{app}.app",
        ],
        "linux2": [
            # /usr/discreet/flame_2017.1/bin/startApplication
            # /usr/discreet/flameassist_2017.1.pr70/bin/startApplication
            # /usr/discreet/flare_2017.1/bin/startApplication
            # /usr/discreet/flamepremium_2017.1/bin/startApplication
            "/usr/discreet/{executable}_{version}/bin/startApplication",
            "/opt/Autodesk/{executable}_{version}/bin/startApplication",
        ]
    }

    @property
    def minimum_supported_version(self):
        """
        The minimum supported Flame version.
        """
        # 2018 was the first version of flame that shipped with taap included.
        return "2018"

    def prepare_launch(self, exec_path, args, file_to_open=None):
        """
        Prepares the given software for launch

        :param str exec_path: Path to DCC executable to launch

        :param str args: Command line arguments as strings

        :param str file_to_open: (optional) Full path name of a file to open on
            launch

        :returns: :class:`LaunchInformation` instance
        """
        plugin_based_launch = self.get_setting("plugin_based_launch")

        # If there is a plugin to launch with, we don't have much in the
        # way of prep work to do.
        if plugin_based_launch:
            # flame comes with toolkit built-in, so no need to
            # run any startup logic.
            env = {
                "SHOTGUN_SITE": self.sgtk.shotgun_url,
                "SHOTGUN_ENTITY_ID": str(self.context.project["id"]),
                "SHOTGUN_ENTITY_TYPE": str(self.context.project["type"]),
                "SHOTGUN_ENTITY_NAME": str(self.context.project["name"])
            }
        else:
            # Classic launch situation, so we use the old prep logic
            # prior to the bootstrap.
            env = dict()
            engine_path = os.path.dirname(__file__)

            # find bootstrap file located in the engine and load that up
            startup_path = os.path.join(engine_path, "python", "startup")

            # add our bootstrap location to the pythonpath
            sys.path.insert(0, startup_path)
            try:
                import bootstrap
                (exec_path, args) = bootstrap.bootstrap(
                    self.engine_name,
                    self.context,
                    exec_path,
                    args,
                )
            except Exception, e:
                self.logger.exception("Error executing engine bootstrap script.")

                if sgtk.platform.current_engine().has_ui:
                    # We have UI support. Launch a dialog with a nice message.
                    from sgtk.platform.qt import QtGui
                    msg = ("<b style='color: rgb(252, 98, 70)'>Failed to launch "
                           "Flame!</b><br><br>The following error was reported: "
                           "<b>%s</b>" %
                            str(e))
                    QtGui.QMessageBox.critical(None, "Flame launch failed!", msg)
                raise TankError("Error executing bootstrap script. Please see log for details.")
            finally:
                # remove bootstrap from sys.path
                sys.path.pop(0)

        return LaunchInformation(exec_path, args, env)

    def scan_software(self):
        """
        Scan the filesystem for flame executables.

        :return: A list of :class:`SoftwareVersion` objects.
        """

        self.logger.debug("Scanning for Flame executables...")

        supported_sw_versions = []
        for sw_version in self._find_software():
            (supported, reason) = self._is_supported(sw_version)
            if supported:
                supported_sw_versions.append(sw_version)
            else:
                self.logger.debug(
                    "SoftwareVersion %s is not supported: %s" %
                    (sw_version, reason)
                )

        return supported_sw_versions

    def _find_software(self):

        # all the executable templates for the current OS
        executable_templates = self.EXECUTABLE_TEMPLATES.get(sys.platform, [])
        executable_regexp = self.COMPONENT_REGEX_LOOKUP.get(sys.platform, [])

        # all the discovered executables
        sw_versions = []

        for executable_template in executable_templates:

            self.logger.debug("Processing template %s.", executable_template)

            executable_matches = self._glob_and_match(
                executable_template,
                executable_regexp
            )

            # Extract all products from that executable.
            for (executable_path, key_dict) in executable_matches:

                # extract the matched keys form the key_dict (default to None if
                # not included)
                executable_version = key_dict.get("version")
                executable_product = key_dict.get("product")
                executable_name = key_dict.get("executable")
                executable_app = key_dict.get("app")

                # we need a product to match against. If that isn't provided,
                # then an executable name should be available. We can map that
                # to the proper product.
                if not executable_product:
                    executable_product = \
                        self.EXECUTABLE_TO_PRODUCT.get(executable_name)

                # Unknown product
                if not executable_product:
                    continue

                # Adapt the FlameAssist product name
                if executable_product == "FlameAssist":
                    executable_product = "Flame Assist"

                # only include the products that are covered in the EXECUTABLE_TO_PRODUCT dict
                if not executable_product.startswith("Flame") and not executable_product.startswith("Flare"):
                    self.logger.debug(
                        "Product '%s' is unrecognized. Skipping." %
                        (executable_product,)
                    )
                    continue

                # exclude Technology demo apps
                if executable_app and "Technology Demo" in executable_app:
                    self.logger.debug(
                        "Ignoring '%s %s - %s'" %
                        (executable_product, executable_version, executable_app)
                    )
                    continue

                # figure out which icon to use
                icon_path = os.path.join(
                    self.disk_location,
                    self.ICON_LOOKUP.get(executable_product, self.ICON_LOOKUP["Flame"])
                )
                self.logger.debug("Using icon path: %s" % (icon_path,))

                sw_versions.append(
                    SoftwareVersion(
                        executable_version,
                        executable_product,
                        executable_path,
                        icon_path
                    )
                )

        return sw_versions
