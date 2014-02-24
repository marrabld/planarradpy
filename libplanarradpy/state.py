__author__ = 'marrabld'

import ConfigParser
import os


class State():
    def __init__(self):
        self.debug = ''

        conf = ConfigParser.ConfigParser()
        conf.read(os.path.join(os.path.dirname(__file__), 'planarradpy.conf'))
        self.debug = conf.get('Debug', 'Level')



