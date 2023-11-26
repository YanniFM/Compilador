# Importaciones necesarias para el programa
import sys  # Importa el módulo sys para interactuar con el intérprete de Python
from genericpath import isfile  # Importa la función isfile para verificar la existencia de archivos
import CuboSemantico
import Lexer
import ply.yacc as yacc
from GestionMemorias import *
from Cuadruplo import Cuadruplo
from MaquinaVirtual import *

# Define los tokens a utilizar en el análisis sintáctico, obtenidos del analizador léxico
tokens = Lexer.tokens

# Definir la precedencia y asociatividad de operadores para el análisis sintáctico
precedence = (
    ("left", "AND", "OR"),
    ("nonassoc", "LTHAN", "GTHAN", "EQUALS", "DIFFERENCE", "LEQUAL", "GEQUAL"),
    ("left", "PLUS", "MINUS"),
    ("left", "TIMES", "DIVIDE", "MOD"),
)

EMPTY = {"id": " "}

idFuncionActual = "" 
programID = ""
tipoDatoActual = "" 
contadorParametros = 0 
directorioFunciones = {} 
tablaConstantes = {} 
cubo = CuboSemantico.CuboSemantico().cubo
CuadruploList = []
pilaOperadores = [] 
contadorResultados = 0
pilaSalto = [] 

# Inicializar las memorias
MemoriaG = MemoriaGlobal()
MemoriaL = MemoriaLocal()
MemoriaC = MemoriaConst()
MemoriaT = MemoriaTemporal()

# Crear y agregar cuádruplo que indica el final del programa
def p_program(p):
    "program : PROGRAM ID init SEMICOLON vars programp main"
    newCuadruplo = Cuadruplo("DONE", EMPTY, EMPTY, " ")
    CuadruploList.append(newCuadruplo)

# Establecer el ID del programa y añadir cuádruplo inicial
def p_init(p):
    "init :"
    global programID, idFuncionActual
    programID = p[-1]
    idFuncionActual = programID
    directorioFunciones[programID] = {"type": "void", "vars": {}}
    newCuadruplo = Cuadruplo("GOTO", EMPTY, EMPTY, EMPTY)
    CuadruploList.append(newCuadruplo)
    pilaSalto.append(0)

# Definición vacía para posible lista de funciones
def p_programp(p):
    """programp : function programp
    | empty"""

# Definición para declaraciones de variables
def p_vars(p):
    """vars : VARS varsp
    | empty"""

# Procesamiento de listas de variables de un tipo
def p_varsp(p):
    """varsp : type varspp SEMICOLON varsp
    | empty"""

# Lista de variables separadas por comas
def p_varspp(p):
    """varspp : varsppp
    | varsppp COMMA varspp"""

# Asignación de un identificador a una variable
def p_varsppp(p):
    "varsppp : ID varspppp"

# Definición para arreglos o variable simple
def p_varspppp(p):
    """varspppp : LBRACKET CTE_I RBRACKET
    | empty"""
    varID = p[-1]
    arrSize = 0
    if len(p) == 4:
        arrSize = p[2]
    checkVarOverlap(varID, arrSize)

# Definición de una función y generación de cuádruplo para el final de función
def p_function(p):
    """function : FUNCTION functionp ID idFuncionActual parameters vars statements
    | empty"""
    global contadorParametros
    newCuadruplo = Cuadruplo("ENDFUNC", EMPTY, EMPTY, p[3])
    CuadruploList.append(newCuadruplo)
    directorioFunciones[idFuncionActual]["reqresultados"] = MemoriaT.clear()
    directorioFunciones[idFuncionActual]["reqVars"] = MemoriaL.clear()

# Definición del tipo de retorno de una función
def p_functionp(p):
    """functionp : type
    | VOID"""
    global tipoDatoActual
    if p[1] == "void":
        tipoDatoActual = p[1]

# Establecer el identificador de la función actual
def p_funcID(p):
    "idFuncionActual :"
    global idFuncionActual
    idFuncionActual = p[-1]
    checkFuncOverlap()

