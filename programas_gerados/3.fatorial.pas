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
     PUSHFP
       LOAD -3
       STRI
     CONCAT
     PUSHS "Fatorial de "
     CONCAT
     WRITES
       WRITELN
STOP
