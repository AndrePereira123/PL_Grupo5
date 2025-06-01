import os
import re
import sys
from lex import tokens
import ply.yacc as yacc

STRING_MAX_SIZE = 256

variaveis = {} ## chave : nome da variavel, valor : (tipo da variavel,index)
label_index = 0 # index da label de forma a ter nome único
index = 0 ## index na maquina virtual
struct_index = 0 # index das estruturas
numero_ciclos_if = 0 ## numero de ciclos ifs 
numero_ciclos_for = 0 ## numero de ciclos fors 
numero_ciclos_while = 0 ## numero de ciclos whiles
index_variavel_ciclo_for = {} ## profundidade da variavel do ciclo for
tipo_ciclo_for = {} ## tipo de ciclo (downto ou to )
 


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
            for i in range(tamanho):
                p[0] += [
                    f"     PUSHST {struct_index - 1}\n",
                    f"     PUSHI {i}\n",
                    f"     PUSHI 0\n",
                    "     STOREN\n"
                ]

        elif p[3].lower() == 'string':
            menor, maior = 1, STRING_MAX_SIZE
            elements_type = 'char'
            variaveis[var] = ('string', (menor, maior, STRING_MAX_SIZE, struct_index, elements_type))
            struct_index += 1
            index += 1

            p[0] += [f"     ALLOC {STRING_MAX_SIZE}\n"]
            
        else:
            variaveis[var] = (p[3].lower(),index) ## registar no dicionario cada variavel 
            index += 1 
            p[3] = p[3].lower()
            if p[3] == 'integer' or p[3] == 'boolean':
                p[0] += ["     PUSHI 0\n"]

            elif p[3] == 'real':
                p[0] += ["     PUSHF 0.0\n"]

    
    

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
    if p[2] is not None:
        p[0] = ["START\n"] + p[2] + ["STOP\n"]
    else:
        p[0] = ["START\n", "STOP\n"]
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
    '''statement : open_statement
                 | closed_statement'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = []

def p_open_statement(p):
    '''open_statement : IF if_condition THEN code_or_statement
                      | IF if_condition THEN code_or_statement ELSE open_statement
                      | WHILE if_condition DO open_statement
                      | FOR for_condition DO open_statement '''
    if p[1].lower() == 'if':
        global numero_ciclos_if
        type1, code1 = p[2]
        if type1.lower() != 'boolean':  
            raise TypeError("Condição do IF tem de ser boolean")
        
        if len(p) == 5:  # IF condition THEN statement (sem else)
            code = code1 + [f"JZ ENDIF{numero_ciclos_if}\n"]
            code += p[4] if p[4] is not None else []
            code += [f"ENDIF{numero_ciclos_if}:\n"]

        else:  # IF condition THEN statement ELSE statement
            code = code1 + [f"JZ ELSE{numero_ciclos_if}\n"]
            code += p[4] if p[4] is not None else []
            code += [f"JUMP ENDIF{numero_ciclos_if}\n"]
            code += [f"ELSE{numero_ciclos_if}:\n"]
            code += p[6] if p[6] is not None else []
            code += [f"ENDIF{numero_ciclos_if}:\n"]
        
        numero_ciclos_if += 1
        p[0] = code

    elif p[1].lower() == 'while':
        type1, code1 = p[2]
        if type1.lower() != 'boolean':
            raise TypeError("Condição do WHILE tem de ser boolean")
        
        code = [f"WHILESTART{numero_ciclos_while}:\n"]
        code += code1
        code += [f"JZ WHILEEND{numero_ciclos_while}\n"]
        code += p[4] if p[4] is not None else []  # Código do corpo
        code += [f"JUMP WHILESTART{numero_ciclos_while}\n"]
        code += [f"WHILEEND{numero_ciclos_while}:\n"]
        
        numero_ciclos_while += 1
        p[0] = code
        
    elif p[1].lower() == 'for':
        global numero_ciclos_for, index_variavel_ciclo_for , index
        type1, code1 = p[2]
        
        code = code1 + ["JZ FOREND" + str(numero_ciclos_for) + "\n"] + p[4] if p[4] is not None else [] ## codigo do for

        distancia = index_variavel_ciclo_for[numero_ciclos_for]
        profundidade = distancia + index
        code += ["     PUSHFP\n     LOAD" + str(distancia) + f"\n     PUSHI {tipo_ciclo_for[numero_ciclos_for]}1\n     ADD\n     STOREG " + str(profundidade) + "\n"]
        code += ["     JUMP FORSTART" + str(numero_ciclos_for) + "\n"] + ["FOREND" + str(numero_ciclos_for) + ":\n"]
        
        
        numero_ciclos_for += 1
        p[0] = code



def p_closed_statement(p):
    '''closed_statement : IDENTIFIER identifier_assign_expression  
                | WRITELN write_statement 
                | WRITE write_statement 
                | READLN readln_statement 
                | IF if_condition THEN code_or_statement ELSE code_or_statement
                | FOR for_condition DO code_or_statement
                | WHILE if_condition DO code_or_statement''' 
    
    if (p.slice[1].type == 'IDENTIFIER'):
        global variaveis, index
        if variaveis.get(p[1]) is not None:
            tipo_guardado, index_var = variaveis[p[1]]  
        else:
            raise NameError(f"Variável não declarada: {p[1]}")
        
        type, expression = p[2]
        # binding de arrays
        if (type == 'array'):
            menor, maior, tamanho, struct_index, elements_type = index_var
            actual_type, commands = expression

            if (elements_type.lower() == actual_type.lower()):
                commands_to_output = []
                commands_to_output += [f'     PUSHST {struct_index}\n']
                commands_to_output += commands
                commands_to_output += ['     STOREN\n']

                p[0] = commands_to_output
            
            else:
                raise NameError(f"Variável do tipo: {actual_type.lower()}. Deveria ser do tipo {elements_type}")

        # binding de variaveis
        else:
            if tipo_guardado == 'string':  ## se for string => simples atribuição
                (menor, maior, tamanho, struct_index, elements_type) = index_var
                (actual_type, tail) = p[2]
                if (tipo_guardado != actual_type.lower()):
                    raise TypeError(f'A atribuição não é válida. Não podes atribuir {actual_type} a {tipo_guardado}')
                
                (commands, actual_size) = tail
                
                if (actual_type.lower() == tipo_guardado):
                    commands_to_output = []
                    for i,c in enumerate(commands):
                        commands_to_output += [f'     PUSHST {struct_index}\n     PUSHI {i+1}\n',
                                    c,
                                    f'     STOREN\n']
                        
                    
                    commands_to_output += [f'       PUSHST {struct_index}\n     PUSHI 0\n     PUSHI {len(commands)}\n       STOREN\n']


                    # atualizar tamanho    
                    index_var = (menor, maior, actual_size, struct_index, elements_type)
                    variaveis[p[1]] = tipo_guardado, index_var

                    p[0] = commands_to_output
                    
                else:
                    raise TypeError('Variável inválida')

            else:
                type, linhas_calculo = p[2]   ## (INTEGER/REAL/...,valor)

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

    elif p[1].lower() == 'if' :
        global numero_ciclos_if
        type1, code1 = p[2]
        
        code = code1 + ["JZ ELSE" + str(numero_ciclos_if) + "\n"]


        code += p[4] if p[4] is not None else [] ## codigo do if
        codigo_else = p[6] if p[6] is not None else []
        code += ["     JUMP ENDIF" + str(numero_ciclos_if) + "\n"] + ["ELSE" + str(numero_ciclos_if) + ":\n"] + codigo_else + ["ENDIF" + str(numero_ciclos_if) + ":\n"]
        
        
        numero_ciclos_if += 1
        p[0] = code

    elif p[1].lower() == 'for':
        global numero_ciclos_for, index_variavel_ciclo_for , index
        type1, code1 = p[2]
        
        code = code1 + ["JZ FOREND" + str(numero_ciclos_for) + "\n"] + p[4] if p[4] is not None else [] ## codigo do for


        distancia = index_variavel_ciclo_for[numero_ciclos_for]
        profundidade = distancia + index
        code += ["     PUSHFP\n     LOAD" + str(distancia) + f"\n     PUSHI {tipo_ciclo_for[numero_ciclos_for]}1\n     ADD\n     STOREG " + str(profundidade) + "\n"]
        code += ["     JUMP FORSTART" + str(numero_ciclos_for) + "\n"] + ["FOREND" + str(numero_ciclos_for) + ":\n"]
        
        
        numero_ciclos_for += 1
        p[0] = code

    elif p[1].lower() == 'while':
        global numero_ciclos_while
        type1, code1 = p[2]
        if type1.lower() != 'boolean':
            raise TypeError("Condição do WHILE tem de ser boolean")
        
        code = [f"WHILESTART{numero_ciclos_while}:\n"]
        code += code1
        code += [f"JZ WHILEEND{numero_ciclos_while}\n"]
        code += p[4] if p[4] is not None else []  # Código do corpo
        code += [f"JUMP WHILESTART{numero_ciclos_while}\n"]
        code += [f"WHILEEND{numero_ciclos_while}:\n"]
        
        numero_ciclos_while += 1
        p[0] = code

    elif p[1].lower() == 'writeln':
        p[0] = p[2] + ["       WRITELN\n"]
    else:
        p[0] = p[2]    

def p_identifier_assign_expression(p):
    '''identifier_assign_expression : ASSIGN expression  
                                    | LBRACKET simple_expression RBRACKET ASSIGN expression
    '''
    if p[1] == ":=":  
        if (p[2][0].lower() == 'string_pure'):            
            commands = []
            string_val = p[2][1]
            for i, c in enumerate(string_val[:STRING_MAX_SIZE]):
                commands += [f'     PUSHI {ord(c)}\n']

            # atualizar tamanho    
            tamanho = len(string_val)
            p[0] = ('string', (commands, tamanho))

        else:
            type, linhas_calculo = p[2]   ## (INTEGER/REAL/...,valor)
            p[0] = p[2]

    elif len(p) == 6 and p[1] == "[" and p[3] == "]" and p[4] == ":=":
            # ('array', (menor, maior, tamanho, struct_index))

            actual_type, command = p[5]
            
            if p[2][0].lower() != 'integer':
                raise TypeError('O índice precisa de ser um valor inteiro')

            commands = []
            commands += p[2][1]
            commands += [f'     PUSHI 1\n     SUB\n'] # por causa dos indices
            commands += command

            # inserir o valor que queremos dar bind
            p[0] = ('array', (actual_type, commands))               

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

def p_code_or_statement(p):
    '''code_or_statement : dotless_code
                         | closed_statement'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = []

