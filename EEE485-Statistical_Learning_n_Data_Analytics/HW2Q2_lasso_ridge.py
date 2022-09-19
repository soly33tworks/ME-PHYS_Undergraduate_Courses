"""
Lasso and Ridge regression regularization visualization. 
The generated data is a 9 variable function + noise; however,
the algorithms should work for other data aswell.
"""

import numpy as np
import matplotlib.pyplot as plt

def Generate_data(dist_range, instances): # Generate Data with noise. You should enter your own data 
    x = np.random.uniform(dist_range[0], dist_range[1], instances)
    for i in range(9-1):
        x_i = np.random.uniform(dist_range[0], dist_range[1], instances)
        x = np.column_stack((x,x_i))

    y = np.zeros((instances, 1))
    for i in range(instances):
        y[i] = -4*x[i][0]-3*x[i][1]-2*x[i][2]-x[i][3]+x[i][5]+2*x[i][6]+3*x[i][7]+4*x[i][8]+np.random.normal(0, 1)
        # 9 variable model + data 
    return x, y

def Standardize_Centralize(data, stdize=True, cent=True):
    try:
        n, col_size = data.shape
    except:
        n, col_size = data.size, 1
        data = data[..., None]

    if cent:
        means = np.array(data).mean(axis=0)
        means = np.tile(means, (n, 1))
        data_cent = data - means
        data = data_cent

    if stdize:
        var = np.array(data).var(axis=0)
        vars = np.zeros(col_size)
        for i in range(col_size):
            vars[i] = var[i]
        stdev = np.sqrt(vars)
        stdev = np.tile(stdev, (n, 1))
        data_norm = np.divide(data, stdev)
        data = data_norm
    
    return data

def Plot_results(weights, fig_no):
    n, n_weights = weights.shape
    n_weights -= 1 # first variable is the λ
    legends = []
    for i in range(n_weights):
        plt.figure(fig_no)
        plt.plot(weights[:,0], weights[:,i+1], '-')
        legends.append("w"+str(i+1))

    plt.title("Weights as a function of λ")
    plt.xlabel('λ')
    plt.ylabel('Weight magnitude')
    plt.grid("on")
    plt.legend(legends)
    plt.show()

def Ridge(X, Y, λ_range, λ_step=0.1):
    x, y = Standardize_Centralize(X), Standardize_Centralize(Y) # Centralize and Normalize
    n, no_vars = x.shape
    n, no_outputs = y.shape

    λ=λ_range[0]
    array_size = round(λ_range[1]/λ_step + 1)
    weights = np.ones((array_size, no_vars+1))
    for i in range(array_size):
        w_rss1 = np.linalg.inv(np.matmul(x.T, x) + λ*np.identity(no_vars))
        w_rss2 = np.matmul(x.T, y)
        w_rss = np.matmul(w_rss1, w_rss2)
        weights[i][0] = λ
        weights[i][1:] = w_rss.T
        λ = λ + λ_step
        
    weights = np.around(weights, decimals=6)
    Plot_results(weights, 1)

def Lasso(X, Y, λ_range, λ_step=0.1):
    x, y = Standardize_Centralize(X), Standardize_Centralize(Y) # Centralize and Normalize
    n, no_vars = x.shape
    n, no_outputs = y.shape

    λ=λ_range[0]
    array_size = round(λ_range[1]/λ_step + 1)
    weights = np.ones((array_size, no_vars+1))
    for i in range(array_size):
        w_rss1 = np.linalg.inv(np.matmul(2*x.T, x))
        w_rss2 = np.matmul(2*x.T, y)
        w_rss = np.matmul(w_rss1, w_rss2)
        err = 1
        j=0
        while err > 0.1 or j < 200:
            w_rss2 = np.matmul(2*x.T, y) - λ*w_rss/(np.sqrt(np.matmul(w_rss.T, w_rss)))
            err = np.amax(np.absolute(w_rss - np.matmul(w_rss1, w_rss2)))
            w_rss = np.matmul(w_rss1, w_rss2)
            j = j +1
        
        w_rss = np.matmul(w_rss1, w_rss2)
        weights[i][0] = λ
        weights[i][1:] = w_rss.T
        λ = λ + 1
        print(λ)
        
    weights = np.around(weights, decimals=6)
    Plot_results(weights, 2)


x,y = Generate_data([-1,1], 1000)
Ridge(x, y, λ_range=[0,5000], λ_step=0.1)
Lasso(x, y, λ_range=[0,900], λ_step=1)