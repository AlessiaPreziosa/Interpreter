# An interpreter is a program that interprets the AST of the source program on the fly (without compiling it first).

from Lexer import *
from Parser import *
from SymbolTable import *

class Interpreter:

    # Initialize Symbol Table
    def __init__(self):
        self.s = None

    # Create a new scope by defining a new Symbol Table
    def create_scope(self, parent, name):
        self.s = SymbolTable(parent, name)

    # Exit from the current scope by returning to its parent's Symbol Table
    def exit_scope(self):
        self.s = self.s.parent

    def evaluate(self, node):
        if node is None:
            return None

        # Script Node
        elif node.value == 'scriptNode':

            lista = node.children[0].children

            # Without a main, code can't run: it checks that there is one and only one main() function
            if sum(1 for child in lista if child.value == 'mainNode') != 1:
                raise Exception("One main function is requested! Can't run code")

            # Public functions and variables are accessible everywhere:
            # to handle this kind of situation, a (fake) call to fun main() is added
            lista.append(ASTNode('mainCallNode', children = [ASTNode('IDNode', leaf='main')]))

            # As soon as the scriptNode is encountered, the first scope is created:
            # it has no parent since it's the root
            self.create_scope(None, 'Root') # Root
            value = self.evaluate(node.children[0]) #statementsNode

            return value

        # Statements Node
        elif node.value == 'statementsNode':

            # each statement is singularly evaluated
            result = None
            for child in node.children:
                result = self.evaluate(child)
            return result

        # Variable Declaration Node
        elif node.value == 'variableDeclarationNode':

            var_name = node.children[1].leaf  # Variable name
            var_value = self.evaluate(node.children[-1]) # Value

            if len(node.children) == 4:

                var_type = node.children[2].leaf # typeParameterNode
                if (var_type == 'Int' and isinstance(var_value, int)) \
                        or (var_type == 'String' and isinstance(var_value, str)) \
                        or (var_type == 'Boolean' and isinstance(var_value, bool)):

                    self.s.declare_variable(node.children[0].leaf, var_name, var_value, var_type, node.line)

                else:
                    raise TypeError(f"Wrong variable type, line {node.line}: "
                                    f"expected {var_type}, got {getType(var_value)}")

            else:
                var_type = getType(var_value)
                self.s.declare_variable(node.children[0].leaf, var_name, var_value, var_type, node.line)

            return var_value

        # Assignment Node
        elif node.value == 'assignmentNode':

            if not self.s.check_father():
                raise Exception(f"Excepting a top level declaration, line {node.line} ")

            var_name = node.children[0].leaf # Variable name
            var_value = self.evaluate(node.children[1]) # Value

            # 'val' variables cannot be reassigned (for the current scope and for those of parent's)
            if not self.s.is_variableVar_declared(var_name):
                raise ValueError(f"Variables not declared or declared with 'val' like "
                                f"'{var_name}' cannot be assigned, line {node.line}")

            declared_type = self.s.get_variableType(var_name) # Type

            # Check whether the type of the to-be assigned value matches the declared type of the variable
            if getType(var_value) != declared_type:
                raise TypeError(f"Cannot assign value of type {getType(var_value)} to variable {var_name} of type {declared_type}," 
                                f" line {node.line}")

            # Perform variable assignment with the new value
            self.s.assign_variable(var_name, var_value)

            return var_value

        # If_expression Node and If_else_expression Node
        elif node.value in ('if_expressionNode', 'if_else_expressionNode'):

            if not self.s.check_father():
                raise Exception(f"Excepting a top level declaration, line {node.line}")

            condition = self.evaluate(node.children[0])
            if not isinstance(condition, bool):
                raise TypeError(f"The condition in an 'if' expression must be boolean, got {getType(condition)} instead"
                                f", line {node.line}!")

            value = None

            # 'if' block
            if condition:
                # create a new scope ONLY IF I enter the 'if' block
                parent = self.s
                self.create_scope(parent, 'if')
                value = self.evaluate(node.children[1]) # IF body
                self.exit_scope() # exit the IF scope

            # 'else' block
            elif node.value == 'if_else_expressionNode':
                # create a new scope ONLY IF I enter the 'else' block
                parent = self.s
                self.create_scope(parent, 'else')
                value = self.evaluate(node.children[2]) # ELSE body
                self.exit_scope() # exit the ELSE scope

            return value

        # While Statement Node
        elif node.value == 'whileStatementNode':

            if not self.s.check_father():
                raise Exception(f"Excepting a top level declaration, line {node.line}")

            condition = self.evaluate(node.children[0])
            if not isinstance(condition, bool):
                raise TypeError(f"The condition in a 'while' statement must be a boolean, "
                                f"got {getType(condition)} instead; line {node.line}")

            # maximum iterations number is set to prevent an infinite loop
            max_iterations = 1000
            iteration_count = 0
            value = None

            while condition:

                # create a new scope each time I enter the 'while' block
                parent = self.s
                self.create_scope(parent, 'while')

                value = self.evaluate(node.children[1]) # while body

                iteration_count += 1
                if iteration_count > max_iterations:
                    raise RuntimeError("Maximum iteration limit exceeded in 'while' loop. "
                                       f"Possible infinite loop detected, line {node.line}")

                self.exit_scope()
                condition = self.evaluate(node.children[0]) # update condition

            return value

        # For Statement Node
        elif node.value == 'forStatementNode':

            if not self.s.check_father():
                raise Exception(f"Excepting a top level declaration, line {node.line}")

            identifier = node.children[0].leaf # ID
            start = self.evaluate(node.children[1]) # start of range
            order = node.children[2].leaf
            end = self.evaluate(node.children[3]) # end of range

            if len(node.children) == 6:
                step = self.evaluate(node.children[4])
                if step < 0:
                    raise ValueError(f"Step must be positive: got {str(step)}, line {node.line}")
            else:
                step = 1

            if step == 0:
                raise ValueError(f"Step must be different from '0', line {node.line}")

            if not isinstance(start, int) or not isinstance(end, int) or not isinstance(step, int):
                raise TypeError(f"All range values must be Integer, "
                                f"got Start: {getType(start)}, End: {getType(end)}, Step: {getType(step)}"
                                f", line {node.line}")

            max_iterations = 1000
            iteration_count = 0
            value = None

            if start > end:
                if order == 'downTo':
                    step = -step
                    end -= 1
            elif start < end:
                if order == '..':
                    end += 1
                else:
                    step = -step
            else:
                end += 1

            for i in range(start, end, step):

                # create a new scope each time I enter the 'for' block for variables' range
                parent = self.s
                self.create_scope(parent, 'variables')

                # Identifier variable is set to start value (and each time the cycle is entered it's updated)
                self.s.declare_variable('val', identifier, i, 'Integer', node.line)

                # create a new scope each time I enter the 'for' block
                parent = self.s
                self.create_scope(parent, 'for')

                value = self.evaluate(node.children[-1])

                iteration_count += 1
                if iteration_count > max_iterations:
                    raise RuntimeError("Maximum iteration limit exceeded in 'for' loop. "
                                       f"Possible infinite loop detected, line {node.line}")

                self.exit_scope() # exit for scope
                self.exit_scope() # exit variables' range scope

            return value

        elif node.value in ('+', '-', '*', '/'):

            if len(node.children) == 1: # Unary MINUS
                operand = self.evaluate(node.children[0])
                if not isinstance(operand, int):
                    raise TypeError(f"Operand must be 'Integer', line {node.line}")
                return -operand

            left = self.evaluate(node.children[0])
            right = self.evaluate(node.children[1])

            op = node.value
            if op == '+':

                if isinstance(left, int) and isinstance(right, int):
                    return left + right

                if isinstance(left, str):
                    return left + str(right) # String Concatenation

                raise Exception(f"Operation is not supported, line {node.line}")

            # Check both operands are Integer
            if not isinstance(left, int) or not isinstance(right, int):
                raise TypeError(f"Both operands must be 'Integer', "
                                f"got {getType(left)} and {getType(right)}"
                                f", line {node.line}")

            # Perform the arithmetic operation

            elif op == '-':
                return left - right
            elif op == '*':
                return left * right
            elif op == '/':
                # Handling division by zero
                if right == 0:
                    raise ZeroDivisionError(f"Division by zero is not allowed, line {node.line}")
                return int(left / right)

        elif node.value in ('==', '!=', '<', '<=', '>', '>='):
            left = self.evaluate(node.children[0])
            right = self.evaluate(node.children[1])

            if not (getType(left) == getType(right)):
                raise TypeError(f"Cannot compare different types of operands ({getType(left)}, {getType(right)}),"
                                f" line {node.line}")

            op = node.value

            if op == '==':
                return left == right
            elif op == '!=':
                return left != right
            if op == '<':
                return left < right
            elif op == '<=':
                return left <= right
            elif op == '>':
                return left > right
            elif op == '>=':
                return left >= right

        elif node.value in ('&&', '||', '!'):

            if node.value == '!': # Unary Logic Operation
                operand = self.evaluate(node.children[0])
                if not isinstance(operand, bool):
                    raise TypeError(f"Cannot evaluate operand {getType(operand)} in a NOT statement, "
                                    f"must be Boolean, line {node.line}")
                return not operand

            left = self.evaluate(node.children[0])
            right = self.evaluate(node.children[1])

            # Check both operands are boolean
            if not isinstance(left, bool) or not isinstance(right, bool):
                raise TypeError(f"Both operands must be Boolean: got {getType(left)} and {getType(right)}, line {node.line}")

            op = node.value
            if op == '&&':
                return left and right
            elif op == '||':
                return left or right

        elif node.value == 'termNode':
            return node.leaf # it's just a value

        elif node.value == 'IDNode':

            var_name = node.leaf
            if not self.s.is_variable_declared(var_name):
                raise ValueError(f"Variable '{var_name}' not declared, line {node.line}")

            return self.s.get_variable(var_name)

        # Readline Node
        elif node.value == 'readLineNode':

            if not self.s.check_father():
                raise Exception(f"Excepting a top level declaration, line {node.line}")

            result = input()
            return result

        # Print Node
        elif node.value == 'printlnNode':

            if not self.s.check_father():
                raise Exception(f"Excepting a top level declaration, line {node.line}")

            value = self.evaluate(node.children[0])
            print(value)

            return value

        # Function Declaration Node
        elif node.value in ('functionDeclarationNode', 'mainNode'):

            name = node.children[0].leaf # Function Name

            if node.children[1].value == 'functionValueParametersNode':
                parameters = self.evaluate(node.children[1]) # functionValueParametersNode
            else:
                parameters = ()

            if len(node.children) == 3 and node.children[1].value == 'typeParameterNode':
                returnType = node.children[1].leaf # typeParameterNode
            elif len(node.children) == 4:
                returnType = node.children[2].leaf # typeParameterNode
            else:
                returnType = None

            if node.children[-2].value == 'typeParameterNode':
                if node.children[-1].value == 'statementsNode':
                    block = node.children[-1].children.copy()
                    block.pop()
                    returnValue = node.children[-1].children[-1].children[0] # returnNode
                else:
                    block = []
                    returnValue = node.children[-1].children[0] # returnNode
            else:
                block = node.children[-1].children
                returnValue = None

            # Function declaration in SymbolTable
            self.s.declare_function(name, parameters, block, returnType, returnValue, self.s, node.line)

            return None

        # Function Value Parameters Node
        elif node.value == 'functionValueParametersNode':

            names = [node.children[i].leaf for i in range(0, len(node.children), 2)]

            if len(names) > len(set(names)):
                raise Exception(f"Parameters names must be unique, line {node.line}")

            # parameters are of this kind: (('x', 'Int'), ('y', 'String'), ...)
            parameters = tuple([(node.children[i].leaf, node.children[i+1].leaf) for i in range(0, len(node.children), 2)])

            return parameters

        # Function Call Node
        elif node.value in ('functionCallNode', 'mainCallNode'):

            name = node.children[0].leaf

            if node.value != 'mainCallNode':
                if not self.s.check_father():
                    raise Exception(f"Excepting a top level declaration, line {node.line}")

            if len(node.children) > 1:
                arguments = self.evaluate(node.children[1])  # parametersNode
            else:
                arguments = ()

            if not self.s.is_function_declared(name, arguments):
                raise Exception(f"Function '{name}' not declared, line {node.line}")

            F = self.s.get_function(name, arguments)
            function = F[0]
            parameters = F[1]

            body = function['body']
            returnType = function['returnType']
            returnValue = function['returnValue']

            to_return = self.s

            if node.value != 'mainCallNode':
                scope = function['scope']
                # Create a new scope for variables' function
                self.create_scope(scope, 'variables')

                # Associating arguments with formal parameters
                for param, arg in zip(parameters, arguments):
                    param_name, param_type = param
                    arg_value, _ = arg

                    self.s.declare_variable('val', param_name, arg_value, param_type, node.line)

            # Create a new scope
            parent = self.s
            self.create_scope(parent, 'function')

            try:
                # We execute the body of the function
                result = None
                for stmt in body:
                    result = self.evaluate(stmt)

                returnValue = self.evaluate(returnValue)

                # Check the return type
                if returnType and getType(returnValue) != returnType:
                        raise TypeError(f"Function '{name}' is expected to return a {returnType},"
                                        f" but returned a {getType(result)}, line {node.line}")

                return returnValue

            finally:
                # Exit the function scope and the variables' scope
                self.s = to_return

        # Parameters Node
        elif node.value == 'parametersNode':
            arguments = []

            # Extract parameters' type
            for arg in node.children:

                # Passed arguments: variables are evaluated at the moment the function is called
                # types of arguments are also evaluated to check the matching with the function declaration

                arg = self.evaluate(arg) # expression is solved

                arguments.append((arg, getType(arg))) # type of argument

            return tuple(arguments)
