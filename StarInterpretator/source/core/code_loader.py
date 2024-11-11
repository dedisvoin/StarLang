import os

def file_check(path: str) -> bool:
    return path.endswith('.star')

def file_founded(path: str) -> bool:
    path = path.replace('\\', '/')
    if '/' not in path:
        file_names = [name.split('.')[0] for name in os.listdir('./')]
        if path.split('.')[0] in file_names:
            return True
        else:
            return False
    else:
        file_names = [name.split('.')[0] for name in os.listdir('./'+path.split('/')[0]+'/')]
        
        if path.split('/')[-1].split('.')[0] in file_names:
            return True
        else:
            return False

def load_code(path: str) -> str:
    with open(path, 'r') as f:
        return f.read() + '\n     '
    
def split_code(code: str) -> list[str]:
    return code.split('\n')

def get_file_name(path: str) -> str:
    return path.split('/')[-1]

def get_file_exctension(path: str) -> str:
    return path.split('.')[-1]

def get_lines_count(code: str) -> int:
    return len(code.split('\n'))

def get_code_len(code: str) -> int:
    return len(code)

def get_file_name(path: str) -> str:
    name = path.split('\\')[-1].split('.')[0]
    return name

class StarFile:
    def __init__(self, path: str) -> 'StarFile':
        self.__path = path
        self.__code = load_code(path)
        self.__code_lines = split_code(self.__code)
        self.__file_name = get_file_name(path)
        self.__lines_count = get_lines_count(self.__code)
        self.__code_len = get_code_len(self.__code)

    @property
    def path(self) -> str:
        return self.__path
    
    @property
    def code(self) -> str:
        return self.__code
    
    @property
    def code_lines(self) -> list[str]:
        return self.__code_lines
    
    @property
    def file_name(self) -> str:
        return self.__file_name
    
    @property
    def lines_count(self) -> int:
        return self.__lines_count
    
    @property
    def code_len(self) -> int:
        return self.__code_len