##@defgroup TarBackupTests Unit Tests for processing/TarBackup.py
# @brief Unit Tests for processing/TarBackup.py 
#
# This package contains (mostly failure) unit tests
# for processing/TarBackup.py. 
#
# @author Siddhu Warrier (siddhuwarrier@gmail.com)
# @author 1 Alderton Close, Liverpool L26 9SB  
# @date 10/01/2009

import ConfigParser
import unittest
import os
import shutil
import commands
import errno
#user defined imports
from processing import TarBackup
from utils import FileError

#where the config files are stored by default
DEFAULT_CONFIG_FILES_LOCATION = os.path.join(os.path.expanduser('~'), '.config', 'TarBackup')
#where the template files are
CONFIG_TEMPLATE_FILE = os.path.join('../templates',\
                                    'tar-backup-template.conf')
LOGGER_TEMPLATE_FILE = os.path.join('../templates',\
                                    'logging-template.conf')

##@brief Set of failure tests
# @ingroup TarBackupTests
# Set of Failure tests for the TarBackup class.
# This will be extended as we go along.
# @author Siddhu Warrier (siddhuwarrier@gmail.com)
# @date 10/01/2009
class ConfigFailureTests(unittest.TestCase):

    ##@brief tests what happens when no default config files.
    #
    # @date 10/01/2009    
    def testNoDefaultConfigFiles(self):
        #delete the default config file location (if exists)
        shutil.rmtree(path = DEFAULT_CONFIG_FILES_LOCATION, ignore_errors = True)
        #it should fail with a FileError exception, with ENOENT errno
        try:
            TarBackup()
            #if no exception, then force failure
            self.fail('Exception should have arisen')
        except FileError as errorDetails:
            self.assertEquals(errorDetails[0], errno.ENOENT)
        
    ##@brief tests when logger file corrupt.
    #
    # @date 10/01/2009
    def testCorruptLoggerFile(self):
        #delete the default config file location (if exists)
        shutil.rmtree(path = DEFAULT_CONFIG_FILES_LOCATION, ignore_errors = True)
        #create the directory and create fake files
        try:
            os.makedirs(DEFAULT_CONFIG_FILES_LOCATION) 
        except OSError as osError:
            if osError[0] == errno.EEXIST: #if directory already exists ignore
                pass
        #create proper config file
        shutil.copy(CONFIG_TEMPLATE_FILE, os.path.join(DEFAULT_CONFIG_FILES_LOCATION,\
                                                               'tar-backup.conf'))
        #create fake logger file
        output = commands.getstatusoutput('touch %s'%os.path.join(DEFAULT_CONFIG_FILES_LOCATION,\
                                                                           'logging.conf'))
        
        #test to see if NoSectionError raised
        if output[0] == 0:
            self.assertRaises(ConfigParser.NoSectionError, TarBackup)
        else:
            self.fail('Could not create logging.conf file')
            
        #delete the default config file location (if exists)
        shutil.rmtree(path = DEFAULT_CONFIG_FILES_LOCATION, ignore_errors = True)            

if __name__ == '__main__':
    unittest.main()