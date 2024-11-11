from copy import copy, deepcopy
from pathlib import Path
import importlib.util
import sys

from colorama import Fore


from source.structures import star_types
from source.parser import star_memory



class PyStarFunction:
    def __init__(self, funct: callable, name: str, returned: bool, waited_args: list) -> None:
        self.__funct = funct
        self.__name = name
        self.__returned = returned
        self.__waited_args = waited_args

    @property
    def waited_args(self) -> list[str]:
        return self.__waited_args

    @property
    def returned(self) -> bool:
        return self.__returned

    @property
    def funct(self) -> callable:
        return self.__funct
    
    @property
    def name(self) -> str:
        return self.__name

    def call(self, args: list[str], error_handler) -> str:
        return self.__funct(args, error_handler)
    
    def __format__(self, arg) -> str:
        return f'{Fore.MAGENTA}PyFunc{Fore.RESET}<{self.__name}>'
    
    def __repr__(self) -> str:
        return f'PyFunc<{self.__name}>'


class PyFunctionPack:
    def __init__(self) -> None:
        self.__functs: list[PyStarFunction] = []

    @property
    def functs(self) -> list[PyStarFunction]:
        return self.__functs

    def add(self, function: PyStarFunction) -> None:
        self.__functs.append(function)


class PyFunctionWaitArg:
    def __init__(self, name, standart_value: star_types.StarValue = star_types.Star_V_Null.set_value(None), types: list[star_types.StarType] = []) -> None:
        self.__name = name
        self.__standart_value = standart_value
        self.__types = types
    
    @property
    def types(self) -> list[star_types.StarType]:
        return self.__types
    
    @property
    def standart_value(self) -> star_types.StarValue:
        return self.__standart_value
    
    @property
    def name(self) -> str:
        return self.__name


class PyStarConstant:
    def __init__(self, name: str, value: star_types.StarValue) -> None:
        self.__name = name
        self.__value = value

    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def value(self) -> star_types.StarValue:
        return self.__value


class PyConstantsPack:
    def __init__(self) -> None:
        self.__constants: list[PyStarConstant] = []
    
    @property
    def constants(self) -> list[PyStarConstant]:
        return self.__constants
    
    def add(self, constant: PyStarConstant) -> None:
        self.__constants.append(constant)


def CreatePyFunction(funct_pack: PyFunctionPack, 
                     function_name: str, 
                     retuned: bool,
                     waited_args: list[PyFunctionWaitArg] = []) -> callable:
    def inner(func):
        funct_pack.add(PyStarFunction(func, function_name, retuned, waited_args))
    
    return inner


def import_module_from_path(file_path):
    # Convert string path to Path object
    path = Path(file_path).resolve()
    
    # Get module name from file name
    module_name = path.stem
    
    # Create spec from file path
    spec = importlib.util.spec_from_file_location(module_name, path)
    
    # Create module from spec
    module = importlib.util.module_from_spec(spec)
    
    # Add module to sys.modules
    sys.modules[module_name] = module
    
    # Execute module
    spec.loader.exec_module(module)
    
    return module

def _dummy_construct(value):
    return value

class StarFunction:
    def __init__(self, arguments: list, used_spaces: list, use_inner_memory: bool,
                 return_type: list, function_instruction, global_memory, function_memory, error_handler, returned: bool = False, name_expr = None) -> None:
        self.__arguments = arguments
        self.__used_spaces = used_spaces
        self.__use_inner_memory = use_inner_memory
        self.__return_type = return_type
        self.__function_instruction = function_instruction
        self.__global_memory = global_memory
        self.__function_memory = function_memory
        self.__error_handler = error_handler
        self.__returned = returned
        if name_expr is not None:
            self.__name = name_expr.eval().get_value()
        else:
            self.__name = 'anonymous'

    def __format__(self, arg) -> str:
        return f'{Fore.MAGENTA}StarFunc{Fore.RESET}<{self.__name}>'
    
    def __repr__(self) -> str:
        return f'StarFunc<{self.__name}>'
    
    def call(self, args: list):
        self.__function_memory.clear()
        
        for i in range(len(args)):
            self.__function_memory.add_memory_object(star_memory.MemoryObject(self.__arguments[i][0].value, args[i], True, True, False))
        
        if not self.__use_inner_memory:
            
            self.__function_memory.merge(self.global_memory)
        if len(self.__used_spaces) > 0:
            for space_expr in self.__used_spaces:
                
                value_space = space_expr.eval()
                
                self.__function_memory.add_memory_object(star_memory.MemoryObject(space_expr.get_name(), value_space.copy(), True, True, False))
                
        self.__function_instruction.exec()
        

        value = star_types.Star_V_Null.set_value(None)
        
        
        return value
    
    @property
    def wait_args(self):
        return self.__arguments
    
    @property
    def return_args(self):
        return self.__return_type
    
    @property
    def expression(self):
        return self.__expression
    
    @property
    def memory(self):
        return self.__memory
    
    @property
    def global_memory(self):
        return self.__global_memory
    
    @property
    def name(self):
        return self.__name
    
    def get_name(self) -> str:
        return self.__name
    
