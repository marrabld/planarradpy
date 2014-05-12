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
        self.graphic_widget = matplotlibWidget()
        self.nb_errors = 0
        self.slider_value = 0
        self.ui.show_all_curves.setCheckState(2)
        self.result_file = "./batch_report.txt"
        # context menu
        self.tableWidget = QtGui.QTableWidget()
        self.tableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

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
            This function gets back data that the user typed.
            """
            self.batch_name_value = self.ui.batch_name_value.text()
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
            self.report_parameter_value = self.ui.report_parameter_value.text()

        #-------------------------------------------------------------------------------#
        #These following functions display a fileDialog to search a file or a directory.
        #-------------------------------------------------------------------------------#
        def search_directory_exec_path():
            self.ui.exec_path.setText(self.file_dialog.getExistingDirectory())

        #Faire appel a la meme fonction?
        def search_file_phyto():
            self.ui.phyto_path.setText(self.file_dialog.getOpenFileName())

        def search_file_bottom():
            self.ui.bottom_path.setText(self.file_dialog.getOpenFileName())

        def search_file_result():
            self.result_file = self.file_dialog.getOpenFileName()
            return self.result_file

        #------------------------------------------------------------------------------#

        def check_values():
            """
            This function checks if there is no problem about values given.
            If there is a problem with a or some values, their label's color is changed to red,
            and call a function to display a error message.
            If there is no problem, their label, if it is necessary, is changed to grey (default color).
            """

            #--------------------------------------------------------#
            #The following checks values seperate by containing comas.
            #--------------------------------------------------------#

            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            #Syntax test doesn't work for paths!
            #And problem with number of errors.
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # No test for "report_parameter_value" !
            # No test for "batch_name_value" !

            check_num = '(^([0-9]+[.]?[0-9]*[,]?){1,})|(^([0-9]+[,]){1,})'  #regular expression to use
            self.prog = re.compile(check_num)  #analysis object creation
            p_result = self.prog.search(self.p_values)  #string retrieval thanks to the regular expression
            wavelength_result = self.prog.search(self.wavelength_values)

            try:
                if p_result.group() != self.ui.p_values.text():
                    self.ui.p_label.setStyleSheet('color: red')
                    self.nb_errors += 1
                    print('error1')
                else:
                    self.ui.p_label.setStyleSheet('color: 0.75')
                    self.nb_errors -= 1
                    print('resolved 1')
            except AttributeError:
                self.ui.p_label.setStyleSheet('color: red')
                self.nb_errors += 1
                print('error1')
            try:
                if wavelength_result.group() != self.ui.wavelength_values.text():
                    self.ui.waveL_label.setStyleSheet('color: red')
                    self.nb_errors += 1
                    print('error2')
                else:
                    self.ui.waveL_label.setStyleSheet('color: 0.75')
                    self.nb_errors -= 1
                    print('resolved 2')
            except AttributeError:
                self.ui.waveL_label.setStyleSheet('color: red')
                self.nb_errors += 1
                print('error2')

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
                    print('error3')
                else:
                    self.ui.particules_label.setStyleSheet('color: 0.75')
                    self.ui.x_label.setStyleSheet('color: 0.75')
                    self.nb_errors -= 1
                    print('resolved 3')
            except AttributeError:
                self.ui.particules_label.setStyleSheet('color: 0.75')
                self.ui.x_label.setStyleSheet('color: red')
                self.nb_errors += 1
                print('error3')
            try:
                if y_result.group() != self.ui.y_value.text():
                    self.ui.particules_label.setStyleSheet('color: red')
                    self.ui.y_label.setStyleSheet('color: red')
                    self.nb_errors += 1
                    print('error4')
                else:
                    self.ui.particules_label.setStyleSheet('color: 0.75')
                    self.ui.y_label.setStyleSheet('color: 0.75')
                    self.nb_errors -= 1
                    print('resolved 4')
            except AttributeError:
                self.ui.particules_label.setStyleSheet('color: red')
                self.ui.y_label.setStyleSheet('color: red')
                self.nb_errors += 1
                print('error4')
            try:
                if g_result.group() != self.ui.g_value.text():
                    self.ui.organic_label.setStyleSheet('color: red')
                    self.ui.g_label.setStyleSheet('color: red')
                    self.nb_errors += 1
                    print('error5')
                else:
                    self.ui.organic_label.setStyleSheet('color: 0.75')
                    self.ui.g_label.setStyleSheet('color: 0.75')
                    self.nb_errors -= 1
                    print('resolved 5')
            except AttributeError:
                self.ui.organic_label.setStyleSheet('color: red')
                self.ui.g_label.setStyleSheet('color: red')
                self.nb_errors += 1
                print('error5')
            try:
                if s_result.group() != self.ui.s_value.text():
                    self.ui.organic_label.setStyleSheet('color: red')
                    self.ui.s_label.setStyleSheet('color: red')
                    self.nb_errors += 1
                    print('error6')
                else:
                    self.ui.organic_label.setStyleSheet('color: 0.75')
                    self.ui.s_label.setStyleSheet('color: 0.75')
                    self.nb_errors -= 1
                    print('resolved 6')
            except AttributeError:
                self.ui.organic_label.setStyleSheet('color: red')
                self.ui.s_label.setStyleSheet('color: red')
                self.nb_errors += 1
                print('error6')
            try:
                if z_result.group() != self.ui.z_value.text():
                    self.ui.z_label.setStyleSheet('color: red')
                    self.nb_errors += 1
                    print('error7')
                else:
                    self.ui.z_label.setStyleSheet('color: 0.75')
                    self.nb_errors -= 1
                    print('resolved 7')
            except AttributeError:
                self.ui.z_label.setStyleSheet('color: red')
                self.nb_errors += 1
                print('error7')

            check_num3 = '[1-6]+'
            self.prog3 = re.compile(check_num3)
            verbose_result = self.prog3.search(self.verbose_value)

            try:
                if verbose_result.group() != self.ui.verbose_value.text():
                    self.ui.verbose_label.setStyleSheet('color: red')
                    self.nb_errors += 1
                    print('error8')
                else:
                    self.ui.verbose_label.setStyleSheet('color: 0.75')
                    self.nb_errors -= 1
                    print('resolved 8')
            except AttributeError:
                self.ui.verbose_label.setStyleSheet('color: red')
                self.nb_errors += 1
                print('error8')

            #------------------------------------------------#
            #The following checks values containing only path.
            #------------------------------------------------#

            #!!!!!!!!!!!!!!!!!!!!!!!!!!
            #Syntax test doesn't work ! ->  #check_num4 = '[/]([A-Za-z]+[/]?)+[A-Za-z]$'
            #!!!!!!!!!!!!!!!!!!!!!!!!!!

            check_num4 = '(.*)' #Take all strings possible.
            self.prog4 = re.compile(check_num4)
            phyto_path_result = self.prog4.search(self.phyto_path)
            bottom_path_result = self.prog4.search(self.bottom_path)
            exec_path_result = self.prog4.search(self.exec_path)

            try:
                if phyto_path_result.group() != self.ui.phyto_path.text():
                    self.ui.phyto_label.setStyleSheet('color: red')
                    self.nb_errors += 1
                    print('error9')
                else:
                    self.ui.phyto_label.setStyleSheet('color: 0.75')
                    self.nb_errors -= 1
                    print('resolved 9')
            except AttributeError:
                self.ui.phyto_label.setStyleSheet('color: red')
                self.nb_errors += 1
                print('error9')
            try:
                if bottom_path_result.group() != self.ui.bottom_path.text():
                    self.ui.bottom_label.setStyleSheet('color: red')
                    self.nb_errors += 1
                    print('error10')
                else:
                    self.ui.bottom_label.setStyleSheet('color: 0.75')
                    self.nb_errors -= 1
                    print('resolved 10')
            except AttributeError:
                self.ui.bottom_label.setStyleSheet('color: red')
                self.nb_errors += 1
                print('error10')
            try:
                if exec_path_result.group() != self.ui.exec_path.text():
                    self.ui.execPath_label.setStyleSheet('color: red')
                    self.nb_errors += 1
                    print('error11')
                else:
                    self.ui.execPath_label.setStyleSheet('color: 0.75')
                    self.nb_errors -= 1
                    print('resolved 11')
            except AttributeError:
                self.ui.execPath_label.setStyleSheet('color: red')
                self.nb_errors += 1
                print('error11')


            print(self.nb_errors)
            return self.nb_errors

        def write_to_file():
            """
            This function calls "gui_batch.py" with inputs values to write the batch file.
            """
            bt = BatchFile(self.batch_name_value, self.p_values, self.x_value, self.y_value, self.g_value, self.s_value, self.z_value,
                           self.wavelength_values, self.verbose_value, self.phyto_path, self.bottom_path, self.nb_cpu,
                           self.exec_path, self.report_parameter_value)
            bt.write_batch_to_file()

        def display_graphic():
            """
            This function plots results of a file into a graphic.
            """
            self.ui.graphic_widget.canvas.picture.clear()

            #the_file_name = "./batch_report.txt"
            the_file_name = str(self.result_file)
            the_file = open(the_file_name, 'r')

            lines = the_file.readlines()

            #We put all lines in an array and we put each part of the line in a column.
            lines_array = []
            for line in lines:
                line = line.split('\t')
                lines_array.append(line)

            labels_line = lines_array[0]
            j = 0
            flag = True
            #ICI ON NE FINI PAS A LA FIN DE LA LIGNE, ON CONTINUE APRES VOILA POURQUOI INDEXERROR
            try:
                while flag:
                    if labels_line[j] == '#wave length (nm) ->':
                        index = labels_line.index(labels_line[j])  #Find the index of the value.
                        flag = False
                    else:
                        j += 1
            except IndexError:
                raise sys.exit("Warning : There is no value named 'wavelength' in the file used to plot curves. "
                               "So, I can't separate data to plot curves and data about tests linking with these curves.")

            information = [] #This array will contain the data displayed under the curves.
            data_wavelength = [] #This array will contain the data to plot curves.
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

            #We transform wavelengths from strings to floats.
            i = 0
            for row_data_wavelength in data_wavelength:
                row_data_wavelength = [float(item) for item in row_data_wavelength]
                data_wavelength[i] = row_data_wavelength
                i += 1

            wavelength = data_wavelength[0]  #The first line contains wavelength
            data_wanted = data_wavelength[1:] #The others contain data useful to plot curves.

            self.nb_case = i-1  #This is the number of line, the number of test.
            graphic_slider(self.nb_case)  #change value's slider to show or highlight the good curve.

            x = scipy.linspace(wavelength[0], wavelength[-1], len(wavelength)) #X-axis

            n = 0
            for row_data_wanted in data_wanted:
                #Following if the checkbox is checked (show all curves) or not.
                if self.ui.show_all_curves.checkState() == 2:
                    y = row_data_wanted
                    #Following the curve selected, we draw it differently.
                    if self.slider_value == n:
                        self.ui.graphic_widget.canvas.picture.plot(x, y, '-r',
                                                           label='Case : ' + str(n + 1) + '/' + str(len(data_wanted)),
                                                           linewidth=4)
                        show_information_nb = n
                    else:
                        self.ui.graphic_widget.canvas.picture.plot(x, y, '0.75')
                else:
                    if self.slider_value == n:
                        y = row_data_wanted
                        self.ui.graphic_widget.canvas.picture.plot(x, y, '-r',
                                                           label='Case : ' + str(n + 1) + '/' + str(len(data_wanted)))
                        show_information_nb = n
                n += 1

            self.ui.graphic_widget.canvas.picture.set_title('Rrs.csv')
            self.ui.graphic_widget.canvas.picture.set_xlabel('Wavelength (${nm}$)')
            self.ui.graphic_widget.canvas.picture.set_ylabel('Reflectance ($Sr^{-1}$)')
            self.legend = self.ui.graphic_widget.canvas.picture.legend()  #Display in a legend curves's labels.
            self.ui.graphic_widget.canvas.picture.legend(bbox_to_anchor=(1.1, 1.05))

            label_information = information[0]
            data_information = information[1:]
            k = 0
            #nb_label = len(label_information)
            #while k <= nb_label:
            #    self.ui.column1_label.setText(label_information[0])
            #    self.ui.column2_label.setText(label_information[0])
            #    self.ui.column3_label.setText(label_information[0])
            #    self.ui.column4_label.setText(label_information[0])
            #    self.ui.column5_label.setText(label_information[0])
            #    self.ui.column6_label.setText(label_information[0])
            #    self.ui.column7_label.setText(label_information[0])
            #    self.ui.column8_label.setText(label_information[0])
            #k += 1

            m = 0
            while m < len(data_information):
                if m == show_information_nb:
                    self.ui.column1_result.setText(data_information[m][0])
                    self.ui.column2_result.setText(data_information[m][1])
                    self.ui.column3_result.setText(data_information[m][2])
                    self.ui.column4_result.setText(data_information[m][3])
                    self.ui.column5_result.setText(data_information[m][4])
                    self.ui.column6_result.setText(data_information[m][5])
                    self.ui.column7_result.setText(data_information[m][6])
                    self.ui.column8_result.setText(data_information[m][7])
                m += 1

            the_file.close()
            self.ui.graphic_widget.canvas.draw()

        def graphic_slider(nb_case):
            """
            This function scales the slider for curves displayed.
            Input : The number of cases (curves).
            Return ; The slider's value.
            """
            self.ui.sens.setRange(0, int(self.nb_case - 1))
            self.slider_value = self.ui.sens.value()

            return self.slider_value

        def display_error_message():
            """
            This function displays an error message when a wrong value is typed.
            """
            self.ui.error_label.setScaledContents(True) #Warning image
            self.ui.error_text_label.show() #Warning message
            self.ui.error_text_label.setStyleSheet('color: red')

        def hide_error_message(self):
            """
            This function hides the error message when all values are correct.
            """
            self.ui.error_label.setScaledContents(False) #Warning image
            self.ui.error_text_label.hide() #Warning message

        def execute_planarrad():
            """
            This function executes planarRad using the batch file.
            """
            data()
            check_values()

            if self.nb_errors > 0:
                display_error_message()
            elif self.nb_errors == 0:
                hide_error_message(self)
                write_to_file()
                progress_bar()
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
            print ("cancel_planarrad not done yet !")
            self.ui.progressBar.reset()

        def save_figure():
            """
            This function programs the button to save the figure displayed
            and save the graphic in a file in the current repository.
            """
            self.ui.graphic_widget.canvas.print_figure('Rrs.png')

        def prerequisite_actions():
            """
            This function do all required actions at the beginning when we run the GUI.
            """
            hide_error_message(self)
            display_graphic()
            self.ui.progressBar.reset()

        # def context_menu(event):
        #     context_menu = QtGui.Menu()
        #     action1 = context_menu.addAction("ssss")
        #     context_menu.exec_(event.globalPos())

        def onClick(self,e):
            if e.button == 3:
                pos = QtGui.QCursor().po()
                self.open_graphic_context_Menu(pos)

        def open_graphic_context_Menu(pos):
            graphic_context_menu = QtGui.Menu()
            save_graphic_action = graphic_context_menu("sss")
            save_graphic_action = graphic_context_menu.exec_(self.tableWidget.mapFromGlobal(pos))

        prerequisite_actions()

        #-------------------------------------------#
        #The following connects buttons to an action.
        #-------------------------------------------#

        self.ui.phyto_button.connect(self.ui.phyto_button, PyQt4.QtCore.SIGNAL('clicked()'), search_file_phyto)
        self.ui.bottom_button.connect(self.ui.bottom_button, PyQt4.QtCore.SIGNAL('clicked()'), search_file_bottom)
        self.ui.exec_path_button.connect(self.ui.exec_path_button, PyQt4.QtCore.SIGNAL('clicked()'),
                                         search_directory_exec_path)
        self.ui.open_result_file_button.connect(self.ui.open_result_file_button, PyQt4.QtCore.SIGNAL('clicked()'),
                                         search_file_result)

        self.ui.run.connect(self.ui.run, PyQt4.QtCore.SIGNAL('clicked()'), execute_planarrad)
        self.ui.cancel.connect(self.ui.cancel, PyQt4.QtCore.SIGNAL('clicked()'), cancel_planarrad)

        self.ui.sens.connect(self.ui.sens, QtCore.SIGNAL('valueChanged(int)'), display_graphic)
        self.ui.show_all_curves.connect(self.ui.show_all_curves, QtCore.SIGNAL('stateChanged(int)'), display_graphic)

        #Save the figure with a right click !
        #self.graphic_right_click = self.ui.graphic_widget.canvas.mpl_connect('button_press_event',onClick)
        self.ui.graphic_widget.canvas.connect(self.ui.graphic_widget.canvas, QtCore.SIGNAL('button_press_event'),onClick)
        self.ui.quit.connect(self.ui.quit, PyQt4.QtCore.SIGNAL('clicked()'), quit)

        self.main_window.show()
        sys.exit(app.exec_())


if __name__ == "__main__":
    FE = FormEvents()