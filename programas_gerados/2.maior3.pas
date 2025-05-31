     PUSHI 0
     PUSHI 0
     PUSHI 0
     PUSHI 0
START
     PUSHS "Introduza o primeiro número: "
     WRITES
     READ
      DUP 1
      ATOI
      STOREG 0
       WRITES WRITELN
     PUSHS "Introduza o segundo número: "
     WRITES
     READ
      DUP 1
      ATOI
      STOREG 1
       WRITES WRITELN
     PUSHS "Introduza o terceiro número: "
     WRITES
     READ
      DUP 1
      ATOI
      STOREG 2
       WRITES WRITELN
     PUSHFP
       LOAD -4
     PUSHFP
       LOAD -3
     SUP
JZ ELSE2
     PUSHFP
       LOAD -4
     PUSHFP
       LOAD -2
     SUP
JZ ELSE0
     PUSHFP
       LOAD -4
       STOREG 3
     JUMP ENDIF0
ELSE0:
     PUSHFP
       LOAD -2
       STOREG 3
ENDIF0:
     JUMP ENDIF2
ELSE2:
     PUSHFP
       LOAD -3
     PUSHFP
       LOAD -2
     SUP
JZ ELSE1
     PUSHFP
       LOAD -3
       STOREG 3
     JUMP ENDIF1
ELSE1:
     PUSHFP
       LOAD -2
       STOREG 3
ENDIF1:
ENDIF2:
     PUSHS "O maior é: "
     WRITES
     PUSHFP
       LOAD -1
       STRI
     WRITES
       WRITELN
STOP
