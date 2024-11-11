# StarLang

StarLang - простой алгоритмический язык программирования, созданный обучения школьников основам программирования и логического мышления. Он отлично подойдет на замену уже давно устаревшеому языку 'Кумир'.


---


### Для запуска программ на StarLang необходимо:

1. Скачать репозиторий интерпретатора StarLang с Github
2. Можно добавить Star.exe в переменную окружения PATH и в дальнейшем запускать программы из любого места
3. Или можно запускать программы из командной стрки запущенной в папке с интерпретатором.

## Аргументы командной строки
При запуске программы на StarLang можно использовать следующие аргументы командной строки:

- `-h` или `-help` - показать справку
- `-d` - включить режим отладки
- `-print-stages` - показывать этапы компиляции
- `-save-cstar` - сохранить скомпилированный код в `.cstar`, который в последующем можно запустить через python при помощи модуля `cloudpickle`.
- `-print-instructs` - показывать выполняемые инструкции


## Особенности языка

- Возможность как строгой так и динамической типизации
- Простой и понятный синтаксис
- Поддержка базовых алгоритмических конструкций
- Встроенные средства отладки
- Интеграция с Python через механизм предзагрузки памяти
- Возможность написания сторонних модулей на Python


## Ограничения

- Отсутствие поддержки объектно-ориентированного программирования (есть планы на будущее, пока можно использовать пространиства имен, но они не оптимизированны под такие задачи)
- Ограниченный набор встроенных функций и стандартной библиотеки (в будущем стандартная библиотека будет расширяться)
- Отсутствие поддержки многопоточности

## Сообщения об ошибках

Интерпретатор выводит понятные сообщения об ошибках с указанием строки и характера проблемы:

- Синтаксические ошибки
- Ошибки типов
- Ошибки выполнения
- Ошибки доступа к памяти

## Компиляция и выполнение

Процесс выполнения программы проходит следующие этапы:

1. Загрузка исходного кода
2. Лексический анализ, разбиение кода на составные языка - токены
3. Синтаксический разбор, построение абстрактного синтаксического дерева, разбиение на ноды
```
                                                                           var age = 10 - 20 * 5;
                                                                           ^^^^^^^^^ ^^^^^^^^^^^
                                                                            /          \
1) тут бы разбиваем на две ноды   --------------------------------   var age     =   10 - 20 * 5
                                                                                     ^^   ^^^^^^  
                                                                                     /        \
2) тут еще две ноды   ----------------------------------------------------------   10    -    20 * 5
                                                                                              ^^   ^
                                                                                            /       \
3) тут еще две   ----------------------------------------------------------------------   20    *     5
```
7. Генерация простых инструкций
8. Выполнение инструкций

При использовании флага `-save-cstar` создается скомпилированный файл с расширением `.cstar`, который можно использовать для более быстрого запуска программы в будущем.

---

## Синтаксис и примеры кода

#### Объявление переменных
```cs
var age = 10; // объявление и инициальизация переменной
var name = "John";

var test; // объявление переменной без инициализации, при этом переменная будет иметь значение `null`

const var PI = 3.14; // объявление константы
PI = 3.14159; // вызовет ошибку, так как константа не может быть изменена
/*
[ execute exception ][ line 8: pos 1 ] In file 'main.star'
|
|  PI = 3.14159; 
|  ^^^
|   |
|   |--->[>] In "PI" variable
|   `--->[?] Const variable redefinition!
*/

var[int] x = 10; // объявление переменной с указанием ожидаемого типа
var[int] y = 10.5; // вызовет ошибку, так как переменная объявлена как целочисленная, а присвоено значение с плавающей точкой
/*
[ execute exception ][ line ...: pos ... ] In file 'main.star'
|
| var[int] y = 10.5;
|    ^^^^^
|  Value to type `StarType<float>` not to be used with types ['int']
*/

var[int, float] z = 10.5; // объявление переменной с указанием ожидаемых типов

const var a = 0;
const var a = 20; // даже константную переменную можно переинициализировать


static var[int] a = 10; // объявление статической переменной
// ей можно присвоить только тот тип который был указан при объявлении
// если не указать тип, то переменную невозможно будет переприсвоить
// невозможно переопределить статическую переменную, если она уже была объявлена

a = 5; // ошибки не будет, так как переменная объявлена как статическая
a = 10.5; // вызовет ошибку, так как переменная объявлена как целочисленная, а присвоено значение с плавающей точкой

