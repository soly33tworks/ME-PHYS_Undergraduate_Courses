"""
Uses power method with scaling to find the eigenvalue and the
eigenvector of a matrix.

Set the convergence percentage or the max number of iterations as a stopping criteria.
Loop will stop when the closest criteria is met.

Note 1: The convergence percentage checks the eigenvector elements.
Note 2: Tested for 3x3 matrices but should work for any. The printing will look bad though. 
"""

from numpy import *
import pandas as pd
import matplotlib.pyplot as plt

def conv_plot(rel_changes):
    plt.clf()
    iters = arange(1,len(rel_changes)+1)
    plt.plot(iters, rel_changes, "ro-")
    plt.xlabel('Iteration', fontsize=14)
    plt.ylabel('Maximum relative change (%)', fontsize=14)
    plt.title('Power Method Eigenvector Convergence', fontsize=14)
    plt.grid("on")
    plt.show()

def Power_method(Arr, X0, converg_perc=1, max_iter=25, Plot=True):
    n = 0
    eigen_vec = X0

    dim = len(Arr[0])
    relative_change = zeros(dim)
    relative_changes = []
    cols = ["n", "λ_n"]
    for var in range(dim):
        cols.append("x"+str(var))
    cols.append("E_max")
    init = ones(dim+3)
    init[0], init[-1] = 0, 0
    print("\n", pd.DataFrame(init, cols).T)

    while n<max_iter:
        n+=1
        old = eigen_vec
        eigen_vec = matmul(Arr, eigen_vec)
        eigen_val = eigen_vec[0]
        eigen_vec = eigen_vec/eigen_val
        #print(eigen_vec, eigen_val)

        relative_change = absolute(eigen_vec-old)*100
        curr = empty(shape=(dim+3,), dtype=float64)
        curr[0], curr[1] = n, eigen_val
        for i in range(dim):
            curr[i+2] = eigen_vec[i]
        curr[-1] = amax(relative_change)
        relative_changes.append(amax(relative_change))
        print(pd.DataFrame(curr, [""]*(dim+3)).T)
        if amax(relative_change) < converg_perc:
            break
    if Plot:
        conv_plot(relative_changes)

# Example array, should work for other dimensions aswell (must be m=n+1)
Arr = array([[1, 2, 0],
            [-2, 1, 2], 
           [1, 3, 1]])

X0 = array([1, 1, 1]).T

Power_method(Arr, X0, converg_perc=1, max_iter=25, Plot=True)