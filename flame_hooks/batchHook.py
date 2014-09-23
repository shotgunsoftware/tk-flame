# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.



# Hook called when a batch setup is loaded
#
# setupName: file path the setup being loaded
def batchSetupLoaded( setupPath ):
   pass



# Hook called when a batch setup is saved
# 
# setupName: file path of the setup being saved 
def batchSetupSaved( setupPath ):
    pass



# Hook called before an export begins. The export will be blocked
# until this function returns.  Note that for stereo export this
# function will be called twice (for left then right channel)
#
# info [Dictionary] [Modifiable]
#    Information about the export,
#
#    Keys:
#
#    nodeName:   [String]
#       Name of the export node.
#
#    exportPath: [String] [Modifiable]
#       Export path as entered in the application UI.
#       Can be modified by the hook to change the where file are written.
#
#    namePattern: [String]
#       List of optional naming tokens as entered in the application UI.
#
#    resolvedPath: [String]
#       Full path to the first frame that will be exported with all
#       the tokens resolved.
#
#    firstFrame: [Integer]
#       Frame number of the first frame that will be exported.
#
#    lastFrame: [Integer]
#       Frame number of the last frame that will be exported.
#
#    versionNumber: [Integer]
#       Current version number of export (0 if unversioned).
#
#    openClipNamePattern: [String]
#       List of optional naming tokens pointing to the open clip created if any
#       as entered in the application UI. This is only available if versionning
#       is enabled.
#
#    openClipResolvedPath: [String]
#       Full path to the open clip created if any with all the tokens resolved.
#       This is only available if versionning is enabled.
#
#    setupNamePattern: [String]
#       List of optional naming tokens pointing to the setup created if any
#       as entered in the application UI. This is only available if versionning
#       is enabled.
#
#    setupResolvedPath: [String]
#       Full path to the setup created if any with all the tokens resolved.
#       This is only available if versionning is enabled.
#
# userData [Dictionary] [Modifiable]
#   Empty Dictionary that will be carried over into the batchExportEnd hook.
#   This can be used by the hook to pass black box data around.
#
def batchExportBegin( info, userData ):
   pass




# Hook called when an export ends. Note that for stereo export this
# function will be called twice (for left then right channel)
#
# This function is a compliment to the batchExporBegin function above
#
# info [Dictionary]
#    Information about the export,
#
#    Keys:
#
#    nodeName:   [String]
#       Name of the export node.
#
#    exportPath: [String]
#       Export path as entered in the application UI.
#       Can be modified by the hook to change the where file are written.
#
#    namePattern: [String]
#       List of optional naming tokens as entered in the application UI.
#
#    resolvedPath: [String]
#       Full path to the first frame that will be exported with all
#       the tokens resolved.
#
#    firstFrame: [Integer]
#       Frame number of the first frame that will be exported.
#
#    lastFrame: [Integer]
#       Frame number of the last frame that will be exported.
#
#    versionNumber: [Integer]
#       Current version number of export (0 if unversioned).
#
#    openClipNamePattern: [String]
#       List of optional naming tokens pointing to the open clip created if any
#       as entered in the application UI. This is only available if versionning
#       is enabled.
#
#    openClipResolvedPath: [String]
#       Full path to the open clip created if any with all the tokens resolved.
#       This is only available if versionning is enabled.
#
#    setupNamePattern: [String]
#       List of optional naming tokens pointing to the setup created if any
#       as entered in the application UI. This is only available if versionning
#       is enabled.
#
#    setupResolvedPath: [String]
#       Full path to the setup created if any with all the tokens resolved.
#       This is only available if versionning is enabled.
#
#    aborted: [Boolean]
#       Full path to the setup created if any with all the tokens resolved.
#       This is only available if versionning is enabled.
#
# userData [Dictionary]
#   Dictionary optionally filled by the batchExportBegin hook.
#   This can be used by the hook to pass black box data around.
#
def batchExportEnd( info, userData ):
   pass








