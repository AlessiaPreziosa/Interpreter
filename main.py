import os
import sys

from Interpreter import *
from Parser import *
from Lexer import *

def resource_path(relative_path):
    """ Get the absolute path to a resource. Works for both dev and PyInstaller."""
    try:
        # PyInstaller creates a temp folder and stores files in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

number = str(input('Insert a number: '))
case = resource_path('Tests/test_case_' + number + '.kt')
with open(case, 'r') as file:
    test = file.read()

# Lexer
lexer.input(test)

# Parser
as_tree = parser.parse(lexer=lexer)

print('\nThe following Abstract Syntax Tree is defined: \n')
print(as_tree)

# Interpreter
Interpreter().evaluate(as_tree)

print("🎉 Yay, you did it! 🎉")

