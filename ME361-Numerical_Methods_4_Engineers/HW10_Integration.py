"""
Numerical integration using Simpson's 1/3 Rule and the Trapezoidal rule with 8 panels.
Note: Plot representation of the integral is not correct.
"""
from numpy import *
import matplotlib.pyplot as plt

def Plot_integral(bounds, panels, vals, i, result, title):
    x = linspace(min(bounds), max(bounds), 1000)
    panels_x, vals_y = [], []
    for k in range(len(panels)-1):
        panels_x.append((panels[k+1]+panels[k])/2)
        vals_y.append((vals[k+1]+vals[k])/2)
    plt.figure(i)
    plt.plot(x, f(x), "b")
    plt.plot(panels, vals, "ro")
    plt.plot(panels_x, vals_y, "mo")
    if title == "S":
        my_title = "Simpson's rule approximation: " + f'{result:.3f}'
    else:
        my_title = "Trapezoidal rule approximation: " + f'{result:.3f}'
    plt.title(my_title)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid("on")
    
def Simpson(bounds, I_e, Plot=False):
    i = linspace(min(bounds), max(bounds), 8+1)
    h=(max(bounds)-min(bounds))/8

    I_s3 = (h/3)*(f(i[0])+4*f(i[1])+2*f(i[2])+4*f(i[3])+2*f(i[4])+4*f(i[5])+2*f(i[6])+4*f(i[7])+f(i[8]))
    print("Simpson's 1/3 rule approximation: ", I_s3)
    if not isinstance(I_e, str):
        print("True Relative Error: ", ((I_e-I_s3)/I_e)*100)
    vals = array([f(i[0]),4*f(i[1]),2*f(i[2]),4*f(i[3]),2*f(i[4]),4*f(i[5]),2*f(i[6]),4*f(i[7]),f(i[8])])/3
    if Plot:
        Plot_integral(bounds, i, vals, 1, I_s3, "S")

def Trapezoidal(bounds, I_e, Plot=False):
    i = linspace(min(bounds), max(bounds), 8+1)
    h=(max(bounds)-min(bounds))/8

    I_tr = (h/2)*(f(i[0])+2*f(i[1])+2*f(i[2])+2*f(i[3])+2*f(i[4])+2*f(i[5])+2*f(i[6])+2*f(i[7])+f(i[8]))
    print("Trap Rule approximation: ", I_tr)
    if not isinstance(I_e, str):
        print("Trap Rule True Relative Error: ", ((I_e-I_tr)/I_e)*100)
    vals = array([f(i[0]),2*f(i[1]),2*f(i[2]),2*f(i[3]),2*f(i[4]),2*f(i[5]),2*f(i[6]),2*f(i[7]),f(i[8])])/2
    if Plot:
        Plot_integral(bounds, i, vals, 2, I_tr, "T")

def f(x):
    return 1/(1+exp(2*x)) # Enter the func. inside the integral here

Exact_solution = -0.5*(log(1+e**4)-log(2))+2 # Exact solution (Optional for comparison, comment it out and use the other option if you dont know)
#Exact_solution = "I dont know"

bounds = [0, 2]
Simpson(bounds, Exact_solution, Plot=True)
Trapezoidal(bounds, Exact_solution, Plot=True)
plt.show()