def p_if_condition(p):
    '''if_condition : expression'''

    if p [1][0].lower() != 'boolean':
        raise TypeError(f"Tipo de dado inválido para condição: {p[1][0]} (esperado = boolean)")

    type1, code1 = p[1]

    if len(p) == 3:
        p[0] = (type1, code1)

    else:
        p[0] = p[1]
    
    



def p_write_statement(p):                               
    'write_statement : LPAREN string_statement RPAREN'
    p[0] = []
    first_iteration = True
    for arg in p[2]:
        check = False
        expressao_ou_string = arg

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

        # string guardada
        elif type.lower() == 'string':
            global variaveis, label_index
            tipo_guardado, (menor, maior, tamanho, struct_index, elements_type) = variaveis[linhas_calculo]
            label_start = f"STR{label_index}PRINTSTART"
            label_end = f"STR{label_index}PRINTEND"
            label_index += 1

            p[0] += [
                f"     PUSHST {struct_index}\n", 
                "     DUP 1\n",
                "     PUSHI 0\n",
                "     LOADN\n",                 
                "     STOREL 0\n",    
                "     PUSHI 0\n",           
                "     STOREL 1\n",          

                f"{label_start}:\n",
                "     PUSHL 1\n",                
                "     PUSHL 0\n",            
                "     INF\n",                   
                f"     JZ {label_end}\n",

                f"     PUSHST {struct_index}\n",
                "     PUSHL 1\n",                
                "     PUSHI 1\n",
                "     ADD\n",              
                "     LOADN\n",         
                "     WRITECHR\n",

                "     PUSHL 1\n",
                "     PUSHI 1\n",
                "     ADD\n",
                "     STOREL 1\n",
                f"     JUMP {label_start}\n",
                f"{label_end}:\n",
                "           POP 2\n"
            ]

            
            check = True

        # char de uma string
        elif type.lower() == 'char':
            linhas_calculo += ["        WRITECHR\n"]
            p[0] = linhas_calculo
            check = True

        # string "real"
        elif type.lower() == 'string_pure':
            p[0] += ["     PUSHS \"" + linhas_calculo + "\"\n"]
        
        else:
            if type.lower() == 'integer' :      
                p[0] += linhas_calculo + ["       STRI\n"]
            elif type.lower() == 'real':
                p[0] += linhas_calculo + ["       STRF\n"]
            elif type.lower() == 'boolean':
                p[0] += linhas_calculo + ["       WRITEI\n"]
                check = True
            
        if not check:
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

        elif (argtype == 'string'):
            global variaveis, label_index
            tipo_guardado, (menor, maior, tamanho, struct_index, elements_type) = variaveis[code]
            label_start = f"STR{label_index}START"
            label_end = f"STR{label_index}END"
            label_index += 1
            # Lê a string e duplica o endereço
            p[0] += [
                "     READ\n",              
                "     DUP 1\n",            
                "     STRLEN\n",            
                f"     DUP 2\n",
                f"     PUSHST {struct_index}\n",
                "     SWAP\n",
                "     PUSHI 0\n",
                "     SWAP\n",
                "     STOREN\n"  
                 "     PUSHI 256\n",
                 "     INF\n",               
                f"     JZ {label_end}\n",   
                f"     PUSHI 0\n",           
                f"{label_start}:\n",
                "     DUP 1\n",             
                f"     PUSHST {struct_index}\n",          
                "     PUSHL 0\n",           
                "     PUSHL 2\n",
                "     CHARAT\n", 
                "     PUSHL 2\n",
                "     PUSHI 1\n",
                "     ADD\n",         
                "     SWAP\n",              
                "     STOREN\n",
                "     PUSHI 1\n",
                "     ADD\n",               
                "     DUP 1\n",
                "     STOREL 2\n",
                "     PUSHL 1\n", 
                "     INF\n",               
                f"     JZ {label_end}\n",  
                f"     JUMP {label_start}\n",
                f"{label_end}:\n",
                "     POP 3\n"              
            ]
            

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
    '''string_statement : expression
                        | expression COMMA string_statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]



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
    '''relation_expression : simple_expression expression_tail
                           | NOT simple_expression expression_tail'''
    if len(p) == 3 and p[2] is None:
        p[0] = p[1]
    elif len(p) == 4 and p[3] is None :
        type1, code1 = p[2]
        if type1.lower() != 'boolean':
            raise TypeError("NOT only allowed for booleans")
        p[0] = ('boolean', code1 + ["     NOT\n"])
    else:

        i = 1 if len(p) == 4 else 0

        op, type2, code2 = p[2 + i]
        type1, code1 = p[1 + i]
        
        if type1.lower() == type2.lower():
            pass
        elif type1.lower() == 'char' and type2.lower() == 'string_pure': # para suportar bin[i] = '1'
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

        if type1.lower() != 'char':
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
        else:
            if type2.lower() == 'string_pure':
                if len(code2) == 1: # só funciona para comparar elementos de uma string
                    code2 = [f"      PUSHS \"{p[2 + i][2]}\"\n     CHRCODE\n"]
                else:
                    raise TypeError(f"O compilador não suportar comprar char com strings")
                
                instr = {
                    '<': 'INF',
                    '>': 'SUP',
                    '<=': 'INFEQ',
                    '>=': 'SUPEQ',
                    '<>': 'EQUAL\n      NOT',
                    '=': 'EQUAL'
                }[op]
            else:
                raise TypeError(f"O compilador não suporta comparar {type1} com {type2}.")

        
        code = code1 + code2 + [f"     {instr}\n"]
        if p[1] == 'NOT':
             code = code + ["     NOT\n"]

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
              | IDENTIFIER identifier_expression
              | IDENTIFIER length_expression
              | TRUE
              | STRING
              | FALSE'''
    
    global variaveis, index
    if len(p) == 3 and p.slice[1].type == 'IDENTIFIER' and p[1] != 'length':
        if p[2] is not None:

            tipo, (menor, maior, tamanho, struct_index, elements_type) = variaveis[p[1]]

            if tipo != 'array' and tipo != 'string':
                raise TypeError(f'A variável {p[1]} deveria ser um array ou uma string.')


            commands = []
            commands += [f'     PUSHST {struct_index}\n']
            commands += p[2][1][0]

            if tipo == 'string':
                p[0] = ('char', commands + ['     LOADN\n'])
            else:
                commands += ['     PUSHI 1\n', '     SUB\n']
                p[0] = ('array', (commands, elements_type))

        else: # não é array
            if variaveis.get(p[1]) is not None:
                tipo, index_var = variaveis[p[1]]
                if tipo == 'string':
                    p[0] = ('string', p[1])
                else:
                    profundidade = index_var - index
                    p[0] = (tipo, ["     PUSHFP\n       LOAD " + str(profundidade) + "\n"])
            elif p.slice[1].type == 'TRUE':
                p[0] = ('boolean', ["     PUSHI 1\n"])
            elif p.slice[1].type == 'FALSE':
                p[0] = ('boolean', ["     PUSHI 0\n"])
    elif len(p) == 3 and p.slice[1].type == 'IDENTIFIER' and p[1] == 'length':
        p[0] = p[2]
    
    elif p.slice[1].type == 'STRING':
        p[0] = ('string_pure', p[1])
        """ if len(p[1]) == 1: # só funciona para comparar elementos de uma string
            p[0] = ('char', [f"      PUSHS \"{p[1]}\"\n     CHRCODE\n"])
        else:
            p[0] = ('string_pure', [f"      PUSHS \"{p[1]}\"\n"]) """

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

