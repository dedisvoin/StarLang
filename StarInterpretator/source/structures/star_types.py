from copy import copy, deepcopy
from colorama import Fore

from source.structures import star_spaces


class StarType:
    def __init__(self, name: str, space: star_spaces.StarSpace) -> None:
        self.__name = name
        self.__useful_operations = []
        self.__space = space


    def get_space(self) -> star_spaces:
        return self.__space

    def get_name(self) -> str:
        return self.__name

    def set_useful_operations(self, operations: list[str]):
        self.__useful_operations = operations

    def get_useful_operations(self) -> list[str]:
        return self.__useful_operations
    
    def __format__(self, args) -> str:
        return f'{f"{Fore.BLUE}StarType{Fore.RESET}<{Fore.BLACK}{self.__name}{Fore.RESET}>"}'
    
    def __str__(self) -> str:
        return f"{Fore.BLUE}StarType{Fore.RESET}<{Fore.BLACK}{self.__name}{Fore.RESET}>"


Star_T_Int =                StarType('int', None)
Star_T_Float =              StarType('float', None)
Star_T_String =             StarType('string', None)
Star_T_Bool =               StarType('bool', None)
Star_T_Type =               StarType('type', None)
Star_T_Space =              StarType('namespace', None)
Star_T_List =               StarType('list', None)
Star_T_Null =               StarType('null', None)
Star_T_PyFunc =             StarType('pyfunc', None)
Star_T_LambdaFunc =         StarType('lambdafunc', None)
Star_T_StarFunc =           StarType('starfunc', None)



Star_T_Basics = [Star_T_Int, Star_T_Float, Star_T_String, Star_T_Bool, Star_T_List, Star_T_Type, Star_T_LambdaFunc, Star_T_StarFunc, Star_T_Null]
def is_basic_type(type: StarType) -> bool:
    if type.get_name() in [T.get_name() for T in Star_T_Basics]:
        return True
    return False



class StarValue:
    def __init__(self, type: StarType):
        self.__type = type
        self.__value = None
        self.__constructor: callable = None
        self.__memory = None
        self.__wait_types = []

    def set_wait_types(self, types: list[str]):
        self.__wait_types = types

    def get_wait_types(self) -> list[str]:
        return self.__wait_types

    def copy(self):
        return self.set_value(deepcopy(self.__value))
    
    def base_copy(self):
        return self.set_value(copy(self.__value))
    
    def set_memory(self, memory):
        self.__memory = memory

    def get_memory(self):
        return self.__memory

    def set_constructor(self, constructor: any):
        self.__constructor = constructor

    def set_value(self, value: any):
        self.__value = self.__constructor(value)
        return copy(self)

    def get_value(self):
        return self.__value
    
    def get_type(self) -> StarType:
        return self.__type


Star_V_LambdaFunc = StarValue(Star_T_LambdaFunc)
def Star_V_LambdaFunc_Constructor(value: callable):
    return value
Star_V_LambdaFunc.set_constructor(Star_V_LambdaFunc_Constructor)

Star_V_StarFunc = StarValue(Star_T_StarFunc)
def Star_V_StarFunc_Constructor(value: callable):
    return value
Star_V_StarFunc.set_constructor(Star_V_StarFunc_Constructor)


Star_V_PyFunc = StarValue(Star_T_PyFunc)
def Star_V_PyFunc_Constructor(value: callable):
    return value
Star_V_PyFunc.set_constructor(Star_V_PyFunc_Constructor)


Star_V_Int = StarValue(Star_T_Int)
def Star_V_Int_Constructor(value: str | int):
    return int(value)
Star_V_Int.set_constructor(Star_V_Int_Constructor)



Star_V_Float = StarValue(Star_T_Float)
def Star_V_Float_Constructor(value: str | float):
    return float(value)
Star_V_Float.set_constructor(Star_V_Float_Constructor)



Star_V_String = StarValue(Star_T_String)
def Star_V_String_Constructor(value: str):
    return str(value)
Star_V_String.set_constructor(Star_V_String_Constructor)



Star_V_Bool = StarValue(Star_T_Bool)
def Star_V_Bool_Constructor(value: str | bool):
    if value == 'true':
        return True
    elif value == 'false':
        return False
    else:
        return bool(value)
Star_V_Bool.set_constructor(Star_V_Bool_Constructor)



Star_V_Type = StarValue(Star_T_Type)
def Star_V_Type_Constructor(value: str):
    from source.parser import star_memory
    args_space = Star_V_Space.set_value(star_spaces.StarSpace(value, star_memory.ContextMemory(), []))
    args_space.get_value().memory.add_memory_object(star_memory.MemoryObject('name', Star_V_String.set_value(value), False, True, True))
    
    return StarType(value, args_space)
Star_V_Type.set_constructor(Star_V_Type_Constructor)



Star_V_Space = StarValue(Star_T_Space)
def Star_V_Space_Constructor(value: str):
    return value
Star_V_Space.set_constructor(Star_V_Space_Constructor)



Star_V_List = StarValue(Star_T_List)
def Star_V_List_Constructor(value: list):
    return value
Star_V_List.set_constructor(Star_V_List_Constructor)



Star_V_Null = StarValue(Star_T_Null)
def Star_V_Null_Constructor(value: str):
    return None
Star_V_Null.set_constructor(Star_V_Null_Constructor)


Star_T = [Star_T_Int, Star_T_Float, Star_T_String, Star_T_Bool, Star_T_Type, Star_T_Space, Star_T_List, Star_T_Null, Star_T_PyFunc, Star_T_LambdaFunc]


def is_basic_value(value: StarValue) -> bool:
    if is_basic_type(value.get_type()):
        return True
    return False

def is_value_type(value: StarValue, type: StarType) -> bool:
    if value.get_type().get_name() == type.get_name():
        return True
    return False