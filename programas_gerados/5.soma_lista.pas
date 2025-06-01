     ALLOC 5
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
     PUSHI 0
     PUSHI 0
START
     PUSHI 0
       STOREG 2
     PUSHS "Introduza 5 números inteiros:"
     WRITES
       WRITELN
     PUSHI 1
      STOREG 1
FORSTART0:
     PUSHFP
      LOAD -2
     PUSHI 5
     INFEQ
JZ FOREND0
     PUSHST 0
     PUSHFP
       LOAD -2
     PUSHI 1
     SUB
     READ
      ATOI
      STOREN
     PUSHFP
       LOAD -1
     PUSHST 0
     PUSHFP
       LOAD -2
     PUSHI 1
     SUB
      LOADN
     ADD
       STOREG 2
     PUSHFP
     LOAD-2
     PUSHI 1
     ADD
     STOREG 1
     JUMP FORSTART0
FOREND0:
     PUSHS "A soma dos números é: "
     WRITES
     PUSHFP
       LOAD -1
       STRI
     WRITES
       WRITELN
STOP
