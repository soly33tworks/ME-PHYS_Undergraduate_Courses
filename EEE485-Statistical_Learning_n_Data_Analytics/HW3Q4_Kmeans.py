"""
K-means algorithm with the commonly used euclidean distance as loss function.
The iterations stop when the change in center values reach the stopping condition
or when the maximum number of iterations is reached.
"""

import numpy as np
import matplotlib.pyplot as plt

def plot_results(X, All_indexes):
    colors = ['b', 'r', 'g', 'c', 'm', 'y', 'k']
    for i, indexes in enumerate(All_indexes):
        plt.plot(X[indexes, 0], X[indexes, 1], color=colors[i], marker='o',markeredgecolor='w',linestyle='',markersize=5, label=str(i)) # 2D input
    plt.xlabel("x1", fontsize=14)
    plt.ylabel("x2", fontsize=14)
    plt.title("K-means grouping", fontsize=14)
    plt.grid("on")
    plt.legend()
    plt.show()

def generate_2Ddata(groups, n_data=10):
    dim = 2
    data = np.zeros((1, dim))

    for group in range(groups):
        deviation = np.random.random()/10+0.1 # about 0.15 covaiance
        cov = deviation*np.identity(dim, dtype=float)
        means = []
        for d in range(dim):
            means.append(np.random.random()*(group + 1))
        data = np.concatenate((data, np.random.multivariate_normal(means, cov, size=n_data)), axis = 0)
        print("Group ", str(group+1), " means: ", means)
    data = np.delete(data, (0), axis=0)

    return data

def Normalize(X, no_vars):
    for var in range(no_vars):
        X[:,var] = (X[:,var] - np.amin(X[:,var]))/(np.amax(X[:,var]) - np.amin(X[:,var]))
    return X

def Kmeans(X, K, max_iters=100, stopping_cond=0.01):
    try:
        n, no_vars = X.shape
    except:
        n, no_vars = X.size, 1
        X = X[..., None]
    print("n, no_vars: ", X.shape)
    
    X = Normalize(X, no_vars)

    u = np.random.rand(K, no_vars)
    C = np.zeros(n)

    for iteration in range(max_iters):
        print("Iteration: ", iteration)
        
        ##### E Step #####
        for i in range(n):
            J_i = []
            for k in range(K):
                J_i.append(np.linalg.norm(X[i]-u[k]))
            J_i = np.array(J_i)
            C[i] = np.argmin(J_i)
        print("Grouping: \n", C)

        ##### M Step #####
        u_old = np.copy(u)
        All_indexes = []
        for i in range(K):
            indexes = []
            array = np.zeros(no_vars)
            for j in range(n):
                if C[j] == i:
                    indexes.append(j)
            All_indexes.append(indexes)
            print("Indexes: \n", indexes)
            for k in indexes:
                array=np.vstack((array, X[k]))
            array = np.delete(array, (0), axis=0)
            u[i] = np.mean(array, axis=0)
        change = np.linalg.norm(u_old - u)
        print("Relative change: ", change)
        if change < stopping_cond:
            break
    return All_indexes, C, u


X = generate_2Ddata(groups = 3) # Generate 2D data for plotting purpuses
All_indexes, C, u = Kmeans(X, K=3, max_iters=15, stopping_cond=0.01)
plot_results(X, All_indexes)
