     PUSHI 0
     PUSHI 0
     PUSHI 0
START
     PUSHS "Introduza um número inteiro positivo:"
     WRITES
       WRITELN
     READ
      DUP 1
      ATOI
      STOREG 0
       WRITES WRITELN
     PUSHI 1
       STOREG 2
     PUSHI 1
      STOREG 1
FORSTART0:
     PUSHFP
      LOAD -2
     PUSHFP
       LOAD -3
     INFEQ
JZ FOREND0
     PUSHFP
       LOAD -1
     PUSHFP
       LOAD -2
     MUL
       STOREG 2
     PUSHFP
     LOAD-2
     PUSHI 1
     ADD
     STOREG 1
     JUMP FORSTART0
FOREND0:
     PUSHS "Fatorial de "
     WRITES
     PUSHFP
       LOAD -3
       STRI
     WRITES
     PUSHS ": "
     WRITES
     PUSHFP
       LOAD -1
       STRI
     WRITES
       WRITELN
STOP
