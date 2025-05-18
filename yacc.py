import os
import re
from lex import tokens
import ply.yacc as yacc

variaveis = {} ## chave : nome da variavel, valor : (tipo da variavel,index)
index = 0 ## index na maquina virtual
struct_index = 0 # index das estruturas
numero_ciclos_if = 0 ## numero de ciclos ifs 
numero_ciclos_for = 0 ## numero de ciclos fors 
numero_ciclos_while = 0 ## numero de ciclos whiles
index_variavel_ciclo_for = {} ## profundidade da variavel do ciclo for
tipo_ciclo_for = {} ## tipo de ciclo (downto ou to  )
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
    global variaveis, index, struct_index
    p[0] = []
    for var in p[1]:
        if (isinstance(p[3], dict)) and p[3].get('type') == 'ARRAY':
            menor, maior = p[3]['size']
            elements_type = p[3]['element_type']
            tamanho = maior - menor + 1
            variaveis[var] = ('array', (menor, maior, tamanho, struct_index, elements_type))
            struct_index += 1
            index += 1

            p[0] += [f"     ALLOC {tamanho}\n"]
            
        else:
            variaveis[var] = (p[3].lower(),index) ## registar no dicionario cada variavel 
            index += 1 
            p[3] = p[3].lower()
            if p[3] == 'integer' or p[3] == 'boolean':
                p[0] += ["     PUSHI 0\n"]

            elif p[3] == 'real':
                p[0] += ["     PUSHF 0.0\n"]

            elif p[3] == 'string':
                p[0] += ["     PUSHS \"\"\n"]

    
    

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
           | ARRAY LBRACKET arraytypes RBRACKET OF type'''
    if len(p) == 2:  
        p[0] = p[1]
    else:  
        p[0] = {'type': 'ARRAY', 'size': p[3], 'element_type': p[6]}

def p_array_types(p):
    '''arraytypes : INTEGER
                  | INTEGER DOT DOT INTEGER  
    '''
    if (len(p) != 2):
        p[0] = (int(p[1]), int(p[4])) # apenas arrays do tipo inteiro

    else:
        p[0] = int(p[1])


############################## programa ##########################################
def p_code(p):
    'code : BEGIN expressions END_DOT'
    p[0] = ["START\n"] + p[2] + ["STOP\n"]
    print(f"Code parsed \n")

def p_dotless_code(p):
    '''dotless_code : BEGIN expressions END''' 
    if len(p) == 4:
        p[0] = p[2]
    else:
        raise Exception("Erro sintático: fim inesperado do arquivo (possível bloco incompleto ou END; em falta)")


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
                | IDENTIFIER LBRACKET expression RBRACKET ASSIGN assign_expression
                | WRITELN write_statement 
                | WRITE write_statement 
                | READLN readln_statement 
                | IF if_condition THEN if_code 
                | FOR for_condition DO for_code
                | WHILE if_condition DO while_code''' 
    
    if p[2] == ":=":   
        global variaveis, index
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

            if tipo_guardado in ['integer', 'real', 'boolean']:      
                p[0] = linhas_calculo + ["       STOREG " + str(index_var) + "\n"]
            else: 
                raise TypeError(f"Tipo de dado inválido para atribuição: {type} (esperado = {tipo_guardado}) para variavel \"{p[1]}\"")

    elif len(p) == 7 and p[2] == "[" and p[4] == "]" and p[5] == ":=":
        if variaveis.get(p[1]) is not None:
            # ('array', (menor, maior, tamanho, struct_index))
            tipo_guardado, dados = variaveis[p[1]]  

            menor, maior, tamanho, struct_index, elements_type = dados

            actual_type, command = p[6]

            if (actual_type.lower() == elements_type):
                print(p[3])

                commands = []
                commands += [f'     PUSHST {struct_index}\n']
                commands += p[3][1]
                commands += [f'     PUSHI 1\n     SUB\n'] # por causa dos indices
                commands += command
                commands += ['     STOREN\n']

                # inserir o valor que queremos dar bind
                p[0] = commands

                # isto n pode ser pq é uma expression
                #raise NameError(f"Índice out of bonds: {p[1]}")
                
            else:
                raise NameError(f"Variável do tipo: {actual_type.lower()}. Deveria ser do tipo {elements_type}")
        else:
            raise NameError(f"Variável não declarada: {p[1]}")
        pass

    elif p[1].lower() == 'if' :
        global numero_ciclos_if
        type1, code1 = p[2]
        
        code = code1 + ["JZ ELSE" + str(numero_ciclos_if) + "\n"]
        code += p[4]
        
        numero_ciclos_if += 1
        p[0] = code

    elif p[1].lower() == 'for':
        global numero_ciclos_for
        type1, code1 = p[2]
        
        code = code1 + ["JZ FOREND" + str(numero_ciclos_for) + "\n"]
        code += p[4]
        
        numero_ciclos_for += 1
        p[0] = code

    elif p[1].lower() == 'while':
        global numero_ciclos_while
        type, code1 = p[2]
        if type.lower() != 'boolean':
            raise TypeError("Condição do WHILE tem de ser boolean")
        code2 = p[4]  # assumindo 'WHILE cond DO if_code'

        code = []
        code += [f"WHILESTART{numero_ciclos_while}:\n"]
        code += code1
        code += [f"     JZ WHILEEND{numero_ciclos_while}\n"]
        code += code2

        
        numero_ciclos_while += 1
        p[0] = code

    elif p[1].lower() == 'writeln':
        p[0] = p[2] + ["       WRITELN\n"]
    else:
        p[0] = p[2]    



