import numpy as np

def eigenvalues(matrix):
    w, _ = np.linalg.eig(matrix)
    return w

# a = np.array([[-1, -6], [2,6]])
# print(eigenvalues(a))