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
    print(f"File: {p[0]}")

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
            p[0] += ["     PUSHF 0\n"]

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
    print(f"Code: {p[0]}")

def p_expressions(p):
    '''expressions : statement expressions
                   | empty'''
    if len(p) == 3:
        if p[2] is not None:
            p[0] = p[1] + p[2]
        else:
            p[0] = p[1]
    else:
        p[0] = p[1] 


#################################### statements ##########################################

def p_statement(p):
    '''statement : IDENTIFIER ASSIGN assign_expression SEMICOLON 
                | WRITELN writeln_statement SEMICOLON
                | WRITE write_statement SEMICOLON
                | READLN 
                | READ 
                | IF            
                | FOR 
                | WHILE ''' ## TODO implementar os outros statements
    if len(p) == 5:
        type, var = p[3]
        global variaveis, index, nivel_apontador
        if variaveis.get(p[1]) is not None:  ##TODO nao suporta varaiveis dentro de arrays
            tipo, index_var = variaveis[p[1]]   
        if type.lower() != tipo:
            raise TypeError(f"Tipo de dado inválido para atribuição: {tipo} para {p[1]}")   
        if tipo == 'integer' :      
            p[0] = ["     PUSHI " + str(var) + "\n"] + ["       STOREG " + str(index_var) + "\n"]
        elif tipo == 'real':
            p[0] = ["     PUSHF " + str(var) + "\n"] + ["       STOREG " + str(index_var) + "\n"]
        elif tipo == 'string':
            p[0] = ["     PUSHS \"" + str(var) + "\"\n"] + ["       STOREG " + str(index_var) + "\n"]
        elif tipo == 'boolean':
            ##TODO ajustar boleano para ser TRUE/FALSE
            pass
    else:
        p[0] = p[2]    



def p_writeln_statement(p):
    'writeln_statement : LPAREN string_statement RPAREN'
    p[0] = []
    first_iteration = True
    for arg in reversed(p[2]):
        argtype = arg[0]
        print(f"Argument: {arg}")
        print(f"Argument type: {argtype}")

        if argtype == 'STRING':
            p[0] += ["     PUSHS \"" + arg[1] + "\"\n"]
        
        elif argtype == 'IDENTIFIER':
            global variaveis, index
            if variaveis.get(arg[1]) is not None:  ##TODO nao suporta varaiveis dentro de arrays
                tipo, index_var = variaveis[arg[1]]
                profundidade = index_var - index
                p[0] += ["     PUSHFP\n       LOAD " + str(profundidade) + "\n"]
                if tipo == 'integer' or tipo == 'boolean':      ##TODO ajustar boleano para ser TRUE/FALSE
                    p[0] += ["       STRI\n"]
                elif tipo == 'real':
                    p[0] += ["       STRF\n"]
                    
        elif argtype == 'INTEGER': ## TODO verificar ints ou reais
            p[0] += ["     PUSHI " + str(arg[1]) + "\n       STRI\n"]
        elif argtype == 'REAL':
            p[0] += ["     PUSHF " + str(arg[1]) + "\n       STRF\n"]
        elif argtype == 'expression':
            p[0] += p[2]    
        
        if not first_iteration:
            p[0] += ["     CONCAT\n"]
        else:
            first_iteration = False
    
    p[0] += ["     WRITES\n       WRITELN\n"]

def p_write_statement(p):
    'write_statement : LPAREN string_statement RPAREN'
    p[0] = p[2]

def p_string_statement(p):
    '''string_statement : assign_expression
                        | assign_expression COMMA string_statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_assign_expression(p):
    '''assign_expression : INTEGER
                         | REAL
                         | IDENTIFIER       
                         | STRING
                         | expression ''' ## TODO implementar expression e identifier
    p[0] = (p.slice[1].type, p[1])

def p_expression(p):
    '''expression : empty'''
    p[0] = p[1]


##################################### assign_variable ##########################################



def p_error(p):
    print("Erro sintático no input!")

def p_empty(p):
    'empty :'
    p[0] = None

parser = yacc.yacc(debug=True)

with open('programas_pascal/hello_world.pas', 'r') as file:
    data = file.read()
    val = parser.parse(data)
    with open('output.txt', 'w') as output_file:
        for linha in val:
            output_file.write(f"{linha}")
