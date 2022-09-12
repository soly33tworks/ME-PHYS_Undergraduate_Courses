"""
Uses Runge-Kutta order 4 to extract a function for 
solving the initial-value problems of differential equations.

Given: y(t0)=y0 and dy/dt
"""

from matplotlib.pyplot import *
from numpy import *

def dydt(t,y): # dy/dt, change here to use other functions
    return (y + (t**2)-2)/(t+1)

def Runge_Kutta4(t0, y0, h, steps, my_title, exact=False): #h: step size
    Y, T = [y0], [t0]
    for i in range(steps): # Generate the range of t
        T.append((i+1)*h)

    for i in range(steps):
        k1 = dydt(T[i],Y[i])
        k2 = dydt(T[i]+0.5*h, Y[i]+0.5*k1*h)
        k3 = dydt(T[i]+0.5*h, Y[i]+0.5*k2*h)
        k4 = dydt(T[i]+h, Y[i]+k3*h)
        y_new = Y[i] + (h/6)*(k1+2*k2+2*k3+k4)
        Y.append(y_new)

    my_legend = ['4th Order RK']
    if exact:
        t = array(arange(0,steps*h, 0.001)) # enter exact solution here for comparison
        y_exact = (t**2)+2*t+2-2*(t+1)*log(t+1)
        plot(t, y_exact, "r")
        my_legend = ['Exact Solution','4th Order RK']
        
    plot(T,Y, "bo")
    xlabel('t')
    ylabel('y')
    grid("on")
    title(my_title)
    legend(my_legend)
    show()

plot_title = 'Plots of dy/dt = (y+t²-2)/(t+1)'
Runge_Kutta4(t0=0, y0=2, h=0.4, steps=5, my_title=plot_title, exact=True)
