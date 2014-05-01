#!/usr/bin/env python

__author__ = 'boulefi'

import sys
import scipy
import os

sys.path.append("../gui")
sys.path.append("../")

import unittest
import gui.gui_batch


class TestBatchFile(unittest.TestCase):
    def setUp(self):
        """
        The following defines default values to check if the script transmit them well.
        """
        # Here you set up what you need for your tests.

        p_values = [0.5, 1, 5, 10]
        x_value = 2
        y_value = 3
        g_value = 4
        s_value = 4
        z_value = 2
        wavelength_values = [410.0, 430.0, 450.0, 470.0, 490.0, 510.0, 530.0, 550.0, 570.0, 590.0, 610.0, 630.0, 650.0,
                             670.0, 690.0, 710.0, 730.0]
        verbose_value = 6
        phyto_path = '/home/boulefi/PycharmProjects/planarradpy/inputs/iop_files/a_phi.csv'
        bottom_path = '/home/boulefi/PycharmProjects/planarradpy/inputs/bottom_files/all_zeros17.txt'
        nb_cpu = -1
        exec_path = '/home/boulefi/jude2_install/bin'

        self.gui_batch = gui.gui_batch.BatchFile(p_values, x_value, y_value, g_value, s_value, z_value,
                                                 wavelength_values, verbose_value, phyto_path, bottom_path, nb_cpu, exec_path)

    def test_write_batch_to_file(self):
        """
        This test will check if the function 'write_batch_to_file' in '/gui/gui_batch' works
        and create the batch file as we want.
        """

        path = '../inputs/batch_files/batch.txt'

        self.gui_batch.write_batch_to_file()

        #-------------------------------------------------------------------------------#
        #The following will check that the file exists in the place you expect it to be
        #and I will check the file is correct
        #-------------------------------------------------------------------------------#
        if (os.path.isfile(path)) & (os.path.getsize(path) > 1000):
            res = True

        #------------------------------------------------------------------------------------#
        #The following will read the file back in and check the different values are the same.
        #-------------------------------------------------------------------------------------#
        self.batch_file = open(path, 'r')

        items = ['p_list', 'x_list', 'y_list', 'g_list', 's_list', 'z_list', 'num_cpus', 'verbose']
        for line in self.batch_file:
            if '=' in line:
                key, val = line.split('= ')
                val = val.rstrip()
                """
                if key in items:
                    val = map(float, val.split(','))
                    self.assertEqual(val, self.gui_batch.items)
                """
                if 'p_list' in key:
                    val = map(float, val.split(','))
                    self.assertSequenceEqual(val, self.gui_batch.p_values)
                    #check the values
                elif 'x_list' in key:
                    val = float(val)
                    self.assertEqual(val, self.gui_batch.x_value)
                elif 'y_list' in key:
                    val = float(val)
                    self.assertEqual(val, self.gui_batch.y_value)
                elif 'g_list' in key:
                    val = float(val)
                    self.assertEqual(val, self.gui_batch.g_value)
                elif 's_list' in key:
                    val = float(val)
                    self.assertEqual(val, self.gui_batch.s_value)
                elif 'z_list' in key:
                    val = float(val)
                    self.assertEqual(val, self.gui_batch.z_value)
                elif 'wavelengths' in key:
                    val = map(float, val.split(','))
                    self.assertListEqual(val, self.gui_batch.waveL_values)
                elif 'verbose' in key:
                    val = float(val)
                    self.assertEqual(val, self.gui_batch.verbose_value)
                elif 'num_cpus' in key:
                    val = float(val)
                    self.assertEqual(val, self.gui_batch.nb_cpu)
                elif 'exec_path' in key:
                    self.assertEqual(val, self.gui_batch.exec_path)
                elif 'phytoplankton_absorption_file' in key:
                    self.assertEqual(val, self.gui_batch.phyto_path)
                elif 'bottom_reflectance_file' in key:
                    self.assertEqual(val, self.gui_batch.bottom_path)
                    # do something
            else:
                # don't
                continue

        self.batch_file.close()


def main():
    unittest.main()


if __name__ == '__main__':
    main()