"""
Benchmark of twiss product:
An array of matrices (A) times array of matrices (B)
    C[0] = A[0] * B[0] * AT[0]
    C[1] = A[1] * B[1] * AT[1]
    C[2] = A[2] * B[2] * AT[2]
    ...
"""

import timeit
from types import SimpleNamespace as Namespace

import cffi_twiss_product
import matplotlib.pyplot as plt
import numpy as np
import twiss_product_reduced
from c_api import twiss_product, twiss_product_old
from numba import njit
from opt_einsum import contract

from master_thesis import figure_path


def twiss_matrix_to_namespace(BE):
    twiss = Namespace()
    twiss.beta_x = BE[:, 0, 0]
    twiss.beta_y = BE[:, 2, 2]
    twiss.alpha_x = -BE[:, 0, 1]
    twiss.alpha_y = -BE[:, 2, 3]
    twiss.gamma_x = BE[:, 1, 1]
    twiss.gamma_y = BE[:, 3, 3]
    return twiss


def twiss_array_to_namespace(twiss_array):
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


@njit(cache=True)
def _numba(matrix_array, b0, n, size):
    twiss = np.empty((n, size, size))
    for i in range(n):
        matrix = matrix_array[i]
        twiss[i] = matrix @ b0 @ matrix.T
    return twiss


def numba():
    return twiss_matrix_to_namespace(_numba(matrix_array, b0, n, size))


def numpy_dot():
    twiss = np.empty((n, size, size))
    for i, matrix in enumerate(matrix_array):
        twiss[i] = matrix @ b0 @ matrix.T
    return twiss_matrix_to_namespace(twiss)


def numpy_dot_trick():
    matrix_array.shape = n * size, size
    twiss_tmp = np.dot(matrix_array, b0)
    matrix_array.shape = n, size, size
    twiss_tmp.shape = n, size, size
    twiss = np.einsum("nik,njk->nij", twiss_tmp, matrix_array, optimize="optimal")
    return twiss_matrix_to_namespace(twiss)


def numpy_einsum():
    # BE =opt_einsum.contract('nij,jk->nik', matrix_array, B0, backend='numpy')
    # BE2 = np.einsum('nik,kj->nij', matrix_array, B0, optimize='optimal')
    # BE = np.einsum('nik,njk->nij', BE2, matrix_array, optimize='optimal')
    twiss = np.einsum(
        "nik,kl,njl->nij", matrix_array, b0, matrix_array, optimize="optimal"
    )
    return twiss_matrix_to_namespace(twiss)


def opt_einsum():
    twiss = contract("nik,kl,njl->nij", matrix_array, b0, matrix_array)
    return twiss_matrix_to_namespace(twiss)


def ctypes_full():
    twiss = np.empty((n, size, size))
    twiss_product_old(matrix_array, b0, twiss, "serial")
    return twiss_matrix_to_namespace(twiss)


def ctypes_full_parallel():
    twiss = np.empty((n, size, size))
    twiss_product_old(matrix_array, b0, twiss, "parallel")
    return twiss_matrix_to_namespace(twiss)


def cython_reduced():
    twiss_array = np.empty((8, matrix_array.shape[0]))
    twiss_product_reduced.twiss_product(
        matrix_array.shape[0], matrix_array, b0_vec, twiss_array
    )
    return twiss_array_to_namespace(twiss_array)


def ctypes_reduced():
    twiss_array = np.empty((8, matrix_array.shape[0]))
    twiss_product(matrix_array, b0_vec, twiss_array, "serial")
    return twiss_array_to_namespace(twiss_array)


def ctypes_reduced_parallel():
    twiss_array = np.empty((8, matrix_array.shape[0]))
    twiss_product(matrix_array, b0_vec, twiss_array, "parallel")
    return twiss_array_to_namespace(twiss_array)


def cffi_reduced():
    twiss_array = np.empty((8, n))
    cffi_twiss_product.twiss_product_reduced_serial(matrix_array, b0_vec, twiss_array)
    return twiss_array_to_namespace(twiss_array)


def cffi_reduced_parallel():
    twiss_array = np.empty((8, n))
    cffi_twiss_product.twiss_product_reduced_parallel(matrix_array, b0_vec, twiss_array)
    return twiss_array_to_namespace(twiss_array)


def get_matrix_array(n):
    matrix_array = np.zeros((n, size, size))
    matrix_array[:, 0:2, 0:2] = np.random.rand(n, 2, 2)
    matrix_array[:, 2:4, 2:4] = np.random.rand(n, 2, 2)
    matrix_array[:, 0:2, 4] = np.random.rand(n, 2)
    matrix_array[:, -1, -1] = 1

    # build twiss array
    b0 = np.zeros((size, size))
    b0[0:2, 0:2], b0[2:4, 2:4] = np.random.rand(2, 2), np.random.rand(2, 2)
    b0[1, 0], b0[3, 2] = b0[0, 1], b0[2, 3]
    b0_vec = np.array([b0[0, 0], b0[2, 2], -b0[0, 1], -b0[2, 3], b0[1, 1], b0[3, 3]])
    return matrix_array, b0, b0_vec


if __name__ == "__main__":
    # setup
    functions = [
        numpy_dot,
        # numpy_dot_trick,
        numpy_einsum,
        opt_einsum,
        cython_reduced,
        ctypes_full,
        ctypes_full_parallel,
        ctypes_reduced,
        ctypes_reduced_parallel,
        cffi_reduced,
        cffi_reduced_parallel,
    ]
    size = 5
    n_min, n_max, steps = 10, 10_000, 100
    n_range = np.arange(n_min, n_max, steps)
    process_time = np.empty((len(functions), len(n_range)))

    if True:  # Bench/Check for fixed n
        n = 50000
        print(f"Twiss product of {n} {size}x{size}-matrices:")
        matrix_array, b0, b0_vec = get_matrix_array(n)
        function_0_beta_x = functions[0]().beta_x
        is_all_close = all(
            np.allclose(function().beta_x, function_0_beta_x) for function in functions
        )
        print(f"Equal for all functions: {is_all_close}")

    if False:
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

    if False:
        for function in functions:
            function = profile(function, num=100)
            function()

        exit(0)

    # Plot in dependence of matrix array length n
    for j, n in enumerate(n_range):
        print(f"\rCreating plot... {j / len(n_range) * 100:.0f}%", end="")
        matrix_array, b0, b0_vec = get_matrix_array(n)
        number = 30
        for i, function in enumerate(functions):
            code, setup = (
                f"{function.__name__}()",
                f"from __main__ import {function.__name__}",
            )
            process_time[i, j] = timeit.timeit(code, setup, number=number) / number

    # Plot in dependence of  matrix array length n
    fig, ax = plt.subplots(figsize=(9, 6))

    for i, function in enumerate(functions):
        ax.semilogy(n_range, process_time[i, :], label=function.__name__)
    ax.legend(loc="upper right")
    ax.set(xlabel="Number of matrices", ylabel="seconds per loop")
    fig.tight_layout()
    fig.savefig(figure_path / "benchmark-twiss-calculation.svg")
