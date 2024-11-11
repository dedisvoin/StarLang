

# Импортируем модули ядра
from colorama import Fore
from source.core import operators
from source.core import tokens
from source.core import errors



# Импортируем классы выражений, инструкций, и памяти
from source.parser import expressions, instructions, star_memory
from source.structures import star_types



class Constructors:


    def ParseVariableTypesExprBracket(self: 'Parser'):
        type_expr = []
        if self.get_token_value() == '[':
            
            self.next_token()

            while self.get_token_value() != ']':

                self.error_wait_type(tokens.T_Types.T_WORD, '<definited type>')
                type_expr.append(self.analize_type_expression(self.get_global_memory()))

                if self.get_token_value() != ']' and self.get_token_value() != ',':
                    self.next_token()
                    self.error_wait_type(tokens.T_Types.T_OPERATOR, '<comma> ","')

                if self.get_token_value() == ',':
                    self.next_token()
                
                if self.get_token_value() == ']':
                    self.next_token()
                    break

        return type_expr


    def ParseVariableTypesExpr(self: 'Parser'):
        self.error_wait_type(tokens.T_Types.T_WORD, '<definited type>')
        type_expr = [self.analize_type_expression(self.get_global_memory())]
        return type_expr



    # Сборка выражения типа
    def ParseVariableTypesExprs(self: 'Parser'):
        if self.get_token_value() == '[':
            return self.ParseVariableTypesExprBracket()   
        else:
            return self.ParseVariableTypesExpr()
        
        
    # Сборка инструкции импорта модуля
    def ConstructImportModule(self: 'Parser', memory: star_memory.ContextMemory):
        self.next_token()

        self.error_wait_value('(', '<bracket> "("')
        self.next_token()

        

        self.error_wait_type(tokens.T_Types.T_STRING, '<module name>')
        module_name = self.get_token_value()
        self.next_token()

        self.error_wait_value(')', '<bracket> ")"')
        self.next_token()

        module_space_name = None
        if self.get_token_value() == 'as':
            self.next_token()

            self.error_wait_value('(', '<bracket> "("')
            self.next_token()
            self.error_wait_type(tokens.T_Types.T_WORD, '<module space name>')
            module_space_name = self.get_token_value()
            self.next_token()
            self.error_wait_value(')', '<bracket> ")"')
            self.next_token()

        self.error_wait_value(';', '<semicolon> ";"')
        self.next_token()

        return instructions.ImportModule(memory, module_name, self.get_private_error_handler, module_space_name)


    # Сборка иструкции присваивания выражения
    def ConstructBasicVarDefinition(self: 'Parser', memory: star_memory.ContextMemory):
        self.next_token()

        var_expression = None
        T_start_expr = self.get_token()
        T_end_expr = self.get_token()

        T_start_types = self.get_token()
        types_exprs = self.ParseVariableTypesExprBracket()
        T_end_types = self.get_token()

        
        self.error_wait_type(tokens.T_Types.T_WORD, '<variabele name>')
        var_name = self.get_token_value()
        self.next_token()

        if self.get_token_value() == ';':
            T_end_expr = self.get_token()
            self.next_token()
            return instructions.BasicVarDefinition(var_name, types_exprs, var_expression, memory, True, self.get_private_error_handler, T_start_types, T_end_types, T_start_expr, T_end_expr)

        self.error_wait_type(tokens.T_Types.T_OPERATOR, '<equal> "="')
        self.next_token()

        T_start_expr = self.get_token()
        var_expression = self.analize_basic_expression(memory)
        T_end_expr = self.get_token()

        self.error_wait_type(tokens.T_Types.T_OPERATOR, '<semicolon> ";"')
        self.next_token()

        return instructions.BasicVarDefinition(var_name, types_exprs, var_expression, memory, True, self.get_private_error_handler, T_start_types, T_end_types, T_start_expr, T_end_expr)



    # Cборка инструкции присваивания статического выражения
    def ConstructBasicStaticVarDefinition(self: 'Parser', memory: star_memory.ContextMemory):
        self.next_token()

        mutable = True
        if self.get_token_value() == 'const':
            mutable = False
            self.next_token()


        self.error_wait_type(tokens.T_Types.T_KEYWWORD, '<keyword> "var"')
        self.next_token()

        var_expression = None
        T_start_expr = self.get_token()
        T_end_expr = self.get_token()

        T_start_types = self.get_token()
        types_exprs = self.ParseVariableTypesExprBracket()
        T_end_types = self.get_token()

        self.error_wait_type(tokens.T_Types.T_WORD, '<variabele name>')
        var_name = self.get_token_value()
        self.next_token()
        
        if self.get_token_value() == '=':
            self.next_token()

            T_start_expr = self.get_token()
            var_expression = self.analize_basic_expression(memory)
            T_end_expr = self.get_token()

            self.error_wait_type(tokens.T_Types.T_OPERATOR, '<semicolon> ";"')
            self.next_token()
            
            
            return instructions.BasicVarDefinition(var_name, types_exprs, var_expression, memory, mutable, self.get_private_error_handler, T_start_types, T_end_types, T_start_expr, T_end_expr, True)

        elif self.get_token_value() == ';':
            self.next_token()

            return instructions.BasicVarDefinition(var_name, types_exprs, None, memory, mutable, self.get_private_error_handler, T_start_types, T_end_types, T_start_expr, T_end_expr, True)



    # Cборка инструкции присваивания статического выражения
    def ConstructBasicDynamicVarDefinition(self: 'Parser', memory: star_memory.ContextMemory):
        self.next_token()

        mutable = True
        if self.get_token_value() == 'const':
            mutable = False
            self.next_token()


        self.error_wait_type(tokens.T_Types.T_KEYWWORD, '<keyword> "var"')
        self.next_token()

        var_expression = None
        T_start_expr = self.get_token()
        T_end_expr = self.get_token()

        T_start_types = self.get_token()
        types_exprs = self.ParseVariableTypesExprBracket()
        T_end_types = self.get_token()

        self.error_wait_type(tokens.T_Types.T_WORD, '<variabele name>')
        var_name = self.get_token_value()
        self.next_token()
        
        
        self.error_wait_value('=', '<equal> "="')
        self.next_token()

        T_start_expr = self.get_token()
        var_expression = self.analize_basic_expression(memory)
        T_end_expr = self.get_token()

        self.error_wait_type(tokens.T_Types.T_OPERATOR, '<semicolon> ";"')
        self.next_token()

        return instructions.BasicVarDefinition(var_name, types_exprs, var_expression, memory, mutable, self.get_private_error_handler, T_start_types, T_end_types, T_start_expr, T_end_expr, False)



    # Сборка инструкции присваивания константного выражения
    def ConstructBasicConstVarDefinition(self: 'Parser', memory: star_memory.ContextMemory):
        self.next_token()

        self.error_wait_type(tokens.T_Types.T_KEYWWORD, '<keyword> "var"')
        self.next_token()

        var_expression = None
        T_start_expr = self.get_token()
        T_end_expr = self.get_token()

        T_start_types = self.get_token()
        types_exprs = self.ParseVariableTypesExprBracket()
        T_end_types = self.get_token()
        
        self.error_wait_type(tokens.T_Types.T_WORD, '<variabele name>')
        var_name = self.get_token_value()
        self.next_token()

        if self.get_token_value() == ';':
            self.next_token()
            return instructions.BasicVarDefinition(var_name, types_exprs, var_expression, memory, True, self.get_private_error_handler, T_start_types, T_end_types, T_start_expr, T_end_expr)


        self.error_wait_type(tokens.T_Types.T_OPERATOR, '<equal> "="')
        self.next_token()


        T_start_expr = self.get_token()
        var_expression = self.analize_basic_expression(memory)
        T_end_expr = self.get_token()


        self.error_wait_type(tokens.T_Types.T_OPERATOR, '<semicolon> ";"')
        self.next_token()
        return instructions.BasicVarDefinition(var_name, types_exprs, var_expression, memory, False, self.get_private_error_handler, T_start_types, T_end_types, T_start_expr, T_end_expr)
    


    # Сборка инструкции присваивания выражения
    def ConstructVarDefinition(self: 'Parser', memory: star_memory.ContextMemory):
        if self.get_token_value() == 'const':
            return self.ConstructBasicConstVarDefinition(memory)
        elif self.get_token_value() == 'static':
            return self.ConstructBasicStaticVarDefinition(memory)
        elif self.get_token_value() == 'dynamic':
            return self.ConstructBasicDynamicVarDefinition(memory)
        else:
            return self.ConstructBasicVarDefinition(memory)



    # Сборка инструкции создания ссылки на тип
    def ConstructBasicTypeDefinition(self: 'Parser', memory: star_memory.ContextMemory):
        T_start = self.get_token(0)
        
        self.next_token()

        static = False
        if self.get_token_value() == 'static':
            static = True
            self.next_token()
        elif self.get_token_value() == 'dynamic':
            static = False
            self.next_token()

        self.error_wait_type(tokens.T_Types.T_WORD, '<type name>')
        type_name = self.get_token_value()
        self.next_token()

        self.error_wait_value('=', '<equal> "="')
        self.next_token()
        
        type_expression = self.analize_basic_expression(memory)
        if type_expression is None : self.get_private_error_handler.ERROR_WAIT_TOKEN_TYPE(self.get_token(-1), '<type expression>, <type name (string)>')

        T_end = self.get_token()


        self.error_wait_value(';', '<semicolon> ";"')
        self.next_token()
        
        
        return instructions.BasicTypeDefinition(type_name, memory, type_expression, False, self.get_private_error_handler, static, T_start, T_end)
    

    # Сборка инструкции блока инструкций
    def ConstructInstructionsBlock(self: 'Parser', memory: star_memory.ContextMemory, wait_dot_and_comma = False):
        i = []
        self.next_token()
        while self.get_token_value() != '}':
            instruct = self.analize_basic_instruction(memory)
            if instruct is not None:
                i.append(instruct) 

        self.next_token()  
        if wait_dot_and_comma:
            self.error_wait_value(';', '<bracket> ";"')
            self.next_token()
        return instructions.BasicInstructinsBlock(i)
            


    # Сборка инструкции создания пространства
    def ConstructBasicSpaceDefinition(self: 'Parser', memory: star_memory.ContextMemory):
        self.next_token()

        self.error_wait_value('(', '<bracket> "("')
        self.next_token()


        
        space_name_expr = self.analize_basic_expression(memory)
        if space_name_expr is None:
            self.get_private_error_handler.ERROR_WAIT_TOKEN_TYPE(self.get_token(-1), '<space name expression>')
        
        self.error_wait_value(')', '<bracket> ")"')
        self.next_token()
        used_spaces = []
        if self.get_token_value() == '!':
            use_inner_memory = False
            self.next_token()
            if self.get_token_value() == '(':
                self.next_token()
                while self.get_token_value() != ')':
                    space_expr = self.analize_basic_expression(memory)
                    used_spaces.append(space_expr)

                    if self.get_token_value() == ',':
                        self.next_token()
                    elif self.get_token_value() == ')':
                        break
                    else:
                        self.error_wait_value(',', '<comma> ","')
                self.next_token()
                use_inner_memory = True
        else:
            use_inner_memory = True
        
        
        space_memory = star_memory.ContextMemory()

        i = self.analize_basic_instruction(space_memory)

        return instructions.BasicSpaceDefinition(space_name_expr, space_memory, memory, i, self.get_private_error_handler, use_inner_memory, used_spaces)
    


    # Сборка инструкции базового вывода
    def ConstructBaseOut(self: 'Parser', memory: star_memory.ContextMemory):
        self.next_token()
        exprs = []
        iterate = 0
        while True:
            expr = self.analize_basic_expression(memory)
            if expr is None:
                self.get_private_error_handler.ERROR_WAIT_TOKEN_TYPE(self.get_token(-1), '<expression>')
            exprs.append(expr)
            if self.get_token_value() == ';':
                break
            elif self.get_token_value() != ',':
                self.error_wait_value(',', '<comma> ","')
            
            self.next_token()
        self.next_token()
        return instructions.BasicOut(exprs)
    


    # Сборка инструкции базового вывода с переводом строки
    def ConstructBaseOutl(self: 'Parser', memory: star_memory.ContextMemory):
        self.next_token()
        exprs = []
        iterate = 0
        while True:
            expr = self.analize_basic_expression(memory)
            if expr is None:
                self.get_private_error_handler.ERROR_WAIT_TOKEN_TYPE(self.get_token(-1), '<expression>')
            exprs.append(expr)
            if self.get_token_value() == ';':
                break
            elif self.get_token_value() != ',':
                self.error_wait_value(',', '<comma> ","')
            
            self.next_token()
        self.next_token()
        return instructions.BasicOutl(exprs)
    


    # Сборка инструкции цикла forin
    def ConstructForIn(self: 'Parser', memory: star_memory.ContextMemory):
        self.next_token()
        self.error_wait_value('(', '<bracket> "("')
        self.next_token()

        iterable_expr = self.analize_basic_expression(memory)

        self.error_wait_value(';', '<comma> ","')
        self.next_token()

        var_define_state = self.ConstructVarDefinition(memory)

        self.error_wait_value(')', '<bracket> ")"')
        self.next_token()

        iterate_state = self.analize_basic_instruction(memory)

        return instructions.BaseForIn(var_define_state, iterate_state, iterable_expr, memory)



    # Сборка инструкции цикла for
    def ConstructFor(self: 'Parser', memory: star_memory.ContextMemory):
        
        self.error_wait_value('(', '<bracket> "("')
        self.next_token()
        
        var_define_state = self.analize_basic_instruction(memory)
        

        var_equal_expr = self.analize_basic_expression(memory)
        
        self.error_wait_value(';', '<semicolon> ";"')
        self.next_token()
        
        if self.get_token_value() == ';':
            var_update_state = instructions.DummyInstruction()
            self.next_token()
        else:
            var_update_state = self.analize_basic_instruction(memory)
        
        

        self.error_wait_value(')', '<bracket> ")"')
        self.next_token()

        iterate_state = self.analize_basic_instruction(memory)
        
        return instructions.BaseFor(var_define_state, var_update_state, iterate_state, var_equal_expr, memory)



    # Сборка инструкции цикла for or forin
    def ConstructBasicFor(self: 'Parser', memory: star_memory.ContextMemory):
        self.next_token()
        if self.get_token_value() == '~':
            return self.ConstructForIn(memory)
        else:
            return self.ConstructFor(memory)
        


    # Сборка инструкции импорта
    def ConstructBasicImport(self: 'Parser', memory: star_memory.ContextMemory):
        self.next_token()

        T_start = self.get_token()
        
        py_libs_names_expr = self.analize_basic_expression(memory);

        T_end = self.get_token()

        space_name = None
        if self.get_token_value() == 'as':
            self.next_token()
            self.error_wait_value('(', '<bracket> "("')
            self.next_token()
            self.error_wait_type(tokens.T_Types.T_WORD, '<space name>')
            space_name = self.get_token_value()
            self.next_token()
            self.error_wait_value(')', '<bracket> ")"')
            self.next_token()

        self.error_wait_value(';', '<semicolon> ";"')
        self.next_token()

        return instructions.BasicImport(memory, py_libs_names_expr, T_start, T_end, self.get_private_error_handler, space_name)
    


    # Сборка инструкции условного оператора
    def ConstructBasicIf(self: 'Parser', memory: star_memory.ContextMemory):
        self.next_token()
        self.error_wait_value('(', '<bracket> "("')
        self.next_token()

        expr = self.analize_basic_expression(memory)

        self.error_wait_value(')', '<bracket> ")"')
        self.next_token()

        if_state = self.analize_basic_instruction(memory)

        if self.get_token_value() == 'else':
            self.next_token()
            else_state = self.analize_basic_instruction(memory)
        else:
            else_state = instructions.DummyInstruction()

        return instructions.BasicIf(expr, if_state, else_state, memory)
    


    # Сборка инструкции цикла while
    def ConstructBasicWhile(self: 'Parser', memory: star_memory.ContextMemory):
        self.next_token()
        self.error_wait_value('(', '<bracket> "("')
        self.next_token()

        expr = self.analize_basic_expression(memory)

        self.error_wait_value(')', '<bracket> ")"')
        self.next_token()

        while_state = self.analize_basic_instruction(memory)

        return instructions.BasicWhile(expr, while_state, memory)



    # Сборка инструкции цикла continue
    def ConstructBasicContinue(self: 'Parser', memory: star_memory.ContextMemory):
        self.next_token()
        self.error_wait_value(';', '<semicolon> ";"')
        self.next_token()
        return instructions.BasicContinue(memory)



    # Сборка инструкции цикла break
    def ConstructBasicBreak(self: 'Parser', memory: star_memory.ContextMemory):
        self.next_token()
        self.error_wait_value(';', '<semicolon> ";"')
        self.next_token()
        return instructions.BasicBreak(memory)
    
    # Сборка инструкции return
    def ConstructBasicReturn(self: 'Parser', memory: star_memory.ContextMemory):
        self.next_token()
        expr = self.analize_basic_expression(memory)
        self.error_wait_value(';', '<semicolon> ";"')
        self.next_token()
        return instructions.BasicReturn(memory, expr)

        