def p_length_expression(p):
    '''length_expression : LPAREN IDENTIFIER RPAREN'''
    
    var_name = p[2]


    if variaveis.get(var_name) is not None:
        tipo, dados = variaveis[var_name]
        
        if tipo == 'string':
            menor, maior, tamanho, struct_index, elements_type = dados
            commands = [
                f'     PUSHST {struct_index}\n',
                '     PUSHI 0\n',
                '     LOADN\n'
            ]
            p[0] = ('integer', commands)
        elif tipo == 'array':
            menor, maior, tamanho, struct_index, elements_type = dados
            commands = [
                f'     PUSHI {tamanho}\n'  # Tamanho fixo do array
            ]
            p[0] = ('integer', commands)
        else:
            raise TypeError(f'length() só funciona com strings ou arrays, mas {var_name} é {tipo}')
    else:
        raise NameError(f"Variável não declarada: {var_name}")



def p_identifier_expression(p):
    '''
    identifier_expression : LBRACKET expression RBRACKET
                          | empty
    '''
    global variaveis, index
    if p[1] is not None:
        if len(p) == 4 and p[2][0].lower() == 'integer':            
            tipo_indice, commands_indice = p[2]
            
            if tipo_indice.lower() != 'integer':
                raise TypeError("Índice de array deve ser inteiro")

            p[0] = ('access', (commands_indice, p[2][0].lower()))
    else:
        p[0] = None



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
    global variaveis, index, numero_ciclos_if , numero_ciclos_for, numero_ciclos_while, index_variavel_ciclo_for, tipo_ciclo_for, struct_index, label_index
    variaveis = {} 
    index = 0 
    numero_ciclos_if = 0 
    numero_ciclos_for = 0 
    numero_ciclos_while = 0 
    label_index = 0
    index_variavel_ciclo_for = {} 
    tipo_ciclo_for = {} 
    struct_index = 0
    

