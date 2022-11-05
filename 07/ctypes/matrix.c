#include <stdlib.h>

long long** matrix_mul(int **matrix1, int row1, int column1, int **matrix2, int row2, int column2) {
    long long **res = malloc(sizeof(long long*) * row1);
    for (int i = 0; i < row1; ++i) {
        res[i] = malloc(sizeof(long long) * column2);
    }
    for (int i = 0; i < row1; ++i) {
        for (int j = 0; j < column2; ++j) {
            res[i][j] = 0;
            for (int k = 0; k < column1; ++k) {
                res[i][j] += (long long) matrix1[i][k] * matrix2[k][j];
            }
        }
    }
    return res;
}

void free_memory(long long **p, int n) {
    for (int i = 0; i < n; ++i) {
        free(p[i]);
    }
    free(p);
}
