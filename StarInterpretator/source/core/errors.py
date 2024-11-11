from source.core import tokens
from source.structures import star_types
from colorama import Fore, Style

import os, sys

class BASIC_ERROR_TYPES:
    PARSE_ERROR = f'[ {Fore.RED}parse exception{Fore.RESET} ]'
    EXECUTE_ERROR = f'[ {Fore.CYAN}Execute exception{Fore.RESET} ]'
    SYNTAX_ERROR = f'[ {Fore.RED}syntax exception{Fore.RESET} ]'

ERRORS_COLOR = Fore.LIGHTBLACK_EX

class DummyStarError(BaseException):
    def __init__(self, message: str) -> None:
        self.__message = message
    
    @property
    def message(self) -> str:
        return self.__message



class ErrorHandler:
    def __init__(self, path: str) -> None:
        self.__path = path

    def set_file_path(self, path: str) -> None:
        self.__path = path

    def get_pos(self, token: tokens.Token) -> str:
        return f'[ {Fore.MAGENTA}line {token.line + 1}: pos {token.pos + 1}{Fore.RESET} ] ->'
    
    def get_code_line(self, line: int):
        file = open(self.__path, 'r').readlines()
        return file[line].replace('\n', '')
    
    def ERROR_WAIT_TOKEN_TYPE(self, before_token: tokens.Token, wait_token_value: str):
        code_stroke = self.get_code_line(before_token.line)
        print()
        print(f"{BASIC_ERROR_TYPES.SYNTAX_ERROR}{self.get_pos(before_token)} In file {Fore.YELLOW}'{self.__path}'{Fore.RESET}")
        print('|')
        print('|',code_stroke)
        error_pos_x = before_token.pos + before_token.lenght
        print('|', ' ' * (error_pos_x - 1), f'{ERRORS_COLOR}^{Fore.RESET}')
        print('|', f'{' ' * error_pos_x}{ERRORS_COLOR}|{Fore.RESET}')
        print('|', f'{' ' * error_pos_x}{ERRORS_COLOR}`---{Fore.RESET} expected {Fore.YELLOW}"{wait_token_value}"{Fore.RESET}')
        print()
        sys.exit(-1)

    def ERROR_TYPE_TO_UNARY_OPERATOR(self, start_token: tokens.Token, end_token: tokens.Token, value: star_types.StarValue, operator: str):
        code_stroke = self.get_code_line(start_token.line)
        print()
        print(f"{BASIC_ERROR_TYPES.EXECUTE_ERROR}{self.get_pos(start_token)} In file {Fore.YELLOW}'{self.__path}'{Fore.RESET}")
        print('|')
        print('|',code_stroke)
        error_pos_x = start_token.pos + start_token.lenght - 1
        lenght = end_token.pos - start_token.pos 
        print('|', ' ' * (error_pos_x - 1), f'{ERRORS_COLOR}{"^"*lenght}{Fore.RESET}')
        print('|', f'{' ' * (error_pos_x + lenght // 2)}{ERRORS_COLOR}|{Fore.RESET}')
        print('|', f'{' ' * (error_pos_x + lenght // 2)}{ERRORS_COLOR}`---{Fore.RESET} value to type {Fore.YELLOW}"{value.get_type().get_name()}"{Fore.RESET} not to be used with operator {Fore.YELLOW}"{operator}"{Fore.RESET}')
        print()
        sys.exit(-1)

    def ERROR_TYPES_TO_BINARY_OPERATOR(self, start_token: tokens.Token, end_token: tokens.Token, value1: star_types.StarValue, value2: star_types.StarValue, operator: str):
        code_stroke = self.get_code_line(start_token.line)
        print()
        print(f"{BASIC_ERROR_TYPES.EXECUTE_ERROR}{self.get_pos(start_token)} In file {Fore.YELLOW}'{self.__path}'{Fore.RESET}")
        print('|')
        print('|',code_stroke)
        error_pos_x = start_token.pos
        lenght = end_token.pos - start_token.pos
        print('|', ' ' * (error_pos_x - 1), f'{ERRORS_COLOR}{"^"*lenght}{Fore.RESET}')
        print('|', f'{' ' * (error_pos_x + lenght // 2 )}{ERRORS_COLOR}|{Fore.RESET}')
        print('|', f'{' ' * (error_pos_x + lenght // 2 )}{ERRORS_COLOR}`---{Fore.RESET} value to types [{Fore.YELLOW}"{value1.get_type().get_name()}"{Fore.RESET} and {Fore.YELLOW}"{value2.get_type().get_name()}"{Fore.RESET}] not to be used with operator {Fore.YELLOW}"{operator}"{Fore.RESET}')
        print()
        sys.exit(-1)

    def ERROR_TYPE_NOT_DEFINITED(self, token: tokens.Token, value: star_types.StarValue):
        code_stroke = self.get_code_line(token.line)
        print()
        print(f"{BASIC_ERROR_TYPES.EXECUTE_ERROR}{self.get_pos(token)} In file {Fore.YELLOW}'{self.__path}'{Fore.RESET}")
        print('|')
        print('|',code_stroke)
        error_pos_x = token.pos
        lenght = token.lenght
        print('|', ' ' * (error_pos_x - 1), f'{ERRORS_COLOR}{"^"*lenght}{Fore.RESET}')
        print('|', f'{' ' * (error_pos_x + lenght // 2)}{ERRORS_COLOR}|{Fore.RESET}')
        print('|', f'{' ' * (error_pos_x + lenght // 2)}{ERRORS_COLOR}`---{Fore.RESET} type {Fore.YELLOW}"{value}"{Fore.RESET} not defined')
        sys.exit(-1)

    def ERROR_INVALID_TYPE_OF_ASSIGNED_EXPR(self, start_token_types: tokens.Token, end_token_types: tokens.Token, start_token_expr: tokens.Token, end_token_expr: tokens.Token, value: star_types.StarValue, wait_types: list[str]):
        code_stroke = self.get_code_line(start_token_types.line)
        print()
        print(f"{BASIC_ERROR_TYPES.EXECUTE_ERROR}{self.get_pos(start_token_expr)} In file {Fore.YELLOW}'{self.__path}'{Fore.RESET}")
        print('|')
        print('|',code_stroke)
        types_error_pos_x = start_token_types.pos + start_token_types.lenght - 1
        types_lenght = end_token_types.pos - start_token_types.pos - 1

        print('|', ' ' * ( types_error_pos_x - 1), f'{Fore.YELLOW}{"^"*types_lenght}{Fore.RESET}')
        print('|', f' Value to type `{value.get_type()}` not to be used with types {Fore.YELLOW}{[t.get_value().get_name() for t in wait_types]}{Fore.RESET}')
        print()
        sys.exit(-1)

    def ERROR_VARIABLE_IS_NOT_DEFINE(self, token: tokens.Token):
        code_stroke = self.get_code_line(token.line)
        print()
        print(f"{BASIC_ERROR_TYPES.EXECUTE_ERROR}{self.get_pos(token)} In file {Fore.YELLOW}'{self.__path}'{Fore.RESET}")
        print('|')
        print('| ',code_stroke)
        error_pos_x = token.pos
        lenght = token.lenght
        print('|', ' ' * (error_pos_x), f'{ERRORS_COLOR}{"^"*lenght}{Fore.RESET}')
        print('|', f'{' ' * (error_pos_x + lenght // 2 + 1)}{ERRORS_COLOR}|{Fore.RESET}')
        print('|', f'{' ' * (error_pos_x + lenght // 2 + 1)}{ERRORS_COLOR}`---{Fore.RESET} {Fore.YELLOW}"{token.value}"{Fore.RESET} is not defined')
        print()
        os._exit(-1)

    def ERROR_VARIABLE_IS_NOT_ITTERABLE(self, start_token: tokens.Token, end_tokenn: tokens.Token, value: star_types.StarValue):
        code_stroke = self.get_code_line(start_token.line)
        print()
        print(f"{BASIC_ERROR_TYPES.EXECUTE_ERROR}{self.get_pos(start_token)} In file {Fore.YELLOW}'{self.__path}'{Fore.RESET}")
        print('|')
        print('|',code_stroke)
        error_pos_x = start_token.pos
        lenght = end_tokenn.pos - start_token.pos
        print('|', ' ' * (error_pos_x - 1), f'{ERRORS_COLOR}{"^"*lenght}{Fore.RESET}')
        print('|', f'{' ' * (error_pos_x + lenght // 2)}{ERRORS_COLOR}|{Fore.RESET}')
        print('|', f'{' ' * (error_pos_x + lenght // 2)}{ERRORS_COLOR}`---{Fore.RESET} {Fore.YELLOW}"{value.get_type().get_name()}"{Fore.RESET} is not itterable')
        print()
        sys.exit(-1)
    
    def ERROR_LIST_INDEX_OUT_OF_RANGE(self, start_token: tokens.Token, end_token: tokens.Token, expr_value):
        code_stroke = self.get_code_line(start_token.line)
        print()
        print(f"{BASIC_ERROR_TYPES.EXECUTE_ERROR}{self.get_pos(start_token)} In file {Fore.YELLOW}'{self.__path}'{Fore.RESET}")
        print('|')
        print('|',code_stroke)
        error_pos_x = start_token.pos
        lenght = end_token.pos - start_token.pos
        print('|', ' ' * (error_pos_x - 1), f'{ERRORS_COLOR}{"^"*lenght}{Fore.RESET}')
        print('|', f'{' ' * (error_pos_x + lenght // 2)}{ERRORS_COLOR}|{Fore.RESET}')
        print('|', f'{' ' * (error_pos_x + lenght // 2)}{ERRORS_COLOR}`---{Fore.RESET} is out of range')
        print()
        sys.exit(-1)


    def ERROR_INVALUD_INSTRUCTION(self, token: tokens.Token):
        code_stroke = self.get_code_line(token.line)
        print()
        print(f"{BASIC_ERROR_TYPES.PARSE_ERROR}{self.get_pos(token)} In file {Fore.YELLOW}'{self.__path}'{Fore.RESET}")
        print('|')
        print('| ',code_stroke)
        error_pos_x = 0
        lenght = len(code_stroke)
        print('|', ' ' * (error_pos_x), f'{ERRORS_COLOR}{"^"*lenght}{Fore.RESET}')

        print('|', f' {ERRORS_COLOR}invalid instruction{Fore.RESET}')
        print()
        sys.exit(-1)

    def ERROR_VARIABLE_IS_NOT_CALLABLE(self, start_token: tokens.Token, end_token: tokens.Token, type: tokens.T_Types):
        code_stroke = self.get_code_line(start_token.line)
        print()
        print(f"{BASIC_ERROR_TYPES.EXECUTE_ERROR}{self.get_pos(start_token)} In file {Fore.YELLOW}'{self.__path}'{Fore.RESET}")
        print('|')
        print('|',code_stroke)
        error_pos_x = start_token.pos
        lenght = end_token.pos - start_token.pos
        print('|', ' ' * (error_pos_x - 1), f'{ERRORS_COLOR}{"^"*lenght}{Fore.RESET}')
        print('|', f'{' ' * (error_pos_x + lenght // 2)}{ERRORS_COLOR}|{Fore.RESET}')
        print('|', f'{' ' * (error_pos_x + lenght // 2)}{ERRORS_COLOR}`---{Fore.RESET} {Fore.YELLOW}"{type.get_name()}"{Fore.RESET} is not callable')
        print()
        sys.exit(-1)

    def ERROR_FUNCTION_ARGUMENTS_COUNT_NOT_MATCH(self, start_token: tokens.Token, end_token: tokens.Token, wargs_len: int, cargs_len: int, funct_name: str):
        code_stroke = self.get_code_line(start_token.line)
        print()
        print(f"{BASIC_ERROR_TYPES.EXECUTE_ERROR}{self.get_pos(start_token)} In file {Fore.YELLOW}'{self.__path}'{Fore.RESET}")
        print('|')
        print('|',code_stroke)
        error_pos_x = start_token.pos
        lenght = end_token.pos - start_token.pos
        print('|', ' ' * (error_pos_x - 1), f'{ERRORS_COLOR}{"^"*lenght}{Fore.RESET}')
        print('|', f'{' ' * (error_pos_x + lenght // 2)}{ERRORS_COLOR}|{Fore.RESET}')
        print('|', f'{' ' * (error_pos_x + lenght // 2)}{ERRORS_COLOR}|---[>]{ Fore.RESET} {Fore.YELLOW}"{funct_name}"{Fore.RESET} function arguments count not match')
        print('|', f'{' ' * (error_pos_x + lenght // 2)}{ERRORS_COLOR}`---[?] {Fore.MAGENTA}{wargs_len}{Fore.RESET} expected, {Fore.MAGENTA}{cargs_len}{Fore.RESET} given')
        print()
        os._exit(-1)
    
    def ERROR_FUNCTION_ARGUMENTS_TYPE_NOT_MATCH(self, start_token: tokens.Token, end_token: tokens.Token, wtype: str, ctype: str, funct_name: str, arg_name: str):
        code_stroke = self.get_code_line(start_token.line)
        print()
        print(f"{BASIC_ERROR_TYPES.EXECUTE_ERROR}{self.get_pos(start_token)} In file {Fore.YELLOW}'{self.__path}'{Fore.RESET}")
        print('|')
        print('|',code_stroke)
        error_pos_x = start_token.pos
        lenght = end_token.pos - start_token.pos
        print('|', ' ' * (error_pos_x - 1), f'{ERRORS_COLOR}{"^"*lenght}{Fore.RESET}')
        print('|', f'{' ' * (error_pos_x + lenght // 2)}{ERRORS_COLOR}|{Fore.RESET}')
        print('|', f'{' ' * (error_pos_x + lenght // 2)}{ERRORS_COLOR}|---[>] {Fore.RESET}{Fore.YELLOW}"{funct_name}"{Fore.RESET} function arguments {Fore.YELLOW}"{arg_name}"{Fore.RESET} type not match')
        print('|', f'{' ' * (error_pos_x + lenght // 2)}{ERRORS_COLOR}`---[?] {Fore.MAGENTA}{wtype}{Fore.RESET} expected, {Fore.MAGENTA}{ctype}{Fore.RESET} given')
        print()
        os._exit(-1)

    def ERROR_PYTHON_MODULE_NOT_FOUND(self, start_token: tokens.Token, end_token: tokens.Token, module_name: str):
        code_stroke = self.get_code_line(start_token.line)
        print()
        print(f"{BASIC_ERROR_TYPES.EXECUTE_ERROR}{self.get_pos(start_token)} In file {Fore.YELLOW}'{self.__path}'{Fore.RESET}")
        print('|')
        print('|',code_stroke)
        error_pos_x = start_token.pos
        lenght = end_token.pos - start_token.pos
        print('|', ' ' * (error_pos_x - 1), f'{ERRORS_COLOR}{"^"*lenght}{Fore.RESET}')
        print('|', f'{' ' * (error_pos_x + lenght // 2)}{ERRORS_COLOR}|{Fore.RESET}')
        print('|', f'{' ' * (error_pos_x + lenght // 2)}{ERRORS_COLOR}`---{Fore.RESET} {Fore.YELLOW}"{module_name}"{Fore.RESET} module not found')
        print()
        sys.exit(-1)

    def ERROR_PYTHON_NODULE_FUNCTION_PACK_NOT_FOUND(self, start_token: tokens.Token, end_token: tokens.Token, module_name: str):
        code_stroke = self.get_code_line(start_token.line)
        print()
        print(f"{BASIC_ERROR_TYPES.EXECUTE_ERROR}{self.get_pos(start_token)} In file {Fore.YELLOW}'{self.__path}'{Fore.RESET}")
        print('|')
        print('|',code_stroke)
        error_pos_x = start_token.pos
        lenght = end_token.pos - start_token.pos
        print('|', ' ' * (error_pos_x - 1), f'{ERRORS_COLOR}{"^"*lenght}{Fore.RESET}')
        print('|', f'{' ' * (error_pos_x + lenght // 2)}{ERRORS_COLOR}|{Fore.RESET}')
        print('|', f'{' ' * (error_pos_x + lenght // 2)}{ERRORS_COLOR}`---{Fore.RESET} in {Fore.YELLOW}"{module_name}"{Fore.RESET} module not found function pack ({Fore.BLUE}FP{Fore.RESET})')
        print()
        sys.exit(-1)

    def ERROR_PYTHON_NODULE_CONSTANTS_PACK_NOT_FOUND(self, start_token: tokens.Token, end_token: tokens.Token, module_name: str):
        code_stroke = self.get_code_line(start_token.line)
        print()
        print(f"{BASIC_ERROR_TYPES.EXECUTE_ERROR}{self.get_pos(start_token)} In file {Fore.YELLOW}'{self.__path}'{Fore.RESET}")
        print('|')
        print('|',code_stroke)
        error_pos_x = start_token.pos
        lenght = end_token.pos - start_token.pos
        print('|', ' ' * (error_pos_x - 1), f'{ERRORS_COLOR}{"^"*lenght}{Fore.RESET}')
        print('|', f'{' ' * (error_pos_x + lenght // 2)}{ERRORS_COLOR}|{Fore.RESET}')
        print('|', f'{' ' * (error_pos_x + lenght // 2)}{ERRORS_COLOR}`---{Fore.RESET} in {Fore.YELLOW}"{module_name}"{Fore.RESET} module not found constants pack ({Fore.BLUE}CP{Fore.RESET})')
        print()
        sys.exit(-1)

    def ERROR_VARIABLE_IS_NOT_NAME_SPACE(self, start_token: tokens.Token, end_token: tokens.Token):
        code_stroke = self.get_code_line(start_token.line)
        print()
        print(f"{BASIC_ERROR_TYPES.EXECUTE_ERROR}{self.get_pos(start_token)} In file {Fore.YELLOW}'{self.__path}'{Fore.RESET}")
        print('|')
        print('|',code_stroke)
        error_pos_x = start_token.pos
        lenght = end_token.pos - start_token.pos
        print('|', ' ' * (error_pos_x - 1), f'{ERRORS_COLOR}{"^"*lenght}{Fore.RESET}')
        print('|', f'{' ' * (error_pos_x + lenght // 2)}{ERRORS_COLOR}|{Fore.RESET}')
        print('|', f'{' ' * (error_pos_x + lenght // 2)}{ERRORS_COLOR}`---{Fore.RESET} is not name space object')
        print()
        sys.exit(-1)

    def STD_ERROR_CONVERT_TO(self, value, to_type):
        print(f"{BASIC_ERROR_TYPES.EXECUTE_ERROR} Can't convert {Fore.YELLOW}'{value}'{Fore.RESET} to {to_type}")
        os._exit(-1)

    def CALL_ERROR(self, start_token: tokens.Token, end_token: tokens.Token, funct_name: str, trace_back: str):
        code_stroke = self.get_code_line(start_token.line)
        print()
        print(f"{BASIC_ERROR_TYPES.EXECUTE_ERROR}{self.get_pos(start_token)} In file {Fore.YELLOW}'{self.__path}'{Fore.RESET}")
        print('|')
        print('|',code_stroke)
        error_pos_x = start_token.pos
        lenght = end_token.pos - start_token.pos
        print('|', ' ' * (error_pos_x - 1), f'{ERRORS_COLOR}{"^"*lenght}{Fore.RESET}')
        print('|', f'{' ' * (error_pos_x + lenght // 2)}{ERRORS_COLOR}|{Fore.RESET}')
        print('|', f'{' ' * (error_pos_x + lenght // 2)}{ERRORS_COLOR}|---{Fore.RESET} In { Fore.YELLOW}"{funct_name}"{Fore.RESET} function')
        print('|', f'{' ' * (error_pos_x + lenght // 2)}{ERRORS_COLOR}`---{Fore.RESET} {trace_back}')
        print()
        os._exit(-1)

    def ERROR_STATIC_VAR_REDEFINITION(self, start_token: tokens.Token, end_token: tokens.Token, var_name: str):
        code_stroke = self.get_code_line(start_token.line)
        print()
        print(f"{BASIC_ERROR_TYPES.EXECUTE_ERROR}{self.get_pos(start_token)} In file {Fore.YELLOW}'{self.__path}'{Fore.RESET}")
        print('|')
        print('|',code_stroke)
        error_pos_x = start_token.pos
        
        lenght = end_token.pos - start_token.pos

        print('|', ' ' * (error_pos_x - 1), f'{ERRORS_COLOR}{"^"*lenght}{Fore.RESET}')
        print('|', f'{' ' * (error_pos_x + lenght // 2)}{ERRORS_COLOR}|{Fore.RESET}')
        print('|', f'{' ' * (error_pos_x + lenght // 2)}{ERRORS_COLOR}|--->[>]{Fore.RESET} In { Fore.YELLOW}"{var_name}"{Fore.RESET} variable')
        print('|', f'{' ' * (error_pos_x + lenght // 2)}{ERRORS_COLOR}`--->[?]{Fore.RESET} {Fore.LIGHTWHITE_EX}Static{Fore.RESET} variable redefinition!')
        print()
        sys.exit(-1)

    def ERROR_CONST_VAR_REDEFINITION(self, start_token: tokens.Token, end_token: tokens.Token, var_name: str):
        code_stroke = self.get_code_line(start_token.line)
        print()
        print(f"{BASIC_ERROR_TYPES.EXECUTE_ERROR}{self.get_pos(start_token)} In file {Fore.YELLOW}'{self.__path}'{Fore.RESET}")
        print('|')
        print('| ',code_stroke)
        error_pos_x = start_token.pos

        lenght = end_token.pos - start_token.pos
        print('|', ' ' * (error_pos_x), f'{ERRORS_COLOR}{"^"*lenght}{Fore.RESET}')
        print('|', f'{' ' * (error_pos_x + lenght // 2 + 1)}{ERRORS_COLOR}|{Fore.RESET}')
        print('|', f'{' ' * (error_pos_x + lenght // 2 + 1)}{ERRORS_COLOR}|--->[>]{Fore.RESET} In { Fore.YELLOW}"{var_name}"{Fore.RESET} variable')
        print('|', f'{' ' * (error_pos_x + lenght // 2 + 1)}{ERRORS_COLOR}`--->[?]{Fore.RESET} {Fore.LIGHTWHITE_EX}Const{Fore.RESET} variable redefinition!')
        print()
        sys.exit(-1)


    def ERROR_STATIC_TYPEDEF_REDEFINITION(self, start_token: tokens.Token, end_token: tokens.Token, var_name: str):
        code_stroke = self.get_code_line(start_token.line)
        print()
        print(f"{BASIC_ERROR_TYPES.EXECUTE_ERROR}{self.get_pos(start_token)} In file {Fore.YELLOW}'{self.__path}'{Fore.RESET}")
        print('|')
        print('| ', code_stroke)
        error_pos_x = start_token.pos

        lenght = end_token.pos - start_token.pos

        print('|', ' ' * (error_pos_x - 1), f'{ERRORS_COLOR}{"^"*lenght}{Fore.RESET}')
        print('|', f'{' ' * (error_pos_x + lenght // 2)}{ERRORS_COLOR}|{Fore.RESET}')
        print('|', f'{' ' * (error_pos_x + lenght // 2)}{ERRORS_COLOR}|---[>]{Fore.RESET} In { Fore.YELLOW}"{var_name}"{Fore.RESET} variable')
        print('|', f'{' ' * (error_pos_x + lenght // 2)}{ERRORS_COLOR}`---[?]{Fore.RESET} {Fore.LIGHTWHITE_EX}Static{Fore.RESET} type redefinition!')
        print()
        sys.exit(-1)

    def ERROR_STATIC_VAR_VALUE_REDEFINITION(self, start_token: tokens.Token, end_token: tokens.Token, var_name: str, expr_type, wait_type):
        code_stroke = self.get_code_line(start_token.line)
        print()
        print(f"{BASIC_ERROR_TYPES.EXECUTE_ERROR}{self.get_pos(start_token)} In file {Fore.YELLOW}'{self.__path}'{Fore.RESET}")
        print('|')
        print('| ', code_stroke)
        error_pos_x = start_token.pos

        lenght = end_token.pos - start_token.pos
        print('|', ' ' * (error_pos_x - 1), f'{ERRORS_COLOR}{"^"*lenght}{Fore.RESET}')
        print('|', f'{' ' * (error_pos_x + lenght // 2)}{ERRORS_COLOR}|{Fore.RESET}')
        print('|', f'{' ' * (error_pos_x + lenght // 2)}{ERRORS_COLOR}|--->[>]{Fore.RESET} In { Fore.YELLOW}"{var_name}"{Fore.RESET} variable.')
        print('|', f'{' ' * (error_pos_x + lenght // 2)}{ERRORS_COLOR}`--->[?]{Fore.RESET} {Fore.LIGHTWHITE_EX}[ Static ]{Fore.RESET} variable redefinition!')
        print('|', f'{' ' * (error_pos_x + lenght // 2)}{ERRORS_COLOR}`--->[!]{Fore.RESET} Type `{expr_type}` is not equal to type `{wait_type}`.')
        print()
        sys.exit(-1)

