"""
.. module:: _linalg
    :platform: Unix, Windows
    :synopsis: Helper functions for linear algebra module

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

# Initialize an empty __all__ for controlling imports
__all__ = []


def doolittle(matrix_a):
    """ Doolittle's Method for LU-factorization.

    :param matrix_a: Input matrix (must be a square matrix)
    :type matrix_a: list, tuple
    :return: a tuple containing matrices (L,U)
    :rtype: tuple
    """
    # Initialize L and U matrices
    matrix_u = [[0.0 for _ in range(len(matrix_a))] for _ in range(len(matrix_a))]
    matrix_l = [[0.0 for _ in range(len(matrix_a))] for _ in range(len(matrix_a))]

    # Doolittle Method
    for i in range(0, len(matrix_a)):
        for k in range(i, len(matrix_a)):
            # Upper triangular (U) matrix
            matrix_u[i][k] = float(matrix_a[i][k] - sum([matrix_l[i][j] * matrix_u[j][k] for j in range(0, i)]))
            # Lower triangular (L) matrix
            if i == k:
                matrix_l[i][i] = 1.0
            else:
                matrix_l[k][i] = float(matrix_a[k][i] - sum([matrix_l[k][j] * matrix_u[j][i] for j in range(0, i)]))
                # Handle zero division error
                try:
                    matrix_l[k][i] /= float(matrix_u[i][i])
                except ZeroDivisionError:
                    matrix_l[k][i] = 0.0

    return matrix_l, matrix_u
