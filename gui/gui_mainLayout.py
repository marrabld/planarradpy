#!/usr/bin/env python

import PyQt4
from PyQt4 import QtGui
import PyQt4.QtCore
import sys
import os
import multiprocessing
import re
import numpy

from gui_batch import BatchFile
from gui_Layout import *

class FormEvents():
    """
    This class create answers of buttons... of the user interface.
    """


    def __init__(self):

        app = QtGui.QApplication(sys.argv)
        self.main_window = QtGui.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_window)
    
        self.fileDialog = QtGui.QFileDialog()
        self.main_window.setFixedSize(1060,780)
        self.problem = False

        #-----------------------------------------------------#
        #The following permit to list CDOM files in a comboBox.
        #-----------------------------------------------------#
        #directory = os.path.join(os.path.dirname(__file__),'../inputs/iop_files')
        #file_table = os.listdir(directory)
        #files = []
        # = 0
        #for my_file in file_table:
        #    my_file = os.path.splitext(os.path.basename(my_file))[0]
        #    self.cdom_file = self.ui.cdom_file.addItem(my_file)
        #   i += 1

        #---------------------------------------------------------------------------------------------#
        #The following permit to know how many CPU there is in the computer to list them in a comboBox.
        #---------------------------------------------------------------------------------------------#
        cpus = multiprocessing.cpu_count()
        self.nb_cpu = self.ui.nb_cpu.addItem("-1")
        j = 1
        while (j <= cpus):
            self.nb_cpu = self.ui.nb_cpu.addItem(str(j))
            j += 1


        def data():
            """
            This function get back data that the user typed.
            No inputs.
            No return.
            """
            self.p_values = self.ui.p_values.text()
            self.x_value = self.ui.x_value.text()
            #check before of after that run button is pressed?
            #check(self.x_value)
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


        #------------------------------------------------------------------------------#
        #These following functions display a fileDialog to search a file or a directory.
        #------------------------------------------------------------------------------#
        def search_directory_exec_path():
            self.ui.exec_path.setText(self.fileDialog.getExistingDirectory())


        def search_file_phyto():
            self.ui.phyto_path.setText(self.fileDialog.getOpenFileName())


        def search_file_bottom():
            self.ui.bottom_path.setText(self.fileDialog.getOpenFileName())

        #-----------------------------------------------------------------------------#


        def check_values():
            """
            This function check if there is no problem about values given.
            If there is a problem with a or some values, their label's color is changed to red,
            and call a function to display a error message.
            """

            #-------------------------------------------#
            #The following check values containing comas.
            #-------------------------------------------#

            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            #Si rien dans le chemin de repertoire, programme freeze
            #a voir si cela fait pareil pour les fichiers
            #PB avec les chemins !!!! -> FREEZZZZEEEEE
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # un point peut etre present sans rien apres,
            # espace avant ou apres virgule marche pas
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            check_num = '(^([0-9]+[.]?[0-9]*[,]?){1,})|(^([0-9]+[,]){1,})' #regular expression to use
            prog = re.compile(check_num) #analysis object creation
            p_result = prog.search(self.p_values) #string retrieval thanks to the regular expression
            waveL_result = prog.search(self.waveL_values)

            try:
                if (p_result.group() != self.ui.p_values.text()):
                    self.ui.p_label.setStyleSheet('color: red')
                    display_error_message()
                else:
                    self.ui.p_label.setStyleSheet('color: black')
            except AttributeError:
                self.ui.p_label.setStyleSheet('color: red')
                display_error_message()
            try:
                if (waveL_result.group() != self.ui.waveL_values.text()):
                    self.ui.waveL_label.setStyleSheet('color: red')
                    display_error_message()
                else:
                    self.ui.waveL_label.setStyleSheet('color: black')
            except AttributeError:
                self.ui.waveL_label.setStyleSheet('color: red')
                display_error_message()

            #--------------------------------------------------#
            #The following check values containing only numbers.
            #--------------------------------------------------#
            check_num2 = '^([0-9]+[.]?[0-9]*)'
            prog2 = re.compile(check_num2)
            x_result = prog2.search(self.x_value)
            y_result = prog2.search(self.y_value)
            g_result = prog2.search(self.g_value)
            s_result = prog2.search(self.s_value)
            z_result = prog2.search(self.z_value)

            try:
                if (x_result.group() != self.ui.x_value.text()):
                    self.ui.particules_label.setStyleSheet('color: red')
                    self.ui.x_label.setStyleSheet('color: red')
                    display_error_message()
                else:
                    self.ui.particules_label.setStyleSheet('color: black')
                    self.ui.x_label.setStyleSheet('color: black')
            except AttributeError:
                self.ui.particules_label.setStyleSheet('color: red')
                self.ui.x_label.setStyleSheet('color: red')
                display_error_message()
            try:
                if (y_result.group() != self.ui.y_value.text()):
                    self.ui.particules_label.setStyleSheet('color: red')
                    self.ui.y_label.setStyleSheet('color: red')
                    display_error_message()
                else:
                    self.ui.particules_label.setStyleSheet('color: black')
                    self.ui.y_label.setStyleSheet('color: black')
            except AttributeError:
                self.ui.particules_label.setStyleSheet('color: red')
                self.ui.y_label.setStyleSheet('color: red')
                display_error_message()
            try:
                if (g_result.group() != self.ui.g_value.text()):
                    self.ui.organic_label.setStyleSheet('color: red')
                    self.ui.g_label.setStyleSheet('color: red')
                    display_error_message()
                else:
                    self.ui.organic_label.setStyleSheet('color: black')
                    self.ui.g_label.setStyleSheet('color: black')
            except AttributeError:
                self.ui.organic_label.setStyleSheet('color: red')
                self.ui.g_label.setStyleSheet('color: red')
                display_error_message()
            try:
                if (s_result.group() != self.ui.s_value.text()):
                    self.ui.organic_label.setStyleSheet('color: red')
                    self.ui.s_label.setStyleSheet('color: red')
                    display_error_message()
                else:
                    self.ui.organic_label.setStyleSheet('color: black')
                    self.ui.s_label.setStyleSheet('color: black')
            except AttributeError:
                self.ui.organic_label.setStyleSheet('color: red')
                self.ui.s_label.setStyleSheet('color: red')
                display_error_message()
            try:
                if (z_result.group() != self.ui.z_value.text()):
                    self.ui.z_label.setStyleSheet('color: red')
                    display_error_message()
                else:
                    self.ui.z_label.setStyleSheet('color: black')
            except AttributeError:
                self.ui.z_label.setStyleSheet('color: red')
                display_error_message()

            check_num3 = '[1-6]+'
            prog3 = re.compile(check_num3)
            verbose_result = prog2.search(self.verbose_value)

            try:
                if (verbose_result.group() != self.ui.verbose_value.text()):
                    self.ui.verbose_label.setStyleSheet('color: red')
                    display_error_message()
                else:
                    self.ui.verbose_label.setStyleSheet('color: black')
            except AttributeError:
                self.ui.verbose_label.setStyleSheet('color: red')
                display_error_message()

            #--------------------------------------------------#
            #The following check values containing only numbers.
            #--------------------------------------------------#
            check_num4 = '[/]?([A-Za-z]+[/]?)+[A-Za-z]$'
            prog4 = re.compile(check_num4)
            phyto_path_result = prog4.search(self.phyto_path)
            bottom_path_result = prog4.search(self.bottom_path)
            exec_path_result = prog4.search(self.exec_path)

            try:
                if (phyto_path_result.group() != self.ui.phyto_path.text()):
                    self.ui.phyto_label.setStyleSheet('color: red')
                    display_error_message()
                else:
                    self.ui.phyto_label.setStyleSheet('color: black')
            except AttributeError:
                self.ui.phyto_label.setStyleSheet('color: red')
                display_error_message()
            try:
                if (bottom_path_result.group() != self.ui.bottom_path.text()):
                    self.ui.bottom_label.setStyleSheet('color: red')
                    display_error_message()
                else:
                    self.ui.bottom_label.setStyleSheet('color: black')
            except AttributeError:
                self.ui.bottom_label.setStyleSheet('color: red')
                display_error_message()
            try:
                if (exec_path_result.group() != self.ui.exec_path.text()):
                    self.ui.execPath_label.setStyleSheet('color: red')
                    display_error_message()
                else:
                    self.ui.execPath_label.setStyleSheet('color: black')
            except AttributeError:
                self.ui.execPath_label.setStyleSheet('color: red')
                display_error_message()


        def display_error_message():
            """
            This function display an error message when a wrong value is typed.
            """
            qqq = 1
            #label = QtGui.QLabel("aa")
            #label.move(200, 100)
            #label.setPixmap(QtGui.QPixmap("beCareful.png"))

            self.BUTTON_IMAGE = "./beCareful.png"
            self.ImageButton = QtGui.QLabel()
            self.ImageButton.move(100,100)
            self.ImageButton.setPixmap(QtGui.QPixmap(self.BUTTON_IMAGE))
            self.ui.MainWindow.setCentralWidget (self, self.ImageButton)
            #pixmap = QtGui.QPixmap("beCareful.png")

            #label = QtGui.QLabel()
            #label.setPixmap(pixmap)

            #self.ui.centralwidget.display(label)


        def write_to_file():
            """
            This function call "gui_batch.py" with inputs values to write the batch file.
            No inputs.
            No return.
            """
            bt = BatchFile(self.p_values, self.x_value, self.y_value, self.g_value, self.s_value, self.z_value, self.waveL_values, self.verbose_value, self.phyto_path, self.bottom_path, self.nb_cpu, self.exec_path)
            bt.write_batch_to_file()


        def execute_planarrad():
            """
            This function execute planarrad using the batch file.
            """
            os.chdir("../")
            os.system("./planarrad.py -i /home/boulefi/PycharmProjects/planarradpy/inputs/batch_files/batch.txt")


        def cancel_planarrad():
            """
            This function cancel planarrad.
            """
            raise sys.exit("doesn't work")


        #------------------------------------------#
        #The following connect buttons to an action.
        #------------------------------------------#
        self.ui.phyto_button.connect(self.ui.phyto_button,PyQt4.QtCore.SIGNAL('clicked()'),search_file_phyto)
        self.ui.bottom_button.connect(self.ui.bottom_button,PyQt4.QtCore.SIGNAL('clicked()'),search_file_bottom)
        self.ui.exec_path_button.connect(self.ui.exec_path_button,PyQt4.QtCore.SIGNAL('clicked()'),search_directory_exec_path)
        self.ui.run.connect(self.ui.run,PyQt4.QtCore.SIGNAL('clicked()'),data)
        self.ui.run.connect(self.ui.run,PyQt4.QtCore.SIGNAL('clicked()'),check_values)
        #while (self.problem == False):
        #    print("je suis la")
        self.ui.run.connect(self.ui.run,PyQt4.QtCore.SIGNAL('clicked()'),write_to_file)
        #self.ui.run.connect(self.ui.run,PyQt4.QtCore.SIGNAL('clicked()'),execute_planarrad)
        self.ui.cancel.connect(self.ui.cancel,PyQt4.QtCore.SIGNAL('clicked()'),cancel_planarrad)
        self.ui.quit.connect(self.ui.quit,PyQt4.QtCore.SIGNAL('clicked()'),quit)


        self.main_window.show()
        sys.exit(app.exec_())


if __name__ == "__main__":
    FE = FormEvents()
