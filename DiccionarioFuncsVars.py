# Diccionario para almacenar funciones y variables

class DiccionarioFuncsVars:
    def __init__(self):
        self.variables = {} # Variables globales
        self.functions = {} # Funciones y variables locales 

    # Metodo para guardar variable global en array de variables
    def insert_variable(self, name, type, scope=None):
        self.variables[name] = {"type": type, "scope": scope}

    # Metodo para insertar variable local en una funcion
    def insert_function_variable(self, functionName, varName, varType):
        # Verificacion de variable en funcion no declarada
        if functionName not in self.functions:
            raise Exception(f"Function '{functionName}' not found")

        # Verificacion de variables locales ya declaradas
        if varName in self.functions[functionName].get("local_vars", {}):
            raise Exception(f"Error: Variable '{varName}' already declared in function '{functionName}'")

        # Verificacion de variable global ya declarada
        if varName in self.variables:
            raise Exception(f"Error: Variable '{varName}' already declared globaly")
        
        self.functions[functionName]["local_vars"][varName] = {"type": varType}

    # Funcion para insertar funcion en array de funcuiones
    def insert_function(self, name, funcType, parameters):
        # Verificacion de funcion ya declarada
        if name in self.functions:
            raise Exception(f"Error: Function '{name}' already declared")

        # Verificacion de repeticion de parametros
        param_names = [param["name"] for param in parameters]
        if len(param_names) != len(set(param_names)):
            raise Exception(f"Error: Duplicate parameter names in function '{name}'")

        self.functions[name] = {"type": funcType, "parameters": parameters, "local_vars": {}}

    # Metodo para buscar si una funcion ya fue declarada
    def lookup_function(self, name):
        return self.functions.get(name)
    
    def lookup_variable(self, var_name, current_function=None):
        """Busca una variable en el diccionario, primero en el ámbito local (función actual) 
        y luego en el ámbito global."""

        # Buscar en el ámbito local (función)
        if current_function:
            function_vars = self.functions.get(current_function, {}).get("vars", {})
            variable_info = function_vars.get(var_name)
            if variable_info:
                return variable_info

        # Buscar en el ámbito global
        variable_info = self.variables.get(var_name)
        if variable_info:
            return variable_info

        # Si no se encuentra, lanzar una excepción
        raise Exception(f"Error: Variable '{var_name}' no declarada.")