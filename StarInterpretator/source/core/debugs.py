from colorama import Fore, Back, Style
from source.core import tokens
from source.parser import star_memory
from source.structures import star_types
from source.structures import star_spaces

import os

ERROR_MESSAGE = f'[ {Fore.RED}ERROR{Fore.RESET} ]'
INFO_MESSAGE = f'[ {Fore.BLUE}INFO{Fore.RESET} ]'
WARNING_MESSAGE = f'[ {Fore.YELLOW}WARNING{Fore.RESET} ]'

YES_MESSAGE = f'[ {Fore.GREEN}YES{Fore.RESET} ]'


def FileNotFounded(path: str):
    print(ERROR_MESSAGE, f'File {Fore.YELLOW}"{path}"{Fore.RESET} not found ')
    os._exit(-1)

def FileFounded(path: str):
    print(INFO_MESSAGE, f'File {Fore.YELLOW}"{path}"{Fore.RESET} founded ')

def FileExctensionError(path: str, extension: str):
    print(WARNING_MESSAGE, f'File {Fore.YELLOW}"{path}"{Fore.RESET} extension {Fore.CYAN}.{extension}{Fore.RESET} error ')
    os._exit(-1)

def TokensSaved(path: str):
    print(INFO_MESSAGE, f'Tokens saved to {Fore.YELLOW}"{path}"{Fore.RESET} file ', YES_MESSAGE)

def StartSerialization():
    print(INFO_MESSAGE, f'Start serialization...')

def SerializationFinished():
    print(INFO_MESSAGE, f'Serialization finished. {YES_MESSAGE}')

def Tokens(t: list[tokens.Token]):
    print()
    print(' - Tokens -----------------------------------------------------------------------------------------------')
    for i, token in enumerate(t):
        print(f'{Fore.BLACK}{i:4}{Fore.RESET}| {Style.BRIGHT}{tokens.Token.COLORS[token.type]}{token.type:<12}{Fore.RESET}{Style.RESET_ALL} |{Fore.BLACK}"{token.value:<20}"{Fore.RESET}| {token.signature}')
    print(' - Tokens -----------------------------------------------------------------------------------------------')

def Memory(m: star_memory.ContextMemory):
    print()
    print(' - Memory -----------------------------------------------------------------------------------------------')
    for i, memory_object_id in enumerate(m.get_memory()):
        memory_object = m.get_memory()[memory_object_id]
        
        if type(memory_object.value) == star_types.StarValue:
            memory_object = memory_object.value.get_value()
        
        if type(memory_object) == star_types.StarType:
            print(f'{Fore.BLACK}{i:4}{Fore.RESET}| {Style.BRIGHT}{Fore.BLACK}{memory_object_id:<20}{Fore.RESET}{Style.RESET_ALL}| {memory_object:<69}')
        elif type(memory_object) == star_spaces.StarSpace:
            print(f'{Fore.BLACK}{i:4}{Fore.RESET}| {Style.BRIGHT}{Fore.BLACK}{memory_object_id:<20}{Fore.RESET}{Style.RESET_ALL}| {memory_object:<69}')
        else:
            try:
                print(f'{Fore.BLACK}{i:4}{Fore.RESET}| {Style.BRIGHT}{Fore.BLACK}{memory_object_id:<20}{Fore.RESET}{Style.RESET_ALL}| {memory_object:<69} | {m.get_memory()[memory_object_id].mutable}')
            except:
                print(f'{Fore.BLACK}{i:4}{Fore.RESET}| {Style.BRIGHT}{Fore.BLACK}{memory_object_id:<20}{Fore.RESET}{Style.RESET_ALL}| {str(memory_object):<69} | {m.get_memory()[memory_object_id].mutable}')
    print(' - Memory -----------------------------------------------------------------------------------------------')