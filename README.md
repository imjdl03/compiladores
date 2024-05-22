# AVANCE 1. PARSER & SCANNER

**JORGE EDUARDO DE LEON REYNA - A00829759**

## DESCRIPCION DE ARCHIVOS

### DESCRIPCION GENERAL

Esta herramienta se compone por dos scripts. En el primero (LittleDuck.g4) se definen las reglas de parseo y lexico. El segundo (main.py) se encarga de tomar el parser y lexer generado por el primer script para analizar los textos que le demos como input.

### DESCRIPCION LittleDuck.g4

Este codigo corresponde a la definicion de las reglas del scanner y del parser de la gramatica definida. La primer sección del codigo "LEXER RULES" contiene la definicion de las expresiones regulares principales definias acorde a los tokens identificados a partir del lenguage Little Duck. La segunda seccion "PARSING RULES" contiene las reglas de produccion definidas acorde al lenguage Little Duck.

### DESCRIPCION main.py

Este codigo corresponde a la llamada del lexer y parser generado por el archivo LittleDuck.g4 para analizar los textos que le demos como entrada para despues identificar si contiene errores o no.

### DESCRIPCION DE ARCHIVOS AUXILIARES

Los archovs extras se generan como resultado de compilar las reglas de parseo y lexico del archivo LittleDuck.g4. Estos archivos son usados para analizar los textos que se den como entrada.

## PASOS PARA CORRERLO

1. Instalar Antlr Tool desde la pagina: https://www.antlr.org/download.html
2. Instalar Antlr Runtime para Python con el comando: pip install antlr4-python3-runtime
3. Compilar reglas de parsing y lexer con el comando: antlr -Dlanguage=Python3 LittleDuck.g4
4. Correr script de python que analiza strings con el comando: python3 main.py
