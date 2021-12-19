import numpy as np

# compile with
# >> pythran -DUSE_XSIMD -fopenmp -march=native pythran_twiss_product.py
# but does not compile for some reason

# pythran export _pyhtran(float[:,5,5], float[5,5], int, int)
def _pyhtran(matrix_array, b0, n, size):
    twiss = np.empty((n, size, size))
    for i in range(len(matrix_array)):
        matrix = matrix_array[i]
        twiss[i, :, :] = matrix @ b0 @ matrix.T
    return twiss
