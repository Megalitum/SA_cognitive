import numpy as np

def eigenvalues(matrix):
    w, _ = np.linalg.eig(matrix)
    return w

def find_cycles(adj : np.array):
    assert adj.shape[0] == adj.shape[1]
    size = adj.shape[0]
    used = np.array([0]*size)
    cycles = list()
    def dfs(root, parent):
        used[root] = 1
        trace = list()
        for num, weight in enumerate(adj[root]):
            if num != root and weight != 0:
                if used[num] == 0:
                    trace.extend(dfs(num, root))
                elif used[num] == 1:
                    trace.append([num])
                else:
                    continue
        used[root] = 2
        for path in reversed(trace):
            if path[0] == root:
                path.reverse()
                cycles.append(path)
                trace.remove(path)
            else:
                path.append(root)
        return trace
    for i in range(size):
        if used[i] == 0:
            dfs(i, -1)
    return cycles

# a = np.array([[-1, -6], [2,6]])
# print(eigenvalues(a))