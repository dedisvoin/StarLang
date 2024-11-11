from copy import copy, deepcopy
from typing import Any
from source.core import tokens
from source.structures import star_types
from source.structures import star_spaces
from source.structures import star_functions
from source.structures import star_lambdas

from source.core import errors
from source.parser import instructions
from source.parser import star_memory

class NumberExpression:
    def __init__(self, token: tokens.Token) -> None:
        self.__token = token
        self.__value = token.value
        if self.__value.count('.') == 0:
            self.__value = star_types.Star_V_Int.set_value(self.__value)
        elif self.__value.count('.') == 1:
            self.__value = star_types.Star_V_Float.set_value(self.__value)
        
    def eval(self):
        return self.__value
    

class StringExpression:
    def __init__(self, token: tokens.Token) -> None:
        self.__token = token
        self.__value = star_types.Star_V_String.set_value(self.__token.value)

    def eval(self):
        return self.__value
    

class ListExpression:
    def __init__(self, start_token: tokens.Token, end_token: tokens.Token, exprs, memory: star_memory.ContextMemory, error_handler: errors.ErrorHandler) -> None:
        self.__start_token = start_token
        self.__end_token = end_token
        self.__exprs = exprs
        self.__memory = memory
        self.__error_handler = error_handler

    def eval(self):
        return star_types.Star_V_List.set_value([e.eval() for e in self.__exprs])


class GetValueForIndexExpression:
    def __init__(self, expr, index_expr, start_token: tokens.Token, end_token: tokens.Token, error_handler: errors.ErrorHandler) -> None:
        self.__expr = expr
        self.__index_expr = index_expr
        self.__start_token = start_token
        self.__end_token = end_token
        self.__error_handler = error_handler
    
    def eval(self):
        expr_value: star_types.StarValue = self.__expr.eval()
        index_value = self.__index_expr.eval()
        if expr_value.get_type().get_name() != 'list':
            self.__error_handler.ERROR_VARIABLE_IS_NOT_ITTERABLE(self.__start_token, self.__end_token, expr_value)
        try:
            return expr_value.get_value()[index_value.get_value()]
        except IndexError:
            self.__error_handler.ERROR_LIST_INDEX_OUT_OF_RANGE(self.__start_token, self.__end_token, expr_value)


class VariableExpression:
    def __init__(self, token: tokens.Token, memory: star_memory.ContextMemory, error_handler: errors.ErrorHandler) -> None:
        self.__token = token
        self.__memory = memory
        self.__error_handler = error_handler

    def get_name(self):
        return self.__token.value

    def eval(self):
        try:
            memory_object = self.__memory.get_memory_object(self.__token.value)
        except:
            self.__error_handler.ERROR_VARIABLE_IS_NOT_DEFINE(self.__token)
        
        if memory_object is None:
            self.__error_handler.ERROR_VARIABLE_IS_NOT_DEFINE(self.__token)
        
        return memory_object.value


class NameSpaceVariableExpression:
    def __init__(self, start_token: tokens.Token ,end_token: tokens.Token, expr, error_handler: errors.ErrorHandler) -> None:
        self.__start_token = start_token
        self.__end_token = end_token
        self.__expr = expr
        self.__error_handler = error_handler

    def eval(self):
        
        name_space_var: star_types.StarValue = self.__expr.eval()

        
        if name_space_var.get_type().get_name() == 'namespace':
            space_memory = name_space_var.get_value().memory
            return VariableExpression(self.__start_token, space_memory, self.__error_handler).eval()
    
        elif name_space_var.get_type().get_name() == 'type':
            space_memory = name_space_var.get_value().get_space().get_value().memory
            return VariableExpression(self.__start_token, space_memory, self.__error_handler).eval()
        else:
            self.__error_handler.ERROR_VARIABLE_IS_NOT_NAME_SPACE(self.__start_token, self.__end_token)
        
        


