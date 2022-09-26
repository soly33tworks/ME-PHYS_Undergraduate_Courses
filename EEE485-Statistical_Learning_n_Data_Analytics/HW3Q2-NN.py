"""
Written for data with 2D inputs to classify between 2 classes as a
proof of concept homework. Works for any arbitrary number of hidden
layers and neuron numbers. 

Write the hidden layers and their neuron counts as: 
neuron_counts=[n1, n2, n3, ...]

Note 1: To use higher dimensonal data, remove the plotting related codes.
Note 2: To classify between types of classes more than 2, atleast one-hot
        encoding is needed. Other than that, maybe replace list indices such
        as x[-1] with x[-no_outputs:]. Other additional small tweaks all 
        around might also be needed such as treating the output as an array 
        instead of a float during back propagation but the core algorithm is correct. 
"""

import numpy as np
import matplotlib.pyplot as plt
import sys

def sigmoid(x, a=1):
    return 1/(1+np.e**(-a*x))

def d_sigmoid(v, a=1):
    return (a*np.e**v)/((1+np.e**(a*v))**2)

def data_prep(data, test_percent=0.2):
    np.random.shuffle(data)
    rows, columns = data.shape
    data_test = data[:round(rows*test_percent),:]
    data_train = data[round(rows*test_percent):,:]
    return data_train, data_test

def generate_data(test_percent=0.2):
    cov = 0.18*np.identity(2, dtype=float)
    X1 = np.random.multivariate_normal([-1,1], cov, size=(150))
    X2 = np.random.multivariate_normal([1,-1], cov, size=(150))
    X_0 = np.concatenate((X1, X2), axis = 0)
    Y_0 = np.array([["0"]]*300, dtype=object)
    data_0 = np.concatenate((X_0, Y_0), axis = 1)

    X1 = np.random.multivariate_normal([-1,-1], cov, size=(150))
    X2 = np.random.multivariate_normal([1,1], cov, size=(150))
    X_1 = np.concatenate((X1, X2), axis = 0)
    Y_1 = np.array([["1"]]*300, dtype=object)
    data_1 = np.concatenate((X_1, Y_1), axis = 1)

    bias = np.ones((600, 1), dtype=int)
    data = np.concatenate((data_0, data_1), axis = 0)
    data = np.concatenate((bias, data), axis = 1)
    data_train, data_test = data_prep(data, test_percent)
    return data_train, data_test

def sort(X, Y):
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
    return X, Y, n, no_vars, no_outputs

def init_layers(neuron_counts, no_vars, no_outputs):
    layers = [np.random.normal(0, 4, size=(neuron_counts[0], no_vars))]
    for i in range(1, len(neuron_counts)):
        layers.append(np.random.normal(0, 4, size=(neuron_counts[i], neuron_counts[i-1])))
    layers.append(np.random.normal(0, 4, size=(no_outputs, neuron_counts[-1])))
    layers = np.array(layers, dtype=object)
    return layers

def forward_propagation(Xi, layers, a):
    x = [Xi]
    v = []
    for l, layer in enumerate(layers):
        x_cache = []
        v_cache = []
        for neuron in layer:
            v_lj = np.dot(x[l], neuron)
            v_cache.append(v_lj)
            x_cache.append(sigmoid(v_lj, a))
        v.append(np.array(v_cache))
        x.append(np.array(x_cache))
    
    return x, v

def back_propagation(Yi, layers, x, v, a):
    y_prime = np.array(x[-1])
    error = np.float64(Yi)-np.float64(y_prime)
    δ = [np.array(error*d_sigmoid(np.array(v[-1]), a))]
    l_δ = 0
    for l,layer in reversed(list(enumerate(layers))):
        δ.append(np.multiply(np.matmul(layer.T, δ[l_δ]), d_sigmoid(v[l-1], a))) # (W_T*δ)☉ϕ
        l_δ += 1
    δ.reverse()

    return δ, error

def update_weights(layers, η, x, δ):
    for l, layer in enumerate(layers):
        layers[l] = layers[l] + η*np.outer(δ[l+1], x[l])  #w += η*(x⊗δ)

    return layers

