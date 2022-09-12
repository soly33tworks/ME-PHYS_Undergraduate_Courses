"""
Code to calculate machine epsilon of your computer in Python
"""

s=1
t=0
for i in range(1,100):
    s=0.5*s
    t=s+1
    if t<=1:
        s=2*s
        print("k = ", i, "\nepsilon = ", s)
        break