class TypeExpression:
    def __init__(self, token: tokens.Token, memory: star_memory.ContextMemory, error_handler: errors.ErrorHandler) -> None:
        self.__token = token
        self.__memory = memory
        self.__error_handler = error_handler
    
    def eval(self):
        memory_object = self.__memory.get_memory_object(self.__token.value)
        if memory_object is None:
            self.__error_handler.ERROR_TYPE_NOT_DEFINITED(self.__token, self.__token.value)
            
        return memory_object.value
    

class BoolExpression:
    def __init__(self, token: tokens.Token) -> None:
        self.__token = token
        self.__value = star_types.Star_V_Bool.set_value(self.__token.value)

    def eval(self):
        return self.__value
    
    
class BinaryExpression:
    def __init__(self, left_expression, operator: str, right_expression, start_token, end_token, error_handler: errors.ErrorHandler) -> None:
        self.__left_expression = left_expression
        self.__operator = operator
        self.__right_expression = right_expression

        self.__start_token = start_token
        self.__end_token = end_token
        self.__error_handler = error_handler

    def eval(self):
        left_value = self.__left_expression.eval()
        right_value = self.__right_expression.eval()

        if star_types.is_basic_value(left_value) and star_types.is_basic_value(right_value):
            if star_types.is_value_type(left_value, star_types.Star_T_String) and star_types.is_value_type(right_value, star_types.Star_T_String):
                if self.__operator == '+':
                    return star_types.Star_V_String.set_value(left_value.get_value() + right_value.get_value())
                if self.__operator == '==':
                    return star_types.Star_V_Bool.set_value(left_value.get_value() == right_value.get_value())
                if self.__operator == '!=':
                    return star_types.Star_V_Bool.set_value(left_value.get_value() != right_value.get_value())
                

            elif star_types.is_value_type(left_value, star_types.Star_T_String) and star_types.is_value_type(right_value, star_types.Star_T_Int):
                if self.__operator == '*':
                    return star_types.Star_V_String.set_value(left_value.get_value() * right_value.get_value())
                

            elif star_types.is_value_type(left_value, star_types.Star_T_List) and star_types.is_value_type(right_value, star_types.Star_T_List):
                if self.__operator == '+':
                    return star_types.Star_V_List.set_value(left_value.get_value() + right_value.get_value())


            elif star_types.is_value_type(left_value, star_types.Star_T_Int) and star_types.is_value_type(right_value, star_types.Star_T_Int):
                if self.__operator == '+':
                    return star_types.Star_V_Int.set_value(left_value.get_value() + right_value.get_value())
                elif self.__operator == '-':
                    return star_types.Star_V_Int.set_value(left_value.get_value() - right_value.get_value())
                elif self.__operator == '*':
                    return star_types.Star_V_Int.set_value(left_value.get_value() * right_value.get_value())
                elif self.__operator == '/':
                    return star_types.Star_V_Int.set_value(left_value.get_value() / right_value.get_value())
                elif self.__operator == '%':
                    return star_types.Star_V_Int.set_value(left_value.get_value() % right_value.get_value())
                elif self.__operator == '>=':
                    return star_types.Star_V_Bool.set_value(left_value.get_value() >= right_value.get_value())
                elif self.__operator == '<=':
                    return star_types.Star_V_Bool.set_value(left_value.get_value() <= right_value.get_value())
                elif self.__operator == '>':
                    return star_types.Star_V_Bool.set_value(left_value.get_value() > right_value.get_value())
                elif self.__operator == '<':
                    return star_types.Star_V_Bool.set_value(left_value.get_value() < right_value.get_value())
                elif self.__operator == '==':
                    return star_types.Star_V_Bool.set_value(left_value.get_value() == right_value.get_value())
                elif self.__operator == '!=':
                    return star_types.Star_V_Bool.set_value(left_value.get_value() != right_value.get_value())
                
            
            elif (star_types.is_value_type(left_value, star_types.Star_T_Float) and star_types.is_value_type(right_value, star_types.Star_T_Int) or
                star_types.is_value_type(left_value, star_types.Star_T_Int) and star_types.is_value_type(right_value, star_types.Star_T_Float)):
                if self.__operator == '+':
                    return star_types.Star_V_Float.set_value(left_value.get_value() + right_value.get_value())
                elif self.__operator == '-':
                    return star_types.Star_V_Float.set_value(left_value.get_value() - right_value.get_value())
                elif self.__operator == '*':
                    return star_types.Star_V_Float.set_value(left_value.get_value() * right_value.get_value())
                elif self.__operator == '/':
                    return star_types.Star_V_Float.set_value(left_value.get_value() / right_value.get_value())
                elif self.__operator == '%':
                    return star_types.Star_V_Float.set_value(left_value.get_value() % right_value.get_value())
                elif self.__operator == '>=':
                    return star_types.Star_V_Bool.set_value(left_value.get_value() >= right_value.get_value())
                elif self.__operator == '<=':
                    return star_types.Star_V_Bool.set_value(left_value.get_value() <= right_value.get_value())
                elif self.__operator == '>':
                    return star_types.Star_V_Bool.set_value(left_value.get_value() > right_value.get_value())
                elif self.__operator == '<':
                    return star_types.Star_V_Bool.set_value(left_value.get_value() < right_value.get_value())
                elif self.__operator == '==':
                    return star_types.Star_V_Bool.set_value(left_value.get_value() == right_value.get_value())
                elif self.__operator == '!=':
                    return star_types.Star_V_Bool.set_value(left_value.get_value() != right_value.get_value())           


            elif (star_types.is_value_type(left_value, star_types.Star_T_Float) and star_types.is_value_type(right_value, star_types.Star_T_Float)):
                if self.__operator == '+':
                    return star_types.Star_V_Float.set_value(left_value.get_value() + right_value.get_value())
                elif self.__operator == '-':
                    return star_types.Star_V_Float.set_value(left_value.get_value() - right_value.get_value())
                elif self.__operator == '*':
                    return star_types.Star_V_Float.set_value(left_value.get_value() * right_value.get_value())
                elif self.__operator == '/':
                    return star_types.Star_V_Float.set_value(left_value.get_value() / right_value.get_value())
                elif self.__operator == '%':
                    return star_types.Star_V_Float.set_value(left_value.get_value() % right_value.get_value())
                elif self.__operator == '>=':
                    return star_types.Star_V_Bool.set_value(left_value.get_value() >= right_value.get_value())
                elif self.__operator == '<=':
                    return star_types.Star_V_Bool.set_value(left_value.get_value() <= right_value.get_value())
                elif self.__operator == '>':
                    return star_types.Star_V_Bool.set_value(left_value.get_value() > right_value.get_value())
                elif self.__operator == '<':
                    return star_types.Star_V_Bool.set_value(left_value.get_value() < right_value.get_value())
                elif self.__operator == '==':
                    return star_types.Star_V_Bool.set_value(left_value.get_value() == right_value.get_value())
                elif self.__operator == '!=':
                    return star_types.Star_V_Bool.set_value(left_value.get_value() != right_value.get_value())
            

            elif (star_types.is_value_type(left_value, star_types.Star_T_Bool) and star_types.is_value_type(right_value, star_types.Star_T_Bool)):
                if self.__operator == '==':
                    return star_types.Star_V_Bool.set_value(left_value.get_value() == right_value.get_value())
                elif self.__operator == '!=':
                    return star_types.Star_V_Bool.set_value(left_value.get_value() != right_value.get_value())
                elif self.__operator == '<':
                    return star_types.Star_V_Bool.set_value(left_value.get_value() < right_value.get_value())
                elif self.__operator == '>':
                    return star_types.Star_V_Bool.set_value(left_value.get_value() > right_value.get_value())
                elif self.__operator == '<=':
                    return star_types.Star_V_Bool.set_value(left_value.get_value() <= right_value.get_value())
                elif self.__operator == '>=':
                    return star_types.Star_V_Bool.set_value(left_value.get_value() >= right_value.get_value())
                elif self.__operator == '&&':
                    return star_types.Star_V_Bool.set_value(left_value.get_value() and right_value.get_value())
                elif self.__operator == '||':
                    return star_types.Star_V_Bool.set_value(left_value.get_value() or right_value.get_value())


            elif (star_types.is_value_type(left_value, star_types.Star_T_Type) and star_types.is_value_type(right_value, star_types.Star_T_Type)):
                
                if self.__operator == '==':
                    return star_types.Star_V_Bool.set_value(left_value.get_value() == right_value.get_value())
                elif self.__operator == '!=':
                    return star_types.Star_V_Bool.set_value(left_value.get_value() != right_value.get_value())
            
            else:
                if self.__operator == '==':
                    return star_types.Star_V_Bool.set_value(left_value.get_value() == right_value.get_value())
                elif self.__operator == '!=':
                    return star_types.Star_V_Bool.set_value(left_value.get_value() != right_value.get_value())

        self.__error_handler.ERROR_TYPES_TO_BINARY_OPERATOR(self.__start_token, self.__end_token, left_value, right_value, self.__operator)


