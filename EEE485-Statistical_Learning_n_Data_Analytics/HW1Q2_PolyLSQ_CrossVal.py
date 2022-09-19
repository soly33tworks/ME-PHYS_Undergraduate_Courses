"""
Least squares solution to a given dataset.
Additional options:
    -Centralizing and Standardizing: Makes 0 the center of the data and magnifies them to make each vector unit amplitude.
    -Polynomization: Polynomizes the X variables up to 2nd degree to increase the power of the model
    -Leave-one-out Cross Validation: To balance the test error with the training error, one data instance is made invisible
                                    to the training process and each model trains on the rest and compared their performance
                                    using the hidden data. (not suggested for large datasets, divide it into 5-6 parts instead)
"""
import pandas as pnd
import matplotlib.pyplot as plt
import numpy as np

def Visualize(X, Y, no_vars):
    for i in range(no_vars):
        plt.figure(i)
        plt.plot(X[:,i], Y, 'r.')
        plt.xlabel('X variable')
        plt.ylabel('Y output')
        plt.grid()
        plt.title("Data "+str(i+1))

def Standardize_Centralize(data, col_size, stdize=True, cent=True):
    n = len(data)
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
        data_norm = data
        data_norm = np.divide(data, stdev)
        data = data_norm
    
    return data
    
def Polynomize(X):
    # Prepare variable structures
    n, no_vars = X.shape
    m = no_vars
    x_poly = np.zeros((n, int(2*m+(m*(m-1)/2))))
    x_poly[:,0:m] = X
    x_poly[:, m:2*m] = X*X

    i = 2*m

    total_cols = round(2*m+(m*(m-1)/2))# For m=7, its 35
    while i < int(total_cols)-1:
        for j in range(m):
            for k in range(j+1, m):
                x_poly[:, i] = x_poly[:,j]*x_poly[:,k]
                i += 1
    return x_poly, total_cols

def Solve(X, Y):
    n, no_vars = X.shape
    n, no_outputs = Y.shape

    xxt = np.zeros((no_vars, no_vars), np.float64)
    xy = np.zeros((no_vars, no_outputs), np.float64)
    for i in range(n):
        x_T = np.array(np.float64(X[i])).reshape((1, no_vars))
        x = np.transpose(x_T)
        y = float(Y[i])
        xxt = np.add(xxt, np.matmul(x, x_T))
        xy = np.add(xy, x*y)

    w = np.matmul(np.linalg.inv(np.matrix(xxt)), xy)

    msq = 0 # Mean Squared Error
    for i in range(n):
        msq = msq + (Y[i] - np.matmul(np.transpose(w), X[i]))**2
    
    return msq/n, w

def Cross_val(X, Y, plot_d):
        min_msq = 100000
        min_err = 100000
        n, no_vars = X.shape
        n, no_outputs = Y.shape

        Errors = []
        for i in range(n):
            x_cross = X[i,:]
            x_data, y_data = np.delete(X, i, 0), np.delete(Y, i, 0)
            msq, w = Solve(x_data, y_data)

            cv_error = (float(Y[i] - np.matmul(np.transpose(w), np.transpose(x_cross))))**2
            print("Model ", i, "MSQ: ", msq, "Error: ", cv_error)
            Errors.append([msq, cv_error])

            # Saves the weight function of model with min cv error, write your own criteria to balance between cv error and msq
            if cv_error < min_err:
                min_err = cv_error
                w_err = w
                min_ind1 = i
            
            if msq < min_msq:
                min_msq = msq
                w_msq = w
                min_ind2 = i

        print("\nMinimum error model:", "Model",min_ind1,"CV Error = ", min_err)
        print("Weight function: ", w_err)
        print("Minimum MSQ model:", "Model",min_ind2,"MSQ = ", min_msq)
        print("Weight function: ", w_msq)

        if plot_d:
            Errors = np.array(Errors)
            msq_errs, cv_errs = Errors[:,0], Errors[:,1]
            iters = np.arange(0, len(msq_errs))
            plt.figure(no_vars+1)
            plt.plot(iters, msq_errs)
            plt.xlabel('Model No.')
            plt.ylabel('Mean squared error')
            plt.grid()

            plt.figure(no_vars+2)
            plt.plot(iters, cv_errs)
            plt.xlabel('Model No.')
            plt.ylabel('Cross validation error')
            plt.grid()
            plt.show()

def LeastSquares(X, Y, cent_stdize=True, polynomize=False, crosval=False, plot_d=False):
    try:
        n, no_vars = X.shape
    except:
        n, no_vars = X.size, 1
        X = X[..., None]
    try:
        n, no_outputs = Y.shape
    except:
        n, no_outputs = Y.size, 1
        Y = Y[..., None]
        
    if plot_d:
        Visualize(X, Y, no_vars) # Visualize data
        
    if cent_stdize:
        X, Y = Standardize_Centralize(X, no_vars), Standardize_Centralize(Y, no_outputs)

    if polynomize:
        X, no_vars = Polynomize(X)

    if crosval:
        Cross_val(X, Y, plot_d)
    
    else:
        msq, w = Solve(X, Y)
        print("Mean squared error: ", np.float64(msq))
        print("Weight function: \n", w)

data = pnd.read_excel('data_HW1Q2.xlsx', index_col=0) # Load data
data = data.to_numpy()
np.random.shuffle(data) # Randomize the data order (important for gradient descent but not here, added for illustration)
x = data[:, 1:8] # x data for the specific data given in our example
y = data[:, 8]
#LeastSquares(x, y) # Data as it is
#LeastSquares(x, y, 1) # Centralized + stdized data
#LeastSquares(x, y, 1, 1) # Centralized + stdized data using polynomial fitting
#LeastSquares(x, y, 1, 1, 1) # Centralized + stdized data using polynomial fitting with leave-one-out cross validation
LeastSquares(x, y, 1, 1, 1, 1)
