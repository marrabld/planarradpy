#! /usr/bin/env python

__author__ = 'marrabld'

import os

#print(os.getcwd())
#os.chdir(os.path.join(os.getcwd(),  'libplanarradpy'))
import subprocess
import getopt
import sys
import libplanarradpy.planrad as pr
import numpy as np

#sys.path.append("../")


def main(argv):
    input_file = ''
    output_file = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('Launching GUI')
        p = subprocess.Popen("./gui/gui_mainLayout.py", shell=True)
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('planarrad.py -i <input_file> -o <output_file>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg
        elif opt in ("-g", "--gui"):
            print('Launching GUI -g')
            p = subprocess.Popen("./gui/gui_mainLayout.py")
            sys.exit()

    #print('Input file is :: ', input_file)
    #print('Report file is :: ', output_file)

    input_parameters = pr.FileTools.read_param_file_to_dict(input_file)
    #--------------------------------------------------#
    # build the required objects
    #--------------------------------------------------#
    rp = pr.RunParameters(input_parameters['wavelengths'])
    rp.verbose = input_parameters['verbose']
    rp.num_cpus = int(input_parameters['num_cpus'])
    rp.exec_path = input_parameters['exec_path']
    rp.phytoplankton_absorption_file = input_parameters['phytoplankton_absorption_file']
    rp.bottom_reflectance_file = input_parameters['bottom_reflectance_file']

    #--------------------------------------------------#
    # update the file names ?
    #--------------------------------------------------#

    #--------------------------------------------------#
    # rebuild the iop files ?
    #--------------------------------------------------#

    # --------------------------------------------------#
    # Check to see if the new syntax of <start>:<stop>:<increment>
    # Is being used.  If it is mangle the string in to place
    # --------------------------------------------------#

    input_param_list = ['saa_list', 'sza_list', 'p_list', 'x_list', 'y_list', 'g_list', 's_list', 'z_list']

    for param in input_param_list:
        if ':' in input_parameters[param]:
            try:
                sub_string = input_parameters[param].split(':')
                param_start = float(sub_string[0])
                param_stop = float(sub_string[1])
                param_inc = int(sub_string[2])

                tmp_param =  str(np.linspace(param_start, param_stop, param_inc))
                tmp_param = ' '.join(tmp_param.split(None))
                tmp_param = str(tmp_param).replace(' ', ',')
                tmp_param = tmp_param.replace('[,', '[')
                tmp_param = tmp_param.replace(',]', ']')

                #myList = ','.join(map(str, myList))

                input_parameters[param] = tmp_param

            except:
                print('error')
                raise


    saa_list = pr.HelperMethods.string_to_float_list(input_parameters['saa_list'])
    sza_list = pr.HelperMethods.string_to_float_list(input_parameters['sza_list'])
    p_list = pr.HelperMethods.string_to_float_list(input_parameters['p_list'])
    x_list = pr.HelperMethods.string_to_float_list(input_parameters['x_list'])
    y_list = pr.HelperMethods.string_to_float_list(input_parameters['y_list'])
    g_list = pr.HelperMethods.string_to_float_list(input_parameters['g_list'])
    s_list = pr.HelperMethods.string_to_float_list(input_parameters['s_list'])
    z_list = pr.HelperMethods.string_to_float_list(input_parameters['z_list'])

    batch_name = input_parameters['batch_name']

    br = pr.BatchRun(rp, batch_name)
    br.batch_parameters(saa_list,
                        sza_list,
                        p_list,
                        x_list,
                        y_list,
                        g_list,
                        s_list,
                        z_list)

    br.generate_directories()
    br.run()

    rt = pr.ReportTools()
    rt.write_batch_report(os.path.abspath(os.path.join('./outputs', batch_name)), input_parameters['report_parameter'])


if __name__ == "__main__":
    main(sys.argv[1:])


