# Copyright (c) 2015 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

# Note! This file implements the hook interface from Flame 2016.1


def getCustomUIActions():
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

    # go through the values from the run_at_startup setting and run any matching commands
    context_commands = engine.get_setting("context_menu", [])
    if not context_commands:
        return ()

    # build a list of the matching commands
    context_commands = engine._get_commands_matching_setting("context_menu")

    # Build the actions dictionary with the matches
    actions = []
    for (instance_name, command_name, callback) in context_commands:
        actions.append({
            "name": instance_name,
            "caption": command_name,
        })

    # do not add the menu if there are no matches
    if not actions:
        return ()

    return (
        {"name": "Shotgun", "actions": tuple(actions)},
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

    for (command_name, value) in engine.commands.iteritems():
        app_instance = value["properties"].get("app")
        if app_instance is None:
            continue
        instance_name = app_instance.instance_name

        if userData["name"] == instance_name and userData["caption"] == command_name:
            # we have a match, run the callback
            value["callback"]()
            break
