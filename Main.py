#!/usr/bin/env python

##@mainpage TarBackup
#
# TarBackup is a very simple module to create backups of folders
# specified in a configuration file, using the tar command.
#
# TarBackup's sister-module, the yet-to-be-written TarCron, can
# be used to schedule TarBackup on cron.
#
# @author Siddhu Warrier (siddhuwarrier@gmail.com)
# @author 1 Alderton Close, Liverpool L26 9SB  
# @date 10/01/2009

#system imports
from ConfigParser import NoSectionError
import os
import shutil
import sys
import errno
#user-defined imports
from utils.Exceptions import *
from processing.TarBackup import *
import optparse

__all__= []
#global variables.
CONFIG_TEMPLATE_FILE = os.path.join(os.path.split(sys.argv[0])[0], 'templates', 'tar-backup-template.conf')
LOGGER_TEMPLATE_FILE = os.path.join(os.path.split(sys.argv[0])[0], 'templates', 'logging-template.conf')

## @brief The main function.
#
#This is the function that starts the program up. This function is called by the 
# if __name__ == "__main__" construct.
# @date 10/01/2009    
def main():
    #try starting up the program    
    try:
        TarBackup([], "", compressionType = "gz")
    #file error; does not exist or invalid
    except FileError as (errorcode, strerror): 
        #if the file does not exist, create template config file in the default location
        if errorcode == errno.ENOENT:
            #copy over template config file
            #create the default dir if not exists
            try:
                os.makedirs(os.path.split(LOGGER_CONFIG_FILE)[0]) 
            except OSError as osError:
                if osError[0] == errno.EEXIST: #if directory already exists ignore
                    pass
            #now copy over both files.
            ##TODO: If one of the files already exists, it is overwritten. Modify behaviour.
        
            shutil.copy(LOGGER_TEMPLATE_FILE, LOGGER_CONFIG_FILE)
            
            print "Config files recreated. Please restart TarBackup.\n\
If any one of them existed previously, they will have been recreated, and \
all of your changes will have been lost. Sorry."
        else:
            #This is if the path is invalid, or anything else.
            sys.stderr.write("FileError[%s]: %s"%(errorcode, strerror))
    
    #invalid logging config file
    except NoSectionError as noSectionError:         
        sys.stderr.write(noSectionError.args[0] + '. Invalid logger config file?')
    #arguments missing
    except NameError as nameError:
        sys.stderr.write("NameError: %s."%nameError.args[0])
    except TypeError as typeError:
        sys.stderr.write("TypeError: %s" %typeError.args[0])

#application execution starts here.
if __name__ == "__main__":
    main()
    