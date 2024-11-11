from colorama import Fore
from source.core import operators


class T_Types:
    T_EOF = 'EOF'
    T_WORD = 'word'
    T_NUMBER = 'number'
    T_BRACKET = 'bracket'
    T_STRING = 'string'
    T_OPERATOR = 'operator'
    T_KEYWWORD = 'keyword'
    T_COMMENTS = 'comment'
    

class KeyWord:
    def __init__(self, name: str, value: str) -> None:
        self.__name = name
        self.__value = value

    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def value(self) -> str:
        return self.__value
    

KEYWORDS = [
    KeyWord('var', 'var'),
    KeyWord('const', 'const'),
    KeyWord('func', 'func'),
    KeyWord('if', 'if'),
    KeyWord('else', 'else'),
    KeyWord('while', 'while'),
    KeyWord('for', 'for'),
    KeyWord('return', '|>'),
    KeyWord('class', 'class'),
    KeyWord('this', 'this'),
    KeyWord('await', 'await'),
    KeyWord('async', 'async'),
    KeyWord('true', 'true'),
    KeyWord('false', 'false'),
    KeyWord('typedef', 'typedef'),
    KeyWord('space', 'space'),
    KeyWord('break', 'break'),
    KeyWord('continue', 'continue'),
    KeyWord('import', 'import'),
    KeyWord('lambda', 'lambda'),
    KeyWord('module', 'module'),
    KeyWord(',', ',')
]

def in_KeyWords(value: str) -> bool:
    for keyword in KEYWORDS:
        if keyword.value == value:
            return True
    return False

def get_identifier(value: str) -> str:
    for keyword in KEYWORDS:
        if keyword.value == value:
            return keyword
    return value




class Token:
    COLORS = {
        T_Types.T_WORD: Fore.CYAN,
        T_Types.T_NUMBER: Fore.GREEN,
        T_Types.T_BRACKET: Fore.BLUE,
        T_Types.T_STRING: Fore.MAGENTA,
        T_Types.T_OPERATOR: Fore.YELLOW,
        T_Types.T_KEYWWORD: Fore.RED,
        T_Types.T_COMMENTS: Fore.LIGHTMAGENTA_EX,
        T_Types.T_EOF: Fore.LIGHTBLACK_EX,
    }


    def __init__(self, type: T_Types, value: str, line: int, pos: int, signature: operators.Operator | None | str = None) -> None:
        self.__type = type
        self.__value = value
        self.__line = line
        self.__pos = pos
        self.__identifier = type
        self.__len = len(value)
        self.__signature = signature
        if self.__signature is not str:
            self.__is_operator = True
        else:
            self.__is_operator = False

    def add_len(self, lenght: int) -> None:
        self.__len += lenght
        return self

    def set_identifier(self, identifier: str) -> None:
        self.__identifier = identifier
        self.__type = T_Types.T_KEYWWORD

    @property
    def identifier(self) -> str:
        return self.__identifier
    
    @property
    def signature(self) -> operators.Operator | None:
        return self.__signature

    @property
    def pos(self) -> int:
        return self.__pos
    
    @property
    def value(self) -> str:
        return self.__value
    
    @property
    def line(self) -> int:
        return self.__line
    
    @property
    def type(self) -> T_Types:
        return self.__type
    
    @property
    def lenght(self) -> int:
        return self.__len
    
