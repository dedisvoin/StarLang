from copy import deepcopy
from source.structures import star_types


class MemoryObject:
    def __init__(self, identifier: str, value: None = None, mutable: bool = True, inited: bool = True, static: bool = False, memory: None = None) -> None:
        self.__identifier = identifier
        self.__value = value
        self.__mutable = mutable
        self.__inited = inited
        self.__static = static
        

    def set_memory(self, memory: 'ContextMemory') -> None:
        self.__value.set_memory(memory)

    @property
    def static(self) -> bool:
        return self.__static

    @property
    def inited(self) -> bool:
        return self.__inited

    @property
    def mutable(self) -> bool:
        return self.__mutable

    @property
    def identifier(self) -> str:
        return self.__identifier
    
    @property
    def value(self):
        return self.__value



class ContextMemory:
    def __init__(self) -> None:
        self.__memory: dict[str, any] = {}

    @property
    def static_memory(self) -> dict[str, any]:
        return self.__memory

    def get_memory(self) -> dict[str, any]:
        return self.__memory
    
    def clear(self) -> None:
        self.__memory.clear()
    
    def merge(self, memory: 'ContextMemory') -> None:
        for key in memory.static_memory:
            self.__memory[key] = memory.static_memory[key]
        
    def add_memory_object(self, memory_object: MemoryObject) -> None:
        memory_object.set_memory(self)
        self.__memory[memory_object.identifier] = memory_object

    def memory_object_exists(self, identifier: str) -> bool:
        return identifier in self.__memory
    
    def memory_object_is_static(self, identifier: str) -> bool:
        return self.__memory[identifier].static
    
    def memory_object_is_mutable(self, identifier: str) -> bool:
        return self.__memory[identifier].mutable

    def get_memory_object(self, identifier: str) -> MemoryObject | None:
        return self.__memory[identifier]
        
            
        
