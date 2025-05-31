     ALLOC 256
     PUSHI 0
     PUSHI 0
     PUSHI 0
START
     PUSHS "Introduza uma string binária:"
     WRITES
       WRITELN
     READ
     DUP 1
     STRLEN
     DUP 2
     PUSHST 0
     SWAP
     PUSHI 0
     SWAP
     STOREN
     PUSHI 256
     INF
     JZ STR0END
     PUSHI 0
STR0START:
     DUP 1
     PUSHST 0
     PUSHL 0
     PUSHL 2
     CHARAT
     PUSHL 2
     PUSHI 1
     ADD
     SWAP
     STOREN
     PUSHI 1
     ADD
     DUP 1
     STOREL 2
     PUSHL 1
     INF
     JZ STR0END
     JUMP STR0START
STR0END:
     POP 3
     PUSHI 0
       STOREG 2
     PUSHI 1
       STOREG 3
     PUSHST 0
     PUSHI 0
     LOADN
      STOREG 1
FORSTART0:
     PUSHFP
      LOAD -3
     PUSHI 1
     SUPEQ
JZ FOREND0
     PUSHST 0
     PUSHFP
       LOAD -3
     LOADN
      PUSHS "1"
     CHRCODE
     EQUAL
JZ ENDIF0
     PUSHFP
       LOAD -2
     PUSHFP
       LOAD -1
     ADD
       STOREG 2
ENDIF0:
     PUSHFP
       LOAD -1
     PUSHI 2
     MUL
       STOREG 3
     PUSHFP
     LOAD-3
     PUSHI -1
     ADD
     STOREG 1
     JUMP FORSTART0
FOREND0:
     PUSHS "O valor inteiro correspondente é: "
     WRITES
     PUSHFP
       LOAD -2
       STRI
     WRITES
       WRITELN
STOP
