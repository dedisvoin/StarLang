
////////////////////////////////////////////////////
//         BASIC AND RECURSION FUNCTIONS          //
////////////////////////////////////////////////////


import 'libs/Time.py' as (Time);

// very slow fibonacci implementation
// рекурсивные вызовы не оптимизированны
var fib = func(n: int) ! (fib) : int ; {
    if (n == 0) {
        |> 0;
    } else if (n == 1) {
        |> 1;
    } else {
        |> fib(n - 1) + fib(n - 2);
    }
};

var st = Time::time();
core::print([fib(7)]);
out 'found in ', Time::time() - st, ' seconds';
// out: 2.88 seconds

// faster fibonacci implementation
// вычисление через цикл
var fib = func(n: int) : int ; {
    var n1 = 1; var n2 = 1; var n3;
    while (n - 2 > 0) {
        n3 = n1;
        n1 = n2; n2 = n1 + n3;
        n = n - 1;
    }
    |> n2;
};


var st = Time::time();
core::print([fib(7)]);
out 'found in ', Time::time() - st, ' seconds';
// out: 0.01 seconds