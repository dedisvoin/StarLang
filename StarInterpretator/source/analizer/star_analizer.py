from source.core import symvols_loader
from source.core import code_loader
from source.core import tokens

from copy import copy, deepcopy

import time


class Analizer:
    def __init__(self) -> None:
        self.__file: code_loader.StarFile | None = None

        self.__symvols = symvols_loader.Symvlos(symvols_loader.load_symvols(r'source\core\using_symvols.json'))

        self.__pos = 0
        self.__pos_in_line = 0
        self.__saved_pos_in_line = 0
        self.__line = 0
        self.__basic_tokens: list[tokens.Token] = []
        self.__tokens: list[tokens.Token] = []

        self.__spent_time = 0


    def out_basic_tokens(self) -> None:
        sorted_tokens = {}
        for token in self.__basic_tokens:
            if token.line in sorted_tokens:
                sorted_tokens[token.line].append(token)
            else:
                sorted_tokens[token.line] = [token]

        for line in sorted_tokens:
            print(f'line {line + 1}: tokens count:{len(sorted_tokens[line])}')
            for token in sorted_tokens[line]:
                print(f' {tokens.Fore.BLACK}| ->{tokens.Fore.RESET}  {tokens.Token.COLORS[token.type]}{token.type}{tokens.Fore.RESET}: {tokens.Fore.BLACK}"{token.value}"{tokens.Fore.RESET}')
            print()


    def out_tokens(self) -> None:
        sorted_tokens = {}
        for token in self.__tokens:
            if token.line in sorted_tokens:
                sorted_tokens[token.line].append(token)
            else:
                sorted_tokens[token.line] = [token]

        for line in sorted_tokens:
            print(f'line {line + 1}: tokens count:{len(sorted_tokens[line])}')
            for i, token in enumerate(sorted_tokens[line]):
                print(f' {tokens.Fore.BLACK}| -> {i + 1}{tokens.Fore.RESET}  {tokens.Token.COLORS[token.type]}{token.type}{tokens.Fore.RESET}: {tokens.Fore.BLACK}"{token.value}"{tokens.Fore.RESET}')
            print()
        print(f'All tokens count: {tokens.Fore.BLACK}{len(self.__tokens)}{tokens.Fore.RESET}')
        print()

    def out_analize_information(self) -> None:
        print(f' - Analize time: {tokens.Fore.BLACK}{round(self.__spent_time, 3)}s{tokens.Fore.RESET}')
        print(f' - Founded {tokens.Fore.BLACK}{len(self.__tokens)}{tokens.Fore.RESET} tokens')

    def get_tokens(self) -> list[tokens.Token]:
        return self.__tokens
    
    def get_basic_tokens(self) -> list[tokens.Token]:
        return self.__basic_tokens


    def set_file(self, file: code_loader.StarFile) -> None:
        self.__file = file


    def next_char(self) -> str:
        self.__pos += 1
        self.__pos_in_line += 1
        
    def before_char(self) -> str:
        self.__pos -= 1
        self.__pos_in_line -= 1

    def get_char(self, offset: int = 0) -> str:
        return self.__file.code[self.__pos + offset]
    
    def get_pos(self) -> int:
        return self.__pos
    
    def add_basic_token(self, token: tokens.Token) -> None:
        self.__basic_tokens.append(token)

    def add_token(self, token: tokens.Token) -> None:
        self.__tokens.append(token)

    def create_token(self, type: tokens.T_Types, value: str, lp: int = 0) -> tokens.Token:
        return tokens.Token(type, value, self.__line, self.__saved_pos_in_line).add_len(lp)
    
    def parse(self) -> None:
        char = self.get_char()

        if char == '/':
            if self.get_char(1) == '/':
                self.parse_comment()
                return
        
            elif self.get_char(1) == '*':
                self.parse_multi_line_comment()
                return

        if self.__symvols.check_in(char, self.__symvols.brackets):
            self.parse_bracket()
            return


        if char == '.':
            if (self.get_char(1) in self.__symvols.numbers):
                self.parse_number()
                return
            else:
                self.parse_operator()
                return

        if self.__symvols.check_in(char, self.__symvols.marks):
            self.parse_text()
            return
        if self.__symvols.check_in(char, self.__symvols.letters) or char == '_':   
            self.parse_word()
            return
        if self.__symvols.check_in(char, self.__symvols.numbers):
            self.parse_number()
            return
        if self.__symvols.check_in(char, self.__symvols.operators):
            self.parse_operator()
            return
        
    def save_pos_this_line(self):
        self.__saved_pos_in_line = copy(self.__pos_in_line)

    def parse_operator(self) -> None:
        operator = ''
        self.save_pos_this_line()
        while self.__symvols.check_in(self.get_char(), self.__symvols.operators):
            operator += self.get_char()
            self.next_char()
        
        self.add_basic_token(self.create_token(tokens.T_Types.T_OPERATOR, operator))
        

    def parse_number(self) -> None:
        number = ''
        self.save_pos_this_line()
        while self.__symvols.check_in(self.get_char(), self.__symvols.numbers) or self.get_char() == '.':
            number += self.get_char()
            self.next_char()
        
        self.add_basic_token(self.create_token(tokens.T_Types.T_NUMBER, number))

    def parse_word(self) -> None:
        word = ''
        self.save_pos_this_line()
        while self.__symvols.check_in(self.get_char(), self.__symvols.letters) or self.get_char() == '_' or self.__symvols.check_in(self.get_char(), self.__symvols.numbers):
            word += self.get_char()
            self.next_char()
        
        self.add_basic_token(self.create_token(tokens.T_Types.T_WORD, word))

    def parse_text(self) -> None:
        text = ''
        self.save_pos_this_line()
        self.next_char()
        while not self.__symvols.check_in(self.get_char(), self.__symvols.marks):
            if self.get_char() == '\n': self.__line += 1
            text += self.get_char()
            self.next_char()
        self.next_char()
        
        self.add_basic_token(self.create_token(tokens.T_Types.T_STRING, text, 2))

    def parse_bracket(self) -> None:
        self.save_pos_this_line()
        self.add_basic_token(self.create_token(tokens.T_Types.T_BRACKET, self.get_char()))
        self.next_char()
    
    def parse_comment(self) -> None:
        comment = ''
        self.save_pos_this_line()
        self.next_char()
        self.next_char()
        while self.get_char() != '\n':
            comment += self.get_char()
            self.next_char()
        
        self.add_basic_token(self.create_token(tokens.T_Types.T_COMMENTS, comment))

    def parse_multi_line_comment(self) -> None:
        comment = ''
        self.save_pos_this_line()
        self.next_char()
        self.next_char()

        
        while True:
            comment += self.get_char()
            self.next_char()
            if self.get_char() == '\n': self.__line += 1
            if self.get_char() == '*' and self.get_char(1) == '/': break

        self.__line += 1
        self.next_char()
        self.next_char()
        
        
        
        self.add_basic_token(self.create_token(tokens.T_Types.T_COMMENTS, comment))
    
    def analize(self) -> None:
        st = time.time()

        while self.__pos < self.__file.code_len:
            self.parse()
            try:
                if self.get_char() == ' ': self.next_char()
            except: ...

            try:
                if self.get_char() == '\n': 
                    self.__line += 1
                    self.next_char()
                    self.__pos_in_line = 0
            except: ...
            
    
        for t in self.__basic_tokens:
            if t.type == tokens.T_Types.T_WORD:
                
                if tokens.in_KeyWords(t.value):
                    t.set_identifier(tokens.get_identifier(t.value))
                    self.add_token(deepcopy(t))
                else:
                    self.add_token(deepcopy(t))
            else:

                self.add_token(deepcopy(t))
        self.__tokens.append(tokens.Token(tokens.T_Types.T_EOF, 'EOF', -2, -2))

        self.__spent_time = time.time() - st
        