def Plot_data(data, acc):
    plt.figure(0)
    colors = ['b', 'r', 'g', 'c', 'm', 'y', 'k']
    labels = np.unique(data[:,-1])
    for i, label in enumerate(labels):
        my_data = data[[(label in a) for a in data[:,-1]]]
        plt.plot(my_data[:,0], my_data[:,1], color=colors[i], marker='o',markeredgecolor='w',linestyle='',markersize=5, label=label) # 2D input
    plt.xlabel("First Component", fontsize=14)
    plt.ylabel("Second Component", fontsize=14)
    plt.title("2D Data (acc="+str(acc)+")", fontsize=14)
    plt.grid("on")
    plt.legend()

def Plot_guess(X, Y, layers, acc, a):
    data = np.concatenate((X, Y), axis = 1)
    Plot_data(data[:,1:], acc)
    data_rangex1 = np.linspace(min(data[:,1]), max(data[:,1]), 100, endpoint=True)
    data_rangex2 = np.linspace(min(data[:,2]), max(data[:,2]), 100, endpoint=True)
    dx, dy = (data_rangex1[1]-data_rangex1[0])/2, (data_rangex2[1]-data_rangex2[0])/2

    for x1 in data_rangex1:
        for x2 in data_rangex2:
            Xi = np.array([1, x1, x2])
            x, v = forward_propagation(Xi, layers, a)
            y_prime = np.float64(x[-1])
            if round(y_prime) == 0:
                plt.fill_between([x1-dx, x1+dx], [x2-dy, x2-dy], x2+dy, color="b", alpha=0.3)
            elif round(y_prime) == 1:
                plt.fill_between([x1-dx, x1+dx], [x2-dy, x2-dy], x2+dy, color="r", alpha=0.3)
    plt.show()

def Plot_loss(errs, η):
    plt.figure(1)
    plt.plot(np.arange(0, len(errs), 1), np.abs(errs))
    plt.ylim(bottom=0) #ymin is your value
    plt.xlabel("Epoch", fontsize=14)
    plt.ylabel("Loss", fontsize=14)
    plt.title("NN training curve (η = "+str(η)+")", fontsize=14)
    plt.grid("on")

def train(X, Y, neuron_counts, a, η, n, visualize):
    X, Y, n_data, no_vars, no_outputs = sort(X, Y)
    layers = init_layers(neuron_counts, no_vars, no_outputs)
    
    errs = []
    for epoch in range(n):
        error = 0
        for iter in range(n_data):
            x, v = forward_propagation(X[iter], layers, a)
            δ, err = back_propagation(Y[iter], layers, x, v, a)
            layers = update_weights(layers, η, x, δ)
            error += np.abs(err)
            #sys.exit("") # USE THIS TO DEBUG
        errs.append(error/n_data)
        print("Error for epoch ", epoch, " : ", error/n_data)
    
    if visualize:
        Plot_loss(errs, η)

    return layers

def test(X, Y, layers, a, visualize=0):
    X, Y, n_data, no_vars, no_outputs = sort(X, Y)

    error = 0
    acc = 0
    for iter in range(n_data):
        x, v = forward_propagation(X[iter], layers, a)
        δ, err = back_propagation(Y[iter], layers, x, v, a)
        error += np.abs(err)
        y_prime, y = np.float64(x[-1]), np.float64(Y[iter])
        if round(y_prime) == round(y):
            acc += 1
    
    if visualize:
        Plot_guess(X, Y, layers, acc/n_data, a) # Too slow for real-time updating, need to use pyqtgraph and optimize the code

    return error/n_data, acc/n_data

plt.clf()
data_train, data_test = generate_data()
X_train, Y_train = data_train[:, :-1], data_train[:, -1]
X_test, Y_test = data_test[:, :-1], data_test[:, -1] 

η = 0.04
a = 1
n = 400
neuron_counts=[4, 3]
visualize = True

layers = train(X_train, Y_train, neuron_counts, a, η, n, visualize)
t_loss, acc = test(X_test, Y_test, layers, a, visualize)
print("Test loss: ", t_loss)
print("Test Accuracy: ", acc)
