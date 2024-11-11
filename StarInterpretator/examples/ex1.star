////////////////////////////////////////////////////
//              BASIC VAR DEFINITIONS             //
////////////////////////////////////////////////////

import 'libs/Colors.py' as (tc);

var name = "Ivan";
const var sername = 'Pavlov';   // define constant value


/*
    create multiline base string value
*/
const var text = "         This is \n       `Starlang`!";                        



var colorama = tc;


out '';
out text; // `out` - basic instruction to print
out ' '*5, colorama::yellow + colorama::underline + 'By: ' + 
                     name + ' ' + sername + colorama::reset;
out '';