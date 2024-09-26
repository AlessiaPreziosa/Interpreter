# A lexer is the part of an interpreter that turns a sequence of characters (source program) into a sequence of tokens
import ply.lex as lex # Import Lex module

# List of token names:
# All lexers must provide a list of tokens that defines all the possible token names that can be produced.

tokens = ('ID', 'ASSIGN', 'NUMBER', 'LITERAL', # identifiers
          'AND', 'OR', 'NOT',  # logical operators
          'EQUALS', 'NEQUALS', 'GT', 'LT', 'GTE', 'LTE',  # comparison operators
          'MINUS', 'PLUS', 'TIMES', 'DIVIDE', # arithmetic operators
          'SLCOMM', 'MLCOMM',  # comment
          'LBRACE', 'RBRACE', 'LPAREN', 'RPAREN', 'COMMA', 'COLONS', 'SEMI', 'RANGE' # grammar
          )

# Reserved keywords
reserved = {
    'Int': 'INT',
    'Boolean': 'BOOLEAN',
    'String': 'STRING',
    'val': 'VAL',
    'var': 'VAR',
    'true': 'TRUE',
    'false': 'FALSE',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'in': 'IN',
    'step': 'STEP',
    'readLine': 'READLINE',
    'println': 'PRINTLN',
    'fun': 'FUN',
    'return': 'RETURN',
    'downTo' : 'DOWNTO'
}

# All tokens
tokens += tuple(reserved.values())

# Regular expression rules for tokens:
# the name following the t_ must exactly match one of the names supplied in tokens.

t_MINUS = r'-'
t_PLUS = r'\+'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'
t_EQUALS = r'=='
t_NEQUALS = r'!='
t_GT = r'>'
t_LT = r'<'
t_LTE = r'<='
t_GTE = r'>='
t_ASSIGN = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_RANGE = r'\.\.'
t_SEMI = r';'
t_COLONS = r':'
t_COMMA = r', '
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_ignore = ' \t'  # string containing ignored characters (spaces and tabs)

# Regular expression rules with some action code

# Regex for Identifiers and reserved words
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*' # match for an Identifier
    t.type = reserved.get(t.value, 'ID')

    if t.value == 'true':
        t.value = True
    if t.value == 'false':
        t.value = False

    return t

# Regex for Literal Strings
def t_LITERAL(t):
    r'"[^\n"]+"' # match for a String
    t.value = t.value[1:-1] # only the string is returned, without double quotes
    return t

# Regex for Integer Numbers
def t_NUMBER(t):
    r'\d+' # match for a digit
    t.value = int(t.value)
    return t

# Comment management: Ignore
def t_SLCOMM(t):
    r'\/\/[^\n\r]+' # match for single-line comment
    pass

def t_MLCOMM(t):
    r'/\*[\s\S]*?\*/' # match for multi-line comment
    t.lexer.lineno += t.value.count('\n')
    pass

# Error Handling
def t_error(t):
    t.lexer.skip(1)
    print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")

# Track new lines
def t_newline(t):
    r'\n+' # match for a new line
    t.lexer.lineno += len(t.value)

# Build the lexer
lexer = lex.lex()
