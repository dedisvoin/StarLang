import json;

def load_symvols(path):
    with open(path, 'r') as f:
        return json.load(f)
    
class Symvlos:
    def __init__(self, symvols_dict: dict[str, str]) -> None:
        self.__symvols = symvols_dict
        self.__symvols['marks'] = ['"', "'"]

    @property
    def operators(self) -> str:
        return self.__symvols['operators']
    
    @property
    def numbers(self) -> str:
        return self.__symvols['numbers']
    
    @property
    def brackets(self) -> str:
        return self.__symvols['brackets']
    
    @property
    def letters(self) -> str:
        return self.__symvols['letters']

    @property
    def marks(self) -> str:
        return self.__symvols['marks']
    
    def check_in(self, char: str, group: list[str]) -> bool:
        return char in group


