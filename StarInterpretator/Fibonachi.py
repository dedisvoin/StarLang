from time import time

# Recursive fibonacci
def fib_rec(n: int) -> int:
    if (n == 0): return 0
    if (n == 1): return 1
    return fib_rec(n - 1) + fib_rec(n - 2)

# Iterative fibonacci
def fib_iter(n: int) -> int:
    if (n == 0): return 0
    if (n == 1): return 1
    a = 0
    b = 1
    for i in range(2, n + 1):
        c = a + b
        a = b; b = c
    return c


def main():
    n = 11
    start = time()
    print(fib_rec(n))
    print('Recursive fibonacci took: ', time() - start)

    start = time()
    print(fib_iter(n))
    print('Iterative fibonacci took: ', time() - start)


if __name__ == '__main__':
    main()

    print(0.0283 / 0.0009)