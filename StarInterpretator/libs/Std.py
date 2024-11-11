from copy import copy, deepcopy
from source.structures.star_functions import PyFunctionWaitArg as PFWA
from source.structures import star_functions
from source.structures import star_types
from source.structures import star_lambdas

from source.core import errors
from source.parser.instructions import get_rec_values

from sys import getsizeof
from colorama import Fore


FP = star_functions.PyFunctionPack()
CP = star_functions.PyConstantsPack()


# filter
@star_functions.CreatePyFunction(
        FP,
        'filter',
        True,
        [PFWA('iterable [list, dict]', types=[star_types.Star_T_List]), PFWA('function', types=[star_types.Star_T_LambdaFunc])]
)
def _(args: list[star_types.StarValue], error_handler: errors.ErrorHandler) -> star_types.StarValue:

    array = args[0].get_value()
    lambdfunc: star_lambdas.StarLambda = args[1].get_value()
    new_array = []
    for value in array: 
        retv = lambdfunc.call([value]).get_value()
        if retv == True:
            new_array.append(deepcopy(value))


    return star_types.Star_V_List.set_value(new_array)

# range
@star_functions.CreatePyFunction(
    FP,
    'range',
    True,
    [PFWA('start' ,types=[star_types.Star_T_Int]), PFWA('end', types=[star_types.Star_T_Int])]
)
def _(args: list[star_types.StarValue], error_handler: errors.ErrorHandler) -> star_types.StarValue:
    return star_types.Star_V_List.set_value([star_types.Star_V_Int.set_value(i) for i in range(int(args[0].get_value()), int(args[1].get_value()))])

# range setp
@star_functions.CreatePyFunction(
    FP,
    'range_step',
    True,
    [PFWA('start' ,types=[star_types.Star_T_Int]), PFWA('end', types=[star_types.Star_T_Int]), PFWA('step', types=[star_types.Star_T_Int])]
)
def _(args: list[star_types.StarValue], error_handler: errors.ErrorHandler) -> star_types.StarValue:
    return star_types.Star_V_List.set_value([star_types.Star_V_Int.set_value(i) for i in range(int(args[0].get_value()), int(args[1].get_value()), int(args[2].get_value()))])

# sizeof function
@star_functions.CreatePyFunction(
    FP,
    'sizeof',
    True,
    [PFWA('value', standart_value=star_types.Star_V_Null, types=star_types.Star_T)]
)
def _(args: list[star_types.StarValue], error_handler: errors.ErrorHandler) -> star_types.StarValue:
    return star_types.Star_V_Int.set_value(getsizeof(args[0].get_value()))



# input function
@star_functions.CreatePyFunction(
        FP, 
        'input', 
        True, 
        [PFWA('text',standart_value=star_types.Star_V_String.set_value(''), types=[
            star_types.Star_T_String, 
        ])]
)
def _(args: list[star_types.StarValue], error_handler: errors.ErrorHandler) -> star_types.StarValue:
    return star_types.Star_V_String.set_value(input(args[0].get_value()))



# type function
@star_functions.CreatePyFunction(
    FP, 
    'type', 
    True, 
    [PFWA('value', types=star_types.Star_T)]
)
def _(args: list[star_types.StarValue], error_handler: errors.ErrorHandler) -> star_types.StarValue:
    return star_types.Star_V_String.set_value(args[0].get_type().get_name())



# len function
@star_functions.CreatePyFunction(
    FP,
    'len',
    True,
    [PFWA('value', types=[star_types.Star_T_String, star_types.Star_T_List])]
)
def _(args: list[star_types.StarValue], error_handler: errors.ErrorHandler) -> star_types.StarValue:
    if args[0].get_type().get_name() == 'string':
        return star_types.Star_V_Int.set_value(len(args[0].get_value()))
    elif args[0].get_type().get_name() == 'list':
        return star_types.Star_V_Int.set_value(len(args[0].get_value()))
    else:
        return star_types.Star_V_Int.set_value(-1)



# to int
@star_functions.CreatePyFunction(
    FP, 
    'to_int', 
    True, 
    [PFWA('value', types=[star_types.Star_T_Float, star_types.Star_T_Int, star_types.Star_T_String])]
)
def _(args: list[star_types.StarValue], error_handler: errors.ErrorHandler) -> star_types.StarValue:
    try:
        if args[0].get_type().get_name() == 'float':
            return star_types.Star_V_Int.set_value(int(args[0].get_value()))
        elif args[0].get_type().get_name() == 'int':
            return star_types.Star_V_Int.set_value(args[0].get_value())
        elif args[0].get_type().get_name() == 'string':
            num = args[0].get_value().split('.')[0]
            return star_types.Star_V_Int.set_value(int(num))   
    except:
        raise errors.DummyStarError(f'Not convertable value: {Fore.MAGENTA}{args[0].get_value()}{Fore.RESET}')
    


# to float
@star_functions.CreatePyFunction(
    FP,
    'to_float',
    True,
    [PFWA('value', types=[star_types.Star_T_Float, star_types.Star_T_Int, star_types.Star_T_String])]
)
def _(args: list[star_types.StarValue], error_handler: errors.ErrorHandler) -> star_types.StarValue:
    if args[0].get_type().get_name() == 'float':
        return star_types.Star_V_Float.set_value(args[0].get_value())
    elif args[0].get_type().get_name() == 'int':
        return star_types.Star_V_Float.set_value(args[0].get_value())
    elif args[0].get_type().get_name() == 'string':
        if args[0].get_value().count('.') == 1:
            num = args[0].get_value()
            return star_types.Star_V_Float.set_value(float(num))
        else:
            num = args[0].get_value().split('.')[0] + '.0'
        return star_types.Star_V_Float.set_value(float(num))
    


# to string
@star_functions.CreatePyFunction(
    FP,
    'to_string',
    True,
    [PFWA('value', types=star_types.Star_T)]
)
def _(args: list[star_types.StarValue], error_handler: errors.ErrorHandler) -> star_types.StarValue:
    return star_types.Star_V_String.set_value(str(get_rec_values([args[0]])[0]))

# copy
@star_functions.CreatePyFunction(
    FP,
    'copy',
    True,
    [PFWA('value', types=star_types.Star_T)]
)
def _(args: list[star_types.StarValue], error_handler: errors.ErrorHandler) -> star_types.StarValue:
    st = star_types.StarValue(star_types.StarType(args[0].get_type().get_name(), None))
    def c(value): return value
    st.set_constructor(c)
    cv = st.set_value(copy(args[0].get_value()))

    return cv