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


class TestBatchRun(unittest.TestCase):
    def setUp(self):
        rp = pr.RunParameters()
        rp.exec_path = '/home/boulefi/jude2_install/bin'
        rp.verbose = 6
        rp.num_cpus = 1
        self.br = pr.BatchRun(rp, 'unit_test')
        self.br.batch_parameters([1, 0.5], [2, 2.3], [3], [4], [5], [30, 35])


    def test_run(self):
        self.br.run()


        #def test_generate_directories(self):

        #    self.br.generate_directories(overwrite=False)


class TestBioOpticalParameters(unittest.TestCase):
    def setUp(self):
        wavelengths = [410.0, 430.0, 450.0, 470.0, 490.0, 510.0, 530.0, 550.0, 570.0, 590.0, 610.0, 630.0, 650.0, 670.0,
                       690.0, 710.0, 730.0]
        self.bio = pr.BioOpticalParameters(wavelengths)

    def test_build_bbp(self):
        x = 0.11
        y = 1

        self.bio.build_bbp(x, y)
        print(self.bio.b_bp)

    def test_build_a_cdom(self):
        g = 0.1
        s = 0.014

        self.bio.build_a_cdom(g, s)
        print(self.bio.a_cdom)


class TestReportTools(unittest.TestCase):
    def setUp(self):
        self.rt = pr.ReportTools()

    def test_read_pr_report(self):
        rep_dict = self.rt.read_pr_report('./test_data/report.txt')
        print(rep_dict['Rrs'])

    def test_write_batch_report(self):
        #print(self.rt.write_batch_report('../outputs/unit_test_5', 'Rrs'))
        print(self.rt.write_batch_report('../outputs/bug_test', 'Rrs'))
