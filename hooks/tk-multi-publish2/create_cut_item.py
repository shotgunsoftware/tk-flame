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
        return "Create new Cut Item"

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
        publisher = self.parent
        engine = publisher.engine
        sg = engine.shotgun
        asset_info = item.properties["assetInfo"]
        path = item.properties["path"]
        publish_type = item.properties.get("type")
        name = item.properties["name"]
        asset_info = item.properties["assetInfo"]
        cut_code = item.properties["Sequence"]["code"]
        cut = item.properties["shared"]["cuts"].get(cut_code)

        if not cut:
            entity = sg.find_one("Sequence", [["code", "is", cut_code]])

            prev_cut = sg.find_one(
                "Cut",
                [["code", "is", cut_code],
                 ["entity", "is", entity]],
                ["revision_number"],
                [{"field_name": "revision_number", "direction": "desc"}]
            )

            if prev_cut is None:
                next_revision_number = 1
            else:
                next_revision_number = prev_cut["revision_number"] + 1

            cut = sg.create(
                "Cut",
                {
                    "project": item.context.project,
                    "entity": entity,
                    "code": cut_code,
                    "description": item.description,
                    "revision_number": next_revision_number,
                    "fps": float(asset_info["fps"])
                }
            )

            item.properties["shared"]["cuts"][cut_code] = cut

        item.properties["Cut"] = cut

        cut_item_data = {
            "project": item.context.project,
            "cut": cut,
            "description": item.description,
            "shot": item.properties.get("Shot"),
            "code": asset_info["assetName"],
            "version": item.properties.get("Version"),
            "cut_order": asset_info["segmentIndex"]
        }

        job_ids = item.properties.get("backgroundJobId")
        job_ids_str = ",".join(job_ids) if job_ids else None

        engine.create_local_backburner_job(
            "Upload Cut Item Image Preview",
            "%s: %s" % (publish_type, name),
            job_ids_str,
            "backburner_hooks",
            "attach_jpg_preview",
            {
                "targets": [cut],
                "width": asset_info["width"],
                "height": asset_info["height"],
                "path": path,
                "name": name
            }
        )

        cut_item = sg.create("CutItem", cut_item_data)
        item.properties["CutItem"] = cut_item

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

    def _frames_to_timecode(self, total_frames, frame_rate, drop):
        """
        Helper method that converts frames to SMPTE timecode.

        :param total_frames: Number of frames
        :param frame_rate: frames per second
        :param drop: true if time code should drop frames, false if not
        :returns: SMPTE timecode as string, e.g. '01:02:12:32' or '01:02:12;32'
        """
        if drop and frame_rate not in [29.97, 59.94]:
            raise NotImplementedError("Time code calculation logic only supports drop frame "
                                      "calculations for 29.97 and 59.94 fps.")

        # for a good discussion around time codes and sample code, see
        # http://andrewduncan.net/timecodes/

        # round fps to the nearest integer
        # note that for frame rates such as 29.97 or 59.94,
        # we treat them as 30 and 60 when converting to time code
        # then, in some cases we 'compensate' by adding 'drop frames',
        # e.g. jump in the time code at certain points to make sure that
        # the time code calculations are roughly right.
        #
        # for a good explanation, see
        # https://documentation.apple.com/en/finalcutpro/usermanual/index.html#chapter=D%26section=6
        fps_int = int(round(frame_rate))

        if drop:
            # drop-frame-mode
            # add two 'fake' frames every minute but not every 10 minutes
            #
            # example at the one minute mark:
            #
            # frame: 1795 non-drop: 00:00:59:25 drop: 00:00:59;25
            # frame: 1796 non-drop: 00:00:59:26 drop: 00:00:59;26
            # frame: 1797 non-drop: 00:00:59:27 drop: 00:00:59;27
            # frame: 1798 non-drop: 00:00:59:28 drop: 00:00:59;28
            # frame: 1799 non-drop: 00:00:59:29 drop: 00:00:59;29
            # frame: 1800 non-drop: 00:01:00:00 drop: 00:01:00;02
            # frame: 1801 non-drop: 00:01:00:01 drop: 00:01:00;03
            # frame: 1802 non-drop: 00:01:00:02 drop: 00:01:00;04
            # frame: 1803 non-drop: 00:01:00:03 drop: 00:01:00;05
            # frame: 1804 non-drop: 00:01:00:04 drop: 00:01:00;06
            # frame: 1805 non-drop: 00:01:00:05 drop: 00:01:00;07
            #
            # example at the ten minute mark:
            #
            # frame: 17977 non-drop: 00:09:59:07 drop: 00:09:59;25
            # frame: 17978 non-drop: 00:09:59:08 drop: 00:09:59;26
            # frame: 17979 non-drop: 00:09:59:09 drop: 00:09:59;27
            # frame: 17980 non-drop: 00:09:59:10 drop: 00:09:59;28
            # frame: 17981 non-drop: 00:09:59:11 drop: 00:09:59;29
            # frame: 17982 non-drop: 00:09:59:12 drop: 00:10:00;00
            # frame: 17983 non-drop: 00:09:59:13 drop: 00:10:00;01
            # frame: 17984 non-drop: 00:09:59:14 drop: 00:10:00;02
            # frame: 17985 non-drop: 00:09:59:15 drop: 00:10:00;03
            # frame: 17986 non-drop: 00:09:59:16 drop: 00:10:00;04
            # frame: 17987 non-drop: 00:09:59:17 drop: 00:10:00;05

            # calculate number of drop frames for a 29.97 std NTSC
            # workflow. Here there are 30*60 = 1800 frames in one
            # minute

            FRAMES_IN_ONE_MINUTE = 1800 - 2

            FRAMES_IN_TEN_MINUTES = (FRAMES_IN_ONE_MINUTE * 10) - 2

            ten_minute_chunks = total_frames / FRAMES_IN_TEN_MINUTES
            one_minute_chunks = total_frames % FRAMES_IN_TEN_MINUTES

            ten_minute_part = 18 * ten_minute_chunks
            one_minute_part = 2 * ((one_minute_chunks - 2) / FRAMES_IN_ONE_MINUTE)

            if one_minute_part < 0:
                one_minute_part = 0

            # add extra frames
            total_frames += ten_minute_part + one_minute_part

            # for 60 fps drop frame calculations, we add twice the number of frames
            if fps_int == 60:
                total_frames = total_frames * 2

            # time codes are on the form 12:12:12;12
            smpte_token = ";"

        else:
            # time codes are on the form 12:12:12:12
            smpte_token = ":"

        # now split our frames into time code
        hours = int(total_frames / (3600 * fps_int))
        minutes = int(total_frames / (60 * fps_int) % 60)
        seconds = int(total_frames / fps_int % 60)
        frames = int(total_frames % fps_int)
        return "%02d:%02d:%02d%s%02d" % (hours, minutes, seconds, smpte_token, frames)

