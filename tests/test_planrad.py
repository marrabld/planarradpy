__author__ = 'marrabld'
import sys

sys.path.append("../..")

import unittest
import libplanarradpy.planrad as pr


class TestRunParameters(unittest.TestCase):
    def setUp(self):
        self.rp = pr.RunParameters()

    def test_write_run_parameters_to_file(self):
        self.rp.write_run_parameters_to_file()

    def test_write_sky_parameters_to_file(self):
        self.rp.write_sky_params_to_file()

    def test_write_surf_params_to_file(self):
        self.rp.write_surf_params_to_file()

    def test_write_phase_params_to_file(self):
        self.rp.write_phase_params_to_file()


class TestBatchRun():
    def setUp(self):
        rp = pr.RunParameters()
        rp.exec_path = '/home/marrabld/Apps/planarRad/bin'
        rp.verbose = 6
        self.br = pr.BatchRun(rp)

    def test_run(self):
        self.br.run()
