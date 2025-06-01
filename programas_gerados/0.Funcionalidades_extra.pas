     PUSHI 0
     PUSHI 0
     PUSHI 0
     PUSHI 0
     PUSHF 0.0
     PUSHF 0.0
     ALLOC 10
     PUSHST 0
     PUSHI 0
     PUSHI 0
     STOREN
     PUSHST 0
     PUSHI 1
     PUSHI 0
     STOREN
     PUSHST 0
     PUSHI 2
     PUSHI 0
     STOREN
     PUSHST 0
     PUSHI 3
     PUSHI 0
     STOREN
     PUSHST 0
     PUSHI 4
     PUSHI 0
     STOREN
     PUSHST 0
     PUSHI 5
     PUSHI 0
     STOREN
     PUSHST 0
     PUSHI 6
     PUSHI 0
     STOREN
     PUSHST 0
     PUSHI 7
     PUSHI 0
     STOREN
     PUSHST 0
     PUSHI 8
     PUSHI 0
     STOREN
     PUSHST 0
     PUSHI 9
     PUSHI 0
     STOREN
     ALLOC 256
START
     PUSHI 1
       STOREG 0
     PUSHI 0
       STOREG 1
     PUSHFP
       LOAD -7
     NOT
       STOREG 0
     PUSHFP
       LOAD -6
     PUSHFP
       LOAD -5
     EQUAL
     NOT
       STOREG 0
     PUSHFP
       LOAD -6
     PUSHI 5
     SUP
     NOT
       STOREG 0
     PUSHS "Elementos do vetor:"
     WRITES
       WRITELN
     PUSHI 1
      STOREG 2
FORSTART0:
     PUSHFP
      LOAD -6
     PUSHI 3
     INFEQ
JZ FOREND0
     PUSHST 0
     PUSHFP
       LOAD -6
     PUSHI 1
     SUB
     PUSHFP
       LOAD -6
     STOREN
     PUSHS "Vetor numero "
     WRITES
     PUSHFP
       LOAD -6
       STRI
     WRITES
     PUSHS "="
     WRITES
     PUSHST 0
     PUSHFP
       LOAD -6
     PUSHI 1
     SUB
     LOADN
       STRI
     WRITES
       WRITELN
     PUSHFP
     LOAD-6
     PUSHI 1
     ADD
     STOREG 2
     JUMP FORSTART0
FOREND0:
     PUSHS "String exemplo:"
     WRITES
     PUSHS " Hello, World!"
     WRITES
       WRITELN
     PUSHST 1
     PUSHI 1
     PUSHI 72
     STOREN
     PUSHST 1
     PUSHI 2
     PUSHI 101
     STOREN
     PUSHST 1
     PUSHI 3
     PUSHI 108
     STOREN
     PUSHST 1
     PUSHI 4
     PUSHI 108
     STOREN
     PUSHST 1
     PUSHI 5
     PUSHI 111
     STOREN
     PUSHST 1
     PUSHI 6
     PUSHI 44
     STOREN
     PUSHST 1
     PUSHI 7
     PUSHI 32
     STOREN
     PUSHST 1
     PUSHI 8
     PUSHI 87
     STOREN
     PUSHST 1
     PUSHI 9
     PUSHI 111
     STOREN
     PUSHST 1
     PUSHI 10
     PUSHI 114
     STOREN
     PUSHST 1
     PUSHI 11
     PUSHI 108
     STOREN
     PUSHST 1
     PUSHI 12
     PUSHI 100
     STOREN
     PUSHST 1
     PUSHI 13
     PUSHI 33
     STOREN
       PUSHST 1
     PUSHI 0
     PUSHI 13
       STOREN
     PUSHST 1
     DUP 1
     PUSHI 0
     LOADN
     STOREL 0
     PUSHI 0
     STOREL 1
STR0PRINTSTART:
     PUSHL 1
     PUSHL 0
     INF
     JZ STR0PRINTEND
     PUSHST 1
     PUSHL 1
     PUSHI 1
     ADD
     LOADN
     WRITECHR
     PUSHL 1
     PUSHI 1
     ADD
     STOREL 1
     JUMP STR0PRINTSTART
STR0PRINTEND:
           POP 2
     PUSHI 10
       STRI
     WRITES
     PUSHST 1
     DUP 1
     PUSHI 0
     LOADN
     STOREL 0
     PUSHI 0
     STOREL 1
STR1PRINTSTART:
     PUSHL 1
     PUSHL 0
     INF
     JZ STR1PRINTEND
     PUSHST 1
     PUSHL 1
     PUSHI 1
     ADD
     LOADN
     WRITECHR
     PUSHL 1
     PUSHI 1
     ADD
     STOREL 1
     JUMP STR1PRINTSTART
STR1PRINTEND:
           POP 2
     PUSHI 10
       STRI
     WRITES
       WRITELN
     PUSHST 1
     PUSHI 1
     LOADN
        WRITECHR
       WRITELN
     PUSHFP
       LOAD -8
     PUSHFP
       LOAD -7
     OR
     PUSHFP
       LOAD -6
     PUSHI 5
     INF
     AND
JZ ELSE0
     PUSHS "Condição verdadeira"
     WRITES
       WRITELN
     PUSHFP
       LOAD -6
     PUSHI 1
     ADD
       STOREG 2
     JUMP ENDIF0
ELSE0:
     PUSHS "Condição falsa"
     WRITES
       WRITELN
     PUSHS "x = "
     WRITES
     PUSHFP
       LOAD -6
       STRI
     WRITES
       WRITELN
ENDIF0:
WHILESTART0:
     PUSHFP
       LOAD -8
     PUSHFP
       LOAD -7
     AND
     PUSHFP
       LOAD -6
     PUSHI 10
     INF
     OR
JZ WHILEEND0
     PUSHS "While executando, x = "
     WRITES
     PUSHFP
       LOAD -6
       STRI
     WRITES
       WRITELN
     PUSHFP
       LOAD -6
     PUSHI 1
     ADD
       STOREG 2
JUMP WHILESTART0
WHILEEND0:
STOP
