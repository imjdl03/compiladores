# Jorge Eduardo de León Reyna - A00829759

# Este codigo corresponde a la llamada del lexer y parser generado por el archivo LittleDuck.g4 para
# analizar los textos que le demos como entrada para despues identificar si contiene errores o no.

from antlr4 import * # type: ignore
from LittleDuckLexer import LittleDuckLexer
from LittleDuckParser import LittleDuckParser
from LittleDuckListener import LittleDuckListener
from Memory import Memory
import pickle
from VirtualMachine import VirtualMachine


# Obteniendo contenido de archivos de pruebas
test_case = "tests_cuadruplos/test4.txt"
with open(test_case, 'r') as file:
    file_content = file.read()

# Analisis lexico
lexer = LittleDuckLexer(InputStream(file_content))
stream = CommonTokenStream(lexer)

# Analisis de sintaxis
parser = LittleDuckParser(stream)

try:
    # Generacion de parser
    tree = parser.programa()
    #print("Arbol de analisis de sintaxis => ", tree.toStringTree(recog=parser))

    # Aplicacion de listener y acciones semanticas
    listener = LittleDuckListener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree) 

    variables_dict = listener.diccionarioFuncsVars.variables
    funcs_dict = listener.diccionarioFuncsVars.functions

    for index, cuadruplo in enumerate(listener.listaCuadruplos):
        print(index+1, ".- ", cuadruplo.operador, cuadruplo.operandoIzq, cuadruplo.operandoDer, cuadruplo.resultado)
     
    print("Memory -> ", listener.memory.get_data_by_segment())

    # guardando cuadruplos y contenido de memoria en archivo .obj
    data = {
        "quads": listener.listaCuadruplos,
        "memory": listener.memory.data,
    }
    with open("test_file.obj", "wb") as f:
        pickle.dump(data, f)

    vm = VirtualMachine()
    vm.run()

except Exception as e:
    print(f"Error: {e}")