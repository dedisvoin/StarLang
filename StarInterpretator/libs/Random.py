from source.structures import star_functions
from source.structures import star_types
from source.structures.star_functions import PyFunctionWaitArg as PFWA

from source.core import errors


import random

FP = star_functions.PyFunctionPack()
CP = star_functions.PyConstantsPack()

# seed function
@star_functions.CreatePyFunction(
    FP,
    'seed',
    True,
    [PFWA('seed', types=[star_types.Star_T_Int, star_types.Star_T_Float])]
)
def _(args: list[star_types.StarValue], error_handler: errors.ErrorHandler) -> star_types.StarValue:
    random.seed(args[0].get_value())
    return star_types.Star_V_Null.set_value(None)


# random function
@star_functions.CreatePyFunction(
    FP,
    'random',
    True,
    []
)
def _(args: list[star_types.StarValue], error_handler: errors.ErrorHandler) -> star_types.StarValue:
    return star_types.Star_V_Float.set_value(random.random())

# randint function
@star_functions.CreatePyFunction(
    FP,
    'randint',
    True,
    [PFWA('min', types=[star_types.Star_T_Int, star_types.Star_T_Float]), PFWA('max', types=[star_types.Star_T_Int, star_types.Star_T_Float])]
)
def _(args: list[star_types.StarValue], error_handler: errors.ErrorHandler) -> star_types.StarValue:
    return star_types.Star_V_Int.set_value(random.randint(int(args[0].get_value()), int(args[1].get_value())))

# choise function
@star_functions.CreatePyFunction(
    FP,
    'choice',
    True,
    [PFWA('list', types=[star_types.Star_T_List])]
)
def _(args: list[star_types.StarValue], error_handler: errors.ErrorHandler) -> star_types.StarValue:
    return random.choice(args[0].get_value())