# Definición de los parámetros de una función
def p_parameters(p):
    "parameters : LPAREN parametersp RPAREN"
    global contadorParametros, tipoDatoActual
    directorioFunciones[idFuncionActual]["params"] = contadorParametros

    while contadorParametros > 0:
        resultado = pilaOperadores.pop(-contadorParametros)
        tipoDatoActual = resultado[1]
        checkVarOverlap(resultado[0], resultado[2])
        contadorParametros = contadorParametros - 1

# Lista de parámetros para una función
def p_parametersp(p):
    """parametersp : type ID parameterArray parameterspp
    | empty"""
    if len(p) == 4:
        global contadorParametros
        pilaOperadores.append([p[2], p[1]])
        contadorParametros += 1

# Definición de un parámetro como arreglo o variable simple
def p_parameterArray(p):
    """parameterArray : LBRACKET CTE_I RBRACKET
    | empty"""
    global contadorParametros
    if len(p) == 4:
        var = [p[-1], p[-2], p[2]]
    else:
        var = [p[-1], p[-2], 0]
    pilaOperadores.append(var)
    contadorParametros += 1

# Procesamiento de parámetros adicionales en funciones, separados por comas
def p_parameterspp(p):
    """parameterspp : COMMA parametersp
    | empty"""

# Definición de la función principal 'main'
def p_main(p):
    "main : MAIN mainID LPAREN RPAREN statements"

# Establecer el identificador de la función principal y completar cuádruplo de salto
def p_mainID(p):
    "mainID :"
    global idFuncionActual
    idFuncionActual = programID
    CuadruploList[pilaSalto.pop()].fill(len(CuadruploList))

# Bloque de declaraciones o instrucciones
def p_statements(p):
    "statements : LBRACE statementsp RBRACE"

# Procesamiento de múltiples declaraciones o instrucciones
def p_statementsp(p):
    """statementsp : statementspp SEMICOLON statementsp
    | statementsppp statementsp
    | empty"""

# Diferentes tipos de declaraciones, incluyendo asignación, llamada a funciones, retorno, lectura y escritura
def p_statementspp(p):
    """statementspp : assignment
    | voidCall
    | return
    | read
    | write"""

# Llamada a funciones sin retorno o funciones especiales
def p_voidCall(p):
    """voidCall : call
    | specCall"""
    if p[1] in directorioFunciones:
        if directorioFunciones[p[1]].get("type") != "void":
            print(f"Return from function is not being saved")
            sys.exit()
    elif p[1] != "reg" and p[1] != "plot":
        print(f"Return from function is not being saved")
        sys.exit()

# Declaraciones para estructuras de control, como condicionales y bucles
def p_statementsppp(p):
    """statementsppp : condition
    | loop"""

# Procesamiento de una asignación
def p_assignment(p):
    "assignment : variable EQUAL assignmentp"
    assignment()

# Asignar una expresión o el resultado de una llamada a función
def p_assignmentp(p):
    """assignmentp : expression
    | funcCall"""

# Llamada a funciones con retorno
def p_funcCall(p):
    """funcCall : call
    | specCall"""
    if p[1] in directorioFunciones:
        if directorioFunciones[p[1]].get("type") == "void":
            print(f"Cannot assign from void function")
            sys.exit()
    elif p[1] == "reg" or p[1] == "plot":
        print(f"Cannot assign from void function")
        sys.exit()

