from copy import deepcopy
from source.structures import star_functions
from source.structures import star_spaces
from source.structures import star_types

from source.parser import star_memory
from source.parser import expressions

from source.core import errors
from source.core import tokens

"error"
def get_this_types_from_memory(type_names: list[str], memory: star_memory.ContextMemory) -> list[star_types.StarType]:
    type_memory_object = []
    for type_name in type_names:
        mo = memory.get_memory_object(type_name)
        if mo is not None:
            type_memory_object.append(mo.value)
    # TODO ДОДЕЛАТЬ ПРОВЕРКУ НА ОШИБКУ
    return type_memory_object
        

class DummyInstruction:
    def __init__(self) -> None:
        ...

    def exec(self):
        ...


class BasicIf:
    def __init__(self, condition, if_state, else_state, memory: star_memory.ContextMemory) -> None:
        self.__condition = condition
        self.__if_state = if_state
        self.__else_state = else_state
        self.__memory = memory

    def exec(self):
        if self.__condition.eval().get_value():
            self.__if_state.exec()
        else:
            self.__else_state.exec()


class BasicVarDefinition:
    def __init__(self, var_name: str, var_types: list[str], 
                 expression: None, memory: star_memory.ContextMemory, mutable: bool = True,
                 error_handler: errors.ErrorHandler | None = None,
                 start_types_token: tokens.Token | None = None, end_types_token: tokens.Token | None = None, 
                 start_expr_token: tokens.Token | None = None, end_expr_token: tokens.Token | None = None, static: bool = False) -> None:
        self.__var_name = var_name
        self.__var_types = var_types
        self.__expression = expression
        self.__memory = memory
        self.__mutable = mutable
        self.__static = static
        self.__error_handler = error_handler
        self.__inited = False if self.__expression is None else True

        self.__start_types_token = start_types_token
        self.__end_types_token = end_types_token
        self.__start_expr_token = start_expr_token
        self.__end_expr_token = end_expr_token

        self.__value = None


    def set_expr(self, expr):
        self.__expression = expr


    def set_value(self, value):
        self.__inited = True
        self.__value = value

    def exec(self):
        
        if self.__inited:
            try:
                self.__value = self.__expression.eval()
            except: 
                ...
                
        else:
            self.__value = star_types.Star_V_Null.set_value(None)
            
        
        
        
        waited_types = [type_expr.eval() for type_expr in self.__var_types]
        waited_types_names = [type_expr.eval().get_value().get_name() for type_expr in self.__var_types]
        if len(waited_types_names) > 0:
            self.__value.set_wait_types(waited_types_names)
        else:
            self.__value.set_wait_types([self.__value.get_type().get_name()])
        
        if len(waited_types) > 0:
            if len(waited_types) == 1 and waited_types_names[0] == 'auto':
                ...
            
            elif self.__value.get_type().get_name() not in waited_types_names:
                self.__error_handler.ERROR_INVALID_TYPE_OF_ASSIGNED_EXPR(self.__start_types_token, self.__end_types_token, self.__start_expr_token, self.__end_expr_token, self.__value, waited_types)
        
        if self.__memory.memory_object_exists(self.__var_name):
            if self.__memory.memory_object_is_static(self.__var_name):
                self.__error_handler.ERROR_STATIC_VAR_REDEFINITION(self.__start_expr_token, self.__end_expr_token, self.__var_name)
        

        
        self.__memory.add_memory_object(star_memory.MemoryObject(self.__var_name, self.__value, self.__mutable, self.__inited, self.__static))
        
        


class BasicTypeDefinition:
    def __init__(self, type_name: str, memory: star_memory.ContextMemory, expression, mutable: bool = False, 
                 error_handler: errors.ErrorHandler | None = None, static: bool = False,
                 token_start: tokens.Token | None = None, token_end: tokens.Token | None = None) -> None:
        self.__type_name = type_name
        self.__expression = expression
        self.__memory = memory
        self.__mutable = mutable
        self.__static = static
        self.__error_handler = error_handler
        self.__token_start = token_start
        self.__token_end = token_end

    def exec(self):
        value = self.__expression.eval()
        if self.__memory.memory_object_exists(self.__type_name):
            if self.__memory.memory_object_is_static(self.__type_name):
                self.__error_handler.ERROR_STATIC_TYPEDEF_REDEFINITION(self.__token_start, self.__token_end, self.__type_name)
        if star_types.is_value_type(value, star_types.Star_T_String):
            value = star_types.Star_V_Type.set_value(self.__type_name)

            self.__memory.add_memory_object(
                star_memory.MemoryObject(
                    self.__type_name, value,  self.__mutable, True, self.__static
                )
            )
        else:
            ...


class BasicInstructinsBlock:
    def __init__(self, instructions: list) -> None:
        self.__instructions = instructions
    
    def exec(self):
        for instruction in self.__instructions:
            instruction.exec()


