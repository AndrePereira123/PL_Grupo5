program Teste_erros;
var
    a, b: boolean;
    x, y: integer;
    r1,r2 : real;
    vetor: array[1..10] of integer;
    s : string;
begin

     // a := 1; // Erro: Atribuição de inteiro a boolean
     // a := 'teste'; // Erro: Atribuição de string a boolean

       // a := true 
       // a := false // Erro: Falta de ponto e vírgula

     //if r1 then // Erro: Uso incorreto de 'if' (igual para while e for)
     //   writeln('A é verdadeiro');

    // r3 := 10.5; // Erro: r3 não foi declarado

       // r1 := 10.5; // Correto: r1 é do tipo real
       // vetor[1]:= r1; // Erro: atribuir real a inteiro
       // vetor[1] := 'teste'; // Erro: atribuir string a inteiro

end. // Erro : End em falta