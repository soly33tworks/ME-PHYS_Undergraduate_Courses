"""
Includes the data and the evaluation for the brittle 
fracture of polymeric rectangular specimens under bending. 

Check my researchgate page for the relevant report.
"""

from numpy import *
from matplotlib.pyplot import *

"DATA calculated from forces during experiment and geometry"
# Averages of fracture toughness K_IC
u1=3.378 # L=25.9cm, Crack=7cm
u2=3.094 # L=25.9cm, Crack=5cm
u3=3.479 # L=22.4cm, Crack=5cm
u4=4.319 # L=22.4cm, Crack=7cm

# Stdevs of fracture toughness K_IC
d1=0.316
d2=0.613
d3=0.453
d4=0.654

x1 = array(arange(0,9,0.001))
y1 = (1/(d1*sqrt(2*pi)))*(e**(-0.5*(((x1-u1)/d1)**2)))
y2 = (1/(d2*sqrt(2*pi)))*(e**(-0.5*(((x1-u2)/d2)**2)))
y3 = (1/(d3*sqrt(2*pi)))*(e**(-0.5*(((x1-u3)/d3)**2)))
y4 = (1/(d4*sqrt(2*pi)))*(e**(-0.5*(((x1-u4)/d4)**2)))

x = array(arange(0,1,0.001))
F=(sqrt((2/(pi*x))*tan(pi*x/2)))*(0.923+0.199*pow((1-sin(pi*x/2)),4))/cos(pi*x/2)

"Graph 1"
def GaussianDist():
    figure(1)
    plot(x1, y1, "k")
    plot(x1, y2, "r")
    plot(x1, y3, "m")
    plot(x1, y4)

    xlabel('Fracture Toughness [MPa · √m]')
    ylabel('Probability')
    title('Gaussian Distribution for Fracture Toughness for Different Geometries')
    grid("on")
    axis([0, 8, 0, 1.5])
    legend(['L=25.9cm, Crack=7cm', 'L=25.9cm, Crack=5cm', 'L=22.4cm, Crack=5cm', 'L=22.4cm, Crack=7cm'])

"Graph 2"
def Form_fact():
    figure(2)
    plot(x, F)
    grid("on")
    axis([0, 1, 0, 5])
    xlabel('α=a/b')
    ylabel('Form factor function')
    title('Form factor function (for large h/b)')

"Graph 3"
def Stress_intensity_o():
    figure(3)
    P=9.80665
    t=3*(10**-3)
    b=1.8*(10**-2)
    h=(25.9/2)*(10**-2)
    K=(F*((3*P*h)/(t*b**2))*sqrt(pi*x*b))*(10**-6)
    plot(x, K)
    grid("on")
    axis([0, 1, 0, 10])
    xlabel('α=a/b')
    ylabel('K_I [MPa · √m]')
    title('Stress intensity as a function of α')

"Graph 4"
def Stress_intensity_h():
    figure(4)
    F=1.078
    P=9.80665
    t=3*(10**-3)
    b=1.8*(10**-2)
    a=0.2778*b
    x=array(arange(0,30,0.001))
    K=(F*((3*P*x)/(t*b**2))*sqrt(pi*a))*(10**-6)
    plot(x*100, K)
    "axis([0, 40, 0, 10])"
    grid("on")
    xlabel('h (cm)')
    ylabel('K_I [MPa · √m]')
    title('Stress intensity as a function of h')

GaussianDist()
Form_fact()
Stress_intensity_o()
Stress_intensity_h()
show()