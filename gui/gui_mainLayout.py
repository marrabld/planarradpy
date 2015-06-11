#!/usr/bin/env python

import PyQt4
from PyQt4 import QtGui
import subprocess
from time import sleep
from timeit import Timer
from gui_About import *
import PyQt4.QtCore
import sys
import os
import multiprocessing
import re
import webbrowser
from PyQt4.QtGui import QContextMenuEvent, QMessageBox, QApplication, QWidget, QVBoxLayout
import subprocess
import signal
from threading import Thread

from PyQt4 import QtCore
import time

from gui_batch import BatchFile
from gui_Layout import *
import gui_matplotlibwidgetFile
from gui_log import *
from PyQt4.QtWebKit import *


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
        self.main_window.setFixedSize(1372, 890)
        self.graphic_widget = gui_matplotlibwidgetFile.matplotlibWidget()
        self.mpl_canvas = gui_matplotlibwidgetFile.MplCanvas()
        # self.ui.actionSave.setIcon(QtGui.QIcon('/home/marrabld/Projects/planarradpy/gui/icons/i_document-save.png'))
        # self.ui.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)

        # ==================================================#
        # The about window
        # ==================================================#
        self.aboutWindow = QtGui.QDialog()
        self.uiAbout = Ui_win_about()
        self.uiAbout.setupUi(self.aboutWindow)

        # ==================================================#
        # The log window
        # ==================================================#
        self.log_window = QtGui.QDialog()
        self.uiLog = Ui_win_log_reader()
        self.uiLog.setupUi(self.log_window)

        self.without_error = True
        self.slider_value = 0

        self.num_line = 0
        self.data_wanted = []
        self.wavelength = []
        self.information = []

        self.authorized_display = False
        self.ui.show_all_curves.setCheckState(2)
        self.ui.show_grid.setCheckState(2)
        self.p = None  # Variable for subprocess to run PlanarRad.
        # self.result_path = '../outputs'
        # self.result_file = os.path.join(self.result_path, "batch_report.txt")
        self.result_file = ''
        self.is_running = False
        self.table_widget = QtGui.QTableWidget()

        self.t = GuiThread(self, 100)  # Thread for the progress bar.
        self.n = 0

        # ----------------------------------------------------------------------------------------------#
        # The following permits to know how many CPU there is in the computer to list them in a comboBox.
        # ----------------------------------------------------------------------------------------------#
        self.cpu = multiprocessing.cpu_count()
        self.nb_cpu = self.ui.nb_cpu.addItem("-1")
        count_cpu = 1  # Iterator on the number of cpu.
        while count_cpu <= self.cpu:
            self.nb_cpu = self.ui.nb_cpu.addItem(str(count_cpu))
            count_cpu += 1

        self.prerequisite_actions()  # Initialise the GUI.

        # -------------------------------------------#
        # The following connects buttons to an action.
        # -------------------------------------------#

        self.ui.phyto_button.connect(self.ui.phyto_button, PyQt4.QtCore.SIGNAL('clicked()'),
                                     self.search_file_phytoplankton)
        self.ui.bottom_button.connect(self.ui.bottom_button, PyQt4.QtCore.SIGNAL('clicked()'), self.search_file_bottom)
        self.ui.exec_path_button.connect(self.ui.exec_path_button, PyQt4.QtCore.SIGNAL('clicked()'),
                                         self.search_directory_executive_path)

        self.ui.open_result_file_button.connect(self.ui.open_result_file_button, PyQt4.QtCore.SIGNAL('clicked()'),
                                                self.search_file_result)
        self.ui.sens.connect(self.ui.sens, QtCore.SIGNAL('valueChanged(int)'), self.display_the_graphic_connection)
        self.ui.show_all_curves.connect(self.ui.show_all_curves, QtCore.SIGNAL('stateChanged(int)'),
                                        self.display_the_graphic_connection)
        self.ui.show_grid.connect(self.ui.show_grid, QtCore.SIGNAL('stateChanged(int)'),
                                  self.display_the_graphic_connection)

        self.ui.actionSave.connect(self.ui.actionSave, QtCore.SIGNAL('triggered()'), self.save_figure)
        self.ui.actionSave_as.connect(self.ui.actionSave_as, QtCore.SIGNAL('triggered()'), self.save_figure_as)
        self.ui.actionThis_GUI.connect(self.ui.actionThis_GUI, QtCore.SIGNAL('triggered()'), self.open_about)
        self.ui.actionLog_file.connect(self.ui.actionLog_file, QtCore.SIGNAL('triggered()'), self.open_log_file)
        self.ui.actionDocumentation.connect(self.ui.actionDocumentation, QtCore.SIGNAL('triggered()'),
                                            self.open_documentation)

        self.ui.actionRun.connect(self.ui.actionRun, PyQt4.QtCore.SIGNAL('triggered()'), self.run)
        self.ui.actionOpen.connect(self.ui.actionOpen, PyQt4.QtCore.SIGNAL('triggered()'), self.search_file_result)
        self.ui.actionQuit.connect(self.ui.actionQuit, PyQt4.QtCore.SIGNAL('triggered()'), self.quit)

        self.ui.run.connect(self.ui.run, PyQt4.QtCore.SIGNAL('clicked()'), self.run)
        self.ui.cancel.connect(self.ui.cancel, PyQt4.QtCore.SIGNAL('clicked()'), self.cancel_planarrad)
        self.ui.quit.connect(self.ui.quit, PyQt4.QtCore.SIGNAL('clicked()'), self.quit)

        self.ui.graphic_widget.canvas.mpl_connect('button_release_event', self.click)
        self.ui.graphic_widget.canvas.mpl_connect('motion_notify_event', self.mouse_move)

        QtCore.QObject.connect(self.t, QtCore.SIGNAL("total(PyQt_PyObject)"), self.total)
        QtCore.QObject.connect(self.t, QtCore.SIGNAL("update()"), self.update)

        self.main_window.show()
        sys.exit(app.exec_())

    def data(self):
        """
        This function gets back data that the user typed.
        """
        self.batch_name_value = self.ui.batch_name_value.text()
        self.saa_values = self.ui.saa_values.text()
        self.sza_values = self.ui.sza_values.text()
        self.p_values = self.ui.p_values.text()
        self.x_value = self.ui.x_value.text()
        self.y_value = self.ui.y_value.text()
        self.g_value = self.ui.g_value.text()
        self.s_value = self.ui.s_value.text()
        self.z_value = self.ui.z_value.text()
        self.wavelength_values = self.ui.wavelength_values.text()
        self.verbose_value = self.ui.verbose_value.text()
        self.phytoplankton_path = self.ui.phyto_path.text()
        self.bottom_path = self.ui.bottom_path.text()
        self.executive_path = self.ui.exec_path.text()
        self.nb_cpu = self.ui.nb_cpu.currentText()
        self.report_parameter_value = str(self.ui.report_parameter_value.text())

    # -------------------------------------------------------------------------------#
    # These following functions display a fileDialog to search a file or a directory.
    # -------------------------------------------------------------------------------#

    def search_directory_executive_path(self):
        self.executive_file = self.file_dialog.getExistingDirectory(caption=str("Planarrad Directory"),
                                                                    directory="..")
        if not self.executive_file == '':
            self.ui.exec_path.setText(self.executive_file)

    def search_file_phytoplankton(self):
        self.phytoplankton_file = self.file_dialog.getOpenFileName(caption=str("Phytoplankton Absorption File"),
                                                                   directory="./inputs/iop_files")
        if not self.phytoplankton_file == '':
            self.ui.phytoplankton_path.setText(self.phytoplankton_file)

    def search_file_bottom(self):
        self.bottom_file = self.file_dialog.getOpenFileName(caption=str("Bottom Reflectance File"),
                                                            directory="./inputs/bottom_files")
        if not self.bottom_file == '':
            self.ui.bottom_path.setText(self.bottom_file)

    def search_file_result(self):
        """
        This function once the file found, display data's file and the graphic associated.
        """
        if self.ui.tabWidget.currentIndex() == TabWidget.NORMAL_MODE:
            self.result_file = self.file_dialog.getOpenFileName(caption=str("Open Report File"), directory="./outputs")
            if not self.result_file == '':
                self.ui.show_all_curves.setDisabled(False)
                self.ui.show_grid.setDisabled(False)
                self.data_processing()
                self.display_the_graphic(self.num_line, self.wavelength, self.data_wanted, self.information)
                self.authorized_display = True

    # ------------------------------------------------------------------------------#

    def check_values(self):
        """
        This function checks if there is no problem about values given.
        If there is a problem with a or some values, their label's color is changed to red,
        and call a function to display an error message.
        If there is no problem, their label, if it is necessary, is changed to grey (default color).
        """

        error_color = 'color: red'
        no_error_color = 'color: 0.75'  # light gray
        self.error_batch_name = False
        self.error_report_parameter = False
        self.error_saa_result = False
        self.error_sza_result = False
        self.error_p_result = False
        self.error_wavelength_result = False
        self.error_x_result = False
        self.error_y_result = False
        self.error_g_result = False
        self.error_s_result = False
        self.error_z_result = False
        self.error_verbose_result = False
        self.error_phytoplankton_path_result = False
        self.error_bottom_path_result = False
        self.error_executive_path_result = False

        """
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        No particular checking for paths!
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        """

        if self.ui.tabWidget.currentIndex() == TabWidget.NORMAL_MODE:

            check_num = '(.*)'  # Regular expression to use
            self.prog = re.compile(check_num)  # Analysis object creation
            batch_name_result = self.prog.search(
                self.batch_name_value)  # String retrieval thanks to the regular expression
            report_parameter_result = self.prog.search(self.report_parameter_value)
            try:
                if (self.ui.batch_name_value.text().isEmpty()) | (
                            batch_name_result.group() != self.ui.batch_name_value.text()):
                    self.ui.batch_name_label.setStyleSheet(error_color)
                    self.error_batch_name = True
                else:
                    self.ui.batch_name_label.setStyleSheet(no_error_color)
                    self.error_batch_name = False
            except AttributeError:
                self.ui.batch_name_label.setStyleSheet(error_color)
                self.error_batch_name = True
            try:
                if (self.ui.report_parameter_value.text().isEmpty()) | (
                            report_parameter_result.group() != self.ui.report_parameter_value.text()):
                    self.ui.report_parameter_label.setStyleSheet(error_color)
                    self.error_report_parameter = True
                else:
                    self.ui.report_parameter_label.setStyleSheet(no_error_color)
                    self.error_report_parameter = False
            except AttributeError:
                self.ui.report_parameter_label.setStyleSheet(error_color)
                self.error_report_parameter = True

            # -----------------------------------------------------------#
            # The following checks values separate by comas without space.
            # -----------------------------------------------------------#

            """
            Problem : The user can write just one letter or starts with a dot or finishes the list with a dot.
            """

            check_num_1 = '(^([0-9]+[.]?[0-9]*[,]?){0,}[^,])|(^([0-9]*[,]){1,}[^,])'  # Regular expression to use
            self.prog_1 = re.compile(check_num_1)  # Analysis object creation
            self.wavelength_values = str(self.wavelength_values).translate(None, ' ').strip(' ')
            # print(self.wavelength_values)
            p_result = self.prog_1.search(self.p_values)  # String retrieval thanks to the regular expression
            saa_result = self.prog_1.search(self.saa_values)
            sza_result = self.prog_1.search(self.sza_values)
            wavelength_result = self.prog_1.search(self.wavelength_values)
            # print(wavelength_result.group())

            try:

                if saa_result.group() != self.ui.saa_values.text():
                    self.ui.saa_label.setStyleSheet(error_color)
                    self.error_sza_result = True
                else:
                    self.ui.saa_label.setStyleSheet(no_error_color)
                    self.error_sza_result = False
            except AttributeError:
                self.ui.saa_label.setStyleSheet(error_color)
                self.error_sza_result = True
            try:
                if sza_result.group() != self.ui.sza_values.text():
                    self.ui.sza_label.setStyleSheet(error_color)
                    self.error_saa_result = True
                else:
                    self.ui.sza_label.setStyleSheet(no_error_color)
                    self.error_saa_result = False
            except AttributeError:
                self.ui.sza_label.setStyleSheet(error_color)
                self.error_saa_result = True
            try:
                if p_result.group() != self.ui.p_values.text():
                    self.ui.p_label.setStyleSheet(error_color)
                    self.error_p_result = True
                else:
                    self.ui.p_label.setStyleSheet(no_error_color)
                    self.error_p_result = False
            except AttributeError:
                self.ui.p_label.setStyleSheet(error_color)
                self.error_p_result = True
            try:
                if wavelength_result.group() != str(self.ui.wavelength_values.text()).translate(None, ' ').strip(' '):
                    self.ui.waveL_label.setStyleSheet(error_color)
                    self.error_wavelength_result = True
                else:
                    self.ui.waveL_label.setStyleSheet(no_error_color)
                    self.error_wavelength_result = False
            except AttributeError:
                self.ui.waveL_label.setStyleSheet(error_color)
                self.error_wavelength_result = True

            # ---------------------------------------------------#
            # The following checks values containing only numbers.
            # ---------------------------------------------------#
            check_num_2 = '(^([0-9]+[.]?[0-9]*[,]?){0,}[^,])|(^([0-9]+[,]){1,}[^,])'
            self.prog_2 = re.compile(check_num_2)
            x_result = self.prog_2.search(self.x_value)
            y_result = self.prog_2.search(self.y_value)
            g_result = self.prog_2.search(self.g_value)
            s_result = self.prog_2.search(self.s_value)
            z_result = self.prog_2.search(self.z_value)

            try:
                if x_result.group() != self.ui.x_value.text():
                    self.ui.particles_label.setStyleSheet(error_color)
                    self.ui.x_label.setStyleSheet(error_color)
                    self.error_x_result = True
                else:
                    self.ui.particles_label.setStyleSheet(no_error_color)
                    self.ui.x_label.setStyleSheet(no_error_color)
                    self.error_x_result = False
            except AttributeError:
                self.ui.particles_label.setStyleSheet(no_error_color)
                self.ui.x_label.setStyleSheet(error_color)
                self.error_x_result = True
            try:
                if y_result.group() != self.ui.y_value.text():
                    self.ui.particles_label.setStyleSheet(error_color)
                    self.ui.y_label.setStyleSheet(error_color)
                    self.error_y_result = True
                else:
                    self.ui.particles_label.setStyleSheet(no_error_color)
                    self.ui.y_label.setStyleSheet(no_error_color)
                    self.error_y_result = False
            except AttributeError:
                self.ui.particles_label.setStyleSheet(error_color)
                self.ui.y_label.setStyleSheet(error_color)
                self.error_y_result = True
            try:
                if g_result.group() != self.ui.g_value.text():
                    self.ui.organic_label.setStyleSheet(error_color)
                    self.ui.g_label.setStyleSheet(error_color)
                    self.error_g_result = True
                else:
                    self.ui.organic_label.setStyleSheet(no_error_color)
                    self.ui.g_label.setStyleSheet(no_error_color)
                    self.error_g_result = False
            except AttributeError:
                self.ui.organic_label.setStyleSheet(error_color)
                self.ui.g_label.setStyleSheet(error_color)
                self.error_g_result = True
            try:
                if s_result.group() != self.ui.s_value.text():
                    self.ui.organic_label.setStyleSheet(error_color)
                    self.ui.s_label.setStyleSheet(error_color)
                    self.error_s_result = True
                else:
                    self.ui.organic_label.setStyleSheet(no_error_color)
                    self.ui.s_label.setStyleSheet(no_error_color)
                    self.error_x_result = False
            except AttributeError:
                self.ui.organic_label.setStyleSheet(error_color)
                self.ui.s_label.setStyleSheet(error_color)
                self.error_x_result = True
            try:
                if z_result.group() != self.ui.z_value.text():
                    self.ui.z_label.setStyleSheet(error_color)
                    self.error_z_result = True
                else:
                    self.ui.z_label.setStyleSheet(no_error_color)
                    self.error_z_result = False
            except AttributeError:
                self.ui.z_label.setStyleSheet(error_color)
                self.error_z_result = True

            check_num_3 = '[1-6]+'
            self.prog_3 = re.compile(check_num_3)
            verbose_result = self.prog_3.search(self.verbose_value)

            try:
                if verbose_result.group() != self.ui.verbose_value.text():
                    self.ui.verbose_label.setStyleSheet(error_color)
                    self.error_verbose_result = True
                else:
                    self.ui.verbose_label.setStyleSheet(no_error_color)
                    self.error_verbose_result = False
            except AttributeError:
                self.ui.verbose_label.setStyleSheet(error_color)
                self.error_verbose_result = True

            # ------------------------------------------------#
            # The following checks values containing only path.
            # ------------------------------------------------#

            """
            #!!!!!!!!!!!!!!!!!!!!!!!!!!
            #Syntax test doesn't work ! ->  #check_num4 = '[/]([A-Za-z]+[/]?)+[A-Za-z]$'
            #!!!!!!!!!!!!!!!!!!!!!!!!!!
            """

            check_num_4 = '(.*)'  # Take all strings possible.
            self.prog_4 = re.compile(check_num_4)
            phytoplankton_path_result = self.prog_4.search(self.phytoplankton_path)
            bottom_path_result = self.prog_4.search(self.bottom_path)
            executive_path_result = self.prog_4.search(self.executive_path)

            try:
                if phytoplankton_path_result.group() != self.ui.phyto_path.text():
                    self.ui.phyto_label.setStyleSheet(error_color)
                    self.error_phytoplankton_path_result = True
                else:
                    self.ui.phyto_label.setStyleSheet(no_error_color)
                    self.error_phytoplankton_path_result = False
            except AttributeError:
                self.ui.phyto_label.setStyleSheet(error_color)
                self.error_phytoplankton_path_result = True
            try:
                if bottom_path_result.group() != self.ui.bottom_path.text():
                    self.ui.bottom_label.setStyleSheet(error_color)
                    self.error_bottom_path_result = True
                else:
                    self.ui.bottom_label.setStyleSheet(no_error_color)
                    self.error_bottom_path_result = False
            except AttributeError:
                self.ui.bottom_label.setStyleSheet(error_color)
                self.error_bottom_path_result = True
            try:
                if executive_path_result.group() != self.ui.exec_path.text():
                    self.ui.execPath_label.setStyleSheet(error_color)
                    self.error_executive_path_result = True
                else:
                    self.ui.execPath_label.setStyleSheet(no_error_color)
                    self.error_executive_path_result = False
            except AttributeError:
                self.ui.execPath_label.setStyleSheet(error_color)
                self.error_executive_path_result = True

        if (self.error_batch_name == True) | (self.error_report_parameter == True) | (
                    self.error_saa_result == True) | (self.error_sza_result == True) | (
                    self.error_p_result == True) | (self.error_wavelength_result == True) | (
                    self.error_x_result == True) | (self.error_y_result == True) | (
                    self.error_g_result == True) | (self.error_s_result == True) | (
                    self.error_z_result == True) | (self.error_verbose_result == True) | (
                    self.error_phytoplankton_path_result == True) | (self.error_bottom_path_result == True) | (
                    self.error_executive_path_result == True):
            self.without_error = False
        else:
            self.without_error = True

    def write_to_file(self):
        """
        This function calls "gui_batch.py" with inputs values to write the batch file.
        """
        bt = BatchFile(self.batch_name_value, self.p_values, self.x_value, self.y_value, self.g_value, self.s_value,
                       self.z_value, self.wavelength_values, self.verbose_value, self.phytoplankton_path,
                       self.bottom_path, self.nb_cpu, self.executive_path, self.saa_values,
                       self.sza_values, self.report_parameter_value)
        # bt.write_batch_to_file(str(self.batch_name_value + "_batch.txt"))
        bt.write_batch_to_file(str(self.batch_name_value + "_batch.txt"))

    def data_processing(self):
        """
        This function separates data, from the file to display curves, and will put them in the good arrays.
        """
        the_file_name = str(self.result_file)
        the_file = open(the_file_name, 'r')

        lines = the_file.readlines()

        # We put all lines in an array and we put each cell of the line in a column.
        lines_array = []
        for line in lines:
            line = line.split(',')  # Each time there is a tabulation, there is a new cell
            lines_array.append(line)

        labels_line = lines_array[0]
        cell_labels_line = 0  # Iterator on each cell of the line labels_line.
        flag = True  # Become FALSE when we find the word which separate data from wavelength values.

        try:
            while flag:  # While it is TRUE, so if the word doesn't match, it's an infinite loop,
                if "wave length (nm)" in labels_line[cell_labels_line]:
                    index = labels_line.index(labels_line[cell_labels_line])  # Find the index of the string searched.
                    flag = False
                else:
                    cell_labels_line += 1
        except IndexError:  # In case of an infinite loop.
            raise sys.exit("Warning : There is no value named 'wavelength' in the file used to plot curves. "
                           "So, I can't separate data to plot curves and data about tests linking with these curves.")

        self.information = []  # This array will contain the data displayed under the curves.
        data_wavelength = []  # This array will contain the data to plot curves.
        self.num_line = 0  # Iterator on each line of lines_array,
        # The array containing data about information and wavelength.
        for line in lines_array:
            cell_line = 0  # Iterator on each cell of the line.
            self.information.append([])
            data_wavelength.append([])
            while cell_line < len(line):
                if cell_line < index:
                    self.information[self.num_line].append(line[cell_line])
                elif cell_line > index:
                    data_wavelength[self.num_line].append(line[cell_line])
                cell_line += 1
            self.num_line += 1

        # We transform wavelengths from strings to floats.
        line_wavelength = 0  # Iterator on each line of data_wavelength
        for row_data_wavelength in data_wavelength:
            row_data_wavelength = [float(item.strip('\n').strip('\"')) for item in row_data_wavelength]
            data_wavelength[line_wavelength] = row_data_wavelength
            line_wavelength += 1

        self.wavelength = data_wavelength[0]  # The first line contains wavelength
        self.data_wanted = data_wavelength[1:]  # The others contain data useful to plot curves.

        the_file.close()

    def display_the_graphic(self, num_line, wavelength, data_wanted, information):
        """
        This function calls the class "MplCanvas" of "gui_matplotlibwidgetFile.py" to plot results.
        Inputs : num_line : The number of cases.
                 wavelength : The wavelengths.
                 data_wanted : The data for wavelengths.
                 information : The array which contains the information, of all curves to display.
        """
        self.nb_case = num_line - 1  # This is the number of line, the number of test.

        self.graphic_slider(self.nb_case)

        self.mpl_canvas.update_fields(wavelength, data_wanted, self.slider_value)

        # Following if the checkbox is checked "All curves" or not.
        if self.ui.show_grid.checkState() == 2:
            grid = True
        else:
            grid = False

        if self.ui.show_all_curves.checkState() == 2:
            self.flag_curves = True
            self.mpl_canvas.display_graphic(self.flag_curves, self.ui, grid)
            self.print_graphic_information(self.slider_value, information)
        else:
            self.flag_curves = False
            self.mpl_canvas.display_graphic(self.flag_curves, self.ui, grid)
            self.print_graphic_information(self.slider_value, information)

    def display_the_graphic_connection(self):
        """
        The following permits to attribute the function "display_the_graphic" to the slider.
        Because, to make a connection, we can not have parameters for the function, but "display_the_graphic" has some.
        """
        self.display_the_graphic(self.num_line, self.wavelength, self.data_wanted, self.information)

    def print_graphic_information(self, num_curve, information):
        """
        This function displays information about curves.
        Inputs ; num_curve ; The index of the curve's line that we have to display.
                 information ; The array which contains the information, of all curves to display.
        """
        """In this function, the best would to create labels each time we need to create one,
        following the number of labels in label_information.
        #self.essai = QtGui.QLabel(self.ui.tab)
        #self.essai.setGeometry(PyQt4.QtCore.QRect(870,650,111,16))
        #self.essai.setText("ESSAI")
        """

        label_information = information[0]
        data_information = information[1:]

        count_nb_label = 0  # Iterator on all labels of label_information
        nb_label = len(label_information)
        while count_nb_label <= nb_label:
            self.ui.column1_label.setText(label_information[0].strip('\"'))
            self.ui.column2_label.setText(label_information[1].strip('\"'))
            self.ui.column3_label.setText(label_information[2].strip('\"'))
            self.ui.column4_label.setText(label_information[3].strip('\"'))
            self.ui.column5_label.setText(label_information[4].strip('\"'))
            self.ui.column6_label.setText(label_information[5].strip('\"'))
            self.ui.column7_label.setText(label_information[6].strip('\"'))
            self.ui.column8_label.setText(label_information[7].strip('\"'))
            count_nb_label += 1

        line_of_data = 0  # Iterator on each line of data_information.
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
        Return ; The slider value.
        """

        """
        The slider range is created each time we call this function. Search to set its range just when it is necessary.
        """

        self.ui.sens.setDisabled(False)
        self.ui.sens.setRange(0, int(nb_case - 1))
        self.slider_value = self.ui.sens.value()

        return self.slider_value

    def display_error_message(self):
        """
        This function displays an error message when a wrong value is typed.
        """
        self.ui.error_label.setScaledContents(True)  # Warning image shown.
        self.ui.error_text_label.show()  # Warning message shown.
        self.ui.error_text_label.setStyleSheet('color: red')

    def hide_error_message(self):
        """
        This function hides the error message when all values are correct.
        """
        self.ui.error_label.setScaledContents(False)  # Warning image hiden.
        self.ui.error_text_label.hide()  # Warning message hiden.

    def run(self):
        """
        This function executes planarRad using the batch file.
        """

        """
        Error when planarRad start : /bin/sh: 1: ../planarrad.py: not found
        """
        print('Executing planarrad')
        # If we are not in the reverse_mode :
        if self.ui.tabWidget.currentIndex() == TabWidget.NORMAL_MODE:
            self.data()
            self.check_values()

            if self.without_error == False:
                self.display_error_message()
            elif self.without_error == True:
                self.is_running = True
                self.hide_error_message()
                self.write_to_file()
                os.chdir('./')
                self.progress_bar()
                this_dir = os.path.dirname(os.path.realpath(__file__)).rstrip('gui/')
                batch_file = os.path.join(this_dir, "inputs/batch_files/" + str(self.batch_name_value) + "_batch.txt")
                print(batch_file)
                self.p = subprocess.Popen(
                    ["./planarrad.py -i " + batch_file],
                    shell=True)
                if self.ui.progressBar.value() == 100:
                    self.display_the_graphic(self.num_line, self.wavelength, self.data_wanted, self.information)

    def update(self):
        """
        This function updates the progress bar.
        """

        """
        Because PlanarRad doesn't lunch, no file created and no possible update of the progress bar.
        """
        # print('update')
        # no_empty = 0
        # number_of_percent = 0
        # result_folders = (os.listdir('outputs/' + self.batch_name_value))
        # nb_folders = len(result_folders)
        # nb_checked_folder = 1
        # for folder in result_folders:
        #     if self.is_running == True:
        #         if os.path.isfile("outputs/" + self.batch_name_value + "/" + folder + "/report.txt") & (
        #                     self.is_running == True):
        #             nb_checked_folder += 1
        #             if (os.path.getsize("outputs/" + self.batch_name_value + "/" + folder + "/report.txt") > 0) & (
        #                         self.is_running == True):
        #                 no_empty += 1
        #     else:
        #         break
        #     number_of_percent = (no_empty * 100 ) / nb_checked_folder
        #     self.ui.progressBar.setValue(number_of_percent)

    def total(self, total):
        """
        This function sets the progress bar with its maximum.
        """
        self.ui.progressBar.setMaximum(total)

    def progress_bar(self):
        """
        This function starts the thread created for the progress bar. Without it, the GUI will freeze..
        """
        self.t.start()

    def cancel_planarrad(self):
        """
        This function cancels PlanarRad.
        """

        """
        This function needs to be tested. We don't know if she works.
        """

        if (self.is_running == True) & (self.ui.tabWidget.currentIndex() == TabWidget.NORMAL_MODE):
            cancel = QtGui.QMessageBox.question(self.ui.cancel, 'Cancel PlanarRad', "Are you sure to cancel ?",
                                                QtGui.QMessageBox.Yes,
                                                QtGui.QMessageBox.No)

            if cancel == QtGui.QMessageBox.Yes:
                self.is_running = False
                os.kill(self.p.pid, signal.SIGTERM)

                print("Necessary to check if cancel_planarrad works well !")
                self.ui.progressBar.reset()
            else:
                pass

    def quit(self):
        """
        This function quits PlanarRad, checking if PlanarRad is running before.
        """

        """
        Nothing programmed for displaying a message box when the user clicks on the window cross in order to quit.
        """

        if self.is_running == True:
            warning_planarrad_running = QtGui.QMessageBox.warning(self.ui.quit, 'Warning !',
                                                                  "PlanarRad is running. Stop it before quit !",
                                                                  QtGui.QMessageBox.Ok)

        else:
            quit = QtGui.QMessageBox.question(self.ui.quit, 'Quit PlanarRad', "Are you sure to quit ?",
                                              QtGui.QMessageBox.Yes,
                                              QtGui.QMessageBox.No)
            if quit == QtGui.QMessageBox.Yes:
                QtGui.qApp.quit()

    def save_figure(self):
        """
        This function programs the button to save the figure displayed
        and save it in a png file in the current repository.
        """

        """
        Increment the name of the figure in order to not erase the previous figure if the user use always this method.
        The png file is put in the "Artists_saved" file localized in the "planarradpy" folder.
        """

        default_name = 'Default_figure.png'
        self.ui.graphic_widget.canvas.print_figure(default_name)

        src = './' + default_name
        dst = './Artists_saved'
        os.system("mv" + " " + src + " " + dst)

    def save_figure_as(self):
        """
        This function programs the button to save the figure displayed
        and save it in a png file where you want / with the name you want thanks to a file dialog.
        """
        self.file_name = QtGui.QFileDialog.getSaveFileName()
        self.file_name = self.file_name + ".png"
        self.ui.graphic_widget.canvas.print_figure(str(self.file_name))

    def open_about(self):
        """
        This function opens the default browser and go on the web page about planarRad and its GUI.
        """
        self.aboutWindow.show()

    def open_log_file(self):
        """
        The following opens the log file of PlanarRad.
        """
        """
        TO DO.
        """
        # webbrowser.open('https://marrabld.github.io/planarradpy/')
        f = open(os.path.expanduser('~/.planarradpy/log/libplanarradpy.log'))
        # self.uiLog.textEdit.setText(str(f.readlines()))
        self.uiLog.textEdit.setPlainText(str(f.read()))
        self.log_window.show()

    def open_documentation(self):
        """
        The following opens the documentation file.
        """
        """
        TO DO.
        """
        # webbrowser.open('https://marrabld.github.io/planarradpy/')

        window = Window()
        html = QtCore.QUrl.fromLocalFile(os.path.join(os.getcwd(), './docs/_build/html/index.html')) #open('./docs/_build/html/index.html').read()
        #window.show()
        window.view.load(html)
        window.show()
        window.exec_()


    def prerequisite_actions(self):
        """
        This function does all required actions at the beginning when we run the GUI.
        """
        self.hide_error_message()

        self.ui.show_all_curves.setDisabled(True)
        self.ui.sens.setDisabled(True)
        self.ui.show_grid.setDisabled(True)

        pathname = os.path.dirname(sys.argv[0])
        path = os.path.abspath(pathname)
        # self.phytoplankton_path = self.ui.phyto_path.setText(path.replace('gui', 'inputs/iop_files'))
        # self.bottom_path = self.ui.bottom_path.setText(path.replace('gui', 'inputs/bottom_files'))
        # self.executive_path = self.ui.exec_path.setText("Decide where will be 'jude2_install/bin'")
        self.verbose_value = self.ui.verbose_value.setText("6")
        self.report_parameter_value = self.ui.report_parameter_value.setText("Rrs")

        self.ui.progressBar.reset()

    def closeEvent(self, event):
        """
        The following asks to the user if he is sure to quit the GUI.
        """
        reply = QtGui.QMessageBox.question(self, 'Quit PlanarRad',
                                           "Are you sure to quit?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def click(self, event):
        """
        This function intercepts the mouse's right click and its position.
        """
        if event.button == 3:
            if self.ui.tabWidget.currentIndex() == TabWidget.NORMAL_MODE:
                self.pos = QtGui.QCursor().pos()
                self.graphic_context_menu(self.pos)

    def mouse_move(self, event):
        """
        The following gets back coordinates of the mouse on the canvas.
        """
        if (self.ui.tabWidget.currentIndex() == TabWidget.NORMAL_MODE):
            self.posX = event.xdata
            self.posY = event.ydata

            self.graphic_target(self.posX, self.posY)

    def graphic_context_menu(self, pos):
        """
        This function will open a context menu on the graphic to save it.
        Inputs : pos : The position of the mouse cursor.
        """
        menu = QtGui.QMenu()
        self.actionSave_bis = menu.addAction("Save Figure")
        self.actionSave_as_bis = menu.addAction("Save Figure As ...")
        action = menu.exec_(self.table_widget.mapFromGlobal(pos))

        if action == self.actionSave_bis:
            self.save_figure()
        elif action == self.actionSave_as_bis:
            self.save_figure_as()

    def graphic_target(self, x, y):
        """
        The following update labels about mouse coordinates.
        """

        if self.authorized_display == True:
            try:
                self.display_the_graphic(self.num_line, self.wavelength, self.data_wanted, self.information)
                self.ui.mouse_coordinate.setText("(%0.3f, %0.3f)" % (x, y))
            except:
                pass


# fileName = self.dalecFileName=QtGui.QFileDialog.getSaveFileName(parent=None, caption='Save Figure',filter ='*.jpg *.bmp *.png *.pdf *.ps *.eps')

class GuiThread(QtCore.QThread):
    def __init__(self, parent, n):
        QtCore.QThread.__init__(self)
        self.n = n

    def run(self):
        self.emit(QtCore.SIGNAL("total(PyQt_PyObject)"), self.n)
        i = 0
        while i < self.n:
            if (time.time() % 1 == 0):
                i += 1
                # print str(i)
                self.emit(QtCore.SIGNAL("update()"))


class TabWidget():
    """
    This class is for the state machine about if we are in the first tab or in the second tab.
    """
    NORMAL_MODE = 0
    REVERSE_MODE = 1

class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.view = QWebView(self)

        layout = QVBoxLayout(self)
        layout.setMargin(0)
        layout.addWidget(self.view)

if __name__ == "__main__":
    FE = FormEvents()
