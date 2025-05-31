program Extras;
var
    a, b: boolean;
    x, y: integer;
    r1,r2 : real;
    vetor: array[1..10] of integer;
    s : string;
begin
    a := true;
    b := false;
    
    // NOT
    a := not b;                    // 1
    a := not (x = y);             // 0
    a := not (x > 5);             // 1

    // Print de elementos de vetor - (so se atribuidos valores)
    writeln('Elementos do vetor:');
    for x := 1 to 3 do
    begin
        vetor[x] := x;         // Atribuindo valores ao vetor
        writeln('Vetor numero ', x ,'=',vetor[x]);
    end;

    // Print de string  ou elemento da string
    writeln('String exemplo:', ' Hello, World!');
    s := 'Hello, World!';
    writeln(s,10,s,10);
    writeln(s[1]);  // Acessando o primeiro caractere



    // if, while e for com OR e AND 
    if (a or b) and (x < 5) then
    begin
        writeln('Condição verdadeira');
        x := x + 1;     // Incrementa x
    end
    else
    begin
        writeln('Condição falsa');
        writeln('x = ', x);  
    end;

    while (a and b) or (x < 10) do
    begin
        writeln('While executando, x = ', x);
        x := x + 1;  // Incrementa x
    end;



    
end.