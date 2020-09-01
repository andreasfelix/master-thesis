"""
Test of twiss product:
An array of matrices (A) times array of matrices (B)
    C[0] = A[0] * B[0] * AT[0]
    C[1] = A[1] * B[1] * AT[1]
    C[2] = A[2] * B[2] * AT[2]
    ...
"""

from types import SimpleNamespace as Namespace
import numpy as np
import timeit
import matplotlib.pyplot as plt
from c_api import twiss_product, twiss_product_old

# from cython_twiss_product_reduced import twiss_product
from pyprofilers import simple_timer as profile


def BE_to_structure(BE):
    twiss = Namespace()
    twiss.beta_x = BE[:, 0, 0]
    twiss.beta_y = BE[:, 2, 2]
    twiss.alpha_x = -BE[:, 0, 1]
    twiss.alpha_y = -BE[:, 2, 3]
    twiss.gamma_x = BE[:, 1, 1]
    twiss.gamma_y = BE[:, 3, 3]
    return twiss


def twiss_array_to_structure(twiss_array):
    twiss = Namespace()
    (
        twiss.beta_x,
        twiss.beta_y,
        twiss.alpha_x,
        twiss.alpha_y,
        twiss.gamma_x,
        twiss.gamma_y,
        *_,
    ) = twiss_array
    return twiss


# @profile_by_line(exit=1)
def dot_app():
    matrix_array.shape = n * size, size
    BE2 = np.dot(matrix_array, B0)
    matrix_array.shape = n, size, size
    BE2.shape = n, size, size
    BE = np.einsum("nik,njk->nij", BE2, matrix_array, optimize="optimal")
    return BE_to_structure(BE)


def einsum():
    # BE =opt_einsum.contract('nij,jk->nik', matrix_array, B0, backend='numpy')
    # BE2 = np.einsum('nik,kj->nij', matrix_array, B0, optimize='optimal')
    # BE = np.einsum('nik,njk->nij', BE2, matrix_array, optimize='optimal')
    BE = np.einsum(
        "nik,kj,nlj->nil", matrix_array, B0, matrix_array, optimize="optimal"
    )
    return BE_to_structure(BE)


def c_full():
    BE = np.empty((n, size, size))
    twiss_product_old(matrix_array, B0, BE, "serial")
    return BE_to_structure(BE)


def c_full_parallel():
    BE = np.empty((n, size, size))
    twiss_product_old(matrix_array, B0, BE, "parallel")
    return BE_to_structure(BE)


import twiss_product_reduced


def cython_c_reduced():
    b0_vec = np.array([B0[0, 0], B0[2, 2], -B0[0, 1], -B0[2, 3], B0[1, 1], B0[3, 3]])
    twiss_array = np.empty((8, matrix_array.shape[0]))
    twiss_product_reduced.twiss_product(
        matrix_array.shape[0], matrix_array, b0_vec, twiss_array
    )
    return twiss_array_to_structure(twiss_array)


def c_reduced():
    b0_vec = np.array([B0[0, 0], B0[2, 2], -B0[0, 1], -B0[2, 3], B0[1, 1], B0[3, 3]])
    twiss_array = np.empty((8, matrix_array.shape[0]))
    twiss_product(matrix_array, b0_vec, twiss_array, "serial")
    return twiss_array_to_structure(twiss_array)


def c_reduced_parallel():
    b0_vec = np.array([B0[0, 0], B0[2, 2], -B0[0, 1], -B0[2, 3], B0[1, 1], B0[3, 3]])
    twiss_array = np.empty((8, matrix_array.shape[0]))
    twiss_product(matrix_array, b0_vec, twiss_array, "parallel")
    return twiss_array_to_structure(twiss_array)


import twiss_product as cffi_twiss_product


# @profile_by_line(exit=1)
def cffi_c_reduced():
    b0_vec = np.array([B0[0, 0], B0[2, 2], -B0[0, 1], -B0[2, 3], B0[1, 1], B0[3, 3]])
    twiss_array = np.empty((8, n))
    cffi_twiss_product.twiss_product_reduced_serial(matrix_array, b0_vec, twiss_array)
    return twiss_array_to_structure(twiss_array)


def get_matrix_array(n):
    matrix_array = np.zeros((n, size, size))
    matrix_array[:, 0:2, 0:2] = np.random.rand(n, 2, 2)
    matrix_array[:, 2:4, 2:4] = np.random.rand(n, 2, 2)
    matrix_array[:, 0:2, 4] = np.random.rand(n, 2)
    matrix_array[:, -1, -1] = 1

    # build twiss array
    B0 = np.zeros((size, size))
    B0[0:2, 0:2], B0[2:4, 2:4] = np.random.rand(2, 2), np.random.rand(2, 2)
    B0[1, 0], B0[3, 2] = B0[0, 1], B0[2, 3]
    b0_vec = np.array([B0[0, 0], B0[2, 2], -B0[0, 1], -B0[2, 3], B0[1, 1], B0[3, 3]])
    return matrix_array, B0, b0_vec


if __name__ == "__main__":
    # setup
    functions = (
        einsum,
        dot_app,
        c_full,
        c_full_parallel,
        cython_c_reduced,
        c_reduced,
        c_reduced_parallel,
        cffi_c_reduced,
    )
    # functions = cffi_c_reduced,
    size = 5
    n_min, n_max, steps = 10, 10000, 100
    n_range = np.arange(n_min, n_max, 100)
    process_time = np.empty((len(functions), len(n_range)))

    if True:  # Bench/Check for fixed n
        n = 50000
        print(f"Twiss product of {n} {size}x{size}-matrices:")
        matrix_array, B0, b0_vec = get_matrix_array(n)
        is_all_close = all(
            np.allclose(function().beta_x, functions[0]().beta_x)
            for function in functions
        )
        print(f"Equal for all functions: {is_all_close}")

        for i, function in enumerate(functions):
            code, setup = (
                f"{function.__name__}()",
                f"from __main__ import {function.__name__}",
            )
            for _ in range(2):
                timer = timeit.Timer(code, setup)
            number, timeit_seconds = timer.autorange()
            print(
                f"{function.__name__:25}{timeit_seconds / number :.6f}s in {number} loops"
            )

        exit(0)

        for function in functions:
            function = profile(function, num=100)
            function()

    exit(0)
    # Plot in dependence of matrix array length n
    for j, n in enumerate(n_range):
        print(f"\rCreating plot... {j / len(n_range) * 100:.0f}%", end="")
        matrix_array, B0, b0_vec = get_matrix_array(n)
        for i, function in enumerate(functions):
            code, setup = (
                f"{function.__name__}()",
                f"from __main__ import {function.__name__}",
            )
            process_time[i, j] = timeit.timeit(code, setup, number=10)

    # Plot in dependence of  matrix array length n
    for i, function in enumerate(functions):
        plt.semilogy(n_range, process_time[i, :], label=function.__name__)
    plt.legend(loc="upper left")
    plt.gca().set(xlabel="Number of matrices", ylabel="seconds per loop")
    plt.tight_layout()
    plt.savefig("test.pdf")
