////////////////////////////////////////////////////
//               LAMBDA EXPRESSIONS               //
////////////////////////////////////////////////////

// basic lambda function definition
var [lambdafunc] sum = lambda (x, y) {x + y};

out sum(10, 20); // call with arguments 10, 20
// out: 30


// out sum(5); аргументы которые вы не указали автоматически будут установлены в значение `null`
/*

при выполнении этой строки выйдет ошибка

[ execute exception ][ line 6: pos 39 ] In file 'examples/ex9.star'
|
| var [lambdafunc] sum = lambda (x, y) {x + y};
|                                       ^^^^^
|                                         |
|                                         `--- value to types ["int" and "null"] not to be used with operator "+"

*/



// поэтому можно оказать стандартное значение аргументу через `=`
var [lambdafunc] distance = lambda(x1 = 0, y1 = 0, x2 = 0, y2 = 0)!(math) {
    math::sqrt(math::pow(x2 - x1, 2) + math::pow(y2 - y1, 2))
};


out distance(3, 4); // out: 5


// типизация аргументов так же поддерживается
var [lambdafunc] distance = lambda(x1: int = 0, y1: int = 0, x2: int = 0, y2: int = 0)! : float  {
    math::sqrt(math::pow(x2 - x1, 2) + math::pow(y2 - y1, 2))
};

// out distance(3, 'ded'); // type error

/*

[ execute exception ][ line 42: pos 5 ] In file 'examples/ex9.star'
|
| out distance(3, 'ded');
|     ^^^^^^^^^^^^^^^^^^
|              |
|              |---[>] "anonymous lambda" function arguments "y1" type not match
|              `---[?] string expected, ['int'] given
*/


// возможна рекурсивная передача аргументов в выражение
// но так не рекомендуется делать (слишком медленно)
const var get_text = lambda (name: string)!(core) {
    lambda (age: int)!(name, core) {
        'Hello ' + name + '! You are ' + core::to_string(age) + ' years old'
    }
};


// тест на производительность вызова lambda функции, возвращающий ссылку на другую функцию имеющую доступ к глобальной памяти

out get_text('John')(20); // out: Hello John! You are 20 years old
out get_text('John')(20); // out: Hello John! You are 20 years old
out get_text('John')(20); // out: Hello John! You are 20 years old
out get_text('John')(20); // out: Hello John! You are 20 years old
out get_text('John')(20); // out: Hello John! You are 20 years old
out get_text('John')(20); // out: Hello John! You are 20 years old
out get_text('John')(20); // out: Hello John! You are 20 years old
out get_text('John')(20); // out: Hello John! You are 20 years old
out get_text('John')(40); // out: Hello John! You are 20 years old


// такая реализация намного быстрее
const var get_text = lambda(name: string, age: int)!(core) {
    'Hello ' + name + '! You are ' + core::to_string(age) + ' years old'
};


// тест производительности вызовоы lambda функции, возвращающей ссылку на другую функцию имеющую доступ к глобальной памяти

out get_text('John', 20); // out: Hello John! You are 20 years old
out get_text('kate', 20); // out: Hello kate! You are 20 years old
out get_text('mira', 30); // out: Hello mira! You are 30 years old
out get_text('John', 20); // out: Hello John! You are 20 years old
out get_text('kate', 20); // out: Hello kate! You are 20 years old
out get_text('mira', 30); // out: Hello mira! You are 30 years old
out get_text('John', 20); // out: Hello John! You are 20 years old
out get_text('kate', 20); // out: Hello kate! You are 20 years old
out get_text('mira', 30); // out: Hello mira! You are 30 years old
out get_text('John', 20); // out: Hello John! You are 20 years old
out get_text('kate', 20); // out: Hello kate! You are 20 years old
out get_text('mira', 30); // out: Hello mira! You are 30 years old
out get_text('John', 20); // out: Hello John! You are 20 years old
out get_text('kate', 20); // out: Hello kate! You are 20 years old
out get_text('mira', 30); // out: Hello mira! You are 30 years old
out get_text('John', 20); // out: Hello John! You are 20 years old
out get_text('kate', 20); // out: Hello kate! You are 20 years old
out get_text('mira', 30); // out: Hello mira! You are 30 years old


// ламбда функцию можно вызвать динамически сразу после её объявления
// но так не рекомендуется делать

out (lambda (x, y) {x + y}) (10, 20); // out: 30
out (lambda (x, y) {x - y}) (10, 20); // out: -10
