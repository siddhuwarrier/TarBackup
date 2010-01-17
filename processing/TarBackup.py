#system imports from python library
from ConfigParser import NoSectionError
import os
import errno
import logging.config
#user-defined imports
from utils.Exceptions import *
from utils.TypeChecker import *

#where the config files are stored by default
LOGGER_CONFIG_FILE = os.path.join(os.path.expanduser('~'), '.config', 'TarBackup', 'logging.conf')

__all__=['TarBackup', 'LOGGER_CONFIG_FILE'] #to prevent inadvertent imports

## @brief Class for initialising Tar backups.
# 
# This class is the starting point for tar backups. It starts up the logger,
# initialises the configuration file, etc.
#
# @throws FileError Expection thrown when file not found.
# @throws NoSectionError Exception thrown when logger file corrupt. 
# @author Siddhu Warrier (siddhuwarrier@gmail.com)
# @date 10/01/2009
class TarBackup(object):
    ## @brief The constructor - accepts variable number of arguments.
    #
    # The constructor sets up the params required to get the Tar backup started.
    #
    #@param[in] sourceDirs (List): List of source directories to be included in the TAR
    # archive
    #@param All arguments are keyword arguments
    #@param[in] destFile (String): The destination file.
    #@param[in] excludeDirs (List): The list of directories and files (incl wildcards) 
    # to be excluded.
    #@param[in] compressionType (String): Supported - gz and bz2
    #@param[in] miscOptions (Dictionary): Supported keys: verbose, exclude-vcs
    # @date 10/01/2009
    @require(validKwargs = ["compressionType", "miscOptions", "excludeDirs"], \
             sourceDirs = (list,), destFile = (str, ), compressionType = (str,),\
             miscOptions = (dict, ), excludeDirs = (list, ))
    def __init__(self, sourceDirs, destFile, **kwargs):
        #by default, unless code modified, it looks in ~/.config for both logger and config files
        #check config files
        #1. Logger file
        #if the file does not exist
        if not os.path.exists(LOGGER_CONFIG_FILE):
            raise FileError(errno.ENOENT, "Logger File %s does not exist"\
                            %LOGGER_CONFIG_FILE)
        #if the path exists, but the path does not refer to a file
        if not os.path.isfile(LOGGER_CONFIG_FILE):
            raise FileError(errno.EINVAL, "Invalid path to logger file: %s"\
                            %LOGGER_CONFIG_FILE)
        
        #set up logging
        try:
            logging.config.fileConfig(LOGGER_CONFIG_FILE)
        except NoSectionError as noSectionError:
            print noSectionError.args
            raise NoSectionError(LOGGER_CONFIG_FILE)
        
        
        self.logger = logging.getLogger('TarBackup')
        self.logger.debug("Test")
        
