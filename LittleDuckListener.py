# Generated from LittleDuck.g4 by ANTLR 4.13.1
from antlr4 import *
from CuboSemantico import CuboSemantico
from Cuadruplo import Cuadruplo
from DiccionarioFuncsVars import DiccionarioFuncsVars

if "." in __name__:
    from .LittleDuckParser import LittleDuckParser
else:
    from LittleDuckParser import LittleDuckParser

# This class defines a complete listener for a parse tree produced by LittleDuckParser.
class LittleDuckListener(ParseTreeListener):
    def __init__(self):  # Constructor
        self.cuboSemantico = CuboSemantico()
        self.diccionarioFuncsVars = DiccionarioFuncsVars()
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

    # Funcion auxiliar para generar cuadruplos
    def generar_cuadruplo(self):
        if len(self.pilaOperandos) < 2 or not self.pilaOperadores:
            raise Exception("Error: faltan operandos o operadores para generar un cuadruplo")
        
        operador = self.pilaOperadores.pop()
        op2 = self.pilaOperandos.pop()
        op1 = self.pilaOperandos.pop()
        tipoIzq = self.pilaTipos.pop()
        tipoDer = self.pilaTipos.pop()

           # Revisión de tipos
        resultado_tipo = self.cuboSemantico.check_operation(operador, tipoIzq, tipoDer)
        if resultado_tipo is None:
            raise Exception(f"Error de tipos: {tipoIzq} {operador} {tipoDer} no es una operación válida.")

        resultado = self.generar_temporal()
        self.pilaOperandos.append(resultado)
        self.pilaTipos.append(resultado_tipo)

        # if operador in [">", "<", "==", "!=", ">=", "<="]:
        #     cuadruplo = Cuadruplo(operador, op2, op1, resultado)
        # else:
        cuadruplo = Cuadruplo(operador, op1, op2, resultado)
        self.listaCuadruplos.append(cuadruplo)

    # Funcion auxiliar para procesar expresiones y controlar orden de precedencia
    def procesar_operador(self, operador):
        precedence = {
                    '(': 4,
                    '*': 3, '/': 3,
                    '+': 2, '-': 2,
                    '>': 1, '<': 1, '!=': 1, '>=': 1, '<=': 1, '==': 1
                }

        while len(self.pilaOperadores) > 0 and (precedence[operador] <= precedence[self.pilaOperadores[-1]]):
            if(self.pilaOperadores[-1] == "("):
                break
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

        self.listaCuadruplos.append(Cuadruplo("=", result, "-", id_name))

    # Enter a parse tree produced by LittleDuckParser#condition.
    def enterCondition(self, ctx:LittleDuckParser.ConditionContext):
        self.insideIf = True # Set the flag to True when entering an 'if' statement

    # Exit a parse tree produced by LittleDuckParser#condition.
    def exitCondition(self, ctx:LittleDuckParser.ConditionContext):
        # Resolviendo cuadruplo GOTOF de condicional sin estatuto else
        if ctx.conditionElse().getText() == "":
            gotof_pos = self.pilaSaltos.pop()
            self.listaCuadruplos[gotof_pos].resultado = len(self.listaCuadruplos) +1     
        self.insideIf = False     
       
    # Enter a parse tree produced by LittleDuckParser#conditionElse.
    def enterConditionElse(self, ctx:LittleDuckParser.ConditionElseContext):
        # Generación de cuadruplos para estatuto else
        if(ctx.getText() != ""):
            # Resolviendo cuadruplo de IF principal
            gotof_pos = self.pilaSaltos.pop()
            self.listaCuadruplos[gotof_pos].resultado = len(self.listaCuadruplos)+2

            # Generando cuadruplo GOTO de estatuto ELSE
            gotof_quadruple = Cuadruplo("GOTO", "-", "-", "-")
            self.listaCuadruplos.append(gotof_quadruple)
            self.pilaSaltos.append(len(self.listaCuadruplos) - 1)  

    # Exit a parse tree produced by LittleDuckParser#conditionElse.
    def exitConditionElse(self, ctx:LittleDuckParser.ConditionElseContext):
        # Resolviendo cuadruplo GOTO de estatuto ELSE
        if ctx.getText() != "":
            goto_pos = self.pilaSaltos.pop()
            self.listaCuadruplos[goto_pos].resultado = len(self.listaCuadruplos) +1
        

    # Enter a parse tree produced by LittleDuckParser#cycle.
    def enterCycle(self, ctx:LittleDuckParser.CycleContext):
        self.pilaSaltos.append(len(self.listaCuadruplos))  # Generando salto pendiente para inicio de ciclo

    # Exit a parse tree produced by LittleDuckParser#cycle.
    def exitCycle(self, ctx:LittleDuckParser.CycleContext):
        # Resolviendo estatuto GOTOV con salto pendiente de inicio de ciclo
        etiqueta_inicio = self.pilaSaltos.pop()+1
        exp = self.pilaOperandos.pop()
        self.listaCuadruplos.append(Cuadruplo("GOTOV", exp, "-", etiqueta_inicio)) 

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
        self.listaCuadruplos.append(Cuadruplo("PRINT", "-", "-", self.pilaOperandos.pop()))

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
        # Manejo de ><, ==, etc
        if ctx.getChildCount() > 1:
            # Se extrae operador y se resuelve si hay otros con la misma precedencia
            operador = ctx.getChild(1).getText()
            self.pilaOperadores.append(operador) 
            self.procesar_operador(operador)
            result = self.pilaOperandos[-1]
            # self.pilaOperandos.append(result)

            # Generacion de cuadruplo GOTOF para condicional
            if self.insideIf:
                gotof_quadruple = Cuadruplo("GOTOF", result, "-", "-")
                self.listaCuadruplos.append(gotof_quadruple)
                self.pilaSaltos.append(len(self.listaCuadruplos) - 1)   

    # Enter a parse tree produced by LittleDuckParser#operador.
    def enterOperador(self, ctx:LittleDuckParser.OperadorContext):
        # Se agrega operador a lista de operadores
        operador = ctx.getText()
        #self.procesar_operador(operador)

    # Exit a parse tree produced by LittleDuckParser#operador.
    def exitOperador(self, ctx:LittleDuckParser.OperadorContext):
        pass

    # Enter a parse tree produced by LittleDuckParser#exp.
    def enterExp(self, ctx:LittleDuckParser.ExpContext):
        pass

    # Exit a parse tree produced by LittleDuckParser#exp.
    def exitExp(self, ctx:LittleDuckParser.ExpContext):
        # Manejo de + y -
        print("exp count", ctx.getChildCount())
        if ctx.getChildCount() != 1:
            # Se extrae operador y se resuelve si hay otros con la misma jerarquia
      
            for i in range(ctx.getChildCount() -1):
                child = ctx.getChild(i)
                print("counter final de exp", child.getChildCount())
                if child.getText() in ["+", "-"]:
                    self.procesar_operador(child.getText())
                    self.pilaOperadores.append(child.getText()) 
                elif child.getChildCount() <= 2  and child.getText()[0] != "(":
                    if(i == ctx.getChildCount()-1):
                        self.pilaOperandos.append(child.getText())
                        self.flag = False

            self.generar_cuadruplo()
            # for child in ctx.getChildren():
            #     print("counter final de exp", child.getChildCount())
            #     if child.getText() in ["+", "-"]:
            #         self.procesar_operador(child.getText())
            #         self.pilaOperadores.append(child.getText()) 
            #     elif child.getChildCount() <= 2  and child.getText()[0] != "(":
            #         self.pilaOperandos.append(child.getText())
            #         self.flag = False
            #         print(child.getText())

            # self.generar_cuadruplo()


    # Enter a parse tree produced by LittleDuckParser#termino.
    def enterTermino(self, ctx:LittleDuckParser.TerminoContext):
        pass

    # Exit a parse tree produced by LittleDuckParser#termino.
    def exitTermino(self, ctx:LittleDuckParser.TerminoContext):

        # Manejo de * y /
        if ctx.getChildCount() > 1:
            # Se extrae operador y se resuelve si hay otros con la misma jerarquia
            for i in range(ctx.getChildCount()-1):
                child = ctx.getChild(i)
                if child.getText() in ["*", "/"]:
                    self.procesar_operador(child.getText())
                    self.pilaOperadores.append(child.getText()) 
                elif child.getChildCount() <= 2 and child.getText()[0] != "(":
                    if(i == ctx.getChildCount()-1):
                        self.pilaOperandos.append(child.getText())
                        self.flag = False
            self.generar_cuadruplo()

            # for child in ctx.getChildren():
            #     if child.getText() in ["*", "/"]:
            #         self.procesar_operador(child.getText())
            #         self.pilaOperadores.append(child.getText()) 
            #     elif child.getChildCount() <= 2 and child.getText()[0] != "(":
            #         self.pilaOperandos.append(child.getText())
            # self.generar_cuadruplo()

           

    # Enter a parse tree produced by LittleDuckParser#factor.
    def enterFactor(self, ctx:LittleDuckParser.FactorContext):
        # Manejode ID, CTE o expresión entre parentesis
        if ctx.getChildCount() > 1 and ctx.getChild(0).getText() == '(':  
            self.pilaOperadores.append('(')  
        operando = ctx.getText()
        print("pre operando -> ", operando, " - ", self.flag)
        if operando[0] != "(" and self.flag:
            self.flag = True
            self.pilaOperandos.append(operando)
        
       
        print(self.pilaOperandos)


    # Exit a parse tree produced by LittleDuckParser#factor.
    def exitFactor(self, ctx:LittleDuckParser.FactorContext):
        pass

    # Enter a parse tree produced by LittleDuckParser#id_or_cte.
    def enterId_or_cte(self, ctx:LittleDuckParser.Id_or_cteContext):
        pass

    # Exit a parse tree produced by LittleDuckParser#id_or_cte.
    def exitId_or_cte(self, ctx:LittleDuckParser.Id_or_cteContext):
        if ctx.ID():
            # Obtener tipo de variable desde el diccionario
            current_child_index = ctx.children.index(ctx.ID()) 
            id_name = ctx.ID().getText()
            variable_type = self.diccionarioFuncsVars.lookup_variable(id_name, self.currentFunction).get("type")
            self.pilaTipos.append(variable_type)
        elif ctx.cte():
            current_child_index = ctx.children.index(ctx.cte()) 
            if ctx.cte().CTE_INT():
                self.pilaTipos.append("int")
            else:
                self.pilaTipos.append("float")
        pass

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