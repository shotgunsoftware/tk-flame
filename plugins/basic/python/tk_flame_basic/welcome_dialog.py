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
from PySide import QtCore, QtGui
from .ui.welcome_dialog import Ui_WelcomeDialog


class WelcomeDialog(QtGui.QDialog):
    """
    Main application dialog window
    """

    (LOGIN, LEARN_MORE, NEW_SITE) = range(3)

    def __init__(self):
        """
        Constructor
        """
        # first, call the base class and let it do its thing.
        QtGui.QDialog.__init__(self)
        
        # now load in the UI that was created in the UI designer
        self.ui = Ui_WelcomeDialog()
        self.ui.setupUi(self)

        self.ui.learn_more.clicked.connect(self._on_learn_more_clicked)
        self.ui.login.clicked.connect(self._on_login_clicked)
        self.ui.register_site.clicked.connect(self._on_register_clicked)

    def _on_learn_more_clicked(self):
        self.done(self.LEARN_MORE)

    def _on_login_clicked(self):
        self.done(self.LOGIN)

    def _on_register_clicked(self):
        self.done(self.NEW_SITE)