# Procesamiento de una llamada a función
def p_call(p):
    "call : ID initParams LPAREN callp RPAREN"
    global contadorParametros, contadorResultados
    id = p[1]
    p[0] = p[1]
    tipoDatoActual, dir, params = findFunc(id)
    if params != contadorParametros:
        print(f"Wrong number of parameters in call to {id}")
        sys.exit()
     # Generar cuádruplos para la ejecución de la función
    newCuadruplo = Cuadruplo("ERA", EMPTY, EMPTY, id)
    CuadruploList.append(newCuadruplo)

    keys = list(directorioFunciones[id]["vars"])
    while contadorParametros > 0:
        parameter = pilaOperadores.pop(-contadorParametros)
        key = keys[params - contadorParametros]
        if parameter.get("type") == directorioFunciones[id]["vars"][key].get(
            "type"
        ) and parameter.get("arrSize") == directorioFunciones[id]["vars"][key].get("arrSize"):
            newCuadruplo = Cuadruplo("PARAM", parameter, EMPTY, params - contadorParametros)

            CuadruploList.append(newCuadruplo)
            contadorParametros -= 1
        else:
            print(
                f"Parameter types or arrSize in line {p.lineno(1)!r} do not match call to {id}"
            )
            sys.exit()

    newCuadruplo = Cuadruplo("GOSUB", EMPTY, EMPTY, dir)
    CuadruploList.append(newCuadruplo)
    # Manejar el valor de retorno si la función no es 'void'
    if tipoDatoActual != "void":
        genresultado(tipoDatoActual)
        resultado = pilaOperadores[-1]
        aux = directorioFunciones[programID]["vars"][id]
        pilaOperadores.append(
            {"id": id, "type": aux.get("type"), "dir": aux.get("dir"), "arrSize": 0}
        )
        assignment()
        pilaOperadores.append(resultado)

# Procesamiento de llamadas a funciones especiales como 'int', 'float', etc.
def p_specCall(p):
    "specCall : specCallp initParams LPAREN callp RPAREN"
    global contadorParametros, contadorResultados
    id = p[1]
    p[0] = p[1]
    # Crear y añadir cuádruplo para iniciar la llamada a la función especial
    newCuadruplo = Cuadruplo("ERA", EMPTY, EMPTY, id)
    CuadruploList.append(newCuadruplo)
    # Procesamiento específico según el tipo de función especial
    if id == "int":
        # Verificar número correcto de parámetros para 'int' y sus tipos
        if contadorParametros != 1:
            print(f"Wrong number of parameters in call to int")
            sys.exit()

        parameter = pilaOperadores.pop()
        if parameter.get("type") != "float" or parameter.get("arrSize") != 0:
            print(
                f"Parameter types or arrSize in line {p.lineno!r} do not match call to {id}"
            )
            sys.exit()
        newCuadruplo = Cuadruplo("PARAM", parameter, EMPTY, 0)
        CuadruploList.append(newCuadruplo)

        genresultado("int")

    elif id == "float":
        # Verificar número correcto de parámetros para 'float' y sus tipos
        if contadorParametros != 1:
            print(f"Wrong number of parameters in call to int")
            sys.exit()

        parameter = pilaOperadores.pop()
        if parameter.get("type") != "int" or parameter.get("arrSize") != 0:
            print(
                f"Parameter types or arrSize in line {p.lineno!r} do not match call to {id}"
            )
            sys.exit()
        newCuadruplo = Cuadruplo("PARAM", parameter, EMPTY, 0)
        CuadruploList.append(newCuadruplo)

        genresultado("float")

    elif id == "pow":
        # Verificar número correcto de parámetros para 'pow' y sus tipos
        if contadorParametros != 2:
            print(f"Wrong number of parameters in call to int")
            sys.exit()

        for i in range(2):
            parameter = pilaOperadores.pop(-2 + i)
            if (
                parameter.get("type") == "float"
                or parameter.get("type") == "int"
                and parameter.get("arrSize") == 0
            ):
                newCuadruplo = Cuadruplo("PARAM", parameter, EMPTY, i)
                CuadruploList.append(newCuadruplo)

            else:
                print(
                    f"Parameter types or arrSize in line {p.lineno(1)!r} do not match call to {id}"
                )
                sys.exit()

        genresultado("float")

    elif id == "rand":
        # Verificar número correcto de parámetros para 'rand'
        if contadorParametros != 0:
            print(f"Wrong number of parameters in call to {id}")
            sys.exit()

        genresultado("float")

    elif id == "plot" or id == "reg":
        # Verificar número correcto de parámetros para 'plot' o 'reg'
        if contadorParametros != 1:
            print(f"Wrong number of parameters in call to {id}")
            sys.exit()

        parameter = pilaOperadores.pop()
        if (
            parameter.get("type") == "float"
            or parameter.get("type") == "int"
            and parameter.get("arrSize") > 1
        ):
            newCuadruplo = Cuadruplo("PARAM", parameter, EMPTY, 0)
            CuadruploList.append(newCuadruplo)

        else:
            print(
                f"Parameter types or arrSize in line {p.lineno(1)!r} do not match call to {id}"
            )
            sys.exit()

    else:
        # Verificar número correcto de parámetros para otras funciones especiales
        if contadorParametros != 1:
            print(f"Wrong number of parameters in call to {id}")
            sys.exit()

        parameter = pilaOperadores.pop()
        if (
            parameter.get("type") != "int"
            or parameter.get("type") != "float"
            and parameter.get("arrSize") > 1
        ):
            newCuadruplo = Cuadruplo("PARAM", parameter, EMPTY, 0)
            CuadruploList.append(newCuadruplo)
        else:
            print(f"Parameter types or arrSize do not match call to {id}")
            sys.exit()

        genresultado("float")
    # Crear y añadir cuádruplo para ejecutar la subrutina de la función especial
    newCuadruplo = Cuadruplo("GOSUB", EMPTY, EMPTY, "spec")
    CuadruploList.append(newCuadruplo)

