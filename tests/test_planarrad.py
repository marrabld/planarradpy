__author__ = 'marrabld'

import sys
import scipy

sys.path.append("../..")
sys.path.append("../")

import unittest
import libplanarradpy.planrad as pr


class TestPlanarrad(unittest.TestCase):
    def setUp(self):
        pass

    def test_main(self):
        pass

    def test_parse_input_file(self):
        input_file = '../inputs/batch_files/batch.txt'
        input_parameters = pr.FileTools.read_param_file_to_dict(input_file)
        pr.lg.info(input_parameters)

        rp = pr.RunParameters()
        rp.exec_path = input_parameters['exec_path']#'/home/marrabld/Apps/planarRad/bin'
        rp.verbose = input_parameters['verbose']
        rp.num_cpus = int(input_parameters['num_cpus'])
        rp.phytoplankton_absorption_file = input_parameters['phytoplankton_absorption_file']
        rp.bottom_reflectance_file = input_parameters['phytoplankton_absorption_file']

        p_list = pr.HelperMethods.string_to_float_list(input_parameters['p_list'])  # map(float, input_parameters['p_list'])
        x_list = pr.HelperMethods.string_to_float_list(input_parameters['x_list'])
        y_list = pr.HelperMethods.string_to_float_list(input_parameters['y_list'])
        g_list = pr.HelperMethods.string_to_float_list(input_parameters['g_list'])
        s_list = pr.HelperMethods.string_to_float_list(input_parameters['s_list'])
        z_list = pr.HelperMethods.string_to_float_list(input_parameters['z_list'])

        batch_name = input_parameters['batch_name']

        br = pr.BatchRun(rp, batch_name)
        br.batch_parameters(p_list,
                            x_list,
                            y_list,
                            g_list,
                            s_list,
                            z_list)

        br.generate_directories()
        #br.run()

