# A parser takes a sequence of tokens (produced by the lexer) and produces an abstract syntax tree (AST)
# of the Kotlin language's restriction.

import ply.yacc as yacc
from Lexer import *        # Required Tokens' map from the lexer
from ASTNode import *

# Precedence (from lowest to highest)
# and associativity (left, right and nonassoc) of operators
precedence = (
    ('right', 'ASSIGN'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQUALS', 'NEQUALS'),
    ('nonassoc', 'LT', 'LTE', 'GT', 'GTE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'NOT', 'UMINUS')
)

# The rules by which a parser operates are usually specified by a formal grammar (productions in docstring).

# The first rule defined in the yacc specification determines the starting grammar symbol: script
def p_script(p):
    """script : statements"""
    p[0] = ASTNode("scriptNode", [p[1]])

def p_statements(p):
    # left-recursive rule
    """statements : statement
                  | statements statement"""
    if len(p) == 2: # base case
        p[0] = ASTNode("statementsNode", [p[1]])
    else:
        p[1].add_siblings([p[2]])
        p[0] = p[1]

def p_statement(p):
    """statement : declaration semis
                 | assignment semis
                 | forStatement semis
                 | whileStatement semis
                 | ifExpression semis
                 | functionCall semis
                 | println semis
                 | comment"""
    p[0] = p[1]

def p_declaration(p):
    """declaration : functionDeclaration
                   | variableDeclaration """
    p[0] = p[1]

def p_variableDeclaration(p):
    """variableDeclaration : VAL termID COLONS typeParameter ASSIGN expression
                           | VAR termID COLONS typeParameter ASSIGN expression
                           | VAL termID ASSIGN expression
                           | VAR termID ASSIGN expression """
    p[1] = ASTNode('declarationType', leaf=p[1])
    if len(p) == 7:
        p[0] = ASTNode('variableDeclarationNode', [p[1], p[2], p[4], p[6]], line=p.lineno(1))
    else:
        p[0] = ASTNode('variableDeclarationNode', [p[1], p[2], p[4]], line=p.lineno(1))

def p_assignment(p):
    """assignment : termID ASSIGN expression """
    p[0] = ASTNode('assignmentNode', [p[1], p[3]], line=p.lineno(1))

def p_functionDeclaration(p):
    """functionDeclaration : FUN termID LPAREN RPAREN block
                           | FUN termID LPAREN functionValueParameters RPAREN block
                           | FUN termID LPAREN RPAREN COLONS typeParameter block_return
                           | FUN termID LPAREN functionValueParameters RPAREN COLONS typeParameter block_return"""

    if len(p) == 6:
        name = 'mainNode' if p[2].leaf == 'main' else 'functionDeclarationNode' # is it a mainNode?
        p[0] = ASTNode(name, [p[2], p[5]], line=p.lineno(1))  # 2 children
    elif len(p) == 7:
        p[0] = ASTNode('functionDeclarationNode', [p[2], p[4], p[6]], line=p.lineno(1)) # 3 children
    elif len(p) == 8:
        p[0] = ASTNode('functionDeclarationNode', [p[2], p[6], p[7]], line=p.lineno(1)) # 3 children
    elif len(p) == 9:
        p[0] = ASTNode('functionDeclarationNode', [p[2], p[4], p[7], p[8]], line=p.lineno(1)) # 4 children

def p_block(p):
    """block : LBRACE statements RBRACE
             | LBRACE RBRACE"""
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = ASTNode('None')

def p_block_return(p):
    """block_return : LBRACE statements return RBRACE
                    | LBRACE return RBRACE"""
    if len(p) == 5:
        p[2].add_siblings([p[3]])
        p[0] = p[2]
    else:
        p[0] = p[2]

def p_typeParameter(p):
    """typeParameter : INT
                     | STRING
                     | BOOLEAN"""
    p[0] = ASTNode('typeParameterNode', leaf=p[1])

def p_expression(p):
    """expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression EQUALS expression
                  | expression NEQUALS expression
                  | expression LT expression
                  | expression LTE expression
                  | expression GT expression
                  | expression GTE expression
                  | expression AND expression
                  | expression OR expression
                  | NOT expression
                  | MINUS expression %prec UMINUS
                  | LPAREN expression RPAREN
                  | term"""
    if len(p) == 4:
        if p[1] != '(':
            p[0] = ASTNode(p[2], [p[1], p[3]], line=p.lineno(1))
        else:
            p[0] = p[2]
    elif len(p) == 3: # NOT, Unary MINUS
        p[0] = ASTNode(p[1], [p[2]], line=p.lineno(1))
    else:
        p[0] = p[1]

def p_ifExpression(p):
    """ifExpression : IF LPAREN expression RPAREN block
                    | IF LPAREN expression RPAREN block ELSE block"""
    if len(p) == 6:
        p[0] = ASTNode('if_expressionNode', [p[3], p[5]], line=p.lineno(1))
    else:
        p[0] = ASTNode('if_else_expressionNode', [p[3], p[5], p[7]], line=p.lineno(1))

def p_forStatement(p):
    """forStatement : FOR LPAREN termID IN expression RANGE expression RPAREN block
                    | FOR LPAREN termID IN expression DOWNTO expression RPAREN block
                    | FOR LPAREN termID IN expression RANGE expression STEP expression RPAREN block
                    | FOR LPAREN termID IN expression DOWNTO expression STEP expression RPAREN block"""

    p[6] = ASTNode('forType', leaf=p[6])
    if len(p) == 10:
        p[0] = ASTNode('forStatementNode', [p[3], p[5], p[6], p[7], p[9]], line=p.lineno(1))
    else:
        p[0] = ASTNode('forStatementNode', [p[3], p[5], p[6], p[7], p[9], p[11]], line=p.lineno(1))

def p_whileStatement(p):
    """whileStatement : WHILE LPAREN expression RPAREN block"""
    p[0] = ASTNode('whileStatementNode', [p[3], p[5]], line=p.lineno(1))

def p_functionValueParameters(p):
    # left-recursive rule
    """functionValueParameters : termID COLONS typeParameter
                               | functionValueParameters COMMA termID COLONS typeParameter"""
    if len(p) == 4: # base case
        p[0] = ASTNode('functionValueParametersNode', [p[1], p[3]], line=p.lineno(1))
    else:
        p[1].add_siblings([p[3], p[5]])
        p[0] = p[1]

def p_parameters(p):
    # left-recursive rule
    """parameters : expression
                  | parameters COMMA expression"""
    if len(p) == 2: # base case
        p[0] = ASTNode('parametersNode', [p[1]], line=p.lineno(1))
    else:
        p[1].add_siblings([p[3]])
        p[0] = p[1]

def p_functionCall(p):
    """functionCall : termID LPAREN parameters RPAREN
                    | termID LPAREN RPAREN
                    | READLINE LPAREN RPAREN"""
    if len(p) == 4:
        if p[1] == 'readLine':
            p[0] = ASTNode('readLineNode')
        else:
            p[0] = ASTNode('functionCallNode', children=[p[1]], line=p.lineno(1))
    else:
        p[0] = ASTNode('functionCallNode', children=[p[1], p[3]], line=p.lineno(1))

def p_term(p):
    """term : NUMBER
            | LITERAL
            | TRUE
            | FALSE
            | functionCall
            | termID"""
    if isinstance(p[1], ASTNode):
        p[0] = p[1]
    else:
        p[0] = ASTNode('termNode', leaf=p[1])

def p_println(p):
    """println : PRINTLN LPAREN expression RPAREN"""
    p[0] = ASTNode('printlnNode', [p[3]], line=p.lineno(1))

def p_return(p):
    """return : RETURN expression"""
    p[0] = ASTNode('returnNode', [p[2]], line=p.lineno(1))

def p_termID(p):
    """termID : ID"""
    p[0] = ASTNode('IDNode', leaf=p[1], line=p.lineno(1))

def p_semis(p): # for semicolons
    """ semis : SEMI
              | empty"""
    pass

def p_empty(p):
    """empty : """

def p_comment(p): # for comments
    """ comment : MLCOMM
                | SLCOMM
                """
    pass

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}' (line {p.lineno})")

        # Read ahead looking for a closing "}"
        while True:
            tok = parser.token()  # Get the next token
            if not tok or tok.type == 'RBRACE':
                break
        parser.restart() # discards the entire parsing stack and resets the parser to its initial state

    else:
        print("Syntax error at EOF")

# Build the parser:
parser = yacc.yacc(debug=True, write_tables=True)

