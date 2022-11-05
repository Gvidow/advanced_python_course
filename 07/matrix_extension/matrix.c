#include <stdlib.h>
#include <stdio.h>

#include <Python.h>

inline long get(PyObject* m, int i, int j) {
    return PyLong_AsLong(PyList_GetItem(PyList_GetItem(m, i), j));
}

PyObject* matrix_matrix_mul(PyObject *self, PyObject *args) {
    PyObject *matrix1 = NULL, *matrix2 = NULL;
    if (!PyArg_ParseTuple(args, "OO", &matrix1, &matrix2)) {
        printf("ERROR: failed to parse arguments\n");
        return NULL;
    }
    
    int row1 = PyList_Size(matrix1), column1 = PyList_Size(PyList_GetItem(matrix1, 0));
    int row2 = PyList_Size(matrix2), column2 = PyList_Size(PyList_GetItem(matrix2, 0));
    if (column1 != row2) {
        printf("ERROR: matrix multiplication error");
        return NULL;
    }

    long **res = malloc(sizeof(long*) * row1);
    for (int i = 0; i < row1; ++i) {
        res[i] = malloc(sizeof(long) * column2);
    }

    for (int i = 0; i < row1; ++i) {
        for (int j = 0; j < column2; ++j) {
            res[i][j] = 0;
            for (int k = 0; k < column1; ++k) {
                res[i][j] += get(matrix1, i, k) * get(matrix2, k, j);
            }
        }
    }

    PyObject *new_matrix;
    PyObject *new_row;
    new_matrix = PyList_New(row1);
    for (int i = 0; i < row1; ++i) {
        new_row = PyList_New(column2);
        for (int j = 0; j < column2; ++j) {
            PyList_SetItem(new_row, j, Py_BuildValue("L", res[i][j]));
        }
        PyList_SetItem(new_matrix, i, new_row);
    }
    for (int i = 0; i < row1; ++i) {
        free(res[i]);
    }
    free(res);
    return new_matrix;
}

static PyMethodDef methods[] = {
    {"matrix_mul", matrix_matrix_mul, METH_VARARGS, "multiplication of two matrices"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef matrix_module = {
    PyModuleDef_HEAD_INIT, "matrix",
    NULL, -1, methods
};

PyMODINIT_FUNC PyInit_matrix(void) {
    return PyModule_Create(&matrix_module);
}
