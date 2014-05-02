#!/usr/bin/env python

import PyQt4
from PyQt4 import QtGui
import PyQt4.QtCore
import sys
import os
import multiprocessing
import re
import pylab
import scipy
import matplotlib.pyplot as pyplot

from gui_batch import BatchFile
from matplotlibwidgetFile import matplotlibWidget
from gui_Layout import *

class FormEvents():
    """
    This class create answers of buttons of the user interface and checks values that the user typed.
    """

    def __init__(self):

        app = QtGui.QApplication(sys.argv)
        self.main_window = QtGui.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_window)

        self.file_dialog = QtGui.QFileDialog()
        self.main_window.setFixedSize(1400, 825)
        self.widget = matplotlibWidget()
        #self.can_run = True
        self.nb_errors = 0

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
        self.cpu = multiprocessing.cpu_count()
        self.nb_cpu = self.ui.nb_cpu.addItem("-1")
        j = 1
        while j <= self.cpu:
            self.nb_cpu = self.ui.nb_cpu.addItem(str(j))
            j += 1

        def data():
            """
            This function get back data that the user typed.
            """
            self.p_values = self.ui.p_values.text()
            self.x_value = self.ui.x_value.text()
            #check before of after that run button is pressed?
            #check(self.x_value)
            self.y_value = self.ui.y_value.text()
            self.g_value = self.ui.g_value.text()
            self.s_value = self.ui.s_value.text()
            self.z_value = self.ui.z_value.text()
            self.wavelength_values = self.ui.wavelength_values.text()
            self.verbose_value = self.ui.verbose_value.text()
            self.phyto_path = self.ui.phyto_path.text()
            self.bottom_path = self.ui.bottom_path.text()
            self.exec_path = self.ui.exec_path.text()
            #self.cdom_file = self.ui.cdom_file.currentText()
            self.nb_cpu = self.ui.nb_cpu.currentText()

        #------------------------------------------------------------------------------#
        #These following functions display a fileDialog to search a file or a directory.
        #------------------------------------------------------------------------------#
        def search_directory_exec_path(self):
            self.ui.exec_path.setText(self.fileDialog.getExistingDirectory())

        def search_file_phyto(self):
            self.ui.phyto_path.setText(self.fileDialog.getOpenFileName())

        def search_file_bottom(self):
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

            #global self.nb_errors

            check_num = '(^([0-9]+[.]?[0-9]*[,]?){1,})|(^([0-9]+[,]){1,})'  #regular expression to use
            self.prog = re.compile(check_num)  #analysis object creation
            p_result = self.prog.search(self.p_values)  #string retrieval thanks to the regular expression
            wavelength_result = self.prog.search(self.wavelength_values)

            try:
                if p_result.group() != self.ui.p_values.text():
                    self.ui.p_label.setStyleSheet('color: red')
                    self.nb_errors += 1
                else:
                    self.ui.p_label.setStyleSheet('color: black')
                    self.nb_errors -= 1
            except AttributeError:
                self.ui.p_label.setStyleSheet('color: red')
                self.nb_errors += 1
            try:
                if wavelength_result.group() != self.ui.wavelength_values.text():
                    self.ui.waveL_label.setStyleSheet('color: red')
                    self.nb_errors += 1
                else:
                    self.ui.waveL_label.setStyleSheet('color: black')
                    self.nb_errors -= 1
            except AttributeError:
                self.ui.waveL_label.setStyleSheet('color: red')
                self.nb_errors += 1

            #--------------------------------------------------#
            #The following check values containing only numbers.
            #--------------------------------------------------#
            check_num2 = '^([0-9]+[.]?[0-9]*)'
            self.prog2 = re.compile(check_num2)
            x_result = self.prog2.search(self.x_value)
            y_result = self.prog2.search(self.y_value)
            g_result = self.prog2.search(self.g_value)
            s_result = self.prog2.search(self.s_value)
            z_result = self.prog2.search(self.z_value)

            try:
                if x_result.group() != self.ui.x_value.text():
                    self.ui.particules_label.setStyleSheet('color: red')
                    self.ui.x_label.setStyleSheet('color: red')
                    self.nb_errors += 1
                else:
                    self.ui.particules_label.setStyleSheet('color: black')
                    self.ui.x_label.setStyleSheet('color: black')
                    self.nb_errors -= 1
            except AttributeError:
                self.ui.particules_label.setStyleSheet('color: red')
                self.ui.x_label.setStyleSheet('color: red')
                self.nb_errors += 1
            try:
                if y_result.group() != self.ui.y_value.text():
                    self.ui.particules_label.setStyleSheet('color: red')
                    self.ui.y_label.setStyleSheet('color: red')
                    self.nb_errors += 1
                else:
                    self.ui.particules_label.setStyleSheet('color: black')
                    self.ui.y_label.setStyleSheet('color: black')
                    self.nb_errors -= 1
            except AttributeError:
                self.ui.particules_label.setStyleSheet('color: red')
                self.ui.y_label.setStyleSheet('color: red')
                self.nb_errors += 1
            try:
                if g_result.group() != self.ui.g_value.text():
                    self.ui.organic_label.setStyleSheet('color: red')
                    self.ui.g_label.setStyleSheet('color: red')
                    self.nb_errors += 1
                else:
                    self.ui.organic_label.setStyleSheet('color: black')
                    self.ui.g_label.setStyleSheet('color: black')
                    self.nb_errors -= 1
            except AttributeError:
                self.ui.organic_label.setStyleSheet('color: red')
                self.ui.g_label.setStyleSheet('color: red')
                self.nb_errors += 1
            try:
                if s_result.group() != self.ui.s_value.text():
                    self.ui.organic_label.setStyleSheet('color: red')
                    self.ui.s_label.setStyleSheet('color: red')
                    self.nb_errors += 1
                else:
                    self.ui.organic_label.setStyleSheet('color: black')
                    self.ui.s_label.setStyleSheet('color: black')
                    self.nb_errors -= 1
            except AttributeError:
                self.ui.organic_label.setStyleSheet('color: red')
                self.ui.s_label.setStyleSheet('color: red')
                self.nb_errors += 1
            try:
                if z_result.group() != self.ui.z_value.text():
                    self.ui.z_label.setStyleSheet('color: red')
                    self.nb_errors += 1
                else:
                    self.ui.z_label.setStyleSheet('color: black')
                    self.nb_errors -= 1
            except AttributeError:
                self.ui.z_label.setStyleSheet('color: red')
                self.nb_errors += 1

            check_num3 = '[1-6]+'
            self.prog3 = re.compile(check_num3)
            verbose_result = self.prog3.search(self.verbose_value)

            try:
                if verbose_result.group() != self.ui.verbose_value.text():
                    self.ui.verbose_label.setStyleSheet('color: red')
                    self.nb_errors += 1
                else:
                    self.ui.verbose_label.setStyleSheet('color: black')
                    self.nb_errors -= 1
            except AttributeError:
                self.ui.verbose_label.setStyleSheet('color: red')
                self.nb_errors += 1

            #--------------------------------------------------#
            #The following check values containing only numbers.
            #--------------------------------------------------#
            """
            check_num4 = '[/]([A-Za-z]+[/]?)+[A-Za-z]$'
            self.prog4 = re.compile(check_num4)
            phyto_path_result = self.prog4.search(self.phyto_path)
            bottom_path_result = self.prog4.search(self.bottom_path)
            exec_path_result = self.prog4.search(self.exec_path)

            try:
                if phyto_path_result.group() != self.ui.phyto_path.text():
                    self.ui.phyto_label.setStyleSheet('color: red')
                    self.nb_errors += 1
                else:
                    self.ui.phyto_label.setStyleSheet('color: black')
                    self.nb_errors -= 1
            except AttributeError:
                self.ui.phyto_label.setStyleSheet('color: red')
                self.nb_errors += 1
            try:
                if bottom_path_result.group() != self.ui.bottom_path.text():
                    self.ui.bottom_label.setStyleSheet('color: red')
                    self.nb_errors += 1
                else:
                    self.ui.bottom_label.setStyleSheet('color: black')
                    self.nb_errors -= 1
            except AttributeError:
                self.ui.bottom_label.setStyleSheet('color: red')
                self.nb_errors += 1
            try:
                if exec_path_result.group() != self.ui.exec_path.text():
                    self.ui.execPath_label.setStyleSheet('color: red')
                    self.nb_errors += 1
                else:
                    self.ui.execPath_label.setStyleSheet('color: black')
                    self.nb_errors -= 1
            except AttributeError:
                self.ui.execPath_label.setStyleSheet('color: red')
                self.nb_errors += 1
            """
            print(self.nb_errors)
            return self.nb_errors

        def write_to_file():
            """
            This function call "gui_batch.py" with inputs values to write the batch file.
            No inputs.
            No return.
            """
            bt = BatchFile(self.p_values, self.x_value, self.y_value, self.g_value, self.s_value, self.z_value,
                           self.wavelength_values, self.verbose_value, self.phyto_path, self.bottom_path, self.nb_cpu,
                           self.exec_path)
            bt.write_batch_to_file()

        def display_error_message():
            """
            This function display an error message when a wrong value is typed.
            """
            self.ui.error_label.setScaledContents(True)
            self.ui.error_text_label.show()
            self.ui.error_text_label.setStyleSheet('color: red')

        def hide_error_message(self):
            """
            This function hide the error message when all values are correct.
            """
            self.ui.error_label.setScaledContents(False)
            self.ui.error_text_label.hide()

        def execute_planarrad():
            """
            This function execute planarrad using the batch file.
            """
            #VERIFIER L'AJOUT/SUPPRESSION D'ERREUR CAR FONCTIONNE MAL. DECREMENTE SIMPLEMENT QUAND PAS D'ERREUR (passage negatif)
            #ET INCREMENTE SIMPLEMENT QUAND ERREUR. NE S'ARRETE PAS A 0 OU 8.
            if self.nb_errors > 0:
                display_error_message()
            elif self.nb_errors == 0:
                hide_error_message(self)
                #PLACER ICI,REECRIT LE FICHIER BATCH ou pas? Appeller la fonction seulement plutot?
                self.ui.run.connect(self.ui.run, PyQt4.QtCore.SIGNAL('clicked()'), write_to_file)
                #os.chdir('../')
                #os.system('./planarrad.py -i /home/boulefi/PycharmProjects/planarradpy/inputs/batch_files/batch.txt')

        def cancel_planarrad():
            """
            This function cancel planarrad.
            """
            #raise sys.exit("Not done yet !")
            print ("Not done yet !")

        def progress_bar():
            self.timer = QtCore.QBasicTimer()
            self.timer.start(100, self)
            self.step = 0
            while self.step < 100 & self.timer.isActive():
                self.step += 1
                self.progressBar.setValue(self.step)

        def display_graphic():
            self.ui.widget.canvas.picture.clear()
            wavelength_min = 410
            wavelength_max = 730

            csv_file_name = "./rrs.csv"
            csv_file = open (csv_file_name,'r')

            wavelength = csv_file.readline() #Wavelength are the first line of the file.
            wavelength = wavelength.split('\t')
            wavelength = map(float,wavelength)
            data = csv_file.readline() #There is data of 'reflectance' in each line after.
            data_array = []
            while data != "":
                data = data.split('\t')
                data = map(float,data)
                data_array.append(data)
                data = csv_file.readline()

            #To chose one line, put them in an array, and in relation to arguments, chose one line

            #Loop on an array which have the curve(s) wanted (number) and get back each results.
            wavelength_wanted = []
            data_wanted = []
            i = 0
            while i < len(data_array):
                data_wanted.append([])
                i += 1

            for value in wavelength: #For each value in the first line (wavelength).
                if (value > wavelength_min) & (value < wavelength_max): #If the wavelength is between min and max (the part that we want to keep).
                    wavelength_wanted.append(value) #We keep the value of the wavelength.
                    index = wavelength.index(value) #Find the index of the value.
                    j = 0
                    for row_data_array in data_array:
                        data_wanted[j].append(row_data_array[index]) #Thanks to this index, we can find where is the value of reflectance we want to keep.
                        j += 1

            x = scipy.linspace(wavelength_min,wavelength_max,len(wavelength_wanted))

            n = 1
            for row_data_wanted in data_wanted:
                y = row_data_wanted
                self.ui.widget.canvas.picture.plot(x,y,label='Case : '+str(n))
                n += 1

            self.ui.widget.canvas.picture.set_xlabel('Wavelength (${nm}$)')
            self.ui.widget.canvas.picture.set_ylabel('Reflectance ($Sr^{-1}$)')
            self.ui.widget.canvas.picture.set_title('Rrs.csv')
            self.ui.widget.canvas.print_figure('Rrs.png') #Save the graphic in a file in the current repository
            self.legend = self.ui.widget.canvas.picture.legend() #display in a legend curves's labels.
            self.legend.figure.canvas.draw()

            csv_file.close()
            self.ui.widget.canvas.draw()

        #------------------------------------------#
        #The following connect buttons to an action.
        #------------------------------------------#
        hide_error_message(self)
        self.ui.phyto_button.connect(self.ui.phyto_button, PyQt4.QtCore.SIGNAL('clicked()'), search_file_phyto)
        self.ui.bottom_button.connect(self.ui.bottom_button, PyQt4.QtCore.SIGNAL('clicked()'), search_file_bottom)
        self.ui.exec_path_button.connect(self.ui.exec_path_button, PyQt4.QtCore.SIGNAL('clicked()'),
                                         search_directory_exec_path)
        self.ui.run.connect(self.ui.run, PyQt4.QtCore.SIGNAL('clicked()'), data)
        #self.ui.run.connect(self.ui.run, PyQt4.QtCore.SIGNAL('clicked()'),
        #                    progress_bar)  #A METTRE DANS 'EXECUTE_PLANARRAD' LORSQUE CELA FONCTIONNERA
        self.ui.run.connect(self.ui.run, PyQt4.QtCore.SIGNAL('clicked()'), check_values)
        self.ui.run.connect(self.ui.run, PyQt4.QtCore.SIGNAL('clicked()'), execute_planarrad)

        #if self.can_run:
        #    self.ui.run.connect(self.ui.run,PyQt4.QtCore.SIGNAL('clicked()'),execute_planarrad)
        #else:
        #    # do something

        self.ui.cancel.connect(self.ui.cancel, PyQt4.QtCore.SIGNAL('clicked()'), cancel_planarrad)
        self.ui.cancel.connect(self.ui.cancel, PyQt4.QtCore.SIGNAL('clicked()'), display_graphic)
        self.ui.quit.connect(self.ui.quit, PyQt4.QtCore.SIGNAL('clicked()'), quit)

        self.main_window.show()
        sys.exit(app.exec_())


if __name__ == "__main__":
    FE = FormEvents()