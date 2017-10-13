# Copyright (c) 2017 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import os
import sgtk

HookBaseClass = sgtk.get_hook_baseclass()


class CreateCutPlugin(HookBaseClass):
    """
    Plugin for creating generic publishes in Shotgun
    """

    @property
    def icon(self):
        """
        Path to an png icon on disk
        """

        # look for icon one level up from this hook's folder in "icons" folder
        return os.path.join(
            self.disk_location,
            os.pardir,
            "icons",
            "publish.png"
        )

    @property
    def name(self):
        """
        One line display name describing the plugin
        """
        return "Create new Cut"

    @property
    def description(self):
        """
        Verbose, multi-line description of what the plugin does. This can
        contain simple html for formatting.
        """
        return ""

    @property
    def settings(self):
        """
        Dictionary defining the settings that this plugin expects to recieve
        through the settings parameter in the accept, validate, publish and
        finalize methods.

        A dictionary on the following form::

            {
                "Settings Name": {
                    "type": "settings_type",
                    "default": "default_value",
                    "description": "One line description of the setting"
            }

        The type string should be one of the data types that toolkit accepts
        as part of its environment configuration.
        """
        return {}

    @property
    def item_filters(self):
        """
        List of item types that this plugin is interested in.

        Only items matching entries in this list will be presented to the
        accept() method. Strings can contain glob patters such as *, for example
        ["maya.*", "file.maya"]
        """
        return ["flame.batch"]

    def accept(self, settings, item):
        """
        Method called by the publisher to determine if an item is of any
        interest to this plugin. Only items matching the filters defined via the
        item_filters property will be presented to this method.

        A publish task will be generated for each item accepted here. Returns a
        dictionary with the following booleans:

            - accepted: Indicates if the plugin is interested in this value at
                all. Required.
            - enabled: If True, the plugin will be enabled in the UI, otherwise
                it will be disabled. Optional, True by default.
            - visible: If True, the plugin will be visible in the UI, otherwise
                it will be hidden. Optional, True by default.
            - checked: If True, the plugin will be checked in the UI, otherwise
                it will be unchecked. Optional, True by default.

        :param settings: Dictionary of Settings. The keys are strings, matching
            the keys returned in the settings property. The values are `Setting`
            instances.
        :param item: Item to process

        :returns: dictionary with boolean keys accepted, required and enabled
        """

        MIN_CUT_SG_VERSION = (7, 0, 0)

        sg = sgtk.platform.current_engine().shotgun

        cut_supported = sg.server_caps.version >= MIN_CUT_SG_VERSION

        shot_context = item.context.entity["type"] == "Shot"

        accepted = cut_supported and shot_context

        return {"accepted": accepted}

    def validate(self, settings, item):
        """
        Validates the given item to check that it is ok to publish.

        Returns a boolean to indicate validity.

        :param settings: Dictionary of Settings. The keys are strings, matching
            the keys returned in the settings property. The values are `Setting`
            instances.
        :param item: Item to process

        :returns: True if item is valid, False otherwise.
        """

        if "created_cut" not in item.properties["shared"]:
            item.properties["shared"]["cuts"] = {}

        return True

    def publish(self, settings, item):
        """
        Executes the publish logic for the given item and settings.

        :param settings: Dictionary of Settings. The keys are strings, matching
            the keys returned in the settings property. The values are `Setting`
            instances.
        :param item: Item to process
        """

        sg = sgtk.platform.current_engine().shotgun

        sequence_name = item.properties["assetInfo"].get("sequenceName")

        if sequence_name is None:
            shot = sg.find_one("Shot", [["id", "is", item.context.entity["id"]]], ["sg_sequence"])
            sequence_name = shot["sequence_name"]

        cut = item.properties["shared"]["cuts"].get(sequence_name)

        if not cut:
            entity = sg.find_one("Sequence", [["code", "is", sequence_name]])

            # first determine which revision number of the cut to create
            prev_cut = sg.find_one(
                "Cut",
                [["code", "is", sequence_name],
                 ["entity", "is", entity]],
                ["revision_number"],
                [{"field_name": "revision_number", "direction": "desc"}]
            )

            if prev_cut is None:
                next_revision_number = 1
            else:
                next_revision_number = prev_cut["revision_number"] + 1

            # first create a new cut
            cut = sg.create(
                "Cut",
                {
                    "project": item.context.project,
                    "entity": entity,
                    "code": sequence_name,
                    "description": item.description,
                    "revision_number": next_revision_number,
                }
            )

            item.properties["shared"]["cuts"][sequence_name] = cut



    def finalize(self, settings, item):
        """
        Execute the finalization pass. This pass executes once
        all the publish tasks have completed, and can for example
        be used to version up files.

        :param settings: Dictionary of Settings. The keys are strings, matching
            the keys returned in the settings property. The values are `Setting`
            instances.
        :param item: Item to process
        """

        pass
