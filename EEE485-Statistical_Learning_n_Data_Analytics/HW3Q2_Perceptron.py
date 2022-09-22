"""
Written for data with 2D inputs to classify between 2 classes as a
proof of concept homework. The core algorithm should work for 
higher dimensional data too if the plotting related codes are omitted.
"""

import numpy as np
import matplotlib.pyplot as plt

def sigmoid(x, a=1):
    return 1/(1+np.e**(-a*x))

def Plot_data(data):
    plt.clf()
    plt.figure(0)
    colors = ['b', 'r', 'g', 'c', 'm', 'y', 'k']
    labels = np.unique(data[:,-1])
    for i, label in enumerate(labels):
        my_data = data[[(label in a) for a in data[:,-1]]]
        plt.plot(my_data[:,0], my_data[:,1], color=colors[i], marker='o',markeredgecolor='w',linestyle='',markersize=5, label=label) # 2D input
    plt.xlabel("First Component", fontsize=14)
    plt.ylabel("Second Component", fontsize=14)
    plt.title("2D Data", fontsize=14)
    plt.grid("on")
    plt.legend()

def Plot_guess(data, w, a):
    Plot_data(data[:,1:])
    data_rangex1 = np.linspace(min(data[:,1]), max(data[:,1]), 100, endpoint=True)
    data_rangex2 = np.linspace(min(data[:,2]), max(data[:,2]), 100, endpoint=True)
    dx, dy = (data_rangex1[1]-data_rangex1[0])/2, (data_rangex2[1]-data_rangex2[0])/2

    for x1 in data_rangex1:
        for x2 in data_rangex2:
            x = np.array([1, x1, x2])
            v = np.matmul(x, w)
            y_prime = sigmoid(np.float64(v), a=a)
            if round(y_prime) == 0:
                plt.fill_between([x1-dx, x1+dx], [x2-dy, x2-dy], x2+dy, color="b", alpha=0.3)
            elif round(y_prime) == 1:
                plt.fill_between([x1-dx, x1+dx], [x2-dy, x2-dy], x2+dy, color="r", alpha=0.3)

def Plot_loss(errs, η):
    plt.figure(1)
    plt.plot(np.arange(0, len(errs), 1), np.abs(errs))
    plt.ylim(bottom=0) #ymin is your value
    plt.xlabel("Epoch", fontsize=14)
    plt.ylabel("Loss", fontsize=14)
    plt.title("Perceptron training curve (η = "+str(η)+")", fontsize=14)
    plt.grid("on")
    plt.show()

def data_prep(data, test_percent=0.2):
    np.random.shuffle(data)
    rows, columns = data.shape
    data_test = data[:round(rows*test_percent),:]
    data_train = data[round(rows*test_percent):,:]
    return data_train, data_test

def generate_data(test_percent=0.2):
    cov = 0.08*np.identity(2, dtype=float)
    X1 = np.random.multivariate_normal([-1,-0.8], cov, size=(100))
    X2 = np.random.multivariate_normal([0.7,-0.1], cov, size=(100))
    X_0 = np.concatenate((X1, X2), axis = 0)
    Y_0 = np.array([["0"]]*200, dtype=object)
    data_0 = np.concatenate((X_0, Y_0), axis = 1)

    X1 = np.random.multivariate_normal([-1,0.7], cov, size=(100))
    X2 = np.random.multivariate_normal([1,0.6], cov, size=(100))
    X_1 = np.concatenate((X1, X2), axis = 0)
    Y_1 = np.array([["1"]]*200, dtype=object)
    data_1 = np.concatenate((X_1, Y_1), axis = 1)

    bias = np.ones((400, 1), dtype=int)
    data = np.concatenate((data_0, data_1), axis = 0)
    data = np.concatenate((bias, data), axis = 1)
    data_train, data_test = data_prep(data, test_percent)
    return data_train, data_test

def forward_propagation(data_i, w, a):
    y = float(data_i[-1])
    x = data_i[:-1]
    v = np.matmul(x, w)
    y_prime = sigmoid(np.float64(v), a=a)
    error = np.float64(y-y_prime)
    # if str(i)[-1] == "0":
    #     print("Error for iteration ",i," : ", error)
    return error, y_prime

def back_propagation(data_i, error_signal, w, η):
    w_new = w + (η*error_signal*data_i[:len(w)]).reshape(3,1)
    return w_new

def train(data, a, η, n, visualize=0):

    min_err = 10**9
    rows, columns = data.shape
    w = np.random.normal(0, 5, size=(columns-1, 1))
    errs = []
    for j in range(n):
        err = 0
        for i in range(rows):
            loss, _ = forward_propagation(data[i], w, a)
            err += loss/rows
            if loss < min_err:
                w_opt = w
                min_err = loss
            w = back_propagation(data[i], loss, w, η)
        np.random.shuffle(data)
        errs.append(err)
        print("Error for epoch ", j, " : ", err)
    
    if visualize:
        Plot_guess(data, w, a) # Too slow for real-time updating, need to use pyqtgraph and optimize the code
        Plot_loss(errs, η)
    return w, errs

def test(data, w):
    rows, columns = data.shape
    RSS = 0
    acc = 0
    for i in range(rows):
        y = float(data[i,-1])
        v = 0
        for j in range(len(w)):
            v += data[i,j]*w[j]
        y_prime = sigmoid(np.float64(v), a=a)
        RSS += np.float64(y-y_prime)**2
        if round(y_prime) == round(y):
            acc += 1
    MSQ = np.sqrt(RSS)/rows
    acc = acc/rows
    return MSQ, acc

data_train, data_test = generate_data()
η = 0.01
a = 1
n = 70
w, errs = train(data_train, a, η, n, visualize=1)
print("Weight function: \n", w)
MSQ, acc = test(data_test, w)
print("MSQ = ", MSQ)
print("Accuracy = ", acc*100, "%")