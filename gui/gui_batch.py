#!/usr/bin/env python

import os


class BatchFile():
    """
    This class creates the batch file which will be used by planarRad.
    The constructor receives data that the user typed and transmitted thanks to files, concerning the environment.
    """

    def __init__(self, batch_name, p_values, x_value, y_value, g_value, s_value, z_value, wavelength_values,
                 verbose_value,
                 phyto_path, bottom_path, nb_cpu, exec_path, report_parameter_value):
        self.batch_name = batch_name
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
        self.nb_cpu = nb_cpu
        self.exec_path = exec_path
        self.report_parameter_value = report_parameter_value

    def write_batch_to_file(self, filename='batch_test_boulefi.txt'):
        """
        This function creates a new file if he doesn't exist already, moves it to 'inputs/batch_file' folder
        and writes data and comments associated to them.
        Inputs: batch_name :
                p_values :
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
                report_parameter :
        No return
        """

        #---------------------------------------------------------#
        # The following is the file which is passed to planarradpy.
        #---------------------------------------------------------#
        self.batch_file = open(str(filename), 'w')

        self.batch_file.write("""#----------------------------------------#
# Name of the batch run
#----------------------------------------#
batch_name = """)
        self.batch_file.write(str(self.batch_name))
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
        self.batch_file.write("""

#----------------------------------------#
# Set the parameter to report
#----------------------------------------#
report_parameter = """)
        self.batch_file.write(self.report_parameter_value)

        self.batch_file.write("""

""")

        self.batch_file.close()

        #-------------------------------------------------------------------#
        # The following is the action to move the file to the good directory.
        #-------------------------------------------------------------------#
        src = './' + filename
        dst = '../inputs/batch_files'
        os.system("mv" + " " + src + " " + dst)

