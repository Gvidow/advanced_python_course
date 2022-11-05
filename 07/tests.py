import unittest
import matrix
from perf import matrix_mul, matrix_mul_ctypes


class TestMatrixMul(unittest.TestCase):
    def test_matrix_mul(self):
        matrix1 = [
            [1, 2],
            [3, 4]
        ]
        matrix2 = [
            [1],
            [7]
        ]
        matrix_res = [
            [15],
            [31]
        ]

        res1 = matrix.matrix_mul(matrix1, matrix2)

        res2 = matrix_mul(matrix1, matrix2)

        res3 = matrix_mul_ctypes(matrix1, matrix2)

        self.assertListEqual(matrix_res, res1)
        self.assertListEqual(matrix_res, res2)
        self.assertListEqual(matrix_res, res3)

        matrix1 = [
            [2, 1, 5],
            [3, 4, 8],
            [1, 0, 0],
            [2, 2, 2]
        ]
        matrix2 = [
            [1, 1, 0, 0, 4],
            [7, 5, 0, 0, 2],
            [5, 0, 2, 2, 7]
        ]
        matrix_res = [
            [34, 7, 10, 10, 45],
            [71, 23, 16, 16, 76],
            [1, 1, 0, 0, 4],
            [26, 12, 4, 4, 26]
        ]

        res1 = matrix.matrix_mul(matrix1, matrix2)

        res2 = matrix_mul(matrix1, matrix2)

        res3 = matrix_mul_ctypes(matrix1, matrix2)

        self.assertListEqual(matrix_res, res1)
        self.assertListEqual(matrix_res, res2)
        self.assertListEqual(matrix_res, res3)


if __name__ == "__main__":
    unittest.main()
