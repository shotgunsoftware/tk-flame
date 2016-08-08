# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

import sgtk
import os
import sys
import threading

# by importing QT from sgtk rather than directly, we ensure that
# the code will be compatible with both PySide and PyQt.
from sgtk.platform.qt import QtCore, QtGui
from .ui.dialog import Ui_Dialog

# Import the shotgun_model module from the shotgun utils framework.
shotgun_model = sgtk.platform.import_framework("tk-framework-shotgunutils",
                                               "shotgun_model")
# Set up alias
ShotgunModel = shotgun_model.ShotgunModel

log = sgtk.platform.get_logger(__name__)

from .delegate_project import ProjectDelegate

class AppDialog(QtGui.QWidget):
    """
    Main application dialog window
    """

    def __init__(self):
        """
        Constructor
        """
        # first, call the base class and let it do its thing.
        QtGui.QWidget.__init__(self)
        
        # now load in the UI that was created in the UI designer
        self.ui = Ui_Dialog() 
        self.ui.setupUi(self)
        
        # most of the useful accessors are available through the Application class instance
        # it is often handy to keep a reference to this. You can get it via the following method:
        self._app = sgtk.platform.current_bundle()
        
        # setup our data backend
        self._model = shotgun_model.SimpleShotgunModel(self)

        # tell the view to pull data from the model
        self.ui.page3_view.setModel(self._model)

        # load all assets from Shotgun
        self._model.load_data(
            entity_type="Project",
            fields=["name"],
            filters=[["tank_name", "is", None]]
        )

        # setup a delegate
        self._delegate = ProjectDelegate(self.ui.page3_view)

        # hook up delegate renderer with view
        self.ui.page3_view.setItemDelegate(self._delegate)

        # navigation
        self.ui.page1_existing.clicked.connect(lambda: self.ui.wizard.setCurrentIndex(2))
        self.ui.page1_new.clicked.connect(lambda: self.ui.wizard.setCurrentIndex(1))
        self.ui.page1_noshotgun.clicked.connect(self._no_shotgun)

        self.ui.page2_back.clicked.connect(lambda: self.ui.wizard.setCurrentIndex(0))
        self.ui.page3_back.clicked.connect(lambda: self.ui.wizard.setCurrentIndex(0))

        self.ui.page3_select.clicked.connect(self._on_project_select)
        self.ui.page2_create.clicked.connect(self._on_project_create)

        self.ui.switch_project.clicked.connect(self._switch_site)

        # setup our data backend
        self._template_projects_model = shotgun_model.SimpleShotgunModel(self)
        self.ui.page2_template.setModel(self._template_projects_model)
        self._template_projects_model.load_data(
            entity_type="Project",
            fields=["name"],
            filters=[["is_template", "is", True]]
        )


    @property
    def hide_tk_title_bar(self):
        "Tell the system to not show the standard toolkit toolbar"
        return True

    def is_logout_requested(self):
        """
        Returns true if the user requested to log out
        """
        return False

    def get_project(self):
        """
        Returns the project entity selected by the user
        or None if no project was desired.
        """
        return None


    def _no_shotgun(self):
        """
        User has indicated no shotgun for this project
        """
        log.debug("no shotgun")

    def _on_project_select(self):
        """
        User selects existing project
        """
        log.debug("selected")

    def _on_project_create(self):
        """
        User selects existing project
        """
        log.debug("create")

    def _switch_site(self):
        """
        log out and switch site
        """
        log.debug("switch!")
