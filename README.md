# Formal Languages and Compilers Project: Kotlin Interpreter (in Python)

An Interpreter of Kotlin language is defined by:

1) A lexer that turns a sequence of characters (source program) into a sequence of tokens
2) A parser that takes the previous sequence of tokens and produces an abstract syntax tree (AST)
3) An interpreter (evaluator) that traverses the AST and executes the code line by line

---

## Tutorial

**Via PyCharm:** 
1. Execute `main.py`
2. Insert a number indicating the test case you want to interpret (from 0 to 6)

**Via Terminal (write the following commands):**
1. cd <path-to-project-directory>
2. python main.py
3. Insert a number indicating the test case you want to interpret (from 0 to 6)

N.B.: Test cases 3, 4 and 5 present errors

### How to create your own executable from console: 

- Linux/MacOS:

`pip install pyinstaller`
`pyinstaller --onefile --hidden-import=Interpreter --hidden-import=Parser --hidden-import=Lexer --add-data "Tests/*:Tests" -n Interpreter main.py`

- Windows:

`pip install pyinstaller`
`pyinstaller --onefile --hidden-import=Interpreter --hidden-import=Parser --hidden-import=Lexer --add-data "Tests/*;Tests" -n Interpreter main.py`

---

## Restriction of Kotlin’s grammar used

Kotlin grammar: https://kotlinlang.org/docs/reference/grammar.html

### DATA TYPES
1.	Boolean
2.	Integer
3.	String

### ARITHMETIC OPERATORS
1.	Addition (`+`)
2.	Subtraction (`-`)
3.	Multiplication (`*`)
4.	Division (`/`)

### LOGICAL OPERATORS
1.	Logical and (`&&`)
2.	Logical or (`||`)
3.	Logical not (`!`)

### COMPARISON OPERATORS
1.	Equal to (`==`)	
2.	Not equal (`!=`)
3.	Greater than (`>`)	
4.	Less than (`<`)	
5.	Greater than or equal to (`>=`)
6.	Less than or equal to (`<=`)

### BRANCHING INSTRUCTION
1.	`if (...) {...} else {...}`

### LOOP INSTRUCTION
1.	`while (...) {...}`
2.	`for (i in ...) {...}`

### I/O INSTRUCTION
1.	`println(...)` (O)
2.	`readLine(...)` (I)

### OTHER LANGUAGE FEATURES
1.	Functions
2.	Comments and Whitespaces (ignored during execution)

---

#### Libraries

PLY (Python Lex-Yacc): https://ply.readthedocs.io/en/latest/

Simple Colors: https://pypi.org/project/simple-colors/

PyInstaller: https://pyinstaller.org/en/stable/

---

**Students**: 

- Fioretti Maria Lucia (590016, m.fioretti1@studenti.poliba.it)

- Preziosa Alessia (590012, a.preziosa2@studenti.poliba.it)