static const var[int] b = 10; // объявление статической константы
// невозможно ни изменить значение, ни переприсвоить, ни переопределить
```

---

#### Простые типы данных
```cs
var a = 10; // int
var b = 10.5; // float
var c = true; // bool
var d = "Hello"; // string
var e = Null; // null

// также существуют сложные типы данных такие как массивы, структуры, функции, lambda-функции и т.д.
```
---

#### Пространства имен
```cs
// пространства имен можно использовать для организации кода
// они могут быть вложенными

// создаются при помощи данного синтаксиса
// space (`выражение возвращающее строку - название пространства`) `тело пространства`

space ("Names") {
    var name1 = "John";
    var name2 = "Doe";
    var name3 = "Jack";
    var name4 = "John";
}

// обращение к переменным из пространства имен
out Names::name1; // John

// out - базовая интсрукция для вывода значение объекта в консоль

Names::name2 = 10; // значение также можно переприсваивать напрямую
out Names::name2; // 10


// также можно создавать вложенные пространства имен

space ("Variables") {
    space ("Strings") {
        var name1 = "John";
        var name2 = "Doe";
    }

    space ("Numbers") {
        var a = 10;
        var b = 20;
    }
}
out Variables::Strings::name1; // John


// в пространства имен можно перекидывать переменные из области внешней памяти
var a = 10;
space ("Variables")!(a) { // перекидываем переменную a в пространство имен Variables
    out a; // 10
}

space ("Variables")! { // при таком синтаксисе вся внешняя область будет перекинута в пространство имен Variables (не рекомендуется так делать)
}
```

---

#### Массивы и генераторы массивов
```cs
var a = []; // объявление пустого массива
var b = [1, 2, 3, 4, 5]; // объявление массива с элементами
var map = [
    [1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1]
]; // объявление двумерного массива

// массивы поддерживают лишь одну арифметическую операцию - сложение (слияние)
// при этом создастся новый массив с элементами из обоих массивов даже с повторениями
var a = [1, 2, 3, 4, 5];
var b = [1, 2, 3, 4, 5];
var c = a + b; // [1, 2, 3, 4, 5, 1, 2, 3, 4, 5]

// при помощи этого можно добавлять к массивам элементы
var arr = [];
arr = arr + [1];
arr = arr + [true];
arr = arr + [10.5];
arr = arr + ["Hello"];
out arr; // [1, true, 10.5, "Hello"]

// также можно создавать массивы при помощи генераторов
var a = ~[0 -> 10]; 
out a; // [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

var c = ~[10 -> 0 : -2]; // создание массива с шагом -2
out c; // [10, 8, 6, 4, 2, 0]

var b = core::range(0, 10);
out b; // [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
// core - стандартное пространство имен, которое содержит в себе множество полезных функций

out core::range_step(10, 0, -2); // [10, 8, 6, 4, 2, 0]


var arr = [0, 1, 2];
var elem = arr[0]; // 0
// также можно обращаться к элементам массива по индексу
// при этом если индекс выходит за пределы массива, то будет выброшено исключение

/*
var a = [1, 2, 3];
out a[5];

[ parse exception ][ line 2: pos 6 ] In file 'main.star'
|
| out a[5];
|      ^^^
|       |
|       `--- is out of range
*/

```

---

#### lambda-функции
```cs
// lambda-функции - это анонимные функции, которым можно передать аргументы а на выходе получать результат

// вот пример простой lambda-функции
var sum = lambda(a, b) {a + b};

out sum(10, 20); // 30

var sum = lambda(a: [int, float], b: [int, float]) : [int, float] {a + b};
// поддерживается строгая типизация
// также можно передавать аргументы по умолчанию
var sum = lambda(a: [int, float] = 0, b: [int, float] = 0) : [int, float] {a + b};


var one = lambda(a: [int, float])!(math, core) : [int, float] {
    core::to_float(math::pow(math::sin(a), 2) + math::pow(math::cos(a), 2))
}; // также возможно перебрасывать переменные из внешней области
// math - стандартное пространство имен, которое содержит в себе множество полезных математических функций
out one(1); // 1.0


// также можно передавать lambda-функции в качестве аргументов
var sum = lambda(a: [int, float], b: [int, float]) : [int, float] {a + b};
var sub = lambda(a: [int, float], b: [int, float]) : [int, float] {a - b};
var mul = lambda(a: [int, float], b: [int, float]) : [int, float] {a * b};
var div = lambda(a: [int, float], b: [int, float]) : [int, float] {a / b};

