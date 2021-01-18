__author__ = 'marrabld'

import configparser
import os


class State():
    def __init__(self):
        self.debug = ''

        conf = configparser.ConfigParser()
        conf.read(os.path.join(os.path.dirname(__file__), 'planarradpy.conf'))
        self.debug = conf.get('Debug', 'Level')



