__author__ = 'marrabld'

import libplanarradpy.planrad as pr

a = pr.RunParameters()
a.write_run_parameters_to_file()
a.write_sky_params_to_file()
a.write_surf_params_to_file()
a.write_phase_params_to_file()
a.exec_path = '/home/boulefi/jude2_install/bin'
a.verbose = 2

b = pr.BatchRun(a)
b.run()