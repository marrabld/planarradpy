# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'logReader.ui'
#
# Created: Mon Jun  8 12:27:17 2015
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

class Ui_win_log_reader(object):
    def setupUi(self, win_log_reader):
        win_log_reader.setObjectName(_fromUtf8("win_log_reader"))
        win_log_reader.setWindowModality(QtCore.Qt.WindowModal)
        win_log_reader.resize(1200, 500)
        win_log_reader.setModal(True)
        self.scrollArea = QtGui.QScrollArea(win_log_reader)
        self.scrollArea.setGeometry(QtCore.QRect(10, 10, 1181, 411))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1179, 409))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.textEdit = QtGui.QTextEdit(self.scrollAreaWidgetContents)
        self.textEdit.setGeometry(QtCore.QRect(0, 0, 1181, 411))
        self.textEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.textEdit.setAutoFormatting(QtGui.QTextEdit.AutoAll)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.btn_close = QtGui.QPushButton(win_log_reader)
        self.btn_close.setGeometry(QtCore.QRect(1070, 440, 98, 27))
        self.btn_close.setToolTip(_fromUtf8(""))
        self.btn_close.setObjectName(_fromUtf8("btn_close"))
        self.btn_clearErrorLog = QtGui.QPushButton(win_log_reader)
        self.btn_clearErrorLog.setGeometry(QtCore.QRect(960, 440, 98, 27))
        self.btn_clearErrorLog.setToolTip(_fromUtf8(""))
        self.btn_clearErrorLog.setObjectName(_fromUtf8("btn_clearErrorLog"))

        self.retranslateUi(win_log_reader)
        QtCore.QObject.connect(self.btn_clearErrorLog, QtCore.SIGNAL(_fromUtf8("clicked()")), self.textEdit.clear)
        QtCore.QMetaObject.connectSlotsByName(win_log_reader)

    def retranslateUi(self, win_log_reader):
        win_log_reader.setWindowTitle(_translate("win_log_reader", "Processing Log", None))
        self.btn_close.setText(_translate("win_log_reader", "Close", None))
        self.btn_clearErrorLog.setText(_translate("win_log_reader", "Clear", None))
        self.btn_clearErrorLog.setShortcut(_translate("win_log_reader", "Ctrl+C", None))

