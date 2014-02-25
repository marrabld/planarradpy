__author__ = 'marrabld'

import libplanarradpy.planrad as pr

a = pr.RunParameters()
a.write_run_parameters_to_file()
a.write_sky_params_to_file()