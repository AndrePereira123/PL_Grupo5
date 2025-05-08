     PUSHI 0
     PUSHI 0
     PUSHI 0
     PUSHI 0
     PUSHF 0.0
     PUSHF 0.0
     PUSHF 0.0
     PUSHI 0
START
     PUSHF 10.0
       STOREG 4
     PUSHF 20.0
       STOREG 5
     PUSHF 30.0
       STOREG 6
     PUSHFP
       LOAD -2
     PUSHFP
       LOAD -3
     FSUP
       WRITEI
     PUSHFP
       LOAD -2
     PUSHFP
       LOAD -3
     FSUPEQ
       WRITEI
     PUSHFP
       LOAD -4
     PUSHFP
       LOAD -3
     FINF
       WRITEI
     PUSHFP
       LOAD -4
     PUSHFP
       LOAD -2
     FINFEQ
       WRITEI
     PUSHFP
       LOAD -4
     PUSHFP
       LOAD -3
     EQUAL
       WRITEI
     PUSHFP
       LOAD -4
     PUSHFP
       LOAD -3
     EQUAL
      NOT
       WRITEI
     PUSHI 1020
       STOREG 3
     PUSHFP
       LOAD -5
     ITOF
       STOREG 4
     PUSHFP
       LOAD -5
       STRI
     PUSHS "O maior é: "
     CONCAT
     WRITES
       WRITELN
STOP
