from copy import deepcopy
from source.parser import star_memory
from source.core import errors

from colorama import Fore

class StarLambda:
    def __init__(self, wait_args: list, return_args: list, expression: str, memory: star_memory.ContextMemory, 
                 error_handler: errors.ErrorHandler, global_memory: star_memory.ContextMemory, use_inner_memory: bool,
                 used_spaces: list) -> None:
        self.__wait_args = wait_args
        self.__return_args = return_args
        self.__expression = expression
        self.__memory = memory
        self.__error_handler = error_handler
        self.__global_memory = deepcopy(global_memory)
        self.__use_inner_memory = use_inner_memory
        self.__used_spaces = used_spaces

    @property
    def wait_args(self):
        return self.__wait_args
    
    @property
    def return_args(self):
        return self.__return_args
    
    @property
    def expression(self):
        return self.__expression
    
    @property
    def memory(self):
        return self.__memory
    
    @property
    def global_memory(self):
        return self.__global_memory

    def call(self, args: list):
        self.__memory.clear()
        
        for i in range(len(args)):
            self.__memory.add_memory_object(star_memory.MemoryObject(self.__wait_args[i][0].value, args[i], True, True, False))
        
        if not self.__use_inner_memory:
            self.__memory.merge(self.global_memory)
        if len(self.__used_spaces) > 0:
            for space_expr in self.__used_spaces:
                value_space = space_expr.eval()
                self.__memory.add_memory_object(star_memory.MemoryObject(space_expr.get_name(), value_space, False, True, True))
        
        value = self.__expression.eval()
        
        
        return value
    
    def __format__(self, arg) -> str:
        return f'{Fore.MAGENTA}StarLambda{Fore.RESET}<>'
    
    def __repr__(self) -> str:
        return f'StarLambda<>'