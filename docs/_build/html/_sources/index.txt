.. Planarradpy documentation master file, created by
   sphinx-quickstart on Wed May  7 14:37:51 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Planarradpy's documentation!
=======================================

Planarradpy
===========

Planarradpy is a tool written in python that can execute Planarrad

Example Use
===========

python planarradpy.py -i <input_parameter_file>

Example input parameters file
-----------------------------

.. code-block:: python

    #----------------------------------------#
    # Give the batch run a name
    #----------------------------------------#
    batch_name = unit_test_3

    #----------------------------------------#
    # Set the Bio-optical parameters list
    #----------------------------------------#
    p_list = 0.5, 1, 1.5, 2, 3, 4, 5, 6 , 7, 8
    x_list = 2
    y_list = 3
    g_list = 4
    s_list = 4
    z_list = 2, 3, 4, 5, 0.5, 1, 1.5, 2, 3, 4, 5, 6 , 7, 8

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
    bottom_reflectance_file = /home/marrabld/projects/planarradpy/inputs/bottom_files/all_zeros17.txt


Contents:

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

