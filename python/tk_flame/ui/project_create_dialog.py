# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'project_create_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

try:
    from tank.platform.qt.QtCore import *
except ImportError:
    from PySide2.QtCore import *
try:
    from tank.platform.qt.QtGui import *
except ImportError:
    from PySide2.QtGui import *
try:
    from tank.platform.qt.QtWidgets import *
except ImportError:
    from PySide2.QtWidgets import *

from  . import resources_rc

class Ui_ProjectCreateDialog(object):
    def setupUi(self, ProjectCreateDialog):
        if not ProjectCreateDialog.objectName():
            ProjectCreateDialog.setObjectName("ProjectCreateDialog")
        ProjectCreateDialog.resize(450, 514)
        ProjectCreateDialog.setStyleSheet("/* this is to force the combo box dropdowns to show all items rather than displaying only a few items and a scroll bar */\n"
"QComboBox QListView {\n"
"height: 100px;\n"
"}")
        self.verticalLayout = QVBoxLayout(ProjectCreateDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_9 = QLabel(ProjectCreateDialog)
        self.label_9.setObjectName("label_9")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setPixmap(QPixmap(":/tk-flame/icon.png"))
        self.label_9.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout.addWidget(self.label_9)

        self.tabWidget = QTabWidget(ProjectCreateDialog)
        self.tabWidget.setObjectName("tabWidget")
        self.project_overview_tab = QWidget()
        self.project_overview_tab.setObjectName("project_overview_tab")
        self.formLayout_3 = QFormLayout(self.project_overview_tab)
        self.formLayout_3.setObjectName("formLayout_3")
        self.label_5 = QLabel(self.project_overview_tab)
        self.label_5.setObjectName("label_5")
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.label_5)

        self.project_name = QLabel(self.project_overview_tab)
        self.project_name.setObjectName("project_name")
        sizePolicy1 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.project_name.sizePolicy().hasHeightForWidth())
        self.project_name.setSizePolicy(sizePolicy1)
        self.project_name.setMinimumSize(QSize(200, 0))
        self.project_name.setWordWrap(False)

        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.project_name)

        self.label_7 = QLabel(self.project_overview_tab)
        self.label_7.setObjectName("label_7")
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.label_7)

        self.volume = QComboBox(self.project_overview_tab)
        self.volume.setObjectName("volume")

        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.volume)

        self.label_6 = QLabel(self.project_overview_tab)
        self.label_6.setObjectName("label_6")
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)

        self.formLayout_3.setWidget(3, QFormLayout.LabelRole, self.label_6)

        self.user_name = QLabel(self.project_overview_tab)
        self.user_name.setObjectName("user_name")
        self.user_name.setWordWrap(False)

        self.formLayout_3.setWidget(3, QFormLayout.FieldRole, self.user_name)

        self.label_19 = QLabel(self.project_overview_tab)
        self.label_19.setObjectName("label_19")
        sizePolicy.setHeightForWidth(self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy)

        self.formLayout_3.setWidget(4, QFormLayout.LabelRole, self.label_19)

        self.host_name = QLabel(self.project_overview_tab)
        self.host_name.setObjectName("host_name")
        self.host_name.setWordWrap(False)

        self.formLayout_3.setWidget(4, QFormLayout.FieldRole, self.host_name)

        self.label_4 = QLabel(self.project_overview_tab)
        self.label_4.setObjectName("label_4")

        self.formLayout_3.setWidget(2, QFormLayout.LabelRole, self.label_4)

        self.label_17 = QLabel(self.project_overview_tab)
        self.label_17.setObjectName("label_17")
        sizePolicy.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy)

        self.formLayout_3.setWidget(5, QFormLayout.LabelRole, self.label_17)

        self.workspace_name = QLabel(self.project_overview_tab)
        self.workspace_name.setObjectName("workspace_name")
        self.workspace_name.setWordWrap(False)

        self.formLayout_3.setWidget(5, QFormLayout.FieldRole, self.workspace_name)

        self.group_name_label = QLabel(self.project_overview_tab)
        self.group_name_label.setObjectName("group_name_label")

        self.formLayout_3.setWidget(6, QFormLayout.LabelRole, self.group_name_label)

        self.group_name = QComboBox(self.project_overview_tab)
        self.group_name.setObjectName("group_name")

        self.formLayout_3.setWidget(6, QFormLayout.FieldRole, self.group_name)

        self.setup_dir = QLineEdit(self.project_overview_tab)
        self.setup_dir.setObjectName("setup_dir")

        self.formLayout_3.setWidget(2, QFormLayout.FieldRole, self.setup_dir)

        self.tabWidget.addTab(self.project_overview_tab, "")
        self.resolution_tab = QWidget()
        self.resolution_tab.setObjectName("resolution_tab")
        self.formLayout_2 = QFormLayout(self.resolution_tab)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label = QLabel(self.resolution_tab)
        self.label.setObjectName("label")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.width = QLineEdit(self.resolution_tab)
        self.width.setObjectName("width")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.width.sizePolicy().hasHeightForWidth())
        self.width.setSizePolicy(sizePolicy2)
        self.width.setMinimumSize(QSize(50, 0))
        self.width.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout.addWidget(self.width)

        self.label_2 = QLabel(self.resolution_tab)
        self.label_2.setObjectName("label_2")
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.label_2)

        self.height = QLineEdit(self.resolution_tab)
        self.height.setObjectName("height")
        sizePolicy3 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.height.sizePolicy().hasHeightForWidth())
        self.height.setSizePolicy(sizePolicy3)
        self.height.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout.addWidget(self.height)


        self.formLayout_2.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout)

        self.label_26 = QLabel(self.resolution_tab)
        self.label_26.setObjectName("label_26")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_26)

        self.aspect_ratio = QComboBox(self.resolution_tab)
        self.aspect_ratio.addItem("")
        self.aspect_ratio.addItem("")
        self.aspect_ratio.addItem("")
        self.aspect_ratio.setObjectName("aspect_ratio")
        self.aspect_ratio.setMaxVisibleItems(100)
        self.aspect_ratio.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.aspect_ratio)

        self.label_27 = QLabel(self.resolution_tab)
        self.label_27.setObjectName("label_27")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.label_27)

        self.frame_rate = QComboBox(self.resolution_tab)
        self.frame_rate.addItem("")
        self.frame_rate.addItem("")
        self.frame_rate.addItem("")
        self.frame_rate.addItem("")
        self.frame_rate.addItem("")
        self.frame_rate.addItem("")
        self.frame_rate.addItem("")
        self.frame_rate.addItem("")
        self.frame_rate.addItem("")
        self.frame_rate.addItem("")
        self.frame_rate.setObjectName("frame_rate")
        self.frame_rate.setMaxVisibleItems(100)
        self.frame_rate.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.frame_rate)

        self.label_3 = QLabel(self.resolution_tab)
        self.label_3.setObjectName("label_3")

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.label_3)

        self.depth = QComboBox(self.resolution_tab)
        self.depth.addItem("")
        self.depth.addItem("")
        self.depth.addItem("")
        self.depth.addItem("")
        self.depth.addItem("")
        self.depth.addItem("")
        self.depth.setObjectName("depth")
        self.depth.setMaxVisibleItems(100)

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.depth)

        self.label_10 = QLabel(self.resolution_tab)
        self.label_10.setObjectName("label_10")

        self.formLayout_2.setWidget(4, QFormLayout.LabelRole, self.label_10)

        self.field_dominance = QComboBox(self.resolution_tab)
        self.field_dominance.addItem("")
        self.field_dominance.addItem("")
        self.field_dominance.addItem("")
        self.field_dominance.setObjectName("field_dominance")
        self.field_dominance.setMaxVisibleItems(100)

        self.formLayout_2.setWidget(4, QFormLayout.FieldRole, self.field_dominance)

        self.tabWidget.addTab(self.resolution_tab, "")
        self.old_proxy_tab = QWidget()
        self.old_proxy_tab.setObjectName("old_proxy_tab")
        self.formLayout = QFormLayout(self.old_proxy_tab)
        self.formLayout.setObjectName("formLayout")
        self.formLayout.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)
        self.proxy_depth_label_2 = QLabel(self.old_proxy_tab)
        self.proxy_depth_label_2.setObjectName("proxy_depth_label_2")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.proxy_depth_label_2)

        self.proxy_mode = QComboBox(self.old_proxy_tab)
        self.proxy_mode.addItem("")
        self.proxy_mode.addItem("")
        self.proxy_mode.addItem("")
        self.proxy_mode.setObjectName("proxy_mode")
        self.proxy_mode.setMaxVisibleItems(100)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.proxy_mode)

        self.proxy_depth_label = QLabel(self.old_proxy_tab)
        self.proxy_depth_label.setObjectName("proxy_depth_label")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.proxy_depth_label)

        self.proxy_depth = QComboBox(self.old_proxy_tab)
        self.proxy_depth.addItem("")
        self.proxy_depth.addItem("")
        self.proxy_depth.setObjectName("proxy_depth")
        self.proxy_depth.setMaxVisibleItems(100)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.proxy_depth)

        self.proxy_quality_label = QLabel(self.old_proxy_tab)
        self.proxy_quality_label.setObjectName("proxy_quality_label")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.proxy_quality_label)

        self.proxy_quality = QComboBox(self.old_proxy_tab)
        self.proxy_quality.addItem("")
        self.proxy_quality.addItem("")
        self.proxy_quality.addItem("")
        self.proxy_quality.addItem("")
        self.proxy_quality.addItem("")
        self.proxy_quality.setObjectName("proxy_quality")
        self.proxy_quality.setMaxVisibleItems(100)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.proxy_quality)

        self.proxy_width_hint_label = QLabel(self.old_proxy_tab)
        self.proxy_width_hint_label.setObjectName("proxy_width_hint_label")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.proxy_width_hint_label)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.proxy_width_hint = QSlider(self.old_proxy_tab)
        self.proxy_width_hint.setObjectName("proxy_width_hint")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.proxy_width_hint.sizePolicy().hasHeightForWidth())
        self.proxy_width_hint.setSizePolicy(sizePolicy4)
        self.proxy_width_hint.setMinimumSize(QSize(100, 0))
        self.proxy_width_hint.setMinimum(24)
        self.proxy_width_hint.setMaximum(8192)
        self.proxy_width_hint.setSingleStep(4)
        self.proxy_width_hint.setPageStep(400)
        self.proxy_width_hint.setOrientation(Qt.Horizontal)
        self.proxy_width_hint.setTickPosition(QSlider.TicksBelow)
        self.proxy_width_hint.setTickInterval(400)

        self.horizontalLayout_6.addWidget(self.proxy_width_hint)

        self.proxy_width_hint_preview = QLabel(self.old_proxy_tab)
        self.proxy_width_hint_preview.setObjectName("proxy_width_hint_preview")
        sizePolicy5 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.proxy_width_hint_preview.sizePolicy().hasHeightForWidth())
        self.proxy_width_hint_preview.setSizePolicy(sizePolicy5)

        self.horizontalLayout_6.addWidget(self.proxy_width_hint_preview)


        self.formLayout.setLayout(3, QFormLayout.FieldRole, self.horizontalLayout_6)

        self.proxy_min_frame_size_label = QLabel(self.old_proxy_tab)
        self.proxy_min_frame_size_label.setObjectName("proxy_min_frame_size_label")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.proxy_min_frame_size_label)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.proxy_min_frame_size = QSlider(self.old_proxy_tab)
        self.proxy_min_frame_size.setObjectName("proxy_min_frame_size")
        sizePolicy4.setHeightForWidth(self.proxy_min_frame_size.sizePolicy().hasHeightForWidth())
        self.proxy_min_frame_size.setSizePolicy(sizePolicy4)
        self.proxy_min_frame_size.setMinimumSize(QSize(100, 0))
        self.proxy_min_frame_size.setMinimum(24)
        self.proxy_min_frame_size.setMaximum(8192)
        self.proxy_min_frame_size.setSingleStep(4)
        self.proxy_min_frame_size.setPageStep(400)
        self.proxy_min_frame_size.setOrientation(Qt.Horizontal)
        self.proxy_min_frame_size.setTickPosition(QSlider.TicksBelow)
        self.proxy_min_frame_size.setTickInterval(400)

        self.horizontalLayout_7.addWidget(self.proxy_min_frame_size)

        self.proxy_min_frame_size_preview = QLabel(self.old_proxy_tab)
        self.proxy_min_frame_size_preview.setObjectName("proxy_min_frame_size_preview")
        sizePolicy5.setHeightForWidth(self.proxy_min_frame_size_preview.sizePolicy().hasHeightForWidth())
        self.proxy_min_frame_size_preview.setSizePolicy(sizePolicy5)

        self.horizontalLayout_7.addWidget(self.proxy_min_frame_size_preview)

        self.proxy_above_8_bits = QCheckBox(self.old_proxy_tab)
        self.proxy_above_8_bits.setObjectName("proxy_above_8_bits")

        self.horizontalLayout_7.addWidget(self.proxy_above_8_bits)


        self.formLayout.setLayout(4, QFormLayout.FieldRole, self.horizontalLayout_7)

        self.tabWidget.addTab(self.old_proxy_tab, "")
        self.new_proxy_tab = QWidget()
        self.new_proxy_tab.setObjectName("new_proxy_tab")
        self.formLayout_4 = QFormLayout(self.new_proxy_tab)
        self.formLayout_4.setObjectName("formLayout_4")
        self.proxy_depth_label_3 = QLabel(self.new_proxy_tab)
        self.proxy_depth_label_3.setObjectName("proxy_depth_label_3")

        self.formLayout_4.setWidget(1, QFormLayout.LabelRole, self.proxy_depth_label_3)

        self.new_proxy_mode = QComboBox(self.new_proxy_tab)
        self.new_proxy_mode.addItem("")
        self.new_proxy_mode.addItem("")
        self.new_proxy_mode.addItem("")
        self.new_proxy_mode.setObjectName("new_proxy_mode")
        self.new_proxy_mode.setMaxVisibleItems(100)

        self.formLayout_4.setWidget(1, QFormLayout.FieldRole, self.new_proxy_mode)

        self.proxy_quality_label_2 = QLabel(self.new_proxy_tab)
        self.proxy_quality_label_2.setObjectName("proxy_quality_label_2")

        self.formLayout_4.setWidget(2, QFormLayout.LabelRole, self.proxy_quality_label_2)

        self.new_proxy_quality = QComboBox(self.new_proxy_tab)
        self.new_proxy_quality.addItem("")
        self.new_proxy_quality.addItem("")
        self.new_proxy_quality.addItem("")
        self.new_proxy_quality.addItem("")
        self.new_proxy_quality.addItem("")
        self.new_proxy_quality.addItem("")
        self.new_proxy_quality.addItem("")
        self.new_proxy_quality.addItem("")
        self.new_proxy_quality.addItem("")
        self.new_proxy_quality.setObjectName("new_proxy_quality")
        self.new_proxy_quality.setMaxVisibleItems(100)

        self.formLayout_4.setWidget(2, QFormLayout.FieldRole, self.new_proxy_quality)

        self.proxy_min_frame_size_label_2 = QLabel(self.new_proxy_tab)
        self.proxy_min_frame_size_label_2.setObjectName("proxy_min_frame_size_label_2")

        self.formLayout_4.setWidget(4, QFormLayout.LabelRole, self.proxy_min_frame_size_label_2)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.new_proxy_width = QSpinBox(self.new_proxy_tab)
        self.new_proxy_width.setObjectName("new_proxy_width")
        self.new_proxy_width.setMaximum(65536)
        self.new_proxy_width.setSingleStep(16)

        self.horizontalLayout_8.addWidget(self.new_proxy_width)

        self.new_proxy_width_label = QLabel(self.new_proxy_tab)
        self.new_proxy_width_label.setObjectName("new_proxy_width_label")
        sizePolicy6 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.new_proxy_width_label.sizePolicy().hasHeightForWidth())
        self.new_proxy_width_label.setSizePolicy(sizePolicy6)

        self.horizontalLayout_8.addWidget(self.new_proxy_width_label)


        self.formLayout_4.setLayout(4, QFormLayout.FieldRole, self.horizontalLayout_8)

        self.new_generate_proxies = QCheckBox(self.new_proxy_tab)
        self.new_generate_proxies.setObjectName("new_generate_proxies")

        self.formLayout_4.setWidget(3, QFormLayout.FieldRole, self.new_generate_proxies)

        self.tabWidget.addTab(self.new_proxy_tab, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.help_link = QLabel(ProjectCreateDialog)
        self.help_link.setObjectName("help_link")
        sizePolicy5.setHeightForWidth(self.help_link.sizePolicy().hasHeightForWidth())
        self.help_link.setSizePolicy(sizePolicy5)

        self.horizontalLayout_2.addWidget(self.help_link)

        self.abort = QPushButton(ProjectCreateDialog)
        self.abort.setObjectName("abort")

        self.horizontalLayout_2.addWidget(self.abort)

        self.create_project = QPushButton(ProjectCreateDialog)
        self.create_project.setObjectName("create_project")

        self.horizontalLayout_2.addWidget(self.create_project)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(ProjectCreateDialog)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(ProjectCreateDialog)
    # setupUi

    def retranslateUi(self, ProjectCreateDialog):
        ProjectCreateDialog.setWindowTitle(QCoreApplication.translate("ProjectCreateDialog", "Submit to ShotGrid", None))
        self.label_9.setText("")
        self.label_5.setText(QCoreApplication.translate("ProjectCreateDialog", "<b>Project Name</b>", None))
#if QT_CONFIG(tooltip)
        self.project_name.setToolTip(QCoreApplication.translate("ProjectCreateDialog", "The <b>Flame project name</b> is automatically generated based on your current ShotGrid project. ", None))
#endif // QT_CONFIG(tooltip)
        self.project_name.setText(QCoreApplication.translate("ProjectCreateDialog", "xxx", None))
        self.label_7.setText(QCoreApplication.translate("ProjectCreateDialog", "<b>Storage Volume</b>", None))
        self.label_6.setText(QCoreApplication.translate("ProjectCreateDialog", "<b>User</b>", None))
#if QT_CONFIG(tooltip)
        self.user_name.setToolTip(QCoreApplication.translate("ProjectCreateDialog", "The <b>User Name</b> associated with your new Flame Project is based on the ShotGrid user that matches your current login name.\n"
"", None))
#endif // QT_CONFIG(tooltip)
        self.user_name.setText(QCoreApplication.translate("ProjectCreateDialog", "xxx", None))
        self.label_19.setText(QCoreApplication.translate("ProjectCreateDialog", "<b>Host</b>", None))
        self.host_name.setText(QCoreApplication.translate("ProjectCreateDialog", "xxx", None))
        self.label_4.setText(QCoreApplication.translate("ProjectCreateDialog", "<b>Setup Directory</b>", None))
        self.label_17.setText(QCoreApplication.translate("ProjectCreateDialog", "<b>Workspace</b>", None))
        self.workspace_name.setText(QCoreApplication.translate("ProjectCreateDialog", "xxx", None))
        self.group_name_label.setText(QCoreApplication.translate("ProjectCreateDialog", "<b>Group</b>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.project_overview_tab), QCoreApplication.translate("ProjectCreateDialog", "Project Overview", None))
        self.label.setText(QCoreApplication.translate("ProjectCreateDialog", "Resolution", None))
        self.width.setPlaceholderText(QCoreApplication.translate("ProjectCreateDialog", "width", None))
        self.label_2.setText(QCoreApplication.translate("ProjectCreateDialog", "x", None))
        self.height.setPlaceholderText(QCoreApplication.translate("ProjectCreateDialog", "height", None))
        self.label_26.setText(QCoreApplication.translate("ProjectCreateDialog", "Aspect Ratio", None))
        self.aspect_ratio.setItemText(0, QCoreApplication.translate("ProjectCreateDialog", "4:3", None))
        self.aspect_ratio.setItemText(1, QCoreApplication.translate("ProjectCreateDialog", "16:9", None))
        self.aspect_ratio.setItemText(2, QCoreApplication.translate("ProjectCreateDialog", "Based on width/height", None))

        self.label_27.setText(QCoreApplication.translate("ProjectCreateDialog", "Frame Rate", None))
        self.frame_rate.setItemText(0, QCoreApplication.translate("ProjectCreateDialog", "23.976 fps", None))
        self.frame_rate.setItemText(1, QCoreApplication.translate("ProjectCreateDialog", "24 fps", None))
        self.frame_rate.setItemText(2, QCoreApplication.translate("ProjectCreateDialog", "25 fps", None))
        self.frame_rate.setItemText(3, QCoreApplication.translate("ProjectCreateDialog", "29.97 fps DF", None))
        self.frame_rate.setItemText(4, QCoreApplication.translate("ProjectCreateDialog", "29.97 fps NDF", None))
        self.frame_rate.setItemText(5, QCoreApplication.translate("ProjectCreateDialog", "30 fps", None))
        self.frame_rate.setItemText(6, QCoreApplication.translate("ProjectCreateDialog", "50 fps", None))
        self.frame_rate.setItemText(7, QCoreApplication.translate("ProjectCreateDialog", "59.94 fps DF", None))
        self.frame_rate.setItemText(8, QCoreApplication.translate("ProjectCreateDialog", "59.94 fps NDF", None))
        self.frame_rate.setItemText(9, QCoreApplication.translate("ProjectCreateDialog", "60 fps", None))

        self.label_3.setText(QCoreApplication.translate("ProjectCreateDialog", "Depth", None))
        self.depth.setItemText(0, QCoreApplication.translate("ProjectCreateDialog", "32-bit fp", None))
        self.depth.setItemText(1, QCoreApplication.translate("ProjectCreateDialog", "16-bit fp", None))
        self.depth.setItemText(2, QCoreApplication.translate("ProjectCreateDialog", "12-bit", None))
        self.depth.setItemText(3, QCoreApplication.translate("ProjectCreateDialog", "12-bit ", None))
        self.depth.setItemText(4, QCoreApplication.translate("ProjectCreateDialog", "10-bit", None))
        self.depth.setItemText(5, QCoreApplication.translate("ProjectCreateDialog", "8-bit", None))

        self.label_10.setText(QCoreApplication.translate("ProjectCreateDialog", "Field Dominance", None))
        self.field_dominance.setItemText(0, QCoreApplication.translate("ProjectCreateDialog", "PROGRESSIVE", None))
        self.field_dominance.setItemText(1, QCoreApplication.translate("ProjectCreateDialog", "FIELD_1", None))
        self.field_dominance.setItemText(2, QCoreApplication.translate("ProjectCreateDialog", "FIELD_2", None))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.resolution_tab), QCoreApplication.translate("ProjectCreateDialog", "Resolution", None))
        self.proxy_depth_label_2.setText(QCoreApplication.translate("ProjectCreateDialog", "Mode", None))
        self.proxy_mode.setItemText(0, QCoreApplication.translate("ProjectCreateDialog", "Proxies Off", None))
        self.proxy_mode.setItemText(1, QCoreApplication.translate("ProjectCreateDialog", "Proxies Conditional", None))
        self.proxy_mode.setItemText(2, QCoreApplication.translate("ProjectCreateDialog", "Proxies On", None))

        self.proxy_depth_label.setText(QCoreApplication.translate("ProjectCreateDialog", "Depth", None))
        self.proxy_depth.setItemText(0, QCoreApplication.translate("ProjectCreateDialog", "8-bit", None))
        self.proxy_depth.setItemText(1, QCoreApplication.translate("ProjectCreateDialog", "SAME AS HIRES", None))

        self.proxy_quality_label.setText(QCoreApplication.translate("ProjectCreateDialog", "Quality", None))
        self.proxy_quality.setItemText(0, QCoreApplication.translate("ProjectCreateDialog", "draft", None))
        self.proxy_quality.setItemText(1, QCoreApplication.translate("ProjectCreateDialog", "coarse", None))
        self.proxy_quality.setItemText(2, QCoreApplication.translate("ProjectCreateDialog", "medium", None))
        self.proxy_quality.setItemText(3, QCoreApplication.translate("ProjectCreateDialog", "quality", None))
        self.proxy_quality.setItemText(4, QCoreApplication.translate("ProjectCreateDialog", "bicubic", None))

        self.proxy_width_hint_label.setText(QCoreApplication.translate("ProjectCreateDialog", "Width", None))
        self.proxy_width_hint_preview.setText(QCoreApplication.translate("ProjectCreateDialog", "720px", None))
        self.proxy_min_frame_size_label.setText(QCoreApplication.translate("ProjectCreateDialog", "Width >", None))
        self.proxy_min_frame_size_preview.setText(QCoreApplication.translate("ProjectCreateDialog", "720px", None))
        self.proxy_above_8_bits.setText(QCoreApplication.translate("ProjectCreateDialog", ">8 bits", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.old_proxy_tab), QCoreApplication.translate("ProjectCreateDialog", "Proxy", None))
        self.proxy_depth_label_3.setText(QCoreApplication.translate("ProjectCreateDialog", "Ratio", None))
        self.new_proxy_mode.setItemText(0, QCoreApplication.translate("ProjectCreateDialog", "Proxy 1/2", None))
        self.new_proxy_mode.setItemText(1, QCoreApplication.translate("ProjectCreateDialog", "Proxy 1/4", None))
        self.new_proxy_mode.setItemText(2, QCoreApplication.translate("ProjectCreateDialog", "Proxy 1/8", None))

        self.proxy_quality_label_2.setText(QCoreApplication.translate("ProjectCreateDialog", "Quality", None))
        self.new_proxy_quality.setItemText(0, QCoreApplication.translate("ProjectCreateDialog", "lanczos", None))
        self.new_proxy_quality.setItemText(1, QCoreApplication.translate("ProjectCreateDialog", "shannon", None))
        self.new_proxy_quality.setItemText(2, QCoreApplication.translate("ProjectCreateDialog", "gaussian", None))
        self.new_proxy_quality.setItemText(3, QCoreApplication.translate("ProjectCreateDialog", "quadratic", None))
        self.new_proxy_quality.setItemText(4, QCoreApplication.translate("ProjectCreateDialog", "bicubic", None))
        self.new_proxy_quality.setItemText(5, QCoreApplication.translate("ProjectCreateDialog", "mitchell", None))
        self.new_proxy_quality.setItemText(6, QCoreApplication.translate("ProjectCreateDialog", "triangle", None))
        self.new_proxy_quality.setItemText(7, QCoreApplication.translate("ProjectCreateDialog", "impulse", None))
        self.new_proxy_quality.setItemText(8, QCoreApplication.translate("ProjectCreateDialog", "draft", None))

        self.proxy_min_frame_size_label_2.setText(QCoreApplication.translate("ProjectCreateDialog", "Conditional Width >", None))
        self.new_proxy_width_label.setText(QCoreApplication.translate("ProjectCreateDialog", "px", None))
        self.new_generate_proxies.setText(QCoreApplication.translate("ProjectCreateDialog", "Generate Proxies By Default", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.new_proxy_tab), QCoreApplication.translate("ProjectCreateDialog", "Proxy", None))
        self.help_link.setText(QCoreApplication.translate("ProjectCreateDialog", "<small><a style='color: #30A7E3;' href='{DOC}'>How do I customize Project creation?</a></small>", None))
        self.abort.setText(QCoreApplication.translate("ProjectCreateDialog", "Abort", None))
        self.create_project.setText(QCoreApplication.translate("ProjectCreateDialog", "Create Project", None))
    # retranslateUi

