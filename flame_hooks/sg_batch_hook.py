# Copyright (c) 2014 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

# Note! This file implements the batchHook interface from Flame 2015.2
def batchSetupLoaded(setupPath):
    """
    Hook called when a batch setup is loaded.
    
    :param setupPath: File path of the setup being loaded.
    """
    import sgtk
    engine = sgtk.platform.current_engine()
    
    # We can't do anything without the Shotgun engine. 
    # The engine is None when the user decides to not use the plugin for the project.
    if engine is None:
        return

    engine.trigger_batch_callback("batchSetupLoaded", {"setupPath": setupPath})        

def batchSetupSaved(setupPath):
    """
    Hook called when a batch setup is saved.
    
    :param setupPath: File path of the setup being loaded.
    """
    import sgtk
    engine = sgtk.platform.current_engine()

    # We can't do anything without the Shotgun engine. 
    # The engine is None when the user decides to not use the plugin for the project.
    if engine is None:
        return

    engine.trigger_batch_callback("batchSetupSaved", {"setupPath": setupPath})        

def batchExportBegin(info, userData):
    """    
    Hook called before an export begins. The export will be blocked
    until this function returns.  Note that for stereo export this
    function will be called twice (for left then right channel)

    
    :param info: Dictionary with a number of parameters:
    
        nodeName:             Name of the export node.   
        exportPath:           [Modifiable] Export path as entered in the application UI.
                              Can be modified by the hook to change where the file are written.
        namePattern:          List of optional naming tokens as entered in the application UI.
        resolvedPath:         Full file pattern that will be exported with all the tokens resolved.
        firstFrame:           Frame number of the first frame that will be exported.
        lastFrame:            Frame number of the last frame that will be exported.
        versionName:          Current version name of export (Empty if unversioned).
        versionNumber:        Current version number of export (0 if unversioned).
        openClipNamePattern:  List of optional naming tokens pointing to the open clip created if any
                              as entered in the application UI. This is only available if versioning
                              is enabled.
        openClipResolvedPath: Full path to the open clip created if any with all the tokens resolved.
                              This is only available if versioning is enabled.
        setupNamePattern:     List of optional naming tokens pointing to the setup created if any
                              as entered in the application UI. This is only available if versioning
                              is enabled.
        setupResolvedPath:    Full path to the setup created if any with all the tokens resolved.
                              This is only available if versioning is enabled.
    
    
    :param userData: Dictionary that could have been populated by previous export hooks and that
                     will be carried over into the subsequent export hooks.
                     This can be used by the hook to pass black box data around.
    """
    import sgtk
    engine = sgtk.platform.current_engine()

    # We can't do anything without the Shotgun engine. 
    # The engine is None when the user decides to not use the plugin for the project.
    if engine is None:
        return

    engine.trigger_batch_callback("batchExportBegin", info)        

def batchExportEnd(info, userData):
    """    
    Hook called when an export ends. Note that for stereo export this
    function will be called twice (for left then right channel)
    
    This function complements the above batchExportBegin function.
    
    :param info: Dictionary with a number of parameters:
    
        nodeName:             Name of the export node.   
        exportPath:           Export path as entered in the application UI.
                              Can be modified by the hook to change where the file are written.
        namePattern:          List of optional naming tokens as entered in the application UI.
        resolvedPath:         Full file pattern that will be exported with all the tokens resolved.
        firstFrame:           Frame number of the first frame that will be exported.
        lastFrame:            Frame number of the last frame that will be exported.
        versionName:          Current version name of export (Empty if unversioned).
        versionNumber:        Current version number of export (0 if unversioned).
        openClipNamePattern:  List of optional naming tokens pointing to the open clip created if any
                              as entered in the application UI. This is only available if versioning
                              is enabled.
        openClipResolvedPath: Full path to the open clip created if any with all the tokens resolved.
                              This is only available if versioning is enabled.
        setupNamePattern:     List of optional naming tokens pointing to the setup created if any
                              as entered in the application UI. This is only available if versioning
                              is enabled.
        setupResolvedPath:    Full path to the setup created if any with all the tokens resolved.
                              This is only available if versioning is enabled.
        aborted:              Indicate if the export has been aborted by the user.
    
    
    :param userData: Dictionary that could have been populated by previous export hooks and that
                     will be carried over into the subsequent export hooks.
                     This can be used by the hook to pass black box data around.
    """
    import sgtk
    engine = sgtk.platform.current_engine()

    # We can't do anything without the Shotgun engine. 
    # The engine is None when the user decides to not use the plugin for the project.
    if engine is None:
        return

    engine.trigger_batch_callback("batchExportEnd", info)        
