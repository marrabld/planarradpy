#! /usr/bin/env python

__author__ = 'marrabld'

import getopt
import sys

sys.path.append("../")


def main(argv):
    input_file = ''
    output_file = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('test.py -i <input_file> -o <output_file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('planarrad.py -i <input_file> -o <output_file>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg

    print('Input file is :: ', input_file)
    print('Report file is :: ', output_file)


if __name__ == "__main__":
    main(sys.argv[1:])


