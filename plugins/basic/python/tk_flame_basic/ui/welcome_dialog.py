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
        WelcomeDialog.resize(459, 356)
        self.logo_example = QtGui.QLabel(WelcomeDialog)
        self.logo_example.setGeometry(QtCore.QRect(50, 110, 81, 101))
        self.logo_example.setText("")
        self.logo_example.setPixmap(QtGui.QPixmap(":/tk_flame_basic/sg_logo.png"))
        self.logo_example.setObjectName("logo_example")
        self.label = QtGui.QLabel(WelcomeDialog)
        self.label.setGeometry(QtCore.QRect(185, 50, 201, 41))
        self.label.setObjectName("label")
        self.learn_more = QtGui.QPushButton(WelcomeDialog)
        self.learn_more.setGeometry(QtCore.QRect(190, 200, 191, 32))
        self.learn_more.setObjectName("learn_more")
        self.login = QtGui.QPushButton(WelcomeDialog)
        self.login.setGeometry(QtCore.QRect(190, 120, 191, 32))
        self.login.setObjectName("login")
        self.register_site = QtGui.QPushButton(WelcomeDialog)
        self.register_site.setGeometry(QtCore.QRect(190, 160, 191, 32))
        self.register_site.setObjectName("register_site")

        self.retranslateUi(WelcomeDialog)
        QtCore.QMetaObject.connectSlotsByName(WelcomeDialog)

    def retranslateUi(self, WelcomeDialog):
        WelcomeDialog.setWindowTitle(QtGui.QApplication.translate("WelcomeDialog", "Welcome to Shotgun", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("WelcomeDialog", "Welcome to Shotgun bla bla bla", None, QtGui.QApplication.UnicodeUTF8))
        self.learn_more.setText(QtGui.QApplication.translate("WelcomeDialog", "Learn more about Shotgun", None, QtGui.QApplication.UnicodeUTF8))
        self.login.setText(QtGui.QApplication.translate("WelcomeDialog", "Log in to my Shotgun Site", None, QtGui.QApplication.UnicodeUTF8))
        self.register_site.setText(QtGui.QApplication.translate("WelcomeDialog", "Register a new Shotgun Site", None, QtGui.QApplication.UnicodeUTF8))

from . import resources_rc