var calc = lambda(a: [int, float], b: [int, float], f: lambdafunc) : [int, float] {f(a, b)};


out calc(1, 2, sum); // 3
out calc(1, 2, sub); // -1
out calc(1, 2, mul); // 2
out calc(1, 2, div); // 0
// не рекомендуется так делать (не оптимизирована декларация таких функций)

// правильнная запись
var[lambdafunc] sum = lambda(a: [int, float], b: [int, float]) : [int, float] {a + b};

```

---

#### Функции

```cs
var print_array_and  = func(arr: list)!(core) ; { // это функция, которая принимает массив и выводит его длину и сам массив в консоль
    out "array: ", arr; 
    out "len: ", core::len(arr);
};

print_array_and([1, 2, 3]); // вызов функции

```

Опрератор возврата - `|>`;

```cs
var person = func(name: string, age: int) : list ; {
    out "Hello, ", name, "! You are ", age, " years old.";
    |> [name, age];
};
var arr_person = person("John", 30);
```

---

#### Пример использования пространств имен как объектов
```cs
static const var Vec2D = func(_x: [int, float], _y: [int, float])!(Vec2D) : namespace ; {
    space ('vector') !(_x, _y, Vec2D) {
        var x = _x;
        var y = _y; 

        static var add = func(v: namespace)!(Vec2D, x, y) : namespace ; {
            |> Vec2D(v::x + x, v::y + y);
        };

        static var sub = func(v: namespace)!(Vec2D, x, y) : namespace ; {
            |> Vec2D(v::x - x, v::y - y);
        };

        static var mul = func(v: namespace)!(Vec2D, x, y) : namespace ; {
            |> Vec2D(v::x * x, v::y * y);
        };

        static var scalar = func(v: [int, float])!(Vec2D, x, y) : namespace ; {
            |> Vec2D(x * v, y * v);
        };

    }
    |> vector;
};


var v1 = Vec2D(1, 2); // создание объекта
var v2 = Vec2D(5, 5); // создание объекта

out v1::add(v2);      // SpaceObj<vector>

```

---

#### Циклы
```cs
var a = [1, 2, 3, 4, 5];
for (var i = 0; i < core::len(a); i = i + 1) {
    outl a[i];
}
// 12345

// укороченный вариант для итерации по массивам
for ~(a; var value;) {
    outl value;
}
// 12345

// цикл while
var i = 0;
while (i < 10) {
    outl i;
    i = i + 1;
}
// 0123456789

// break и continue
var i = 0;
while (i < 10) {
    i = i + 1;
    if (i % 2 == 0) continue; // если число четное, то пропускаем дальнейшее выполнение итерации
    outl i;
}
// 13579

for ~(~[0 -> 10]; var[int] value;) {
    if (value > 5) break; // если значение больше 5, то выходим из цикла
    outl value;
}
// 012345

```

---

#### Условные операторы
```cs
var a = 10;
if (a > 5) {
    out "a is greater than 5";
} else {
    out "a is less than or equal to 5";
}


var a = "test";
if (a == "test") {
    out "a is test";
} else if (a == "test2") {
    out "a is test2";
} else {
    out "a is not test or test2";
}
```

---

#### Получение ввода от пользователя
```cs

var name = core::input("Enter your name: "); // функция `input` принимает строку и возвращает строку
out "Hello, ", name, "!";

```

---

#### Преобразования типов
```cs

var x = core::to_int("123");        // преобразование строки в число
var y = core::to_float("123.456");  // преобразование строки в число с плавающей точкой
var z = core::to_string(123);       // преобразование числа в строку

out z * core::to_int(x + y);        // число с плавающей точкой в целое число
```

#### Импортирование файлов `.star` как модулей
```cs
//        путь к модулю
//              |
module ("testmodule.star") as (Module); // импортируем файл `testmodule.star` и перемещаем его в пространство имен `Module`

out Module::sum(1, 2); // выводит 3
```


```cs
// testmodule.star
static var sum = lambda(a: [int, float], b: [int, float]) : [int, float] {a + b};
```


---

#### Модуль `Random`
```cs

import "libs/Random.py" as (Random);    // Импортируем модуль `Random.py` и перемещаем его в пространство имен `Random`

out Random::random();                   // выводит случайное дробное число от 0 до 1