def p_while_code(p):
    '''while_code : dotless_code 
                | statement 
                | empty'''
    if len(p) == 2:
        global numero_ciclos_while
        code = p[1] if p[1] is not None else [] 

        code += [f"     JUMP WHILESTART{numero_ciclos_while}\n"]
        code += [f"WHILEEND{numero_ciclos_while}:\n"]

        p[0] = code
    else:
        p[0] = []


def p_if_code(p):
    '''if_code : dotless_code opt_else
               | statement opt_else
               | empty'''
    if len(p) == 3:
        global numero_ciclos_if
        code = p[1] if p[1] is not None else [] ## codigo do if
        codigo_else = p[2] if p[2] is not None else []
        code += ["     JUMP ENDIF" + str(numero_ciclos_if) + "\n"] + ["ELSE" + str(numero_ciclos_if) + ":\n"] + codigo_else + ["ENDIF" + str(numero_ciclos_if) + ":\n"]
        
        p[0] = code
    else:
        p[0] = []

def p_for_condition(p):
    '''for_condition : expression ASSIGN expression to_expression'''  ## x := 0 to 10       ou       x := y+2 to z*2 


    type1, code1 = p[1]  ## so fazemos para verificar q e inteiro e para saber index para guardar novo valor usado no ciclo
    if type1.lower() != 'integer':
        raise TypeError(f"Tipo de dado inválido para acolher ciclo for (var :=) : {p[1][0]} (esperado = integer)")
    type2, code2 = p[3]
    if type2.lower() != 'integer':
        raise TypeError(f"Tipo de dado inválido para atribuir a variavel do ciclo for (:= var): {p[3][0]} (esperado = integer)")

    code3 = p[4] 

    if len(p) == 5:
        global numero_ciclos_for , index_variavel_ciclo_for, index
        match = re.search(r'LOAD\s+(-?\d+)', code1[0])
        if match:
            distancia = int(match.group(1))  ## valor negativo (para LOADs) , conta de cima para baixo
            profundidade = distancia + index  ## valor positivo (relativo a variaveis na stack inicial) conta de baixo para cima

            index_variavel_ciclo_for[numero_ciclos_for] = distancia

            p[0] = (type1, code2 + ["      STOREG " + str(profundidade) + "\n"]  # guardamos  o valor inicial da variavel do ciclo for na stack
                                + ["FORSTART" + str(numero_ciclos_for) + ":\n"]    # comecamos o ciclo
                                + ["     PUSHFP\n      LOAD " + str(distancia) + "\n"] + code3) # comparacao entre o valor da variavel e o valor final a alcancar
                                
    else:
        p[0] = p[1]

def p_to_expression(p):
    '''to_expression : TO expression
                     | DOWNTO expression'''
    if len(p) == 3:
        global numero_ciclos_for
        type1, code1 = p[2]
        if type1.lower() != 'integer':
            raise TypeError(f"Tipo de dado inválido para comparação com a variável do ciclo for (to var): {p[2][0]} (esperado = integer)")
        
        if p[1].lower() == 'to':
            p[0] = code1 + ["     INFEQ\n"]    ## se queremos alcancar um numero ele verifica que ainda e inferior para continuar o ciclo
            tipo_ciclo_for[numero_ciclos_for] = ''
        else: 
            p[0] = code1 + ["     SUPEQ\n"]
            tipo_ciclo_for[numero_ciclos_for] = '-'
    else:
        p[0] = []

def p_for_code(p):
    '''for_code : dotless_code 
               | statement 
               | empty'''
    if len(p) == 2:
        global numero_ciclos_for, index_variavel_ciclo_for , index
        code = p[1] if p[1] is not None else [] 

        distancia = index_variavel_ciclo_for[numero_ciclos_for]
        profundidade = distancia + index
        code += ["     PUSHFP\n     LOAD" + str(distancia) + f"\n     PUSHI {tipo_ciclo_for[numero_ciclos_for]}1\n     ADD\n     STOREG " + str(profundidade) + "\n"]
                                                           # o tipo de ciclo for guarda um - se o ciclo for "for downto"
        code += ["     JUMP FORSTART" + str(numero_ciclos_for) + "\n"] + ["FOREND" + str(numero_ciclos_for) + ":\n"]
        
        p[0] = code
    else:
        p[0] = []

