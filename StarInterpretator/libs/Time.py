"""
Time-related functions for the Star programming language.

This module provides functions for working with time, including getting the current time
and adding delays to program execution.

Functions:
    time(): Returns the current time in seconds since the epoch
    sleep(value): Suspends execution for the specified number of seconds
"""

from source.structures.star_functions import PyFunctionWaitArg as PFWA
from source.structures import star_functions
from source.structures import star_types

from source.core import errors


import time


FP = star_functions.PyFunctionPack()
CP = star_functions.PyConstantsPack()


# time
@star_functions.CreatePyFunction(
    FP, 'time', True, []
)
def _(args: list[star_types.StarValue], error_handler: errors.ErrorHandler) -> star_types.StarValue:
    """
    Returns the current time in seconds since the epoch as a floating point number.
    
    The time is measured in seconds since the epoch, which is platform dependent.
    On Unix systems, the epoch is January 1, 1970, 00:00:00 (UTC).
    
    Args:
        args: List of StarValue arguments (empty for this function)
        error_handler: Error handler instance for managing runtime errors
        
    Returns:
        StarValue: A Star_V_Float containing the current time in seconds
        
    Example:
        current_time = time()  # Returns current time as float
    """
    return star_types.Star_V_Float.set_value(time.time())

# sleep
@star_functions.CreatePyFunction(
    FP, 'sleep', True, [PFWA('value', types=[star_types.Star_T_Int])]
)
def _(args: list[star_types.StarValue], error_handler: errors.ErrorHandler) -> star_types.StarValue:
    """
    Suspends execution for the given number of seconds.
    
    This function will pause the program execution for at least the specified number
    of seconds. The actual suspension time may be longer due to system scheduling
    or other factors.
    
    Args:
        args: List of StarValue arguments containing:
            - args[0]: Star_T_Int value representing seconds to sleep
        error_handler: Error handler instance for managing runtime errors
        
    Returns:
        StarValue: Star_V_Null indicating no return value
        
    Example:
        sleep(5)  # Pauses execution for 5 seconds
        
    Note:
        The function accepts only integer values for the sleep duration.
        For sub-second precision, consider implementing a millisecond-based sleep function.
    """
    time.sleep(args[0].get_value())
    return star_types.Star_V_Null.set_value(None)