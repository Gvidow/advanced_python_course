import time
import ctypes
import random
import matrix


def matrix_mul(matrix1, matrix2):
    return [[sum(matrix1[i][k] * matrix2[k][j] for k in range(len(matrix2)))
             for j in range(len(matrix2[0]))] for i in range(len(matrix1))]


def matrix_mul_ctypes(matrix1, matrix2):
    lib = ctypes.CDLL("ctypes/matrix.so")
    lib.matrix_mul.argtypes = [
                               ctypes.POINTER(ctypes.POINTER(ctypes.c_int)),
                               ctypes.c_int, ctypes.c_int,
                               ctypes.POINTER(ctypes.POINTER(ctypes.c_int)),
                               ctypes.c_int, ctypes.c_int
                               ]
    lib.matrix_mul.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_longlong))

    type1_row = ctypes.c_int * len(matrix1[0])
    type2_row = ctypes.c_int * len(matrix2[0])
    type1 = ctypes.POINTER(ctypes.c_int) * len(matrix1)
    type2 = ctypes.POINTER(ctypes.c_int) * len(matrix2)

    res_c = lib.matrix_mul(
        type1(*(type1_row(*matrix1[i]) for i in range(len(matrix1)))),
        len(matrix1), len(matrix1[0]),
        type2(*(type2_row(*matrix2[i]) for i in range(len(matrix2)))),
        len(matrix2), len(matrix2[0]))
    res = [[res_c[i][j] for j in range(len(matrix2[0]))]
           for i in range(len(matrix1))]

    lib.free_memory.argtypes = \
        [ctypes.POINTER(ctypes.POINTER(ctypes.c_longlong)), ctypes.c_int]
    lib.free_memory.restype = ctypes.c_void_p
    lib.free_memory(res_c, len(matrix1))

    return res


def main():
    matrix1 = [[random.randint(0, 10000) for _ in range(125)]
               for _ in range(150)]
    matrix2 = [[random.randint(0, 10000) for _ in range(100)]
               for _ in range(125)]
    count_test = 40
    start = time.time()
    print("=====    matrix_mul     =====")
    for _ in range(count_test):
        res1 = matrix_mul(matrix1, matrix2)
    print(time.time() - start)

    start = time.time()
    print("\n===== matrix_mul_ctypes =====")
    for _ in range(count_test):
        res2 = matrix_mul_ctypes(matrix1, matrix2)
    print(time.time() - start)

    start = time.time()
    print("\n===== matrix.matrix_mul =====")
    for _ in range(count_test):
        res3 = matrix.matrix_mul(matrix1, matrix2)
    print(time.time() - start)

    assert res1 == res2 == res3


if __name__ == "__main__":
    main()
