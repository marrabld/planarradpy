#!/usr/bin/env python

import os


class BatchFile():
    """
    This class create the batch file which will be used by Planarrad.
    The constructor receive data that the user typed and transmitted thanks to files, concerning the environment.
    """

    def __init__(self, p_values, x_value, y_value, g_value, s_value, z_value, wavelength_values, verbose_value, phyto_path,
                 bottom_path, nb_cpu, exec_path):
        self.p_values = p_values
        self.x_value = x_value
        self.y_value = y_value
        self.g_value = g_value
        self.s_value = s_value
        self.z_value = z_value
        self.wavelength_values = wavelength_values
        self.verbose_value = verbose_value
        self.phyto_path = phyto_path
        self.bottom_path = bottom_path
        #self.cdom_file = cdom_file
        self.nb_cpu = nb_cpu
        self.exec_path = exec_path

    def write_batch_to_file(self, filename='batch_test.txt'):  # p_values, x_value, y_value, g_value, s_value, z_value, wavelength_values, verbose_value, phyto_path, bottom_path, nb_cpu, exec_path):
        """
        This function create a new file if he doesn't exist already, move it to 'inputs/batch_file' folder and write data and comments associated to them.
        Inputs: p_values :
                x_value :
                y_value :
                g_value :
                s_value :
                waveL_values :
                verbose_value :
                phyto_path :
                bottom_path :
                nb_cpu :
                exec_path :
        No return
        """

        #--------------------------------------------------------#
        # The following is the file that is passed to planarradpy.
        #--------------------------------------------------------#
        self.batch_file = open(str(filename), 'w')

        self.batch_file.write("""#----------------------------------------#
# Name of the batch run
#----------------------------------------#
batch_name = """)
        self.batch_file.write("unity_test_4")
        self.batch_file.write("""

#----------------------------------------#
# Bio-optical parameters list
#----------------------------------------#
p_list = """)
        self.batch_file.write(str(self.p_values))
        self.batch_file.write("""
x_list = """)
        self.batch_file.write(str(self.x_value))
        self.batch_file.write("""
y_list = """)
        self.batch_file.write(str(self.y_value))
        self.batch_file.write("""
g_list = """)
        self.batch_file.write(str(self.g_value))
        self.batch_file.write("""
s_list = """)
        self.batch_file.write(str(self.s_value))
        self.batch_file.write("""
z_list = """)
        self.batch_file.write(str(self.z_value))
        self.batch_file.write("""

#----------------------------------------#
# Wavelengths
# All IOPs are interpolated to these 
# Wavelengths
#----------------------------------------#
wavelengths = """)
        self.batch_file.write(str(self.wavelength_values))
        self.batch_file.write("""

#----------------------------------------#
# Number of CPUs
# -1 means query the number of CPUs
#----------------------------------------#
num_cpus = """)
        self.batch_file.write(str(self.nb_cpu))
        self.batch_file.write("""

#----------------------------------------#
# Path of Planarrad
#----------------------------------------#
exec_path = """)
        self.batch_file.write(self.exec_path)
        self.batch_file.write("""

#----------------------------------------#
# Logging level
#----------------------------------------#
verbose = """)
        self.batch_file.write(str(self.verbose_value))
        self.batch_file.write("""

#----------------------------------------#
# File paths
# Using absolute paths
#----------------------------------------#
phytoplankton_absorption_file =""")
        self.batch_file.write(self.phyto_path)
        self.batch_file.write("""
bottom_reflectance_file = """)
        self.batch_file.write(self.bottom_path)

        self.batch_file.close()

        #--------------------------------------------------------#
        # The following is to move the file to the good directory.
        #--------------------------------------------------------#
        src = './'+filename
        dst = '../inputs/batch_files'
        os.system("mv"+ " " + src + " " + dst)

