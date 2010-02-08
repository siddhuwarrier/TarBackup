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
# @date 10/01/2009

#system imports
from ConfigParser import NoSectionError
import os
import shutil
import sys
import errno
#user-defined imports
from typeutils.Exceptions import * 
from processing.TarBackup import *

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
        TarBackup(["~/workspace/personal"], "~/personal_workspace_backup", "~/personal_workspace_backup.snar", 
                  compressionType = "gz", excludeDirs = ["~/workspace/personal/Pydocs"], 
                  miscOptions = ["verbos"])
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
            print("FileError[%s]: %s"%(errorcode, strerror))
    
    #invalid logging config file
    except NoSectionError as noSectionError:         
        print(noSectionError.args[0] + '. Invalid logger config file?')
    #arguments missing
    except NameError as nameError:
        print("NameError: %s"%nameError.args[0])
    except TypeError as typeError:
        print("TypeError: %s" %typeError.args[0])
    except IllegalArgumentError as illegalArgumentError: 
        print("IllegalArgumentError: %s" %illegalArgumentError.args[0])

#application execution starts here.
if __name__ == "__main__":
    main()
    