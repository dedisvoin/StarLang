////////////////////////////////////////////////////
//                VAR REDEFINITIONS               //
////////////////////////////////////////////////////


static var a = 10; // define var with [int] type
/*
    теперь эта переменная может хранить в себе только целые числа,
    и ее нельзя будет переинициализировать другим типом данных.
*/

core::print([a]); // output: 10

a = a * a;

core::print([a]); // output: 100

/*

a = 'string' * a; 

[ execute exception ][ line 14: pos 1 ] In file 'examples/ex11.star'
|
|  a = 'string' * a; // error: [int] type can't be assigned to [string] type
|  ^^
|  |
|  |--->[>] In "a" variable.
|  `--->[?] [ Static ] variable redefinition!
|  `--->[!] Type `StarType<string>` is not equal to type `StarType<int>`.

*/


static const var[float] pi = 3.141592653589793; // define const var with [float] type

/*

var pi = 3.141592653589793; // define var with [float] type

[ execute exception ][ line 35: pos 10 ] In file 'examples/ex11.star'
|
| var pi = 3.141592653589793; // define var with [float] type
|          ^^^^^^^^^^^^^^^^^
|                  |
|                  |--->[>] In "pi" variable
|                  `--->[?] Static variable redefinition!

*/

core::print([pi]);