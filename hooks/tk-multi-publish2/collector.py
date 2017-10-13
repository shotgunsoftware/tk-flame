# Copyright (c) 2017 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Ccollect_current_sceneode License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import mimetypes
import os
import sys

import re
import sgtk

HookBaseClass = sgtk.get_hook_baseclass()

# This is a dictionary of file type info that allows the basic collector to
# identify common production file types and associate them with a display name,
# item type, and config icon.
COMMON_FILE_INFO = {
    "Alembic Cache": {
        "extensions": ["abc"],
        "icon": "alembic.png",
        "item_type": "file.alembic",
    },
    "3dsmax Scene": {
        "extensions": ["max"],
        "icon": "3dsmax.png",
        "item_type": "file.3dsmax",
    },
    "Hiero Project": {
        "extensions": ["hrox"],
        "icon": "hiero.png",
        "item_type": "file.hiero",
    },
    "Houdini Scene": {
        "extensions": ["hip", "hipnc"],
        "icon": "houdini.png",
        "item_type": "file.houdini",
    },
    "Maya Scene": {
        "extensions": ["ma", "mb"],
        "icon": "maya.png",
        "item_type": "file.maya",
    },
    "Nuke Script": {
        "extensions": ["nk"],
        "icon": "nuke.png",
        "item_type": "file.nuke",
    },
    "Photoshop Image": {
        "extensions": ["psd", "psb"],
        "icon": "photoshop.png",
        "item_type": "file.photoshop",
    },
    "Rendered Image": {
        "extensions": ["dpx", "exr"],
        "icon": "image_sequence.png",
        "item_type": "file.image",
    },
    "Texture Image": {
        "extensions": ["tiff", "tx", "tga", "dds", "rat"],
        "icon": "texture.png",
        "item_type": "file.texture",
    },
    "Flame Batch File": {
        "extensions": ["batch"],
        "icon": "texture.png",
        "item_type": "file.texture",
    },
    "Open Clip": {
        "extensions": ["clip"],
        "icon": "texture.png",
        "item_type": "file.texture",
    },
}


