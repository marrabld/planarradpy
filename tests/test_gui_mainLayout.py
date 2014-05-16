#!/usr/bin/env python

__author__ = 'boulefi'

import sys
import os

sys.path.append("../gui")
sys.path.append("../")

import unittest
import gui.gui_mainLayout

class TestFormEvents(unittest.TestCase):
    def SetUp(self):
        """

        """
        self.batch_name_value = "batch_name"
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


    def test_data(self):
        """
        The following will check if all data filled are get back well.
        """
        #envoyer les donnees dans les cases et les recuperer ensuite. Puis comparer le recuperer avec celles declarer.
        self.ui.batch_name.setText("batch_name")
        self.ui.p_values.setText("10, 11, 12")
        self.ui.x_value.setText("1")
        self.ui.y_value.setText("2")
        self.ui.g_value.setText("3")
        self.ui.s_value.setText("4")
        self.ui.z_value.setText("5")
        self.ui.wavelength_values.setText("6, 7, 8, 9")
        self.ui.verbose_value.setText("2")
        self.ui.phyto_path.setText("gui/file_phyto")
        self.ui.bottom_path.setText("gui/file_bottom")
        self.ui.exec_path.setText("gui/file_exec")
        self.ui.nb_cpu.itemText(0)
        self.ui.report_parameter_value.setText("Rrs")

        self.assertEqual(self.batch_name, self.gui_mainLayout.report_parameter_value)
        self.assertEqual(self.p_values, self.gui_mainLayout.p_values)
        self.assertEqual(self.x_value, self.gui_mainLayout.x_value)
        self.assertEqual(self.y_value, self.gui_mainLayout.y_value)
        self.assertEqual(self.g_value, self.gui_mainLayout.g_value)
        self.assertEqual(self.s_value, self.gui_mainLayout.s_value)
        self.assertEqual(self.z_value, self.gui_mainLayout.z_value)


    def test_search_directory_exec_path(self):
        """
        The following will check if the the fileDialog for the directory works well.
        """
        test = 1

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
