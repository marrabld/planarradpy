.. Planarradpy documentation master file, created by
   sphinx-quickstart on Wed May  7 14:37:51 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Planarradpy's documentation!
=======================================

.. warning:: Pre-Alpha  Not ready for any one to use except for testers!

Planarradpy
===========

Planarradpy is a tool written in python that can execute `Planarrad <http://www.planarrad.com/index.php?title=PlanarRad>`_

.. image:: ./images/1_main_screen.png

Example Use
-----------

python planarradpy.py -i <input_parameter_file>

Example input parameters file
-----------------------------

.. code-block:: python

#----------------------------------------#
# Give the batch run a name
#----------------------------------------#
batch_name = bug_test

#----------------------------------------#
# Set the Bio-optical parameters list
#----------------------------------------#
saa_list = 130.0
sza_list = 40
p_list = 0.01, 0.1, 1, 10
x_list = 0.1
y_list = 1.0
g_list = 0.1
s_list = 0.014
z_list = 10

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
num_cpus = 2

#----------------------------------------#
# Set the path of Planarrad
#----------------------------------------#
exec_path = /home/marrabld/Apps/planarRad/bin

#----------------------------------------#
# Set the logging level
#----------------------------------------#
verbose = 1

#----------------------------------------#
# Set the file paths
# Use absolute paths
#----------------------------------------#
phytoplankton_absorption_file = /home/marrabld/projects/planarradpy/inputs/iop_files/a_phi.csv
bottom_reflectance_file = /home/marrabld/projects/planarradpy/inputs/bottom_files/ger_sand17.txt

#--------------------------------------------------#
# Set the parameter to report
#--------------------------------------------------#
report_parameter = Rrs

Source code
-----------

`Planarradpy <https://github.com/marrabld/planarradpy>`_


Contents:
---------

.. toctree::
   :maxdepth: 2

.. automodule:: libplanarradpy
   :members:

.. automodule:: libplanarradpy.planrad
   :members:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

