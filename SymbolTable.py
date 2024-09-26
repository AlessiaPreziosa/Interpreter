# Symbol table for storing variables and functions

class SymbolTable:
    def __init__(self, parent, name):
        self.variables = {}
        self.functions = {}
        self.parent = parent
        self.name = name

    def declare_variable(self, v, name, value, var_type, line):

        """
        Declare a new variable
        :param line: Line number
        :param var_type: Type of variable
        :param value: Value of the variable
        :param name: Name of the variable
        :param v: Declaration can be var or val (val variables cannot be reassigned)

        It raises an Exception if the variable has already been declared in the same scope
        """

        if name in self.variables:
            raise Exception(f"Variable '{name}' already declared, line {line}")
        self.variables[name] = {'declaration': v, 'type': var_type, 'value': value}

    def assign_variable(self, name, value):

        """
        Assign a value to an existing variable
        :param name: Name of the variable
        :param value: New value of the variable
        """

        if name in self.variables:
            self.variables[name]['value'] = value
        elif self.parent:
            self.parent.assign_variable(name, value)

    def is_variable_declared(self, name):

        """
        Check if a variable is declared in this or any parent scope
        :param name: Name of the variable
        :return: True if the variable is declared
        """

        if name in self.variables:
            return True
        elif self.parent:
            return self.parent.is_variable_declared(name)
        else:
            return False

    def is_variableVar_declared(self, name):

        """
        Check if a variable is declared in this or any parent scope with 'var'
        :param name: Name of the variable
        :return: True if the variable is declared with 'var'
        """

        if name in self.variables and self.variables[name]['declaration'] == 'var':
            return True
        elif self.parent:
            return self.parent.is_variableVar_declared(name)
        else:
            return False

    def get_variable(self, name):

        """
        Retrieves a variable having the passed Name
        :param name: Name of the variable to be retrieved
        """

        if name in self.variables:
            return self.variables[name]['value']
        elif self.parent:
            return self.parent.get_variable(name)

    def get_variableType(self, name):

        """
        Retrieves type of a variable having the passed Name
        :param name: Name of the variable to be retrieved
        """

        if name in self.variables:
            return self.variables[name]['type']
        elif self.parent:
            return self.parent.get_variableType(name)

    def check_father(self):

        """Check if the node is child of a functionDeclarationNode (or mainNode)."""

        if self.name == 'function':
            return True
        elif self.parent:
            return self.parent.check_father()
        else:
            return False

    def declare_function(self, name, parametersF, body, returnType, returnValue, scope, line):

        """
        Declare a new function.
        :param scope: Scope of the function
        :param name: Name of the function
        :param parametersF: parameters of the function
        :param body: block
        :param returnType: type of return value of the function
        :param returnValue: return value of the function
        :param line: line number

        It raises an Exception if the function has already been declared in the same scope
        """

        names = [list(self.functions.keys())[i][0] for i in range(len(self.functions.keys()))] # functions' names of the current scope
        if name in names:
            check = self.check_parameters(name, parametersF)[0]
            if check:
                raise Exception(f"Function '{name}' already declared, line {line}")

        self.functions[(name, parametersF)] = {'body': body, 'returnType': returnType, 'returnValue': returnValue,
                                               'scope': scope}

    def get_function(self, name, arguments):

        """
        Retrieves a function.
        :param name: Name of the function
        :param arguments: arguments passed to the function
        """
        names = [list(self.functions.keys())[i][0] for i in range(len(self.functions.keys()))]
        if name in names:
            check = self.check_parameters(name, arguments)
            if check[0]:
                return self.functions[(name, check[1])], check[1]
            elif self.parent:
                return self.parent.get_function(name, arguments)
        elif self.parent:
            return self.parent.get_function(name, arguments)

    def is_function_declared(self, name, arguments):
        """Check if a function is declared in this or any parent scope."""
        names = [list(self.functions.keys())[i][0] for i in range(len(self.functions.keys()))]
        if name in names:
            check = self.check_parameters(name, arguments)
            if check[0]:
                return True
            elif self.parent:
                return self.parent.is_function_declared(name, arguments)
        elif self.parent:
            return self.parent.is_function_declared(name, arguments)
        return False

    def check_parameters(self, fname, arguments):

        """
        Checks if parameters' types are matched with a declared function and returns them if found.
        :param fname: Function name
        :param arguments: Function arguments
        :return: True if found, found parameters
        """

        for (name, parameters), info in self.functions.items():
            if fname == name:
                types = [parameters[i][1] for i in range(len(parameters))]

                if len(types) == len(arguments):
                    check_list = [types[i] == arguments[i][1] for i in range(len(types))]
                    if all(check_list):
                        return True, parameters
        return False, ()

# typeParameter
def getType(term):
    if str(type(term)) == "<class 'str'>":
        return "String"
    if str(type(term)) == "<class 'int'>":
        return "Int"
    if str(type(term)) == "<class 'bool'>":
        return "Boolean"
    if str(type(term)) == "<class 'NoneType'>":
        return "None"