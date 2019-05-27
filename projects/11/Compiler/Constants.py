# Token Types
KEYWORD = 'KEYWORD'
SYMBOL = 'SYMBOL'
IDENTIFIER = 'IDENTIFIER'
INT_CONST = 'INT_CONST'
STRING_CONST = 'STRING_CONST'

# Keywords
CLASS = 'class'
CONSTRUCTOR = 'constructor'
FUNCTION = 'function'
METHOD = 'method'
FIELD = 'field'
STATIC = 'static'
VAR = 'var'
INT = 'int'
CHAR = 'char'
BOOLEAN = 'boolean'
VOID = 'void'
TRUE = 'true'
FALSE = 'false'
NULL = 'null'
THIS = 'this'
LET = 'let'
DO = 'do'
IF = 'if'
ELSE = 'else'
WHILE = 'while'
RETURN = 'return'

KEYWORDS = [
    CLASS, CONSTRUCTOR, FUNCTION, METHOD, FIELD, STATIC, VAR,
    INT, CHAR, BOOLEAN, VOID, TRUE, FALSE, NULL, THIS, LET,
    DO, IF, ELSE, WHILE, RETURN
]

SYMBOLS = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*',
    '/', '&', '|', '<', '>', '=', '~']

OPS = ['+', '-', '*', '/', '&', '&amp;', '|', '<', '&lt;', '>', '&gt;', '=', '~']

# Used for handling identifiers
DEFINED = 'defined'
USED = 'used'
LOCAL = 'local'
ARGUMENT = 'argument'
SUBROUTINE = 'subroutine'
FIELD = 'field'