# Captura el identificador de la función especial a llamar
def p_specCallp(p):
    """specCallp : INT
    | FLOAT
    | POW
    | RAND
    | MED
    | MODA
    | VAR
    | REG
    | PLOT"""
    p[0] = p[1]

# Procesa una expresión en una llamada a función y maneja parámetros adicionales
def p_callp(p):
    """callp : expression callpp
    | empty"""
    global contadorParametros
    if len(p) == 3:
        contadorParametros += 1

# Maneja múltiples parámetros en llamadas a funciones, separados por comas
def p_callpp(p):
    """callpp : COMMA callp
    | empty"""

# Procesa la instrucción 'return' en funciones
def p_return(p):
    "return : RETURN LPAREN expression RPAREN"
    aux = pilaOperadores.pop()

    if programID == idFuncionActual:
        print(f"Cannot have return on function main")
        sys.exit()

    elif aux.get("type") == directorioFunciones[idFuncionActual].get("type"):
        newCuadruplo = Cuadruplo("RETURN", EMPTY, EMPTY, aux.get("dir"))
        CuadruploList.append(newCuadruplo)

    else:
        print(f"Type mismatch on return for function {idFuncionActual}")
        sys.exit()


# Genera cuádruplos para leer entradas del usuario
def p_read(p):
    "read : READ initParams LPAREN readp RPAREN"
    global pilaOperadores, contadorParametros
    while contadorParametros > 0:
        resultado = pilaOperadores.pop(-contadorParametros)
        newCuadruplo = Cuadruplo("READ", EMPTY, EMPTY, resultado.get("dir"))
        CuadruploList.append(newCuadruplo)
        contadorParametros = contadorParametros - 1


# Contabiliza los parámetros en la instrucción 'read'
def p_readp(p):
    "readp : variable readpp"
    global contadorParametros
    contadorParametros = contadorParametros + 1

# Maneja múltiples variables para leer, separadas por comas
def p_readpp(p):
    """readpp : COMMA readp
    | empty"""


# Crea cuádruplos para imprimir todo en la llamada en la misma línea y luego imprimir un salto de línea
def p_write(p):
    "write : WRITE initParams LPAREN writep RPAREN"
    global pilaOperadores, contadorParametros
    while contadorParametros > 0:
        resultado = pilaOperadores.pop(-contadorParametros)
        arrSize = resultado.get("arrSize")
        # Procesa y formatea arreglos para imprimir
        if arrSize > 1:
            checkConstOverlap({"type": "string", "id": "[ "})
            newCuadruplo = Cuadruplo("PRINT", EMPTY, EMPTY, pilaOperadores.pop().get("dir"))
            CuadruploList.append(newCuadruplo)
            for i in range(arrSize):
                newCuadruplo = Cuadruplo("PRINT", EMPTY, EMPTY, resultado.get("dir") + i)
                CuadruploList.append(newCuadruplo)
                checkConstOverlap({"type": "string", "id": " "})
                newCuadruplo = Cuadruplo("PRINT", EMPTY, EMPTY, pilaOperadores.pop().get("dir"))
                CuadruploList.append(newCuadruplo)
            checkConstOverlap({"type": "string", "id": "]"})
            newCuadruplo = Cuadruplo("PRINT", EMPTY, EMPTY, pilaOperadores.pop().get("dir"))
            CuadruploList.append(newCuadruplo)
        else:
            newCuadruplo = Cuadruplo("PRINT", EMPTY, EMPTY, resultado.get("dir"))
            CuadruploList.append(newCuadruplo)
        contadorParametros = contadorParametros - 1
    # Cuádruplo para imprimir salto de línea al final
    checkConstOverlap({"type": "string", "id": "\n"})
    newCuadruplo = Cuadruplo("PRINT", EMPTY, EMPTY, pilaOperadores.pop().get("dir"))
    CuadruploList.append(newCuadruplo)


