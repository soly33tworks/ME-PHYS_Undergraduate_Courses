"""
Principal Component Analysis (PCA) used on the iris dataset.
The algorithm should work for other classification datasets aswell
with the class data stored at the last column.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def Load_generate_data():
    ######### Load data #########
    data = pd.read_csv("bezdekIris.data", delimiter=",", header=None)
    data = data.to_numpy()
    X = data[:,:4]
    Y = data[:, 4]
    rows, columns = data.shape

    ######### Generate noisy data and normalize #########
    noise_low = np.random.normal(10, 0.01, size=(rows, 20)) - np.random.normal(-10, 0.01, size=(rows, 20))
    noise_medium= np.random.normal(10, 0.01, size=(rows, 40)) - np.random.normal(-10, 0.01, size=(rows, 40))
    noise_high = np.random.normal(10, 0.01, size=(rows, 80)) - np.random.normal(-10, 0.01, size=(rows, 80))

    X_L = np.concatenate((data[:,:4], noise_low.reshape(rows,20)), axis = 1)
    X_M = np.concatenate((data[:,:4], noise_medium.reshape(rows,40)), axis = 1)
    X_H = np.concatenate((data[:,:4], noise_high.reshape(rows,80)), axis = 1)
    return X, X_L, X_M, X_H, Y

def plot(data, tag, fig_no=1):
    labels = np.unique(data[:,-1])
    datas = []
    for label in labels:
        my_data = data[[(label in a) for a in data[:,-1]]]
        plt.figure(fig_no)
        plt.plot(my_data[:,0], my_data[:,1], '.', label=label)
    plt.xlabel("First Principle Component")
    plt.ylabel("Second Principle Component")
    plt.title(tag)
    plt.grid("on")
    plt.legend()
    plt.show()

def Centralize(X):
    rows = len(X)
    means = np.array(X).mean(axis=0)
    means = np.tile(means, (rows, 1))
    X = X - means
    var = np.array(X).var(axis=0, dtype=float)
    stdev = np.sqrt(var)
    X = X/stdev.reshape((1,-1))
    return X

def PCA(X, Y, j=0, Tag="PCA", plot_pca=False):
    # 0-Centralize
    X = Centralize(X)
    # 1-Compute cross correlation
    rows = len(X)
    E = (np.matmul(X.T, X))/rows
    E = np.array(E, dtype=float)
    λ, u_T = np.linalg.eig(E)
    λ = np.array([λ], dtype=float)
    print(λ)
    print(np.argsort(np.max(λ, axis=0))[-1])
    print(np.argsort(np.max(λ, axis=0))[-2])
    # 2-Reduce to dimension to 2 and plot
    u_T1 = u_T[:,np.argsort(np.max(λ, axis=0))[-1]]
    u_T2 = u_T[:,np.argsort(np.max(λ, axis=0))[-2]]
    r = u_T1.size
    u_T= np.concatenate((u_T1.reshape(r,1), u_T2.reshape(r,1)), axis = 1) # Choose first two principal components
    Z = np.matmul(X,u_T)
    data = np.concatenate((Z, Y.reshape(rows,1)), axis = 1)
    if plot_pca:
        plot(data, Tag, fig_no=j)
    return data

X, X_L, X_M, X_H, Y = Load_generate_data()
######### Use PCA (only first 2 inputs are needed) #########
PCA(X, Y, 1, "PCA with original IRIS data", True)
PCA(X_L, Y, 2, "PCA with IRIS data (Low Noise)", True)
PCA(X_M, Y, 3, "PCA with IRIS data (Medium Noise)", True)
PCA(X_H, Y, 4, "PCA with IRIS data (High Noise)", True)
