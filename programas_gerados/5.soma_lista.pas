     ALLOC 5
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
     PUSHFP
     LOAD-2
     PUSHI 1
     ADD
     STOREG 1
     JUMP FORSTART0
FOREND0:
     PUSHFP
       LOAD -1
       STRI
     PUSHS "A soma dos números é: "
     CONCAT
     WRITES
       WRITELN
STOP