# Inicializa el contador de parámetros
def p_initParams(p):
    "initParams :"
    global contadorParametros
    contadorParametros = 0


# Cuenta la cantidad de parámetros en 'write'
def p_writep(p):
    """writep : expression writepp
    | CTE_S string writepp"""
    global contadorParametros
    contadorParametros = contadorParametros + 1

# Maneja parámetros adicionales para imprimir, separados por comas
def p_writepp(p):
    """writepp : COMMA writep
    | empty"""

# Procesa la estructura condicional 'if-then-else'
def p_condition(p):
    "condition : IF LPAREN expression c1 THEN statements conditionp c3"

# Procesa la parte 'else' de la estructura condicional
def p_conditionp(p):
    """conditionp : c2 ELSE statements
    | empty"""


# Comprueba si la expresión es de tipo booleano y añade un salto a la pila
def p_c1(p):
    "c1 : RPAREN"
    pilaSalto.append(len(CuadruploList))
    aux = pilaOperadores.pop()
    if aux.get("type") == "bool":
        newCuadruplo = Cuadruplo("GOTOF", aux, EMPTY, EMPTY)
        CuadruploList.append(newCuadruplo)
    else:
        print(f"expression in line {p.lineno(1)!r} needs to result in boolean type")
        sys.exit()


# Genera un cuádruplo para saltar al final del 'else' y llena el salto desde la pila
def p_c2(p):
    "c2 :"
    CuadruploList[pilaSalto.pop()].fill(len(CuadruploList) + 1)
    newCuadruplo = Cuadruplo("GOTO", EMPTY, EMPTY, EMPTY)

    pilaSalto.append(len(CuadruploList))
    CuadruploList.append(newCuadruplo)


# Llena el salto desde la pila
def p_c3(p):
    "c3 :"
    CuadruploList[pilaSalto.pop()].fill(len(CuadruploList))

# Define bucles 'while' y 'for'
def p_loop(p):
    """loop : while
    | for"""

# Define la estructura del bucle 'while'
def p_while(p):
    "while : WHILE w1 LPAREN expression w2 DO statements w3"


# Añade un salto a la pila para el bucle 'while'
def p_w1(p):
    "w1 :"
    pilaSalto.append(len(CuadruploList))


# Comprueba si la expresión del 'while' es de tipo booleano y añade un salto a la pila
def p_w2(p):
    "w2 : RPAREN"
    aux = pilaOperadores.pop()
    if aux.get("type") == "bool":
        newCuadruplo = Cuadruplo("GOTOF", aux, EMPTY, EMPTY)
        pilaSalto.append(len(CuadruploList))
        CuadruploList.append(newCuadruplo)
    else:
        print(f"expression in line {p.lineno(1)!r} needs to result in boolean type")
        sys.exit()


# Genera un cuádruplo para volver al inicio del 'while'
def p_w3(p):
    "w3 :"
    aux = pilaSalto.pop()
    newCuadruplo = Cuadruplo("GOTO", EMPTY, EMPTY, pilaSalto.pop())
    CuadruploList.append(newCuadruplo)
    CuadruploList[aux].fill(len(CuadruploList))


