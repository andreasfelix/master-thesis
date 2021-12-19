"""
Benchmark of matrices accumulation:
The input matrices A[0], A[2], ... of the input array (A)
are accumlated into the ouput array (B) as follows:
    B[0] = A[0] (Frist entry remains unchanged)
    B[1] = A[1] * matrix_array[0]
    B[2] = A[1] * A[0] * B[0]
"""

import timeit
from functools import reduce
from itertools import accumulate

import numba
import numpy as np
from apace.clib import matrix_product_accumulated


def for_loop():
    array = np.empty((n, size, size))
    array[0] = matrices[0]
    for i in range(1, n):
        np.dot(matrices[i], array[i - 1], out=array[i])
    return array


def ft_reduce():
    matrices_list_flattend = [y for x in matrices_list_nested for y in x]
    return [reduce(lambda x, y: y.dot(x), matrices_list_flattend)]


def it_accumulate():
    matrices_list_flattend = [y for x in matrices_list_nested for y in x]
    return np.array(list(accumulate(matrices_list_flattend, lambda x, y: y.dot(x))))


for_loop_numba = numba.njit(fastmath=True)(for_loop)
for_loop_numba.__name__ = "for_loop_numba"


def c_code():
    accumulated = np.empty((n, size, size))
    matrix_product_accumulated(matrices, accumulated, 0)
    return accumulated


if __name__ == "__main__":
    size = 6
    n = 10_000
    n_nested = 10
    functions = [for_loop, ft_reduce, it_accumulate, for_loop_numba, c_code]
    matrices = np.random.rand(n, size, size) / 2.984
    matrices_list = [matrices[i, :, :] for i in range(n)]
    matrices_list_nested = [matrices_list[i : i + n_nested] for i in range(n)[::10]]

    # warm-up numba
    for_loop_numba()

    number = 1
    print("\nProcessing speed:")
    for func in functions:
        time = timeit.timeit(
            f"{func.__name__}()",
            setup=f"from __main__ import {func.__name__}",
            number=number,
        )
        print(f"{func.__name__:20}{time:.9f} s")

    # check allclose
    print("\nCheck numpy allclose:")
    reference = functions[0]()[-1]
    for func in functions:
        is_equal = np.allclose(func()[-1], reference)
        print(f"{func.__name__} {is_equal=}")

    # check random index
    index = 0, 0
    print(f"\nTest element with index {index}:")
    for func in functions:
        print(func()[-1][index])
