import os
from lex import tokens
import ply.yacc as yacc


variaveis = {} ## chave : nome da variavel, valor : (tipo da variavel,index)
index = 0 ## index na maquina virtual
nivel_apontador = 0
## index = valor na maquina virtual 

def p_file(p):
    'file : PROGRAM name vars code'
    if p[3] is not None:
        p[0] = p[3] + p[4]
    else:
        p[0] = p[4]
    print(f"File parsed \n")

def p_name(p):
    'name : IDENTIFIER SEMICOLON'
    p[0] = p[1]
    print(f"Name: {p[0]}")

################################ variaveis ##########################################
def p_vars(p):
    '''vars : VAR varstail
           | empty'''
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = None
    
    print(f"Vars:")
    for key,val in variaveis.items():
        print(f"  {key}: {val}")

def p_varstail(p):
    '''varstail : vardecl varstail
                | empty'''
    if len(p) == 3:
        if p[2] is not None:
            p[0] = p[1] + p[2]
        else:
            p[0] = p[1]
    else:
        p[0] = []

    

def p_vardecl(p):
    'vardecl : idlist COLON type SEMICOLON'
    global variaveis, index, nivel_apontador
    p[0] = []
    for var in p[1]:
        variaveis[var] = (p[3].lower(),index) ## registar no dicionario cada variavel 
        index += 1 
        p[3] = p[3].lower()
        if p[3] == 'integer' or p[3] == 'boolean':
            p[0] += ["     PUSHI 0\n"]

        elif p[3] == 'real':
            p[0] += ["     PUSHF 0.0\n"]

        elif p[3] == 'string':
            p[0] += ["     PUSHS \"\"\n"]

        elif p[3] == 'array':
            pass  ## TODO: array
    
    

def p_idlist(p):
    'idlist : IDENTIFIER idlistTail'
    if p[2] is None:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]
    

def p_idlistTail(p):
    '''idlistTail : COMMA IDENTIFIER idlistTail
           | empty'''
    if len(p) == 4:
        if p[3] is not None:
            p[0] = [p[2]] + p[3]
        else:
            p[0] = [p[2]]
    else:
        p[0] = None


def p_type(p):
    '''type : TYPE_INTEGER
           | TYPE_REAL
           | BOOLEAN
           | TYPE_STRING
           | ARRAY LBRACKET INTEGER RBRACKET OF type'''
    if len(p) == 2:  
        p[0] = p[1]
    else:  
        p[0] = {'type': 'ARRAY', 'size': p[3], 'element_type': p[6]}

############################## programa ##########################################
def p_code(p):
    'code : BEGIN expressions END'
    p[0] = ["START\n"] + p[2] + ["STOP\n"]
    print(f"Code parsed \n")

def p_expressions(p):
    '''expressions : statement expressions_tail
                   | empty'''
    if len(p) == 3:
        if p[2] is not None:
            p[0] = p[1] + p[2]
        else:
            p[0] = p[1]

    else: ## caso de empty
        p[0] = p[1] 

def p_expressions_tail(p):
    '''expressions_tail : SEMICOLON expressions
                        | empty'''
    if len(p) == 3:
        if p[2] is not None:
            p[0] = p[2]
        else:
            p[0] = []
    else: ## caso de empty
        p[0] = p[1]


#################################### statements ##########################################

