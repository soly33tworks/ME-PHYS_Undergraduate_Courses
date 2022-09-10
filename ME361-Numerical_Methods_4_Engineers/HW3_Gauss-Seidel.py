"""
Uses Gauss-Seidel iterations to solve a set of linear equations in the form:
a*x1+b*x2+c*x3 = A          [ a  b  c  A ]
d*x1+e*x2+f*x3 = B  ----->  [ d  e  f  B ]
g*x1+h*x2+i*x3 = C          [ g  h  i  C ]

Set the convergence percentage or the max number of iterations as a stopping criteria.
Loop will stop when the closes criteria is met.

Note 1: Number of variables must be equal to number of equations (for ex: its 3 here).
Note 2: Checks for the convergence criteria and checks for zeros in the main diagonal. 
Note 3: Tested for 4x5 matrices but should work for any. The printing will look bad though. 
"""

from numpy import *
import pandas as pd
import matplotlib.pyplot as plt

def check_conv(n, m, arr):
    # Sort rows to satisfy convergence criterion
    max_positions = []
    for i, row in enumerate(arr):
        pos = argmax(row[:-1])
        max_positions.append((pos,i))

    max_positions.sort(key = lambda x: x[0])
    new_arr = empty(shape=(n, m), dtype=float64)
    for i in range(n):
        new_arr[i] = arr[max_positions[i][1]]

    # Check if the convergence criterion is satisfied
    for i, row in enumerate(new_arr):
        if (sum(absolute(row[:-1])) - absolute(row[i])) > absolute(row[i]):
            print("Conv. criterion not satisfied for row ", i)
            return new_arr
    print("Conv. criterion is satisfied, arranged the matrix as: \n", new_arr)
    return new_arr


def check_zeros(n, m, arr):
    for row in range(n):
        for col in range(m-1):
            if (arr[row][col] == 0)&(row==col):
                print("row ", row, " has a 0 in the main diagonal. Terminating...")
                return 1

def Change_perc(new, old): # Returns True relative absolute error
    return ((((new-old)/new)**2)**0.5)*100

def conv_plot(rel_changes):
    plt.clf()
    iters = arange(1,len(rel_changes)+1)
    plt.plot(iters, rel_changes, "ro-")
    plt.xlabel('Iteration', fontsize=14)
    plt.ylabel('Maximum relative change (%)', fontsize=14)
    plt.title('Gauss-Seidel Convergence', fontsize=14)
    plt.grid("on")
    plt.show()

def Gauss_Seidel(Arr, converg_perc=1, max_iter=25, Plot=False):
    n, m = Arr.shape
    if n+1!=m:
        print("The matrix is overconstrained or underconstrained")
        return 0
    Arr = check_conv(n, m, Arr)
    zero_flag = check_zeros(n, m, Arr)
    if zero_flag:
        return 0
    
    for i, row in enumerate(Arr):
        Arr[i] = row/amax(row[:-1])
    
    set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
    print("\n Reduced form: \n",Arr)

    guess = ones(n)
    relative_change = zeros(n)
    relative_changes = []
    iter = 1
    cols = ["n"]
    for var in range(n):
        cols.append("x"+str(var))
    cols.append("E_max")
    init = ones(n+2)
    init[0], init[-1] = 0, 0
    print("\n", pd.DataFrame(init, cols).T)
    while iter < max_iter:
        for row in range(n):
            my_val = guess[row]
            const = Arr[row][-1]
            cache = 0
            #print("----------\nIter =", iter, " ROW =",row)
            for col in range(m-1):
                if col!=row:
                    #print(col, guess[col], Arr[row][col])
                    cache-=guess[col]*Arr[row][col]
            guess[row] = cache + const

            relative_change[row] = Change_perc(guess[row], my_val)
            #print("\n",guess)
        curr = empty(shape=(n+2,), dtype=float64)
        curr[0] = iter
        for i in range(n):
            curr[i+1] = guess[i]
        curr[-1] = amax(relative_change)
        relative_changes.append(amax(relative_change))
        print(pd.DataFrame(curr, [""]*(n+2)).T)
        if amax(relative_change) < converg_perc:
            break
        iter+=1
    if Plot:
        conv_plot(relative_changes)
    

# Example array, should work for other dimensions aswell (must be m=n+1)
Arr = array([[0, 3, -1, 8, 15],
            [10, -1, 2, 0, 6], 
           [-1, 11, -1, 3, 25], 
           [2, -1, 10, -1, -11]])

Gauss_Seidel(Arr, converg_perc=1, max_iter=25, Plot=True)