# Define la estructura del bucle 'for'
def p_for(p):
    "for : FOR ID EQUAL expression f1 expression f2 statements"
    var = pilaOperadores.pop()
    aux = pilaSalto.pop()
    checkConstOverlap({"type": "int", "id": 1})
    newCuadruplo = Cuadruplo("+", var, pilaOperadores.pop(), var.get("dir"))

    CuadruploList.append(newCuadruplo)
    newCuadruplo = Cuadruplo("GOTO", EMPTY, EMPTY, pilaSalto.pop())
    CuadruploList.append(newCuadruplo)
    CuadruploList[aux].fill(len(CuadruploList))


# Comprueba que el valor inicial del 'for' sea de tipo entero y añade un salto a la pila
def p_f1(p):
    "f1 : TO"
    aux = pilaOperadores.pop()
    if aux.get("type") == "int":
        var = findIdType(p[-3])
        pilaOperadores.append(aux)
        assignment()
        pilaOperadores.append(var)
        pilaOperadores.append(aux)
        pilaSalto.append(len(CuadruploList))
    else:
        print(
            f"first expression in line {p.lineno(1)!r} needs to result in integer type"
        )
        sys.exit()


# Genera cuádruplos para probar si la variable es menor o igual al límite y para ir al final del 'for' cuando sea falso
def p_f2(p):
    "f2 : DO"
    global contadorResultados
    exp2 = pilaOperadores.pop()
    exp1 = pilaOperadores.pop()
    var = pilaOperadores.pop()
    if exp2.get("type") == "int":
        pilaOperadores.append(var)
        pilaOperadores.append(exp2)
        genCuadruplo("<=")
        pilaSalto.append(len(CuadruploList))
        newCuadruplo = Cuadruplo("GOTOF", pilaOperadores.pop(), EMPTY, " ")
        CuadruploList.append(newCuadruplo)
        pilaOperadores.append(var)

    else:
        print(
            f"second expression in line {p.lineno(1)!r} needs to result in integer type"
        )
        sys.exit()

# Define expresiones y factores
def p_expression(p):
    """expression : expression expressionp
    | factor"""
    p[0] = p[1]

# Genera cuádruplos para operaciones binarias
def p_expressionp(p):
    """expressionp : AND expression
    | OR expression

    | LTHAN expression
    | GTHAN expression
    | EQUALS expression
    | DIFFERENCE expression
    | LEQUAL expression
    | GEQUAL expression

    | PLUS expression
    | MINUS expression

    | TIMES expression
    | DIVIDE expression
    | MOD expression"""
    genCuadruplo(p[1])

# Procesa factores que pueden ser una expresión entre paréntesis, una variable o una constante
def p_factor(p):
    """factor : LPAREN expression RPAREN
    | var_cte
    | variable"""
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = p[1]

# Define una variable con su identificador y procesa posibles índices o propiedades
def p_variable(p):
    "variable : ID variablep"


# Carga una variable a la pila de operandoos, manejando índices de arreglo
def p_variablep(p):
    """variablep : LBRACKET expression RBRACKET
    | empty"""
    findIdType(p[-1])
    if len(p) == 4:
        global CuadruploList

        var = pilaOperadores.pop()
        exp = pilaOperadores.pop()
        if exp.get("type") != "int":
            print(
                f"Expression for array in line {p.lineno(1)!r} needs to result in integer type"
            )
            sys.exit()
        else:
            newCuadruplo = Cuadruplo("VER", exp, EMPTY, var.get("arrSize"))
            CuadruploList.append(newCuadruplo)
            checkConstOverlap({"type": var.get("type"), "id": var.get("dir")})
            pilaOperadores.append(exp)
            genCuadruplo("+")
            resultado = pilaOperadores.pop()
            resultado["dir"] = f"*{resultado.get('dir')}"
            pilaOperadores.append(resultado)

# Define constantes de diferentes tipos
def p_var_cte(p):
    """var_cte : TRUE bool
    | FALSE bool
    | CTE_C char
    | CTE_S string
    | CTE_I int
    | CTE_F float"""

# Maneja constantes booleanas
def p_bool(p):
    "bool :"
    global pilaOperadores
    cn = {"id": p[-1], "arrSize": 0, "type": "bool"}
    checkConstOverlap(cn)

# Maneja constantes de tipo carácter
def p_char(p):
    "char :"
    global pilaOperadores
    cn = {"id": p[-1], "arrSize": 0, "type": "char"}
    checkConstOverlap(cn)

