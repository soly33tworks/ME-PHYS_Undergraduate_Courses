"""
Code for using Newton Raphson method for root finding.
In this example, f(x) = 3*exp(-0.15*x)-10*exp(-0.5*x)
"""

from matplotlib.pyplot import *
from numpy import *

def f(x): # Returns f(x), manually written
    return (3*exp(-0.15*x))-(10*exp(-0.5*x))

def f_d(x): # Returns the 1st derivative of f(x), manually written
    return (-0.45*exp(-0.15*x))+(5*exp(-0.5*x))

def Error(guess, truVal): # Returns True relative absolute error
    if truVal == nan:
        return nan
    return (((guess-truVal)/truVal)**2)**0.5

def plot_errs(errs, iters):
    if not isnan(errs[0]):
        clf()
        plot(iters, errs, "r.-")
        xlabel('Iteration', fontsize=14)
        ylabel('True relative error (%)', fontsize=14)
        grid("on")
        title('Newton-Raphson convergence performance', fontsize=14)
        show()
    else:
        print("Enter true value to display the plot")

# Finds the root based on the iteration count and initial guess. Shows the true error if it is given
def NewtonRaphson(n, x_0, tru_val=NaN):
    errs, iters = [], []
    print("Beginning with initial guess x_0 = ", x_0, ":\n")
    x_n = x_0
    for i in range(n):
        print("\nIteration ", i, "\nx_n: ", x_n, "\nf(x_n): ", f(x_n), "\nf'(x_n): ", f_d(x_n))
        err = Error(x_n, tru_val)*100
        if not isnan(err):
            print("True Relative Error(%) = ", Error(x_n, tru_val)*100)
        x_n = x_n-((f(x_n))/(f_d(x_n)))
        errs.append(err)
        iters.append(i)
    plot_errs(errs, iters)

NewtonRaphson(n=10, x_0=3.4, tru_val=(1/0.35)*log(10/3)) # enter "nan" in tru_val if it is not known

