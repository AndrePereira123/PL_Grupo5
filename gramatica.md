program HelloWorld;
begin
    writeln('Ola, Mundo!');
end.

LL(1) - Transformed Grammar


file : name vars program

name : IDENTIFIER SEMICOLON

vars : VAR varstail
     | 

varstail : vardecl varstail
         | 

vardecl : idlist COLON type SEMICOLON

idlist : IDENTIFIER idlistTail

idlistTail : COMMA idlist
           | 

type : INTEGER
     | TYPE_REAL
     | BOOLEAN
     | STRING
     | ARRAY LBRACKET NUMBER RBRACKET OF type

program : BEGIN expressions END

expressions : statement expressions
            | 

statement : WRITELN writeln_statement SEMICOLON
          | WRITE write_statement SEMICOLON
          | READLN
          | READ
          | IF 
          | FOR 
          | WHILE


gramatica para write(s)-------------------

tipos suportados:
Strings (e.g., writeln('Hello');)
Numbers (e.g., writeln(42);)
Variables (e.g., writeln(a);)
Expressions (e.g., writeln(1 + 2);)
Multiple values separated by commas (e.g., writeln('Sum:', 1 + 2);)


writeln_statement : LPAREN string_statement RPAREN

write_statement : LPAREN string_statement RPAREN


string_statement : string_argument
                 | string_argument COMMA string_statement

string_argument : STRING
                | IDENTIFIER  
                | NUMBER
                | expression

-------------------------------------------------------






