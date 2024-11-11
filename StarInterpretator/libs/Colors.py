from source.structures import star_functions
from source.structures import star_types
from source.structures.star_functions import PyFunctionWaitArg as PFWA
from source.core import errors


FP = star_functions.PyFunctionPack()
CP = star_functions.PyConstantsPack()


CP.add(star_functions.PyStarConstant('red',     star_types.Star_V_String.set_value('\033[31m')))
CP.add(star_functions.PyStarConstant('green',   star_types.Star_V_String.set_value('\033[32m')))
CP.add(star_functions.PyStarConstant('yellow',  star_types.Star_V_String.set_value('\033[33m')))
CP.add(star_functions.PyStarConstant('blue',    star_types.Star_V_String.set_value('\033[34m')))
CP.add(star_functions.PyStarConstant('magenta', star_types.Star_V_String.set_value('\033[35m')))
CP.add(star_functions.PyStarConstant('cyan',    star_types.Star_V_String.set_value('\033[36m')))
CP.add(star_functions.PyStarConstant('white',   star_types.Star_V_String.set_value('\033[37m')))
CP.add(star_functions.PyStarConstant('reset',   star_types.Star_V_String.set_value('\033[0m')))

CP.add(star_functions.PyStarConstant('bold',    star_types.Star_V_String.set_value('\033[1m')))
CP.add(star_functions.PyStarConstant('underline',star_types.Star_V_String.set_value('\033[4m')))
CP.add(star_functions.PyStarConstant('blink',   star_types.Star_V_String.set_value('\033[5m')))
CP.add(star_functions.PyStarConstant('reverse', star_types.Star_V_String.set_value('\033[7m')))
CP.add(star_functions.PyStarConstant('hidden',  star_types.Star_V_String.set_value('\033[8m')))
CP.add(star_functions.PyStarConstant('black',   star_types.Star_V_String.set_value('\033[30m')))

@star_functions.CreatePyFunction(
        FP, 'count', True,
        [PFWA('string', types=[star_types.Star_T_String]), 
         PFWA('char', types=[star_types.Star_T_String])]
)
def _(args: list[star_types.StarValue], error_handler: errors.ErrorHandler) -> star_types.StarValue:
    return star_types.Star_V_Int.set_value(args[0].get_value().count(args[1].get_value()))