class UnaryExpression:
    def __init__(self, operator: str, expression, start_token, end_token, error_handler: errors.ErrorHandler) -> None:
        self.__operator = operator
        self.__expression = expression

        self.__start_token = start_token
        self.__end_token = end_token
        self.__error_handler = error_handler
    
    def eval(self):
        value = self.__expression.eval()
        if star_types.is_basic_value(value):
            if star_types.is_value_type(value, star_types.Star_T_Int):
                if self.__operator == '-':
                    return star_types.Star_V_Int.set_value(-value.get_value())
                elif self.__operator == '+':
                    return star_types.Star_V_Int.set_value(+value.get_value())
            if star_types.is_value_type(value, star_types.Star_T_Float):
                if self.__operator == '-':
                    return star_types.Star_V_Float.set_value(-value.get_value())
                elif self.__operator == '+':
                    return star_types.Star_V_Float.set_value(+value.get_value())
            if star_types.is_value_type(value, star_types.Star_T_Bool):
                if self.__operator == '!':
                    return star_types.Star_V_Bool.set_value(not value.get_value())

        self.__error_handler.ERROR_TYPE_TO_UNARY_OPERATOR(self.__start_token, self.__end_token, value, self.__operator)


class CallExpression:
    def __init__(self, expr, exprs, start_token: tokens.Token, end_token: tokens.Token, error_handler: errors.ErrorHandler) -> None:
        self.__expr = expr
        self.__exprs = exprs
        self.__start_token = start_token
        self.__end_token = end_token
        self.__error_handler = error_handler

    def eval(self):
        callable_value: star_types.StarValue = self.__expr.eval()
        
        if callable_value.get_type().get_name() == star_types.Star_T_PyFunc.get_name():
            
            function_object: star_functions.PyStarFunction = callable_value.get_value()
            compiled_argments: list[star_types.StarValue] = []
            for expr in self.__exprs:
                compiled_argments.append(expr.eval())
            waited_args: list[star_functions.PyFunctionWaitArg] = function_object.waited_args

            # args count check
            
            if len(compiled_argments) == len(waited_args): pass
            else: self.__error_handler.ERROR_FUNCTION_ARGUMENTS_COUNT_NOT_MATCH(self.__start_token, self.__end_token, len(compiled_argments), len(waited_args), function_object.name)
            
            # args type check and mismatch
            # TODO ДОДЕЛАТЬ ПОДСТАНОВКУ СТАНДАРТНЫХ ЗНАЧЕНИЙ
            
            determinated_args = []
            
            
            
            
            for i, comp_arg in enumerate(compiled_argments):
                if comp_arg.get_type().get_name() in [t.get_name() for t in waited_args[i].types]: 
                    ...
                else: 
                    
                    self.__error_handler.ERROR_FUNCTION_ARGUMENTS_TYPE_NOT_MATCH(self.__start_token, self.__end_token, comp_arg.get_type().get_name(), [t.get_name() for t in waited_args[i].types], function_object.name, waited_args[i].name)
                
                determinated_args.append(comp_arg)
            
            
            try:
                
                fr = function_object.call(determinated_args, self.__error_handler)
                
            except errors.DummyStarError as e:
                self.__error_handler.CALL_ERROR(self.__start_token, self.__end_token, function_object.name, e.message)
            
            return fr
        
        elif callable_value.get_type().get_name() == star_types.Star_T_LambdaFunc.get_name():

            lambda_object: star_lambdas.StarLambda = callable_value.get_value()
            compiled_argments: list[star_types.StarValue] = []
            for expr in self.__exprs:
                compiled_argments.append(expr.eval())
            waited_args: list = lambda_object.wait_args

            
            # проверка на соответсвие количества аргументов
            if len(compiled_argments) <= len(waited_args): pass
            else: self.__error_handler.ERROR_FUNCTION_ARGUMENTS_COUNT_NOT_MATCH(self.__start_token, self.__end_token, len(compiled_argments), len(waited_args), 'anonymous lambda')

            
            determinated_args = []
            for i, w_arg in enumerate(waited_args):
                try:
                    comp_arg = compiled_argments[i]
                except:
                    try:
                        comp_arg = w_arg[2].eval()
                    except:
                        comp_arg = w_arg[2]

                compiled_types_names = [t.eval().get_value().get_name() for t in waited_args[i][1]]

                if len(compiled_types_names) > 0:
                    if comp_arg.get_type().get_name() in compiled_types_names: ...
                    else: self.__error_handler.ERROR_FUNCTION_ARGUMENTS_TYPE_NOT_MATCH(self.__start_token, self.__end_token, comp_arg.get_type().get_name(), compiled_types_names, 'anonymous lambda', waited_args[i][0].value)

                
                determinated_args.append(comp_arg)



            try:
                fr = lambda_object.call(determinated_args)
            except errors.DummyStarError as e:
                self.__error_handler.CALL_ERROR(self.__start_token, self.__end_token, lambda_object.name, e.message)

            if len(lambda_object.return_args) > 0:
                if fr.get_type().get_name() in [t.eval().get_value().get_name() for t in lambda_object.return_args]: pass
                else: raise 'error_return_type'

            return fr
        
        elif callable_value.get_type().get_name() == star_types.Star_T_StarFunc.get_name():
            function_object: star_functions.StarFunction = callable_value.get_value()
            compiled_argments: list[star_types.StarValue] = []
            for expr in self.__exprs:
                compiled_argments.append(expr.eval())
            waited_args: list = function_object.wait_args

            
            # проверка на соответсвие количества аргументов
            if len(compiled_argments) <= len(waited_args): pass
            else: self.__error_handler.ERROR_FUNCTION_ARGUMENTS_COUNT_NOT_MATCH(self.__start_token, self.__end_token, len(compiled_argments), len(waited_args), function_object.name)

            
            determinated_args = []
            for i, w_arg in enumerate(waited_args):
                try:
                    comp_arg = compiled_argments[i]
                except:
                    try:
                        comp_arg = w_arg[2].eval()
                    except:
                        comp_arg = w_arg[2]

                compiled_types_names = [t.eval().get_value().get_name() for t in waited_args[i][1]]

                if len(compiled_types_names) > 0:
                    if comp_arg.get_type().get_name() in compiled_types_names: ...
                    else: self.__error_handler.ERROR_FUNCTION_ARGUMENTS_TYPE_NOT_MATCH(self.__start_token, self.__end_token, comp_arg.get_type().get_name(), compiled_types_names, function_object.name, waited_args[i][0].value)

                
                determinated_args.append(comp_arg)



            try:
                fr = function_object.call(determinated_args)
            except instructions.ExcReturn as e:   
                fr = e.get_value()
                
            except errors.DummyStarError as e:
                self.__error_handler.CALL_ERROR(self.__start_token, self.__end_token, function_object.name, e.message)

            
            if len(function_object.return_args) > 0:
                if fr.get_type().get_name() in [t.eval().get_value().get_name() for t in function_object.return_args]: pass
                else: raise
            
            return fr

        
        
        
        else:
            self.__error_handler.ERROR_VARIABLE_IS_NOT_CALLABLE(self.__start_token, self.__end_token, callable_value.get_type())
        

