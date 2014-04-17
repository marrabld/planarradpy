#!/usr/bin/env python

#from library import *

class BatchFile():
    """
    Class description  ....
    """

    def __init__(self, p_values, x_value, y_value, g_value, s_value, z_value, waveL_values, verbose_value, phyto_path,
                 bottom_path, nb_cpu, exec_path):
        self.p_values = p_values
        self.x_value = x_value
        self.y_value = y_value
        self.g_value = g_value
        self.s_value = s_value
        self.z_value = z_value
        self.waveL_values = waveL_values
        self.verbose_value = verbose_value
        self.phyto_path = phyto_path
        self.bottom_path = bottom_path
        #self.cdom_file = cdom_file
        self.nb_cpu = nb_cpu
        self.exec_path = exec_path

    def write_batch_to_file(self):  # p_values, x_value, y_value, g_value, s_value, z_value, waveL_values, verbose_value, phyto_path, bottom_path, nb_cpu, exec_path, filename='batch.txt'):
        """
        description .....
        inputs ......
        returns ......
        """

        #----------#
        # The following is the file that is passed to planarradpy
        #----------#
        self.batch_file = open(str(filename), 'w')

        self.batch_file.write("""#----------------------------------------#
# Name of the batch run
#----------------------------------------#
batch_name = """)
        BatchFile.write("unity_test_4")
        BatchFile.write("""

#----------------------------------------#
# Bio-optical parameters list
#----------------------------------------#
p_list = """)
        BatchFile.write(str(self.p_values))
        BatchFile.write("""
x_list = """)
        BatchFile.write(self.x_value)
        BatchFile.write("""
y_list = """)
        BatchFile.write(self.y_value)
        BatchFile.write("""
g_list = """)
        BatchFile.write(g_value)
        BatchFile.write("""
s_list = """)
        BatchFile.write(s_value)
        BatchFile.write("""
z_list = """)
        BatchFile.write(str(z_value))
        BatchFile.write("""

#----------------------------------------#
# Wavelengths
# All IOPs are interpolated to these 
# Wavelengths
#----------------------------------------#
wavelengths = """)
        BatchFile.write(waveL_values)
        BatchFile.write("""

#----------------------------------------#
# Number of CPUs
# -1 means query the number of CPUs
#----------------------------------------#
num_cpus = """)
        BatchFile.write(nb_cpu)
        BatchFile.write("""

#----------------------------------------#
# Path of Planarrad
#----------------------------------------#
exec_path = """)
        BatchFile.write(exec_path)
        BatchFile.write("""

#----------------------------------------#
# Logging level
#----------------------------------------#
verbose = """)
        BatchFile.write(verbose_value)
        BatchFile.write("""

#----------------------------------------#
# File paths
# Using absolute paths
#----------------------------------------#
phytoplankton_absorption_file =""")
        BatchFile.write(phyto_path)
        BatchFile.write("""
bottom_reflectance_file = """)
        BatchFile.write(bottom_path)

        BatchFile.close()
