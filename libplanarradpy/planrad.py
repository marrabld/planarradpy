from numpy import loadtxt
import os
import sys
import time

sys.path.append("../..")

import logger as log
import scipy
import libplanarradpy
import libplanarradpy.state
import csv
from multiprocessing import Process

__author__ = 'marrabld'

DEBUG_LEVEL = libplanarradpy.state.State().debug
lg = log.logger
lg.setLevel(DEBUG_LEVEL)


class RunParameters():
    def __init__(self):
        lg.info('============')
        lg.info('Initialising')
        lg.info('============')

        self.wavelengths = scipy.linspace(410, 730, 17)
        #print(self.wavelengths.shape)
        self.a = scipy.zeros_like(self.wavelengths)  # total absorption
        self.a_phi = scipy.zeros_like(self.wavelengths)
        self.a_water = scipy.zeros_like(self.wavelengths)
        self.a_cdom = scipy.zeros_like(self.wavelengths)  # CDOM absorption
        self.bb = scipy.zeros_like(self.wavelengths)  # backscatter
        self.bbp = scipy.zeros_like(self.wavelengths)  # particulate scatter
        self.b_water = scipy.zeros_like(self.wavelengths)
        self.b = scipy.zeros_like(self.wavelengths)  # scatter
        self.c = scipy.zeros_like(self.wavelengths)  # attenuation
        self.iop_backscatter_proportion_list = ''  #scipy.asarray([])
        self.depth = 5
        self.theta_points = [0, 5, 15, 25, 35, 45, 55, 65, 75, 85, 90, 95, 105, 115, 125, 135, 145, 155, 165, 175, 180]
        self.input_path = os.path.abspath(os.path.join('..', 'inputs'))
        self.output_path = os.path.abspath(os.path.join('..', 'outputs'))
        self.pure_water_absorption_file = os.path.abspath(
            os.path.join(os.path.join(self.input_path, 'iop_files'), 'a_water.csv'))
        self.pure_water_scattering_file = os.path.abspath(
            os.path.join(os.path.join(self.input_path, 'iop_files'), 'b_water.csv'))
        self.phytoplankton_absorption_file = os.path.abspath(
            os.path.join(os.path.join(self.input_path, 'iop_files'), 'a_phi.csv'))
        self.project_file = os.path.abspath(os.path.join(os.path.join(self.input_path, 'batch_files'), 'batch_run.txt'))
        self.attenuation_file = os.path.abspath(
            os.path.join(os.path.join(self.input_path, 'iop_files'), 'bz052_c17.txt'))
        self.absorption_file = os.path.abspath(os.path.join(os.path.join(self.input_path, 'iop_files'), 'batch_a.txt'))
        self.scattering_file = os.path.abspath(
            os.path.join(os.path.join(self.input_path, 'iop_files'), 'bz052_b17.txt'))
        self.sky_azimuth = 50
        self.sky_zenith = 45
        self.euler_steps_per_optical_depth = 100
        self.integrator = 'runga4'
        self.iop_type = 'petzold'
        self.sample_point_distance = 1
        self.sample_point_delta_distance = 0.01
        self.bottom_reflectance_file = os.path.abspath(
            os.path.join(os.path.join(self.input_path, 'bottom_files'), 'ger_sand17.txt'))
        self.sky_type = 'hlideal'
        self.sky_c = 1
        self.sky_r_dif = 0.3
        self.iface_type = 'coxmunk'
        self.ds_name = 'HL Standard'
        self.vn = 18
        self.hn = 24
        self.num_bands = self.wavelengths.shape[0]
        self.sky_state = 'clear'
        self.surf_state = 'flat'
        self.ds_code = 'HL_' + str(self.vn) + 'x' + str(self.hn)
        self.partition = 'sphere'
        self.sky_file = os.path.abspath(
            os.path.join(os.path.join(self.input_path, 'sky_files'),
                         'sky_' + self.sky_state + '_z' + str(self.sky_zenith) + '_a' + str(
                             self.sky_azimuth) + '_' + str(
                             self.num_bands) + '_' + self.ds_code))
        self.iface_0_ri = 1.34
        self.iface_1_ri = 1.00
        self.bound_bottom_reflec_diffuse_data = 0
        self.sky_sub_quad_count = '1E6'
        self.iface_sub_quad_count = '1E6'
        self.pf_sub_quad_count = '1E4'
        self.midpoint_steps_per_optical_depth = 50
        self.runga4_steps_per_optical_depth = 20
        self.runga4adap_min_steps_per_optical_depth = 5
        self.runga4adap_max_steps_per_optical_depth = 40
        self.runga4adap_min_error = 0.01
        self.runga4adap_max_error = 0.1
        self.ld_b_image_save_file = os.path.join(self.output_path, 'image_Ld_b.ppm')
        self.ld_b_image_sens_k = 0.0008
        self.ld_b_save_file = os.path.join(self.output_path, 'Ld_b_data')
        self.verbose = 6
        self.num_cpus = -1
        self.wind_speed = 5
        self.crosswind_vertices = 100
        self.upwind_vertices = 100
        self.surface_size = 1
        self.surface_radius = 0.5
        self.target_size = 0.2
        self.rays_per_quad = 10
        self.surface_count = 200
        self.azimuthally_average = 'yes'
        self.water_surface_file = os.path.abspath(
            os.path.join(os.path.join(self.input_path, 'surface_files'),
                         'sf_' + self.iface_type + '_w' + str(self.wind_speed) + '_r' + str(
                             self.rays_per_quad) + '_s' + \
                         str(self.surface_count) + '_' + self.azimuthally_average + '_mono_' + self.ds_code))
        self.wind_direc = 0
        self.crosswind_vertices = 100
        self.model_eqn = 'clear'
        self.phase_function_file = os.path.abspath(
            os.path.join(os.path.join(self.input_path, 'phase_files'), 'pf_' + self.iop_type + '_mono_' + self.ds_code))
        self.exec_path = '/usr/bin/jude_test/bin/'
        self.report_file = os.path.join(self.output_path, 'batch_run_report.txt\n')

    def write_run_parameters_to_file(self):
        """

        """

        lg.info('Writing Inputs to file : ' + self.project_file)

        # First update the file names in case we changed the file values.  the file name includes the file values
        #self.updateFileNames()

        f = open(self.project_file, 'w')

        f.write('name = ' + self.project_file + '\n')
        f.write('band_count = ' + str(len(self.wavelengths)) + '\n')
        f.write('bs_name = ' + str(len(self.wavelengths)) + ' Bands (' + str(self.wavelengths[0]) + '-' + str(
            self.wavelengths[len(self.wavelengths) - 1]) + ' nm) \n')
        f.write('bs_code = ' + str(len(self.wavelengths)) + '\n')
        f.write('band_centres_data = ')
        f.write(",".join([str(wave) for wave in self.wavelengths]) + '\n')
        # f.write('band_widths_data = ')
        # for i in range(0, len(self.wavelengths) - 1):  # Find better way to do this!
        #     width = self.wavelengths[i + 1] - self.wavelengths[i]
        #     f.write(str(width))
        #     if i < len(self.wavelengths) - 2:
        #         f.write(',')
        f.write('\n')
        f.write('ds_name = ' + self.ds_name + '\n')
        f.write('ds_code = ' + self.ds_code + '\n')
        f.write('partition = ' + self.partition + '\n')
        f.write('vn = ' + str(self.vn) + '\n')
        f.write('hn = ' + str(self.hn) + '\n')
        f.write('theta_points=')
        f.write(",".join([str(theta) for theta in self.theta_points]) + '\n')
        f.write('depth = ' + str(self.depth) + '\n')
        f.write('sample_point_distance = ' + str(self.sample_point_distance) + '\n')
        f.write('sample_point_delta_distance = ' + str(self.sample_point_delta_distance) + '\n')
        f.write('\n')
        f.write('sky_fp = ' + self.sky_file + '\n')  # need to create these files from sky tool
        f.write('water_surface_fp =' + self.water_surface_file)
        f.write('\n')
        f.write('atten_fp = ' + self.attenuation_file + '\n')
        f.write('scat_fp = ' + self.scattering_file + '\n')
        f.write('pf_fp = ' + self.phase_function_file + '\n')
        f.write('bottom_reflec_diffuse_fp = ' + self.bottom_reflectance_file + '\n')
        f.write('sky_type = ' + self.sky_type + '\n')
        f.write('sky_azimuth = ' + str(self.sky_azimuth) + '\n')
        f.write('sky_zenith = ' + str(self.sky_zenith) + '\n')
        f.write('sky_C = ' + str(self.sky_c) + '\n')
        f.write('sky_rdif = ' + str(self.sky_r_dif) + '\n')
        f.write('iface_type = ' + self.iface_type + '\n')
        f.write('iface_refrac_index_0 = ' + str(self.iface_0_ri) + '\n')
        f.write('iface_refrac_index_1 = ' + str(self.iface_1_ri) + '\n')
        #        f.write('iop_atten_data = 1\n')
        #        f.write('iop_absorp_data = 0\n')
        f.write('iop_type = ' + self.iop_type + '\n')
        f.write('iop_backscatter_proportion_list = ' + str(self.iop_backscatter_proportion_list) + '\n')
        f.write('bound_bottom_reflec_diffuse_data = ' + str(self.bound_bottom_reflec_diffuse_data) + '\n')
        f.write('sky_sub_quad_count = ' + self.sky_sub_quad_count + '\n')
        f.write('iface_sub_quad_count = ' + self.iface_sub_quad_count + '\n')
        f.write('pf_sub_quad_count = ' + self.pf_sub_quad_count + '\n')
        f.write('integrator = ' + self.integrator + '\n')
        f.write('euler_steps_per_optical_depth = ' + str(self.euler_steps_per_optical_depth) + '\n')
        f.write('midpoint_steps_per_optical_depth = ' + str(self.midpoint_steps_per_optical_depth) + '\n')
        f.write('runga4_steps_per_optical_depth = ' + str(self.runga4_steps_per_optical_depth) + '\n')
        f.write('runga4adap_min_steps_per_optical_depth = ' + str(self.runga4adap_min_steps_per_optical_depth) + '\n')
        f.write('runga4adap_max_steps_per_optical_depth = ' + str(self.runga4adap_max_steps_per_optical_depth) + '\n')
        f.write('runga4adap_min_error = ' + str(self.runga4adap_min_error) + '\n')
        f.write('runga4adap_max_error = ' + str(self.runga4adap_max_error) + '\n')
        f.write('\n')

        f.write('Ld_b_image_save_fp = ' + os.path.join(self.output_path,
                                                       'image_Ld_b.ppm') + '\n')  #todo update this in the constructor not here

        f.write('Ld_b_image_sens_k = ' + str(self.ld_b_image_sens_k) + '\n')
        f.write('\n')
        f.write('Ld_b_save_fp = ' + os.path.join(self.output_path,
                                                 'Ld_b_data') + '\n')
        f.write('\n')
        f.write('report_save_fp = ' + self.report_file)
        f.write('\n')
        f.write('verbose = ' + str(self.verbose) + '\n')
        f.close()

    def write_sky_params_to_file(self):
        """
        @brief Writes the params to file that skytool_Free needs to generate the sky radiance distribution.
        """

        inp_file = self.sky_file + '_params.txt'
        lg.info('Writing Inputs to file : ' + inp_file)

        f = open(inp_file, 'w')

        f.write('verbose= ' + str(self.verbose) + '\n')
        f.write('band_count= ' + str(self.num_bands) + '\n')
        f.write('band_centres_data= ')
        f.write(",".join([str(wave) for wave in self.wavelengths]) + '\n')
        f.write('partition= ' + self.partition + '\n')
        f.write('vn= ' + str(self.vn) + '\n')
        f.write('hn= ' + str(self.hn) + '\n')
        f.write('rdif= ' + str(self.sky_r_dif) + '\n')
        f.write('theta_points= ')
        f.write(",".join([str(theta) for theta in self.theta_points]) + '\n')
        f.write('type= ' + self.sky_type + '\n')
        f.write('azimuth= ' + str(self.sky_azimuth) + '\n')
        f.write('zenith= ' + str(self.sky_zenith) + '\n')
        f.write('sky_save_fp= ' + inp_file.strip('_params.txt') + '\n')
        f.write('sky_image_save_fp= image_' + self.sky_file + '.ppm' + '\n')
        f.write('sky_image_size= 256' + '\n')
        if self.sky_type == 'hlideal':
            f.write('C= ' + str(self.sky_c) + '\n')
            f.write('rdif= ' + str(self.sky_r_dif) + '\n')
        f.flush()
        f.close()

    def write_surf_params_to_file(self):
        """
        @brief Writes the params to file that surftool_Free needs to generate the surface facets
        """

        inp_file = self.water_surface_file + '_params.txt'
        lg.info('Writing Inputs to file : ' + inp_file)

        if self.surf_state == 'flat':  # this is the only one that currently works.
            lg.info('Surface Type is :: flat')
            f = open(inp_file, 'w')

            f.write('verbose= ' + str(self.verbose) + '\n')
            f.write('band_count= ' + str(self.num_bands) + '\n')
            f.write('band_centres_data= ')
            f.write(",".join([str(wave) for wave in self.wavelengths]) + '\n')
            f.write('partition= ' + self.partition + '\n')
            f.write('vn= ' + str(self.vn) + '\n')
            f.write('hn= ' + str(self.hn) + '\n')
            f.write('theta_points= ')
            f.write(",".join([str(theta) for theta in self.theta_points]) + '\n')
            f.write('type= ' + self.iface_type + '\n')
            f.write('refrac_index_0= ' + str(self.iface_0_ri) + '\n')
            f.write('refrac_index_1= ' + str(self.iface_1_ri) + '\n')
            f.write('wind_speed= ' + str(self.wind_speed) + '\n')
            f.write('wind_direc= ' + str(self.wind_direc) + '\n')
            f.write('crosswind_vertices= ' + str(self.crosswind_vertices) + '\n')
            f.write('upwind_vertices= ' + str(self.upwind_vertices) + '\n')
            f.write('surface_size= ' + str(self.surface_size) + '\n')
            f.write('surface_radius=' + str(self.surface_radius) + '\n')
            f.write('target_size= ' + str(self.target_size) + '\n')
            f.write('rays_per_quad= ' + str(self.rays_per_quad) + '\n')
            f.write('surface_count= ' + str(self.surface_count) + '\n')
            f.write('azimuthally_average= ' + str(self.azimuthally_average) + '\n')
            f.write('surface_save_fp= ' + inp_file.strip('_params.txt') + '\n')
            f.flush()
            f.close()

    def write_phase_params_to_file(self):
        """
        @brief Writes the params to file that surftool_Free needs to generate the surface facets
        """
        inp_file = os.path.join(os.path.join(self.input_path, 'phase_files'), self.phase_function_file) + '_params.txt'
        lg.info('Writing Inputs to file : ' + inp_file)

        if self.iop_type == 'isotropic' or 'isotropic_integ' or 'petzold' or 'pure_water ':
            lg.info('Iop type is :: ' + self.iop_type)

            f = open(inp_file, 'w')

            f.write('verbose = ' + str(self.verbose) + '\n')
            f.write('band_count = ' + str(self.num_bands) + '\n')
            f.write('band_centres_data = ')
            f.write(",".join([str(wave) for wave in self.wavelengths]) + '\n')
            f.write('partition = ' + self.partition + '\n')
            f.write('vn = ' + str(self.vn) + '\n')
            f.write('hn = ' + str(self.hn) + '\n')
            f.write('theta_points = ')
            f.write(",".join([str(theta) for theta in self.theta_points]) + '\n')
            f.write('type = ' + self.iop_type + '\n')
            f.write('phase_func_save_fp = ' + inp_file.strip('_params.txt') + '\n')
            f.flush()
            f.close()


