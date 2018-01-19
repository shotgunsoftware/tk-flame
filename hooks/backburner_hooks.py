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
Hook that handles logic and automation around automatic Flame project setup
"""
import sgtk
from sgtk import TankError
from functools import partial
from tempfile import mkstemp
import os
import subprocess

HookBaseClass = sgtk.get_hook_baseclass()


class BackburnerHooks(HookBaseClass):
    # constants
    # default height for Shotgun uploads
    # see https://support.shotgunsoftware.com/entries/26303513-Transcoding
    SHOTGUN_QUICKTIME_TARGET_HEIGHT = 720

    # default height for thumbs
    SHOTGUN_THUMBNAIL_TARGET_HEIGHT = 400

    FFMPEG_PRESET = "-threads 2 -vcodec libx264 -me_method umh -directpred 3 -coder ac -me_range 16 -g 250 -rc_eq " \
                    "'blurCplx^(1-qComp)' -keyint_min 25 -sc_threshold 40 -i_qfactor 0.71428572 -b_qfactor 0.76923078 " \
                    "-b_strategy 1 -qcomp 0.6 -qmin 10 -qmax 51 -qdiff 4  -trellis 1 -subq 6 -partitions " \
                    "+parti8x8+parti4x4+partp8x8+partp4x4+partb8x8 -bidir_refine 1 -cmp 1 -flags2 fastpskip -flags2 " \
                    "dct8x8 -flags2 mixed_refs -flags2 wpred -refs 2 -deblockalpha 0 -deblockbeta 0 -bf 3 -crf 18 "

    def attach_jpg_preview(self, path, width, height, targets, name):
        # first figure out a good scale-down res
        scaled_down_width, scaled_down_height = self._calculate_aspect_ratio(
            self.SHOTGUN_THUMBNAIL_TARGET_HEIGHT,
            width,
            height
        )

        input_cmd = "%s -n \"%s@CLIP\" -h %s -W %s -H %s -L" % (
            self.parent.get_read_frame_path(),
            path,
            "%s:Gateway" % self.parent.get_server_hostname(),
            scaled_down_width,
            scaled_down_height
        )

        jpg_fd, jpg_path = mkstemp(suffix=".jpg", prefix=name + ".", dir=self.parent.get_backburner_tmp())
        try:
            full_cmd = "%s > %s" % (input_cmd, jpg_path)

            jpg_job = subprocess.Popen([full_cmd], stdout=subprocess.PIPE, shell=True)
            stdout, stderr = jpg_job.communicate()
            return_code = jpg_job.returncode

            if return_code:
                self.parent.log_warning(
                    "Thumbnail process failed!\nError code: %s\nOutput:\n%s" % (return_code, stderr))
                return return_code

            for target in targets:
                self.parent.shotgun.upload(target["type"], target["id"], jpg_path, "thumb_image", name)

        finally:
            os.close(jpg_fd)
            os.remove(jpg_path)

    def attach_mov_preview(self, path, width, height, targets, name, fps):
        # first figure out a good scale-down res
        scaled_down_width, scaled_down_height = self._calculate_aspect_ratio(
            self.SHOTGUN_QUICKTIME_TARGET_HEIGHT,
            width,
            height
        )

        input_cmd = "%s -n \"%s@CLIP\" -h %s -W %s -H %s -L -N -1 -r" % (
            self.parent.get_read_frame_path(),
            path,
            "%s:Gateway" % self.parent.get_server_hostname(),
            scaled_down_width,
            scaled_down_height
        )

        ffmpeg_cmd = "%s -f rawvideo -top -1 -r %s -pix_fmt rgb24 -s %sx%s -i - -y" % (
            self.parent.get_ffmpeg_path(),
            fps,
            scaled_down_width,
            scaled_down_height
        )

        mov_fd, mov_path = mkstemp(suffix=".mov", prefix=name + ".", dir=self.parent.get_backburner_tmp())

        try:
            full_cmd = "%s | %s %s %s" % (input_cmd, ffmpeg_cmd, self.FFMPEG_PRESET, mov_path)

            mov_job = subprocess.Popen([full_cmd], stdout=subprocess.PIPE, shell=True)
            stdout, stderr = mov_job.communicate()
            return_code = mov_job.returncode

            if return_code:
                self.parent.log_warning("Movie process failed!\nError code: %s\nOutput:\n%s" % (return_code, stderr))
                return return_code

            for target in targets:
                self.parent.shotgun.upload(target["type"], target["id"], mov_path, "sg_uploaded_movie", name)
        finally:
            os.close(mov_fd)
            os.remove(mov_path)

    def _calculate_aspect_ratio(self, target_height, width, height):
        """
            Calculation of aspect ratio.

            Takes the given width and height and produces a scaled width and height given
            the following constraints:

            - the height should be target_height or lower if the original height is lower
            - width and height both need to be divisible by four (ffmpeg requirement)
            - the aspect ratio needs to be as close as possible to the original one

            :param target_height: The desired height
            :param width: The current width
            :param height: The current height
            :returns: int tuple, e.g. (768, 440)
            """

        self.parent.log_debug("Trying to find a scaled down resolution "
                              "with height %s for %sx%s" % (target_height, width, height))

        # If the target_height is bigger than the height, we don't want to enlarge the resolution but we still want to
        # make sure that both width and height is divisible by four
        if target_height > height:
            target_height = height

        # Generate the target resolution keeping the original aspect ratio and the target_height
        aspect_ratio = float(width) / float(height)
        new_height = target_height
        new_width = int(new_height * aspect_ratio)

        # Find the nearest height that's divisible by four
        for i in range(0, 3):
            if ((new_width - i) % 4) == 0:
                return new_width - i, new_height
            elif ((new_width + i) % 4) == 0:
                return new_width + i, new_height

        # Return the original dimension if all the above fail
        return width, height
