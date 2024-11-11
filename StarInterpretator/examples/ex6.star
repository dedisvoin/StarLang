
////////////////////////////////////////////////////
//                   NAME SPACES                  //
////////////////////////////////////////////////////


// core - standart star lang space

out core::input("Enter your name: "); // echo input
// out: you name

out core::type(1); // print type of 1
// out: int

out core::type(core::input);
// out: pyfunc


/*
    move to math namespace sin function to global namespace as sin
*/
var[pyfunc] sin = math::sin; 

out sin(math::pi/2); // print 1.0
out math::sin(math::pi/2); // print 1.0


// another way to do the same thing any type convert to int
var i1 = core::to_int('1');;
var i2 = core::to_int('3.1415');
var i3 = core::to_int(10);
var i4 = core::to_int(6.2831);

out i1; out i2; out i3; out i4; // print 1 3 10 6



out core::to_float(.32); // print 0.32

out core::to_string(10) + core::to_string(10); // print 1010
