##@defgroup Exceptions User-defined Exception classes
# @brief User-defined exceptions as Python's built-in exceptions are too few.
#
# This package contains several user-defined exception classes to supplement
# Python's all-too-few built-in exceptions.
# @author Siddhu Warrier (siddhuwarrier@gmail.com)
# @author 1 Alderton Close, Liverpool L26 9SB  
# @date 10/01/2009
from errno import errorcode
import errno

__all__ = ['FileError'] #to prevent inadvertent imports

## @brief Class for FileErrors.
#
# @ingroup Exceptions
# The different kinds of file errors are identified using
# the enumerators which use the errno.h numbers
# @param[in] errcode Error code which should be in the list of error codes in errno module.
# @param[in] strerror Human-readable string describing error.
# @author Siddhu Warrier (siddhuwarrier@gmail.com)  
# @date 10/01/2009
class FileError(Exception):
    def __init__(self, errcode, strerror):
        if errcode not in errorcode.keys():
            raise Exception(errno.EINVAL, "FileError: Invalid Error Code")
        #set the exception args (errno, strerror)
        self.args = (errcode, "FileError: %s"%strerror)      
            