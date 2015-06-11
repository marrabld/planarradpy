import os
import sys
import time
from os.path import expanduser

sys.path.append("../..")
try:
    log_dir = expanduser('~/.planarradpy')
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
except:
    print("Can't create log dir " + log_dir + " : it may exist")

try:
    if not os.path.exists(os.path.join(log_dir, 'log')):
        os.mkdir(os.path.join(log_dir, 'log'))
except:
    print("Can't create log directory " + log_dir + '/log' + " : it may exist")


import logger as log
import scipy
from scipy import loadtxt
import libplanarradpy
import libplanarradpy.state
import csv
from multiprocessing import Process

__author__ = 'marrabld'

DEBUG_LEVEL = libplanarradpy.state.State().debug
lg = log.logger
lg.setLevel(DEBUG_LEVEL)


class RunParameters():
    """Run parameters required by PlanarRad

    All parameters are properties of this class
    """

    def __init__(self, wavelengths):
        lg.info('============')
        lg.info('Initialising')
        lg.info('============')

        if not wavelengths:
            self.wavelengths = scipy.linspace(410.0, 730.0, 17)
        else:
            self.wavelengths = scipy.fromstring(wavelengths, dtype=float, sep=',')

        self.a = scipy.zeros_like(self.wavelengths)  # total absorption
        self.a_phi = scipy.zeros_like(self.wavelengths)
        self.a_water = scipy.zeros_like(self.wavelengths)
        self.a_cdom = scipy.zeros_like(self.wavelengths)  # CDOM absorption
        self.bb = scipy.zeros_like(self.wavelengths)  # backscatter
        self.bbp = scipy.zeros_like(self.wavelengths)  # particulate scatter
        self.b_water = scipy.zeros_like(self.wavelengths)
        self.b = scipy.zeros_like(self.wavelengths)  # scatter
        self.c = scipy.zeros_like(self.wavelengths)  # attenuation
        self.iop_backscatter_proportion_list = ''  # scipy.asarray([])
        self.depth = 5
        self.theta_points = [0, 5, 15, 25, 35, 45, 55, 65, 75, 85, 90, 95, 105, 115, 125, 135, 145, 155, 165, 175, 180]
        #self.input_path = os.path.abspath(os.path.join('..', 'inputs'))
        #self.output_path = os.path.abspath(os.path.join('..', 'outputs'))
        self.input_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../inputs'))
        #print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1111" + os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../inputs')))
        self.output_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../outputs'))
        self.pure_water_absorption_file = os.path.abspath(
            os.path.join(os.path.join(self.input_path, 'iop_files'), 'a_water.csv'))
        self.pure_water_scattering_file = os.path.abspath(
            os.path.join(os.path.join(self.input_path, 'iop_files'), 'b_water.csv'))
        self.phytoplankton_absorption_file = os.path.abspath(
            os.path.join(os.path.join(self.input_path, 'iop_files'), 'a_phi.csv'))
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ' + self.phytoplankton_absorption_file)
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
        """All of the class properties are written to a text file

        Each property is on a new line with the key and value seperated with an equals sign '='
        This is the mane planarrad properties file used by slabtool
        """

        self.update_filenames()

        lg.info('Writing Inputs to file : ' + self.project_file)

        # First update the file names in case we changed the file values.  the file name includes the file values
        # self.updateFileNames()

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
        # width = self.wavelengths[i + 1] - self.wavelengths[i]
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
        """Writes the params to file that skytool_Free needs to generate the sky radiance distribution."""

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
        f.write('sky_image_save_fp= ' + self.sky_file + '.ppm' + '\n')
        f.write('sky_image_size= 256' + '\n')
        if self.sky_type == 'hlideal':
            f.write('C= ' + str(self.sky_c) + '\n')
            f.write('rdif= ' + str(self.sky_r_dif) + '\n')
        f.flush()
        f.close()

    def write_surf_params_to_file(self):
        """Write the params to file that surftool_Free needs to generate the surface facets"""

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
        """Write the params to file that surftool_Free needs to generate the surface facets"""
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

    def update_filenames(self):
        """Does nothing currently.  May not need this method"""
        self.sky_file = os.path.abspath(os.path.join(os.path.join(self.input_path, 'sky_files'),
                                                     'sky_' + self.sky_state + '_z' + str(
                                                         self.sky_zenith) + '_a' + str(
                                                         self.sky_azimuth) + '_' + str(
                                                         self.num_bands) + '_' + self.ds_code))


