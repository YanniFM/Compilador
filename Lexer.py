import ply.lex as lex

# Palabras reservadas y su token correspondiente
reserved = {
    'program': 'PROGRAM', 'vars': 'VARS', 'function': 'FUNCTION', 
    'main': 'MAIN', 'return': 'RETURN', 'read': 'READ', 'write': 'WRITE', 
    'if': 'IF', 'then': 'THEN', 'else': 'ELSE', 'while': 'WHILE', 
    'do': 'DO', 'for': 'FOR', 'to': 'TO', 'int': 'INT', 'float': 'FLOAT', 
    'char': 'CHAR', 'true': 'TRUE', 'false': 'FALSE', 'void': 'VOID',
    'pow': 'POW', 'rand': 'RAND', 'med': 'MED', 'moda': 'MODA', 
    'var': 'VAR', 'reg': 'REG', 'plot': 'PLOT'
}


# Lista de tokens que el lexer reconocerá, incluyendo las palabras reservadas
tokens = [
    "ID", "CTE_I", "CTE_F", "CTE_C", "CTE_S",
    "PLUS", "MINUS", "TIMES", "DIVIDE", "EQUALS", "DIFFERENCE",
    "GTHAN", "LTHAN", "GEQUAL", "LEQUAL", "AND", "OR",
    "LPAREN", "RPAREN", "LBRACE", "RBRACE", "LBRACKET", "RBRACKET",
    "SEMICOLON", "COMMA",
    "EQUAL", "MOD"
] + list(reserved.values())



# Ignorar espacios
t_ignore = ' \t'

# Definiciones de expresiones regulares para tokens simples

t_LPAREN = r'\('    # Paréntesis izquierdo
t_RPAREN = r'\)'    # Paréntesis derecho
t_LBRACKET = r'\['  # Corchete izquierdo
t_RBRACKET = r'\]'  # Corchete derecho
t_LBRACE = r'\{'    # Llave izquierda
t_RBRACE = r'\}'    # Llave derecha
t_PLUS = r'\+'      # Operador de suma
t_MINUS = r'-'      # Operador de resta
t_TIMES = r'\*'     # Operador de multiplicación
t_DIVIDE = r'/'     # Operador de división
t_MOD = r'%'        # Operador de módulo
t_AND = r'&'       # Operador lógico AND
t_OR = r'\|\|'      # Operador lógico OR
t_EQUALS = r'=='    # Operador de igualdad
t_DIFFERENCE = r'!='# Operador de desigualdad
t_GTHAN = r'>'      # Operador de mayor que
t_LTHAN = r'<'      # Operador de menor que
t_GEQUAL = r'>='    # Operador de mayor o igual que
t_LEQUAL = r'<='    # Operador de menor o igual que
t_SEMICOLON = r';'  # Punto y coma
t_COMMA = r','      # Coma
t_EQUAL = r'='      # Signo de asignación
t_CTE_S = r'"(.*?)"'# Constantes de tipo cadena (string)
t_CTE_C = r"(L)?\'([^\\\n]|(\\.))*?\'" # Constantes de tipo carácter (char)

# Función para identificadores y palabras reservadas
# Solo acepta identificadores que comiencen con letra minúscula, seguida de letras y números.
def t_ID(t):
    r"([a-z][a-zA-Z0-9]*)"
    if t.value in reserved:
        t.type = reserved[t.value]
    return t

# Función para constantes flotantes
# Permite números negativos y flotantes.
def t_CTE_F(t):
    r"[-]?[0-9]+([.][0-9]+)"
    t.value = float(t.value)
    return t

# Función para constantes enteras
# Permite números negativos.
def t_CTE_I(t):
    r"[-]?[0-9]+"
    t.value = int(t.value)
    return t

# Función para manejar errores léxicos
# Imprime un mensaje de error
def t_error(t):
    print(f"Illegal character {t.value[0]} in line {t.lexer.lineno}")
    t.lexer.skip(1)

# Función para manejar comentarios.
# Ignora los comentarios que comienzan con '%'.
def t_LINE_COMMENT(t):
    r"%.*"
    pass

# Función para manejar saltos de línea.
# Actualiza el número de línea al encontrar saltos de línea.
def t_skip_newline(t):
    r"\n+"
    t.lexer.lineno += t.value.count("\n")


# Se crea el lexer
lexer = lex.lex()