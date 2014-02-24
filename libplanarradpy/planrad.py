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

        self.wavelengths = scipy.asarray([])
        self.a = scipy.asarray([]) # total absorption
        self.a_phi = scipy.asarray([])
        self.a_water = scipy.asarray([])
        self.a_cdom = scipy.asarray([]) # CDOM absorption
        self.bb = scipy.asarray([]) # backscatter
        self.bbp = scipy.asarray([]) # particulate scatter
        self.b_water = scipy.asarray([])
        self.b = scipy.asarray([]) # scatter
        self.c = scipy.asarray([]) # attenuation
        self.depth = 5
        self.theta_points = []  # [0, 5, 15, 25, 35, 45, 55, 65, 75, 85, 90, 95, 105, 115, 125, 135, 145, 155, 165, 175, 180]
        self.input_path = os.path.join('..', 'inputs')
        self.output_path = os.path.join('..', 'outputs')
        self.project_file = 'batch_run.txt'
        self.attenuation_file = 'batch_c.txt'
        self.absorption_file = 'batch_a.txt'
        self.scattering_file = 'batch_b.txt'
        self.sky_azimuth = 50
        self.sky_zenith = 45
        self.euler_steps_pod = 100
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
        self.i_face_0_ri = 1.34
        self.i_face_1_ri = 1.00
        self.bound_bottom_reflec_diffuse_data = 0
        self.sky_sub_quad_count = '1E6'
        self.i_face_sub_quad_count = '1E6'
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
        self.target_size = 0.2
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
        lg.message('Writing Inputs to file')

        # First update the file names in case we changed the file values.  the file name includes the file values
        #self.updateFileNames()

        f = open(self.project_file, 'w')

        f.write('name='+self.project_file+'\n')
        f.write('band_count = '+str(len(self.__wave))+'\n')
        f.write('bs_name = ' + str(len(self.__wave)) + ' Bands (' + str(self.__wave[0]) + '-' + str(self.__wave[len(self.__wave)-1]) + ' nm) \n')
        f.write('bs_code = ' + str(len(self.__wave))+'\n')
        f.write('band_centres_data = ')
        for i in range(0,len(self.__wave)-1):
            f.write(str(self.__wave[i])+',') # so we don't end with __a comma
        f.write(str(self.__wave[len(self.__wave)-1])+'\n')

        f.write('band_widths_data = ')
        for i in range(0,len(self.__wave)-1):
            width = self.__wave[i+1] - self.__wave[i]
            f.write(str(width)+',')

        f.write('\n')
        f.write('ds_name = '+self.__dsName+'\n')
        f.write('ds_code = '+self.__dsCode+'\n')
        f.write('partition = '+self.__partition+'\n')
        f.write('vn = '+str(self.__vn)+'\n')
        f.write('hn = '+str(self.__hn)+'\n')
        f.write('theta_points=')
        for i in range(0,len(self.get_theta_points())-1):
            f.write(str(self.get_theta_points()[i])+',') # so we don't end with __a comma
        f.write(str(self.get_theta_points()[len(self.get_theta_points())-1])+'\n')
        f.write('depth = '+str(self.__depth)+'\n')
        f.write('sample_point_distance = '+str(self.__samplePointDistance)+'\n')
        f.write('sample_point_delta_distance = '+str(self.__samplePointDeltaDistance)+'\n')
        f.write('\n')
        f.write('sky_fp = '+self.__skyFp+'\n') # need to create these files from sky tool
        f.write('\n') # Got to here!!!!! Need sleep.
        f.write('water_surface_fp = '+self.__waterSurfaceFp+'\n')
        f.write('\n')
        f.write('atten_fp = '+self.__attenuationFile+'\n')
        f.write('scat_fp = '+self.__scatteringFile+'\n')
        f.write('pf_fp = '+self.__phaseFunctionFp+'\n')
        f.write('\n')
        f.write('bottom_reflec_diffuse_fp = '+self.__bottomReflectanceFp+'\n')
        f.write('sky_type = '+self.__skyType+'\n')
        f.write('sky_azimuth = '+str(self.__skyAzimuth)+'\n')
        f.write('sky_zenith = '+str(self.__skyZenith)+'\n')
        f.write('sky_C = '+str(self.__skyC)+'\n')
        f.write('sky_rdif = '+str(self.__skyRDif)+'\n')
        f.write('iface_type = '+self.__ifaceType+'\n')
        f.write('iface_refrac_index_0 = '+str(self.__iFace0RI)+'\n')
        f.write('iface_refrac_index_1 = '+str(self.__iFace1RI)+'\n')
#        f.write('iop_atten_data = 1\n')
#        f.write('iop_absorp_data = 0\n')
        f.write('iop_type = '+self.__iopType+'\n')
        f.write('iop_backscatter_proportion_list = ' +str(self.__backscatterproportionlist)+'\n')

        f.write('bound_bottom_reflec_diffuse_data = '+str(self.__boundBottomReflecDiffuseData)+'\n')
        f.write('sky_sub_quad_count = '+self.__skySubQuadCount+'\n')
        f.write('iface_sub_quad_count = '+self.__iFaceSubQuadCount+'\n')
        f.write('pf_sub_quad_count = '+self.__pFSubQuadCount+'\n')
        f.write('integrator = ' + self.__integrator + '\n')
        f.write('euler_steps_per_optical_depth = ' + str(self.__eulerStepsPOD) +'\n')
        f.write('midpoint_steps_per_optical_depth = '+str(self.__midpointStepsPerOpticalDepth)+'\n')
        f.write('runga4_steps_per_optical_depth = '+str(self.__runga4StepsPerOpticalDepth)+'\n')
        f.write('runga4adap_min_steps_per_optical_depth = '+str(self.__runga4adapMinStepsPerOpticalDepth)+'\n')
        f.write('runga4adap_max_steps_per_optical_depth = '+str(self.__runga4adapMaxStepsPerOpticalDepth)+'\n')
        f.write('runga4adap_min_error = '+str(self.__runga4adapMinError)+'\n')
        f.write('runga4adap_max_error = '+str(self.__runga4adapMaxError)+'\n')
        f.write('\n')
        f.write('Ld_b_image_save_fp = '+self.__LdBImageSaveFp+'\n')
        f.write('Ld_b_image_sens_k = '+str(self.__LdBImageSensK)+'\n')
        f.write('\n')
        f.write('Ld_b_save_fp = '+self.__LdBSaveFp+'\n')
        f.write('\n')
        f.write('report_save_fp = '+self.__projectFile.partition('.')[0]+'_report.txt\n') # this should remove the .txt out of the project file name
        f.write('\n')
        f.write('verbose = '+str(self.__verbose)+'\n')

        f.close()