class BioOpticalParameters():
    def __init__(self, wavelengths):
        self.wavelengths = scipy.asarray([wavelengths])
        self.b_bp = scipy.asarray([])
        self.a_cdom = scipy.asarray([])
        self.a_phi = scipy.asarray([])
        self.a_water = scipy.asarray([])
        self.b_water = scipy.asarray([])

        self.b_b = scipy.asarray([])
        self.b = scipy.asarray([])
        self.a = scipy.asarray([])
        self.c = scipy.asarray([])


    def build_bbp(self, x, y, wave_const=550):
        r"""
        Builds the particle backscattering function  :math:`X(\frac{550}{\lambda})^Y`
        param: x function coefficient
        param: y order of the power function
        param: waveConst wave constant Default 550 nm
        retval: null
        """
        lg.info('Building b_bp spectra')
        self.b_bp = x * (wave_const / self.wavelengths) ** y

    def build_a_cdom(self, g, s, wave_const=400):
        r"""
        Builds the CDOM absorption function :: :math:`G \exp (-S(\lambda - 400))`
        param: g function coefficient
        param: s slope factor
        param: wave constant
        retval null
        """
        lg.info('building CDOM absorption')
        self.a_cdom = g * scipy.exp(-s * (self.wavelengths - wave_const))

    def read_aphi_from_file(self, file_name):
        """

        """
        lg.info('Reading ahpi absorption')
        try:
            self.a_phi = self._read_iop_from_file(file_name)
        except:
            lg.exception('Problem reading file :: ' + file_name)
            self.a_phi = -1

    def scale_aphi(self, scale_paraemter):
        """

        """
        lg.info('Scaling a_phi by :: ' + str(scale_paraemter))
        try:
            self.a_phi = self.a_phi * scale_paraemter
        except:
            lg.exception("Can't scale a_phi, check that it has been defined ")

    def read_pure_water_absorption_from_file(self, file_name):
        """

        """
        lg.info('Reading water absorption from file')
        try:
            self.a_water = self._read_iop_from_file(file_name)
        except:
            lg.exception('Problem reading file :: ' + file_name)
            self.a_phi = -1

    def read_pure_water_scattering_from_file(self, file_name):
        """

        """
        lg.info('Reading water scattering from file')
        try:
            self.b_water = self._read_iop_from_file(file_name)
        except:
            lg.exception('Problem reading file :: ' + file_name)
            self.b_phi = -1


    def _read_iop_from_file(self, file_name):
        """
        Generic IOP reader that interpolates the iop to the common wavelengths defined in the constructor

        returns: interpolated iop
        """
        lg.info('Reading :: ' + file_name + ' :: and interpolating to ' + str(self.wavelengths))

        if os.path.isfile(file_name):
            iop_reader = csv.reader(open(file_name), delimiter=',', quotechar='"')
            wave = iop_reader.next()
            iop = iop_reader.next()
        else:
            lg.exception('Problem reading file :: ' + file_name)
            raise IOError

        try:
            return scipy.interp(self.wavelengths, wave, iop)
        except IOError:
            lg.exception('Error interpolating IOP to common wavelength')
            return -1

    def write_b_to_file(self, file_name):
        self._write_iop_to_file(self.b, file_name)

    def write_c_to_file(self, file_name):
        self._write_iop_to_file(self.c, file_name)

    def _write_iop_to_file(self, iop, file_name):
        lg.info('Writing :: ' + file_name)
        f = open(file_name, 'w')
        for i in scipy.nditer(iop):
            f.write(str(i) + '\n')

    def build_bb(self):
        lg.info('Building bb spectra')
        self.b_b = self.b_bp + self.b_water

    def build_b(self, scattering_fraction=0.2):
        lg.info('Building b with scattering fraction of :: ' + str(scattering_fraction))
        self.b = self.b_b / scattering_fraction

    def build_a(self):
        lg.info('Building total absorption')
        self.a = self.a_water + self.a_cdom + self.a_phi

    def build_c(self):
        lg.info('Building total attenuation C')
        self.c = self.a + self.b

    def build_all_iop(self):
        lg.info('Building all b and c from IOPs')

        self.build_a()
        self.build_bb()
        self.build_b()
        self.build_c()


