#!/usr/bin/env python

import PyQt4
from PyQt4 import QtGui
from time import sleep
from timeit import Timer
import PyQt4.QtCore
import sys
import os
import multiprocessing
import re
import scipy

from gui_batch import BatchFile
from matplotlibwidgetFile import matplotlibWidget
from gui_Layout import *

class FormEvents():
    """
    This class creates answers of buttons of the user interface and checks values that the user typed.
    """

    def __init__(self):

        app = QtGui.QApplication(sys.argv)
        self.main_window = QtGui.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_window)

        self.file_dialog = QtGui.QFileDialog()
        self.main_window.setFixedSize(1400, 825)
        self.widget = matplotlibWidget()
        self.nb_errors = 0
        self.slider_value = 0
        self.ui.show_all_curves.setCheckState(2)

        #----------------------------------------------------------------------------------------------#
        #The following permits to know how many CPU there is in the computer to list them in a comboBox.
        #----------------------------------------------------------------------------------------------#
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
            self.y_value = self.ui.y_value.text()
            self.g_value = self.ui.g_value.text()
            self.s_value = self.ui.s_value.text()
            self.z_value = self.ui.z_value.text()
            self.wavelength_values = self.ui.wavelength_values.text()
            self.verbose_value = self.ui.verbose_value.text()
            self.phyto_path = self.ui.phyto_path.text()
            self.bottom_path = self.ui.bottom_path.text()
            self.exec_path = self.ui.exec_path.text()
            self.nb_cpu = self.ui.nb_cpu.currentText()

        #-------------------------------------------------------------------------------#
        #These following functions displays a fileDialog to search a file or a directory.
        #-------------------------------------------------------------------------------#
        def search_directory_exec_path(self):
            self.ui.exec_path.setText(self.fileDialog.getExistingDirectory())

        def search_file_phyto(self):
            self.ui.phyto_path.setText(self.fileDialog.getOpenFileName())

        def search_file_bottom(self):
            self.ui.bottom_path.setText(self.fileDialog.getOpenFileName())

        #------------------------------------------------------------------------------#

        def check_values():
            """
            This function check if there is no problem about values given.
            If there is a problem with a or some values, their label's color is changed to red,
            and call a function to display a error message.
            """

            #--------------------------------------------#
            #The following checks values containing comas.
            #--------------------------------------------#

            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            #Si rien dans le chemin de repertoire, programme freeze
            #a voir si cela fait pareil pour les fichiers
            #PB avec les chemins !!!! -> FREEZE
            # un point peut etre present sans rien apres,
            # espace avant ou apres virgule marche pas
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            check_num = '(^([0-9]+[.]?[0-9]*[,]?){1,})|(^([0-9]+[,]){1,})'  #regular expression to use
            self.prog = re.compile(check_num)  #analysis object creation
            p_result = self.prog.search(self.p_values)  #string retrieval thanks to the regular expression
            wavelength_result = self.prog.search(self.wavelength_values)

            try:
                if p_result.group() != self.ui.p_values.text():
                    self.ui.p_label.setStyleSheet('color: red')
                    self.nb_errors += 1
                else:
                    self.ui.p_label.setStyleSheet('color: 0.75')
                    self.nb_errors -= 1
            except AttributeError:
                self.ui.p_label.setStyleSheet('color: red')
                self.nb_errors += 1
            try:
                if wavelength_result.group() != self.ui.wavelength_values.text():
                    self.ui.waveL_label.setStyleSheet('color: red')
                    self.nb_errors += 1
                else:
                    self.ui.waveL_label.setStyleSheet('color: 0.75')
                    self.nb_errors -= 1
            except AttributeError:
                self.ui.waveL_label.setStyleSheet('color: red')
                self.nb_errors += 1

            #---------------------------------------------------#
            #The following checks values containing only numbers.
            #---------------------------------------------------#
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
                    self.ui.particules_label.setStyleSheet('color: 0.75')
                    self.ui.x_label.setStyleSheet('color: 0.75')
                    self.nb_errors -= 1
            except AttributeError:
                self.ui.particules_label.setStyleSheet('color: 0.75')
                self.ui.x_label.setStyleSheet('color: red')
                self.nb_errors += 1
            try:
                if y_result.group() != self.ui.y_value.text():
                    self.ui.particules_label.setStyleSheet('color: red')
                    self.ui.y_label.setStyleSheet('color: red')
                    self.nb_errors += 1
                else:
                    self.ui.particules_label.setStyleSheet('color: 0.75')
                    self.ui.y_label.setStyleSheet('color: 0.75')
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
                    self.ui.organic_label.setStyleSheet('color: 0.75')
                    self.ui.g_label.setStyleSheet('color: 0.75')
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
                    self.ui.organic_label.setStyleSheet('color: 0.75')
                    self.ui.s_label.setStyleSheet('color: 0.75')
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
                    self.ui.z_label.setStyleSheet('color: 0.75')
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
                    self.ui.verbose_label.setStyleSheet('color: 0.75')
                    self.nb_errors -= 1
            except AttributeError:
                self.ui.verbose_label.setStyleSheet('color: red')
                self.nb_errors += 1

            #---------------------------------------------------#
            #The following checks values containing only numbers.
            #---------------------------------------------------#
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
                    self.ui.phyto_label.setStyleSheet('color: 0.75')
                    self.nb_errors -= 1
            except AttributeError:
                self.ui.phyto_label.setStyleSheet('color: red')
                self.nb_errors += 1
            try:
                if bottom_path_result.group() != self.ui.bottom_path.text():
                    self.ui.bottom_label.setStyleSheet('color: red')
                    self.nb_errors += 1
                else:
                    self.ui.bottom_label.setStyleSheet('color: 0.75')
                    self.nb_errors -= 1
            except AttributeError:
                self.ui.bottom_label.setStyleSheet('color: red')
                self.nb_errors += 1
            try:
                if exec_path_result.group() != self.ui.exec_path.text():
                    self.ui.execPath_label.setStyleSheet('color: red')
                    self.nb_errors += 1
                else:
                    self.ui.execPath_label.setStyleSheet('color: 0.75')
                    self.nb_errors -= 1
            except AttributeError:
                self.ui.execPath_label.setStyleSheet('color: red')
                self.nb_errors += 1
            """
            print(self.nb_errors)
            return self.nb_errors

        def write_to_file():
            """
            This function calls "gui_batch.py" with inputs values to write the batch file.
            """
            bt = BatchFile(self.p_values, self.x_value, self.y_value, self.g_value, self.s_value, self.z_value,
                           self.wavelength_values, self.verbose_value, self.phyto_path, self.bottom_path, self.nb_cpu,
                           self.exec_path)
            bt.write_batch_to_file()

        def display_graphic():
            """
            This function plots results of a file into a graphic.
            """
            self.ui.widget.canvas.picture.clear()

            the_file_name = "./batch_report.txt"
            the_file = open(the_file_name,'r')

            lines = the_file.readlines()

            lines_array = []
            for line in lines:
                line = line.split('\t')
                lines_array.append(line)

            labels_line = lines_array[0]
            index = 8
            for label in labels_line:
                if label == ".*wave?length[.*]":
                    index = labels_line.index(label) #Find the index of the value.
                    break
                #else:
                #    raise sys.exit("Warning : There is no value named 'wavelength' in the file used to plot curves. "
                #                   "So, I can't separate data to plot curves and data about tests linking with these curves.")

            information = []
            data_wavelength = []
            l = 0
            for line in lines_array:
                c = 0
                information.append([])
                data_wavelength.append([])
                while c != len(line):
                    if c < index:
                        information[l].append(line[c])
                    elif c > index:
                        data_wavelength[l].append(line[c])
                    c += 1
                l += 1

            i = 0
            for row_data_wavelength in data_wavelength:
                row_data_wavelength = [float(item) for item in row_data_wavelength]
                data_wavelength[i] = row_data_wavelength
                i += 1

            wavelength = data_wavelength[0] #first line contains wavelength
            data_wanted = data_wavelength[1:]

            self.nb_case = i #This is the number of line, the number of case tested.
            graphic_slider(self.nb_case) #change values's slider to show or highlight the good curve.

            x = scipy.linspace(wavelength[0],wavelength[-1],len(wavelength))

            n = 0
            for row_data_wanted in data_wanted:
                if self.ui.show_all_curves.checkState() == 2:
                    y = row_data_wanted
                    if self.slider_value == n:
                        self.ui.widget.canvas.picture.plot(x,y,'-r',label='Case : '+str(n+1)+'/'+str(len(data_wanted)),linewidth=4)
                    else:
                        self.ui.widget.canvas.picture.plot(x,y,'0.75')
                else:
                    if self.slider_value == n:
                        y = row_data_wanted
                        self.ui.widget.canvas.picture.plot(x,y,'-r',label='Case : '+str(n+1)+'/'+str(len(data_wanted)))
                n += 1

            self.ui.widget.canvas.picture.set_title('Rrs.csv')
            self.ui.widget.canvas.picture.set_xlabel('Wavelength (${nm}$)')
            self.ui.widget.canvas.picture.set_ylabel('Reflectance ($Sr^{-1}$)')
            self.legend = self.ui.widget.canvas.picture.legend() #Display in a legend curves's labels.
            self.ui.widget.canvas.picture.legend(bbox_to_anchor=(1.1, 1.05))

            the_file.close()
            self.ui.widget.canvas.draw()

            """"
