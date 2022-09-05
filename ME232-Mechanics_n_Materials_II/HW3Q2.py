"""
Book: Dowling, Mechanical Behavior of Materials: Engineering Methods for Deformation, Fracture, and Fatigue 4th edition

CH4, Q8:
Engineering stress/strain data from a tension test on AISI 4140 steel tempered at 649◦C
(1200◦F) are listed in Table P4.8. The diameter before testing was 10 mm, and after fracture
the minimum diameter in the necked region was 6 mm. Determine the following: elastic
modulus, 0.2% offset yield strength, ultimate tensile strength, percent elongation, and percent
reduction in area.

S: Stress
P: Force
e: Strain
A: Area
"""

from numpy import *
from matplotlib.pyplot import *
from shapely.geometry import LineString
clf()

def MLE(x, y, N, λ=0.01): # w=(X_T*X)^-1 * (X_T * Y), w=[1/n * log(1/H), 1/n]
    X = zeros((len(x), N+1))
    for i in range(N+1):
        X[:,i] = x**i
    try:
        w1 = linalg.inv(matmul(X.T,X))
    except:
        w1 = linalg.inv(matmul(X.T,X)+λ) # Ridge regression to make the matrix invertible
    w2 = matmul(X.T,y)
    w = matmul(w1,w2)
    Y = matmul(X,w)
    return w, Y

### Data ###
d=10*(10**-3) # Specimen diameter
A=pi*(d**2)/4 # Area

S=array([0, 202, 403, 587, 785, 822, 836, 832, 
   829, 828, 864, 897, 912, 918, 915, 899, 
   871, 831, 772, 689, 574])*(10**6) # Stress data

e1=array([0, 0.099, 0.195, 0.283, 0.382, 0.405, 0.423, 
    0.451, 0.887, 1.988, 2.94, 4.51, 5.96, 
    8.07, 9.94, 12.04, 13.53, 15.03, 16.70,
    18.52, 20.35])/100 # Strain data (given as percentage)

n_samples = len(e1)
############

######### A - Engineering/True Stress #########
P = zeros(n_samples)
for i in range(0, n_samples): # Force = Stress x Area
    P[i]=S[i]*A

E=(S[2]-S[1])/(e1[2]-e1[1]) # take derivative to find slope (Euler's const)
print("Young's modulus (E) = ", f'{E/(10**9):.3f}', "GPa")

S_off = zeros(n_samples)
for i in range(0, n_samples):
    S_off[i]=-0.002*E+E*e1[i] # Find the Modulus of Elasticity (E)

S_t=zeros(n_samples)
for i in range(0, n_samples):
    S_t[i]=S[i]*(1+e1[i]) # True stress

e1_t = zeros(n_samples)
for i in range(0, n_samples):
    e1_t[i]=log(1+e1[i]) # True strain


plot(e1, S/(10**6), label='σ_engineering') 
plot(e1_t, S_t/(10**6), label='σ_true')

######### B - 0.02 Offset Intercept for Yield Strength #########
plot(e1, S_off/(10**6), label='0.02 offset strain intercept')
line1 = LineString(column_stack((S/(10**6), e1)))
line2 = LineString(column_stack((S_off/(10**6), e1)))
intersect = line1.intersection(line2)
print("Yield Strength = ", f'{intersect.x:.3f}', "MPa")
annotate('Yield Point', xy =(intersect.y, intersect.x),
                xytext =(intersect.y+0.02, intersect.x-max(S/(10**6))/6), 
                arrowprops = dict(facecolor ='green',shrink = 0.05))
plot(intersect.y, intersect.x, 'ro')

######### C - Ramberg-Osgood Model #########
# Linear reg. on the equation Ramberg-Osgood eqs: (S/E)+(S**(1/n))*((1/H)**1/n) (on the linearized version)
w, Y = MLE(log(S[1:]), log(e1[1:]-S[1:]/E), 1)
n = 1/w[1]
H = exp(-w[0]*n)
print("Ramberg-Osgood paramters: n =", n, " H =", H)
S_rayosg = linspace(0, max(S_t)+200*(10**6), 40)
e_rayosg = (S_rayosg/E)+(power(S_rayosg,(1/n)))*(power((1/H),1/n))
plot(e_rayosg, S_rayosg/(10**6), 'm', label = "Ramberg-Osgood Model Fit")

xlabel('Strain')
ylabel('Stress (MPA)')
title('AISI 4140 Tempered Steel Stress-Strain (and 0.002 offset)')
axis([0, max(e1)+0.05*max(e1), 0, max(S_t/(10**6))+25]) # Sets the borders, change if you want
grid("on")
legend()

show()
