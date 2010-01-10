#system imports
from ConfigParser import NoSectionError
import os
import errno
import logging.config
#user-defined imports
from utils.Exceptions import *

#where the config files are stored by default
TAR_CONFIG_FILE = os.path.join(os.path.expanduser('~'), '.config', 'TarBackup', 'tar-backup.conf')
LOGGER_CONFIG_FILE = os.path.join(os.path.expanduser('~'), '.config', 'TarBackup', 'logging.conf')

__all__=['TarBackup', 'TAR_CONFIG_FILE', 'LOGGER_CONFIG_FILE'] #to prevent inadvertent imports

## @brief Class for initialising Tar backups.
# 
# This class is the starting point for tar backups. It starts up the logger,
# initialises the configuration file, etc. 
# @author Siddhu Warrier (siddhuwarrier@gmail.com)
# @date 10/01/2009
class TarBackup(object):
    
    ## @brief The constructor - accepts variable number of arguments.
    #
    # The constructor starts up the logger, verifies the contents of
    # the configuration file, etc.
    #
    # @date 10/01/2009  
    def __init__(self):
        
        #by default, unless code modified, it looks in ~/.config for both logger and config files

        #check the config files
        #1. Config File
        #if the file does not exist
        if not os.path.exists(TAR_CONFIG_FILE):
            raise FileError(errno.ENOENT, "Config File %s does not exist"\
                            %TAR_CONFIG_FILE)
        #if the path exists, but the path does not refer to a file
        if not os.path.isfile(TAR_CONFIG_FILE):
            raise FileError(errno.EINVAL, "Invalid path to config file: %s"\
                            %TAR_CONFIG_FILE)
        
        #2. Logger file
        #if the file does not exist
        if not os.path.exists(LOGGER_CONFIG_FILE):
            raise FileError(errno.ENOENT, "Logger File %s does not exist"\
                            %LOGGER_CONFIG_FILE)
        #if the path exists, but the path does not refer to a file
        if not os.path.isfile(LOGGER_CONFIG_FILE):
            raise FileError(errno.EINVAL, "Invalid path to logger file: %s"\
                            %LOGGER_CONFIG_FILE)
        
        #both files are fine
        #set up logging
        try:
            logging.config.fileConfig(LOGGER_CONFIG_FILE)
        except NoSectionError as noSectionError:
            print noSectionError.args
            raise NoSectionError(LOGGER_CONFIG_FILE)
        
        self.logger = logging.getLogger('TarBackup')
        self.logger.debug('This is a test message')
