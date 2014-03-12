planarradpy
===========

Python batch scripts for running [planarrad] (http://www.planarrad.com/index.php?title=PlanarRad)


Example use:
------------

./planarrad.py -i /home/marrabld/projects/planarradpy/inputs/batch_files/batch.txt 


Batch file example:
-------------------
```bash
#----------------------------------------#
# Give the batch run a name
#----------------------------------------#
batch_name = unit_test_3

#----------------------------------------#
# Set the Bio-optical parameters list
#----------------------------------------#
p_list = 0.5, 1, 1.5, 2, 3
x_list = 2
y_list = 3
g_list = 4
s_list = 4
z_list = 5, 10, 20, 50 

#----------------------------------------#
# Wavelengths must be defined
# All IOPs are interpolated to these 
# Wavelengths
#----------------------------------------#
wavelengths = 410.0, 430.0, 450.0, 470.0, 490.0, 510.0, 530.0, 550.0, 570.0, 590.0, 610.0, 630.0, 650.0, 670.0, 690.0, 710.0, 730.0

#----------------------------------------#
# Choose the number of CPUs
# -1 means query the number of CPUs
#----------------------------------------#
num_cpus = -1

#----------------------------------------#
# Set the path of Planarrad
#----------------------------------------#
exec_path = /home/marrabld/Apps/planarRad/bin

#----------------------------------------#
# Set the logging level
#----------------------------------------#
verbose = 6

#----------------------------------------#
# Set the file paths
# Use absolute paths
#----------------------------------------#
phytoplankton_absorption_file = /home/marrabld/projects/planarradpy/inputs/iop_files/a_phi.csv
bottom_reflectance_file = /home/marrabld/projects/planarradpy/inputs/iop_files/all_zeros17.txt
```
