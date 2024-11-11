////////////////////////////////////////////////////
//            OPERATORS AND OPERATIONS            //
////////////////////////////////////////////////////


var name = "abc" * 10;
out name; // out: abcabcabcabcabcabcabcabcabcabc

/*

var name = 10 * "abc"; // error !
out name; 

[ execute exception ][ line 9: pos 12 ] In file 'examples/ex2.star'
|
| var name = 10 * "abc"; // error !
|            ^^^^^^^^^^
|                 └--- value to types ["int" and "string"] not to be used with operator "*"
*/



var n1 = 10 * 10; out n1;                       // out: 100
var n2 = (3.141592 - 10) * 100; out n2;         // out: -685.8408
var n3 = 2 / 3; out n3;                         // out: 0
var n4 = 2 / 3.0; out n4;                       // out: 0.666666666666666
var n5 = 2.0 / 3; out n5;                       // out: 0.666666666666666



var n1;                                         // not inited variable!
out n1;                                         // out `None`

/*

var test = n1 + 10; 

[ execute exception ][ line 34: pos 12 ] In file 'examples/ex2.star'
|
| var test = n1 + 10;
|            ^^^^^^^
|               └--- value to types ["null" and "int"] not to be used with operator "+"

*/