import ctypes
import os

import numpy as np

__all__ = ['twiss_product', 'twiss_product_old']
SHARED_OBJECTS_PATH = os.path.dirname(__file__) + '/shared_objects/'

twiss_product_modes = {'twiss_product_reduced_serial': 'serial', 'twiss_product_reduced_parallel': 'parallel'}
twiss_product_lib = {}
for name, mode in twiss_product_modes.items():
    twiss_product_lib[mode] = ctypes.CDLL(SHARED_OBJECTS_PATH + f'{name}.so')[f'twiss_product_{mode}']
    twiss_product_lib[mode].restype = None



# from pyprofilers import profile_by_line
# @profile_by_line(exit=0)
def twiss_product(matrix_array, B0vec, twiss, mode):
    n = matrix_array.shape[0]
    matrix_array.__array_interface__['data'],
    args = (
        ctypes.c_int(n),
        np.ctypeslib.as_ctypes(matrix_array),
        np.ctypeslib.as_ctypes(B0vec),
        np.ctypeslib.as_ctypes(twiss)
    )
    twiss_product_lib[mode](*args)


twiss_product_modes_old = {'twiss_product_full_serial': 'serial', 'twiss_product_full_parallel': 'parallel'}
twiss_product_lib_old = {}
for name, mode in twiss_product_modes_old.items():
    twiss_product_lib_old[mode] = ctypes.CDLL(SHARED_OBJECTS_PATH + f'{name}.so')[f'twiss_product_{mode}']
    twiss_product_lib_old[mode].restype = None


# @profile_by_line(exit=1)
def twiss_product_old(A, B, out, mode):
    n = A.shape[0]
    size = A.shape[1]
    args = (
        ctypes.c_int(n),
        ctypes.c_int(size),
        np.ctypeslib.as_ctypes(A),
        np.ctypeslib.as_ctypes(B),
        np.ctypeslib.as_ctypes(out)
    )
    twiss_product_lib_old[mode](*args)
