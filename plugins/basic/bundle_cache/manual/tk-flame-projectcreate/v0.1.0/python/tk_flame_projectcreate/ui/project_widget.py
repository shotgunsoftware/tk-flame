# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'project_widget.ui'
#
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from tank.platform.qt import QtCore, QtGui

class Ui_ProjectWidget(object):
    def setupUi(self, ProjectWidget):
        ProjectWidget.setObjectName("ProjectWidget")
        ProjectWidget.resize(154, 175)
        self.verticalLayout_2 = QtGui.QVBoxLayout(ProjectWidget)
        self.verticalLayout_2.setSpacing(1)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.box = QtGui.QFrame(ProjectWidget)
        self.box.setFrameShape(QtGui.QFrame.StyledPanel)
        self.box.setFrameShadow(QtGui.QFrame.Raised)
        self.box.setObjectName("box")
        self.verticalLayout = QtGui.QVBoxLayout(self.box)
        self.verticalLayout.setObjectName("verticalLayout")
        self.thumbnail = QtGui.QLabel(self.box)
        self.thumbnail.setMinimumSize(QtCore.QSize(128, 128))
        self.thumbnail.setMaximumSize(QtCore.QSize(128, 128))
        self.thumbnail.setText("")
        self.thumbnail.setPixmap(QtGui.QPixmap(":/res/loading_512x400.png"))
        self.thumbnail.setScaledContents(True)
        self.thumbnail.setAlignment(QtCore.Qt.AlignCenter)
        self.thumbnail.setObjectName("thumbnail")
        self.verticalLayout.addWidget(self.thumbnail)
        self.label = QtGui.QLabel(self.box)
        self.label.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.verticalLayout_2.addWidget(self.box)

        self.retranslateUi(ProjectWidget)
        QtCore.QMetaObject.connectSlotsByName(ProjectWidget)

    def retranslateUi(self, ProjectWidget):
        ProjectWidget.setWindowTitle(QtGui.QApplication.translate("ProjectWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ProjectWidget", "Project name", None, QtGui.QApplication.UnicodeUTF8))

from . import resources_rc