########################################################################################
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

            wavelength_wanted = []
            data_wanted = []
            i = 0
            while i < len(data_array):
                data_wanted.append([])
                i += 1

            self.nb_case = i #This is the number of line, the number of case tested.

            graphic_slider(self.nb_case) #change values's slider to show or highlight the good curve.

            for value in wavelength: #For each value in the first line (wavelength).
                if (value > wavelength_min) & (value < wavelength_max): #If the wavelength is between min and max (the part that we want to keep).
                    wavelength_wanted.append(value) #We keep the value of the wavelength.
                    index = wavelength.index(value) #Find the index of the value.
                    j = 0
                    for row_data_array in data_array:
                        data_wanted[j].append(row_data_array[index]) #Thanks to this index, we can find where is the value of reflectance we want to keep.
                        j += 1

            x = scipy.linspace(wavelength_min,wavelength_max,len(wavelength_wanted))

            n = 0
            for row_data_wanted in data_wanted:
                if self.ui.show_all_curves.checkState() == 2:
                    y = row_data_wanted
                    if self.slider_value == n:
                        self.ui.widget.canvas.picture.plot(x,y,'-r',label='Case : '+str(n+1)+'/'+str(len(data_wanted)),linewidth=4)
                    else:
                        self.ui.widget.canvas.picture.plot(x,y,'0.75')
                else:
                    if self.slider_value == n:
                        y = row_data_wanted
                        self.ui.widget.canvas.picture.plot(x,y,'-r',label='Case : '+str(n+1)+'/'+str(len(data_wanted)))
                n += 1


            self.ui.widget.canvas.picture.set_xlabel('Wavelength (${nm}$)')
            self.ui.widget.canvas.picture.set_ylabel('Reflectance ($Sr^{-1}$)')
            self.ui.widget.canvas.picture.set_title('Rrs.csv')
            self.legend = self.ui.widget.canvas.picture.legend() #Display in a legend curves's labels.
            self.ui.widget.canvas.picture.legend(bbox_to_anchor=(1.1, 1.05))

            csv_file.close()
            self.ui.widget.canvas.draw()
