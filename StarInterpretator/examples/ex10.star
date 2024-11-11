////////////////////////////////////////////////////
//                VAR REDEFINITIONS               //
////////////////////////////////////////////////////

// define var and assign value
var a;
a = 10;
out a;

// space variables redefinition
space ('space1') {
    const var a = "Name Age";
    var name = "Ivan";
}

out space1::a;

/*

space1::a = "Pavlov Ivan";

[ execute exception ][ line 17: pos 1 ] In file 'examples/ex10.star'
|
|  space1::a = "Pavlov Ivan";
|  ^^^^^^^^^^
|       |
|       |--->[>] In "a" variable
|       `--->[?] Const variable redefinition!

*/
out space1::name;
space1::name = false;
out space1::name;