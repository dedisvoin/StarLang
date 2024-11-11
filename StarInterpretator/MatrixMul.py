import random
from time import time



random.seed(1)
# random matrix generator
def gen_matrix(width: int, height) -> list:
    return [[random.randint(0, 100) for i in range(width)] for j in range(height)]

# matrix multiplication
def mul_matrix(m1: list, m2: list) -> list:
    if (len(m1[0]) != len(m2)):
        raise ValueError("Matrixes are not compatible")
    return [
        [sum([m1[i][k] * m2[k][j] for k in range(len(m1[0]))]) for j in range(len(m2[0]))] for i in range(len(m1))
    ]

# output matrix
def print_matrix(m: list) -> None:
    for i in m:
        print(i)


matrix_width = matrix_height = 100
mat_1 = gen_matrix(matrix_width, matrix_height)
mat_2 = gen_matrix(matrix_width, matrix_height)

print('Matrix a:')
print_matrix(mat_1)
print('Matrix b:')
print_matrix(mat_2)
st = time()
res = mul_matrix(mat_1, mat_2)
print('Matrix a * b:')
print_matrix(res)
print('Multiplication took', time() - st)
        
