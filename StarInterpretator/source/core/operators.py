OPERATOR_EQUAL_EQUAL = "=="
OPERATOR_NOT_EQUAL = "!="
OPERATOR_GREATER_THAN = ">"
OPERATOR_GREATER_THAN_OR_EQUAL = ">="
OPERATOR_LESS_THAN = "<"
OPERATOR_LESS_THAN_OR_EQUAL = "<="
OPERATOR_DOT = "."
OPERATOR_DOUBLE_DOT = ":"
OPERATOR_DOT_AND_DOT = ".."

OPERATOR_BRACKET_LEFT = "("
OPERATOR_BRACKET_RIGHT = ")"
OPERATOR_BRACKET_CURLY_LEFT = "{"
OPERATOR_BRACKET_CURLY_RIGHT = "}"
OPERATOR_BRACKET_SQUARE_LEFT = "["
OPERATOR_BRACKET_SQUARE_RIGHT = "]"

OPERATOR_EQUAL = "="
OPERATOR_DOT_AND_COMMA = ";"
OPERATOR_RETURN = '|>'

OPERATOR_MINUS = "-"
OPERATOR_PLUS = "+"
OPERATOR_MULTIPLY = "*"
OPERATOR_DIVIDE = "/"
OPERATOR_MODULO = "%"
OPERATOR_NOT = '!'
OPERATOR_COMMA = ','
OPERATOR_PLUS_PLUS = "++"
OPERATOR_MINUS_MINUS = "--"


KEYWORD_VAR = "var"
KEYWORD_CONST = "const"
KEYWORD_STATIC = "static"
KEYWORD_DYNAMIC = "dynamic"
KEYWORD_IF = "if"
KEYWORD_ELSE = "else"
KEYWORD_WHILE = "while"
KEYWORD_FOR = "for"
KEYWORD_FUNC = "func"
KEYWORD_TYPEDEF = "typedef"
KEYWORD_SPACE = "space"
KEYWORD_OUT = "out"
KEYWORD_OUTl = 'outl'
KEYWORD_IMPORT = "import"
KEYWORD_CONTINUE = "continue"
KEYWORD_BREAK = "break"
KEYWORD_MODULE = "module"

OPERATOR_EOF = 'EOF'



class Operator:
    def __init__(self, name: str) -> None:
        self.name = name


SIGNATURES = {
    "EOF":          Operator(OPERATOR_EOF),
    "var":          Operator(KEYWORD_VAR),
    "const":        Operator(KEYWORD_CONST),
    'typedef':      Operator(KEYWORD_TYPEDEF),
    'space':        Operator(KEYWORD_SPACE),
    'out':          Operator(KEYWORD_OUT),
    'outl':         Operator(KEYWORD_OUTl),
    'for':          Operator(KEYWORD_FOR),
    'import':       Operator(KEYWORD_IMPORT),
    'while':        Operator(KEYWORD_WHILE),
    'continue':     Operator(KEYWORD_CONTINUE),
    'break':        Operator(KEYWORD_BREAK),
    'static':       Operator(KEYWORD_STATIC),
    'dynamic':      Operator(KEYWORD_DYNAMIC),
    'module':       Operator(KEYWORD_MODULE),
    'if':           Operator(KEYWORD_IF),
    "-":            Operator(OPERATOR_MINUS),
    "+":            Operator(OPERATOR_PLUS),
    "*":            Operator(OPERATOR_MULTIPLY),
    "/":            Operator(OPERATOR_DIVIDE),
    "%":            Operator(OPERATOR_MODULO),
    '!':            Operator(OPERATOR_NOT),
    ',':            Operator(OPERATOR_COMMA),
    '{':            Operator(OPERATOR_BRACKET_CURLY_LEFT),
    '}':            Operator(OPERATOR_BRACKET_CURLY_RIGHT),

    '++':           Operator(OPERATOR_PLUS_PLUS),
    '--':           Operator(OPERATOR_MINUS_MINUS),

}



OPERATORS = [
    Operator(OPERATOR_EQUAL_EQUAL),
    Operator(OPERATOR_NOT_EQUAL),
    Operator(OPERATOR_GREATER_THAN),
    Operator(OPERATOR_GREATER_THAN_OR_EQUAL),
    Operator(OPERATOR_LESS_THAN),
    Operator(OPERATOR_LESS_THAN_OR_EQUAL),
    Operator(OPERATOR_DOT),
    Operator(OPERATOR_DOUBLE_DOT),
    Operator(OPERATOR_DOT_AND_DOT),

    Operator(OPERATOR_EQUAL),
    Operator(OPERATOR_DOT_AND_COMMA),
    Operator(OPERATOR_RETURN),
    Operator(OPERATOR_EOF),

    Operator(OPERATOR_BRACKET_LEFT),
    Operator(OPERATOR_BRACKET_RIGHT),
    Operator(OPERATOR_BRACKET_CURLY_LEFT),
    Operator(OPERATOR_BRACKET_CURLY_RIGHT),
    Operator(OPERATOR_BRACKET_SQUARE_LEFT),
    Operator(OPERATOR_BRACKET_SQUARE_RIGHT),

    Operator(KEYWORD_VAR),
    Operator(KEYWORD_CONST),
    Operator(KEYWORD_IF),
    Operator(KEYWORD_ELSE),
    Operator(KEYWORD_WHILE),
    Operator(KEYWORD_FOR),
    Operator(KEYWORD_FUNC),
    Operator(KEYWORD_TYPEDEF),
    Operator(KEYWORD_SPACE),
    Operator(KEYWORD_OUT),
    Operator(KEYWORD_OUTl),
    Operator(KEYWORD_IMPORT),
    Operator(KEYWORD_CONTINUE),
    Operator(KEYWORD_BREAK),
    Operator(KEYWORD_MODULE),

    Operator(OPERATOR_MINUS),
    Operator(OPERATOR_PLUS),
    Operator(OPERATOR_MULTIPLY),
    Operator(OPERATOR_DIVIDE),
    Operator(OPERATOR_MODULO),
    Operator(OPERATOR_NOT),
    Operator(OPERATOR_COMMA),
    Operator(OPERATOR_PLUS_PLUS),
    Operator(OPERATOR_MINUS_MINUS),

]

def this_is_operator(name: str) -> bool:
    for operator in OPERATORS:
        if operator.name == name:
            return True
    return False

def get_operator(name: str) -> Operator:
    for operator in OPERATORS:
        if operator.name == name:
            return operator
    return None