class BasicSpaceDefinition:
    def __init__(self, space_name: str, space_memory: star_memory.ContextMemory, 
                 global_memory: star_memory.ContextMemory ,instructs: list, 
                 error_handler: errors.ErrorHandler | None = None, use_inner_memory: bool = False,
                 used_spaces: list = []) -> None:
        self.__space_name = space_name
        self.__space_memory = space_memory
        self.__global_memory = global_memory
        self.__use_inner_memory = use_inner_memory
        self.__error_handler = error_handler
        self.__inistructs = instructs
        self.__used_spaces = used_spaces

    def exec(self):
        

        sn = self.__space_name
        if type(self.__space_name) == expressions.StringExpression:
            sn = self.__space_name.eval().get_value()

        
        self.__space_memory.clear()
        if not self.__use_inner_memory:
            self.__space_memory.merge(self.__global_memory)
        else:
            if len(self.__used_spaces) > 0:
                for space_expr in self.__used_spaces:
                    
                    value_space = space_expr.eval()
                    
                    

                    self.__space_memory.add_memory_object(star_memory.MemoryObject(space_expr.get_name(), value_space, False, True, True))
        
        
        self.__inistructs.exec()
        
        space = star_spaces.StarSpace(sn, self.__space_memory, self.__inistructs)
        space_object = star_types.Star_V_Space.set_value(space)
        
        self.__global_memory.add_memory_object(star_memory.MemoryObject(sn, space_object, False))


def get_rec_values(values: list[star_types.StarValue]):
    result = []
    for value in values:
        if value.get_type().get_name() == 'list':
            result.append(get_rec_values(value.get_value()))
        else:
            if value.get_type().get_name() == 'string':
                result.append(str(value.get_value()).replace('\\n', '\n'))
            elif value.get_type().get_name():
                result.append(value.get_value())
            
    
    return result
    
    
class BasicOut:
    def __init__(self, exprs) -> None:
        self.__exprs = exprs

    def exec(self):
        values = [expr.eval() for expr in self.__exprs]
        print(*get_rec_values(values), sep='')


class BasicOutl:
    def __init__(self, exprs) -> None:
        self.__exprs = exprs

    def exec(self):
        values = [expr.eval() for expr in self.__exprs]
        print(*get_rec_values(values), end='')


class BaseForIn:
    def __init__(self, var_define_state: str, instructions: list, expr, memory: star_memory.ContextMemory) -> None:
        self.__var_define_state = var_define_state
        self.__instructions = instructions
        self.__expr = expr
        self.__memory = memory
        
    def exec(self):
        for value in self.__expr.eval().get_value():
            
            self.__var_define_state.set_value(value)
            self.__var_define_state.exec()
            try:
                self.__instructions.exec()
            except ExcContinue: continue
            except ExcBreak:    break


class BaseFor:
    def __init__(self, var_define_state: str, var_update_state: str, instructions: list, expr, memory: star_memory.ContextMemory) -> None:
        self.__var_define_state = var_define_state
        self.__var_update_state = var_update_state
        self.__instructions = instructions
        self.__expr = expr

        self.__memory = memory

    def exec(self):
        self.__var_define_state.exec()
        while self.__expr.eval().get_value():
            try:
                self.__instructions.exec()
            except ExcContinue: continue
            except ExcBreak:    break
            self.__var_update_state.exec()


class BasicWhile:
    def __init__(self, expr, instructions: list, memory: star_memory.ContextMemory) -> None:
        self.__expr = expr
        self.__instructions = instructions
        self.__memory = memory
    
    def exec(self):
        while self.__expr.eval().get_value():
            try:
                self.__instructions.exec()
            except ExcContinue: continue
            except ExcBreak:    break


