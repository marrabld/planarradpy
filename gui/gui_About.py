# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'aboutGui.ui'
#
# Created: Mon Jun  8 12:27:16 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_win_about(object):
    def setupUi(self, win_about):
        win_about.setObjectName(_fromUtf8("win_about"))
        win_about.resize(589, 474)
        self.buttonBox = QtGui.QDialogButtonBox(win_about)
        self.buttonBox.setGeometry(QtCore.QRect(230, 430, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.label = QtGui.QLabel(win_about)
        self.label.setGeometry(QtCore.QRect(250, 20, 101, 91))
        self.label.setPixmap(QtGui.QPixmap(_fromUtf8("../../../../../../../opt/extras.ubuntu.com/pymi/icons/pymi.png")))
        self.label.setScaledContents(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(win_about)
        self.label_2.setGeometry(QtCore.QRect(200, 130, 171, 41))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(win_about)
        self.label_3.setGeometry(QtCore.QRect(20, 190, 551, 231))
        self.label_3.setMaximumSize(QtCore.QSize(551, 16777215))
        self.label_3.setScaledContents(True)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName(_fromUtf8("label_3"))

        self.retranslateUi(win_about)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), win_about.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), win_about.reject)
        QtCore.QMetaObject.connectSlotsByName(win_about)

    def retranslateUi(self, win_about):
        win_about.setWindowTitle(_translate("win_about", "About Planarradpy", None))
        self.label_2.setText(_translate("win_about", "<html><head/><body><p><span style=\" font-size:22pt; font-weight:600;\">Planarradpy 0.1</span></p></body></html>", None))
        self.label_3.setText(_translate("win_about", "<html><head/><body><p align=\"justify\"><span style=\" font-family:\'Ubuntu,Ubuntu Beta,UbuntuBeta,Ubuntu,Bitstream Vera Sans,DejaVu Sans,Tahoma,sans-serif\'; font-size:14px; color:#333333; background-color:#ffffff;\">Planarradpy is a wrapper tool desgined for batch processing </span><a href=\"http://www.planarrad.com\"><span style=\" text-decoration: underline; color:#0000ff;\">Planarrad</span></a><span style=\" font-family:\'Ubuntu,Ubuntu Beta,UbuntuBeta,Ubuntu,Bitstream Vera Sans,DejaVu Sans,Tahoma,sans-serif\'; font-size:14px; color:#333333; background-color:#ffffff;\"> based on varying IOPs and visualising the outputs.</span></p><p align=\"justify\"><span style=\" font-family:\'Ubuntu,Ubuntu Beta,UbuntuBeta,Ubuntu,Bitstream Vera Sans,DejaVu Sans,Tahoma,sans-serif\'; font-size:14px; color:#333333; background-color:#ffffff;\">Licence : GNU GPL v 3</span></p><p><span style=\" font-family:\'Ubuntu,Ubuntu Beta,UbuntuBeta,Ubuntu,Bitstream Vera Sans,DejaVu Sans,Tahoma,sans-serif\'; font-size:14px; color:#333333; background-color:#ffffff;\">Authors : </span><a href=\"https://launchpad.net/~marrabld\"><span style=\" text-decoration: underline; color:#0000ff;\">Dan Marrable</span></a></p><p><span style=\" font-family:\'Ubuntu,Ubuntu Beta,UbuntuBeta,Ubuntu,Bitstream Vera Sans,DejaVu Sans,Tahoma,sans-serif\'; font-size:14px; color:#333333; background-color:#ffffff;\">Contributors : Frederic Boule, Anders Knudby </span></p><p><span style=\" font-family:\'Ubuntu,Ubuntu Beta,UbuntuBeta,Ubuntu,Bitstream Vera Sans,DejaVu Sans,Tahoma,sans-serif\'; font-size:14px; color:#333333; background-color:#ffffff;\">Website : </span><a href=\"https://marrabld.github.io/planarradpy/\"><span style=\" text-decoration: underline; color:#0000ff;\">Planarradpy</span></a></p><p><br/></p></body></html>", None))

