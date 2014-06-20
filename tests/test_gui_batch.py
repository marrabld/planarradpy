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
        The following defines defaults values to check if the script transmit them well.
        """
        # Here you set up what you need for your tests.

        batch_name = 'unit_test_test_gui_batch'
        p_values = 0.01, 0.1
        x_value = 0.1
        y_value = 1.0
        g_value = 0.1
        s_value = 0.014
        z_value = 20
        wavelength_values = [410.0, 430.0, 450.0, 470.0, 490.0, 510.0, 530.0, 550.0, 570.0, 590.0, 610.0, 630.0, 650.0, 670.0, 690.0, 710.0, 730.0]
        verbose_value = 6
        phyto_path = '/home/boulefi/PycharmProjects/planarradpy/inputs/iop_files/a_phi.csv'
        bottom_path = '/home/boulefi/PycharmProjects/planarradpy/inputs/bottom_files/all_zeros17.txt'
        nb_cpu = -1
        exec_path = '/home/boulefi/jude2_install/bin'
        saa_values = 40
        sza_values = 90.0, 130.0
        report_parameter_value = 'Rrs'
        self.key_array = []
        self.val_array = []

        self.gui_batch = gui.gui_batch.BatchFile(batch_name, p_values, x_value, y_value, g_value, s_value, z_value,
                                                 wavelength_values, verbose_value, phyto_path, bottom_path, nb_cpu,
                                                 exec_path, saa_values, sza_values, report_parameter_value)

    def test_write_batch_to_file_open(self):
        """
        This test will check if the function 'write_batch_to_file' in '/gui/gui_batch' works
        and create the batch file as we want.
        """

        path = '../inputs/batch_files/batch_test_default.txt'

        self.gui_batch.write_batch_to_file()

        #-------------------------------------------------------------------------------#
        #The following will check that the file exists in the place you expect it to be
        #and I will check the file's size is correct
        #-------------------------------------------------------------------------------#
        if (os.path.isfile(path)) & (os.path.getsize(path) > 1000):
            res = True

        #------------------------------------------------------------------------------------#
        #The following will read the file back in and check the different values are the same.
        #------------------------------------------------------------------------------------#
        self.batch_file = open(path, 'r')
        self.assertFalse(self.batch_file.closed)

        for line in self.batch_file:
            if '=' in line:
                key, val = line.split('=')
                self.key_array.append(key)
                self.val_array.append(val)

        self.batch_file.close()
        self.assertTrue(self.batch_file.closed)


    def test_write_batch_to_file_batch_name(self):
        i = 0
        for key in self.key_array:
            self.val_array[i] = self.val_array[i].rstrip()
            if 'batch_name' in key:
                self.assertEqual(self.val_array[i], self.setUp.batch_name)
                break
            i += 1

    def test_write_batch_to_file_p_list(self):
        i = 0
        for key in self.key_array:
            self.val_array[i] = self.val_array[i].rstrip()
            if 'p_list' in key:
                val = map(float, self.val_array[i].split(','))
                self.assertSequenceEqual(val, self.gui_batch.p_values)
                break
            i += 1

    def test_write_batch_to_file_x_list(self):
        i = 0
        for key in self.key_array:
            self.val_array[i] = self.val_array[i].rstrip()
            if 'x_list' in key:
                val = float(self.val_array[i])
                self.assertEqual(val, self.gui_batch.x_value)
                break
            i += 1

    def test_write_batch_to_file_y_list(self):
        i = 0
        for key in self.key_array:
            self.val_array[i] = self.val_array[i].rstrip()
            if 'y_list' in key:
                val = float(self.val_array[i])
                self.assertEqual(val, self.gui_batch.y_value)
                break
            i += 1

    def test_write_batch_to_file_g_list(self):
        i = 0
        for key in self.key_array:
            self.val_array[i] = self.val_array[i].rstrip()
            if 'g_list' in key:
                val = float(self.val_array[i])
                self.assertEqual(val, self.gui_batch.g_value)
                break
            i += 1

    def test_write_batch_to_file_s_list(self):
        i = 0
        for key in self.key_array:
            self.val_array[i] = self.val_array[i].rstrip()
            if 's_list' in key:
                val = float(self.val_array[i])
                self.assertEqual(val, self.gui_batch.s_value)
                break
            i += 1

    def test_write_batch_to_file_z_list(self):
        i = 0
        for key in self.key_array:
            self.val_array[i] = self.val_array[i].rstrip()
            if 'z_list' in key:
                val = float(self.val_array[i])
                self.assertEqual(val, self.gui_batch.z_value)
                break
            i += 1

    def test_write_batch_to_file_wavelength(self):
        i = 0
        for key in self.key_array:
            self.val_array[i] = self.val_array[i].rstrip()
            if 'wavelengths' in key:
                val = map(float, self.val_array[i].split(','))
                self.assertListEqual(val, self.gui_batch.wavelength_values)
                break
            i += 1

    def test_write_batch_to_file_verbose(self):
        i = 0
        for key in self.key_array:
            self.val_array[i] = self.val_array[i].rstrip()
            if 'verbose' in key:
                val = float(self.val_array[i])
                self.assertEqual(val, self.gui_batch.verbose_value)
                break
            i += 1

    def test_write_batch_to_file_num_cpu(self):
        i = 0
        for key in self.key_array:
            self.val_array[i] = self.val_array[i].rstrip()
            if 'num_cpus' in key:
                val = float(self.val_array[i])
                self.assertEqual(val, self.gui_batch.nb_cpu)
                break
            i += 1

    def test_write_batch_to_file_exec_path(self):
        i = 0
        for key in self.key_array:
            self.val_array[i] = self.val_array[i].rstrip()
            if 'exec_path' in key:
                val = float(self.val_array[i])
                self.assertEqual(val, self.gui_batch.exec_path)
                break
            i += 1

    def test_write_batch_to_file_pytho_path(self):
        i = 0
        for key in self.key_array:
            self.val_array[i] = self.val_array[i].rstrip()
            if 'phytoplankton_absorption_file' in key:
                val = float(self.val_array[i])
                self.assertEqual(val, self.gui_batch.phyto_path)
                break
            i += 1

    def test_write_batch_to_file_bottom_path(self):
        i = 0
        for key in self.key_array:
            self.val_array[i] = self.val_array[i].rstrip()
            if 'bottom_reflectance_file' in key:
                val = float(self.val_array[i])
                self.assertEqual(val, self.gui_batch.bottom_path)
                break
            i += 1

    def test_write_batch_to_file_saa_values(self):
        i = 0
        for key in self.key_array:
            self.val_array[i] = self.val_array[i].rstrip()
            if 'saa_values' in key:
                val = float(self.val_array[i])
                self.assertEqual(val, self.gui_batch.saa_values)
                break
            i += 1

    def test_write_batch_to_file_sza_values(self):
        i = 0
        for key in self.key_array:
            self.val_array[i] = self.val_array[i].rstrip()
            if 'sza_values' in key:
                val = float(self.val_array[i])
                self.assertEqual(val, self.gui_batch.sza_values)
                break
            i += 1

    def test_write_batch_to_file_report_parameter(self):
        i = 0
        for key in self.key_array:
            self.val_array[i] = self.val_array[i].rstrip()
            if 'report_parameter' in key:
                val = float(self.val_array[i])
                self.assertEqual(val, self.gui_batch.report_parameter_value)
                break
            i += 1

def main():
    unittest.main()


if __name__ == '__main__':
    main()