def p_statement(p):
    '''statement : IDENTIFIER ASSIGN assign_expression  
                | WRITELN write_statement 
                | WRITE write_statement 
                | READLN readln_statement 
                | IF if_condition THEN expressions ELSE expressions
                | FOR 
                | WHILE ''' ## TODO implementar os outros statements
    if p[2] == ":=":   
        global variaveis, index, nivel_apontador
        if variaveis.get(p[1]) is not None:  ##TODO nao suporta varaiveis dentro de arrays
            tipo_guardado, index_var = variaveis[p[1]]  
        else:
            raise NameError(f"Variável não declarada: {p[1]}")

        if isinstance(p[3], str): ## (So quando é string)
            if tipo_guardado == 'string':               ## se for string => simples atribuição
                p[0] = ["     PUSHS \"" + str(p[3]) + "\"\n"] + ["       STOREG " + str(index_var) + "\n"]
            else: 
                raise TypeError(f"Tipo de dado inválido para atribuição: {p[3].slice[1].type} (esperado = {tipo_guardado}) para variavel \"{p[1]}\"")
        else:
            type, linhas_calculo = p[3]   ## (INTEGER/REAL/...,valor)

            if type.lower() != tipo_guardado:
                if (tipo_guardado, type.lower()) in [('integer', 'real'), ('real', 'integer')]:
                    if tipo_guardado == 'real':
                        linhas_calculo = linhas_calculo + ["     ITOF\n"]   ## converte para real um inteiro, se for atribuido a um real
                        type = 'real'
                    else:
                        raise TypeError(f"Tipo de dado inválido para atribuição para variavel \"{p[1]}\", valor inteiro n pode tomar valor de real")
                else:
                    raise TypeError(f"Tipo de dado inválido para atribuição: {type} (esperado = {tipo_guardado}) para variavel \"{p[1]}\"")

            if tipo_guardado == 'integer' :      
                p[0] = linhas_calculo + ["       STOREG " + str(index_var) + "\n"]
            elif tipo_guardado == 'real':
                p[0] = linhas_calculo + ["       STOREG " + str(index_var) + "\n"]
            elif tipo_guardado == 'boolean':
                p[0] = linhas_calculo + ["       WRITEI\n"]
                ##TODO ajustar boleano para ser TRUE/FALSE

            
        

    elif p[1].lower() == 'writeln':
        p[0] = p[2] + ["       WRITELN\n"]
    else:
        p[0] = p[2]    


def p_if_condition(p):
    '''if_condition : expression
                    | expression AND if_condition
                    | expression OR if_condition'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[3]


def p_write_statement(p):                               
    'write_statement : LPAREN string_statement RPAREN'
    p[0] = []
    first_iteration = True
    for arg in reversed(p[2]):
        expressao_ou_string = arg

        if isinstance(expressao_ou_string, str):
            p[0] += ["     PUSHS \"" + arg + "\"\n"]
        
        else:
                type, linhas_calculo = expressao_ou_string
                
                if type.lower() == 'integer' :      
                    p[0] = linhas_calculo + ["       STRI\n"]
                elif type.lower() == 'real':
                    p[0] = linhas_calculo + ["       STRF\n"]
                elif type.lower() == 'boolean':
                    p[0] = linhas_calculo + ["       WRITEI\n"]
                    ##TODO ajustar boleano para ser TRUE/FALSE
            
        if not first_iteration:
            p[0] += ["     CONCAT\n"]
        else:
            first_iteration = False
    
    p[0] += ["     WRITES\n"]


def p_readln_statement(p):
    'readln_statement : LPAREN string_statement RPAREN'
    p[0] = []
    for arg in p[2]:
        argtype = arg[0]
        if argtype == 'IDENTIFIER':
            global variaveis, index
            if variaveis.get(arg[1]) is not None:  ##TODO nao suporta varaiveis dentro de arrays
                tipo, index_var = variaveis[arg[1]]
                p[0] += ["     READ\n      DUP 1\n"]
                if tipo == 'integer' or tipo == 'boolean':      ##TODO ajustar boleano para ser TRUE/FALSE
                    p[0] += ["      ATOI\n"]
                elif tipo == 'real':
                    p[0] += ["      ATOF\n"]
                p[0] += ["      STOREG " + str(index_var) + "\n       WRITES WRITELN\n"]


def p_string_statement(p):
    '''string_statement : assign_expression
                        | assign_expression COMMA string_statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_assign_expression(p):
    '''assign_expression : expression
                         | STRING ''' ## TODO implementar expression e identifier
    p[0] = p[1]


##################################### expression (aritmetrica e booleana) ##########################################

