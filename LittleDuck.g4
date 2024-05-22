// Jorge Eduardo de León Reyna - A00829759

// Este codigo corresponde a la definicion de las reglas del scanner y del parser de la gramatica
// definida. La primer sección del codigo "LEXER RULES" contiene la definicion de las expresiones
// regulares principales definias acorde a los tokens identificados a partir del lenguage Little
// Duck. La segunda seccion "PARSING RULES" contiene las reglas de produccion definidas acorde al
// lenguage Little Duck.

grammar LittleDuck;

// LEXER RULES ----------------------------------------------------------------------------
ID       : [a-zA-Z][a-zA-Z0-9]*;

fragment Digits: [0-9]+ ;  
fragment FloatWithDecimal   : (Digits '.' Digits{1,10})?; 
fragment FloatWithoutDecimal: ('.' Digits{1,10});

CTE_INT : [0-9]+ ;
CTE_FLOAT : (FloatWithDecimal | FloatWithoutDecimal);
CTE_STRING : ('\'' .*? '\'' | '"' .*? '"') ; 
WS       : [ \r\t\n]+ -> skip; 


// -------------------------------------PARSER RULES -----------------------------------------

// PROGRAMA ----------------------------------------------------------------------------------
programa : 'program' ID ';' vars funcs 'main' body 'end'; 

// TYPE --------------------------------------------------------------------------------------
type : 'int' | 'float';   

// VARS --------------------------------------------------------------------------------------
vars     : 'var' var_list | ;  
var_list : var_declaration ';' var_list | ;
var_declaration: id_list_vars ':' type ; 
id_list_vars  : ID id_list_vars | ',' ID id_list_vars | ;  

// FUNCS -------------------------------------------------------------------------------------
funcs: 'void' ID '(' id_list_funcs ')' '[' vars body ']' ';' funcs  
     | ; 

id_list_funcs : ID ':' type id_list_funcs 
        | ',' ID ':' type id_list_funcs
        | ; 

// ASSIGN ------------------------------------------------------------------------------------
assign : ID '=' expression ';' ; 

// CONDITION ---------------------------------------------------------------------------------
condition : 'if' '(' expression ')' body conditionElse ';';
conditionElse : 'else' body
              | ;

// CICLYE ------------------------------------------------------------------------------------
cycle : 'do' body 'while' '(' expression ')' ';' ;

// BODY --------------------------------------------------------------------------------------
body : '{' statementList '}' ;

statementList : statement statementList 
              |
              ; 

statement : assign 
          | condition 
          | cycle 
          | fCall
          | print 
          ;


// F_CALL --------------------------------------------------------------------------------------
fCall : ID '(' expressionList ')' ';';
expressionList : expression expressionList_ ;
expressionList_ : ',' expression expressionList_
                    | ;

// PRINT ---------------------------------------------------------------------------------------
print : 'print' '(' printList ')' ';' ;
printList : expression printList_tail
          | CTE_STRING printList_tail 
          ; 
printList_tail : ',' expression printList_tail 
               | ;

// EXPRESSION ----------------------------------------------------------------------------------
expression : exp (operador exp)? ;  // Opcional: operador y otro exp

// OPERADOR -----------------------------------------------------------------------------------
operador   : '>' | '<' | '!=' | '>=' ;  // Sin recursión 

// EXP -----------------------------------------------------------------------------------------
exp : termino (('+' | '-') termino)* ; // Recursión a la derecha con operadores + y -

// TERMINO --------------------------------------------------------------------------------------
termino : factor (('*' | '/') factor)* ; // Recursión a la derecha con * y /

// FACTOR ---------------------------------------------------------------------------------------
factor : '(' expression ')'
       | suma_resta id_or_cte
       | id_or_cte;

// ID_OR_CTE & CTE (Sin cambios) ----------------------------------------------------------------
id_or_cte : ID | cte ; 
cte : CTE_INT | CTE_FLOAT ;

suma_resta : '+' | '-' | ; 

// // ID_OR_CONSTANTE & CTE -------------------------------------------------------------------------