class ListGeneratorExpression:
    def __init__(self, start_expr, end_expr, step_expr, memory: star_memory.ContextMemory, error_handler: errors.ErrorHandler):
        self.__start_expr = start_expr
        self.__end_expr = end_expr
        self.__step_expr = step_expr
        self.__memory = memory
        self.__error_handler = error_handler
        

    def eval(self):
        
        start_value = self.__start_expr.eval()
        end_value = self.__end_expr.eval()
        step_value = self.__step_expr.eval() if self.__step_expr != None else None
        
        if star_types.is_value_type(start_value, star_types.Star_T_Int) and star_types.is_value_type(end_value, star_types.Star_T_Int) and (step_value == None or star_types.is_value_type(step_value, star_types.Star_T_Int)):
            start_value = start_value.get_value()
            end_value = end_value.get_value()
            step_value = step_value.get_value() if step_value != None else 1
            
            arr = range(start_value, end_value, step_value)
            return star_types.Star_V_List.set_value([star_types.Star_V_Int.set_value(val) for val in arr])
            

class LambdaExpression:
    def __init__(self, arguments: list, return_argument_types: list, 
                 lambda_memory: star_memory.ContextMemory, lambda_expr, error_handler: errors.ErrorHandler, global_memory: star_memory.ContextMemory, 
                 use_inner_memory: bool = True, used_spaces: list = []) -> None:
        self.__waited_arguments = arguments
        self.__return_argument_types = return_argument_types
        self.__lambda_memory = lambda_memory
        self.__lambda_expr = lambda_expr
        self.__error_handler = error_handler
        self.__global_memory = global_memory
        self.__use_inner_memory = use_inner_memory
        self.__used_spaces = used_spaces

    def eval(self):
        return star_types.Star_V_LambdaFunc.set_value(
            star_lambdas.StarLambda(self.__waited_arguments, self.__return_argument_types, self.__lambda_expr, self.__lambda_memory, self.__error_handler, self.__global_memory, self.__use_inner_memory, self.__used_spaces)
        )
    

class FunctionExpression:
    def __init__(self, arguments: list, used_spaces: list, use_inner_memory: bool, return_type: list, 
                 function_instruction, global_memory: star_memory.ContextMemory, 
                 function_memory: star_memory.ContextMemory, error_handler: errors.ErrorHandler, name_expr) -> None:
        self.__arguments = arguments
        self.__used_spaces = used_spaces
        self.__use_inner_memory = use_inner_memory
        self.__return_type = return_type
        self.__function_instruction = function_instruction
        self.__global_memory = global_memory
        self.__function_memory = function_memory
        self.__error_handler = error_handler
        self.__name_expr = name_expr

    def eval(self):
        
        return star_types.Star_V_StarFunc.set_value(
            star_functions.StarFunction(self.__arguments, self.__used_spaces, self.__use_inner_memory, 
                                        self.__return_type, self.__function_instruction, 
                                        self.__global_memory, self.__function_memory, self.__error_handler,True, self.__name_expr)
        )