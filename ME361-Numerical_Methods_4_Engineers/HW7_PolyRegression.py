"""
Y=X*w
In our homework, the problem was given as a modeling problem for the motion
of an object in freefall with (F)orce and (v)elocity data: F=v*w

w: The weight function containing the constants for polynomial fit.
"""
from matplotlib.pyplot import *
from numpy import *

def Plot_fit(X, Y, w, R2):
    clf()
    x = array(arange(0,12, 0.0001))
    y=0
    for i in range(len(w)):
        y += w[i]*(x**i)
    plot(x,y, "r")
    plot(v,F, "bo")
    xlabel('V [m/s]', fontsize=14)
    ylabel('F [N]', fontsize=14)
    grid("on")
    legend(['F(V)','Data'])
    my_title = "Degree-" +str(len(w)-1) + " Polynomial Fit (R2 = " + f'{R2:.3f}' +")"
    title(my_title)
    show()

def MLE(x, y, N, λ=0.001): # Maximum Likelihood Estimation ==> w=(X_T*X)^-1 * (X_T * Y)
    X = zeros((len(x), N+1))
    λ = 5*identity(N+1)
    for i in range(N+1):
        X[:,i] = x**i
    try:
        w1 = linalg.inv(matmul(X.T,X))
    except:
        print("Using Ridge regression with λ =", λ)
        w1 = linalg.inv(matmul(X.T,X)+λ) # Ridge regression to make the matrix invertible
    w2 = matmul(X.T,y)
    w = matmul(w1,w2)
    Y_pred = matmul(X,w) # Return the results here if you'd like
    RSS, TSS = 0, 0
    for i in range(len(y)):
        RSS += (y[i]-Y_pred[i])**2
        TSS += (y[i]-mean(y))**2
    R2 = float(1 - RSS/TSS)
    return w, R2

def PolyRegress(x, y, n=2):
    w, R2 = MLE(x, y, n)
    print("The weight function: \n", w)
    print("R2 Score: ", R2)
    Plot_fit(v, F, w, R2)

F=array([4.9, 4.8, 4.6, 4.55, 4.5, 4.4, 4.15, 4.05, 3.75, 3.55, 3.0,
   2.6, 2.25, 1.95, 1.05, 0.75, 0.45, 0.15, 0.0])

v=array([0, 1.38, 1.99, 2.2, 2.51, 3.06, 3.77, 4.09, 4.65, 5.51, 6.21,
   7.22, 7.88, 8.53, 9.79, 10.31, 10.93, 11.21, 11.37])

PolyRegress(v, F, n=2)