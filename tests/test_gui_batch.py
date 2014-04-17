__author__ = 'boulefi'

import sys
import scipy
import gui.gui_batch

sys.path.append("../..")
sys.path.append("../")

import unittest

class TestBatchFile(unittest.TestCase):
    def setUp(self):
        """


        """
        # Here you set up what you need for your tests.

        p_values = [1, 2, 3]
        # .... and all the others.

        self.gui_batch = gui.gui_batch.BatchFile(p_values, ....)


    def test_write_batch_to_file(self):
        """
        #  Describe the test!!
        """

        # Now we write the test!

        # You will need to Google how to do good tests in python.

        self.gui_batch.write_batch_to_file()

        #  Now you need to check the file is correct

        # at the least check that the file exists in the place you expect it to be.
        # Read the file back in and check the pvalues are the same??

        #  do this using assert methods.  <-- Google