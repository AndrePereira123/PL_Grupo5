     PUSHI 0
     PUSHF 0.0
     ALLOC 256
START
     PUSHF 12.23
       STRF
     PUSHS "Ola, Mundo!"
     CONCAT
     WRITES
       WRITELN
     READ
      DUP 1
      ATOI
      STOREG 0
       WRITES WRITELN
     PUSHFP
       LOAD -3
       STRI
     WRITES
       WRITELN
     PUSHFP
       LOAD -3
       STRI
     PUSHS "Ola, Mundo!"
     CONCAT
     WRITES
       WRITELN
     PUSHI 10
       STOREG 0
     PUSHFP
       LOAD -3
       STRI
     PUSHS "Ola, Mundo!"
     CONCAT
     WRITES
       WRITELN
STOP
