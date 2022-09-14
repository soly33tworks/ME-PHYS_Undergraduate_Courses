"""
Draws the root locus plot and prints the stability range for K 
for a given transfer function of form:
tf = num/den
where the numerators/denominators are written as a list in terms of
the polynomial constants they have.
e.g. s**2+ 5*s + 12 = [1, 5, 12]
"""

from numpy import *
import matplotlib.pyplot as plt

# Assumes degree_num <= degree_den

def RLocus(num, den, increment=0.1, max_iter=3000, sensitivity=0.01):
    if len(num) > len(den):
        Den = [0]*(len(num) - len(den))
        Den.extend(den)
        den = Den
    elif len(num) < len(den):
        Num = [0]*(len(den) - len(num))
        Num.extend(num)
        num = Num

    plt.clf()
    plt.xlabel("Re", fontsize=14)
    plt.ylabel("Img", fontsize=14)
    plt.title("Root Locus of the Transfer Function", fontsize=14)
    plt.grid()
    num, den = array(num, float64), array(den, float64)
    Zeros = roots(num)
    Roots = roots(den)
    shared_point = False
    for Root in Roots:
        for Zero in Zeros:
            if abs(Root-Zero)<sensitivity:
                shared_point = True
    if shared_point:
        print("A root intersects with a zero")

    plt.axvline(x=0, color='k', lw=1)
    plt.plot(real(Zeros), imag(Zeros), color='b', marker='o', markersize=10, linestyle='', markerfacecolor='none', label="Zeros")
    plt.plot(real(Roots), imag(Roots), "rX", label="Poles")

    print("Zeros: ", Zeros, "\nRoots: ", Roots)
    Points_list = []
    K = 0
    K_inf = False
    Stable_Ks = []
    while (not K_inf) and (K/increment < max_iter):
        Points = roots(den+K*num)
        Points_list.append(Points)

        for Point in Points:
            for Zero in Zeros:
                if not shared_point:
                    if abs(Point-Zero)<sensitivity:
                        K_inf = True

        if min(real(Points)<=0):
            Stable_Ks.append(K)
        K+=increment

    plt.plot(real(Points_list), imag(Points_list), color='m', marker='o', markersize=2, linestyle='')
    plt.legend()
    # for Points in Points_list:
    #     plt.plot(real(Points), imag(Points), "m.")
    #     plt.pause(0.001)

    my_title = "Root Locus (stable for "+ f'{min(Stable_Ks):.2f}'+ "> K >"+ f'{max(Stable_Ks):.2f}'+")"
    plt.title(my_title, fontsize=14)
    if len(Stable_Ks)>1:
        print("Stability margin: ", f'{min(Stable_Ks):.2f}', "> K >", f'{max(Stable_Ks):.2f}')
    else:
        print("System is not stable.")

# Example systems
# num = [1, -6, 8]
# den = [1, 6, 25]

# num = [10]
# den = [1, 9, 18, 0]

num = [1, 1]
den = [1, 3, 8, 6, 0]

RLocus(num, den)
plt.show()