def p_expression(p):
    '''expression : simple_expression expression_tail'''
    if p[2] is None:
        p[0] = p[1]
    else:
        op, type2, code2 = p[2]
        type1, code1 = p[1]
        
        if type1.lower() == type2.lower():
            pass
        elif (type1.lower(), type2.lower()) in [('integer', 'real'), ('real', 'integer')]:
            # Converte integer para real
            if type1.lower() == 'integer':
                code1 = ["     ITOF\n"] + code1
                type1 = 'real'
            else:
                code2 = ["     ITOF\n"] + code2
                type2 = 'real'
        else:
            raise TypeError(f"Tipo de dado inválido para comparação: {type1} {op} {type2}")

        
        # Seleciona instrução de comparação
        if type1.lower() == 'integer':
            instr = {
                '<': 'INF',
                '>': 'SUP',
                '<=': 'INFEQ',
                '>=': 'SUPEQ',
                '<>': 'EQUAL\n      NOT',
                '=': 'EQUAL'
            }[op]
        elif type1.lower() == 'real':
            instr = {
                '<': 'FINF',
                '>': 'FSUP',
                '<=': 'FINFEQ',
                '>=': 'FSUPEQ',
                '<>': 'EQUAL\n      NOT',
                '=': 'EQUAL'
            }[op]
        else:
            raise TypeError(f"Tipo de dado inválido para comparação: {type1} {op} {type2}")

        code = code1 + code2 + [f"     {instr}\n"]
        p[0] = ('boolean', code)


def p_expression_tail(p):
    '''expression_tail : LT simple_expression
                        | GT simple_expression
                        | LE simple_expression
                        | GE simple_expression
                        | NE simple_expression
                        | EQUAL simple_expression
                        | empty'''
    if len(p) == 3:
        operation = p[1]
        type2, code2 = p[2]
        p[0] = (operation, type2, code2)
    else:
        p[0] = None



def p_simple_expression(p):
    '''simple_expression : term simple_expression_tail'''
    if p[2] is None:
        p[0] = p[1]
    else:
        type1, code1 = p[1]
        type2, code2 = p[2]
        if type1.lower() != type2.lower():
            if type1.lower() in ['integer', 'real'] and type2.lower() in ['integer', 'real']:
                if type1.lower() == 'integer':
                    code1 =  code1 + ["     ITOF\n"]
                    type1 = 'real'
                else:
                    code2 =  code2 + ["     ITOF\n"]
                    type2 = 'real'
            else:
                raise TypeError(f"Tipo de dado inválido para soma: {type1} + {type2}")
        
        p[0] = (type1, code1 + code2)
        

def p_simple_expression_tail(p):
    '''simple_expression_tail : PLUS term simple_expression_tail
                             | MINUS term simple_expression_tail
                             | empty'''
    if len(p) == 4:
        # Cria uma nova lista somando as instruções
        type = p[2][0]
        
        if type.lower() == "integer":
            if p[1] == '+':
                code = p[2][1] + ["     ADD\n"]
            else:
                code = p[2][1] + ["     SUB\n"]
        elif type.lower() == "real":
            if p[1] == '+':
                code = p[2][1] + ["     FADD\n"]
            else:
                code = p[2][1] + ["     FSUB\n"]
        

        if p[3] is not None:
            if type.lower() != p[3][0].lower():
                raise TypeError(f"Tipo de dado inválido para soma: {type} + {p[3][0]}")
            code += p[3][1]
        p[0] = (type, code)
        print(f"Simple expression tail: {p[0]}")

    else:
        p[0] = p[1]

def p_term(p):
    '''term : factor term_tail'''
    if p[2] is None:
        p[0] = p[1]
    else:
        type1, code1 = p[1]
        type2, code2 = p[2]
        if type1.lower() != type2.lower():
            if type1.lower() in ['integer', 'real'] and type2.lower() in ['integer', 'real']:
                if type1.lower() == 'integer':
                    code1 = ["     ITOF\n"] + code1
                    type1 = 'real'
                else:
                    code2 = ["     ITOF\n"] + code2
                    type2 = 'real'
                    code2[-1] = code2[-1].replace("MUL", "FMUL").replace("DIV", "FDIV")
            else: 
                raise TypeError(f"Tipo de dado inválido para multiplicação: {type1} * {type2}")
            
        p[0] = (type1, code1 + code2)
        

