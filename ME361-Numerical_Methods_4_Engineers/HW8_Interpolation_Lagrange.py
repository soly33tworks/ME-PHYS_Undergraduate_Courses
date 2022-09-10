"""
Uses Lagrange Interpolating Polynomial of chosen degree n
to interpolate for a given dataset.
"""

from numpy import *
from matplotlib.pyplot import *

def Plot_Inter(X, Y, P, x0, n):
    clf()
    x = linspace(X[0], X[-1], 100)
    y = Interpolate(X, Y, x0=x, n=2)
    plot(X,Y, "bo")
    plot(x, y, "m")
    plot([x0],[P], "ro")
    xlabel('x', fontsize=14)
    ylabel('F(x)', fontsize=14)
    grid("on")
    legend(['Data','L-Interp.', 'Desired Pt.'])
    my_title = "Degree-" +str(n) + " Lagrange Interpolation"
    title(my_title)
    show()

def Interpolate(X, Y, x0, n=2, Plot=False):
    L = []
    for i in range(n+1):
        L_i = 1
        for j in range(n+1):
            if i!=j:
                L_i*=(x0-X[j])/(X[i]-X[j])
        L.append(L_i)

    P=0
    for i in range(len(L)):
        P += L[i]*Y[i]
    if isinstance(x0, int):
        print("f(", f'{x0:.3f}', ") = ", P)
    if Plot:
        Plot_Inter(X, Y, P, x0, n)

    return P

# Data
X=array([1.775, 2.480, 3.655])
Y=array([20, 30, 40])

Interpolate(X, Y, x0=3, n=2, Plot=True) # data, interp point, degree, plot