# Maneja constantes de tipo cadena
def p_string(p):
    "string :"
    global pilaOperadores
    string = p[-1]
    cn = {"id": string[1:-1], "arrSize": 0, "type": "string"}
    checkConstOverlap(cn)

# Maneja constantes de tipo entero
def p_int(p):
    "int :"
    global pilaOperadores
    cn = {"id": p[-1], "arrSize": 0, "type": "int"}
    checkConstOverlap(cn)

# Maneja constantes de tipo flotante
def p_float(p):
    "float :"
    global pilaOperadores
    cn = {"id": p[-1], "arrSize": 0, "type": "float"}
    checkConstOverlap(cn)

# Define el tipo de datos para variables o constantes
def p_type(p):
    """type : INT
    | FLOAT
    | CHAR"""
    global tipoDatoActual
    tipoDatoActual = p[1]
    p[0] = p[1]

# Define un nodo vacío en la gramática
def p_empty(p):
    "empty :"
    p[0] = "void"
    pass

# Maneja errores sintácticos
def p_error(p):
    if p is None:
        print(f"Missing \u007D at end of file")
    else:
        print(f"Syntax error at {p.value!r} in line {p.lineno!r}")
    sys.exit()


# Genera cuádruplo para guardar el último elemento de la pila de operandoos en el penúltimo
def assignment():
    resultado = pilaOperadores.pop()
    variable = pilaOperadores.pop()
    arrSize = variable.get("arrSize")
    if resultado.get("type") == variable.get("type"):
        if resultado.get("arrSize") == arrSize:
            if arrSize < 2:
                newCuadruplo = Cuadruplo("=", resultado, EMPTY, variable.get("dir"))
                CuadruploList.append(newCuadruplo)
            else:
                for i in range(arrSize):
                    newCuadruplo = Cuadruplo(
                        "=",
                        {"dir": resultado.get("dir") + i},
                        EMPTY,
                        variable.get("dir") + i,
                    )
                    CuadruploList.append(newCuadruplo)
        else:
            print(
                f"Mismatched size of arrays caused by = on {resultado.get('id')} and {variable.get('id')}"
            )
            sys.exit()
    else:
        print(f"Type mismatch caused by = on {resultado.get('id')} and {variable.get('id')}")
        sys.exit()


# Verifica si una variable ya ha sido declarada, si no, la añade a directorioFunciones
def checkVarOverlap(id, arrSize):
    global directorioFunciones
    overlap = False
    if id in directorioFunciones[programID]["vars"]:
        overlap = True
    if idFuncionActual != programID:
        if id in directorioFunciones[idFuncionActual]["vars"]:
            overlap = True

    if not overlap:
        var = {"type": tipoDatoActual, "arrSize": arrSize}
        if idFuncionActual == programID:
            dir = MemoriaG.asignarMemoria(var)
        else:
            dir = MemoriaL.asignarMemoria(var)
        var["dir"] = dir

        directorioFunciones[idFuncionActual]["vars"][id] = var
    else:
        print(f"Variable name {id} has been declared elsewhere")
        sys.exit()


# Verifica si el identificador ha sido declarado, lo añade a la pila de operandoos y retorna su tipo
def findIdType(id):
    global pilaOperadores
    idType = "error"
    local = False
    # Busca el identificador en las variables globales y locales
    if id in directorioFunciones[programID]["vars"]:
        # Procesa el identificador global
        idType = directorioFunciones[programID]["vars"][id].get("type")
        dir = directorioFunciones[programID]["vars"][id].get("dir")
        arrSize = directorioFunciones[programID]["vars"][id].get("arrSize")
    elif idFuncionActual != programID:
        if id in directorioFunciones[idFuncionActual]["vars"]:
            idType = directorioFunciones[idFuncionActual]["vars"][id].get("type")
            dir = directorioFunciones[idFuncionActual]["vars"][id].get("dir")
            arrSize = directorioFunciones[idFuncionActual]["vars"][id].get("arrSize")
            local = True

    if idType != "error":
        var = {"id": id, "arrSize": arrSize, "type": idType, "dir": dir}
        pilaOperadores.append(var)
        if local:
            return directorioFunciones[idFuncionActual]["vars"][id]
        else:
            return directorioFunciones[programID]["vars"][id]

    else:
        print(f"Variable name {id} has not been declared")
        sys.exit()


