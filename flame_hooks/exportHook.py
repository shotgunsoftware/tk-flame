# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.








# Hook called before a custom export begins. The export will be blocked
# until this function returns. This can be used to fill information that would
# have normally been extracted from the export window.
#
# info [Dictionary] [Modifiable]
#    Information about the export,
#
#    Keys:
#
#    destinationHost: [String] [Modifiable]
#       Host name where the exported files will be written to.
#       Defaults to localhost.
#
#    destinationPath: [String] [Modifiable]
#       Export path root.
#       Defaults to /tmp
#
#    presetPath: [String] [Modifiable]
#       Path to the preset used for the export.
#       Must be defined by this method.
#
# userData [Dictionary] [Modifiable]
#   Dictionary that could have been populated by previous export hooks and that
#   will be carried over into the subsequent export hooks.
#   This can be used by the hook to pass black box data around.
 
def preCustomExport( info, userData ):
   pass
 
 
# Hook called after a custom export ends. The export will be blocked
# until this function returns.
#
# info [Dictionary] [Modifiable]
#    Information about the export,
#
#    Keys:
#
#    destinationHost: [String]
#       Host name where the exported files were written to.
#
#    destinationPath: [String]
#       Export path root.
#
#    presetPath: [String]
#       Path to the preset used for the export.
#
# userData [Dictionary] [Modifiable]
#   Dictionary that could have been populated by previous export hooks and that
#   will be carried over into the subsequent export hooks.
#   This can be used by the hook to pass black box data around.
 
def postCustomExport( info, userData ):
   pass


# Hook called before an export begins. The export will be blocked
# until this function returns.
#
# info [Dictionary] [Modifiable]
#    Information about the export,
#
#    Keys:
#
#    destinationHost: [String]
#       Host name where the exported files will be written to.
#
#    destinationPath: [String]
#       Export path root.
#
# userData [Dictionary] [Modifiable]
#   Dictionary that could have been populated by previous export hooks and that
#   will be carried over into the subsequent export hooks.
#   This can be used by the hook to pass black box data around.
def postExport( info, userData ):
   pass
 
 

# Hook called after an export ends. The export will be blocked
# until this function returns.
#
# info [Dictionary] [Modifiable]
#    Information about the export,
#
#    Keys:
#
#    destinationHost: [String]
#       Host name where the exported files were written to.
#
#    destinationPath: [String]
#       Export path root.
#
# userData [Dictionary] [Modifiable]
#   Dictionary that could have been populated by previous export hooks.
#   This can be used by the hook to pass black box data around.
 
def postExport( info, userData ):
   pass


# Hook called before a sequence export begins. The export will be blocked
# until this function returns.
#
# info [Dictionary] [Modifiable]
#    Information about the export,
#
#    Keys:
#
#    destinationHost: [String]
#       Host name where the exported files will be written to.
#
#    destinationPath: [String]
#       Export path root.
#
#    sequenceName: [String]
#       Name of the exported sequence.
#
#    shotNames: [String]
#       Tuple of all shot names in the exported sequence. Multiple segments
#       could have the same shot name.
#
# userData [Dictionary] [Modifiable]
#   Dictionary that could have been populated by previous export hooks and that
#   will be carried over into the subsequent export hooks.
#   This can be used by the hook to pass black box data around.
 
def preExportSequence( info, userData ):
   pass


# Hook called after a sequence export ends. The export will be blocked
# until this function returns.
#
# info [Dictionary] [Modifiable]
#    Information about the export,
#
#    Keys:
#
#    destinationHost: [String]
#       Host name where the exported files were written to.
#
#    destinationPath: [String]
#       Export path root.
#
#    sequenceName: [String]
#       Name of the exported sequence.
#
#    shotNames: [String]
#       Tuple of all shot names in the exported sequence. Multiple segment
#       could have the same shot name.
#
# userData [Dictionary] [Modifiable]
#   Dictionary that could have been populated by previous export hooks and that
#   will be carried over into the subsequent export hooks.
#   This can be used by the hook to pass black box data around.
 
def postExportSequence( info, userData ):
   pass
 
 
