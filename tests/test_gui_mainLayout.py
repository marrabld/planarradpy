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
        test = 1

    def test_data(self):
        """
        The foolowing will check if all data filled are get back well.
        """
        test = 1

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
        THe following will checks if "gui_batch.py" is called with data
        and use one ofits function to write the batch file.
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