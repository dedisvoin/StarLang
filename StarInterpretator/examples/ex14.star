/*
Передача переменных из внешних областей памяти во внутренние,
дает возможность реализоввывать `замыкания` в функциях.
*/
var generate_func = func(op: string) : starfunc ; {
    |> func(x: [int, float], y: [int, float]) ! (op) : [int, float] ; { // мы перабрасываем `op` в память внутренней функции.
        if (op == '+') |> x + y;
        if (op == '-') |> x - y;
        if (op == '*') |> x * y;
        if (op == '/') |> x / y; 
    };
};

var f = generate_func('/');
out f(10, 3);
var f = generate_func('*');
out f(10, 3);
var f = generate_func('-');
out f(10, 3);
var f = generate_func('+');
out f(10, 3);
