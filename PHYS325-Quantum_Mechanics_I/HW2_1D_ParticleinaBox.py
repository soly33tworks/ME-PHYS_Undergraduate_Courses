"""
Code for simulating a particle in an infinite 1D quantum well
extending from x=-a/2 to x=a/2.

Initial state = 0 for x<0 and x>a/2
                A*x*(x-a/2) for 0<x<a/2
"""

from matplotlib.pyplot import *
from numpy import *
clf()

h = (6.62607004*(10**-34))/(2*pi)
m = 9.10938356*(10**-31)
a = 1
A = sqrt(30*((2/a)**5))



"1) Fig.1: Wavefunction at t=0  (Ψ(x,0))"
def wavefunc_n_amplitude():
    figure(1)
    x_0 = array(arange(0, a/2, 0.0001))
    x_01 = array(arange(-1, 0, 0.001))
    x_02 = array(arange(a/2, 1, 0.001))

    Ψ_0=A*x_0*(x_0-a/2)
    Ψ_01=x_01*0
    Ψ_02=x_02*0
    plot(x_0,Ψ_0, "m")
    plot(x_01,Ψ_01, "m")
    plot(x_02,Ψ_02, "m")

    xposition = [-a/2, a/2]
    for xc in xposition:
        axvline(x=xc, color='r', linestyle='-')

    xlabel('x/a')
    ylabel('Ψ(x,0)')
    title("Wavefunction at t=0  (Ψ(x,0))")
    axis([-0.75, 0.75, -4, 4])
    grid("on")

    "2) Fig.2: Probability density at t=0 (|Ψ(x,0)|²)"
    figure(2)
    p_0=(abs(Ψ_0))**2
    p_01=(abs(Ψ_01))**2
    p_02=(abs(Ψ_02))**2
    plot(x_0, p_0, "b")
    plot(x_01, p_01, "b")
    plot(x_02, p_02, "b")

    xposition = [-a/2, a/2]
    for xc in xposition:
        axvline(x=xc, color='r', linestyle='-')

    xlabel('x/a')
    ylabel('|Ψ(x,0)|²')
    title("Probability density at t=0 (|Ψ(x,0)|²)")
    axis([-0.75, 0.75, -4, 4])
    grid("on")


"3) Full wave-function solution"
def Time_evolution(τ=0.5):
    figure(3)
    
    clf()
    x = array(arange(-a/2, a/2, 0.0001))
    S_ev=0
    S_odd=0
    E_1=((pi**2)*(h**2))/(2*m*(a**2))
    "E_n = n²(E_1)"
    t=(h/E_1)*τ # τ = planck const / ground state energy

    for i in range(2,11,2):
        n=i
        S_ev+=(2/pi)*(1/(n**3))*(cos(n*pi*0.5)-1)*(sin(n*pi*x/a))*exp(-(1j*(E_1*(n**2))*t)/h)

    for i in range(2,11,2):
        n=(i-1)
        S_odd+=((1/(2*(n**2)))-(2/(pi*(n**3)))*(sin(n*pi*0.5)))*(cos(n*pi*x/a))*exp(-(1j*(E_1*(n**2))*t)/h)

    S = [a + b for a, b in zip(S_odd, S_ev)]

    Ψ = []
    p = []
    for i in range(len(S)):
        Ψ.append(((1/(pi**2))*(2**3)*sqrt(30))*(sqrt(2/a))*(S[i]))

    for i in range(len(Ψ)):
        p.append((abs(Ψ[i]))**2)

    plot(x,p, "b")

    x_1 = array(arange(-1, -a/2, 0.001))
    x_2 = array(arange(a/2, 1, 0.001))
    Ψ_1=x_1*0
    Ψ_2=x_2*0
    plot(x_1,Ψ_1, "b")
    plot(x_2,Ψ_2, "b")

    xposition = [-a/2, a/2]
    for xc in xposition:
        axvline(x=xc, color='r', linestyle='-')
    xlabel('x/a')
    ylabel('|Ψ(x,t)|²')
    plot_title = "Amplitude of the wavefunction (t = " + str(τ) + "τ)" 
    title(plot_title)
    axis([-0.75, 0.75, -4, 4])
    grid("on")
    pause(0.1)

wavefunc_n_amplitude()
for i in range(0,21):
    Time_evolution(i/20)

show()