__author__ = 'marrabld'

import os
print(os.getcwd())
os.chdir(os.path.join(os.getcwd(),  '../libplanarradpy'))

import libplanarradpy.planrad as pr

rt = pr.ReportTools()

#rep_dict = rt.read_pr_report('/home/marrabld/Desktop/rod_test/nadir/SAA262.39_SZA45.28_P0.01_X0.001_Y1.0_G0.01_S0.015_Z0.5/report.txt')

print(rt.write_batch_report('/home/marrabld/Desktop/rod_test/rod_Refl_BenthicMixture_1/', 'rrs'))