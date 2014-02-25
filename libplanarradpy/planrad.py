import os
import sys

sys.path.append("../..")
import logger as log
import scipy
import libplanarradpy
import libplanarradpy.state

__author__ = 'marrabld'

DEBUG_LEVEL = libplanarradpy.state.State().debug
lg = log.logger
lg.setLevel(DEBUG_LEVEL)


class RunParameters(object):
    def __init__(self):
        lg.info('============')
        lg.info('Initialising')
        lg.info('============')

        self.wavelengths = scipy.asarray([440, 750])
        self.a = scipy.asarray([]) # total absorption
        self.a_phi = scipy.asarray([])
        self.a_water = scipy.asarray([])
        self.a_cdom = scipy.asarray([]) # CDOM absorption
        self.bb = scipy.asarray([]) # backscatter
        self.bbp = scipy.asarray([]) # particulate scatter
        self.b_water = scipy.asarray([])
        self.b = scipy.asarray([]) # scatter
        self.c = scipy.asarray([]) # attenuation
        self.iop_backscatter_proportion_list = scipy.asarray([])
        self.depth = 5
        self.theta_points = [0, 5, 15, 25, 35, 45, 55, 65, 75, 85, 90, 95, 105, 115, 125, 135, 145, 155, 165, 175, 180]
        self.input_path = os.path.join('..', 'inputs')
        self.output_path = os.path.join('..', 'outputs')
        self.project_file = 'batch_run.txt'
        self.attenuation_file = 'batch_c.txt'
        self.absorption_file = 'batch_a.txt'
        self.scattering_file = 'batch_b.txt'
        self.sky_azimuth = 50
        self.sky_zenith = 45
        self.euler_steps_per_optical_depth = 100
        self.integrator = 'runga4'
        self.iop_type = 'petzold'
        self.sample_point_distance = 1
        self.sample_point_delta_distance = 0.01
        self.bottom_reflectance_file = 'ger_sand17.txt'
        self.sky_type = 'hlideal'
        self.sky_c = 1
        self.sky_r_dif = 0.3
        self.iface_type = 'coxmunk'
        self.ds_name = 'HL Standard'
        self.vn = 18
        self.hn = 24
        self.num_bands = 17
        self.sky_state = 'clear'
        self.surf_state = 'flat'
        self.ds_code = 'HL_' + str(self.vn) + 'x' + str(self.hn)
        self.partition = 'sphere'
        self.sky_file = 'sky_' + self.sky_state + '_z' + str(self.sky_zenith) + '_a' + str(
            self.sky_azimuth) + '_' + str(
            self.num_bands) + '_' + self.ds_code
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
        self.ld_b_image_save_file = 'image_Ld_b.ppm'
        self.ld_b_image_sens_k = 0.0008
        self.ld_b_save_file = 'Ld_b_data'
        self.verbose = 6
        self.num_cpus = -1
        self.wind_speed = 5
        self.crosswind_vertices = 100
        self.upwind_vertices = 100
        self.surface_size = 1
        self.surface_radius = 0.5
        self.tarsize = 0.2
        self.rays_per_quad = 10
        self.surface_count = 200
        self.azimuthally_average = 'yes'
        self.water_surface_file = 'sf_' + self.iface_type + '_w' + str(self.wind_speed) + '_r' + str(
            self.rays_per_quad) + '_s' + \
                                  str(self.surface_count) + '_' + self.azimuthally_average + '_mono_' + self.ds_code
        self.wind_direc = 0
        self.crosswind_vertices = 100
        self.model_eqn = 'clear'
        self.phase_function_file = 'pf_' + self.iop_type + '_mono_' + self.ds_code
        self.exec_path = '/usr/bin/jude_test/bin/'

    def write_run_parameters_to_file(self):
        """

        """
        lg.info('Writing Inputs to file : ' + self.project_file)

        # First update the file names in case we changed the file values.  the file name includes the file values
        #self.updateFileNames()

        f = open(self.project_file, 'w')

        f.write('name=' + self.project_file + '\n')
        f.write('band_count = ' + str(len(self.wavelengths)) + '\n')
        f.write('bs_name = ' + str(len(self.wavelengths)) + ' Bands (' + str(self.wavelengths[0]) + '-' + str(
            self.wavelengths[len(self.wavelengths) - 1]) + ' nm) \n')
        f.write('bs_code = ' + str(len(self.wavelengths)) + '\n')
        f.write('band_centres_data = ')
        for i in range(0, len(self.wavelengths) - 1):
            f.write(str(self.wavelengths[i]) + ',') # so we don't end with __a comma
        f.write(str(self.wavelengths[len(self.wavelengths) - 1]) + '\n')

        f.write('band_widths_data = ')
        for i in range(0, len(self.wavelengths) - 1):
            width = self.wavelengths[i + 1] - self.wavelengths[i]
            f.write(str(width) + ',')

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
        f.write('\n')
        f.write('water_surface_fp = ' + self.water_surface_file + '\n')
        f.write('\n')
        f.write('atten_fp = ' + self.attenuation_file + '\n')
        f.write('scat_fp = ' + self.scattering_file + '\n')
        f.write('pf_fp = ' + self.phase_function_file + '\n')
        f.write('\n')
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
        f.write('Ld_b_image_save_fp = ' + self.ld_b_image_save_file + '\n')
        f.write('Ld_b_image_sens_k = ' + str(self.ld_b_image_sens_k) + '\n')
        f.write('\n')
        f.write('Ld_b_save_fp = ' + self.ld_b_save_file + '\n')
        f.write('\n')
        f.write('report_save_fp = ' + self.project_file.partition('.')[
            0] + '_report.txt\n')  # this should remove the .txt out of the project file name
        f.write('\n')
        f.write('verbose = ' + str(self.verbose) + '\n')
        f.close()

    def write_sky_params_to_file(self):
        """
        @brief Writes the params to file that skytool_Free needs to generate the sky radiance distribution.
        """

        f = open(self.sky_file + '_params.txt', 'w')

        f.write('verbose=' + str(self.verbose) + '\n')
        f.write('band_count=' + str(self.num_bands) + '\n')
        f.write('band_centres_data=')
        f.write(",".join([str(wave) for wave in self.wavelengths]) + '\n')
        f.write('partition=' + self.partition + '\n')
        f.write('vn=' + str(self.vn) + '\n')
        f.write('hn=' + str(self.hn) + '\n')
        f.write('C=' + str(self.sky_c) + '\n')
        f.write('rdif=' + str(self.sky_r_dif) + '\n')
        f.write('theta_points=')
        f.write(",".join([str(theta) for theta in self.theta_points]) + '\n')
        f.write('type=' + self.sky_type + '\n')
        f.write('azimuth=' + str(self.sky_azimuth) + '\n')
        f.write('zenith=' + str(self.sky_zenith) + '\n')
        f.write('sky_save_fp=' + os.path.join(self.output_path, self.sky_file) + '\n')
        f.write('sky_image_save_fp=image_' + self.sky_file + '.ppm' + '\n')
        f.write('sky_image_size=256' + '\n')
        f.flush()
        f.close()
