////////////////////////////////////////////////////
//                    FUNCTIONS                   //
////////////////////////////////////////////////////


var dummy = func() ; {}; // this is basic function

dummy(); // call function dummy
out dummy(); // call function dummy and output result to console (output: None)
/*
|> - return instruction
*/


var sum = func(a: [int, float], b: [int, float]) : [int, float] ; { 
    |> a + b;
};

out sum(10, 3.14);



var math_functs = func(operator: string) : starfunc; {
    if (operator == '+') {
        |> func(a: [int, float], b: [int, float]) : [int, float] ; {
            |> a + b;
        };
    } else if (operator == '-') {
        |> func(a: [int, float], b: [int, float]) : [int, float] ; {
            |> a - b;
        };
    } else if (operator == '*') {
        |> func(a: [int, float], b: [int, float]) : [int, float] ; {
            |> a * b;
        };
    } else if (operator == '/') {
        |> func(a: [int, float], b: [int, float]) : [int, float] ; {
            |> a / b;
        };
    } else if (operator == '%') {
        |> func(a: [int, float], b: [int, float]) : [int, float] ; {
            |> a % b;
        };
    }
};

out math_functs('+')(10, 3.14); // output: 13.14
out math_functs('-')(10, 3.14); // output: 6.86
out math_functs('*')(10, 3.14); // output: 31.4
out math_functs('/')(10, 3.14); // output: 3.184713375796178
//...
out '-' * 50;


var Vector2D = func(_x: [int, float], _y: [int, float])!(Vector2D, core) : namespace ; {
    space ('Vector') ! (_x, _y, Vector2D, core) {
        
        var x = _x;
        var y = _y;

        // vector lenght function
        var lenght = func(x = x, y = y) : [int, float] ; {
            import 'libs/Math.py';
            |> sqrt(pow(x, 2) + pow(y, 2));
        };

        // vector sum function
        var sum = func(v: namespace)!(Vector2D, x, y) : namespace ; {
            |> Vector2D(x + v::x, y + v::y);
        };

        var mull = func(v: namespace)!(Vector2D, x, y) : namespace ; {
            |> Vector2D(x * v::x, y * v::y);
        };

        
    }
    |> Vector;
};


var v1 = Vector2D(10, 20); // space based class instance 'Vector'
var v2 = Vector2D(5, 2);
var v2 = v1::mull(v2);

core::print([v1::x, v1::y]); // object properties not update
core::print([v2::x, v2::y]);

var update = func(v) ;{
    v = 10;
    out v;
};
var x = 0;
update(x);
out x;


space ('Array') ! (core) {

    const var __core__ = core;


    // Namespaces based class object Constructor 
    static const var Array = func(array: list = []) ! (__core__, Array) ; {
        /*
        Array object constructor.

        :param array: list

        :return: NameSpace<Array>
        */

        space('array') ! (
            __core__, array, Array
        ) {
            static var _array = array; // The basic array type

            static const var Append = func(__value__) ! (
                _array
            ) ; {
                /*
                Add a value to the array.

                :param value: any
                */
                _array = _array + [__value__];
            };

            static const var GetAll = func() ! (
                _array
            ) : list ; {
                /*
                Get all the values in the array.

                :return: list
                */

                |> _array;
            };

            static const var Get = func(__index__: int) ! (
                _array
            ); {
                /*
                Get the value at the index.

                :param index: int

                :return: any
                */

                |> _array[__index__];
            };

            static const var Lenght = func() ! (
                __core__, _array
            ) ; {
                /*
                Get the lenght of the array.
                :return: int
                */

                |> __core__::len(_array);
            };

            static const var Add = func(__array__: namespace) ! (
                Array, _array
            ) ; {
                /*
                Add an array to the array.

                :param array: NameSpace<Array>

                :return: NameSpace<Array>
                */

                |> Array(_array + __array__::GetAll());
            };

            static const var SubArray = func(__start__: int, __end__: int) ! (
                Array, _array
            ) ; {
                /*
                Get a sub array from the array.

                :param start: int
                :param end: int

                :return: NameSpace<Array>
                */

                var dummy_array = [];
                for (var[int] i = __start__; i < __end__ + 1; i = i + 1;) {
                    dummy_array = dummy_array + [_array[i]];
                }
                |> Array(dummy_array);
            };
        }
        |> array;

    };

    static const var RandomArray = func(__lenght__: int, __min__: int, __max__: int) ! (
        Array
    ) ; {
        /*
        Generate a random array of length lenght with values between min and max.

        :param lenght: int
        :param min: int
        :param max: int

        :return: NameSpace<Array>
        */

        import 'libs/Random.py' as (Random);
        var dummy_array = [];
        for (var i = 0; i < __lenght__; i = i + 1;) 
            dummy_array = dummy_array + [Random::randint(__min__, __max__)];
        |> Array(dummy_array);
    };
}

// very slow !

var a1 = Array::Array([1, 2, 3, 4, 5]);
var a2 = Array::Array([6, 7, 8, 9, 10]);

var a3 = a1::Add(a2); // summed array a1 with a2
out a3::GetAll(); // [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
var a4 = a3::SubArray(3, 7); // sub array from index 3 to 7
out a4::GetAll(); // [4, 5, 6, 7, 8]


var random_array = Array::RandomArray(0, 0, 100);
out random_array::GetAll();