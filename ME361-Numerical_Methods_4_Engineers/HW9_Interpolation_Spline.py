"""
Uses Natural Cubic Spline Interpolation to interpolate for a given dataset.
"""

from matplotlib.pyplot import *
from numpy import *

def get_interval(data_x, x): # Finds which interval is desired to draw spline for
    for i in range(len(data_x)-1):
        if (data_x[i] <= x):
            x_L = data_x[i]
            k = i
    return k, x_L

# Cubic spline: P_3,k = ak*(x-xk_L)**3 + bk*(x-xk_L)**2 + ck*(x-xk_L) + dk
def Spline(data_x, x_arr, weight_func):
    a, b, c, d = weight_func[0], weight_func[1], weight_func[2], weight_func[3]
    P_k = []
    if isinstance(x_arr, int) or isinstance(x_arr, float):
        x = x_arr
        k, x_L = get_interval(data_x, x)
        return a[k]*(x-x_L)**3 + b[k]*(x-x_L)**2 + c[k]*(x-x_L) + d[k]

    for i, x in enumerate(x_arr):
        k, x_L = get_interval(data_x, x)
        P_k.append(a[k]*(x-x_L)**3 + b[k]*(x-x_L)**2 + c[k]*(x-x_L) + d[k])
    
    return P_k

def Plot_spline(data_x, data_y, x0, weight_func):
    clf()
    x = linspace(data_x[0], data_x[-1], 150)
    plot(x, Spline(data_x, x, weight_func), "b")
    plot(data_x, data_y, "ro")
    plot(x0, Spline(data_x, x0, weight_func), "mo")
    xlabel('x', fontsize=14)
    ylabel('y', fontsize=14)
    title('Cubic spline interpolation', fontsize=14)
    legend(["Interpolation", "Data", "Interpolation point"])
    grid("on")
    show()

def Natural_Spline(x, y, x_0, Plot=False):
    n_regions = len(x)-1
    h=[]
    for i in range(n_regions):
        h.append(x[i+1]-x[i])
    
    # RHS of the recurrence formula (X1*C = Y1 where C's are the 2nd derivatives)
    Y1=[]
    X1=[]
    for i in range(1,n_regions):
        Y1.append(6*(((y[i+1]-y[i])/h[i])-((y[i]-y[i-1])/h[i-1])))
        X1.append([h[i-1], 2*(h[i-1]+h[i]), h[i]])

    # C1 = C_last = 0 for natural cubic splines, so we ignore the first and last terms
    X1, Y1 = array(X1), array(Y1)
    X1_arr = zeros((len(Y1), len(Y1)+2))
    for i in range(len(Y1)):
        X1_arr[i][i:i+len(X1[0])] = X1[i]
    X1_arr = X1_arr[:,1:-1]

    Cdd = concatenate(([0], linalg.solve(X1_arr, Y1), [0])) # Solve the X1*C = Y1
    # Cubic spline: P_3,k = ak*(x-xk_L)**3 + bk*(x-xk_L)**2 + ck*(x-xk_L) + dk
    # Where x_L is the x data point closest to x from left
    a_k, b_k, c_k, d_k = [], [], [], []
    for k in range(len(Cdd)-1):
        a_k.append((Cdd[k+1]-Cdd[k])/(6*h[k]))
        b_k.append((Cdd[k])/2)
        c_k.append((y[k+1]-y[k])/h[k] - (2*h[k]*Cdd[k]+h[k]*Cdd[k+1])/6)
        d_k.append(y[k])
    #print(a_k, b_k, c_k, d_k)
    weight_func = [a_k, b_k, c_k, d_k]

    if Plot:
        Plot_spline(x, y, x_0, weight_func)

# Data
u=array([1.005, 1.775, 2.480, 3.655, 4.620, 5.925])
C=array([0, 20, 30, 40, 45, 50])
Natural_Spline(u, C, x_0=3, Plot=True)