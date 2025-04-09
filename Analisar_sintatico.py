from Analisar_lex import lexer

prox_simb = ('Erro', '', 0, 0)

def parserError(simb):
    print(f"Erro sintático, token inesperado: {simb}")
    exit(1)

def rec_term(simb):
    global prox_simb
    if prox_simb and prox_simb.type == simb:
        prox_simb = lexer.token()
    else:
        parserError(prox_simb)

def rec_var_declaration():
    global prox_simb
    if prox_simb.type == 'KEYWORD' and prox_simb.value == 'var':
        rec_term('KEYWORD')  # Reconhece 'var'
        while prox_simb.type == 'IDENTIFIER':
            # Reconhece uma lista de variáveis separadas por vírgulas
            while prox_simb.type == 'IDENTIFIER':
                rec_term('IDENTIFIER')  # Nome da variável
                if prox_simb.type == 'COMMA':  # Vírgula entre variáveis
                    rec_term('COMMA')
                else:
                    break
            rec_term('COLON')  # ':'
            if prox_simb.type == 'KEYWORD' and prox_simb.value in ['integer', 'real', 'boolean', 'string']:
                rec_term('KEYWORD')  # Tipo da variável
            else:
                parserError(prox_simb)
            rec_term('SEMICOLON')  # ';'
        print("Reconheci: Declaração de Variáveis")
    else:
        parserError(prox_simb)

def rec_program():
    global prox_simb
    if prox_simb.type == 'KEYWORD' and prox_simb.value == 'program':
        rec_term('KEYWORD')
        rec_term('IDENTIFIER')
        rec_term('SEMICOLON')
        if prox_simb.type == 'KEYWORD' and prox_simb.value == 'var':
            rec_var_declaration()  # Adiciona suporte para a seção 'var'
        rec_block()
        rec_term('DOT')
        print("Reconheci: Program")
    else:
        parserError(prox_simb)

def rec_block():
    global prox_simb
    if prox_simb.type == 'KEYWORD' and prox_simb.value == 'begin':
        rec_term('KEYWORD')
        rec_statements()
        rec_term('KEYWORD')  # end
        print("Reconheci: Block")
    else:
        parserError(prox_simb)

def rec_statements():
    global prox_simb
    rec_statement()
    while prox_simb and prox_simb.type == 'SEMICOLON':
        rec_term('SEMICOLON')
        rec_statement()
    print("Reconheci: Statements")

def rec_statement():
    global prox_simb
    if prox_simb.type == 'IDENTIFIER':
        rec_term('IDENTIFIER')
        rec_term('ASSIGN')
        rec_expression()
        print("Reconheci: Assignment")
    elif prox_simb.type == 'KEYWORD' and prox_simb.value in ['write', 'writeln']:
        rec_term('KEYWORD')
        rec_term('LPAREN')
        # Processa múltiplos argumentos separados por vírgulas
        while True:
            if prox_simb.type == 'STRING':  # Suporte para strings
                rec_term('STRING')
            else:
                rec_expression()
            if prox_simb.type == 'COMMA':  # Vírgula entre argumentos
                rec_term('COMMA')
            else:
                break
        rec_term('RPAREN')
        print("Reconheci: Write")
    elif prox_simb.type == 'KEYWORD' and prox_simb.value == 'if':
        rec_term('KEYWORD')
        rec_expression()
        rec_term('KEYWORD')  # then
        rec_statement()
        if prox_simb.type == 'KEYWORD' and prox_simb.value == 'else':
            rec_term('KEYWORD')
            rec_statement()
        print("Reconheci: If")
    elif prox_simb.type == 'KEYWORD' and prox_simb.value == 'while':
        rec_term('KEYWORD')
        rec_expression()
        rec_term('KEYWORD')  # do
        rec_statement()
        print("Reconheci: While")
    elif prox_simb.type == 'KEYWORD' and prox_simb.value == 'for':
        rec_term('KEYWORD')  # Reconhece 'for'
        rec_term('IDENTIFIER')  # Variável de controle
        rec_term('ASSIGN')  # ':='
        rec_expression()  # Valor inicial
        if prox_simb.type == 'KEYWORD' and prox_simb.value in ['to', 'downto']:
            rec_term('KEYWORD')  # Reconhece 'to' ou 'downto'
        else:
            parserError(prox_simb)
        rec_expression()  # Valor final
        rec_term('KEYWORD')  # do
        rec_statement()  # Corpo do loop
        print("Reconheci: For")
    elif prox_simb.type == 'KEYWORD' and prox_simb.value == 'begin':
        rec_block()
    else:
        print("Reconheci: Empty Statement")

def rec_expression():
    global prox_simb
    rec_term_expression()
    while prox_simb and prox_simb.type in ['PLUS', 'MINUS', 'AND', 'OR']:
        rec_term(prox_simb.type)  # Reconhece operadores como +, -, AND, OR
        rec_term_expression()
    print("Reconheci: Expression")

def rec_term_expression():
    global prox_simb
    rec_factor()
    while prox_simb and prox_simb.type in ['TIMES', 'DIVIDE', 'MOD']:
        rec_term(prox_simb.type)  # Reconhece operadores como *, /, MOD
        rec_factor()
    print("Reconheci: Term")

def rec_factor():
    global prox_simb
    if prox_simb.type == 'NUMBER':
        rec_term('NUMBER')
        print("Reconheci: Number")
    elif prox_simb.type == 'IDENTIFIER':
        rec_term('IDENTIFIER')
        print("Reconheci: Identifier")
    elif prox_simb.type == 'LPAREN':
        rec_term('LPAREN')  # Reconhece '('
        rec_expression()    # Processa a expressão dentro dos parênteses
        rec_term('RPAREN')  # Reconhece ')'
        print("Reconheci: Parenthesized Expression")
    else:
        parserError(prox_simb)

def rec_Parser(data):
    global prox_simb
    lexer.input(data)
    prox_simb = lexer.token()
    rec_program()
    if prox_simb and prox_simb.type != 'EOF':
        parserError(prox_simb)
    print("Parsing concluído com sucesso!")

# Entrada do usuário
if __name__ == "__main__":
    linha = input("Introduza o código Pascal: ")
    rec_Parser(linha)