def p_opt_else(p):
    '''opt_else : ELSE code_or_statement
                | empty'''
    if len(p) == 3:
        p[0] = p[2] if p[2] is not None else []
    else:
        p[0] = []

def p_code_or_statement(p):
    '''code_or_statement : dotless_code
                         | statement'''
    p[0] = p[1] if p[1] is not None else []



def p_if_condition(p):
    '''if_condition : expression if_condition_tail'''

    if p [1][0].lower() != 'boolean':
        raise TypeError(f"Tipo de dado inválido para condição: {p[1][0]} (esperado = boolean)")
    if p[2] is not None:
        if p[2][0].lower() != 'boolean':
            raise TypeError(f"Tipo de dado inválido para condição: {p[2][0]} (esperado = boolean)")

    type1, code1 = p[1]
    type2, code2 = p[2] if p[2] is not None else (None, [])

    if len(p) == 3:
        p[0] = (type1, code1 + code2)

    else:
        p[0] = p[1]
    
    

def p_if_condition_tail(p):
    '''if_condition_tail : OR if_condition_tail_2
                         | if_condition_tail_2'''
    if len(p) == 3:                            
        type1, code1 = p[2]
        if type1.lower() != 'boolean':
            raise TypeError("OR only allowed for booleans")
        p[0] = ('boolean', code1 + ["     OR\n"])
    else:
        p[0] = p[1]

def p_if_condition_tail_2(p):
    '''if_condition_tail_2 : AND if_condition
                           | empty'''
    if len(p) == 3:                            
        type1, code1 = p[2]
        if type1.lower() != 'boolean':
            raise TypeError("OR only allowed for booleans")
        p[0] = ('boolean', code1 + ["     AND\n"])
    else:
        p[0] = p[1]


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

                if type == 'array':
                    
                    commands, element_type = linhas_calculo
                    p[0] += commands
                    p[0] += [f"     LOADN\n"]
                    if element_type.lower() == 'integer' :      
                        p[0] += ["       STRI\n"]
                    elif element_type.lower() == 'real':
                        p[0] += ["       STRF\n"]
                    elif element_type.lower() == 'boolean':
                        p[0] += ["       WRITEI\n"]
                
                else:
                    if type.lower() == 'integer' :      
                        p[0] += linhas_calculo + ["       STRI\n"]
                    elif type.lower() == 'real':
                        p[0] += linhas_calculo + ["       STRF\n"]
                    elif type.lower() == 'boolean':
                        p[0] += linhas_calculo + ["       WRITEI\n"]
            
        if not first_iteration:
            p[0] += ["     CONCAT\n"]
        else:
            first_iteration = False
    
    p[0] += ["     WRITES\n"]


def p_readln_statement(p):
    'readln_statement : LPAREN string_statement RPAREN'
    p[0] = []
    for arg in p[2]:
        argtype, code = arg

        if (argtype == 'array'):
            commands, tipo_elemento = code
            global index
            p[0] += commands
            p[0] += ["     READ\n"]
            if tipo_elemento == 'integer' or tipo_elemento == 'boolean':     
                p[0] += ["      ATOI\n"]
            elif tipo_elemento == 'real':
                p[0] += ["      ATOF\n"]

            p[0] += ["      STOREN\n"]
            

        else:
            match = re.search(r'LOAD\s+(-?\d+)', code[0])
            if match:
                global index
                profundidade = int(match.group(1)) + index
                p[0] += ["     READ\n      DUP 1\n"]
                if argtype == 'integer' or argtype == 'boolean':     
                    p[0] += ["      ATOI\n"]
                elif argtype == 'real':
                    p[0] += ["      ATOF\n"]
                p[0] += ["      STOREG " + str(profundidade) + "\n       WRITES WRITELN\n"]


