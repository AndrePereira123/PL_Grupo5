# Gramática Pascal - PL 2025 - Grupo 5

## Regras de Produção

### **Estrutura Principal**
```
file → PROGRAM name vars code

name → IDENTIFIER SEMICOLON
```

### **Declaração de Variáveis**
```
vars → VAR varstail
     | empty

varstail → vardecl varstail
         | empty

vardecl → idlist COLON type SEMICOLON

idlist → IDENTIFIER idlistTail

idlistTail → COMMA IDENTIFIER idlistTail
           | empty
```

### **Tipos de Dados**
```
type → TYPE_INTEGER
     | TYPE_REAL
     | BOOLEAN
     | TYPE_STRING
     | ARRAY LBRACKET arraytypes RBRACKET OF type

arraytypes → INTEGER
           | INTEGER DOT DOT INTEGER
```

### **Estrutura do Programa**
```
code → BEGIN expressions END_DOT

dotless_code → BEGIN expressions END

expressions → statement expressions_tail
            | empty

expressions_tail → SEMICOLON expressions
                 | empty
```

### **Statements (Solução Dangling Else)**
```
statement → open_statement
          | closed_statement

open_statement → IF if_condition THEN code_or_statement
               | IF if_condition THEN code_or_statement ELSE open_statement 
               | WHILE if_condition DO open_statement
               | FOR for_condition DO open_statement

closed_statement → IDENTIFIER identifier_assign_expression
                 | WRITELN write_statement
                 | WRITE write_statement
                 | READLN readln_statement
                 | IF if_condition THEN code_or_statement ELSE code_or_statement
                 | FOR for_condition DO code_or_statement
                 | WHILE if_condition DO code_or_statement
```

### **Atribuições e Condições**
```
identifier_assign_expression → ASSIGN expression
                             | LBRACKET simple_expression RBRACKET ASSIGN expression

for_condition → expression ASSIGN expression to_expression

to_expression → TO expression
              | DOWNTO expression

code_or_statement → dotless_code
                  | closed_statement

if_condition → expression
```

### **I/O Statements**
```
write_statement → LPAREN string_statement RPAREN

readln_statement → LPAREN string_statement RPAREN

string_statement → expression
                 | expression COMMA string_statement
```

### **Expressões Booleanas e Aritméticas**
```
expression → expression OR and_expression
           | and_expression

and_expression → and_expression AND relation_expression
               | relation_expression

relation_expression → simple_expression expression_tail
                    | NOT simple_expression expression_tail

expression_tail → LT simple_expression
                | GT simple_expression
                | LE simple_expression
                | GE simple_expression
                | NE simple_expression
                | EQUAL simple_expression
                | empty
```

### **Expressões Aritméticas**
```
simple_expression → term simple_expression_tail

simple_expression_tail → PLUS term simple_expression_tail
                       | MINUS term simple_expression_tail
                       | empty

term → factor term_tail

term_tail → TIMES factor term_tail
          | DIVIDE factor term_tail
          | MOD factor term_tail
          | REAL_DIVIDE factor term_tail
          | empty
```

### **Fatores**
```
factor → PLUS factor
       | MINUS factor
       | LPAREN expression RPAREN
       | INTEGER
       | REAL
       | IDENTIFIER identifier_expression
       | IDENTIFIER length_expression
       | TRUE
       | STRING
       | FALSE
```

### **Acesso a Arrays e funçao length**
```
length_expression → LPAREN IDENTIFIER RPAREN

identifier_expression → LBRACKET expression RBRACKET
                      | empty
```

### **Regra Vazia**
```
empty → ε
```

Esta gramática implementa uma versão simplificada do Pascal.