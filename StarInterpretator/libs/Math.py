from source.structures.star_functions import PyFunctionWaitArg as PFWA
from source.structures import star_functions
from source.structures import star_types


from source.core import errors

import math

FP = star_functions.PyFunctionPack()
CP = star_functions.PyConstantsPack()

# sin function
@star_functions.CreatePyFunction(
        FP, 'sin', True, 
        [PFWA('x', types=[star_types.Star_T_Float, star_types.Star_T_Int])]
)
def _(args: list[star_types.StarValue], error_handler: errors.ErrorHandler) -> star_types.StarValue:
    return star_types.Star_V_Float.set_value(math.sin(args[0].get_value()))




# cos function
@star_functions.CreatePyFunction(
        FP, 'cos', True, 
        [PFWA('x', types=[star_types.Star_T_Float, star_types.Star_T_Int])]
)
def _(args: list[star_types.StarValue], error_handler: errors.ErrorHandler) -> star_types.StarValue:
    return star_types.Star_V_Float.set_value(math.cos(args[0].get_value()))




# tan function
@star_functions.CreatePyFunction(
        FP, 'tan', True,
        [PFWA('x', types=[star_types.Star_T_Float, star_types.Star_T_Int])]
)
def _(args: list[star_types.StarValue], error_handler: errors.ErrorHandler) -> star_types.StarValue:
    return star_types.Star_V_Float.set_value(math.tan(args[0].get_value()))




# asin function
@star_functions.CreatePyFunction(
        FP, 'asin', True,
        [PFWA('x', types=[star_types.Star_T_Float, star_types.Star_T_Int])]
)
def _(args: list[star_types.StarValue], error_handler: errors.ErrorHandler) -> star_types.StarValue:
    return star_types.Star_V_Float.set_value(math.asin(args[0].get_value()))




# acos function
@star_functions.CreatePyFunction(
        FP, 'acos', True,
        [PFWA('x', types=[star_types.Star_T_Float, star_types.Star_T_Int])]
)
def _(args: list[star_types.StarValue], error_handler: errors.ErrorHandler) -> star_types.StarValue:
    return star_types.Star_V_Float.set_value(math.acos(args[0].get_value()))




# atan function
@star_functions.CreatePyFunction(
        FP, 'atan', True,
        [PFWA('x', types=[star_types.Star_T_Float, star_types.Star_T_Int])]
)
def _(args: list[star_types.StarValue], error_handler: errors.ErrorHandler) -> star_types.StarValue:
    return star_types.Star_V_Float.set_value(math.atan(args[0].get_value()))




# atan2 function
@star_functions.CreatePyFunction(
        FP, 'atan2', True,
        [PFWA('y', types=[star_types.Star_T_Float, star_types.Star_T_Int]),
         PFWA('x', types=[star_types.Star_T_Float, star_types.Star_T_Int])]
)
def _(args: list[star_types.StarValue], error_handler: errors.ErrorHandler) -> star_types.StarValue:
    return star_types.Star_V_Float.set_value(math.atan2(args[0].get_value(), args[1].get_value()))




# sinh function
@star_functions.CreatePyFunction(
        FP, 'sinh', True,
        [PFWA('x', types=[star_types.Star_T_Float, star_types.Star_T_Int])]
)
def _(args: list[star_types.StarValue], error_handler: errors.ErrorHandler) -> star_types.StarValue:
    return star_types.Star_V_Float.set_value(math.sinh(args[0].get_value()))




# cosh function
@star_functions.CreatePyFunction(
        FP, 'cosh', True,
        [PFWA('x', types=[star_types.Star_T_Float, star_types.Star_T_Int])]
)
def _(args: list[star_types.StarValue], error_handler: errors.ErrorHandler) -> star_types.StarValue:
    return star_types.Star_V_Float.set_value(math.cosh(args[0].get_value()))




# tanh function
@star_functions.CreatePyFunction(
        FP, 'tanh', True,
        [PFWA('x', types=[star_types.Star_T_Float, star_types.Star_T_Int])]
)
def _(args: list[star_types.StarValue], error_handler: errors.ErrorHandler) -> star_types.StarValue:
    return star_types.Star_V_Float.set_value(math.tanh(args[0].get_value()))




# pow function
@star_functions.CreatePyFunction(
        FP, 'pow', True,
        [PFWA('x', types=[star_types.Star_T_Float, star_types.Star_T_Int]),
         PFWA('y', types=[star_types.Star_T_Float, star_types.Star_T_Int])]
)
def _(args: list[star_types.StarValue], error_handler: errors.ErrorHandler) -> star_types.StarValue:
    return star_types.Star_V_Float.set_value(math.pow(args[0].get_value(), args[1].get_value()))




# sqrt function
@star_functions.CreatePyFunction(
        FP, 'sqrt', True,
        [PFWA('x', types=[star_types.Star_T_Float, star_types.Star_T_Int])]
)
def _(args: list[star_types.StarValue], error_handler: errors.ErrorHandler) -> star_types.StarValue:
    return star_types.Star_V_Float.set_value(math.sqrt(args[0].get_value()))





# abs function
@star_functions.CreatePyFunction(
        FP, 'abs', True,
        [PFWA('x', types=[star_types.Star_T_Float, star_types.Star_T_Int])]
)
def _(args: list[star_types.StarValue], error_handler: errors.ErrorHandler) -> star_types.StarValue:
    return star_types.Star_V_Float.set_value(math.fabs(args[0].get_value()))