def p_string_statement(p):
    '''string_statement : assign_expression
                        | assign_expression COMMA string_statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_assign_expression(p):
    '''assign_expression : expression
                         | STRING ''' 
    p[0] = p[1]


##################################### expression (aritmetrica e booleana) ##########################################

def p_expression(p):
    '''expression : expression OR and_expression
                  | and_expression'''
    if len(p) == 4:                             ## OR... (X AND Y) OR (X AND Y) ou (AND... AND X AND Y AND Z) ou (X) 
        # Combine left and right with OR
        type1, code1 = p[1]
        type2, code2 = p[3]
        if type1.lower() != 'boolean' or type2.lower() != 'boolean':
            raise TypeError("OR only allowed for booleans")
        p[0] = ('boolean', code1 + code2 + ["     OR\n"])
    else:
        p[0] = p[1]

def p_and_expression(p):                                            ## (AND... AND X AND Y AND Z) ou (X) 
    '''and_expression : and_expression AND relation_expression          
                      | relation_expression'''
    if len(p) == 4:
        type1, code1 = p[1]
        type2, code2 = p[3]
        if type1.lower() != 'boolean' or type2.lower() != 'boolean':
            raise TypeError("AND only allowed for booleans")
        p[0] = ('boolean', code1 + code2 + ["     AND\n"])
    else:
        p[0] = p[1]

def p_relation_expression(p):                                               ## (X) => (10 + 20) || (10 < (20 + 10)) etc.
    '''relation_expression : simple_expression expression_tail'''
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


        # verificar
        elif type.lower() == "array":
            array_data = p[2][1]
            commands, element_type = array_data

            code = commands
            code += ["      LOADN\n"] 

            if element_type.lower() == "integer":
                if p[1] == '+':
                    code += ["     ADD\n"]
                else:
                    code = ["     SUB\n"]

            elif element_type.lower() == "real":
                if p[1] == '+':
                    code = ["     FADD\n"]
                else:
                    code = ["     FSUB\n"]
            
            type = element_type.lower()       
        

        if p[3] is not None:
            if type.lower() != p[3][0].lower():
                raise TypeError(f"Tipo de dado inválido para soma: {type} + {p[3][0]}")
            code += p[3][1]
        p[0] = (type, code)


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
                 | MOD factor term_tail
                 | REAL_DIVIDE factor term_tail
                 | empty'''
    if len(p) == 4:
        type = p[2][0]          ## so tem divisao e multiplicacao para inteiros  ; pascal : "*"" e "div" 
                                ##TODO // falta mod 
        
        if type.lower() == "integer":
            if p[1] == '*':
                code = p[2][1] + ["     MUL\n"]
            elif p[1].lower() == 'mod':
                code = p[2][1] + ["     MOD\n"]
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
              | IDENTIFIER
              | IDENTIFIER LBRACKET expression RBRACKET
              | TRUE
              | FALSE'''
    
    global variaveis, index
    print(p[1])
    if len(p) == 5 and p.slice[1].type == 'IDENTIFIER' and p[3][0].lower() == 'integer':
        var = variaveis.get(p[1])
        if var is None or var[0] != 'array':
            raise NameError(f'Variável não declarada ou não é array: {p[1]}')
        
        menor, maior, tamanho, struct_index, tipo_elemento = var[1]

        tipo_indice, commands_indice = p[3]

        if tipo_indice.lower() != 'integer':
            raise TypeError("Índice de array deve ser inteiro")

        commands = []
        commands += [f'      PUSHST {struct_index}\n']
        commands += commands_indice
        commands += ['      PUSHI 1\n       SUB\n']

        p[0] = ('array', (commands, tipo_elemento))

    elif len(p) == 4:
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
            if variaveis.get(p[1]) is not None:  ##TODO nao suporta varaiveis dentro de arrays
                tipo, index_var = variaveis[p[1]]
                profundidade = index_var - index
                p[0] = (tipo, ["     PUSHFP\n       LOAD " + str(profundidade) + "\n"])
        elif p.slice[1].type == 'TRUE':
            p[0] = ('boolean', ["     PUSHI 1\n"])
        elif p.slice[1].type == 'FALSE':
            p[0] = ('boolean', ["     PUSHI 0\n"])






def p_error(p):
    if not p:
        raise Exception("Erro sintático: fim inesperado do arquivo (possível bloco incompleto ou END. faltando)")
        return
    
    statement_starters = {'IDENTIFIER', 'IF', 'WRITE', 'WRITELN', 'READLN', 'FOR', 'WHILE'}
    
    if p.type in statement_starters:
        raise Exception(f"Erro sintático possivelmente devido à falta de ponto e vírgula antes da linha {p.lineno}: token inesperado '{p.value}' ({p.type})")
    else:
        raise Exception(f"Erro sintático na linha {p.lineno}: token inesperado '{p.value}' ({p.type})")

def p_empty(p):
    'empty :'
    p[0] = None

def reset_variaveis():
    global variaveis, index, numero_ciclos_if , numero_ciclos_for, numero_ciclos_while, index_variavel_ciclo_for, tipo_ciclo_for
    variaveis = {} 
    index = 0 
    numero_ciclos_if = 0 
    numero_ciclos_for = 0 
    numero_ciclos_while = 0 
    index_variavel_ciclo_for = {} 
    tipo_ciclo_for = {} 
    

parser = yacc.yacc(debug=True)

folder_path = 'programas_pascal'
limite_ficheiros = 5
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