class ExcContinue(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class BasicContinue:
    def __init__(self, memory: star_memory.ContextMemory) -> None:
        self.__memory = memory

    def exec(self):
        raise ExcContinue()


class ExcBreak(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class BasicBreak:
    def __init__(self, memory: star_memory.ContextMemory) -> None:
        self.__memory = memory
    
    def exec(self):
        raise ExcBreak()
    

class ExcReturn(BaseException):
    def __init__(self, expr) -> None:
        super().__init__()
        self.__expr = expr

    def get_value(self):
        ex = self.__expr.eval()
        return ex

class BasicReturn:
    def __init__(self, memory: star_memory.ContextMemory, expr) -> None:
        self.__memory = memory
        self.__expr = expr
    
    def exec(self):
        raise ExcReturn(self.__expr)


class BasicImport:
    def __init__(self, memory: star_memory.ContextMemory, expr, token_start: tokens.Token, token_end: tokens.Token, error_handler: errors.ErrorHandler, space_name: None | str = None) -> None:
        self.__memory = memory
        self.__expr = expr
        self.__token_start = token_start
        self.__token_end = token_end
        self.__error_handler = error_handler
        self.__space_name = space_name
    
    def exec(self):
        libs_paths_expr = self.__expr.eval()

        if libs_paths_expr.get_type().get_name() == 'string':
            libs_paths = [libs_paths_expr.get_value()]
        elif libs_paths_expr.get_type().get_name() == 'list':
            libs_paths = [name.get_value() for name in libs_paths_expr.get_value()]

        if self.__space_name is not None:
            
            BasicSpaceDefinition(self.__space_name, star_memory.ContextMemory(), self.__memory, BasicInstructinsBlock([]), self.__error_handler).exec()
        
        for path in libs_paths:
            try:
                PYSTARMODULE = star_functions.import_module_from_path(path)
            except: self.__error_handler.ERROR_PYTHON_MODULE_NOT_FOUND(self.__token_start, self.__token_end, path)
            try:
                FUNCTION_PACK: star_functions.PyFunctionPack = PYSTARMODULE.__dict__['FP']
            except: self.__error_handler.ERROR_PYTHON_NODULE_FUNCTION_PACK_NOT_FOUND(self.__token_start, self.__token_end, path)
            try:
                CONSTANT_PACK: star_functions.PyConstantsPack = PYSTARMODULE.__dict__['CP']
            except: self.__error_handler.ERROR_PYTHON_NODULE_CONSTANTS_PACK_NOT_FOUND(self.__token_start, self.__token_end, path)

            if self.__space_name is None:
                for func in FUNCTION_PACK.functs:
                    self.__memory.add_memory_object(star_memory.MemoryObject(func.name, star_types.Star_V_PyFunc.set_value(func), False))
            
                for const in CONSTANT_PACK.constants:
                    self.__memory.add_memory_object(star_memory.MemoryObject(const.name, const.value, False))
            else:
                mob: star_spaces.StarSpace = self.__memory.get_memory_object(self.__space_name).value.get_value()
                for func in FUNCTION_PACK.functs:
                    mob.memory.add_memory_object(star_memory.MemoryObject(func.name, star_types.Star_V_PyFunc.set_value(func), False))
                
                for const in CONSTANT_PACK.constants:
                    mob.memory.add_memory_object(star_memory.MemoryObject(const.name, const.value, False))


class BasicLeftArg:
    def __init__(self, expr) -> None:
        self.__expr = expr
    
    def exec(self):
        self.__expr.eval()


class BasicAssigned:
    def __init__(self, expr_left, expr, error_handler: errors.ErrorHandler, token_start: tokens.Token, token_end: tokens.Token) -> None:
        self.__error_handler = error_handler
        self.__expr_left = expr_left
        self.__start_token = token_start
        self.__end_token = token_end
        self.__expr = expr
    
    def exec(self):
        value = self.__expr_left.eval()
        if isinstance(self.__expr_left, expressions.NameSpaceVariableExpression):
            memory_identifier = self.__expr_left._NameSpaceVariableExpression__start_token.value
        else:
            memory_identifier = self.__expr_left._VariableExpression__token.value
        

        memory: star_memory.ContextMemory = value.get_memory()

        if not memory.memory_object_is_mutable(memory_identifier):
            self.__error_handler.ERROR_CONST_VAR_REDEFINITION(self.__start_token, self.__end_token, memory_identifier)
        
        evaluated_expression = self.__expr.eval()

        if memory.memory_object_is_static(memory_identifier):
            if evaluated_expression.get_type().get_name() not in memory.get_memory_object(memory_identifier).value.get_wait_types():
                self.__error_handler.ERROR_STATIC_VAR_VALUE_REDEFINITION(self.__start_token, self.__end_token, memory_identifier, 
                evaluated_expression.get_type(), memory.get_memory_object(memory_identifier).value.get_wait_types())

            
        memory.add_memory_object(star_memory.MemoryObject(memory_identifier, evaluated_expression, True))


class ImportModule:
    def __init__(self, memory: star_memory.ContextMemory, module_path: str, error_handler: errors.ErrorHandler, module_space_name: str | None = None):
        self.__memory = memory
        self.__module_path = module_path
        self.__error_handler = error_handler
        self.__module_space_name = module_space_name

    def exec(self):
        from source.Interpretator import StarIntepretator

        module_interpretator = StarIntepretator([0, self.__module_path])
        std = StarIntepretator([0, "runtime/__init__.star"])
        std.run()
        module_interpretator.preload_memory(std.get_memory())
        module_interpretator.run()

        if self.__module_space_name is None:
            for name in module_interpretator.get_memory().static_memory:
                self.__memory.static_memory[name] = module_interpretator.get_memory().static_memory[name]
        else:
            space_memory = star_memory.ContextMemory()
            for name in module_interpretator.get_memory().static_memory:
                space_memory.static_memory[name] = module_interpretator.get_memory().static_memory[name]

            ss = star_spaces.StarSpace(self.__module_space_name, space_memory, [])
            self.__memory.add_memory_object(star_memory.MemoryObject(self.__module_space_name, star_types.Star_V_Space.set_value(ss), True, True, False, None))