class BioOpticalParameters():
    """Contains useful parameters and methods for modelling IOPs using bio-optical models

    Constructor takes wavelengths.  This is a common wavelength that all IOPs will be interpolated to
    """

    def __init__(self, wavelengths):
        """Constructor

        :param wavelengths: list of wavelengths all IOPs will be interpolated to
        """
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
        """
        Builds the particle backscattering function  :math:`X(\\frac{550}{\\lambda})^Y`

        :param x: function coefficient
        :param y: order of the power function
        :param wave_const: wave constant default 550 (nm)
        :returns null:
        """
        lg.info('Building b_bp spectra')
        self.b_bp = x * (wave_const / self.wavelengths) ** y

    def build_a_cdom(self, g, s, wave_const=400):
        """
        Builds the CDOM absorption function :: :math:`G \exp (-S(\lambda - 400))`

        :param g: function coefficient
        :param s: slope factor
        :param wave_const: wave constant default = 400 (nm)
        :returns null:
        """
        lg.info('building CDOM absorption')
        self.a_cdom = g * scipy.exp(-s * (self.wavelengths - wave_const))

    def read_aphi_from_file(self, file_name):
        """Read the phytoplankton absorption file from a csv formatted file

        :param file_name: filename and path of the csv file
        """
        lg.info('Reading ahpi absorption')
        try:
            self.a_phi = self._read_iop_from_file(file_name)
        except:
            lg.exception('Problem reading file :: ' + file_name)
            self.a_phi = -1

    def scale_aphi(self, scale_parameter):
        """Scale the spectra by multiplying by linear scaling factor

        :param scale_parameter: Linear scaling factor
        """
        lg.info('Scaling a_phi by :: ' + str(scale_parameter))
        try:
            self.a_phi = self.a_phi * scale_parameter
        except:
            lg.exception("Can't scale a_phi, check that it has been defined ")

    def read_pure_water_absorption_from_file(self, file_name):
        """Read the pure water absorption from a csv formatted file

        :param file_name: filename and path of the csv file
        """
        lg.info('Reading water absorption from file')
        try:
            self.a_water = self._read_iop_from_file(file_name)
        except:
            lg.exception('Problem reading file :: ' + file_name)


    def read_pure_water_scattering_from_file(self, file_name):
        """Read the pure water scattering from a csv formatted file

        :param file_name: filename and path of the csv file
        """
        lg.info('Reading water scattering from file')
        try:
            self.b_water = self._read_iop_from_file(file_name)
        except:
            lg.exception('Problem reading file :: ' + file_name)


    def _read_iop_from_file(self, file_name):
        """
        Generic IOP reader that interpolates the iop to the common wavelengths defined in the constructor

        :param file_name: filename and path of the csv file
        :returns interpolated iop
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
        """Write the total scattering to csv file

        :param file_name: filename and path of the csv file
        """
        self._write_iop_to_file(self.b, file_name)

    def write_c_to_file(self, file_name):
        """Write the total attentuation to file

        :param file_name: filename and path of the csv file
        """
        self._write_iop_to_file(self.c, file_name)

    def _write_iop_to_file(self, iop, file_name):
        """Generic iop file writer

        :param iop numpy array to write to file
        :param file_name the file and path to write the IOP to
        """
        lg.info('Writing :: ' + file_name)
        f = open(file_name, 'w')
        for i in scipy.nditer(iop):
            f.write(str(i) + '\n')

    def build_bb(self):
        """Calculates the total backscattering


        """
        lg.info('Building bb spectra')
        self.b_b = self.b_bp  # + b_bphi

    def build_b(self, scattering_fraction=0.01833):
        """Calculates the total scattering from back-scattering

        :param scattering_fraction: the fraction of back-scattering to total scattering default = 0.01833
        """
        lg.info('Building b with scattering fraction of :: ' + str(scattering_fraction))
        self.b = (self.b_b + self.b_water / 2.0) / scattering_fraction

    def build_a(self):
        """Calculates the total absorption from water, phytoplankton and CDOM

        a = awater + acdom + aphi
        """
        lg.info('Building total absorption')
        self.a = self.a_water + self.a_cdom + self.a_phi

    def build_c(self):
        """Calculates the total attenuation from the total absorption and total scattering

        c = a + b
        """
        lg.info('Building total attenuation C')
        self.c = self.a + self.b

    def build_all_iop(self):
        """Meta method that calls all of the build methods in the correct order

        self.build_a()
        self.build_bb()
        self.build_b()
        self.build_c()
        """
        lg.info('Building all b and c from IOPs')

        self.build_a()
        self.build_bb()
        self.build_b()
        self.build_c()


class BatchRun():
    """This class is used for batch running PlanarRad for many different IOPs.

    It will also distribute the work over many CPUs.  It will run an single instance for PlanarRad on each available
    cores or the number of cores defined in the batchrun file.

    Available 'batchable' parameters are: \n
    Sun Azimuth Angle (deg) [saa] \n
    Sun Zenith Angle (deg) [sza] \n
    Phytoplankton scaling parameter [p] \n
    particulate scattering parameters [x, y] see BioOpticalParameters \n
    CDOM absorption parameters [g, s] \n
    depth (m) [z]
    """

    def __init__(self, object, batch_name='batch'):
        """Construcuter that sets the up batch run with 'batchable' parameters

        :param batch_name: the name of the project.  All outputs will be put in a directory of the same name
        """
        self.run_params = object
        self.saa_list = []
        self.sza_list = []
        self.p_list = []  # Phyto scaling param
        self.x_list = []
        self.y_list = []
        self.g_list = []
        self.s_list = []
        self.z_list = []

        self.batch_output = os.path.join(self.run_params.output_path, batch_name)
        self.bio_params = BioOpticalParameters(self.run_params.wavelengths)

    def run(self):
        """Distributes the work across the CPUs.  It actually uses _run()"""
        done = False
        dir_list = []
        tic = time.clock()
        lg.info('Starting batch run at :: ' + str(tic))

        if self.run_params.num_cpus == -1:  # user hasn't set a throttle
            self.run_params.num_cpus = os.sysconf("SC_NPROCESSORS_ONLN")
            lg.info('Found ' + str(self.run_params.num_cpus) + ' CPUs')

        # --------------------------------------------------#
        # COUNT THE NUMBER OF DIRECTORIES TO ITERATE THROUGH
        # --------------------------------------------------#
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

                    if rep_size < 1.0:  # TODO this is a spoof!
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
        """This is just for spoofing the batch.  Doesn't run anything"""
        lg.debug(run_dir)

    def _run(self, run_dir):
        """Distributed process"""

        # Check to see if the required run_params files exist, if they dont use the tools to generate them

        # --------------------------------------------------#
        # HERE WE RECREATE OUR RUN_PARAMS OBJECT FROM
        # THE RUN FILE WE WROTE TO DISK EARLIER
        # --------------------------------------------------#
        file_tools = FileTools()
        run_dict = file_tools.read_param_file_to_dict(os.path.join(run_dir, 'batch.txt'))
        #print(run_dict['band_centres_data'])

        #self.run_params.wavelengths = run_dict['wavelengths']
        #run_params = RunParameters()
        #run_params = file_tools.dict_to_object(run_params, run_dict)
        #------------------------------------------------#
        # Sky inputs
        #------------------------------------------------#
        #lg.debug(run_dict.keys())
        #self.run_params.update_filenames()
        #lg.debug('!!!!!!!!!' + run_dict['sky_fp'])
        if os.path.isfile(run_dict['sky_fp']):
            sky_file_exists = True
            lg.info('Found sky_tool generated file' + run_dict['sky_fp'])
        else:
            lg.info('No sky_tool generated file, generating one')
            #try:
            inp_file = run_dict['sky_fp'] + '_params.txt'
            #self.run_params.sky_file = inp_file
            self.run_params.write_sky_params_to_file()
            #if not os.path.isfile(inp_file):
            #    lg.error(inp_file + ' : is not a valid parameter file')
            lg.debug('Runing skytool' + os.path.join(self.run_params.exec_path, 'skytool_free') + '#')
            lg.debug(os.path.join(self.run_params.exec_path, 'skytool_free') + ' params=' + inp_file)
            os.system(os.path.join(self.run_params.exec_path, 'skytool_free') + ' params=' + inp_file)
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
                os.system(os.path.join(self.run_params.exec_path, 'surftool_free') + ' params=' + inp_file)
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
                os.system(os.path.join(self.run_params.exec_path, 'phasetool_free') + ' params=' + inp_file)
            except OSError:
                lg.exception('Cannot execute PlannarRad, cannot find executable file to phasetool_free')

        #------------------------------------------------#
        # slabtool inputs [Run planarrad]
        #------------------------------------------------#

        inp_file = run_dict['name']

        if not os.path.isfile(inp_file):
            lg.error(inp_file + ' : is not a valid batch file')

        try:
            os.system(os.path.join(self.run_params.exec_path, 'slabtool_free') + ' params=' + inp_file)
        except OSError:
            lg.exception('Cannot execute PlannarRad, cannot find executable file to slabtool_free')

    def generate_directories(self, overwrite=False):
        """For all possible combinations of 'batchable' parameters. create a unique directory to story outputs

        Each directory name is unique and contains the run parameters in the directory name

        :param overwrite: If set to True will over write all files default = False
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



        # --------------------------------------------------#
        # GENERATE ALL THE IOPS FROM BIOP
        # --------------------------------------------------#

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

        for saa in self.saa_list:
            # update the saa in the run file & the todo filename!
            self.run_params.sky_aziumth = saa
            self.run_params.sky_file = os.path.abspath(
                os.path.join(os.path.join(self.run_params.input_path, 'sky_files'),
                             'sky_' + self.run_params.sky_state + '_z' + str(self.run_params.sky_zenith) + '_a' + str(
                                 self.run_params.sky_azimuth) + '_' + str(
                                 self.run_params.num_bands) + '_' + self.run_params.ds_code))

            for sza in self.sza_list:
                # update the saz in the run file
                self.run_params.sky_zenith = sza
                self.run_params.sky_file = os.path.abspath(
                    os.path.join(os.path.join(self.run_params.input_path, 'sky_files'),
                                 'sky_' + self.run_params.sky_state + '_z' + str(
                                     self.run_params.sky_zenith) + '_a' + str(self.run_params.sky_azimuth) + '_' + str(
                                     self.run_params.num_bands) + '_' + self.run_params.ds_code))
                for p in self.p_list:
                    for x in self.x_list:
                        for y in self.y_list:
                            for g in self.g_list:
                                for s in self.s_list:
                                    for z in self.z_list:
                                        file_name = 'SAA' + str(saa) + '_SZA' + str(sza) + '_P' + str(p) + '_X' + str(
                                            x) + '_Y' + str(y) + '_G' + str(g) + '_S' + str(s) + '_Z' + str(z)
                                        dir_name = os.path.join(self.batch_output, file_name)
                                        self.run_params.output_path = dir_name
                                        #--------------------------------------------------#
                                        # UPDATE THE IOP PARAMETERS FOR THE RUN FILE
                                        #--------------------------------------------------#
                                        self.run_params.sky_azimuth = saa
                                        self.run_params.sky_zenith = sza
                                        self.run_params.depth = z
                                        self.bio_params.build_bbp(x, y)  # todo add wave const as a kwarg
                                        self.bio_params.build_a_cdom(g, s)
                                        # Need to re-read the file as it was scaled in a the other run!
                                        self.bio_params.read_aphi_from_file(
                                            self.run_params.phytoplankton_absorption_file)
                                        self.bio_params.scale_aphi(p)

                                        self.bio_params.build_all_iop()
                                        self.run_params.scattering_file = os.path.join(
                                            os.path.join(self.run_params.input_path, 'iop_files'), 'b_' + file_name)
                                        self.bio_params.write_b_to_file(self.run_params.scattering_file)

                                        self.run_params.attenuation_file = os.path.join(
                                            os.path.join(self.run_params.input_path, 'iop_files'), 'c_' + file_name)
                                        self.bio_params.write_c_to_file(self.run_params.attenuation_file)

                                        self.run_params.project_file = os.path.join(dir_name, 'batch.txt')
                                        self.run_params.report_file = os.path.join(dir_name, 'report.txt')

                                        self.run_params.write_sky_params_to_file()
                                        self.run_params.write_surf_params_to_file()
                                        self.run_params.write_phase_params_to_file()

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


    def batch_parameters(self, saa, sza, p, x, y, g, s, z):
        """Takes lists for parameters and saves them as class properties

        :param saa: <list> Sun Azimuth Angle (deg)
        :param sza: <list> Sun Zenith Angle (deg)
        :param p: <list> Phytoplankton linear scalling factor
        :param x: <list> Scattering scaling factor
        :param y: <list> Scattering slope factor
        :param g: <list> CDOM absorption scaling factor
        :param s: <list> CDOM absorption slope factor
        :param z: <list> depth (m)"""
        self.saa_list = saa
        self.sza_list = sza
        self.p_list = p
        self.x_list = x
        self.y_list = y
        self.g_list = g
        self.s_list = s
        self.z_list = z


class FileTools():
    """Useful static methods for file mangling"""

    def __init__(self):
        pass

    @staticmethod
    def read_param_file_to_dict(file_name):
        """Loads a text file to a python dictionary using '=' as the delimiter

        :param file_name: the name and path of the text file
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
        """Maps a dictionary to an object.  Variable names become the key in the dict

        :param data_object: Is an instantiated class
        :param data_dict: is the python dictionary
        :returns data_object:
        """
        data_object.__dict__ = data_dict
        return data_object