out Random::randint(1, 100);            // выводит случайное целое число от 1 до 100

var arr = [10, 20, true, Null, "Hello", 30.5];
out Random::choice(arr);                // выводит случайный элемент из массива

```

---

#### Модуль `Time`
```cs
import "libs/Time.py" as (Time);    // Импортируем модуль `Time.py` и перемещаем его в пространство имен `Time`

Time::sleep(1);                       // Приостанавливает выполнение программы на 1 секунду

var start = Time::time();             // Возвращает текущее время в секундах с начала эпохи Unix

```

---

# Написание сторонних модулей на python
Для написания сторонних модулей на python необходимо создать файл с расширением `.py` и поместить его в папку `libs` в корневой директории проекта (пока, в дальнейшем это будет изменено).

назовем наш модуль `Colors.py`

Структура модуля:
```python
from source.structures.star_functions import PyFunctionWaitArg as PFWA # класс описывающий аргумент функци
from source.structures import star_functions    # модуль для работы управления функциями
from source.structures import star_types        # модуль для работы с типами

FP = star_functions.PyFunctionPack()            # Константа для храниения python функций 
CP = star_functions.PyConstantsPack()           # Константа для храниения python констант
```

давайте добавим пару констант в наш модуль:
```python
from source.structures.star_functions import PyFunctionWaitArg as PFWA
from source.structures import star_functions
from source.structures import star_types

FP = star_functions.PyFunctionPack()
CP = star_functions.PyConstantsPack()

# с помощью метода `add` мы добавляем константы в наш модуль
# константы создаются как объекты класса `PyStarConstant`
# объекты класса `PyStarConstant` имеют следующие поля:

# - `name`  : str                  - имя константы
# - `value` : star_types.StarValue - значение константы

CP.add(
    star_functions.PyStarConstant('green',   star_types.Star_V_String.set_value('\033[32m'))

)
CP.add(
    star_functions.PyStarConstant('reset',   star_types.Star_V_String.set_value('\033[0m'))
)

```

теперь мы можем импортировать наш модуль и использовать константы:
```cs
import "libs/Colors.py" as (Colors);
out Colors::green, "Hello, world!", Colors::reset;
// Hello, world! зеленым цветом
```

попробуем добавить функцию в наш модуль:
```python
from source.structures.star_functions import PyFunctionWaitArg as PFWA
from source.structures import star_functions
from source.structures import star_types

FP = star_functions.PyFunctionPack()
CP = star_functions.PyConstantsPack()

# с помощью метода `add` мы добавляем константы в наш модуль
# константы создаются как объекты класса `PyStarConstant`
# объекты класса `PyStarConstant` имеют следующие поля:

# - `name`  : str                  - имя константы
# - `value` : star_types.StarValue - значение константы

CP.add(
    star_functions.PyStarConstant('green',   star_types.Star_V_String.set_value('\033[32m'))

)
CP.add(
    star_functions.PyStarConstant('reset',   star_types.Star_V_String.set_value('\033[0m'))
)

# например добавим функцию нахождения количества указанных символов в строке
# функция создается как объект класса `PyStarFunction` при помощи декоратора `star_functions.CreatePyFunction`
# он принимает следующие аргументы:

# - `function_pack`  : PyFunctionPack - пакет функций
# - `name`           : str            - имя функции
# - `returned`       : bool           - возвращает ли функция значение
# - `args`           : list[PFWA]     - список аргументов функции

# самаже функция должна принимать два аргумента
# - `args`           : list[star_types.StarValue] - список аргументов функции
# - `error_handler`  : errors.ErrorHandler        - обработчик ошибок
from source.core import errors # не забудем импортировать модуль `errors`

@star_functions.CreatePyFunction(
        FP, 'count', True,
        [PFWA('string', types=[star_types.Star_T_String]), 
         PFWA('char', types=[star_types.Star_T_String])]
)
def _(args: list[star_types.StarValue], error_handler: errors.ErrorHandler) -> star_types.StarValue:
    return star_types.Star_V_Int.set_value(args[0].get_value().count(args[1].get_value()))

```
теперь мы можем импортировать наш модуль и использовать функцию:
```cs
import "libs/Colors.py" as (Colors);
out Colors::count("Hello, world!", "l"); // 3
```

Создание классов и оббъектов классов пока не реализовано.
Также не реализован переброс python обьектов напрямую в язык.

