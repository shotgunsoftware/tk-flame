# Copyright (c) 2014 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

import sgtk
from sgtk.platform.qt import QtCore, QtGui
from .ui.project_create_dialog import Ui_ProjectCreateDialog

class ProjectCreateDialog(QtGui.QWidget):
    """
    Project setup dialog for flame
    """
    
    def __init__(self, project_name, user_name, workspace_name, storage_name, host_name, project_settings):
        """
        Constructor
        """
        # first, call the base class and let it do its thing.
        QtGui.QWidget.__init__(self)
        
        self._engine = sgtk.platform.current_bundle()
        
        # now load in the UI that was created in the UI designer
        self.ui = Ui_ProjectCreateDialog() 
        self.ui.setupUi(self) 
        
        # with the tk dialogs, we need to hook up our modal 
        # dialog signals in a special way
        self.__exit_code = QtGui.QDialog.Rejected
        self.ui.create_project.clicked.connect(self._on_submit_clicked)
        self.ui.abort.clicked.connect(self._on_abort_clicked)
        
        # set up callbacks for various UI constraints
        self.ui.proxy_width_hint.valueChanged.connect(self._on_proxy_width_hint_change)
        self.ui.proxy_min_frame_size.valueChanged.connect(self._on_proxy_min_frame_size_change)
        self.ui.help_link.linkActivated.connect(self._on_help_url_clicked)
        self.ui.proxy_mode.currentIndexChanged.connect(self._on_proxy_mode_change)
        
        # -------------------------------------------------------------------------
        # populate fixed fields (the first tab)
        self.ui.project_name.setText(project_name)
        self.ui.user_name.setText(user_name)
        if workspace_name:
            self.ui.workspace_name.setText(workspace_name)
        else:
            self.ui.workspace_name.setText("Will use a Flame Default Workspace")
        self.ui.storage_name.setText(storage_name)
        self.ui.host_name.setText(host_name)
        
        # -------------------------------------------------------------------------
        # populate the resolution tab
        self.ui.width.setText(str(project_settings.get("FrameWidth")))
        self.ui.height.setText(str(project_settings.get("FrameHeight")))

        self.__set_combo_value(project_settings, self.ui.depth, "FrameDepth")
        self.__set_combo_value(project_settings, self.ui.field_dominance, "FieldDominance")
        
        aspect_ratio = project_settings.get("AspectRatio")
        
        # aspect ratio: ["4:3", "16:9", "Based on width/height"]
        if aspect_ratio == "1.7778":
            self.ui.aspect_ratio.setCurrentIndex(1)
        elif aspect_ratio == "1.333":
            self.ui.aspect_ratio.setCurrentIndex(0)
        else:
            # use width/height aspect ratio
            self.ui.aspect_ratio.setCurrentIndex(2)
        
        # -------------------------------------------------------------------------
        # populate the proxy tab
        # mode states: [off, conditional, on]
        
        enable_proxy = project_settings.get("ProxyEnable") == "true"
        proxy_min_frame_size = int(project_settings.get("ProxyMinFrameSize"))
        
        # first reset the combo to trigger the change events later
        self.ui.proxy_mode.setCurrentIndex(-1)
        
        if enable_proxy == False and proxy_min_frame_size == 0:
            self.ui.proxy_mode.setCurrentIndex(0) # off
        elif enable_proxy == False and proxy_min_frame_size > 0:
            self.ui.proxy_mode.setCurrentIndex(1) # on 
        else:
            self.ui.proxy_mode.setCurrentIndex(2) # conditionally
           
        self.__set_combo_value(project_settings, self.ui.proxy_depth, "ProxyDepthMode")
        self.__set_combo_value(project_settings, self.ui.proxy_quality, "ProxyQuality")
        
        if project_settings.get("ProxyAbove8bits") == "true":
            self.ui.proxy_above_8_bits.setChecked(True)
        else:
            self.ui.proxy_above_8_bits.setChecked(False)

        pmfs = int(project_settings.get("ProxyMinFrameSize"))
        pwh = int(project_settings.get("ProxyWidthHint"))
        
        self.ui.proxy_width_hint.setValue(pwh)
        self.ui.proxy_min_frame_size.setValue(pmfs)
        
    def __set_combo_value(self, project_settings, combo_widget, setting):
        """
        Helper method.
        Given a settings value, set up a combo box
        """
        value = project_settings.get(setting)
        if value is None:
            # nothing selected
            combo_widget.setCurrentIndex(-1)
        else:
            idx = combo_widget.findText(str(value))
            combo_widget.setCurrentIndex(idx)
         
    def get_settings(self):
        """
        Returns a settings dictionary, on the following form:
        
         - FrameWidth (e.g. "1280")
         - FrameHeight (e.g. "1080")
         - FrameDepth (16-bit fp, 12-bit, 12-bit u, 10-bit, 8-bit) 
         - FrameRate (23.976, 24, 25, 29.97 df, 29.97 ndf, 30, 50, 50.94 df, 50.94 ndf, 60)
         - FieldDominance (PROGRESSIVE, FIELD_1, FIELD_2)
         - AspectRatio (4:3, 16:9, or floating point value as string)
         
         For proxy settings see http://images.autodesk.com/adsk/files/wiretap2011_sdk_guide.pdf
         - ProxyEnable ("true" or "false")
         - ProxyWidthHint
         - ProxyDepthMode
         - ProxyMinFrameSize
         - ProxyAbove8bits
         - ProxyQuality
        
        """
        settings = {}
        
        settings["FrameWidth"] = self.ui.width.text()
        settings["FrameHeight"] = self.ui.height.text()
        settings["FrameDepth"] = self.ui.depth.currentText()
        settings["FieldDominance"] = self.ui.field_dominance.currentText()
        
        # aspect ratio: ["4:3", "16:9", "Based on width/height"]
        
        if self.ui.aspect_ratio.currentIndex() == 0:
            settings["AspectRatio"] = "1.33333"
        elif self.ui.aspect_ratio.currentIndex() == 1:
            settings["AspectRatio"] = "1.777778"
        else:
            settings["AspectRatio"] = "%4f" % (float(settings["FrameWidth"]) / float(settings["FrameHeight"]))
        
        
        # populate the proxy tab
        # mode states: [off, conditional, on]
        if self.ui.proxy_mode.currentIndex() == 0:
            settings["ProxyEnable"] = "false"
            settings["ProxyWidthHint"] = "0"
            
        elif self.ui.proxy_mode.currentIndex() == 1:
            settings["ProxyEnable"] = "false"
            settings["ProxyWidthHint"] = "%s" % self.ui.proxy_width_hint.value()
            settings["ProxyDepthMode"] = self.ui.proxy_depth.currentText()
            settings["ProxyMinFrameSize"] = "%s" % self.ui.proxy_min_frame_size.value()
            settings["ProxyAbove8bits"] = "true" if self.ui.proxy_above_8_bits.isChecked() else "false"
            settings["ProxyQuality"] = self.ui.proxy_quality.currentText()
        
        else:
            settings["ProxyEnable"] = "true"
            settings["ProxyWidthHint"] = "%s" % self.ui.proxy_width_hint.value()
            settings["ProxyDepthMode"] = self.ui.proxy_depth.currentText()
            settings["ProxyMinFrameSize"] = "%s" % self.ui.proxy_min_frame_size.value()
            settings["ProxyAbove8bits"] = "true" if self.ui.proxy_above_8_bits.isChecked() else "false"
            settings["ProxyQuality"] = self.ui.proxy_quality.currentText()
            
        return settings
        
    @property
    def exit_code(self):
        """
        Used to pass exit code back though sgtk dialog
        
        :returns:    The dialog exit code
        """
        return self.__exit_code
                
    @property
    def hide_tk_title_bar(self):
        """
        Tell the system to not show the std toolbar
        """
        return True
                
    def _on_submit_clicked(self):
        """
        Called when the 'submit' button is clicked.
        """
        self.__exit_code = QtGui.QDialog.Accepted
        self.close()
        
    def _on_abort_clicked(self):
        """
        Called when the 'cancel' button is clicked.
        """
        self.__exit_code = QtGui.QDialog.Rejected
        self.close()

    def _on_help_url_clicked(self):
        """
        Called when someone clicks the help url
        """
        url = self._engine.documentation_url
        if url:
            self._engine.log_debug("Opening documentation url %s..." % url)
            QtGui.QDesktopServices.openUrl(QtCore.QUrl(url))
        else:
            self._engine.log_warning("No documentation found!")

    def _on_proxy_width_hint_change(self):
        """
        Update slider preview for proxy width hint
        """
        val = self.ui.proxy_width_hint.value()
        self.ui.proxy_width_hint_preview.setText("%s px" % val)
        # min frame size value must be greater or equal to this value
        self.ui.proxy_min_frame_size.setMinimum(val)
        
    def _on_proxy_min_frame_size_change(self):
        """
        Update slider preview for proxy min size
        """
        val = self.ui.proxy_min_frame_size.value()
        self.ui.proxy_min_frame_size_preview.setText("%d px" % val)
        
    def _on_proxy_mode_change(self, idx):
        """
        Proxy enabled clicked. Enable/disable a bunch 
        of fields based on the value.
        """
        # [off, conditional, on]
        
        # first turn off everything
        self.ui.proxy_depth.setVisible(False)
        self.ui.proxy_quality.setVisible(False)
        self.ui.proxy_width_hint.setVisible(False)
        self.ui.proxy_width_hint_preview.setVisible(False)
        self.ui.proxy_depth_label.setVisible(False)
        self.ui.proxy_quality_label.setVisible(False)
        self.ui.proxy_width_hint_label.setVisible(False)
        
        self.ui.proxy_min_frame_size.setVisible(False)
        self.ui.proxy_min_frame_size_preview.setVisible(False)
        self.ui.proxy_above_8_bits.setVisible(False)
        self.ui.proxy_min_frame_size_label.setVisible(False)
        
        if idx > 0:
            # on / conditional
            self.ui.proxy_depth.setVisible(True)
            self.ui.proxy_quality.setVisible(True)
            self.ui.proxy_width_hint.setVisible(True)
            self.ui.proxy_width_hint_preview.setVisible(True)
            self.ui.proxy_depth_label.setVisible(True)
            self.ui.proxy_quality_label.setVisible(True)
            self.ui.proxy_width_hint_label.setVisible(True)
            
        
        if idx == 1:
            # conditional
            self.ui.proxy_min_frame_size.setVisible(True)
            self.ui.proxy_min_frame_size_preview.setVisible(True)
            self.ui.proxy_above_8_bits.setVisible(True)
            self.ui.proxy_min_frame_size_label.setVisible(True)
        
