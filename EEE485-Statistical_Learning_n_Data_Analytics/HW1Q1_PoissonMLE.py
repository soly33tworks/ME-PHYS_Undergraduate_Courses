from numpy import *
import matplotlib.pyplot as plt
from math import factorial

def fact(x):
    ans = []
    for e in x:
        ans.append(factorial(e))
    return ans

def get_data():
    f = open("Q1\data_HW1Q1.txt","r")
    lines = f.readlines()
    data = []
    for line in lines:
        data.append(int(line))

    data = array(data)
    f.close()
    return data

def poisson(data, bins=25):
    plt.hist(data, bins, density=1, label="Data")

    x = arange(0, 24, 1)
    λ = sum(data)/len(data)
    y = (exp(-λ)*(λ**x))/fact(x)
    plt.plot(x,y, 'r', label="λ = "+str(λ))
    plt.title('Poisson distribution MLE')
    plt.xlabel('Time of day')
    plt.ylabel('Probability')
    plt.grid()
    plt.legend()

    plt.show()

data = get_data()
poisson(data)