class FlameItemCollector(HookBaseClass):
    """
    A basic collector that handles files and general objects.
    """

    def process_current_session(self, parent_item):
        # go ahead and build the path to the icon for use by any documents
        """

        :param parent_item:
        """
        publisher = self.parent
        engine = publisher.engine
        project = publisher.context.project
        export_context = engine.export_cache
        engine.clean_export_cache()

        shared_information = {}

        if type(export_context) is dict:
            for sequence_name, sequence_info in sorted(export_context.items()):
                sequence = None
                if sequence_name:
                    sg_filter = [["code", "is", sequence_name], ["project", "is", project]]

                    sequences = publisher.shotgun.find("Sequence", sg_filter)

                    if not sequences:
                        seq_data = {
                            "code": sequence_name,
                            "project": project
                        }

                        sequence = publisher.shotgun.create("Sequence", seq_data)
                    elif len(sequences) == 1:
                        sequence = sequences[0]

                for shot_name, shot_info in sorted(sequence_info.items()):
                    shot = None
                    if shot_name:
                        sg_filter = [["code", "is", shot_name]]

                        if sequence:
                            sg_filter.append(["sg_sequence", "is", sequence])

                        shots = publisher.shotgun.find("Shot", sg_filter)

                        if not shots:
                            shot_data = {
                                "code": shot_name,
                                "project": project
                            }

                            if sequence:
                                shot_data["sg_sequence"] = sequence

                            shot = publisher.shotgun.create("Shot", shot_data)
                        elif len(shots) == 1:
                            shot = shots[0]

                    key_order = ["batch", "batchOpenClip", "openClip", "video", "audio", "sequence"]
                    for asset_type, asset_type_info in sorted(shot_info.items(), key=lambda i: key_order.index(i[0])):
                        for asset_info, asset_info_list in asset_type_info.items():
                            for asset_info in asset_info_list:

                                create_item = getattr(self, "create_{}_items".format(asset_type))
                                items = create_item(parent_item, asset_info)
                                for item in items:
                                    item.properties["fromBatch"] = False
                                    item.properties["assetInfo"] = asset_info
                                    item.properties["lastJobID"] = asset_info.get("backgroundJobID")
                                    item.properties["shared"] = shared_information
                                    item.properties["Shot"] = shot
                                    item.properties["Sequence"] = sequence

                                    is_sequence = item.properties.get("is_sequence", False)

                                    if is_sequence:
                                        # generate the name from one of the actual files in the sequence
                                        name_path = item.properties["sequence_files"][0]
                                    else:
                                        name_path = item.properties["path"]

                                    # get the publish name for this file path. this will ensure we get a
                                    # consistent name across version publishes of this file.
                                    item.properties["name"] = publisher.util.get_publish_name(
                                        name_path, sequence=is_sequence)

                                    if shot:
                                        item.context = publisher.sgtk.context_from_entity(shot["type"], shot["id"])
                                    elif sequence:
                                        item.context = publisher.sgtk.context_from_entity(sequence["type"],
                                                                                          sequence["id"])

        elif type(export_context) == list:
            for asset_info in export_context:
                shot = None
                sequence = None
                shot_name = asset_info.get("shotName", "")

                if shot_name:
                    sg_filter = [["code", "is", shot_name]]
                    shots = publisher.shotgun.find("Shot", sg_filter, ["sg_sequence"])

                    if len(shots) == 1:
                        shot = shots[0]
                        sequence = shot["sg_sequence"]

                if shot is None and "openClipResolvedPath" in asset_info:
                    filters = [["project", "is", project]]
                    fields = ["path", "entity"]
                    entity_type = "PublishedFile"

                    published_files = self.parent.shotgun.find(
                        entity_type, filters=filters, fields=fields
                    )
                    for publish_file in published_files:
                        if asset_info["openClipResolvedPath"] in publish_file.get("path", {}).get("url", ""):
                            shot = publish_file.get("entity", None)

                if shot and not sequence:
                    filter = [["id", "is", shot["id"]]]
                    fields = ["sg_sequence"]
                    entity_type = "Shot"

                    shots = self.parent.shotgun.find(
                        entity_type, filters=filter, fields=fields
                    )

                    if len(shots) == 1:
                        sequence = shots[0]["sg_sequence"]

                items = self.create_render_items(parent_item, asset_info)
                for item in items:
                    item.properties["fromBatch"] = True
                    item.properties["assetInfo"] = asset_info
                    item.properties["lastJobID"] = asset_info.get("backgroundJobID")
                    item.properties["shared"] = shared_information
                    item.properties["Shot"] = shot
                    item.properties["Sequence"] = sequence

                    is_sequence = item.properties.get("is_sequence", False)

                    if is_sequence:
                        # generate the name from one of the actual files in the sequence
                        name_path = item.properties["sequence_files"][0]
                    else:
                        name_path = item.properties["path"]

                    # get the publish name for this file path. this will ensure we get a
                    # consistent name across version publishes of this file.
                    item.properties["name"] = publisher.util.get_publish_name(
                        name_path, sequence=is_sequence)

                    if shot:
                        item.context = publisher.sgtk.context_from_entity(shot["type"], shot["id"])

    def create_render_items(self, parent_item, asset_info):
        video_info = asset_info.copy()
        video_info["path"] = video_info["resolvedPath"]
        video = self.create_video_items(parent_item, asset_info, is_batch_render=True)

        batch, openclip = [None], [None]
        if "setupResolvedPath" in asset_info:
            batch_info = asset_info.copy()
            batch_info["path"] = batch_info["setupResolvedPath"]
            batch = self.create_batch_items(parent_item, batch_info)

        if "openClipResolvedPath" in asset_info:
            openclip_info = asset_info.copy()
            openclip_info["path"] = openclip_info["openClipResolvedPath"]
            openclip = self.create_batchOpenClip_items(parent_item, openclip_info)

        return [item for item in video + batch + openclip if item is not None]

    def create_batch_items(self, parent_item, asset_info):
        type = "Flame Batch File"
        path = self._path_from_asset(asset_info)
        icon = os.path.join(self.disk_location, "icons", "SG_Batch.png")

        name = asset_info.get("shotName", self.parent.util.get_publish_name(path))

        item = parent_item.create_item("flame.batch", type, name)
        item.set_icon_from_path(icon)
        item.thumbnail_enabled = False

        item.properties["path"] = path
        item.properties["name"] = name
        item.properties["type"] = type

        return [item]

    def create_batchOpenClip_items(self, parent_item, asset_info):
        type = "Flame Batch OpenClip"
        path = self._path_from_asset(asset_info)
        icon = os.path.join(self.disk_location, "icons", "flame.png")

        name = self.parent.util.get_publish_name(path)

        item = parent_item.create_item("flame.batchOpenClip", type, name)
        item.set_icon_from_path(icon)
        item.thumbnail_enabled = False

        item.properties["path"] = path
        item.properties["name"] = name
        item.properties["type"] = type

        return [item]

    def create_openClip_items(self, parent_item, asset_info):
        type = "Flame OpenClip"
        path = self._path_from_asset(asset_info)
        icon = os.path.join(self.disk_location, "icons", "flame.png")

        name = self.parent.util.get_publish_name(path)

        item = parent_item.create_item("flame.openClip", type, name)
        item.set_icon_from_path(icon)
        item.thumbnail_enabled = False

        item.properties["path"] = path
        item.properties["name"] = name
        item.properties["type"] = type

        return [item]

    def create_video_items(self, parent_item, asset_info, is_batch_render=False):
        type = "Flame Render"
        path = self._path_from_asset(asset_info)
        sequence = self._get_file_sequence(path)
        icon = os.path.join(self.disk_location, "icons", "image_sequence.png")

        # get the publish name for this file path.
        is_sequence = len(sequence) != 0

        if is_sequence:
            # generate the name from one of the actual files in the sequence
            name_path = sequence[0]
        else:
            name_path = path

        # get the publish name for this file path. this will ensure we get a
        # consistent name across version publishes of this file.
        name = self.parent.util.get_publish_name(
            name_path, sequence=is_sequence)

        item = parent_item.create_item("flame.video", type, name)
        item.set_icon_from_path(icon)
        item.thumbnail_enabled = False

        if sequence:
            item.properties["is_sequence"] = True
            item.properties["sequence_files"] = sequence

        item.properties["path"] = path
        item.properties["name"] = name
        item.properties["type"] = type

        return [item]

    def create_audio_items(self, parent_item, asset_info):
        type = "Flame Audio"
        path = self._path_from_asset(asset_info)
        icon = os.path.join(self.disk_location, "icons", "audio.png")

        name = self.parent.util.get_publish_name(path)

        item = parent_item.create_item("flame.audio", type, name)
        item.set_icon_from_path(icon)
        item.thumbnail_enabled = False

        item.properties["path"] = path
        item.properties["name"] = name
        item.properties["type"] = type

        return [item]

    def create_sequence_items(self, parent_item, asset_info):
        type = "Flame Sequence"
        path = self._path_from_asset(asset_info)
        icon = os.path.join(self.disk_location, "icons", "flame.png")

        name = self.parent.util.get_publish_name(path)

        item = parent_item.create_item("flame.sequence", type, name)
        item.set_icon_from_path(icon)
        item.thumbnail_enabled = False

        item.properties["path"] = path
        item.properties["name"] = name
        item.properties["type"] = type

        return [item]

    def _path_from_asset(self, asset_info):
        if "path" in asset_info:
            path = asset_info["path"]
        else:
            path = os.path.join(asset_info.get("destinationPath", ""), asset_info["resolvedPath"])

        return path

    def process_file(self, parent_item, path):
        """
        Analyzes the given file and creates one or more items
        to represent it.

        :param parent_item: Root item instance
        :param path: Path to analyze
        :returns: The main item that was created, or None if no item was created
            for the supplied path
        """

        # handle files and folders differently
        if os.path.isdir(path):
            self._collect_folder(parent_item, path)
            return None
        else:
            return self._collect_file(parent_item, path)

    def _collect_file(self, parent_item, path, frame_sequence=False):
        """
        Process the supplied file path.

        :param parent_item: parent item instance
        :param path: Path to analyze
        :param frame_sequence: Treat the path as a part of a sequence
        :returns: The item that was created
        """

        # make sure the path is normalized. no trailing separator, separators
        # are appropriate for the current os, no double separators, etc.
        path = sgtk.util.ShotgunPath.normalize(path)

        publisher = self.parent

        # get info for the extension
        item_info = self._get_item_info(path)
        item_type = item_info["item_type"]
        type_display = item_info["type_display"]
        evaluated_path = path
        is_sequence = False

        if frame_sequence:
            # replace the frame number with frame spec
            seq_path = publisher.util.get_frame_sequence_path(path)
            if seq_path:
                evaluated_path = seq_path
                type_display = "%s Sequence" % (type_display,)
                item_type = "%s.%s" % (item_type, "sequence")
                is_sequence = True

        display_name = publisher.util.get_publish_name(
            path, sequence=is_sequence)

        # create and populate the item
        file_item = parent_item.create_item(
            item_type, type_display, display_name)

        # if the supplied path is an image, use the path as # the thumbnail.
        if (item_type.startswith("file.image") or
                item_type.startswith("file.texture")):
            file_item.set_thumbnail_from_path(path)

            # disable thumbnail creation since we get it for free
            file_item.thumbnail_enabled = False

        # all we know about the file is its path. set the path in its
        # properties for the plugins to use for processing.
        file_item.properties["path"] = evaluated_path

        if is_sequence:
            # include an indicator that this is an image sequence and the known
            # file that belongs to this sequence
            file_item.properties["is_sequence"] = True
            file_item.properties["sequence_files"] = [path]

        self.logger.info("Collected file: %s" % (evaluated_path,))

        return file_item

    def _collect_folder(self, parent_item, folder):
        """
        Process the supplied folder path.

        :param parent_item: parent item instance
        :param folder: Path to analyze
        :returns: The item that was created
        """

        # make sure the path is normalized. no trailing separator, separators
        # are appropriate for the current os, no double separators, etc.
        folder = sgtk.util.ShotgunPath.normalize(folder)

        publisher = self.parent
        img_sequences = publisher.util.get_frame_sequences(
            folder)

        file_items = []

        for (image_seq_path, img_seq_files) in img_sequences:
            # get info for the extension
            item_info = self._get_item_info(image_seq_path)
            item_type = item_info["item_type"]
            type_display = item_info["type_display"]

            # the supplied image path is part of a sequence. alter the
            # type info to account for this.
            type_display = "%s Sequence" % (type_display,)
            item_type = "%s.%s" % (item_type, "sequence")
            icon_name = "image_sequence.png"

            # get the first frame of the sequence. we'll use this for the
            # thumbnail and to generate the display name
            img_seq_files.sort()
            first_frame_file = img_seq_files[0]
            display_name = publisher.util.get_publish_name(
                first_frame_file, sequence=True)

            # create and populate the item
            file_item = parent_item.create_item(
                item_type,
                type_display,
                display_name
            )

            # use the first frame of the seq as the thumbnail
            file_item.set_thumbnail_from_path(first_frame_file)

            # disable thumbnail creation since we get it for free
            file_item.thumbnail_enabled = False

            # all we know about the file is its path. set the path in its
            # properties for the plugins to use for processing.
            file_item.properties["path"] = image_seq_path
            file_item.properties["is_sequence"] = True
            file_item.properties["sequence_files"] = img_seq_files

            self.logger.info("Collected file: %s" % (image_seq_path,))

            file_items.append(file_item)

        if not file_items:
            self.logger.warn("No image sequences found in: %s" % (folder,))

        return file_items

    def _get_item_info(self, path):
        """
        Return a tuple of display name, item type, and icon path for the given
        filename.

        The method will try to identify the file as a common file type. If not,
        it will use the mimetype category. If the file still cannot be
        identified, it will fallback to a generic file type.

        :param path: The file path to identify type info for

        :return: A dictionary of information about the item to create::

            # path = "/path/to/some/file.0001.exr"

            {
                "item_type": "file.image.sequence",
                "type_display": "Rendered Image Sequence",
                "icon_path": "/path/to/some/icons/folder/image_sequence.png",
                "path": "/path/to/some/file.%04d.exr"
            }

        The item type will be of the form `file.<type>` where type is a specific
        common type or a generic classification of the file.
        """

        publisher = self.parent

        # extract the components of the supplied path
        file_info = publisher.util.get_file_path_components(path)
        extension = file_info["extension"]
        filename = file_info["filename"]

        # default values used if no specific type can be determined
        type_display = "File"
        item_type = "file.unknown"
        icon_name = "file.png"

        # keep track if a common type was identified for the extension
        common_type_found = False

        # look for the extension in the common file type info dict
        for display in COMMON_FILE_INFO:
            type_info = COMMON_FILE_INFO[display]

            if extension in type_info["extensions"]:
                # found the extension in the common types lookup. extract the
                # item type, icon name.
                type_display = display
                item_type = type_info["item_type"]
                icon_name = type_info["icon"]
                common_type_found = True
                break

        if not common_type_found:
            # no common type match. try to use the mimetype category. this will
            # be a value like "image/jpeg" or "video/mp4". we'll extract the
            # portion before the "/" and use that for display.
            (category_type, _) = mimetypes.guess_type(filename)

            if category_type:
                # the category portion of the mimetype
                category = category_type.split("/")[0]

                type_display = "%s File" % (category.title(),)
                item_type = "file.%s" % (category,)
                icon_name = "%s.png" % (category,)

        # everything should be populated. return the dictionary
        return dict(
            item_type=item_type,
            type_display=type_display
        )

    def _get_file_sequence(self, path):
        file_sequence = []

        match = re.match(r"(.*\.)((?:\[\d+-\d+\])|(?:\d+))(\..*)", path)
        if not match:
            # The path is not a sequence
            return file_sequence

        # Get the first and last frame of the sequence
        first, last = match.group(2).replace("[", "").replace("]", "").split("-")

        # Get the frame value padding length
        frame_size = len(first)

        # Check if every frame in the sequence exists
        for frame in range(int(first), int(last)):
            # Apply frame padding
            frame = "0" * (frame_size - len(str(frame))) + str(frame)

            # Build frame file name
            file_name = match.group(1) + frame + match.group(3)
            file_sequence.append(file_name)

        return file_sequence
