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
     PUSHI 2
       STOREG 1
WHILESTART0:
     PUSHFP
       LOAD -2
     PUSHFP
       LOAD -3
     PUSHI 2
     DIV
     INFEQ
     PUSHFP
       LOAD -1
     AND
     JZ WHILEEND0
     PUSHFP
       LOAD -3
     PUSHFP
       LOAD -2
     MOD
     PUSHI 0
     EQUAL
JZ ELSE0
     PUSHI 0
       STOREG 2
     JUMP ENDIF0
ELSE0:
ENDIF0:
     PUSHFP
       LOAD -2
     PUSHI 1
     ADD
       STOREG 1
     JUMP WHILESTART0
WHILEEND0:
     PUSHFP
       LOAD -1
JZ ELSE1
     PUSHS " é um número primo"
     PUSHFP
       LOAD -3
       STRI
     CONCAT
     WRITES
       WRITELN
     JUMP ENDIF1
ELSE1:
     PUSHS " não é um número primo"
     PUSHFP
       LOAD -3
       STRI
     CONCAT
     WRITES
       WRITELN
ENDIF1:
STOP
