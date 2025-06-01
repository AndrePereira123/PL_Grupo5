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
     READ
      DUP 1
      ATOI
      STOREG 2
       WRITES WRITELN
     READ
      DUP 1
      ATOF
      STOREG 4
       WRITES WRITELN
STOP
