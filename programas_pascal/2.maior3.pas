program Maior3;
var
    num1, num2, num3, maior: Integer;
    x, y, z: Real;
    b : Boolean;
begin
    { Ler 3 números 
    Write('Introduza o primeiro número: ');
    ReadLn(num1);
    
    Write('Introduza o segundo número: ');
    ReadLn(num2);

    Write('Introduza o terceiro número: ');
    ReadLn(num3);}

    x := 10.0;
    y := 20.0;
    z := 30.0;

    b := z > y; 
    b := z >= y; 
    b := x < y;
    b := x <= z;

    b := x = y;
    b := x <> y;

    maior := 1020;

    { Escrever os números lidos

    
    

    { Calcular o maior
    if num1 > num2 then
        if num1 > num3 then maior := num1
        else maior := num3
    else
        if num2 > num3 then maior := num2
        else maior := num3;
    

    { Escrever o resultado }
    x := maior;
    WriteLn('O maior é: ', maior);
    
end.