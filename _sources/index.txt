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

Example Use [command line]
--------------------------

python planarradpy.py -i <input_parameter_file>

Example input parameters file
-----------------------------

.. code-block:: python

  #----------------------------------------#
  # Name of the batch run
  #----------------------------------------#
  batch_name = P_VARY_HOPE_2

  #----------------------------------------#
  # Bio-optical parameters list
  #----------------------------------------#
  saa_list = 0.0
  sza_list = 130.0
  p_list = 0.01,0.05,0.1,0.2
  x_list = 0.01
  y_list = 1.0
  g_list = 0.1
  s_list = 0.015
  z_list = 30.0

  #----------------------------------------#
  # Wavelengths
  # All IOPs are interpolated to these
  # Wavelengths
  #----------------------------------------#
  wavelengths = 410.0,430.0,450.0,470.0,490.0,510.0,530.0,550.0,570.0,590.0,610.0,630.0,650.0,670.0,690.0,710.0,730.0

  #----------------------------------------#
  # Number of CPUs
  # -1 means query the number of CPUs
  #----------------------------------------#
  num_cpus = 1

  #----------------------------------------#
  # Path of Planarrad
  #----------------------------------------#
  exec_path = /home/marrabld/Apps/jude2_install/bin

  #----------------------------------------#
  # Logging level
  #----------------------------------------#
  verbose = 6

  #----------------------------------------#
  # File paths
  # Using absolute paths
  #----------------------------------------#
  phytoplankton_absorption_file =/home/marrabld/Projects/planarradpy/inputs/iop_files/a_phi.csv
  bottom_reflectance_file = /home/marrabld/Projects/hope_test/RodFiles/Refl_BenthicMixture_1_17Bands.txt

  #----------------------------------------#
  # Set the parameter to report
  #----------------------------------------#
  report_parameter = Rrs@6.0:135.0

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