def p_term_tail(p):
    '''term_tail : TIMES factor term_tail
                 | DIVIDE factor term_tail
                 | REAL_DIVIDE factor term_tail
                 | empty'''
    if len(p) == 4:
        type = p[2][0]          ## so tem divisao e multiplicacao para inteiros  ; pascal : "*"" e "div" 
                                ##TODO // falta mod e / e * para reais
                                ## TODO testar misturar operacoes de reais com inteiros
        
        if type.lower() == "integer":
            if p[1] == '*':
                code = p[2][1] + ["     MUL\n"]
            else:
                code = p[2][1] + ["     DIV\n"]

        elif type.lower() == "real":
            if p[1] == '*':
                code = p[2][1] + ["     FMUL\n"]
            else:
                code = p[2][1] + ["     FDIV\n"]


        if p[3] is not None:
            if type.lower() != p[3][0].lower():
                raise TypeError(f"Tipo de dado inválido para multiplicação: {type} * {p[3][0]}")
            code += p[3][1]
        p[0] = (type, code)

    else:
        p[0] = p[1]

def p_factor(p):                        ## carrega o valor para topo da stack
    '''factor : PLUS factor
              | MINUS factor
              | LPAREN expression RPAREN
              | INTEGER
              | REAL
              | IDENTIFIER'''
    if len(p) == 4:
        p[0] = p[2]
    elif len(p) == 3:
        tipo, code = p[2]
        # Se o fator for um número gera PUSHI -x ou PUSHF -x
        if tipo == 'INTEGER' and len(code) == 1 and code[0].startswith("     PUSHI "):
            valor = code[0].split()[1]
            if p.slice[1].type == 'MINUS':
                p[0] = (tipo, [f"     PUSHI -{valor}\n"])

        elif tipo == 'REAL' and len(code) == 1 and code[0].startswith("     PUSHF "):
            valor = code[0].split()[1]
            if p.slice[1].type == 'MINUS':
                p[0] = (tipo, [f"     PUSHF -{valor}\n"])

        else:
            # Para variáveis ou expressões - multiplicar por -1 
            if p.slice[1].type == 'MINUS':
                code += ["     PUSHI -1\n     MUL\n"]
            p[0] = (tipo, code)
    else:

        if p.slice[1].type == 'INTEGER':
            p[0] = (p.slice[1].type,["     PUSHI " + str(p[1]) + "\n"])
        elif p.slice[1].type == 'REAL':
            p[0] = (p.slice[1].type,["     PUSHF " + str(p[1]) + "\n"])
        elif p.slice[1].type == 'IDENTIFIER':
            global variaveis, index
            if variaveis.get(p[1]) is not None:  ##TODO nao suporta varaiveis dentro de arrays
                tipo, index_var = variaveis[p[1]]
                profundidade = index_var - index
                p[0] = (tipo, ["     PUSHFP\n       LOAD " + str(profundidade) + "\n"])






def p_error(p):
    print("Erro sintático no input!")

def p_empty(p):
    'empty :'
    p[0] = None

def reset_variaveis():
    global variaveis, index, nivel_apontador
    variaveis = {} 
    index = 0 
    nivel_apontador = 0

parser = yacc.yacc(debug=True)

folder_path = 'programas_pascal'
limite_ficheiros = 2
ficheiro = 0
for file_name in os.listdir(folder_path) :
    if ficheiro < limite_ficheiros:
        if file_name.endswith('.pas'):
            with open(os.path.join(folder_path, file_name), 'r') as file:
                reset_variaveis() ## para garantir que cada ficheiro tem o seu proprio dicionario de variaveis senao aponta 
                                  ## para slots errados na maquina virtual
                data = file.read()
                val = parser.parse(data)
                with open(f'programas_gerados/{file_name}', 'w') as output_file:
                    for linha in val:
                        output_file.write(f"{linha}")
        ficheiro += 1
