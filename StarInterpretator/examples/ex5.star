////////////////////////////////////////////////////
//                   NAME SPACES                  //
////////////////////////////////////////////////////


// create name space
space ('MyVars') {
    var n1 = 10;
    var n2 = 20;
    var n3 = 10 * 3;
}
/*

out n1, n2, n3;  // error

*/

out MyVars::n1, ' ', MyVars::n2, ' ', MyVars::n3;

/////////////////////////////////////////////////////////////////////

var n1 = 'out';
space ('s') {
    var n1 = 'in';
}
out n1; // out: out
out s::n1; // out: in

/////////////////////////////////////////////////////////////////////

space ('n1') space ('n2') space ('n3') {
    var [int] age = 18;
}

out n1::n2::n3::age; // out: 18


