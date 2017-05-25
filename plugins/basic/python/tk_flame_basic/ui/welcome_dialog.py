# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'welcome_dialog.ui'
#
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_WelcomeDialog(object):
    def setupUi(self, WelcomeDialog):
        WelcomeDialog.setObjectName("WelcomeDialog")
        WelcomeDialog.resize(625, 305)
        self.horizontalLayout = QtGui.QHBoxLayout(WelcomeDialog)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.logo_example = QtGui.QLabel(WelcomeDialog)
        self.logo_example.setText("")
        self.logo_example.setPixmap(QtGui.QPixmap(":/tk_flame_basic/sg_logo.png"))
        self.logo_example.setObjectName("logo_example")
        self.horizontalLayout.addWidget(self.logo_example)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtGui.QLabel(WelcomeDialog)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.login = QtGui.QPushButton(WelcomeDialog)
        self.login.setObjectName("login")
        self.verticalLayout.addWidget(self.login)
        self.register_site = QtGui.QPushButton(WelcomeDialog)
        self.register_site.setObjectName("register_site")
        self.verticalLayout.addWidget(self.register_site)
        self.learn_more = QtGui.QPushButton(WelcomeDialog)
        self.learn_more.setObjectName("learn_more")
        self.verticalLayout.addWidget(self.learn_more)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(WelcomeDialog)
        QtCore.QMetaObject.connectSlotsByName(WelcomeDialog)

    def retranslateUi(self, WelcomeDialog):
        WelcomeDialog.setWindowTitle(QtGui.QApplication.translate("WelcomeDialog", "Welcome to Shotgun", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("WelcomeDialog", "<big>Welcome to Shotgun</big>\n"
"\n"
"<p>Shotgun is a review and production tracking toolset that helps you collaborate, communicate and review with other members of your team, directly from Flame. Click Log in to your Shotgun below in order to enable the Shotgun integration in Flame.</p>", None, QtGui.QApplication.UnicodeUTF8))
        self.login.setText(QtGui.QApplication.translate("WelcomeDialog", "Log in to my Shotgun Site", None, QtGui.QApplication.UnicodeUTF8))
        self.register_site.setText(QtGui.QApplication.translate("WelcomeDialog", "Register a new Shotgun Site", None, QtGui.QApplication.UnicodeUTF8))
        self.learn_more.setText(QtGui.QApplication.translate("WelcomeDialog", "Learn more about Shotgun", None, QtGui.QApplication.UnicodeUTF8))

from . import resources_rc
