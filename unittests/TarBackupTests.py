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
from typeutils import FileError

#where the config files are stored by default
DEFAULT_CONFIG_FILES_LOCATION = os.path.join(os.path.expanduser('~'), '.config', 'TarBackup')
#where the template files are
LOGGER_TEMPLATE_FILE = os.path.join('../templates',\
                                    'logging-template.conf')

## @brief A simple function to recreate the template config files. 
#
# @author Siddhu Warrier (siddhuwarrier@gmail.com)
# @date 08/02/2010
def recreateTemplateConfigFile():
    #create the default dir if not exists
    try:
        os.makedirs(os.path.split(LOGGER_CONFIG_FILE)[0]) 
    except OSError as osError:
        if osError[0] == errno.EEXIST: #if directory already exists ignore
            pass
    #recreate the default config file location for other tests
    shutil.copy(LOGGER_TEMPLATE_FILE, LOGGER_CONFIG_FILE)

##@brief Set of failure tests for the config file
# @ingroup TarBackupTests
# Set of Failure tests for the TarBackup class.
# This will be extended as we go along.
# @author Siddhu Warrier (siddhuwarrier@gmail.com)
# @date 10/01/2010
class ConfigFailureTests(unittest.TestCase):

    ##@brief tests what happens when no default config files.
    #
    # @date 10/01/2009    
    def testNoDefaultConfigFiles(self):
        #delete the default config file location (if exists)
        shutil.rmtree(path = DEFAULT_CONFIG_FILES_LOCATION, ignore_errors = True)
        #it should fail with a FileError exception, with ENOENT errno
        try:
            TarBackup([], "", "")
            #if no exception, then force failure
            self.fail('Exception should have arisen')
        except FileError as errorDetails:
            self.assertEquals(errorDetails[0], errno.ENOENT)
        
        #recreate config file(s)
        recreateTemplateConfigFile()
                
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
            self.assertRaises(ConfigParser.NoSectionError, TarBackup, [], "", "")
        else:
            self.fail('Could not create logging.conf file')
            
        #recreate config file(s)
        recreateTemplateConfigFile()
            
##@brief Set of failure tests for the argument semantics
# We are not testing wrogn arg types, as this test has already been done by TypeCheckerTests
# @ingroup TarBackupTests
# Set of Failure tests for the TarBackup class.
# This will be extended as we go along.
# @author Siddhu Warrier (siddhuwarrier@gmail.com)
# @date 10/01/2010

    #@param[in] sourceDirs (List): List of source directories to be included in the TAR
    # archive
    #@param[in] destFile (String): The destination file.
    #@param[in] incrementalMetaFile (String): The file that stores the incremental backup
    # information.
    #@param All arguments that follow are optional keyword arguments
    #@param[in] excludeDirs (List): The list of directories and files (incl wildcards) 
    # to be excluded.
    #@param[in] compressionType (String): Supported - gz and bz2
    #@param[in] miscOptions (Dictionary): Supported keys: verbose, exclude-vcs
class TarBackupIllegalArgTests(unittest.TestCase):
    ##@brief Checks if TarBackup fails with the right sort of error if you ent-
    # -er invalid source directories.
    def testInvalidSourceDir(self):
        #it should fail with a OSError exception, with ENOENT errno
        try:
            TarBackup([], "", "")
            #if no exception, then force failure
            self.fail('Exception should have arisen')
        except OSError as errorDetails:
            self.assertEquals(errorDetails[0], errno.ENOENT)
        #one valid and one invalid source dir
        #it should fail with a OSError exception, with ENOENT errno
        try:
            TarBackup([os.path.expanduser("~"), ""], "", "")
            #if no exception, then force failure
            self.fail('Exception should have arisen')
        except OSError as errorDetails:
            self.assertEquals(errorDetails[0], errno.ENOENT)

    #@brief Tests to see program fails gracefully when an invalid dest file
    # is specified.
    #
    #@author Siddhu Warrier (siddhuwarrier@gmail.com)
    #@date 08/02/2010
    def testInvalidDestFile(self):
        self.assertRaises(OSError, TarBackup, [os.path.expanduser("~")], "", "")
    
    #@brief Tests to see program fails gracefully when an valid dest dir
    # is specified, but the user does not have perm to write in there.
    #
    #@author Siddhu Warrier (siddhuwarrier@gmail.com)
    #@date 08/02/2010    
    def testNoPermDestFile(self):
        #specify a dir where we're pretty sure the user does no have permission
        # to create a file. If you're running these tests as root, this will
        # fail. And anyway, you're a naughty boy for doing that.
        self.assertRaises(OSError, TarBackup, [os.path.expanduser("~")], "/usr/bin/myfile.tar", "")
    
    
        

def tarBackupTestSuite():
    suite = unittest.TestLoader().loadTestsFromTestCase(ConfigFailureTests)
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TarBackupIllegalArgTests))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(sys.stdout, verbosity=2)
    runner.run(tarBackupTestSuite())