parser = yacc.yacc(debug=True)

if len(sys.argv) == 1:  # Nenhum argumento fornecido
    folder_path = 'programas_pascal'
    limite_ficheiros = 7
    ficheiro = 0
    for file_name in os.listdir(folder_path):
        if ficheiro < limite_ficheiros:
            if file_name.endswith('.pas'):
                with open(os.path.join(folder_path, file_name), 'r', encoding='utf-8') as file:
                    reset_variaveis()  # Para garantir que cada ficheiro tem o seu próprio dicionário de variáveis
                    data = file.read()
                    val = parser.parse(data)
                    with open(f'programas_gerados/{file_name}', 'w') as output_file:
                        for linha in val:
                            output_file.write(f"{linha}")
            ficheiro += 1
            
elif len(sys.argv) == 2:  # Um argumento fornecido (caminho do arquivo)
    file_path = sys.argv[1]
    if file_path.endswith('.pas'):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reset_variaveis()
                data = file.read()
                val = parser.parse(data)
                
                base_name = os.path.basename(file_path)
                output_path = f'programas_gerados/{base_name}'
                
                with open(output_path, 'w') as output_file:
                    for linha in val:
                        output_file.write(f"{linha}")
                        
                print(f"Arquivo compilado: {file_path} -> {output_path}")
                
        except FileNotFoundError:
            print(f"Erro: Arquivo não encontrado: {file_path}")
        except Exception as e:
            print(f"Erro ao processar arquivo {file_path}: {e}")
    else:
        print("Erro: O arquivo deve ter extensão .pas")
        
