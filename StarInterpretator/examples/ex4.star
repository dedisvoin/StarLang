////////////////////////////////////////////////////
//                 FOR INSTRUCTIONS               //
////////////////////////////////////////////////////



var array = [1, 2, 3, 4, 5, 6];


// this ia for instruction to iterate
for ~(array ; var value;) {
    outl value;
}
// out: 12345

out '';

// iterate and type check
for ~(array ; var[int, float] value;) {
    outl value;
}


out '';

/*

var array = [1, 2, 3, 'hello', 5, 6];
for ~(array, var<int, float> value;) {
    outl value;
};

[ execute exception ][ line 20: pos 17 ] In file 'examples/ex4.star'
|
| for ~(array, var<int, float> value;) {
|                 ^^^^^^^^^^^^
|  value to type "string" not to be used with types ['int', 'float']
*/

for (var i = 0; i < 10; var i = i + 1;) outl i;
// out: 0123456789
