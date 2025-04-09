import ply.lex as lex

error_count = 0  # Contador de erros

# Lista de tokens
tokens = (
    'COMMENT',
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
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
    'STRING',
    'KEYWORD'
)

# Palavras-chave de Pascal
keywords = {
    'program', 'begin', 'end', 'var', 'integer', 'real', 'boolean', 'if', 'then', 'else',
    'while', 'do', 'for', 'to', 'downto', 'function', 'procedure', 'array', 'of', 'write',
    'writeln', 'read', 'readln', 'true', 'false'
}

# Regras para tokens simples
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_SEMICOLON = r';'
t_COLON = r':'
t_COMMA = r','
t_DOT = r'\.'
t_ASSIGN = r':='
t_EQUAL = r'='
t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='
t_NE = r'<>'

# Comentários
def t_COMMENT(t):
    r'\{[^}]*\}|\(\*[^*]*\*\)'
    pass  # Ignorar comentários

# Strings
def t_STRING(t):
    r'\'[^\']*\''
    t.value = t.value[1:-1]  # Remover aspas
    return t

# Números
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Identificadores e palavras-chave
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value.lower() in keywords:
        t.type = 'KEYWORD'
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
lexer = lex.lex()

# Testar o lexer com um exemplo de código Pascal
if __name__ == "__main__":
    file = open("./texto_exemplo.txt", "r", encoding="utf-8")
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