class Parser(Constructors):
    def __init__(self, path: str) -> 'Parser':
        self.__tokens: list[tokens.Token] =     []
        self.__statements: list =               []
        self.__error_handler =                  errors.ErrorHandler(path)
        self.__path =                           path

        self.__pos =                            0
        self.__GLOBAL_MEMORY =                  star_memory.ContextMemory()


    # Метод для получения доступа к глобальной памяти
    def get_global_memory(self) -> star_memory.ContextMemory:
        return self.__GLOBAL_MEMORY
    

    # Метод слияния внешней области памяти с глобальной
    def add_to_global_memory(self, memory: star_memory.ContextMemory) -> star_memory.ContextMemory:
        for name in memory.static_memory:
            self.__GLOBAL_MEMORY.static_memory[name] = memory.static_memory[name]


    # Получение обработчика ошибок
    @property
    def get_private_error_handler(self) -> errors.ErrorHandler:
        return self.__error_handler


    # Получение списка инструкций
    def get_instructions(self) -> list:
        return self.__statements


    # Метод установки файла
    def set_file_path(self, path: str) -> None:
        self.__path = path
        self.__error_handler.set_file_path(self.__path)

    def next_token(self):
        self.__pos += 1
    
    def before_token(self):
        self.__pos -= 1

    def set_tokens(self, tokens: list[tokens.Token]):
        self.__tokens = tokens

    def get_token(self, offset: int = 0) -> tokens.Token:
        return self.__tokens[self.__pos + offset]
    
    def get_token_value(self, offset: int = 0) -> str:
        return self.get_token(offset).value
    
    def get_token_type(self, offset: int = 0) -> tokens.T_Types:
        return self.get_token(offset).type
    
    def signature_is_equal(self, signature: operators.Operator) -> bool:
        return self.get_token().signature.name == signature.name
    
    def match_signature(self, signature: operators.Operator) -> bool:
        if self.signature_is_equal(signature):
            self.next_token()
            return True
        return False
    
    def wait_type(self, type: tokens.T_Types):
        if self.get_token().type == type:
            return True
        return False
    
    def error_wait_type(self, type: tokens.T_Types, wait_token_value: str = ''):
        if self.wait_type(type):
            return True
        else:
            self.__error_handler.ERROR_WAIT_TOKEN_TYPE(self.get_token(-1), wait_token_value)

    def error_wait_value(self, value: str, wait_token_value: str = ''):
        if self.get_token_value() == value:
            return True
        else:
            self.__error_handler.ERROR_WAIT_TOKEN_TYPE(self.get_token(-1), wait_token_value)
            
    def error_wait_type_this(self, type: tokens.T_Types, wait_token_value: str = ''):
        if self.wait_type(type):
            return True
        else:
            self.__error_handler.ERROR_WAIT_TOKEN_TYPE(self.get_token(), wait_token_value)



    
    
    def analize(self, memory: star_memory.ContextMemory = None):
        return self.analize_basic_instruction(memory)





    def analize_basic_instruction(self, memory: star_memory.ContextMemory = None):
        
        # Парсинг инструкции присваивания 
        if (self.signature_is_equal(operators.SIGNATURES['var']) or 
            self.signature_is_equal(operators.SIGNATURES['const']) or 
            self.signature_is_equal(operators.SIGNATURES['static']) or
            self.signature_is_equal(operators.SIGNATURES['dynamic'])
        ):
            return self.ConstructVarDefinition(memory)
        
        
        # Парсинг инструкции определения ссылки на тип
        if self.signature_is_equal(operators.SIGNATURES['typedef']):
            return self.ConstructBasicTypeDefinition(memory)
        
        # Парсинг инструкции определения пространства имен
        if self.signature_is_equal(operators.SIGNATURES['space']):
            return self.ConstructBasicSpaceDefinition(memory)
        

        # Парсинг инструкции определения блока инструкций
        if self.signature_is_equal(operators.SIGNATURES['{']):
            return self.ConstructInstructionsBlock(memory)
        

        # Парсинг инструкции вывода
        if self.signature_is_equal(operators.SIGNATURES['out']):
            return self.ConstructBaseOut(memory)
        

        # Парсинг инструкции вывода с переводом строки
        if self.signature_is_equal(operators.SIGNATURES['outl']):
            return self.ConstructBaseOutl(memory)
        

        # Парсинг инструкции for
        if self.signature_is_equal(operators.SIGNATURES['for']):
            return self.ConstructBasicFor(memory)
        

        # Парсинг инструкции import
        if self.signature_is_equal(operators.SIGNATURES['import']):
            return self.ConstructBasicImport(memory)
        

        # Парсинг инструкции if
        if self.signature_is_equal(operators.SIGNATURES['if']):
            return self.ConstructBasicIf(memory)
        

        # Парсинг инструкции while
        if self.signature_is_equal(operators.SIGNATURES['while']):
            return self.ConstructBasicWhile(memory)
        

        # Парсинг инструкции continue
        if self.signature_is_equal(operators.SIGNATURES['continue']):
            return self.ConstructBasicContinue(memory)
        

        # Парсинг инструкции break
        if self.signature_is_equal(operators.SIGNATURES['break']):
            return self.ConstructBasicBreak(memory)
        
        
        # Парсинг инструкции return
        if self.get_token_value() == '|>':
            return self.ConstructBasicReturn(memory)
             
        # Парсинг инструкции импорта модуля
        if self.signature_is_equal(operators.SIGNATURES['module']):
            return self.ConstructImportModule(memory)
        
        if self.get_token_type() == tokens.T_Types.T_WORD:
            T_start = self.get_token()
            left_expr = self.analize_recursion_statement(memory)
            T_end = self.get_token()

            if self.get_token_value() == '=':
                self.next_token()
                right_expr = self.analize_basic_expression(memory)
                
                self.error_wait_value(';', '<semicolon> ";"')
                self.next_token()
                return instructions.BasicAssigned(left_expr, right_expr, self.__error_handler, T_start, T_end)

            self.error_wait_value(';', '<semicolon> ";"')
            self.next_token()

            return instructions.BasicLeftArg(left_expr)
            
        
        self.__error_handler.ERROR_INVALUD_INSTRUCTION(self.get_token())





    def analize_recursion_statement(self, memory: star_memory.ContextMemory = None):
        start_token = self.get_token(0)
        expr = self.analize_single_expression(memory)
        
        while True:
            if self.get_token_value() == '::':
                self.next_token()
                self.error_wait_type(tokens.T_Types.T_WORD, '<variable name')
                expr = expressions.NameSpaceVariableExpression(self.get_token(), start_token, expr, self.get_private_error_handler)
                self.next_token()
                continue
            if self.get_token_value() == '[':
                start_token = self.get_token()
                self.next_token()
                index_expr = self.analize_basic_expression(memory)
                self.error_wait_value(']', '<bracket> "]')
                self.next_token()
                expr = expressions.GetValueForIndexExpression(expr, index_expr, start_token, self.get_token(), self.__error_handler)
                continue
            if self.get_token_value() == '(':
                exprs = []
                self.next_token()
                if self.get_token_value() == ')':
                    self.next_token()
                else:
                    while self.get_token_value() != ')':
                        exprs.append(self.analize_basic_expression(memory))
                        if self.get_token_value() == ',':
                            self.next_token()
                        elif self.get_token_value() == ')':
                            self.next_token()
                            break
                        else:
                            self.error_wait_value('', '<comma> ","')
                
                
                expr = expressions.CallExpression(expr, exprs, start_token, self.get_token(), self.__error_handler)
                continue
            break
        
        return expr
        




    def analize_basic_expression(self, memory: star_memory.ContextMemory = None):
        return self.analize_binare_conditions_4(memory)
    




    def analize_binare_conditions_4(self, memory: star_memory.ContextMemory = None):
        start_token = self.get_token()
        expr = self.analize_binare_conditions_3(memory)
        while True:
            if self.get_token_value() == '&&':
                self.next_token()
                expr = expressions.BinaryExpression(expr, '&&', self.analize_binare_conditions_3(memory), start_token, self.get_token(), self.__error_handler)
                continue
            break
        return expr
    




    def analize_binare_conditions_3(self, memory: star_memory.ContextMemory = None):
        start_token = self.get_token()
        expr = self.analize_binare_conditions_2(memory)
        while True:
            if self.get_token_value() == '||':
                self.next_token()
                expr = expressions.BinaryExpression(expr, '||', self.analize_binare_conditions_2(memory), start_token, self.get_token(), self.__error_handler)
                continue
            break
        return expr
    




    def analize_binare_conditions_2(self, memory: star_memory.ContextMemory = None):
        start_token = self.get_token()
        expr = self.analize_binare_conditions_1(memory)
        while True:
            if self.get_token_value() == '==':
                self.next_token()
                expr = expressions.BinaryExpression(expr, '==', self.analize_binare_conditions_1(memory), start_token, self.get_token(), self.__error_handler)
                continue
            if self.get_token_value() == '!=':
                self.next_token()
                expr = expressions.BinaryExpression(expr, '!=', self.analize_binare_conditions_1(memory), start_token, self.get_token(), self.__error_handler)
                continue
            break
        return expr
    




    def analize_binare_conditions_1(self, memory: star_memory.ContextMemory = None):
        start_token = self.get_token()
        expr = self.analize_binare_expression_2(memory)
        while True:
            if self.get_token_value() == '>':
                self.next_token()
                expr = expressions.BinaryExpression(expr, '>', self.analize_binare_expression_2(memory), start_token, self.get_token(), self.__error_handler)
                continue
            if self.get_token_value() == '<':
                self.next_token()
                expr = expressions.BinaryExpression(expr, '<', self.analize_binare_expression_2(memory), start_token, self.get_token(), self.__error_handler)
                continue
            if self.get_token_value() == '>=':
                self.next_token()
                expr = expressions.BinaryExpression(expr, '>=', self.analize_binare_expression_2(memory), start_token, self.get_token(), self.__error_handler)
                continue
            if self.get_token_value() == '<=':
                self.next_token()
                expr = expressions.BinaryExpression(expr, '<=', self.analize_binare_expression_2(memory), start_token, self.get_token(), self.__error_handler)
                continue
            break
        return expr
    




    def analize_binare_expression_2(self, memory: star_memory.ContextMemory = None):
        start_token = self.get_token()
        expr = self.analize_binare_expression_1(memory)
        while True:
            if self.get_token_value() == '+':
                self.next_token()
                expr = expressions.BinaryExpression(expr, '+', self.analize_binare_expression_1(memory), start_token, self.get_token(), self.__error_handler)
                continue
            if self.get_token_value() == '-':
                self.next_token()
                expr = expressions.BinaryExpression(expr, '-', self.analize_binare_expression_1(memory), start_token, self.get_token(), self.__error_handler)
                continue
            break
        return expr
    




    def analize_binare_expression_1(self, memory: star_memory.ContextMemory = None):
        start_token = self.get_token()
        expr = self.analize_unary_expression(memory)
        while True:
            if self.get_token_value() == '/':
                self.next_token()
                expr = expressions.BinaryExpression(expr, '/', self.analize_unary_expression(memory), start_token, self.get_token(), self.__error_handler)
                continue
            if self.get_token_value() == '*':
                self.next_token()
                expr = expressions.BinaryExpression(expr, '*', self.analize_unary_expression(memory), start_token, self.get_token(), self.__error_handler)
                continue
            if self.get_token_value() == '%':
                self.next_token()
                expr = expressions.BinaryExpression(expr, '%', self.analize_unary_expression(memory), start_token, self.get_token(), self.__error_handler)
                continue
            break
        return expr





    def analize_unary_expression(self, memory: star_memory.ContextMemory = None):
        start_token = self.get_token()
        if self.get_token_type() == tokens.T_Types.T_OPERATOR:
            if self.get_token_value() == '-':
                self.next_token()
                return expressions.UnaryExpression('-', self.analize_calls(memory), start_token, self.get_token(), self.__error_handler)
            if self.get_token_value() == '+':
                self.next_token()
                return expressions.UnaryExpression('-', self.analize_calls(memory), start_token, self.get_token(), self.__error_handler)
            if self.get_token_value() == '!':
                self.next_token()
                return expressions.UnaryExpression('!', self.analize_calls(memory), start_token, self.get_token(), self.__error_handler)
        
        return self.analize_calls(memory)




    # TODO write namespaces calls
    def analize_calls(self, memory: star_memory.ContextMemory = None):
        start_token = self.get_token()
        expr = self.analize_single_expression(memory)
        
        while True:
            if self.get_token_value() == '::':
                self.next_token()
                self.error_wait_type(tokens.T_Types.T_WORD, '<variable name')
                expr = expressions.NameSpaceVariableExpression(self.get_token(), start_token, expr, self.get_private_error_handler)
                self.next_token()
                continue
            if self.get_token_value() == '[':
                start_token = self.get_token()
                self.next_token()
                index_expr = self.analize_basic_expression(memory)
                self.error_wait_value(']', '<bracket> "]')
                self.next_token()
                expr = expressions.GetValueForIndexExpression(expr, index_expr, start_token, self.get_token(), self.__error_handler)
                continue
            if self.get_token_value() == '(':
                exprs = []
                self.next_token()
                if self.get_token_value() == ')':
                    self.next_token()
                else:
                    while self.get_token_value() != ')':
                        exprs.append(self.analize_basic_expression(memory))
                        if self.get_token_value() == ',':
                            self.next_token()
                        elif self.get_token_value() == ')':
                            self.next_token()
                            break
                        else:
                            self.error_wait_value('', '<comma> ","')
                
                
                expr = expressions.CallExpression(expr, exprs, start_token, self.get_token(), self.__error_handler)
                continue
            break
        
        return expr





    def analize_single_expression(self, memory: star_memory.ContextMemory = None):
        # Parse Number
        if self.get_token_type() == tokens.T_Types.T_NUMBER:
            expr = expressions.NumberExpression(self.get_token())
            self.next_token()
            return expr
        
        # Parse String
        if self.get_token_type() == tokens.T_Types.T_STRING:
            expr = expressions.StringExpression(self.get_token())
            self.next_token()
            return expr
        
        # Parse Bool
        if self.get_token_value() == 'true' or self.get_token_value() == 'false':
            expr = expressions.BoolExpression(self.get_token())
            self.next_token()
            return expr
        
        # Parse Bracket
        if self.get_token_type() == tokens.T_Types.T_BRACKET:
            if self.get_token_value() == '(':
                self.next_token()
                expr = self.analize_basic_expression(memory)
                self.error_wait_type(tokens.T_Types.T_BRACKET, '(')
                self.next_token()
                return expr
            
        # Parse List
        if self.get_token_type() == tokens.T_Types.T_BRACKET:
            if self.get_token_value() == '[':
                self.next_token()
                T_start = self.get_token()
                exprs = []
                while True:
                    expr = self.analize_basic_expression(memory)
                    if expr is not None:
                        exprs.append(expr)
                    else:
                        if self.get_token_value() == ']':
                            self.next_token()
                            break
                    
                    if self.get_token_value() == ']':
                        self.next_token()
                        break
                    else:
                        
                        self.error_wait_value(',', '<comma> ","')
                        self.next_token()
                T_end =  self.get_token()
                return expressions.ListExpression(T_start, T_end, exprs, memory, self.__error_handler)

        # Parse ListGenerator:
        if self.get_token_value() == '~' and self.get_token_value(1) == '[':
            self.next_token()
            self.next_token()
            start_expr = self.analize_basic_expression(memory)

            self.error_wait_value('->', '<arrow> "->"')
            self.next_token()

            end_expr = self.analize_basic_expression(memory)

            if self.get_token_value() == ':':
                self.next_token()
                step_expr = self.analize_basic_expression(memory)
            else:
                step_expr = None
            
            self.error_wait_value(']', '<bracket> "]')
            self.next_token()
            
            return expressions.ListGeneratorExpression(start_expr, end_expr, step_expr, memory, self.__error_handler)

        # Parse Variable
        if self.get_token_type() == tokens.T_Types.T_WORD:
            expr = expressions.VariableExpression(self.get_token(), memory, self.__error_handler)
            self.next_token()
            return expr

        # Parse Lambda
        if self.get_token_type() == tokens.T_Types.T_KEYWWORD and self.get_token_value() == 'lambda':
            return self.analize_lambda_expression(memory)
    
        # Parse Function
        if self.get_token_type() == tokens.T_Types.T_KEYWWORD and self.get_token_value() == 'func':
            return self.analize_function_expression(memory)
        




    def analize_function_expression(self, memory: star_memory.ContextMemory = None):
        self.next_token()

        arguments = self.analize_lambda_arguments(memory)
        used_spaces = []
        
        if self.get_token_value() == '[':
            self.next_token()
            
            name_expr = self.analize_basic_expression(memory)
            self.error_wait_value(']', '<bracket> "]"')
            self.next_token()
        else:
            name_expr = None

        if self.get_token_value() == '!':
            use_inner_memory = False
            self.next_token()

            if self.get_token_value() == '(':
                self.next_token()
                while self.get_token_value() != ')':
                    space_expr = self.analize_basic_expression(memory)
                    used_spaces.append(space_expr)

                    if self.get_token_value() == ',':
                        self.next_token()
                    elif self.get_token_value() == ')':
                        break
                    else:
                        self.error_wait_value(',', '<comma> ","')
                self.next_token()
                use_inner_memory = True
        else:
            use_inner_memory = True

        
        if self.get_token_value() == ':':
            self.next_token()
            return_type = self.ParseVariableTypesExprs()
        else:
            return_type = []
        
        self.error_wait_value(';', '<semicolon> ";"')
        self.next_token()

        function_memory = star_memory.ContextMemory()

        function_instructions = self.analize_basic_instruction(function_memory)
        fe = expressions.FunctionExpression(arguments, used_spaces, use_inner_memory, return_type, function_instructions, 
                                              memory, function_memory, self.__error_handler, name_expr)
        
        return fe


                

    def analize_lambda_expression(self, memory: star_memory.ContextMemory = None):
        self.next_token()
        
        arguments = self.analize_lambda_arguments(memory)
        used_spaces = []
        if self.get_token_value() == '!':
            use_inner_memory = False
            self.next_token()
            
            if self.get_token_value() == '(':
                self.next_token()
                while self.get_token_value() != ')':
                    space_expr = self.analize_basic_expression(memory)
                    used_spaces.append(space_expr)
                    
                    if self.get_token_value() == ',':
                        self.next_token()
                    elif self.get_token_value() == ')':
                        break
                    else:
                        self.error_wait_value(',', '<comma> ","')
                self.next_token()
                use_inner_memory = True
        else:
            use_inner_memory = True
        
        if self.get_token_value() == ':':
            self.next_token()
            return_type = self.ParseVariableTypesExprs()
        else:
            return_type = []

        
        

        self.error_wait_value('{', '<bracket> "{"')
        self.next_token()

        lambda_memory = star_memory.ContextMemory()
        lambda_expr = self.analize_basic_expression(lambda_memory)
        if lambda_expr is None:
            self.__error_handler.ERROR_WAIT_TOKEN_TYPE(self.get_token(-1), '<expression> "expression"')
        self.error_wait_value('}', '<bracket> "}"')
        self.next_token()

        
        return expressions.LambdaExpression(arguments, return_type, lambda_memory, lambda_expr, self.__error_handler, memory, use_inner_memory, used_spaces)
        

        

    
    def analize_lambda_arguments(self, memory: star_memory.ContextMemory = None):
        self.error_wait_value('(', '<bracket> "("')
        self.next_token()
        args = []
        

        while True:
            if self.get_token_value() == ')':
                self.next_token()
                break

            self.error_wait_type(tokens.T_Types.T_WORD, '<argument> "word"')
            arg_name = self.get_token()
            arg_types = []
            self.next_token()
            if self.get_token_value() == ':':
                self.next_token()
                arg_types = self.ParseVariableTypesExprs()

            if self.get_token_value() == '=':
                self.next_token()
                arg_default_value = self.analize_basic_expression(memory)
            else:
                arg_default_value = star_types.Star_V_Null.set_value(None)
            
            args.append((arg_name, arg_types, arg_default_value))
            if self.get_token_value() == ',':
                self.next_token()
                continue
            else:
                self.error_wait_value(')', '<bracket> ")"')
                self.next_token()
                break

        return args
            




    def analize_type_expression(self, memory: star_memory.ContextMemory = None):
        return self.analize_basic_type_expression(memory)
        




    def analize_basic_type_expression(self, memory: star_memory.ContextMemory = None):
        if self.get_token_type() == tokens.T_Types.T_WORD:
            expr = expressions.TypeExpression(self.get_token(), memory, self.__error_handler)
            self.next_token()
            return expr





    def parse(self):
        while not self.signature_is_equal(operators.SIGNATURES['EOF']):
            self.__statements.append(self.analize(self.__GLOBAL_MEMORY))


class Executer:
    def __init__(self, ) -> None:
        self.__instructions: list = []

    def set_instructions(self, instructions: list):
        self.__instructions = instructions

    def run(self, print_instructs: bool = False):
        for i, instruction in enumerate(self.__instructions):
            if print_instructs:
                print(f'{Fore.YELLOW}~{Fore.RESET}Instruction: {Fore.BLACK}({i+1}){Fore.RESET} {Fore.MAGENTA}{instruction.__class__.__name__}{Fore.RESET}')
            instruction.exec()
