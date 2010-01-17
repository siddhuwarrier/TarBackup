##@package utils
# @brief Utilities to assist in the operation of the backup (contains other packages). 
#
# This package provides utilities. Right now, it contains
# only user-defined exceptions
#
# @author Siddhu Warrier (siddhuwarrier@gmail.com)
# @author 1 Alderton Close, Liverpool L26 9SB  
# @date 10/01/2009

__all__ = ['Exceptions']
from Exceptions import *
from TypeChecker import *