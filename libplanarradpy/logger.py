__author__ = 'marrabld'

import logging.config
import os

log_conf_file = os.path.join(os.path.dirname(__file__), 'logging.conf')
print(log_conf_file)
#log_conf_file = ('logging.conf')
logging.config.fileConfig(log_conf_file)

# create logger
logger = logging.getLogger('libplanarradpy')


def clear_log():
    """
    This method will clear the log file by reopening the file for writing.
    """
    with open('libplanarradpy.log', 'w'):
        pass


def clear_err():
    """
    This method will clear the log file by reopening the file for writing.
    """

    with open('libplanarradpy.err', 'w'):
        pass