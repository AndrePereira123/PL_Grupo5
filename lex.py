import ply.lex as lex
import re

error_count = 0  # Contador de erros

# Lista de tokens (SEM COMMENT)
tokens = (
    'INTEGER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'MOD',
    'REAL_DIVIDE',
    'LPAREN',
    'RPAREN',
    'LBRACKET',
    'RBRACKET',
    'SEMICOLON',
    'COLON',
    'COMMA',
    'DOT',
    'ASSIGN',
    'EQUAL',
    'LT',
    'GT',
    'LE',
    'GE',
    'NE',
    'IDENTIFIER',
    'TYPE_STRING',
    'STRING',
    'PROGRAM',
    'BEGIN',
    'END_DOT',
    'END',
    'VAR',
    'TYPE_INTEGER',
    'TYPE_REAL',
    'REAL',
    'BOOLEAN',
    'IF',
    'THEN',
    'ELSE',
    'WHILE',
    'DO',
    'FOR',
    'TO',
    'DOWNTO',
    'ARRAY',
    'OF',
    'WRITE',
    'WRITELN',
    'READLN',
    'TRUE',
    'FALSE',
    'AND',
    'OR',
    'NOT'
)

# Regras para tokens simples
t_ASSIGN = r':='
t_LE = r'<='
t_GE = r'>='    ## mais longos primeiro 
t_NE = r'<>'
t_REAL_DIVIDE = r'/'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_SEMICOLON = r';'
t_COLON = r':'
t_COMMA = r','
t_DOT = r'\.'
t_EQUAL = r'='
t_LT = r'<'
t_GT = r'>'



# COMENTÁRIOS - Colocar no início das funções de tokens
def t_COMMENT(t):
    r'\{[^}]*\}|\(\*([^*]|\*(?!\)))*\*\)|//.*'
    pass  # Ignorar comentários

# Palavras-chave (por ordem de precedência)
def t_PROGRAM(t):
    r'program'
    t.type = 'PROGRAM'
    return t

def t_BEGIN(t):
    r'begin'
    t.type = 'BEGIN'
    return t

def t_END_DOT(t):
    r'end\.'
    t.type = 'END_DOT'
    return t

def t_END(t):
    r'end'
    t.type = 'END'
    return t

def t_VAR(t):
    r'var'
    t.type = 'VAR'
    return t

def t_TYPE_INTEGER(t):
    r'integer'
    t.type = 'TYPE_INTEGER'
    return t

def t_TYPE_STRING(t):
    r'string'
    t.type = 'TYPE_STRING'
    return t

def t_TYPE_REAL(t):
    r'real'
    t.type = 'TYPE_REAL'
    return t

def t_BOOLEAN(t):
    r'boolean'
    t.type = 'BOOLEAN'
    return t

def t_IF(t):
    r'if'
    t.type = 'IF'
    return t

def t_THEN(t):
    r'then'
    t.type = 'THEN'
    return t

def t_ELSE(t):
    r'else'
    t.type = 'ELSE'
    return t

def t_WHILE(t):
    r'while'
    t.type = 'WHILE'
    return t

def t_DOWNTO(t):
    r'downto'
    t.type = 'DOWNTO'
    return t

def t_DO(t):
    r'do'
    t.type = 'DO'
    return t

def t_FOR(t):
    r'for'
    t.type = 'FOR'
    return t

def t_TO(t):
    r'to'
    t.type = 'TO'
    return t

def t_ARRAY(t):
    r'array'
    t.type = 'ARRAY'
    return t

def t_OF(t):
    r'of'
    t.type = 'OF'
    return t

def t_WRITELN(t):
    r'writeln'
    t.type = 'WRITELN'
    return t

def t_WRITE(t):
    r'write'
    t.type = 'WRITE'
    return t

def t_READLN(t):
    r'readln|read'
    t.type = 'READLN'
    return t


def t_TRUE(t):
    r'true'
    t.type = 'TRUE'
    return t

def t_FALSE(t):
    r'false'
    t.type = 'FALSE'
    return t

def t_AND(t):
    r'and'
    t.type = 'AND'
    return t

def t_OR(t):
    r'or'
    t.type = 'OR'
    return t

def t_NOT(t):
    r'not'
    t.type = 'NOT'
    return t

def t_DIVIDE(t):
    r'div'
    t.type = 'DIVIDE'
    return t

def t_MOD(t):
    r'mod'
    t.type = 'MOD'
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    t.type = 'IDENTIFIER'
    return t

# Strings
def t_STRING(t):
    r"'([^\\\n]|(\\.))*?'"
    t.value = t.value[1:-1]  # Remover aspas
    return t


def t_REAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

# Números
def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Nova linha
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignorar espaços e tabulações
t_ignore = ' \t'

# Erros
def t_error(t):
    global error_count
    print(f"Illegal character '{t.value[0]}'")
    error_count += 1
    t.lexer.skip(1)

# Construir o lexer
lexer = lex.lex(reflags=re.IGNORECASE)

# Testar o lexer com um exemplo de código Pascal
if __name__ == "__main__":
    file = open("programas_pascal/1.hello_world.pas", "r", encoding="utf-8")
    data = file.read()
    file.close()

    lexer.input(data)

    Contagem_instancias = {}

    verde = "\033[92m"
    vermelho = "\033[91m"
    amarelo = "\033[93m"
    RESET = "\033[0m"

    for i, tok in enumerate(lexer):
        color = verde if i % 2 == 0 else vermelho

        if tok.type in Contagem_instancias:
            Contagem_instancias[tok.type] += 1
        else:
            Contagem_instancias[tok.type] = 1

        print(f"{color}{tok.type:<10}: {tok.value:^15}   Linha: {tok.lineno}   Posição: {tok.lexpos}{RESET}")

    print(f"{amarelo}\n||", end=" ")
    for k, v in Contagem_instancias.items():
        print(f"{v} {k}", end=" || ")
    print(f"\n{RESET}")

    if (error_count > 0):
        print(f"{vermelho}Total de erros encontrados: {error_count}{RESET}")
    else:
        print(f"{verde}Total de erros encontrados: {error_count}{RESET}")