"""
        def graphic_slider(nb_case):
            """
            This function scales the slider for curves displayed.
            Return the value of the slider.
            """
            self.ui.sens.setRange(0,int(self.nb_case-1))
            self.slider_value = self.ui.sens.value()

            return self.slider_value

        def display_error_message():
            """
            This function displays an error message when a wrong value is typed.
            """
            self.ui.error_label.setScaledContents(True)
            self.ui.error_text_label.show()
            self.ui.error_text_label.setStyleSheet('color: red')

        def hide_error_message(self):
            """
            This function hides the error message when all values are correct.
            """
            self.ui.error_label.setScaledContents(False)
            self.ui.error_text_label.hide()

        def execute_planarrad():
            """
            This function executes planarRad using the batch file.
            """
            #VERIFIER L'AJOUT/SUPPRESSION D'ERREUR CAR FONCTIONNE MAL. DECREMENTE SIMPLEMENT QUAND PAS D'ERREUR (passage negatif)
            #ET INCREMENTE SIMPLEMENT QUAND ERREUR. NE S'ARRETE PAS A 0 OU 8.
            data()
            check_values()
            if self.nb_errors > 0:
                display_error_message()
            elif self.nb_errors == 0:
                hide_error_message(self)
                #PLACER ICI,REECRIT LE FICHIER BATCH ou pas? Appeller la fonction seulement plutot?
                self.ui.run.connect(self.ui.run, PyQt4.QtCore.SIGNAL('clicked()'), write_to_file)
                progress_bar() #FREEZE, BESOIN D'UN THREAD, LE MEME AUE POUR EXECUTER PANARRAD?
                #os.chdir('../')
                #os.system('./planarrad.py -i /home/boulefi/PycharmProjects/planarradpy/inputs/batch_files/batch.txt')

        def progress_bar():
            """
            This function updates the progress bar.
            """
            self.step = 0
            self.ui.progressBar.reset()
            while self.step < 100:
                sleep(1)
                self.step += 1
                self.ui.progressBar.setValue(self.step)

        def cancel_planarrad():
            """
            This function cancels planarRad.
            """
            #Besoin de faire deux threads, un pour lancer planaRad, que l'on stoppera avec ce bouton.'
            #raise sys.exit("Not done yet !")
            print ("cancel_planarrad Not done yet !")
            self.ui.progressBar.reset()

        def save_figure():
            """
            This function programs the button to save the figure displayed.
            """
            self.ui.widget.canvas.print_figure('Rrs.png') #Save the graphic in a file in the current repository

        def prerequisite_actions():
            """
            This function do all required actions at the beginning when we run the GUI.
            """
            hide_error_message(self)
            display_graphic()
            self.ui.progressBar.reset()

        #-------------------------------------------#
        #The following connects buttons to an action.
        #-------------------------------------------#
        prerequisite_actions()

        self.ui.phyto_button.connect(self.ui.phyto_button, PyQt4.QtCore.SIGNAL('clicked()'), search_file_phyto)
        self.ui.bottom_button.connect(self.ui.bottom_button, PyQt4.QtCore.SIGNAL('clicked()'), search_file_bottom)
        self.ui.exec_path_button.connect(self.ui.exec_path_button, PyQt4.QtCore.SIGNAL('clicked()'),
                                         search_directory_exec_path)

        self.ui.run.connect(self.ui.run, PyQt4.QtCore.SIGNAL('clicked()'), execute_planarrad)
        self.ui.cancel.connect(self.ui.cancel, PyQt4.QtCore.SIGNAL('clicked()'), cancel_planarrad)

        self.ui.sens.connect(self.ui.sens, QtCore.SIGNAL('valueChanged(int)'), display_graphic)
        self.ui.show_all_curves.connect(self.ui.show_all_curves, QtCore.SIGNAL('stateChanged(int)'), display_graphic)
        self.ui.save_figure.connect(self.ui.save_figure, PyQt4.QtCore.SIGNAL('clicked()'), save_figure)

        self.ui.quit.connect(self.ui.quit, PyQt4.QtCore.SIGNAL('clicked()'), quit)

        self.main_window.show()
        sys.exit(app.exec_())


if __name__ == "__main__":
    FE = FormEvents()