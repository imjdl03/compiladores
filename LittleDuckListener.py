# Generated from LittleDuck.g4 by ANTLR 4.13.1
from antlr4 import * # type: ignore
from CuboSemantico import CuboSemantico
from Cuadruplo import Cuadruplo
from DiccionarioFuncsVars import DiccionarioFuncsVars
from Memory import Memory

if "." in __name__:
    from .LittleDuckParser import LittleDuckParser
else:
    from LittleDuckParser import LittleDuckParser

# This class defines a complete listener for a parse tree produced by LittleDuckParser.
class LittleDuckListener(ParseTreeListener):
    def __init__(self):  # Constructor
        self.cuboSemantico = CuboSemantico()
        self.diccionarioFuncsVars = DiccionarioFuncsVars()
        self.memory = Memory()
        self.currentFunction = None
        self.listaCuadruplos = []  
        self.pilaOperadores = []  
        self.pilaOperandos = []  
        self.pilaTipos = [] 
        self.pilaSaltos = []
        self.insideIf = False 
        self.contador = 0
        self.flag = True

    # Funcion auxiliar para controlar la generación de variables "temporales"
    def generar_temporal(self):
        temporal = f"t{self.contador}"
        self.contador += 1
        return temporal

    # Funcion auxiliar para obtener el codigo de operacion de cada operador
    def get_operator_code(self, operator):
        operator_codes = {
        "+": 1,
        "-": 2,
        "*": 3,
        "/": 4,
        "=": 5,  
        "<": 6,
        ">": 7,
        "<=": 8,
        ">=": 9,
        "==": 10,
        "!=": 11,
        "GOTO": 12,
        "GOTOF": 13,
        "GOTOV": 14,
        "PRINT": 15,
        }
        return operator_codes.get(operator, None)

    # Funcion auxiliar para generar cuadruplos
    def generar_cuadruplo(self):
        if len(self.pilaOperandos) < 2 or not self.pilaOperadores:
            raise Exception("Error: faltan operandos o operadores para generar un cuadruplo")

        # Extrayendo operandos y operadores para generar cuadruplo
        operador = self.pilaOperadores.pop()
        op2 = self.pilaOperandos.pop()
        op1 = self.pilaOperandos.pop()
        tipoIzq = self.pilaTipos.pop()
        tipoDer = self.pilaTipos.pop()

        # Revisión de tipos
        resultado_tipo = self.cuboSemantico.check_operation(operador, tipoIzq, tipoDer)
        if resultado_tipo is None:
            raise Exception(f"Error de tipos: {tipoIzq} {operador} {tipoDer} no es una operación válida.")

        # Generación de temporales
        resultado = self.generar_temporal()
        temp_address = self.memory.store(-1, resultado_tipo, "temp")

        # Guardar direccion de variables temporales
        self.diccionarioFuncsVars.update_variable_address(resultado, temp_address, "temp")

        # Guardamos variable temporal en pilas correspondientes
        self.pilaOperandos.append(temp_address)  
        self.pilaTipos.append(resultado_tipo)

        # Generacion de cuadruplo
        operator = self.get_operator_code(operador)
        cuadruplo = Cuadruplo(operator, op1, op2, temp_address)
        self.listaCuadruplos.append(cuadruplo)
        

    # Funcion auxiliar para procesar expresiones y controlar orden de precedencia
    def procesar_operador(self, operador):
        precedence = {
                    '(': 4,
                    '*': 3, '/': 3,
                    '+': 2, '-': 2,
                    '>': 1, '<': 1, '!=': 1, '>=': 1, '<=': 1, '==': 1
                }

        if self.pilaOperadores and (precedence[operador] <= precedence[self.pilaOperadores[-1]]):
            if self.pilaOperadores[-1] == "(":
                self.pilaOperadores.pop()
            else:
                self.generar_cuadruplo()

            
            

    # Enter a parse tree produced by LittleDuckParser#programa.
    def enterPrograma(self, ctx:LittleDuckParser.ProgramaContext):
        pass

    # Exit a parse tree produced by LittleDuckParser#programa.
    def exitPrograma(self, ctx:LittleDuckParser.ProgramaContext):
        pass


    # Enter a parse tree produced by LittleDuckParser#type.
    def enterType(self, ctx:LittleDuckParser.TypeContext):
        pass

    # Exit a parse tree produced by LittleDuckParser#type.
    def exitType(self, ctx:LittleDuckParser.TypeContext):
        pass


    # Enter a parse tree produced by LittleDuckParser#vars.
    def enterVars(self, ctx:LittleDuckParser.VarsContext):
        pass

    # Exit a parse tree produced by LittleDuckParser#vars.
    def exitVars(self, ctx:LittleDuckParser.VarsContext):
        pass


    # Enter a parse tree produced by LittleDuckParser#var_list.
    def enterVar_list(self, ctx:LittleDuckParser.Var_listContext):
        pass

    # Exit a parse tree produced by LittleDuckParser#var_list.
    def exitVar_list(self, ctx:LittleDuckParser.Var_listContext):
        pass


    # Enter a parse tree produced by LittleDuckParser#var_declaration.
    def enterVar_declaration(self, ctx:LittleDuckParser.Var_declarationContext):
        # Buscamos por palabras clave de tipo de dato
        for child in ctx.getChildren():
            if(child.getText() in ["int", "float"]):
                varType = child.getText() # Cuando llegamos a tipo de dato lo guardamos

        # Funcion para procesar lista de variables
        def process_id_list_vars(id_list_ctx):
            if id_list_ctx.ID():
                varName = id_list_ctx.ID().getText() #Obtenemos ID de variable

                # Guardamos variable en diccionario de variables
                if self.currentFunction is not None:
                    self.diccionarioFuncsVars.insert_function_variable(self.currentFunction, varName, varType)
                else:
                    self.diccionarioFuncsVars.insert_variable(varName, varType, scope="global")

                # Guardando variable vacia en memoria
                initial_value = -1  # You might need to get this from elsewhere
                address = self.memory.store(initial_value, varType, "global")
                self.diccionarioFuncsVars.update_variable_address(varName, address, scope="global")


            # Llamamos recursivamente la funcion para iterar los otros posibles nodos con IDs de variables
            if id_list_ctx.id_list_vars():
                process_id_list_vars(id_list_ctx.id_list_vars())
                
        process_id_list_vars(ctx.id_list_vars())

    # Exit a parse tree produced by LittleDuckParser#var_declaration.
    def exitVar_declaration(self, ctx:LittleDuckParser.Var_declarationContext):
        pass


    # Enter a parse tree produced by LittleDuckParser#id_list_vars.
    def enterId_list_vars(self, ctx:LittleDuckParser.Id_list_varsContext):
        pass

    # Exit a parse tree produced by LittleDuckParser#id_list_vars.
    def exitId_list_vars(self, ctx:LittleDuckParser.Id_list_varsContext):
        pass


    # Enter a parse tree produced by LittleDuckParser#funcs.
    def enterFuncs(self, ctx:LittleDuckParser.FuncsContext):
        if(ctx.ID() != None ): # Verificamos si no estamos en un nodo vacio
            funcName = ctx.ID().getText() # Obtenemos nombre de funcion
            funcType = "void" # Definimos el tipo de la funcion (siempre es void)
            funcParameters = [] # Inicializamos array de parametros

            def process_id_list_funcs(id_list_ctx):
                if id_list_ctx.ID(): #
                    paramType = None
                    paramName = id_list_ctx.ID().getText() # Obtenemos IDs de parametros
                    for child in id_list_ctx.getChildren(): # iteramos por los nodos hijos buscando por tipos de datos
                        if child.getText() in ['int', 'float']:
                            paramType = child.getText() # Guardamos tipo de dato
                    
                    funcParameters.append({"name": paramName, "type": paramType}) # Guardamos en array de parametros
                    
                    if id_list_ctx.id_list_funcs(): # Llamamos recursivamente buscando mas nodos por explorar en el sub-arbol de parametros
                        process_id_list_funcs(id_list_ctx.id_list_funcs())

            if ctx.id_list_funcs():
                process_id_list_funcs(ctx.id_list_funcs())

            self.diccionarioFuncsVars.insert_function(funcName, funcType, funcParameters) # Guardamos funcion en el diccionario
            self.currentFunction = funcName # Guardamos la funcion en la que nos encontramos actualmente


    # Exit a parse tree produced by LittleDuckParser#funcs.
    def exitFuncs(self, ctx:LittleDuckParser.FuncsContext):
        pass


    # Enter a parse tree produced by LittleDuckParser#id_list_funcs.
    def enterId_list_funcs(self, ctx:LittleDuckParser.Id_list_funcsContext):
        pass

    # Exit a parse tree produced by LittleDuckParser#id_list_funcs.
    def exitId_list_funcs(self, ctx:LittleDuckParser.Id_list_funcsContext):
        pass


    # Enter a parse tree produced by LittleDuckParser#assign.
    def enterAssign(self, ctx:LittleDuckParser.AssignContext):
        pass
    # Exit a parse tree produced by LittleDuckParser#assign.
    def exitAssign(self, ctx:LittleDuckParser.AssignContext):
        # Generacion cuadruplo de estatuto de asignación
        id_name = ctx.ID().getText()
        result = self.pilaOperandos.pop()

        right_type = self.pilaTipos.pop()
        left_type = self.diccionarioFuncsVars.lookup_variable(id_name, self.currentFunction).get("type")

        # Revisión de compatibilidad de tipos en asignacion
        if not self.cuboSemantico.check_assignment(left_type, right_type):
            raise Exception(f"Error de tipos: No se puede asignar '{right_type}' a '{left_type}'")
        
        variable_info = self.diccionarioFuncsVars.lookup_variable(id_name, self.currentFunction)
        if variable_info:
            address = variable_info.get("address")

            # Actualizando direccion de memoria de variable
            self.memory.update_value(result, address=address)  # Use the existing address

        # Generando cuadruplo
        operator = self.get_operator_code("=")
        self.listaCuadruplos.append(Cuadruplo(operator, result, None, address))


    # Enter a parse tree produced by LittleDuckParser#condition.
    def enterCondition(self, ctx:LittleDuckParser.ConditionContext):
        self.insideIf = True # Set the flag to True when entering an 'if' statement

    # Exit a parse tree produced by LittleDuckParser#condition.
    def exitCondition(self, ctx:LittleDuckParser.ConditionContext):
        # Resolviendo cuadruplo GOTOF de condicional sin estatuto else
        gotof_pos = self.pilaSaltos.pop()
        self.listaCuadruplos[gotof_pos].resultado = len(self.listaCuadruplos) +1
        self.insideIf = False     


    # Enter a parse tree produced by LittleDuckParser#conditionElse.
    def enterConditionElse(self, ctx:LittleDuckParser.ConditionElseContext):
        # Generación de cuadruplos para estatuto else
        if ctx.getText() != "":
            # Generando cuadruplo GOTO de estatuto ELSE
            operator = self.get_operator_code("GOTO")
            gotof_quadruple = Cuadruplo(operator, None, None, None)
            self.listaCuadruplos.append(gotof_quadruple)

            # Sacnado pos de cuad pendiente de IF
            gotof_pos = self.pilaSaltos.pop()

            # Agregamos salto pendiente de goto
            self.pilaSaltos.append(len(self.listaCuadruplos) - 1)  

            # Resolvemos gotof de if            
            self.listaCuadruplos[gotof_pos].resultado = len(self.listaCuadruplos)+1


    # Exit a parse tree produced by LittleDuckParser#conditionElse.
    def exitConditionElse(self, ctx:LittleDuckParser.ConditionElseContext):
        pass


    # Enter a parse tree produced by LittleDuckParser#cycle.
    def enterCycle(self, ctx:LittleDuckParser.CycleContext):
        self.pilaSaltos.append(len(self.listaCuadruplos))  # Generando salto pendiente para inicio de ciclo

    # Exit a parse tree produced by LittleDuckParser#cycle.
    def exitCycle(self, ctx:LittleDuckParser.CycleContext):
        # Resolviendo estatuto GOTOV con salto pendiente de inicio de ciclo
        etiqueta_inicio = self.pilaSaltos.pop()+1
        exp = self.pilaOperandos.pop()
        operator = self.get_operator_code("GOTOV")
        self.listaCuadruplos.append(Cuadruplo(operator, exp, None, etiqueta_inicio)) 


    # Enter a parse tree produced by LittleDuckParser#body.
    def enterBody(self, ctx:LittleDuckParser.BodyContext):
        pass

    # Exit a parse tree produced by LittleDuckParser#body.
    def exitBody(self, ctx:LittleDuckParser.BodyContext):
        pass


    # Enter a parse tree produced by LittleDuckParser#statementList.
    def enterStatementList(self, ctx:LittleDuckParser.StatementListContext):
        pass

    # Exit a parse tree produced by LittleDuckParser#statementList.
    def exitStatementList(self, ctx:LittleDuckParser.StatementListContext):
        pass


    # Enter a parse tree produced by LittleDuckParser#statement.
    def enterStatement(self, ctx:LittleDuckParser.StatementContext):
        pass

    # Exit a parse tree produced by LittleDuckParser#statement.
    def exitStatement(self, ctx:LittleDuckParser.StatementContext):
        pass


    # Enter a parse tree produced by LittleDuckParser#fCall.
    def enterFCall(self, ctx:LittleDuckParser.FCallContext):
        # Verificacion de funcion no declarada
        func_name = ctx.ID().getText()
        if not self.diccionarioFuncsVars.lookup_function(func_name):
            raise Exception(f"Error: Function '{func_name}' not declared")


    # Exit a parse tree produced by LittleDuckParser#fCall.
    def exitFCall(self, ctx:LittleDuckParser.FCallContext):
        pass


    # Enter a parse tree produced by LittleDuckParser#expressionList.
    def enterExpressionList(self, ctx:LittleDuckParser.ExpressionListContext):
        pass

    # Exit a parse tree produced by LittleDuckParser#expressionList.
    def exitExpressionList(self, ctx:LittleDuckParser.ExpressionListContext):
        pass


    # Enter a parse tree produced by LittleDuckParser#expressionList_.
    def enterExpressionList_(self, ctx:LittleDuckParser.ExpressionList_Context):
        pass

    # Exit a parse tree produced by LittleDuckParser#expressionList_.
    def exitExpressionList_(self, ctx:LittleDuckParser.ExpressionList_Context):
        pass


    # Enter a parse tree produced by LittleDuckParser#print.
    def enterPrint(self, ctx:LittleDuckParser.PrintContext):
        pass

    # Exit a parse tree produced by LittleDuckParser#print.
    def exitPrint(self, ctx:LittleDuckParser.PrintContext):
        pass


    # Enter a parse tree produced by LittleDuckParser#printList.
    def enterPrintList(self, ctx:LittleDuckParser.PrintListContext):
        pass

    # Exit a parse tree produced by LittleDuckParser#printList.
    def exitPrintList(self, ctx:LittleDuckParser.PrintListContext):
        # Se verifica si el objeto a imprimir no es una constante
        if ctx.CTE_STRING() == None:
            print_result =  self.pilaOperandos.pop()
            operator = self.get_operator_code("PRINT")
            self.listaCuadruplos.append(Cuadruplo(operator, None, None, print_result))
        else: # Si es una constante lo añade a la memoria y genera el cuadruplo correspondiente
            constante = ctx.CTE_STRING().getText()
            address = self.memory.store(constante, "string", "constant")
            operator = self.get_operator_code("PRINT")
            self.listaCuadruplos.append(Cuadruplo(operator, None, None,address))

    # Enter a parse tree produced by LittleDuckParser#printList_tail.
    def enterPrintList_tail(self, ctx:LittleDuckParser.PrintList_tailContext):
        pass

    # Exit a parse tree produced by LittleDuckParser#printList_tail.
    def exitPrintList_tail(self, ctx:LittleDuckParser.PrintList_tailContext):
        pass


    # Enter a parse tree produced by LittleDuckParser#expression.
    def enterExpression(self, ctx:LittleDuckParser.ExpressionContext):
        pass

    # Exit a parse tree produced by LittleDuckParser#expression.
    def exitExpression(self, ctx:LittleDuckParser.ExpressionContext):
        # Verifica si hay al menos dos operandos y un operador para generar cuadruplo al salir de una expresion
        if(len(self.pilaOperandos) > 1 and len(self.pilaOperadores) > 0):
            self.generar_cuadruplo()
        result = self.pilaOperandos[-1]
        
        # Genera gotof para if
        if self.insideIf:
            operator = self.get_operator_code("GOTOF")
            gotof_quadruple = Cuadruplo(operator, result, None, None)
            self.listaCuadruplos.append(gotof_quadruple)
            self.pilaSaltos.append(len(self.listaCuadruplos) - 1)   
            self.insideIf = False


    # Enter a parse tree produced by LittleDuckParser#operador.
    def enterOperador(self, ctx:LittleDuckParser.OperadorContext):
        # Se agrega operador a lista de operadores
        operador = ctx.getText()
        self.procesar_operador(operador)
        self.pilaOperadores.append(operador) 

    # Exit a parse tree produced by LittleDuckParser#operador.
    def exitOperador(self, ctx:LittleDuckParser.OperadorContext):
        pass

    # Enter a parse tree produced by LittleDuckParser#exp.
    def enterExp(self, ctx:LittleDuckParser.ExpContext):
        pass

    # Exit a parse tree produced by LittleDuckParser#exp.
    def exitExp(self, ctx:LittleDuckParser.ExpContext):
        # Verifica si hay operandos pendientes de resolver al salir de exp (suma)
        if len(self.pilaOperadores) > 1 and len(self.pilaOperandos) > 2:
            self.generar_cuadruplo()
    
    # Enter a parse tree produced by LittleDuckParser#operador_exp.
    def enterOperador_exp(self, ctx:LittleDuckParser.Operador_expContext):
        pass

    # Exit a parse tree produced by LittleDuckParser#operador_exp.
    def exitOperador_exp(self, ctx:LittleDuckParser.Operador_expContext):
        # Agrega operador de suma o resta a pila
        self.procesar_operador(ctx.getText())
        self.pilaOperadores.append(ctx.getText()) 


    # Enter a parse tree produced by LittleDuckParser#termino.
    def enterTermino(self, ctx:LittleDuckParser.TerminoContext):
        pass

    # Exit a parse tree produced by LittleDuckParser#termino.
    def exitTermino(self, ctx:LittleDuckParser.TerminoContext):
        pass



    # Enter a parse tree produced by LittleDuckParser#operador_termino.
    def enterOperador_termino(self, ctx:LittleDuckParser.Operador_terminoContext):
        pass

    # Exit a parse tree produced by LittleDuckParser#operador_termino.
    def exitOperador_termino(self, ctx:LittleDuckParser.Operador_terminoContext):
        # Agrega operador de multi o div a pila
        self.procesar_operador(ctx.getText())
        self.pilaOperadores.append(ctx.getText()) 

    # Enter a parse tree produced by LittleDuckParser#factor.
    def enterFactor(self, ctx:LittleDuckParser.FactorContext):
        # Revisa si hay operacion con parentesis
        operando = ctx.getText()
        if operando[0] == '(':  
            self.pilaOperadores.append('(')  # Si lo hay, añade parentesis a lista de operadores

        if operando[0] != "(" and operando[0] != ")":
            # Verifica si el operando es una variable o una constante
            if ctx.id_or_cte().ID():
                # Verifica si la variable ha sido declarada y la guarda en memoria y en pila operandos
                id_name = operando
                variable_info = self.diccionarioFuncsVars.lookup_variable(id_name, self.currentFunction)
                
                if variable_info:
                    address = variable_info.get("address") 
                    self.pilaOperandos.append(address)
                else:
                    raise Exception(f"Error: Variable '{id_name}' not declared")
            else:  
                # Guardando contante en memoria y en pila operandos
                if ctx.id_or_cte().cte().CTE_INT() != None:
                    data_type = "int"
                else:
                    data_type = "float"

                address = self.memory.store(operando, data_type, "constant")
                self.pilaOperandos.append(address)



    # Exit a parse tree produced by LittleDuckParser#factor.
    def exitFactor(self, ctx:LittleDuckParser.FactorContext):
        pass

    # Enter a parse tree produced by LittleDuckParser#id_or_cte.
    def enterId_or_cte(self, ctx:LittleDuckParser.Id_or_cteContext):
        pass

    # Exit a parse tree produced by LittleDuckParser#id_or_cte.
    def exitId_or_cte(self, ctx:LittleDuckParser.Id_or_cteContext):
        # Guardamos tipo de dato en pila de datos
        if ctx.ID():
            # Obtener tipo de variable desde el diccionario
            id_name = ctx.ID().getText()
            variable_type = self.diccionarioFuncsVars.lookup_variable(id_name, self.currentFunction).get("type")
            self.pilaTipos.append(variable_type)
        elif ctx.cte():
            if ctx.cte().CTE_INT():
                self.pilaTipos.append("int")
            elif ctx.cte().CTE_FLOAT():
                self.pilaTipos.append("float")
            else:
                self.pilaTipos.append("string")
        


    # Enter a parse tree produced by LittleDuckParser#cte.
    def enterCte(self, ctx:LittleDuckParser.CteContext):
        pass

    # Exit a parse tree produced by LittleDuckParser#cte.
    def exitCte(self, ctx:LittleDuckParser.CteContext):
        pass


    # Enter a parse tree produced by LittleDuckParser#suma_resta.
    def enterSuma_resta(self, ctx:LittleDuckParser.Suma_restaContext):
        pass

    # Exit a parse tree produced by LittleDuckParser#suma_resta.
    def exitSuma_resta(self, ctx:LittleDuckParser.Suma_restaContext):
        pass



del LittleDuckParser