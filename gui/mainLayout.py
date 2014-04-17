#!/usr/bin/env python

import PyQt4
from PyQt4 import QtGui
import PyQt4.QtCore
import sys
import os
import multiprocessing

from library import *
from batch import batch_file
from Layout import *

class FormEvents():
    def __init__(self):

        app = QtGui.QApplication(sys.argv)
        self.main_window = QtGui.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_window)
    
        self.fileDialog = QtGui.QFileDialog()
        self.main_window.setFixedSize(910,780)

        def datas():
            self.p_values = self.ui.p_values.text()
            self.x_value = self.ui.x_value.text()
            self.y_value = self.ui.y_value.text()
            self.g_value = self.ui.g_value.text()
            self.s_value = self.ui.s_value.text()
            self.z_value = self.ui.z_value.text()
            self.waveL_values = self.ui.waveL_values.text()
            self.verbose_value = self.ui.verbose_value.text()
            self.phyto_path = self.ui.phyto_path.text()
            self.bottom_path = self.ui.bottom_path.text()
            self.exec_path = self.ui.exec_path.text()
            #self.cdom_file = self.ui.cdom_file.currentText()
            self.nb_cpu = self.ui.nb_cpu.currentText()

        directory = os.path.join(os.path.dirname(__file__),'../inputs/iop_files')
        file_table = os.listdir(directory)
        files = []
        i = 0
        for my_file in file_table:
            my_file = os.path.splitext(os.path.basename(my_file))[0]
            self.cdom_file = self.ui.cdom_file.addItem(my_file)
            i += 1

        cpus = multiprocessing.cpu_count()
        self.nb_cpu = self.ui.nb_cpu.addItem("-1")
        j = 1
        while (j <= cpus):
            self.nb_cpu = self.ui.nb_cpu.addItem(str(j))
            j += 1

        def search_directory_exec_path():
            self.ui.exec_path.setText(self.fileDialog.getExistingDirectory())
        def search_file_phyto():
            self.ui.phyto_path.setText(self.fileDialog.getOpenFileName())
        def search_file_bottom():
            self.ui.bottom_path.setText(self.fileDialog.getOpenFileName())
        def write_to_file():
            bt = batch_file(self.p_values, self.x_value, self.y_value, self.g_value, self.s_value, self.z_value, self.waveL_values, self.verbose_value, self.phyto_path, self.bottom_path, self.nb_cpu, self.exec_path)
            bt.write_batch_to_file(self.p_values, self.x_value, self.y_value, self.g_value, self.s_value, self.z_value, self.waveL_values, self.verbose_value, self.phyto_path, self.bottom_path, self.nb_cpu, self.exec_path)
        def execute_software():
            exec("../scripts/test.py")




        self.ui.phyto_button.connect(self.ui.phyto_button,PyQt4.QtCore.SIGNAL('clicked()'),search_file_phyto)
        self.ui.bottom_button.connect(self.ui.bottom_button,PyQt4.QtCore.SIGNAL('clicked()'),search_file_bottom)
        self.ui.exec_path_button.connect(self.ui.exec_path_button,PyQt4.QtCore.SIGNAL('clicked()'),search_directory_exec_path)
        self.ui.run.connect(self.ui.run,PyQt4.QtCore.SIGNAL('clicked()'),datas)
        self.ui.run.connect(self.ui.run,PyQt4.QtCore.SIGNAL('clicked()'),write_to_file)
        self.ui.run.connect(self.ui.run,PyQt4.QtCore.SIGNAL('clicked()'),execute_software)
        self.ui.quit.connect(self.ui.quit,PyQt4.QtCore.SIGNAL('clicked()'),quit)

        self.main_window.show()
        sys.exit(app.exec_())


if __name__ == "__main__":
    FE = FormEvents()