class BatchRun():
    """

    """
    def __init__(self, object, batch_name='batch'):
        """

        """
        self.run_params = object
        self.p_list = []  # Phyto scaling param
        self.x_list = []
        self.y_list = []
        self.g_list = []
        self.s_list = []
        self.z_list = []

        self.batch_output = os.path.join(self.run_params.output_path, batch_name)
        self.bio_params = BioOpticalParameters(self.run_params.wavelengths)

    def run(self):
        """

        """
        done = False
        dir_list = []
        tic = time.clock()
        lg.info('Starting batch run at :: ' + str(tic))

        if self.run_params.num_cpus == -1:  # user hasn't set a throttle
            self.run_params.num_cpus = os.sysconf("SC_NPROCESSORS_ONLN")
            lg.info('Found ' + str(self.run_params.num_cpus) + ' CPUs')

        #--------------------------------------------------#
        # COUNT THE NUMBER OF DIRECTORIES TO ITERATE THROUGH
        #--------------------------------------------------#
        tmp_dir_list = os.listdir(self.batch_output)
        for direc in tmp_dir_list:
            dir_list.append(os.path.join(self.batch_output, direc))

        num_dirs = len(dir_list)
        lg.info('Found ' + str(num_dirs) + ' directories to process in ' + self.batch_output)

        sub = scipy.floor(num_dirs / self.run_params.num_cpus)
        remainder = num_dirs - (sub * self.run_params.num_cpus)
        if remainder > 0:
            lg.warning('Number of variations not evenly divisible by number of CPUs')
            lg.warning('This is not a problem, last block will not use all available CPUs')
            lg.warning('The remainder is :: ' + str(remainder))

        while not done:
            for l in range(0, int(sub)):
                lg.info('Starting processing block of :: ' + str(self.run_params.num_cpus) + ' processes')

                for m in range(0, self.run_params.num_cpus):
                    #row = (m * sub) + l
                    _dir = dir_list.pop()

                    #--------------------------------------------------#
                    # CHECK TO SEE IF REPORT HAS BEEN GENERATED AND DON'T
                    # BOTHER RUNNING AGAIN IF THEY DO EXIST
                    #--------------------------------------------------#

                    report_dir, report_file_name = os.path.split(self.run_params.report_file)
                    lg.debug(report_file_name)
                    lg.debug(os.path.join(_dir, report_file_name))

                    try:
                        rep_size = os.path.getsize(os.path.join(_dir, report_file_name.strip('\n')))
                        lg.debug('report size is :: ' + str(rep_size))
                    except:
                        rep_size = 0


                    if rep_size < 1.0:   # TODO this is a spoof!
                        lg.info('No report file found, running process')
                        p = Process(target=self._run, args=(_dir,))
                    else:
                        lg.warning('Report file found :: ' + os.path.join(_dir, report_file_name.strip(
                            '\n')) + ' not redoing run ')
                        p = Process(target=self._dummy, args=(_dir,))

                    # !! for testing
                    #p = Process(target=self._dummy, args=(_dir,))
                    p.start()
                    lg.info('Starting Process :: Process ID :: ' + str(p.pid))

                p.join()

            self.run_params.num_cpus = remainder
            remainder = 0
            lg.info('Processing remainder')
            sub = 1
            if remainder == 0:
                done = True

        toc = time.clock()  # this isn't working
        lg.info('Ending batch run at :: ' + str(toc))
        timeTaken = toc - tic
        lg.info('Time taken ::' + str(timeTaken))

    def _dummy(self, run_dir):
        lg.debug(run_dir)

    def _run(self, run_dir, exec_path='/home/marrabld/Apps/planarRad/bin'):
        """

        """

        # Check to see if the required run_params files exist, if they dont use the tools to generate them

        #--------------------------------------------------#
        # HERE WE RECREATE OUR RUN_PARAMS OBJECT FROM
        # THE RUN FILE WE WROTE TO DISK EARLIER
        #--------------------------------------------------#
        file_tools = FileTools()
        run_dict = file_tools.read_param_file_to_dict(os.path.join(run_dir, 'batch.txt'))
        #run_params = RunParameters()
        #run_params = file_tools.dict_to_object(run_params, run_dict)
        #------------------------------------------------#
        # Sky inputs
        #------------------------------------------------#
        #lg.debug(run_dict.keys())
        lg.debug('!!!!!!!!!' + run_dict['sky_fp'])
        if os.path.isfile(run_dict['sky_fp']):
            sky_file_exists = True
            lg.info('Found sky_tool generated file' + run_dict['sky_fp'])
        else:
            lg.info('No sky_tool generated file, generating one')
            #try:
            inp_file = run_dict['sky_fp']  # + '_params.txt'
            self.run_params.sky_file = inp_file
            self.run_params.write_sky_params_to_file()
            #if not os.path.isfile(inp_file):
            #    lg.error(inp_file + ' : is not a valid parameter file')
            lg.debug('Runing skytool!!!!! @ ' + os.path.join(exec_path, 'skytool_free') + '#')
            lg.debug(os.path.join(exec_path, 'skytool_free') + ' params=' + inp_file)
            os.system(os.path.join(exec_path, 'skytool_free') + ' params=' + inp_file)
            #except OSError:
            #    lg.exception('Cannot execute PlannarRad, cannot find executable file to skytool_free')

        #------------------------------------------------#
        # Water surface inputs
        #------------------------------------------------#
        if os.path.isfile(run_dict['water_surface_fp']):
            surface_file_exists = True
            lg.info('Found surf_tool generated file' + run_dict['water_surface_fp'])
        else:
            lg.info('No surf_tool generated file, generating one')
            try:
                inp_file = run_dict['water_surface_fp'] + '_params.txt'
                self.run_params.write_surf_params_to_file()
                if not os.path.isfile(inp_file):
                    lg.error(inp_file + ' : is not a valid parameter file')
                os.system(os.path.join(exec_path, 'surftool_free') + ' params=' + inp_file)
            except OSError:
                lg.exception('Cannot execute PlannarRad, cannot find executable file to surftool_free')

        #------------------------------------------------#
        # Phase functions inputs
        #------------------------------------------------#
        if os.path.isfile(run_dict['pf_fp']):
            phase_file_exists = True
            lg.info('Found phase_tool generated file' + run_dict['pf_fp'])
        else:
            lg.info('No sky_tool generated file, generating one')
            try:
                inp_file = run_dict['pf_fp'] + '_params.txt'
                self.run_params.write_phase_params_to_file()
                if not os.path.isfile(inp_file):
                    lg.error(inp_file + ' : is not a valid parameter file')
                os.system(os.path.join(exec_path, 'phasetool_free') + ' params=' + inp_file)
            except OSError:
                lg.exception('Cannot execute PlannarRad, cannot find executable file to phasetool_free')

        #------------------------------------------------#
        # slabtool inputs [Run planarrad]
        #------------------------------------------------#

        inp_file = run_dict['name']

        if not os.path.isfile(inp_file):
            lg.error(inp_file + ' : is not a valid batch file')

        try:
            os.system(os.path.join(exec_path, 'slabtool_free') + ' params=' + inp_file)
        except OSError:
            lg.exception('Cannot execute PlannarRad, cannot find executable file to slabtool_free')

    def generate_directories(self, overwrite=False):
        """

        """
        if not os.path.exists(self.batch_output):
            try:
                lg.info('Creating batch project directory')
                if self.batch_output == self.run_params.output_path + 'batch':
                    lg.warning('Using default project name.  Consider renaming!')
                os.makedirs(self.batch_output)
            except OSError:
                lg.exception('Could not create project directory')

        elif os.path.exists(self.batch_output) and overwrite == True:
            try:
                lg.info('Creating batch project directory')
                lg.warning('Overwriting existing directories')
                if self.batch_output == self.run_params.output_path + 'batch':
                    lg.warning('Using default project name.  Consider renaming!')
                os.makedirs(self.batch_output)
            except OSError:
                lg.exception('Could not create project directory')



        #--------------------------------------------------#
        # GENERATE ALL THE IOPS FROM BIOP
        #--------------------------------------------------#

        #--------------------------------------------------#
        # WRITE EACH BIOP TO CSV FILE INTO THE INPUT
        # DIRECTORY IF IT DOESNT EXIST
        #--------------------------------------------------#

        #--------------------------------------------------#
        # GENERATE A LIST OF ALL COMBINATIONS OF BIOPS
        #--------------------------------------------------#

        #--------------------------------------------------#
        # WRITE THE DIRECTORIES FOR EACH BIOP AND NAME APPROPRIATELY
        # DON'T OVERWRITE IF THEY EXIST ALREADY
        #--------------------------------------------------#

        self.bio_params.read_pure_water_absorption_from_file(
            self.run_params.pure_water_absorption_file)
        self.bio_params.read_pure_water_scattering_from_file(
            self.run_params.pure_water_scattering_file)
        self.bio_params.read_aphi_from_file(self.run_params.phytoplankton_absorption_file)

        for p in self.p_list:
            for x in self.x_list:
                for y in self.y_list:
                    for g in self.g_list:
                        for s in self.s_list:
                            for z in self.z_list:
                                file_name = 'P' + str(p) + '_X' + str(x) + '_Y' + str(y) + '_G' + str(g) + '_S' + str(
                                    s) + '_Z' + str(z)
                                dir_name = os.path.join(self.batch_output, file_name)
                                self.run_params.output_path = dir_name
                                #--------------------------------------------------#
                                # UPDATE THE IOP PARAMETERS FOR THE RUN FILE
                                #--------------------------------------------------#
                                self.run_params.depth = z
                                self.bio_params.build_bbp(x, y)  # todo add wave const as a kwarg
                                self.bio_params.build_a_cdom(g, s)

                                self.bio_params.build_all_iop()
                                self.run_params.scattering_file = os.path.join(
                                    os.path.join(self.run_params.input_path, 'iop_files'), 'b_' + file_name)
                                self.bio_params.write_b_to_file(self.run_params.scattering_file)

                                self.run_params.attenuation_file = os.path.join(
                                    os.path.join(self.run_params.input_path, 'iop_files'), 'c_' + file_name)
                                self.bio_params.write_c_to_file(self.run_params.attenuation_file)

                                self.run_params.project_file = os.path.join(dir_name, 'batch.txt')

                                if not os.path.exists(dir_name):
                                    try:
                                        lg.info('Creating run directory')
                                        os.makedirs(dir_name)
                                        self.run_params.write_run_parameters_to_file()
                                    except OSError:
                                        lg.exception('Could not create run directory')

                                elif os.path.exists(dir_name) and overwrite == True:
                                    try:
                                        lg.info('Creating run directory')
                                        lg.warning('Overwriting existing directories')
                                        os.makedirs(dir_name)
                                        self.run_params.write_run_parameters_to_file()
                                    except OSError:
                                        lg.exception('Could not create run directory')
                                        #--------------------------------------------------#
                                        # FIGURE OUT WHICH IOP TO USE FROM THE DIRECTORY NAME
                                        # WRITE THE PARAM FILE IN TO THE DIRECTORY
                                        #--------------------------------------------------#

                                        #--------------------------------------------------#
                                        # MAKE A LIST OF ALL THE DIRECTORIES AND CHECK
                                        # IF THEY HAVE ANY OUTPUTS IN THEM, IF THEY DO THEY
                                        # HAVE BEEN RUN ALREADY.  IF NOT PARSE THAT RUN FILE
                                        # TO PLANARRAD.  THIS MEANS IF IT FALLS OVER THEN THE
                                        # BATCH CAN BE STARTED AGAIN WITHOUT
                                        #--------------------------------------------------#


    def batch_parameters(self, p, x, y, g, s, z):
        self.p_list = p
        self.x_list = x
        self.y_list = y
        self.g_list = g
        self.s_list = s
        self.z_list = z


class FileTools():
    """

    """
    def __init__(self):
        pass

    @staticmethod
    def read_param_file_to_dict(file_name):
        """

        """
        data = loadtxt(file_name, delimiter='=', dtype=scipy.string0)
        data_dict = dict(data)
        for key in data_dict.keys():
            data_dict[key] = data_dict[key].strip()
            data_dict[key.strip()] = data_dict[key]
            del data_dict[key]

        return data_dict

    @staticmethod
    def dict_to_object(data_object, data_dict):
        """

        """
        data_object.__dict__ = data_dict
        return data_object


class HelperMethods():
    """

    """
    def __init__(self):
        pass

    @staticmethod
    def string_to_float_list(string_var):
        """

        """
        return [float(s) for s in string_var.strip('[').strip(']').split(', ')]















