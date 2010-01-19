import sys

__all__ = ["require"]

## @brief Decorator for type checking.
# 
# This method performs type checking for Python function arguments.
# This code is modified from Per Vognsen's ActiveState recipe 454322
# http://code.activestate.com/recipes/454322/
# Vognsen's code has been cleaned up and modified in order to 
# support checking multiple kwargs.
# It also performs checks as to whether the kwarg provided is valid.
# 
# @throws NameError When argument invalid, or required argument not found.
# @throws TypeError When argument type does not match argument type expected.
# @author Siddhu Warrier (siddhuwarrier@gmail.com)
# @date 17/01/2009
def require(validKwargs, kwargsCompulsory = False, **typeMap):
    def makeWrapper(functionName):
        #when functionName is the function to decorate
        if hasattr(functionName, "wrapped_args"):
            print functionName, "has attr wrapped_args:", getattr(functionName, "wrapped_args")
            wrapped_args = getattr(functionName, "wrapped_args")
            
        #when functionName is the nested wrapper function.
        else:
            code = functionName.func_code
            wrapped_args = list(code.co_varnames[:code.co_argcount]) #adds everything except kwargs
            #print wrapped_args
            if 'args' in functionName.func_code.co_varnames:
                sys.stderr.write("Warning: Variable length args cannot be type-checked.")

        #wrapper function
        def wrapper(*args, **kwargs):
            for kwArgName in kwargs.keys():
                #remember, we can specify the positional arguments as kwargs as well.
                if kwArgName not in validKwargs and kwArgName not in wrapped_args:
                    validKwargList = " or ".join(str(validKwarg) for validKwarg in validKwargs)
                    raise NameError, "Invalid keyword argument %s. \
                    Supported keyword arguments (not inclusive of the positional arguments): %s."\
                    %(kwArgName, validKwargList)
                if kwArgName not in wrapped_args:
                    wrapped_args.append(kwArgName)
            
            errorMsg = "Expected '%s' to be %s; was %s."
            for argumentNameToCheck in typeMap.keys():
                #get the argument index
                try:
                    argIdx = wrapped_args.index(argumentNameToCheck)
                except ValueError:
                    if argumentNameToCheck in validKwargs and kwargsCompulsory == False:
                        print "Warning: Cannot find keyword argument %s.\n"%argumentNameToCheck
                        continue
                    else:
                        raise NameError, "Cannot find argument %s."%argumentNameToCheck
                
                #define the error message
                typeList = " or ".join(str(allowedType) for allowedType in typeMap[argumentNameToCheck])
                
                #first check the positional arguments
                if len(args) > argIdx:
                    arg = args[argIdx]
                else: #check if it is a keyword argument
                    #if in keyword args, run the check
                    try:
                        arg = kwargs[argumentNameToCheck]
                    except:
                        raise NameError, "Compulsory argument %s missing."\
                        %argumentNameToCheck
                
                raiseTypeError = True #raise type error unless we are able to match
                #the type of the arg to the allowed types
                for allowedType in typeMap[argumentNameToCheck]:
                    #can be done: make this more permissive.
                    if isinstance(arg, allowedType):
                        raiseTypeError = False
                        break
                
                #if none of the allowed types matched, then sod it, raise a TypeError
                if raiseTypeError:
                    raise TypeError, errorMsg%(str(argumentNameToCheck), typeList, type(arg))
                
            #remove all the optional keyword arguments for if another instance of the same class is instantiated
            #the other arguments are added in when the class is first read by the interpreter.
            for kwargName in validKwargs:
                if kwargName in wrapped_args:
                    wrapped_args.remove(kwargName)
                      
                        
            #call the function and return
            return functionName(*args, **kwargs)
        #return from make_wrapper
        return wrapper
    #return from require
    return makeWrapper
