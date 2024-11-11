from source.structures import star_spaces
from source.parser import star_memory


from colorama import Fore

class StarSpace:
    def __init__(self, name: str, memory: star_memory.ContextMemory, instructions: list) -> None:
        self.__name = name
        self.__memory = memory
        self.__instructions = instructions

    def get_name(self) -> str:
        return self.__name
    
    @property
    def memory(self) -> star_memory.ContextMemory:
        return self.__memory
    
    def __format__(self, arg) -> str:
        return f'{Fore.MAGENTA}StarSpace{Fore.RESET}<{self.__name}>'
    
    def __repr__(self) -> str:
        return f'SpaceObj<{self.__name}>'