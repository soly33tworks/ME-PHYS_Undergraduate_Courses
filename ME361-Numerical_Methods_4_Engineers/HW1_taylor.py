"""
Plot code for the Taylor expansion of f(x) = sqrt(x+b) about x0
"""

from matplotlib.pyplot import *
from numpy import *
clf()

def taylor_sqrtx(x0=20, b=1):
    x = array(arange(0,2.5*x0, 0.0001))
    y = sqrt(x+b)
    y0=[sqrt(x0+b)]*(len(x))
    y1=sqrt(x0+b)+(x-x0)/(2*sqrt(x0+b))
    y2 = sqrt(x0+b)+(x-x0)/(2*sqrt(x0+b))-((x-x0)**2)/(8*sqrt((x0+b)**3))

    plot(x,y)
    plot(x,y0)
    plot(x,y1)
    plot(x,y2)
    xlabel('x')
    ylabel('y')
    p_title = 'Taylor expansion of sqrt(x+'+str(b)+') about x0 = '+str(x0)
    title(p_title)
    legend(['f(x)','P0(x)','P1(x)', 'P2(x)'])
    axis([0, 2.5*x0, 0, 7.5])
    grid("on")

taylor_sqrtx(20, 1)
show()
