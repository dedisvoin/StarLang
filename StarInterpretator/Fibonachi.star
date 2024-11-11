import 'libs/Time.py' as (Time);

// recursive fibonacci
var [starfunc] fib_rec = func(n: int)!(fib_rec) : int ; {
    if (n == 0) |> 0;
    if (n == 1) |> 1;
    |> fib_rec(n - 1) + fib_rec(n - 2);
};

// loop fibonacci
var [starfunc] fib_loop = func(n: int)!(fib_loop) : int ; {
    var a = 0; var b = 1; var c = 0; var i = 0;
    while (i < n - 1) {
        c = a + b;
        a = b; b = c;
        i = i + 1;
    }
    |> c;
};

static const var[starfunc] main = func(args: list = []) ! 
(fib_rec, fib_loop, Time) : int ; {

    var n = 11;

    var st = Time::time();
    out fib_rec(n);
    out 'Rcursive fibonacci took ', Time::time() - st, 'ms';

    var st = Time::time();
    out fib_loop(n);
    out 'Loop fibonacci took ', Time::time() - st, 'ms';
    |> 0;
};



main();

