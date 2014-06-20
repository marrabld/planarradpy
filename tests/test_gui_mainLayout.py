#!/usr/bin/env python

__author__ = 'boulefi'

import sys
import os
import unittest

sys.path.append("../gui")
sys.path.append("../")


import gui
from gui.gui_mainLayout import *

class TestFormEvents(unittest.TestCase):
    """

    """
    def setUp(self):
        """

        """
        self.batch_name_value = "batch_name_test"
        self.p_values = "10, 11, 12"
        self.x_value = "1"
        self.y_value = "2"
        self.g_value = "3"
        self.s_value = "4"
        self.z_value = "5"
        self.wavelength_values = "6, 7, 8, 9"
        self.verbose_value = "2"
        self.phyto_path = "gui/file_phyto"
        self.bottom_path = "gui/file_bottom"
        self.exec_path = "gui/file_exec"
        self.nb_cpu = "1"
        self.report_parameter_value = "Rrs"
        self.saa_values = '10'
        self.sza_values = '11'

    def test_data(self):
        """
        The following will check if all data filled are get back well.
        """
        self.FE = gui.gui_mainLayout.FormEvents()
        self.ui = self.FE.ui

        # self.ui.batch_name_value.setText(self.batch_name_value)
        # self.ui.p_values.setText(self.p_values)
        # self.ui.x_value.setText(self.x_value)
        # self.ui.y_value.setText(self.y_value)
        # self.ui.g_value.setText(self.g_value)
        # self.ui.s_value.setText(self.s_value)
        # self.ui.z_value.setText(self.z_value)
        # self.ui.wavelength_values.setText(self.wavelength_values)
        # self.ui.verbose_value.setText(self.verbose_value)
        # self.ui.phyto_path.setText(self.phyto_path)
        # self.ui.bottom_path.setText(self.bottom_path)
        # self.ui.exec_path.setText(self.exec_path)
        # self.ui.nb_cpu.itemText(self.nb_cpu)
        # self.ui.report_parameter_value.setText(self.report_parameter_value)
        # self.ui.saa_values.text(self.saa_values)
        # self.ui.sza_values.text(self.sza_values)

        data = self.FE.data()

        self.assertEqual(self.batch_name_value, data.batch_name_value)
        self.assertEqual(self.p_values, data.p_values)
        self.assertEqual(self.x_value, data.x_value)
        self.assertEqual(self.y_value, data.y_value)
        self.assertEqual(self.g_value, data.g_value)
        self.assertEqual(self.s_value, data.s_value)
        self.assertEqual(self.z_value, data.z_value)
        self.assertEqual(self.wavelength_values, data.wavelength_values)
        self.assertEqual(self.verbose_value, data.verbose_value)
        self.assertEqual(self.phyto_path, data.phyto_path)
        self.assertEqual(self.bottom_path, data.bottom_path)
        self.assertEqual(self.exec_path, data.exec_path)
        self.assertEqual(self.nb_cpu, data.nb_cpu)
        self.assertEqual(self.report_parameter_value, data.report_parameter_value)
        self.assertEqual(self.saa_values, data.saa_values)
        self.assertEqual(self.sza_values, data.sza_values)

    def test_search_directory_exec_path(self):
        """
        The following will check if the fileDialog for the directory works well.
        """
        # self.ui = gui.gui_Layout.Ui_MainWindow()
        # self.FE.search_directory_exec_path()
        essai = 1

    def test_search_file_phyto(self):
        """
        The following will check if the the fileDialog for the file about phytoplankton works well.
        """
        test = 1

    def test_search_file_bottom(self):
        """
        The following will check if the the fileDialog for the file about the bottom works well.
        """
        test = 1

    def test_search_file_result(self):
        """

        """
        #self.ui = Ui_MainWindow()
        #self.ui.tabWidget.currentIndex(gui.gui_mainLayout.TabWidget.NORMAL_MODE)

    def test_check_values(self):
        """
        The following will check if all values given are the good case, are writen by the good way.
        """
        test = 1

    def test_write_to_file(self):
        """
        The following will checks if "gui_batch.py" is called with data
        and use one of its function to write the batch file.
        """
        test = 1

    def test_display_graphic(self):
        """
        The following will test if the results are plotted correctly.
        """
        test = 1

    def test_graphic_slider(nb_case):
        """
        The following will test if the slider under the graphic has the good values to display curves.
        """
        test = 1

    def test_display_error_message(self):
        """
        The following will check if the error message is well displayed.
        """
        test = 1

    def test_hide_error_message(self):
        """
        The following will check if the error message is well remove.
        """
        test = 1

    def test_execute_planarrad(self):
        """
        The following will check if planarRad is execute only if there is no errors.
        """
        test = 1

    def test_progress_bar(self):
        """
        The following will verify if the progress bar works and go through default values.
        """
        test = 1

    def test_cancel_planarrad(self):
        """
        The following will test if the cancel button stop planarRad.
        """
        test = 1

    def test_save_figure(self):
        """
        The following will check if the button to save the figure of the graphic works.
        """
        test = 1

def main():
    unittest.main()


if __name__ == '__main__':
    main()