# Hook called before an asset export begins. The export will be blocked
# until this function returns.
#
# info [Dictionary] [Modifiable]
#    Information about the export,
#
#    Keys:
#
#    destinationHost: [String]
#       Host name where the exported files will be written to.
#
#    destinationPath: [String]
#       Export path root.
#
#    namePattern: [String]
#       List of optional naming tokens.
#
#    resolvedPath: [String]
#       Full file pattern that will be exported with all the tokens resolved.
#
#    name: [String]
#       Name of the exported asset.
#
#    sequenceName: [String]
#       Name of the sequence the asset is part of.
#
#    shotName: [String]
#       Name of the shot the asset is part of.
#
#    assetType: [String]
#       Type of exported asset.
#       ( 'video', 'audio', 'batch', 'openClip', 'batchOpenClip' )
#
#    width: [Long]
#       Frame width of the exported asset.
#
#    height: [Long]
#       Frame height of the exported asset.
#
#    aspectRatio: [Double]
#       Frame aspect ratio of the exported asset.
#
#    depth: [String]
#       Frame depth of the exported asset.
#       ( '8-bits', '10-bits', '12-bits', '16 fp' )
#
#    scanFormat: [String]
#       Scan format of the exported asset.
#       ( 'FILED_1', 'FIELD_2', 'PROGRESSIVE' )
#
#    fps: [Double]
#       Frame rate of exported asset.
#
#    versionName: [String]
#       Current version name of export (Empty if unversioned).
#
#    versionNumber: [Integer]
#       Current version number of export (0 if unversioned).
#
# userData [Dictionary] [Modifiable]
#   Dictionary that could have been populated by previous export hooks and that
#   will be carried over into the subsequent export hooks.
#   This can be used by the hook to pass black box data around.
 
def preExportAsset( info, userData ):
   pass
 
# Hook called after an asset export ends. The export will be blocked
# until this function returns.
#
# info [Dictionary] [Modifiable]
#    Information about the export,
#
#    Keys:
#
#    destinationHost: [String]
#       Host name where the exported files were written to.
#
#    destinationPath: [String]
#       Export path root.
#
#    namePattern: [String]
#       List of optional naming tokens.
#
#    resolvedPath: [String]
#       Full file pattern that will be exported with all the tokens resolved.
#
#    name: [String]
#       Name of the exported asset.
#
#    sequenceName: [String]
#       Name of the sequence the asset is part of.
#
#    shotName: [String]
#       Name of the shot the asset is part of.
#
#    assetType: [String]
#       Type of exported asset.
#       ( 'video', 'audio', 'batch', 'openClip', 'batchOpenClip' )
#
#    isBackground: [Boolean]
#       True if the export of the asset happened in the background.
#
#    backgroundJobId: [String]
#       Id of the background job given by the backburner manager upon
#       submission. Empty if job is done in foreground.
#
#    width: [Long]
#       Frame width of the exported asset.
#
#    height: [Long]
#       Frame height of the exported asset.
#
#    aspectRatio: [Double]
#       Frame aspect ratio of the exported asset.
#
#    depth: [String]
#       Frame depth of the exported asset.
#       ( '8-bits', '10-bits', '12-bits', '16 fp' )
#
#    scanFormat: [String]
#       Scan format of the exported asset.
#       ( 'FILED_1', 'FIELD_2', 'PROGRESSIVE' )
#
#    fps: [Double]
#       Frame rate of exported asset.
#
#    versionName: [String]
#       Current version name of export (Empty if unversioned).
#
#    versionNumber: [Integer]
#       Current version number of export (0 if unversioned).
#
# userData [Dictionary] [Modifiable]
#   Dictionary that could have been populated by previous export hooks and that
#   will be carried over into the subsequent export hooks.
#   This can be used by the hook to pass black box data around.
 
def postExportAsset( info, userData ):
   pass
   
 
 
 
 
# Indicates whether postExportAsset should be called from a backburner job or
# directly from the application.
#
# Warning: Not generating a postExportAsset backburner job for exports that are
# using backburner could result in postExportAsset being called before the
# export job is complete.
 
def useBackburnerPostExportAsset():
   return True
 
 

 
# Hook returning the custom export profiles to display to the user in the
# contextual menu.
#
# profiles [Dictionary] [Modifiable]
#
#    A dictionary of userData dictionaries where the keys are the name
#    of the profiles to show in contextual menus.
 
def getCustomExportProfiles( profiles ):
   pass






