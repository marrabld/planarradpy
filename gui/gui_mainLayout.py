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

from gui_batch import BatchFile
from gui_Layout import *
import matplotlibwidgetFile


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
        self.graphic_widget = matplotlibwidgetFile.matplotlibWidget()
        self.mpl_canvas = matplotlibwidgetFile.MplCanvas()
        self.nb_errors = 0
        self.slider_value = 0
        self.data_wanted = []
        self.num_line = 0
        self.wavelength = []
        self.information = []
        self.ui.show_all_curves.setCheckState(2)
        self.result_file = "./batch_report.txt"

        # context menu
        #self.tableWidget = QtGui.QTableWidget()
        #self.tableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        #----------------------------------------------------------------------------------------------#
        #The following permits to know how many CPU there is in the computer to list them in a comboBox.
        #----------------------------------------------------------------------------------------------#
        self.cpu = multiprocessing.cpu_count()
        self.nb_cpu = self.ui.nb_cpu.addItem("-1")
        count_cpu = 1  #Iterator on the number of cpu.
        while count_cpu <= self.cpu:
            self.nb_cpu = self.ui.nb_cpu.addItem(str(count_cpu))
            count_cpu += 1

        self.prerequisite_actions()

        #-------------------------------------------#
        #The following connects buttons to an action.
        #-------------------------------------------#

        self.ui.phyto_button.connect(self.ui.phyto_button, PyQt4.QtCore.SIGNAL('clicked()'), self.search_file_phyto)
        self.ui.bottom_button.connect(self.ui.bottom_button, PyQt4.QtCore.SIGNAL('clicked()'), self.search_file_bottom)
        self.ui.exec_path_button.connect(self.ui.exec_path_button, PyQt4.QtCore.SIGNAL('clicked()'),
                                         self.search_directory_exec_path)

        self.ui.open_result_file_button.connect(self.ui.open_result_file_button, PyQt4.QtCore.SIGNAL('clicked()'),
                                                self.search_file_result)
        # self.old_result_file = self.result_file
        # if self.old_result_file != self.result_file:
        #     self.data_processing()
        #     self.display_the_graphic(self.num_line, self.wavelength, self.data_wanted, self.information)

        self.ui.run.connect(self.ui.run, PyQt4.QtCore.SIGNAL('clicked()'), self.execute_planarrad)
        self.ui.cancel.connect(self.ui.cancel, PyQt4.QtCore.SIGNAL('clicked()'), self.cancel_planarrad)

        self.ui.sens.connect(self.ui.sens, QtCore.SIGNAL('valueChanged(int)'), self.display_the_graphic_connection)
        self.ui.show_all_curves.connect(self.ui.show_all_curves, QtCore.SIGNAL('stateChanged(int)'),
                                        self.display_the_graphic_connection)

        #Save the figure with a right click !
        #self.graphic_right_click = self.ui.graphic_widget.canvas.mpl_connect('button_press_event',onClick)
        #self.ui.graphic_widget.canvas.connect(self.ui.graphic_widget.canvas, QtCore.SIGNAL('button_press_event'),
        #                                      self.onClick)

        self.ui.quit.connect(self.ui.quit, PyQt4.QtCore.SIGNAL('clicked()'), quit)
        self.main_window.show()
        sys.exit(app.exec_())

    def data(self):
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
    def search_directory_exec_path(self):
        self.ui.exec_path.setText(self.file_dialog.getExistingDirectory())

    """ Maybe create only one function with a variable to know which line we execute"""

    def search_file_phyto(self):
        self.ui.phyto_path.setText(self.file_dialog.getOpenFileName())

    def search_file_bottom(self):
        self.ui.bottom_path.setText(self.file_dialog.getOpenFileName())

    def search_file_result(self):
        """
        This function once the file found, display again a graphic with the nez data.
        """
        self.result_file = self.file_dialog.getOpenFileName()
        self.data_processing()
        self.display_the_graphic(self.num_line, self.wavelength, self.data_wanted, self.information)

    #------------------------------------------------------------------------------#

    def check_values(self):
        """
        This function checks if there is no problem about values given.
        If there is a problem with a or some values, their label's color is changed to red,
        and call a function to display a error message.
        If there is no problem, their label, if it is necessary, is changed to grey (default color).
        Return ; nb_errors ; The number of errors.
        """

        #--------------------------------------------------------#
        #The following checks values separate by containing comas.
        #--------------------------------------------------------#

        """
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        Syntax test doesn't work for paths!
        And problem with number of errors.
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        No test for "report_parameter_value" !
        No test for "batch_name_value" !
        """

        check_num = '(^([0-9]+[.]?[0-9]*[,]?){1,})|(^([0-9]+[,]){1,})'  #Regular expression to use
        self.prog = re.compile(check_num)  #Qnalysis object creation
        p_result = self.prog.search(self.p_values)  #String retrieval thanks to the regular expression
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

        #------------------------------------------------#
        #The following checks values containing only path.
        #------------------------------------------------#

        """
        #!!!!!!!!!!!!!!!!!!!!!!!!!!
        #Syntax test doesn't work ! ->  #check_num4 = '[/]([A-Za-z]+[/]?)+[A-Za-z]$'
        #!!!!!!!!!!!!!!!!!!!!!!!!!!
        """

        check_num4 = '(.*)'  #Take all strings possible.
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

        print(self.nb_errors)
        return self.nb_errors

    def write_to_file(self):
        """
        This function calls "gui_batch.py" with inputs values to write the batch file.
        """
        bt = BatchFile(self.batch_name_value, self.p_values, self.x_value, self.y_value, self.g_value, self.s_value,
                       self.z_value, self.wavelength_values, self.verbose_value, self.phyto_path, self.bottom_path,
                       self.nb_cpu, self.exec_path, self.report_parameter_value)
        bt.write_batch_to_file()

    def data_processing(self):
        """
        This function will separate data, from the file to display curves, and will put them in the good arrays.
        """
        the_file_name = str(self.result_file)
        the_file = open(the_file_name, 'r')

        lines = the_file.readlines()

        #We put all lines in an array and we put each cell of the line in a column.
        lines_array = []
        for line in lines:
            line = line.split('\t')  #Each time there is a tabulation, there is a new cell
            lines_array.append(line)

        labels_line = lines_array[0]
        cell_labels_line = 0  #Iterator on each cell of the line labels_line.
        flag = True  #Become FALSE when we find the word which separate data from wavelength values.
        try:
            while flag:  #While it is TRUE, so if the word doesn't match, it's an infinite loop,
                if labels_line[cell_labels_line] == '#wave length (nm) ->':
                    index = labels_line.index(labels_line[cell_labels_line])  #Find the index of the string searched.
                    flag = False
                else:
                    cell_labels_line += 1
        except IndexError:  #In case of an infinite loop.
            raise sys.exit("Warning : There is no value named 'wavelength' in the file used to plot curves. "
                           "So, I can't separate data to plot curves and data about tests linking with these curves.")

        self.information = []  #This array will contain the data displayed under the curves.
        data_wavelength = []  #This array will contain the data to plot curves.
        self.num_line = 0  #Iterator on each line of lines_array, the array containing data about information and wavelength.
        for line in lines_array:
            cell_line = 0  #Iterator on each cell of the line.
            self.information.append([])
            data_wavelength.append([])
            while cell_line < len(line):
                if cell_line < index:
                    self.information[self.num_line].append(line[cell_line])
                elif cell_line > index:
                    data_wavelength[self.num_line].append(line[cell_line])
                cell_line += 1
            self.num_line += 1

        #We transform wavelengths from strings to floats.
        line_wavelength = 0  #Iterator on each line of data_wavelength
        for row_data_wavelength in data_wavelength:
            row_data_wavelength = [float(item) for item in row_data_wavelength]
            data_wavelength[line_wavelength] = row_data_wavelength
            line_wavelength += 1

        self.wavelength = data_wavelength[0]  #The first line contains wavelength
        self.data_wanted = data_wavelength[1:]  #The others contain data useful to plot curves.

        the_file.close()

    def display_the_graphic(self, num_line, wavelength, data_wanted, information):
        """
        This function calls the class "MplCanvas" of "matplotlibwidgetFile.py" to plot results.
        """
        self.nb_case = num_line - 1  #This is the number of line, the number of test.

        self.graphic_slider(self.nb_case)

        self.mpl_canvas.update_fields(wavelength, data_wanted, self.slider_value)

        #Following if the checkbox is checked (show all curves) or not.
        if self.ui.show_all_curves.checkState() == 2:
            self.flag_curves = True
            self.mpl_canvas.display_graphic(self.flag_curves, self.ui)
            self.print_graphic_information(self.slider_value, information)
        else:
            self.flag_curves = False
            self.mpl_canvas.display_graphic(self.flag_curves, self.ui)
            self.print_graphic_information(self.slider_value, information)

    def display_the_graphic_connection(self):
        self.display_the_graphic(self.num_line, self.wavelength, self.data_wanted, self.information)

    def print_graphic_information(self, num_curve, information):
        """
        This function will display information about curves.
        Inputs ; num_curve ; the index of the curve's line that we have to display.
                 information ; the array which contains the information, of all curves, to display
        """
        """In this function, the best would to create labels each time we need to create one,
        following the number of labels in label_information.
        #self.essai = QtGui.QLabel(self.ui.tab)
        #self.essai.setGeometry(PyQt4.QtCore.QRect(870,650,111,16))
        #self.essai.setText("ESSAI")
        """

        label_information = information[0]
        data_information = information[1:]

        count_nb_label = 0  #Iterator on all labels of label_information
        nb_label = len(label_information)
        while count_nb_label <= nb_label:
            self.ui.column1_label.setText(label_information[0])
            self.ui.column2_label.setText(label_information[1])
            self.ui.column3_label.setText(label_information[2])
            self.ui.column4_label.setText(label_information[3])
            self.ui.column5_label.setText(label_information[4])
            self.ui.column6_label.setText(label_information[5])
            self.ui.column7_label.setText(label_information[6])
            self.ui.column8_label.setText(label_information[7])
            count_nb_label += 1

        line_of_data = 0  #Iterator on each line of data_information.
        while line_of_data < len(data_information):
            if line_of_data == num_curve:
                self.ui.column1_result.setText(data_information[line_of_data][0])
                self.ui.column2_result.setText(data_information[line_of_data][1])
                self.ui.column3_result.setText(data_information[line_of_data][2])
                self.ui.column4_result.setText(data_information[line_of_data][3])
                self.ui.column5_result.setText(data_information[line_of_data][4])
                self.ui.column6_result.setText(data_information[line_of_data][5])
                self.ui.column7_result.setText(data_information[line_of_data][6])
                self.ui.column8_result.setText(data_information[line_of_data][7])
            line_of_data += 1

    def graphic_slider(self, nb_case):
        """
        This function scales the slider for curves displayed.
        Input : The number of cases (curves).
        Return ; The slider's value.
        """
        #faire en sorte de ne pas creer taille slider a chaque fois, une fois au debut suffisant.
        self.ui.sens.setRange(0, int(nb_case - 1))
        self.slider_value = self.ui.sens.value()

        return self.slider_value

    def display_error_message(self):
        """
        This function displays an error message when a wrong value is typed.
        """
        self.ui.error_label.setScaledContents(True)  #Warning image
        self.ui.error_text_label.show()  #Warning message
        self.ui.error_text_label.setStyleSheet('color: red')

    def hide_error_message(self):
        """
        This function hides the error message when all values are correct.
        """
        self.ui.error_label.setScaledContents(False)  #Warning image
        self.ui.error_text_label.hide()  #Warning message

    def execute_planarrad(self):
        """
        This function executes planarRad using the batch file.
        """
        self.data()
        self.check_values()

        if self.nb_errors > 0:
            self.display_error_message()
        elif self.nb_errors == 0:
            self.hide_error_message()
            self.write_to_file()
            self.progress_bar()
            #os.chdir('../')
            #os.system('./planarrad.py -i /home/boulefi/PycharmProjects/planarradpy/inputs/batch_files/batch.txt')

    def progress_bar(self):
        """
        This function updates the progress bar.
        """
        self.step = 0
        self.ui.progressBar.reset()
        while self.step < 100:
            sleep(1)
            self.step += 1
            self.ui.progressBar.setValue(self.step)

    def cancel_planarrad(self):
        """
        This function cancels planarRad.
        """
        print("cancel_planarrad not done yet !")
        self.ui.progressBar.reset()

    def save_figure(self):
        """
        This function programs the button to save the figure displayed
        and save the graphic in a file in the current repository.
        """
        self.ui.graphic_widget.canvas.print_figure('Rrs.png')

    def prerequisite_actions(self):
        """
        This function do all required actions at the beginning when we run the GUI.
        """
        self.hide_error_message()
        self.data_processing()
        self.display_the_graphic(self.num_line, self.wavelength, self.data_wanted, self.information)
        self.ui.progressBar.reset()
        print("je suis appeller")

        # def context_menu(event):
        #     context_menu = QtGui.Menu()
        #     action1 = context_menu.addAction("ssss")
        #     context_menu.exec_(event.globalPos())

        #def onClick(self, e):
        #    if e.button == 3:
        #        pos = QtGui.QCursor().po()
        #        self.open_graphic_context_Menu(pos)

        #def open_graphic_context_Menu(self, pos):
        #    graphic_context_menu = QtGui.Menu()
        #    save_graphic_action = graphic_context_menu("sss")
        #    save_graphic_action = graphic_context_menu.exec_(self.tableWidget.mapFromGlobal(pos))


class Tab():
    NORMAL_MODE = 0
    REVERSE_MODE = 1


if __name__ == "__main__":
    FE = FormEvents()