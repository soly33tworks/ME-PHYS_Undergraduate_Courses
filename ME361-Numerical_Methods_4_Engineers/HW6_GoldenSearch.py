"""
Uses golden ratio search to find local minima or maxima.
Set the initial guess interval [a,b] and type in your function F(x) manually to use.
"""

from numpy import *
import pandas as pd
import matplotlib.pyplot as plt

def Golden_estimated_error(b, a, x_opt): # Returns True relative absolute error
    r = (sqrt(5)-1)/2
    return (1-r)*((((b-a)/x_opt)**2)**0.5)*100

def F(x, maxima=False): # Example function. Change it to your needs.
    ans = (10-20*(exp(-0.15*x) - exp(-0.5*x)))
    if maxima:
        ans = -ans
    return ans

def conv_plot(rel_changes):
    plt.clf()
    iters = arange(1,len(rel_changes)+1)
    plt.plot(iters, rel_changes, "ro-")
    plt.xlabel('Iteration', fontsize=14)
    plt.ylabel('Estimated maximum error (%)', fontsize=14)
    plt.title('Golden Ratio Search Convergence', fontsize=14)
    plt.grid("on")
    plt.show()

def GoldenRatioSearch(guess_interval, converg_perc=1, max_iter=25, Plot=True):
    errors = []
    cols = ["n", "a", "c", "d", "b", "f(c)", "f(d)", "E_max"]
    n = 0
    a, b = guess_interval[0], guess_interval[1] # Initial interval guess a < minima < b
    while n<max_iter:
        a_old, b_old = a, b
        x_opt = a # Initial x_opt choice for error estimation

        r = (sqrt(5)-1)/2
        c = a+(1-r)*(b-a)
        d = a+r*(b-a)

        if F(d) > F(c):
            b = d
            x_opt = c
        else:
            a = c
            x_opt = d

        error = Golden_estimated_error(b_old, a_old, x_opt)
        
        errors.append(amax(error))
        if n == 0:
            print(pd.DataFrame([n, a_old, c, d, b_old, F(c), F(d), error], cols).T)
        else:
            print(pd.DataFrame([n, a_old, c, d, b_old, F(c), F(d), error], [""]*len(cols)).T)
        if error < converg_perc:
            break
        n+=1

    print("\nThe minima/maxima is located at x =", x_opt)

    if Plot:
        conv_plot(errors)

GoldenRatioSearch(guess_interval=[2, 5], converg_perc=0.5, max_iter=25, Plot=True)