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
        "version": "[\w.]+",    # word chars and .
        "executable": "[\w]+",  # word characters (a-z0-9)
    }

    # This dictionary defines a list of executable template strings for each
    # of the supported operating systems. The templates are used for both
    # globbing and regex matches by replacing the named format placeholders
    # with an appropriate glob or regex string.
    EXECUTABLE_TEMPLATES = [
            # /usr/discreet/flame_2017.1/bin/startApplication
            # /usr/discreet/flameassist_2017.1.pr70/bin/startApplication
            # /usr/discreet/flare_2017.1/bin/startApplication
            # /usr/discreet/flamepremium_2017.1/bin/startApplication
            "/usr/discreet/{executable}_{version}/bin/startApplication",
            "/opt/Autodesk/{executable}_{version}/bin/startApplication",
    ]


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
        # flame comes with toolkit built-in, so no need to
        # run any startup logic.
        return LaunchInformation(exec_path, args, {})

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
        executable_templates = self.EXECUTABLE_TEMPLATES

        # all the discovered executables
        sw_versions = []

        for executable_template in executable_templates:

            self.logger.debug("Processing template %s.", executable_template)

            executable_matches = self._glob_and_match(
                executable_template,
                self.COMPONENT_REGEX_LOOKUP
            )

            # Extract all products from that executable.
            for (executable_path, key_dict) in executable_matches:

                # extract the matched keys form the key_dict (default to None if
                # not included)
                executable_version = key_dict.get("version")
                executable_name = key_dict.get("executable")

                # With the executable name we can map that to the proper product.
                executable_product = self.EXECUTABLE_TO_PRODUCT.get(executable_name)

                # only include the products that are covered in the EXECUTABLE_TO_PRODUCT dict
                if executable_product is None or executable_product not in self.EXECUTABLE_TO_PRODUCT.values():
                    self.logger.debug(
                        "Product '%s' is unrecognized. Skipping." %
                        (executable_product,)
                    )
                    continue

                # figure out which icon to use
                icon_path = os.path.join(
                    self.disk_location,
                    self.ICON_LOOKUP[executable_product]
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
