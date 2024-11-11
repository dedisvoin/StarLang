////////////////////////////////////////////////////
//               MORE INSTRUCTIONS                //
////////////////////////////////////////////////////

var[list] arr = [];
// appending to array string values
while (core::len(arr) < 3) var arr = arr + [core::to_int(core::input('enter the text: '))];

out arr, ' ', core::len(arr);


// infinite loop with break
while (true) {
    var i = core::input('enter the text: ');
    if (i == 'exit') break;
}

// infinite loop with continue
var _text = '0';
while (true) {
    var i = core::input(_text + ' number enter: ');
    var _text = core::to_string(core::to_int(_text) + 1);
    var number = core::to_int(i);
    if (number%2==0) continue;
    if (_text == 'exit') break;
    out 'odd number: ', number;
}