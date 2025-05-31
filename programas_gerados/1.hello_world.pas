     PUSHI 0
     PUSHF 0.0
     ALLOC 256
START
     PUSHS "Ola, Mundo!"
     WRITES
     PUSHF 12.23
       STRF
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
     PUSHS "Ola, Mundo!"
     WRITES
     PUSHFP
       LOAD -3
       STRI
     WRITES
       WRITELN
     PUSHI 10
       STOREG 0
     PUSHS "Ola, Mundo!"
     WRITES
     PUSHFP
       LOAD -3
       STRI
     WRITES
       WRITELN
STOP
