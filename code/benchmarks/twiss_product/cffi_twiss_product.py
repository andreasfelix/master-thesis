from _twiss_product import ffi, lib


def twiss_product_reduced_serial(matrix_array, b0_vec, twiss_array):
    n = matrix_array.shape[0]
    args = (
        n,
        ffi.cast("double (*)[5][5]", ffi.from_buffer(matrix_array)),
        ffi.cast("double *", ffi.from_buffer(b0_vec)),
        ffi.cast("double (*)[]", ffi.from_buffer(twiss_array)),
    )

    lib.twiss_product_serial(*args)


def twiss_product_reduced_parallel(matrix_array, b0_vec, twiss_array):
    n = matrix_array.shape[0]
    args = (
        n,
        ffi.cast("double (*)[5][5]", ffi.from_buffer(matrix_array)),
        ffi.cast("double *", ffi.from_buffer(b0_vec)),
        ffi.cast("double (*)[]", ffi.from_buffer(twiss_array)),
    )

    lib.twiss_product_parallel(*args)
