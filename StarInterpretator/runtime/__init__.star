/*
   standart types
*/
typedef static int =           '0x00000000';
typedef static string =        '0x00000001';
typedef static float =         '0x00000002';
typedef static bool =          '0x00000003';
typedef static list =          '0x00000006';  


/*
    namespace type used to represent a namespace
    namespace is a special type that allows you to create a namespace
    that can be used to group related functions and variables together
*/

typedef static namespace =     '0x00000004';


// auto type
typedef static auto =          '0x00000005';





// null type used to represent no value
typedef static null =          '0x00000007';
static const var[null] Null;


// function type used to represent a python function
typedef static pyfunc =        '0x00000008';

// lambda type used to represent a lambda function
typedef static lambdafunc =    '0x00000009';

typedef static starfunc =      '0x0000000A';

// math namespace
space ('math') {
    import ['libs/Math.py'];

    // math constants
    static const var[float] pi = 3.141592653589793;
    static const var[float] e =  2.718281828459045;

    // base math function impleementation to python
    static const var[pyfunc] sin        = sin;
    static const var[pyfunc] cos        = cos;
    static const var[pyfunc] tan        = tan;
    static const var[pyfunc] asin       = asin;
    static const var[pyfunc] acos       = acos;
    static const var[pyfunc] atan       = atan;
    static const var[pyfunc] sqrt       = sqrt;
    static const var[pyfunc] pow        = pow;
    static const var[pyfunc] abs        = abs;
    static const var[pyfunc] atan2      = atan2;

    // math anonymous functions
    static const var[lambdafunc] distance = lambda (
        x1: [int, float] = 0,
        y1: [int, float] = 0,
        x2: [int, float] = 0,
        y2: [int, float] = 0
    ) : [float, int] {
        /*
        Calculate the distance between
        two points in 2D space.

        :param x1: [int, float]
        :param y1: [int, float]
        :param x2: [int, float]
        :param y2: [int, float]

        :return: [float, int]
        */

        sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2))
    };

    static const var[lambdafunc] point_in_rect = lambda (
        rect_x: [int, float] = 0,
        rect_y: [int, float] = 0,
        rect_width: [int, float] = 0,
        rect_height: [int, float] = 0,
        point_x: [int, float] = 1,
        point_y: [int, float] = 1
    ) : bool {
        /*
        Check if a point is inside a rectangle.

        :param rect_x: [int, float]
        :param rect_y: [int, float]
        :param rect_width: [int, float]
        :param rect_height: [int, float]
        :param point_x: [int, float]
        :param point_y: [int, float]

        :return: bool
        */

        point_x >= rect_x && point_x <= rect_x + rect_width && point_y >= rect_y && point_y <= rect_y + rect_height
    };

    static const var[lambdafunc] point_in_circle = lambda (
        circle_x: [int, float] = 0,
        circle_y: [int, float] = 0,
        circle_radius: [int, float] = 0,
        point_x: [int, float] = 1,
        point_y: [int, float] = 1
    ) : bool {
        /*
        Check if a point is inside a circle.

        :param circle_x: [int, float]
        :param circle_y: [int, float]
        :param circle_radius: [int, float]
        :param point_x: [int, float]
        :param point_y: [int, float]

        :return: bool
        */

        distance(circle_x, circle_y, point_x, point_y) <= circle_radius
    };

    static const var[starfunc] fibonacci = func(n: int) : int ; {
        var n1 = 1; var n2 = 1; var n3;
        while (n - 2 > 0) {
            n3 = n1;
            n1 = n2; n2 = n1 + n3;
            n = n - 1;
        }
        |> n2;
    };
}


// standart functions namespace
space ('core') {
    import ['libs/Std.py'];
    static const var[pyfunc] input      = input;
    static const var[pyfunc] type       = type;
    static const var[pyfunc] sizeof     = sizeof;
    static const var[pyfunc] len        = len;
    static const var[pyfunc] to_int     = to_int;
    static const var[pyfunc] to_float   = to_float;
    static const var[pyfunc] to_string  = to_string;
    static const var[pyfunc] copy       = copy;

    static const var[starfunc] print = func(_args: list, _sep: string = ' ')!(len, to_string) ; {
        for (static var[int] i = 0; i < len(_args); i = i + 1;) {
            if (i == len(_args) - 1) {
                outl to_string(_args[i]);
            } else outl to_string(_args[i]) + _sep;
        }
        out '';
    };
}





