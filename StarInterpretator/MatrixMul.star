import "libs/Random.py" as (Random);
import "libs/Time.py" as (Time);

var matrix_width = 100;
var matrix_height = 100;


// generate random matrix
var GenerateRandomMatrix = func(width: int, height: int)!(Random) : list ; {
    var matrix = [];
    for (var i = 0; i < height; i = i + 1;) {
        var row = [];
        for (var j = 0; j < width; j = j + 1;) {
            row = row + [Random::randint(0, 100)];
        }
        matrix = matrix + [row];
    }
    |> matrix;
};

// matrix multiplication
var MatrixMul = func(matrix1: list, matrix2: list)!(core) : list ; {
    var result = [];
    for (var i = 0; i < core::len(matrix1); i = i + 1;) {
        var row = [];
        for (var j = 0; j < core::len(matrix2[0]); j = j + 1;) {
            var sum = 0;
            for (var k = 0; k < core::len(matrix1[0]); k = k + 1;) {
                sum = sum + matrix1[i][k] * matrix2[k][j];
            }
            row = row + [sum];
        }
        result = result + [row];
    }
    |> result;
};


// out matrix
var OutputMatrix = func(matrix: list)!(core) ; {
    for (var i = 0; i < core::len(matrix); i = i + 1;) {
        out matrix[i];
    }
};

Random::seed(1);
var mat_1 = GenerateRandomMatrix(matrix_width, matrix_height);
var mat_2 = GenerateRandomMatrix(matrix_width, matrix_height);

out "Matrix a:";
OutputMatrix(mat_1);
out "Matrix b:";
OutputMatrix(mat_2);
out "Result:";
var st = Time::time();
var res = MatrixMul(mat_1, mat_2);

OutputMatrix(res);
out 'Multiplication took ', Time::time() - st, ' ms';