# Trabalho Prático - Relatório  
**Processamento de Linguagens**  
**(3º ano - LEI)**

**Andre Pereira - A104275**
**Leonardo Alves - A104093** 

*31 de Maio de 2025*

---
## Resumo

Este relatório tem como proposito a exposicao do processo de desenvolvimento de um compilador para uma versão simplificada da linguagem Pascal, focado na traduçao do código escrito em pascal para codigo "maquina" que seja funcional na virtual machine EWVM (https://ewvm.epl.di.uminho.pt). Os resultados demonstram a eliminação completa dos conflitos shift/reduce e reduce/reduce, garantindo uma análise sintática determinística e geração correta de código para estruturas condicionais e iterativas.

---

# Introdução

No âmbito da disciplina de Processamento de Linguagens, fomos desafiados a desenvolver um compilador para Pascal Standard, fazendo a sua tradução para código máquina da EWVM. Perante isto, para a geração de código máquina, seguimos uma tradução dirigida pela sintaxe, onde o código Pascal é automaticamente convertido em código da VM.

Para a análise léxica e sintática, recorremos ao PLY, que foi a biblioteca utilizada ao longo do semestre na aulas práticas e teóricas. 

Referente aos testes fornecidos, conseguimos implementar todas as funcionalidades presentes neles menos as funcionalidades de funções e procedures.

O presente relatório irá abordar temas como a análise léxica, análise sintática e eventuais problemas e decisões sobre a arquitetura do compilador.


# Análise léxica 

Definida no ficheiro "lex.py" encontra-se o análisador léxico que desenvolvemos para capturar os tokens associados à linguagem Pascal. Para o desenvolver percorremos os programas de pascal de exemplo e adicionamos todos os tokens à medida que os identificávamos; assim, iterativamente, e com as impressões geradas pelo lexer na consola, alcançamos uma lista de tokens compreensiva. Dada a lista de tokens definimos as regras de captura para cada uma, tendo atenção à ordem com que as definiamos para garantir a precedência correta. 

É importante mencionar que os tokens tantos e tratam de palavras reservadas (p.ex. PROGRAM) como símbolos variáveis, como por exemplo números, nome das variáveis etc..

Segue-se uma descrição dos tokens: 

## Tokens

O analisador léxico reconhece os seguintes tokens organizados por categoria funcional:

### **Literais e identificadores**
| Token | Descrição | Exemplo |
|-------|-----------|---------|
| `INTEGER` | Números inteiros | `42`, `0`, `-15` |
| `REAL` | Números reais | `3.14`, `0.5`, `-2.718` |
| `STRING` | Literais de string (entre plicas) | `'Hello World'`, `'Pascal'` |
| `TRUE` | Literal booleano verdadeiro | `true` |
| `FALSE` | Literal booleano falso | `false` |
| `IDENTIFIER` | Identificadores de variáveis/funções | `x`, `contador` |

### **Operadores Aritméticos**
| Token | Descrição | Exemplo |
|-------|-----------|---------|
| `PLUS` | Operador de adição | `+` |
| `MINUS` | Operador de subtração | `-` |
| `TIMES` | Operador de multiplicação | `*` |
| `DIVIDE` | Divisão inteira (div) | `div` |
| `REAL_DIVIDE` | Divisão real | `/` |
| `MOD` | Operador módulo (resto) | `mod` |

### **Operadores Relacionais**
| Token | Descrição | Exemplo |
|-------|-----------|---------|
| `EQUAL` | Igualdade | `=` |
| `NE` | Diferente | `<>` |
| `LT` | Menor que | `<` |
| `GT` | Maior que | `>` |
| `LE` | Menor ou igual | `<=` |
| `GE` | Maior ou igual | `>=` |

### **Operadores Lógicos**
| Token | Descrição | Exemplo |
|-------|-----------|---------|
| `AND` | Conjunção lógica | `and` |
| `OR` | Disjunção lógica | `or` |
| `NOT` | Negação lógica | `not` |

### **Delimitadores e Pontuação**
| Token | Descrição | Exemplo |
|-------|-----------|---------|
| `LPAREN` | Parêntesis esquerdo | `(` |
| `RPAREN` | Parêntesis direito | `)` |
| `LBRACKET` | Bracket esquerda | `[` |
| `RBRACKET` | Bracket direita | `]` |
| `SEMICOLON` | Ponto e vírgula | `;` |
| `COLON` | Dois pontos | `:` |
| `COMMA` | Vírgula | `,` |
| `DOT` | Ponto | `.` |

### **Operadores de Atribuição**
| Token | Descrição | Exemplo |
|-------|-----------|---------|
| `ASSIGN` | Atribuição | `:=` |

### **Palavras-chave do Pascal**
| Token | Descrição | Exemplo |
|-------|-----------|---------|
| `PROGRAM` | Declaração de programa | `program` |
| `BEGIN` | Início de bloco | `begin` |
| `END` | Fim de bloco | `end` |
| `END_DOT` | Fim de programa | `end.` |
| `VAR` | Declaração de variáveis | `var` |

### **Tipos de Dados**
| Token | Descrição | Exemplo |
|-------|-----------|---------|
| `TYPE_INTEGER` | Tipo inteiro | `integer` |
| `TYPE_REAL` | Tipo real | `real` |
| `TYPE_STRING` | Tipo string | `string` |
| `BOOLEAN` | Tipo booleano | `boolean` |
| `ARRAY` | Declaração de array | `array` |
| `OF` | Palavra-chave para arrays | `of` |

### **Estruturas de controlo**
| Token | Descrição | Exemplo |
|-------|-----------|---------|
| `IF` | Palavra chave de if | `if` |
| `THEN` | Palavra chave de if | `then` |
| `ELSE` | Palavra chave de if | `else` |
| `WHILE` | Palavra chave de loop | `while` |
| `DO` | Palavra chave de loop | `do` |
| `FOR` | Palavra chave de loop | `for` |
| `TO` | Palavra chave de loop | `to` |
| `DOWNTO` | Palavra chave de loop | `downto` |

### **Comandos de I/O**
| Token | Descrição | Exemplo |
|-------|-----------|---------|
| `WRITE` | Escrita sem quebra de linha | `write` |
| `WRITELN` | Escrita com quebra de linha | `writeln` |
| `READLN` | Leitura do stdin | `readln` 


# Análise sintática (YACC)

O processo de implementacao da gramatica foi gradual e irregular, começou com uma gramática simples para o primeiro exemplo de programa "hello_world" e, rapidamente, as falhas reveleram-se quantos mais testes fossem realizados; problemas de shift/reduce com declarações if foram um dos maiores problemas.

É importante mencionar que, por defeito, o símbolos terminais são expressos em em maiúsculas e os símbolos não terminais em minúsculas.

A forma como definimos as strings foi guardando uma struct na struct heap, onde o índice 0 dessa struct corresponde ao tamanho da string e, os restantes a partir do índice 1, corresponde aos valores de ASCII de cada letra da string. O tamanho máximo da string foi definido com 256 mas, pode ser alterado no ficheiro **yacc.py**, mudando a variável global **STRING_MAX_SIZE**.


A gramatica final tomou esta forma : ("gramatica.md")
### **Estrutura Principal**
```
file → PROGRAM name vars code

name → IDENTIFIER SEMICOLON
```

A estrutura principal trata da definição base dum programa Pascal:
```
program programa1;
var
    ...
begin
...
end.
```

O símbolo NT name vai buscar o nome do programa e o ponto e vírgula;

O símbolo NT vars vai buscar todas as variáveis definidas no início do programa;

O símbolo NT code vai buscar todo o código dentro dos blocos **begin** e **ends.**

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

De forma a declarar as variáveis, criámos uma produção base chamada vars, que reconhece o símbolo terminal VAR e depois um varstail, que é uma lista de todas as variáveis declaradas no início.

Relativamente à declaração da variável em si, temos a produção **vardecl**, onde o símbolo não terminal idlist vai buscar uma lista dos identificadores desse tipo da **vardecl** que pode ter um ou mais elementos. De seguida, reconhece o símbolo terminal ':' e por fim o type, indica o tipo da variável (integer, real, array), e o semicolon, ';'.

```
var 
    i: Integer;
    n: Real;
    numeros: array[1..5] of integer;
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

Para refletir os tipos basicos em pascal criamos um "TYPE_INTEGER","TYPE_REAL","BOOLEAN" e "TYPE_STRING". O prefixo "TYPE_" existe para distinguir a declaracao do tipo inteiro ou seja "integer" e um valor inteiro "1,2,3,...", o mesmo aplica-se para reais e strings. Os valores booleanos destacam-se pelo facto de nao terem um equivalente na maquina virtual, pelo que soa tratados como inteiros que so podem tomar valor 1 e 0 e sem necessidade de distinguir tipo booleano de um val
ekot sem pascal :  ioaveins deste genero,  () pascala:

```
var
    numeros : array[1..5] of integer;
    i, soma: integer;
    b : boolean
    r : real
    s : stringt
```
icilpxe amrof edopen_statementsnekot son .ocode_or_statementnaeloob

Um programa vai ser composto por uma lista devdeclaracoes (statements). Inicialmente nao implementamos logica de statements open ou closed mas , mais tarde, problemas de shift/reduce causados por problemas de dangling else  r






arrays arrays etc. etc.mn


Em conjuntos as gramaticas para variaveis e tipos de dados permitem interpretar declaracoes de variaveis na maquina virtual.
nitsid assed edadissecen evuoho oan missa ,.ritsixe oan oticilpxe onaelollob opit o ,lautriv aniuqam an euq ed otca

arrays arrays etc. etc.mn

### **Estrutura do Programa**
```
code → BEGIN expressions END_DOT

dotless_code → BEGIN expressions END

expressions → statement expressions_tail
            | empty

expressions_tail → SEMICOLON expressions
                 | empty
```

Relativamente à secção de código, temos a produção **code** que começa por ler o símbolo terminal **BEGIN**, de seguida reconhece expressions, que é todo o conjunto de expressões possíveis pelo no compilador, como por exemplo ciclos for, if's, atribuição de valores a variáveis.

Temos ainda o dotless_code que, são blocos de código BEGIN-END que não têm o ponto final, por exemplo utilizados em statements de if ou for.

Da mesma forma,



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
identifier_assign_expression → ASSIGN assign_expression
                             | LBRACKET expression RBRACKET ASSIGN assign_expression

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

string_statement → assign_expression
                 | assign_expression COMMA string_statement

assign_expression → expression
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

## **Características Especiais da Gramática**

### **1. Solução para Dangling Else**
- **open_statement**: Statements incompletos que podem causar ambiguidade
- **closed_statement**: Statements completos e bem definidos

### **2. Precedência de Operadores (da maior para menor)**
1. **Unário**: `+`, `-`, `NOT`
2. **Multiplicativo**: `*`, `div`, `mod`, `/`
3. **Aditivo**: `+`, `-`
4. **Relacional**: `=`, `<>`, `<`, `>`, `<=`, `>=`
5. **Lógico AND**: `AND`
6. **Lógico OR**: `OR`

### **3. Tipos Suportados**
- **Primitivos**: `integer`, `real`, `boolean`, `string`
- **Compostos**: `array[min..max] of integer`
- **Literais**: `números inteiros`, `reais`, `strings`, `true`, `false`
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
identifier_assign_expression → ASSIGN assign_expression
                             | LBRACKET expression RBRACKET ASSIGN assign_expression

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

string_statement → assign_expression
                 | assign_expression COMMA string_statement

assign_expression → expression
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

## **Características Especiais da Gramática**

### **1. Solução para Dangling Else**
- **open_statement**: Statements incompletos que podem causar ambiguidade
- **closed_statement**: Statements completos e bem definidos

### **2. Precedência de Operadores (da maior para menor)**
1. **Unário**: `+`, `-`, `NOT`
2. **Multiplicativo**: `*`, `div`, `mod`, `/`
3. **Aditivo**: `+`, `-`
4. **Relacional**: `=`, `<>`, `<`, `>`, `<=`, `>=`
5. **Lógico AND**: `AND`
6. **Lógico OR**: `OR`

### **3. Tipos Suportados**
- **Primitivos**: `integer`, `real`, `boolean`, `string`
- **Compostos**: `array[min..max] of integer`
- **Literais**: `números inteiros`, `reais`, `strings`, `true`, `false`
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
identifier_assign_expression → ASSIGN assign_expression
                             | LBRACKET expression RBRACKET ASSIGN assign_expression

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

string_statement → assign_expression
                 | assign_expression COMMA string_statement

assign_expression → expression
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

## **Características Especiais da Gramática**

### **1. Solução para Dangling Else**
- **open_statement**: Statements incompletos que podem causar ambiguidade
- **closed_statement**: Statements completos e bem definidos

### **2. Precedência de Operadores (da maior para menor)**
1. **Unário**: `+`, `-`, `NOT`
2. **Multiplicativo**: `*`, `div`, `mod`, `/`
3. **Aditivo**: `+`, `-`
4. **Relacional**: `=`, `<>`, `<`, `>`, `<=`, `>=`
5. **Lógico AND**: `AND`
6. **Lógico OR**: `OR`

### **3. Tipos Suportados**
- **Primitivos**: `integer`, `real`, `boolean`, `string`
- **Compostos**: `array[min..max] of integer`
- **Literais**: `números inteiros`, `reais`, `strings`, `true`, `false`

### **4. Estruturas de Controle**
- **Condicionais**: `if-then`, `if-then-else`
- **Loops**: `while-do`, `for-to-do`, `for-downto-do`
- **I/O**: `write()`, `writeln()`, `readln()`

### **5. Operações com Arrays e Strings**
- **Acesso**: `array[index]`, `string[index]`
- **Função length**: `length(variable)`
- **Atribuição**: `variable := value`, `array[index] := value`

Esta gramática implementa uma versão simplificada do Pascal.


# Capítulo 4
## Implementação (Analise Semantica)

### 4.1 Alternativas Tecnológicas e Decisões

**Tecnologias Utilizadas:**

1. **Python 3.x**
   - Linguagem principal de implementação
   - Facilidade de prototipagem e debugging
   - Excelente suporte para processamento de texto

2. **PLY (Python Lex-Yacc)**
   - Framework para criação de lexers e parsers
   - Compatível com lex/yacc tradicionais
   - Geração automática de tabelas de parsing

3. **Arquitetura Assembly Customizada**
   - Conjunto de instruções simplificado
   - Foco em estruturas de controle
   - Compatível com máquina virtual educacional

**Decisões de Design:**

| Aspecto | Alternativa Escolhida | Justificativa |
|---------|----------------------|---------------|
| Parser Generator | PLY vs ANTLR | PLY integra melhor com Python |
| Estratégia Conflicts | Precedence vs Grammar Rewrite | Grammar rewrite mais elegante |
| Code Generation | During parsing vs Separate phase | Durante parsing é mais eficiente |
| Error Recovery | Panic mode vs Phrase level | Panic mode mais simples |


# Capítulo 5
## Utilizaçao

O programa pode ser executado sem argumentos e, assim, traduz os programas na pasta "programas_pascal" exceto o programa numero 7, nesse e necessaria a traducao de functions e nao implementamos essa funcionalidade como mencionado previamente. 

Depois da execucao a pasta "programas_gerados" contem o codigo pronto para ser testado na maquina virtual que reflete o comportamento do original. 

Tambem e possivel executar com 1 argumento que sera o nome de um ficheiro na pasta do projeto ("PL_Grupo5") e deve terminar em ".pas". A traducao sera guardada em "programas_gerados" com o mesmo nome do ficheiro original.


---

# Capítulo 6
## Conclusão

### Análise Crítica dos Resultados

**Pontos Fortes:**
1. **Solução elegante para o dangling else**: A abordagem de gramática estratificada mostrou-se superior às soluções baseadas apenas em precedência
2. **Código assembly otimizado**: Geração eficiente de labels únicos e instruções de salto
3. **Arquitetura extensível**: Design modular permite futuras extensões

**Limitações Identificadas:**
1. **Subconjunto limitado de Pascal**: Apenas estruturas básicas implementadas
2. **Verificação semântica básica**: Ausência de verificação rigorosa de tipos
3. **Otimizações de código**: Espaço para melhorias na qualidade do assembly gerado

**Impacto Técnico:**
- Eliminação de 100% dos conflitos de parsing
- Redução significativa da complexidade da gramática
- Manutenção da semântica original da linguagem Pascal

### Trabalho Futuro

**Extensões de Curto Prazo:**
1. **Estruturas de dados avançadas**: Implementação de arrays multidimensionais e records
2. **Subprogramas**: Suporte a procedures e functions com parâmetros
3. **Verificação semântica**: Implementação completa de verificação de tipos

**Extensões de Longo Prazo:**
1. **Otimizações**: Implementação de técnicas de otimização de código
2. **Ambiente de desenvolvimento**: Criação de IDE específico para a linguagem
3. **Máquina virtual**: Desenvolvimento de interpretador para o assembly gerado

---