class HelperMethods():
    """Useful static methods"""

    def __init__(self):
        pass

    @staticmethod
    def string_to_float_list(string_var):
        """Pull comma separated string values out of a text file and converts them to float list"""
        try:
            return [float(s) for s in string_var.strip('[').strip(']').split(', ')]
        except:
            return [float(s) for s in string_var.strip('[').strip(']').split(',')]


class ReportTools():
    """Load the report in to a dictionary"""

    def __init__(self):
        self.data_dictionary = {}

    def read_pr_report(self, filename):
        """Reads in a PlanarRad generated report

        Saves the single line reported parameters as a python dictionary

        :param filename: The name and path of the PlanarRad generated file
        :returns self.data_dictionary: python dictionary with the key and values from the report
        """
        done = False
        f = open(filename)
        while f:
        #for line in open(filename):
            line = f.readline()
            if not line:
                done = True
                break

            if "# Quad solid angle mean point theta table (rows are horizontal, columns are vertical):" in line.strip():
                # read in the bunch of lines.
                tmp = []
                for i_iter in range(0, len(self.data_dictionary['theta_points_deg']) - 2):
                    tmp.append(f.readline())

                self.data_dictionary['Quad_solid_angle_mean_point_theta'] = tmp

            elif '#' not in line or not line.strip():
                element = line.split(',')
                self.data_dictionary[element[0]] = element[1:]

            if "# Quad solid angle mean point phi table (rows are horizontal, columns are vertical):" in line.strip():
                # read in the bunch of lines.
                tmp = []
                for i_iter in range(0, len(self.data_dictionary['theta_points_deg']) - 2):
                    tmp.append(f.readline())

                self.data_dictionary['Quad_solid_angle_mean_point_phi'] = tmp

            elif '#' not in line or not line.strip():
                element = line.split(',')
                self.data_dictionary[element[0]] = element[1:]

            if "L_w band" in line.strip():

                for i_iter in range(0, int(self.data_dictionary['band_count'][1])):
                    tmp = []
                    for j_iter in range(0, len(self.data_dictionary['theta_points_deg']) - 2):
                        tmp.append(f.readline())

                    self.data_dictionary['L_w_band_' + str(i_iter + 1)] = tmp
                    f.readline()
                    f.readline()  # skip the next 2 lines

            if "L_it band" in line.strip():

                for i_iter in range(0, int(self.data_dictionary['band_count'][1])):
                    tmp = []
                    for j_iter in range(0, len(self.data_dictionary['theta_points_deg']) - 2):
                        tmp.append(f.readline())

                    self.data_dictionary['L_it_band_' + str(i_iter + 1)] = tmp
                    f.readline()
                    f.readline()  # skip the next 2 lines




        return self.data_dictionary

    def get_parameter(self, parameter):
        pass

    def calc_directional_aop(self, report, parameter, parameter_dir):
        """
        Will calcuate the directional AOP (only sub-surface rrs for now) if the direction is defined using @
        e.g. rrs@32.0:45  where <zenith-theta>:<azimuth-phi>

        :param report: The planarrad report dictionary.  should include the quadtables and the directional info
        :param parameter: parameter to calc.  Currently only sub-surface reflectance rrs.
        :return:
        """
        lg.debug('calculating the directional ' + parameter)
        tmp_zenith = []

        param_zenith = parameter_dir.split(':')[0]
        param_azimuth = parameter_dir.split(':')[1]

        # --------------------------------------------------#
        # find the mean directions values
        # --------------------------------------------------#
        for i_iter in range(0, int(report['vn'][1])):
            tmp_zenith.append(report['Quad_solid_angle_mean_point_theta'][i_iter][:].split(',')[0]) #that was a pain!

        tmp_azimuth = report['Quad_solid_angle_mean_point_phi'][1]
        zenith = scipy.asarray(tmp_zenith, dtype=float)
        azimuth = scipy.fromstring(tmp_azimuth, dtype=float, sep=',')

        # --------------------------------------------------#
        # now grab the min and max index of the closest match
        # --------------------------------------------------#
        #min_zenith_idx = (scipy.abs(zenith - param_zenith)).argmin()

        from scipy import interpolate


        lw = scipy.zeros(int(report['band_count'][1]))

        for j_iter in range(0, int(report['band_count'][1])):

            if parameter == 'rrs':
                lg.info('Calculating directional rrs')
                tmp_lw = report['L_w_band_' + str(j_iter + 1)]
            elif parameter == 'Rrs':
                lg.info('Calculating directional Rrs')
                print(report.keys())
                tmp_lw = report['L_it_band_' + str(j_iter + 1)]

            lw_scal = scipy.zeros((int(report['vn'][1]), int(report['hn'][1])))

            # for the fist and last line we have to replicate the top and bottom circle
            for i_iter in range(0, int(report['hn'][1])):
                lw_scal[0, i_iter] = tmp_lw[0].split(',')[0]
                lw_scal[int(report['vn'][1]) - 1, i_iter] = tmp_lw[-1].split(',')[0]

            for i_iter in range(1, int(report['vn'][1]) - 1):
                lw_scal[i_iter, :] = scipy.asarray(tmp_lw[i_iter].split(','), dtype=float)

            # to do, make an array of zeros and loop over each list an apply to eah line.  bruteforce

            f1 = interpolate.interp2d(zenith, azimuth, lw_scal)
            lw[j_iter] = f1(float(param_zenith), float(param_azimuth))

        # ----
        # Now we finally have L_w we calculate the rrs
        # ----

        if parameter == 'rrs':
            tmp_rrs = lw / scipy.asarray(report['Ed_w'], dtype=float)[1:]  # ignore the first val as that is depth of val
        elif parameter == 'Rrs':
            tmp_rrs = lw / scipy.asarray(report['Ed_a'], dtype=float)[1:]  # ignore the first val as that is depth of val

        # make rrs a string so it can be written to file.

        rrs = ",".join(map(str, tmp_rrs))

        return " ," + rrs  # Note could be rrs or Rrs

    def write_batch_report(self, input_directory, parameter):
        """
        Collect all of the batch reports and concatenate the results.  The report should be :

        :param input_directory:
        :param parameter: This is the parameter in which to report.
        """

        # Check to see if there is an @ in the parameter.  If there is split
        if '@' in parameter:
            parameter_dir = parameter.split('@')[1]
            parameter = parameter.split('@')[0]

        # --------------------------------------------------#
        # we put the batch report one directory up in the tree
        # --------------------------------------------------#
        batch_report_file = 'batch_report.txt'
        batch_report_file = os.path.join(input_directory, batch_report_file)
        f = open(batch_report_file, 'w')
        w = csv.writer(f, delimiter=',')

        #--------------------------------------------------#
        # Read in the report from planarrad and pull out the parameter that we want
        #--------------------------------------------------#
        dir_list = os.listdir(input_directory)

        #--------------------------------------------------#
        # Sometimes the report isn't generated for some reason.
        # this checks to see if the first file in the dir list exists and skips if it doesn't
        #--------------------------------------------------#
        read_first_file = True
        i_iter = 0
        while read_first_file:
            if os.path.exists(os.path.join(input_directory, os.path.join(dir_list[i_iter], 'report.txt'))):
                report = self.read_pr_report(
                    os.path.join(input_directory, os.path.join(dir_list[i_iter], 'report.txt')))
                read_first_file = False
            else:
                lg.warning('Missing report file in' + dir_list[i_iter])
                i_iter += 1

        try:
            wave_val = report['band_centres']
            param_val = report[parameter]
        except:
            lg.exception('Parameter :: ' + str(parameter) + ' :: Not in report')

        wave_str = str(wave_val)
        wave_str = wave_str.strip('[').strip(']').replace('\'', '').replace('\\n', '').replace('  ', '').replace(' -,',
                                                                                                                 '').replace(
            ',', '\",\"')

        f.write(
            '\"Sun Azimuth (deg)\",\"Sun Zenith (deg)\",\"Phytoplankton\",\"Scattering X\",\"Scattering Y\",\"CDOM G\",\"CDOM S\",\"Depth (m)\",\"#wave length (nm) ->\",\"' + wave_str + '\"\n')

        #--------------------------------------------------#
        # Get all of the directories under the batch directories
        # The directory names have the IOP parameters in the names
        #--------------------------------------------------#

        for dir in dir_list:
            if os.path.isdir(os.path.abspath(os.path.join(input_directory, dir))):
                tmp_str_list = dir.split('_')
                #for tmp_str in tmp_str_list:
                saa = ''.join(c for c in tmp_str_list[0] if not c.isalpha())
                sza = ''.join(c for c in tmp_str_list[1] if not c.isalpha())
                p = ''.join(c for c in tmp_str_list[2] if not c.isalpha())
                x = ''.join(c for c in tmp_str_list[3] if not c.isalpha())
                y = ''.join(c for c in tmp_str_list[4] if not c.isalpha())
                g = ''.join(c for c in tmp_str_list[5] if not c.isalpha())
                s = ''.join(c for c in tmp_str_list[6] if not c.isalpha())
                z = ''.join(c for c in tmp_str_list[7] if not c.isalpha())

                #--------------------------------------------------#
                # Write the report header and then the values above in the columns
                #--------------------------------------------------#
                try:
                    f.write(saa + ',' + sza + ',' + p + ',' + x + ',' + y + ',' + g + ',' + s + ',' + z + ',')

                    report = self.read_pr_report(os.path.join(input_directory, os.path.join(dir, 'report.txt')))
                    try:
                        # check to see if the parameter has the @ parameter.  If it does pass to directional calculator
                        if 'parameter_dir' in locals():
                            param_val = self.calc_directional_aop(report, parameter, parameter_dir)
                        else:
                            param_val = report[parameter]

                        param_str = str(param_val)
                        param_str = param_str.strip('[').strip(']').replace('\'', '').replace('\\n', '').replace('  ',
                                                                                                                 '')
                        f.write(param_str + '\n')
                    except:
                        lg.exception('Parameter :: ' + str(parameter) + ' :: Not in report')
                except:
                    lg.warning('Cannot find a report in directory :: ' + dir)
