////////////////////////////////////////////////////
//            BASIC VAR DEFINE TYPING             //
////////////////////////////////////////////////////


var[string] name = "Jon"; // definition waited <base string type> value

var[int, float] number = 3.141592; // waited <int or float walue>

/*

var <string> age = 10; 

[ execute exception ][ line 10: pos 20 ] In file 'examples/ex3.star'
|
| var <string> age = 10;
|     ^^^^^^^^       ^^
|  value to type "int" not to be used with types ['string']

*/

var [auto] array = [1, 2, 3, "10", 5, true, 7, 8, 8];    // succes !
// array type is auto detected - <list>

var [auto] element = array[0];                           // succes !
out element;                                            // out: 1
out array[5];                                           // out: True

out array[0] == array[-1];                              // out: False

