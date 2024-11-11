from source.analizer import star_analizer
from source.parser import star_parser

from source.core import tokens_manipulator
from source.core import code_loader
from source.core import debugs
from source.core import tokens

from source.parser import star_memory

from colorama import Fore

from time import time

import cloudpickle

import sys


def save_compiled_code(executer_object: star_parser.Executer, file_name: str, d: bool = False):
    file = open(file_name, 'wb')
    if d: debugs.StartSerialization()
    cloudpickle.dump(executer_object, file)
    if d: debugs.SerializationFinished()
    


class Args:
    def __init__(self, args: list[str]) -> None:
        self.__args = args
        if len(self.__args) == 1:
            sys.exit(0)
            
        self.__debug = False if '-d' not in self.__args else True
        self.__print_stages = False if '-print-stages' not in self.__args else True
        self.__print_help = True if '-h' in self.__args or '-help' in self.__args else False
        self.__save_compiled = False if '-save-cstar' not in self.__args else True
        self.__instruction_calls = False if '-print-instructs' not in self.__args else True
        if self.__print_help: self.ph()

    def ph(self):
        print('usage:')
        print(f' {Fore.BLACK}>>> {Fore.MAGENTA}Star{Fore.RESET} [ {Fore.YELLOW}`file_path`{Fore.RESET} or ({Fore.CYAN}-h, -help{Fore.RESET}) ] [ {Fore.CYAN}-d{Fore.RESET} ] [ {Fore.CYAN}-print-stages{Fore.RESET} ]')
        print()
        print(f' [ {Fore.CYAN}-h           {Fore.RESET} ]  Use this flag to see the hint.')
        print(f' [ {Fore.CYAN}-d           {Fore.RESET} ]  Use this flag to see the debug info.')
        print(f' [ {Fore.CYAN}-print-stages{Fore.RESET} ]  Use this flag to see the stages of the program.')

        exit(0)

    @property
    def save_cstar(self) -> bool: return self.__save_compiled

    @property
    def deb(self) -> bool: return self.__debug

    @property
    def args(self) -> list[str]:
        return self.__args
    
    @property
    def print_stages(self) -> bool: return self.__print_stages

    @property
    def print_instructs(self) -> bool: return self.__instruction_calls


class StarIntepretator:
    def __init__(self, args: list[str]) -> None:
        self.__compiler_args = Args(args)
        self.__file_path: str | None = None
        self.__file: code_loader.StarFile | None = None
        self.__analized_tokens: list[tokens.Token] = []

        self.__analizer = star_analizer.Analizer()
        self.__parser = star_parser.Parser(self.__file_path)
        self.__executer = star_parser.Executer()

    def preload_memory(self, memory: star_memory.ContextMemory) -> star_memory.ContextMemory:
        
        self.__parser.add_to_global_memory(memory)

    def get_memory(self):
        return self.__parser.get_global_memory() 

    def run(self) -> None:
        
        # CODE FILE LOADING
        self.__file_path = self.__compiler_args.args[1]
        if code_loader.file_founded(self.__file_path):
            if code_loader.file_check(self.__file_path):
                self.__file = code_loader.StarFile(self.__file_path)
                #debugs.FileFounded(self.__file_path)
            else:   debugs.FileExctensionError(self.__file_path, code_loader.get_file_exctension(self.__file_path))
        else:   debugs.FileNotFounded(self.__file_path)
        
        #########################################################################################################
        #                                                                                                       #
        #                                              ANALIZE CODE                                             #
        #                                                                                                       #
        #########################################################################################################

        # PRINT ANALIZE STAGE
        if self.__compiler_args.print_stages: 
            print(f'[ {Fore.MAGENTA}"{self.__file_path}"{Fore.RESET} ] {Fore.GREEN}Analize...{Fore.RESET}', end='')
        ANALIZE_START_TIME = time()
        
        self.__analizer.set_file(self.__file)
        self.__analizer.analize()
        if self.__compiler_args.deb:
            self.__analizer.out_tokens()
        self.__analized_tokens = tokens_manipulator.load_tokens(self.__analizer.get_tokens())
        self.__analized_tokens = tokens_manipulator.clear_comments(self.__analized_tokens)

        # PRINT ANALIZE STAGE
        if self.__compiler_args.print_stages: 
            print(f'{Fore.BLACK} {round(time() - ANALIZE_START_TIME,2)}s {Fore.RESET}')
        


        #########################################################################################################
        #                                                                                                       #
        #                                              PARSE TOKENS                                             #
        #                                                                                                       #
        #########################################################################################################

        # PRINT PARSE STAGE
        if self.__compiler_args.print_stages:
            print(f'[ {Fore.MAGENTA}"{self.__file_path}"{Fore.RESET} ] {Fore.GREEN}Parse...{Fore.RESET}', end='')
        PARSE_START_TIME = time()

        self.__parser.set_file_path(self.__file_path)
        self.__parser.set_tokens(self.__analized_tokens)
        self.__parser.parse()

        # PRINT PARSE STAGE
        if self.__compiler_args.print_stages:
            print(f'{Fore.BLACK} {round(time() - PARSE_START_TIME,2)}s {Fore.RESET}')
        
        
        #########################################################################################################
        #                                                                                                       #
        #                                        EXECUTE INSTRUCTIONS                                           #
        #                                                                                                       #
        #########################################################################################################
        
        # PRINT EXECUTE STAGE
        if self.__compiler_args.print_stages: 
            print(f'[ {Fore.MAGENTA}"{self.__file_path}"{Fore.RESET} ] {Fore.GREEN}Execute...{Fore.RESET}')
        

        self.__executer.set_instructions(self.__parser.get_instructions())
        if self.__compiler_args.save_cstar:
            save_compiled_code(self.__executer, code_loader.get_file_name(self.__file_path)+'.cstar', True)
        else:
            self.__executer.run(self.__compiler_args.print_instructs)

        



        

        










