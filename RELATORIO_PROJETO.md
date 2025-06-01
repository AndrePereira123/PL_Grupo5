# Trabalho Prático - Relatório  
**Processamento de Linguagens**  

**(3º ano - LEI)**



**Andre Pereira - A104275**

**Leonardo Alves - A104093** 



*31 de Maio de 2025*



---

## Resumo



Este relatório tem como propósito a exposição do processo de desenvolvimento de um compilador para uma versão simplificada da linguagem Pascal, focado na tradução do código escrito em pascal para código "maquina" que seja funcional na virtual machine EWVM (https://ewvm.epl.di.uminho.pt). Os resultados demonstram a eliminação completa dos conflitos shift/reduce, reduce/reduce,... , garantindo uma análise sintática determinística e geração correta de código para estruturas condicionais e iterativas.



---



# Introdução



No âmbito da disciplina de Processamento de Linguagens, fomos desafiados a desenvolver um compilador para Pascal Standard, fazendo a sua tradução para código máquina da EWVM. Perante isto, para a geração de código máquina, seguimos uma tradução dirigida pela sintaxe, onde o código Pascal é automaticamente convertido em código da VM.



Para a análise léxica e sintática, recorremos ao PLY, que foi a biblioteca utilizada ao longo do semestre nas aulas práticas e teóricas. 



Referente aos testes fornecidos, conseguimos implementar todas as funcionalidades presentes neles exceto as funcionalidades de funções e procedures.



O presente relatório irá abordar temas como a análise léxica, análise sintática e eventuais problemas e decisões sobre a arquitetura do compilador.





# Análise léxica 



Definida no ficheiro "lex.py" encontra-se o analisador léxico que desenvolvemos para capturar os tokens associados à linguagem Pascal. Para o desenvolver percorremos os programas de pascal de exemplo e adicionamos todos os tokens à medida que os identificávamos; assim, iterativamente, e com as impressões geradas pelo lexer na consola, alcançamos uma lista de tokens compreensiva. Dada a lista de tokens definimos as regras de captura para cada uma, tendo atenção à ordem com que as definíamos para garantir a precedência correta. 



É importante mencionar que os tokens abrangem tanto símbolos terminais fixos (palavras reservadas como PROGRAM, IF, WHILE) como símbolos terminais variáveis (literais numéricos, identificadores, strings, etc.).

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



O processo de implementação da gramática foi gradual e irregular, começou com uma gramática simples para o primeiro exemplo de programa "hello_world" e, rapidamente, as falhas surgiram à medida que mais testes foram realizados; problemas de shift/reduce com declarações if foram um dos maiores problemas.

É importante mencionar que, por defeito, os símbolos terminais são expressos em maiúsculas e os símbolos não terminais em minúsculas.

A gramática final tomou esta forma: ("gramatica.md")

### **Estrutura Principal**

```
file → PROGRAM name vars code

name → IDENTIFIER SEMICOLON
```

A estrutura principal trata da definição base dum programa Pascal:

```
program programa1;
var ...
begin
...
end.
```



O símbolo NT name vai buscar o nome do programa e o ponto e vírgula;

O símbolo NT vars vai buscar todas as variáveis definidas no início do programa;

O símbolo NT code vai buscar todo o código nos blocos **begin** e **ends.**



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



Para refletir os tipos básicos em pascal criamos um "TYPE_INTEGER","TYPE_REAL","BOOLEAN" e "TYPE_STRING". O prefixo "TYPE_" existe para distinguir a declaracao do tipo inteiro ou seja "integer" e um valor inteiro "1,2,3,...", o mesmo aplica-se para reais e strings. Os valores booleanos destacam-se pelo facto de não terem um equivalente na máquina virtual, pelo que decidimos trata-los como inteiros que só podem tomar valor 1 ou 0.

Apenas implementamos arrays de inteiros "ARRAY ..." onde o arraytypes permite a definição de um array com 1 só elemento ou mais de 1 elemento.

Em conjunto a gramática para variáveis e a gramática para tipos de dados permitem interpretar declarações de variáveis em Pascal:

```
var
    numeros : array[1..5] of integer;
    i, soma: integer;
    b : boolean
    r : real
    s : string
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



Relativamente à secção de código, temos a produção **code** que começa por ler o símbolo terminal **BEGIN**, de seguida reconhece expressions, que é todo o conjunto de expressões possíveis no compilador, como, por exemplo ciclos for, if's, atribuição de valores a variáveis,etc..


Temos ainda o dotless_code que são blocos de código BEGIN-END que não têm o ponto final, por exemplo, utilizados em statements de if ou for.

Temos então a produção referente a expressions, que reconhece precisamente cada uma das expressões do código, recorrendo ao expressions_tail, que é uma lista de expressions, separadas por ponto e vírgulas.



#### **code**

```
begin
    writeln('Ola, Mundo!', 12.23);  
    ReadLn(i);
    writeln(i);
end.
```

#### **dotless_code**

```
for i := 1 to 5 do
    begin
        readln(numeros[i]);
        soma := soma + numeros[i];
    end;
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

Um programa vai ser composto por uma lista de declarações (statements). Inicialmente não implementamos lógica de **statements** open ou closed, mas , mais tarde, problemas de shift/reduce causados pelo paradigma do **dangling else** (ambiguidade na atribuição do else ao if correspondente), levaram-nos a implementar essa distinção. 

Para declarações abertas temos que garantir que existe pelo menos 1 declaração if sem um else associado, desta forma não pode ser uma declaração simples como uma atribuição, um write/writeln ou um readln, esses garantem que não existe um ciclo if aberto, logo, são consideradas declarações fechadas.

 Declarações abertas podem, assim, ser declarações if , com ou sem else, ou ciclos while/for, uma vez que todos estes tem a possibilidade de ter código que contenha múltiplas declarações ou uma só declaração que se trate de um if sem else associado.



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



Nesta secção apresentámos a gramática para as atribuições de valores a variáveis, no caso a produção de **identifier_assign_expression**, que pode ter dois tipos:

- **Atribuir um valor a uma variável**, sendo a primeira produção de **identifier_assign_expression**, onde reconhece em primeiro lugar o símbolo de ASSIGN ':=', e de seguida a **expression**, que é uma expressão que pode ser tanto um valor único, como um conjunto de operações relacionais, aritméticas ou lógicas, dependendo do tipo da variável que estamos a dar assign. É importante mencionar que fizemos uma verificação de tipos na atribuição, ou seja, verificar se as duas expressões são do mesmo tipo;



- **Atribuir um valor a um índice de um array**, que reconhece o índice do array, através de do reconhecimento do LBRACKET '[', e de seguida a expressão relativa a ir buscar o seu índice, que só pode ser simple_expression, no entanto, no YACC é necessário verificar se o valor proveniente dessa expression é um valor inteiro, caso não for, dá erro de tipos. Por fim, reconhece RBRACKET ']' e ASSIGN ':=' e a expressão que pretende associar a essa variável.



#### **Atribuir um valor a uma variável**

```
:= 0;
:= 10.4;
:= 'valor';
```



#### **Atribuir um valor a um índice de um array**

```
[1] := 2
```



Temos ainda a gramática referente às condições das operações for, **for_condition** e **to_expression**, onde a primeira define a condição do ciclo for, por exemplo, percorrer enquanto o valor de i é menor que 10 e, a segunda, **to_expression**, que define se o for é do tipo TO ou DOWNTO.



Por fim, temos o **code_or_statement**, que define o bloco de "código" do if, for ou while, ou seja, as operações que serão efetuadas dentro dos ciclos ou nas operações de if.



### **I/O Statements**

```
write_statement → LPAREN string_statement RPAREN

readln_statement → LPAREN string_statement RPAREN

string_statement → expression
                 | expression COMMA string_statement

```



Nos statemets de **input/output** temos símbolos não terminais para identificar ações de escrita "write_statement" e leitura "readln_statement", ambas recebem um string_statement que pode ser uma só "expression", ou uma lista com varias separadas por virgulas; no caso de escrita serão concatenados os resultados e no caso de leitura lê o input 1 a 1 na ordem recebida. 


A expression pode tomar vários valores e, no caso de não serem uma string, são transformados numa, no caso de um inteiro usamos o "STRI",no de um valor real o "STRF" e, no caso de um valor booleano, escrevemos logo o output "WRITEI".



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



Esta parte da gramática define como as expressões lógicas e aritméticas podem ser combinadas, **respeitando** a **precedência** dos operadores em Pascal.



A definição destas produções foi cuidadosamente desenhada para garantir que a precedência e associatividade dos operadores em Pascal é corretamente respeitada, evitando ambiguidades e conflitos de parsing. 



Ao separar as expressões em diferentes níveis (`expression`, `and_expression`, `relation_expression`, etc.), conseguimos refletir a ordem natural de avaliação dos operadores: primeiro as operações relacionais, depois os operadores lógicos `AND` e, por fim, o `OR`. Esta abordagem torna a gramática mais clara, permitindo ao parser distinguir facilmente entre expressões aritméticas, relacionais e booleanas, assegurando que cada operação é efetuada conforme os seus requisitos de precedência.


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

Para implementar gramática relativa a **expressões aritméticas** tivemos que ter atenção extra à precedência de operações; uma expressão aritmética, podendo tomar qualquer valor desde um simples inteiro a uma expressão enorme, trata-se de um termo e uma "simple_expression_tail". 

A cauda pode ser uma operação de mais(PLUS) ou de menos(MINUS), assim estas terão menor prioridade que aquelas que são descritas na especificação do termo (term); na "term_tail" podemos ter operações de multiplicação, divisão e resto; estas terão, assim, prioridade respeitando as regras esperadas de operações aritméticas.

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



A produção `factor` define os elementos mais básicos que podem aparecer numa expressão aritmética ou booleana. Esta produção permite representar:



- **Operadores unários**: O uso de `PLUS` e `MINUS` antes de um fator permite lidar com sinais positivos e negativos, respeitando a precedência dos operadores unários;

- **Parêntesis**: O uso de `LPAREN expression RPAREN` permite alterar a ordem de avaliação das operações, garantindo que expressões entre parêntesis são avaliadas em primeiro;

- **Literais**: Permite o uso direto de valores inteiros, reais, booleanos e strings nas expressões;

- **Identificadores**: Permite o uso de variáveis simples, acesso a arrays ou strings por índice, e também o uso da função `length` para obter o tamanho de arrays ou strings.





### **Acesso a Arrays e funçao length**

```
length_expression → LPAREN IDENTIFIER RPAREN

identifier_expression → LBRACKET expression RBRACKET
                      | empty
```

A "length_expression" permite reconhecer a varíavel a ser utilizada como input na função de length.

A "identifier_expression" serve para reconhecer o índice de um array, no caso, o símbolo não terminal "expression" (verifica se é um valor inteiro).

### **Regra Vazia**

```
empty → ε
```




# Implementação 



Na presente secção iremos apresentar algumas decisões e implementações de funcionalidades que não estavam evidentes nos programas de testes fornecidos pela equipa docente.



## Variáveis globais no YACC



De forma a facilitar o controlo das variáveis e de outros parâmetros necessários à compilação de programas Pascal e escrita de código na VM, utilizámos as seguintes variáveis globais no nosso analisador sintático:

- **variaveis**: Dicionário que guarda as variáveis do programa, onde a chave é o nome da variável e o valor é um tuplo onde o primeiro elemento indica o tipo de variável e o segundo elemento indica o índice dessa variável no **Global Pointer** da VM;

- **label_index**: De forma às labels da VM terem nomes únicos para não haver conflitos, recorremos a esta variável que é utilizada para dar diferentes nomes às labels (**LABEL0**, **LABEL1**, etc..);

- **index**: Variável que indica o número de variáveis que foram guardadas antes do **START** na VM;

- **struct_index**: Variável que indica o número de estruturas guardadas na Struct Heap;

- **numero_ciclos_if**: Variável que controla o número de labels referentes aos IF's, de forma às labels serem valores únicos;

- **numero_ciclos_for**: Variável que controla o número de labels referentes aos FOR's, de forma às labels serem valores únicos;

- **numero_ciclos_while**: Variável que controla o número de labels referentes aos WHILE's, de forma às labels serem valores únicos;

- **index_variavel_ciclo_for**: Este dicionário guarda, para cada ciclo for, a "distancia" da variável usada para o ciclo for na stack; ou seja, permite dar "**LOAD**" da variável ou, em conjunto com o index, determinar com que valor usar o comando "**STOREG**" de forma a guardar a variável na posição correta da stack.

- **tipo_ciclo_for**: Como o nome diz este dicionário regista o tipo de cada ciclo for, ou seja, se representa um "down to" ou "to" no código pascal original; assim, a cada iteração, podemos determinar se subtraímos ou somamos 1 valor à variável de ciclo.







## Arrays e strings

De forma a guardámos as strings e arrays no nosso programa, utilizámos uma arquitetura bastante similar entre ambas onde, o que difere é o tamanho que cada uma ocupa. Ambos são guardados na struct heap e, no caso das strings, é guardado o seu valor de ASCII.



Para um array, se este for definido da seguinte forma: ```v: array[1..5] of integer```, apenas serão alocados 5 elementos do array ao contrário da string que, como é definida da seguinte forma: ```s: string```, são alocados 256 posições, valor predefinido no YACC através da variável **STRING_MAX_SIZE**.



É importante também mencionar que, a forma como é calculado o tamanho de uma string é acedendo ao índice 0 da sua estrutura, uma vez que esse valor representa precisamente o tamanho da string guardada na struct. Por outro lado, o tamanho do array é sempre o mesmo quer esteja preenchido ou não (definição do Pascal) e, por isso, para calcular o tamanho do array basta pesquisar pela variável no dicionário guardado no YACC e, pegar no valor do tamanho do array. Opcionalmente podias controlar da mesma forma que as strings, no entanto, não achámos necessário uma vez que um array terá sempre o mesmo tamanho.



Quanto aos arrays, é importante mencionar que iniciámos todos os índices com o valor de 0. Esta decisão foi apenas uma decisão de arquitetura uma vez que se tentarmos aceder a um índice de um certo array que não foi inicializado, este dará um valor sem significado e não dá erro(em Pascal Standard).



## Write de strings

Uma vez que guardámos as nossas strings na **struct heap**, para conseguirmos escrevê-la no ecrã decidimos recorrer à utilização de labels onde, será feito uma espécie de ciclo while enquanto não forem percorridos todos os elementos. Ou seja, iremos buscar o valor do tamanho da string (índice 0 da struct heap) e de seguida percorrer cada um dos índices válidos, utilizando o comando **WRITECHR** da VM para escrever a letra correspondente ao símbolo ASCII.



## Controlo de erros

De forma a evitar erros desnecessários de compilação, fazemos algum controlo de erros nomeadamente no assignment de um valor a uma certa variável, ou seja, verificámos se os tipos entre o valor a associar e o valor da variável são iguais, caso não sejam, irá ser lançado um TypeError pelo YACC. (Mais exemplos em "erros.pas")

## Read

De forma a tornar os programas mais legíveis na VM, decídimos que nas operações de read do Pascal, irá surgir uma instrução no final de ler que escreve no ecrã o texto que acabou de ser lido. Este mudança foi apenas para facilitar a compreensão e fluxo do programa na VM e, ao mesmo tempo, refletir de forma fiel o comportamento de programas Pascal.

## Testes extra
Uma vez que implementámos certas funcionalidades que não estavam presentes nos testes fornecidos pela equipa docente, decídimos criar um ficheiro (**0.Funcionalidades_extra.pas**) que as ilustra. Dentro das novas funcionalidades podemos destacar a escrita no ecrã de elementos de um array ou de um certo índice de uma string.




# Utilização



O programa pode ser executado sem argumentos e, assim, traduz os programas na pasta "programas_pascal" exceto o programa número 7, nesse e necessária a tradução de functions e não implementamos essa funcionalidade como mencionado previamente. 



Depois da execução a pasta "**programas_gerados**" contem o código pronto para ser testado na máquina virtual que reflete o comportamento do original. 



Também é possível executar com 1 argumento que será o nome de um ficheiro na pasta do projeto ("PL_Grupo5") e deve terminar em ".pas" (p.e. erros.pas). A tradução será guardada em "**programas_gerados**" com nome idêntico ao do ficheiro original.



---

# Capítulo 6
## Conclusão

Em suma, o desenvolvimento deste compilador permitiu-nos consolidar conhecimentos sobre análise léxica, sintática e geração de código para a máquina virtual. 

Apesar dos desafios encontrados, especialmente na resolução de conflitos sintáticos e na gestão de estruturas como arrays e strings, conseguimos implementar uma solução funcional para a maioria dos programas de teste fornecidos pela equipa docente, havendo ainda outros tipos de funcionalidades que implementámos e não estavam nesses testes. A curva de aprendizagem inicial da máquina virtual dificultou a tradução de código mas, depois da fase inicial, tornou-se relativamente intuitiva e gratificante compreender o código minimalista sob o qual depende.

No geral, consideramos que os objetivos propostos foram atingidos e que o trabalho realizado contribuiu para uma melhor compreensão dos conceitos fundamentais do processamento de linguagens.

Para melhoria futura poderiamos realizar melhor otimização do código traduzido, uma vez que não demos muito destaque a essa característica da tradução; focamo-nos apenas em garantir a funcionalidade. 


---