# Verifica si una función ya ha sido declarada. Si no, crea una variable para almacenar los retornos y la añade a directorioFunciones
def checkFuncOverlap():
    global directorioFunciones, idFuncionActual
    if idFuncionActual in directorioFunciones:
        print(f"Function name {idFuncionActual} has been declared elsewhere")
        sys.exit()
    else:
        directorioFunciones[idFuncionActual] = {"type": tipoDatoActual, "dir": len(CuadruploList), "vars": {}}
        if tipoDatoActual != "void":
            id = idFuncionActual
            idFuncionActual = programID
            checkVarOverlap(id, 0)
            idFuncionActual = id


# Verifica si una función existe en directorioFunciones y devuelve sus datos
def findFunc(func):
    global idFuncionActual
    if func in directorioFunciones:
        return (
            directorioFunciones[func].get("type"),
            directorioFunciones[func].get("dir"),
            directorioFunciones[func].get("params"),
        )
    else:
        print(f"Function {func} has not been declared")
        sys.exit()


# Añade una constante a la pila de operandoos, asigna dirección y la añade a tablaConstantes si aún no existe
def checkConstOverlap(cn):
    global tablaConstantes
    id = cn.get("id")
    if id not in tablaConstantes:
        dir = MemoriaC.asignarMemoria(cn)
        tablaConstantes[id] = {"type": cn.get("type"), "arrSize": 0, "dir": dir}
    else:
        dir = tablaConstantes[id].get("dir")

    cn["dir"] = dir
    pilaOperadores.append(cn)


def genCuadruplo(operador):
    # Crea cuádruplos para operaciones simples
    global pilaOperadores, CuadruploList, contadorResultados, tipoDatoActual
    operando2 = pilaOperadores.pop()
    operando1 = pilaOperadores.pop()
    resultadoType = cubo[operando1.get("type")][operando2.get("type")][operador]

    if resultadoType != "error":
        genresultado(resultadoType)
        newCuadruplo = Cuadruplo(operador, operando1, operando2, pilaOperadores[-1].get("dir"))
        CuadruploList.append(newCuadruplo)
    else:
        print(
            f"Desajuste de tipo causado por {operador} en {operando1.get('id')} y {operando2.get('id')}"
        )
        sys.exit()


# Genera una nueva variable resultadooral y la añade a la pila de operandoos
def genresultado(resultadoType):
    global contadorResultados
    resultado = "resultado" + str(contadorResultados)
    contadorResultados += 1
    isLocal = programID != idFuncionActual
    dir = MemoriaT.asignarMemoria(resultadoType, isLocal)
    pilaOperadores.append({"id": resultado, "type": resultadoType, "dir": dir, "arrSize": 0})


# Construir el analizador (parser)
parser = yacc.yacc()

# Obtener la entrada
if __name__ == "__main__":
    fileName = sys.argv[1]

    # Comprobar que el archivo exista y abrirlo
    if isfile(fileName):
        inputFile = open(fileName, "r")
        inputCode = inputFile.read()
        inputFile.close()
        parser.parse(inputCode)
    else:
        print("El archivo no existe")
        sys.exit()

    # Mostrar la tabla de funciones
    for key in directorioFunciones:
        print(f"{key}:")
        for element in directorioFunciones[key]:
            print(f"{element}: {directorioFunciones[key][element]}")
        print()

    # Mostrar la tabla de constantes
    # print(tablaConstantes)

    # Mostrar cuádruplos en lista
    cont = 0
    for Cuadruplo in CuadruploList:
        print(cont, str(Cuadruplo))
        cont = cont + 1

    # Inicializar y ejecutar la Máquina Virtual
    vm = MaquinaVirtual(programID, directorioFunciones, MemoriaG, MemoriaL, MemoriaC, MemoriaT)

    # Mostrar datos internos de ejecución
    show = True
    vm.run(CuadruploList, show)
