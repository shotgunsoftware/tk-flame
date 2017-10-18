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


class PushShotMetadataPlugin(HookBaseClass):
    """
    Plugin for pushing Shot metadata in Shotgun
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
        return "Update Shot metadata"

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
        return ["flame.batchOpenClip"]

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

        is_accepted = item.context.entity["type"] == "Shot" and not item.properties["fromBatch"]

        if is_accepted:
            is_checked = False
            shot_data = self._shot_data(item)
            query_filter = [["id", "is", item.context.entity["id"]]]
            query_fields = shot_data.keys()
            shot_info = self.parent.shotgun.find_one("Shot", fields=query_fields, filters=query_filter)

            for k, v in shot_data.items():
                if shot_info[k] != v:
                    is_checked = True
                    break
        else:
            is_checked = False

        return {
            "accepted": is_accepted,
            "checked": is_checked
        }

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
        return item.context.entity["type"] == "Shot"

    def publish(self, settings, item):
        """
        Executes the publish logic for the given item and settings.

        :param settings: Dictionary of Settings. The keys are strings, matching
            the keys returned in the settings property. The values are `Setting`
            instances.
        :param item: Item to process
        """

        publisher = self.parent
        engine = publisher.engine
        shot_data = self._shot_data(item)
        asset_info = item.properties["assetInfo"]
        path = item.properties["path"]
        publish_type = item.properties.get("type")
        name = item.properties["name"]

        self.parent.shotgun.update("Shot", item.context.entity['id'], shot_data)

        job_ids = item.properties.get("backgroundJobId")
        job_ids_str = ",".join(job_ids) if job_ids else None

        engine.create_local_backburner_job(
            "Upload Shot Image Preview",
            "%s: %s" % (publish_type, name),
            job_ids_str,
            "backburner_hooks",
            "attach_jpg_preview",
            {
                "targets": [item.context.entity],
                "width": asset_info["width"],
                "height": asset_info["height"],
                "path": path,
                "name": name
            }
        )
        if asset_info["segmentIndex"] == 1:
            sequence = item.properties.get("Sequence")

            if sequence:
                engine.create_local_backburner_job(
                    "Upload Sequence Image Preview",
                    "%s: %s" % (publish_type, name),
                    job_ids_str,
                    "backburner_hooks",
                    "attach_jpg_preview",
                    {
                        "targets": [sequence],
                        "width": asset_info["width"],
                        "height": asset_info["height"],
                        "path": path,
                        "name": name
                    }
                )

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

    def _shot_data(self, item):
        asset_info = item.properties["assetInfo"]

        shot_data = {
            "description": item.description,
            "sg_cut_in": asset_info["handleIn"],
            "sg_head_in": 0,
            "sg_cut_order": asset_info["segmentIndex"]
        }
        shot_data["sg_cut_out"] = shot_data["sg_cut_in"] + (asset_info["recordOut"] - asset_info["recordIn"] - 1 )
        shot_data["sg_cut_duration"] = shot_data["sg_cut_out"] - shot_data["sg_cut_in"] + 1
        shot_data["sg_tail_out"] = shot_data["sg_cut_out"] + asset_info["handleOut"]

        return shot_data
