##@defgroup TarBackupTests Unit Tests for processing/TarBackup.py
# @brief Unit Tests for processing/TarBackup.py 
#
# This package contains (mostly failure) unit tests
# for processing/TarBackup.py. 
#
# @author Siddhu Warrier (siddhuwarrier@gmail.com)  
# @date 10/01/2009

import ConfigParser
import unittest
import os
import shutil
import commands
import errno
import sys
#user defined imports
from processing import TarBackup, LOGGER_CONFIG_FILE
from utils import FileError

#where the config files are stored by default
DEFAULT_CONFIG_FILES_LOCATION = os.path.join(os.path.expanduser('~'), '.config', 'TarBackup')
#where the template files are
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
            TarBackup([], "")
            #if no exception, then force failure
            self.fail('Exception should have arisen')
        except FileError as errorDetails:
            self.assertEquals(errorDetails[0], errno.ENOENT)
        
        #recreate the default config file location for other tests
        
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
        #create fake logger file
        output = commands.getstatusoutput('touch %s'%os.path.join(DEFAULT_CONFIG_FILES_LOCATION,\
                                                                           'logging.conf'))
        
        #test to see if NoSectionError raised
        if output[0] == 0:
            self.assertRaises(ConfigParser.NoSectionError, TarBackup, [], "")
        else:
            self.fail('Could not create logging.conf file')
            
class TypeSuccessTests(unittest.TestCase):
    
    ## @brief Performs set up operations before test cases are executed.
    #
    # This module recreates the logger config file 
    # @date 18/01/2010    
    def setUp(self):
        #recreate the default config file location for other tests      
        try:  
            os.makedirs(os.path.split(LOGGER_CONFIG_FILE)[0])
        except OSError as (errnum, strerror):
            
            if errnum == errno.EEXIST:
                pass
            else:
                raise OSError
        #now copy over both files.
        ##TODO: If one of the files already exists, it is overwritten. Modify behaviour.
        shutil.copy(LOGGER_TEMPLATE_FILE, LOGGER_CONFIG_FILE)
        
    ## @brief Tests TarBackup if no keyword arguments are provided.
    #
    # This test case initialises TarBackup with all of the required arguments
    # and none of the optional keyword arguments 
    # @date 18/01/2010
    def testNoOptionalKeywordArguments(self):
        try:
            TarBackup([], "")
        except Exception as error:
            self.fail("Exception" + str(error.args) + "raised.")
    
    ## @brief Tests TarBackup if only some keyword arguments are specified
    #
    # This test case initialises TarBackup with all of the required arguments
    # and some of the optional arguments.
    # @date 19/01/2010
    def testSomeOptionalKeywordArguments(self):
        try:
            TarBackup([], "", excludeDirs = [])
        except Exception as error:
            self.fail("Exception" + str(error.args) + "raised.")
    
    ## @brief Tests TarBackup if only some keyword arguments are specified
    #
    # This test case initialises TarBackup with all of the required arguments
    # and all of the optional arguments.
    # @date 19/01/2010
    def testAllOptionalKeywordArguments(self):
        #"compressionType", "miscOptions", "excludeDirs"
        try:
            TarBackup([], "", compressionType = "gz", miscOptions = {"blah":2}, excludeDirs = [])
        except Exception as error:
            self.fail("Exception" + str(error.args) + "raised.")        
    
    def testCompulsoryArgumentsAsKeywordArguments(self):
        try:
            TarBackup(sourceDirs = [], destFile = "", compressionType = "gz", miscOptions = {"blah":2}, excludeDirs = [])
        except Exception as error:
            self.fail("Exception" + str(error.args) + "raised.")        
        


def typeSuite():
    suite = unittest.TestLoader().loadTestsFromTestCase(TypeSuccessTests)

    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(sys.stdout, verbosity=2)
    runner.run(typeSuite())