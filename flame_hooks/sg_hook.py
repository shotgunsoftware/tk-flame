# Copyright (c) 2015 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import os

def getCustomUIActions():
    major_version = os.environ.get("SHOTGUN_FLAME_MAJOR_VERSION")
    if major_version is not None and int(major_version) >= 2018:
        # Bypass getCustomUIActions contextual hook from version 2018.
        # More recent version will use the main menu instead.
        return ()

    return getMainMenuCustomUIActions()

def getMainMenuCustomUIActions( ):
    """
    Hook returning the custom ui actions to display to the user in the contextual menu.

    :returns: a tuple of group dictionaries.

    A group dictionary defines a custom menu group where keys defines the group.

    Keys:
        name: [String] Name of the action group that will be created in the menu.
        actions: [String] Tuple of action dictionary which menu items will be created in the group.

    An action dictionary of userData where the keys defines the action

    Keys:
        name: [String] Name of the action that will be passed on customUIAction callback.
        caption: [String] Caption of the menu item.

    For example: 2 menu groups containing 1 custom action each:

    return (
        {
            "name": "Custom Group 1",
            "actions": (
                {"name": "action1", "caption": "Action Number 1"},
            )
        },
        {
            "name": "Custom Group 2",
            "actions": (
                {"name": "action2", "caption": "Action Number 2"},
            )
        },
    )
    """
    # first, get the toolkit engine
    import sgtk
    engine = sgtk.platform.current_engine()

    # We can't do anything without the Shotgun engine. 
    # The engine is None when the user decides to not use the plugin for the project.
    if engine is None:
        return ()

    
    # build a list of the matching commands
    # returns a list of items, each a tuple with (instance_name, name, callback)
    context_commands = engine._get_commands_matching_setting("context_menu")

    # Commands are uniquely identified by name so build a list of them
    commands = []
    for (instance_name, command_name, callback) in context_commands:
        commands.append(command_name)

    # now add any 'normal' registered commands not already in the actions dict
    # omit system actions that are on the context menu
    for command_name in engine.commands:
        properties = engine.commands[command_name]["properties"]
        if command_name not in commands and properties.get("type") != "context_menu":
            commands.append(command_name)

    # do not add the menu if there are no matches
    if not commands:
        return ()

    # generate flame data structure
    actions = [{"name": x, "caption": x} for x in commands]

    return (
        {
            "name": "Shotgun",
            "actions": tuple(actions)
        },
    )


def customUIAction(info, userData):
    """
    Hook called when a custom action is triggered in the menu

    :param info: A dictionary containing information about the custom action with the keys
                 - name: Name of the action being triggered
                 - selection: Tuple of wiretap ids

    :param userData: The action dictionary that was passed to getCustomUIActions
    """
    # first, get the toolkit engine
    import sgtk
    engine = sgtk.platform.current_engine()

    # We can't do anything without the Shotgun engine. 
    # The engine is None when the user decides to not use the plugin for the project.
    if engine is None:
        return

    # get the comand name
    command_name = info["name"]
    # find it in toolkit
    command_obj = engine.commands[command_name]
    # execute the callback
    command_obj["callback"]()
