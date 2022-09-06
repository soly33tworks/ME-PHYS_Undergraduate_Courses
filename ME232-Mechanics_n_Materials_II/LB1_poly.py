"""
Includes the data and the evaluation for hardness 
testing experiment for polymers.
Relevant method: Shore A hardness, ASTM D2240 test standard

Check my researchgate page for the relevant report.
"""

from numpy import *
from matplotlib.pyplot import *
clf()

"1) DATA"
"Constants and the Young's modulus eqs"
def E(s):
    d=0.79 # mm
    C1=0.549 # N
    C2=0.07516 # N
    C3=0.025 # mm
    return (3/(4*d*C3))*((C1+C2*s)/(100-s))

"Specimens"
S1=[15.5, 15.5, 15.5, 15.5, 15.5, 15.5, 14, 14, 15, 15, 15, 15, 15, 15, 15, 
    15, 14, 14, 14, 14, 15, 15, 15.5, 15.5, 15.5, 15.5]

S2=[31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 
    31, 31, 31, 31, 31, 31, 31, 31]

S3=[82, 83, 83, 83, 83, 83, 83, 83, 82, 82, 83, 83, 83, 83, 83, 83, 83, 
    83, 83, 83, 82, 82, 81, 81, 82, 82]

n_samples = len(S1)

"2) MEAN VALUES"
S1u=0
S2u=0
S3u=0

i=0
for i in range(n_samples):
    S1u+=S1[i]/n_samples
    S2u+=S2[i]/n_samples
    S3u+=S3[i]/n_samples

S1E = E(S1u) 
S2E = E(S2u)
S3E = E(S3u)

"3) STANDARD DEVIATION"
S1d=0
S2d=0
S3d=0

i=0
for i in range(n_samples):
    S1d+=((S1[i]-S1u)**2)/n_samples
    S2d+=((S2[i]-S2u)**2)/n_samples
    S3d+=((S3[i]-S3u)**2)/n_samples
    
S1d=S1d**0.5
S2d=S2d**0.5
S3d=S3d**0.5

"4) PROBABILITY GRAPHS"
def prob():
    x = array(arange(0,100,0.001))
    y1 = (1/(S1d*sqrt(2*pi)))*(e**(-0.5*(((x-S1u)/S1d)**2)))
    y2 = (1/(S2d*sqrt(2*pi)))*(e**(-0.5*(((x-S2u)/S2d)**2)))
    y3 = (1/(S3d*sqrt(2*pi)))*(e**(-0.5*(((x-S3u)/S3d)**2)))

    figure(1)
    plot(x, y1, "k")
    plot(x, y2, "r")
    plot(x, y3)

    xlabel('Shore A Hardness (s)')
    ylabel('Probability')
    title('Gaussian Distribution of Shore A Hardness for the Specimens')
    grid("on")
    axis([0, 100, 0, 0.7])
    legend(['Specimen 1', 'Specimen 2', 'Specimen 3'])

"5) OTHER GRAPHS"
def other():
    x = array(arange(0,100,0.001))    
    y = E(x)   

    figure(2)
    plot(x, y)
    plot([S1u], [S1E], "rx")
    plot([S2u], [S2E], "gx")
    plot([S3u], [S3E], "mx")

    xlabel('Shore A hardness')
    ylabel('Elastic Modulus (MPa)')
    title('Modulus of elasticity as a function of Shore A hardness value')
    grid("on")
    axis([0, 100, 0, 35])
    legend(['Shore A function','Specimen 1', 'Specimen 2', 'Speciment 3'])

prob()
other()
show()