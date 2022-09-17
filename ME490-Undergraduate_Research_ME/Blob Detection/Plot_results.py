import matplotlib.pyplot as plt
import pickle
import numpy as np

def plot_results(data, events, channel, scale):
    frameNO, t, velocity, area, coors_avg = data[:,0], data[:,1], data[:,2], data[:,3], data[:,4]
    y_avg, x_avg = np.array([i for i, j in coors_avg]), np.array([j for i, j in coors_avg])
    
    f1 = plt.figure(1)
    plt.plot(frameNO, velocity, 'bo')
    plt.xlabel("Frame No")
    plt.ylabel("Average Velocity (μm/s)")
    plt.title("Velocity vs Time Plot for Events")
    plt.vlines(x = events, ymin = 0, ymax = data[:,2].max(axis=0),colors = 'purple')
    plt.grid(True)

    f2 = plt.figure(2)
    plt.plot(frameNO, area, 'bo')
    plt.xlabel("Frame No")
    plt.ylabel("Area (μm²)")
    plt.title("Area vs Time Plot for Events")
    plt.vlines(x = events, ymin = 0, ymax = data[:,3].max(axis=0),colors = 'purple')
    plt.grid(True)

    f3 = plt.figure(3)
    plt.plot(area, velocity, 'bo')
    plt.xlabel("Area (μm²)")
    plt.ylabel("Average Velocity (μm/s)")
    plt.title("Area vs Velocity Plot for Events")
    plt.grid(True)

    channel = np.array([channel])/scale
    f4 = plt.figure(4)
    plt.plot(area, y_avg, 'bo')
    plt.xlabel("Area (μm²)")
    plt.ylabel("y position (μm)")
    plt.title("Area vs y position Plot for Events")
    plt.hlines(y = channel, xmin = 0, xmax = area.max(axis=0),colors = 'purple')
    plt.grid(True)

    f5 = plt.figure(5)
    plt.plot(velocity, y_avg, 'bo')
    plt.xlabel("Average Velocity (μm/s)")
    plt.ylabel("y position (μm)")
    plt.title("Velocity vs y position Plot for Events")
    plt.hlines(y = channel, xmin = 0, xmax = velocity.max(axis=0),colors = 'purple')
    plt.grid(True)

    with open('Extracted Data/Plots.fig.pickle', 'wb') as file: figa = pickle.dump(f1, file) # Saves plot as backup
    with open('Extracted Data/Plots2.fig.pickle', 'wb') as file2: figb = pickle.dump(f2, file2)
    with open('Extracted Data/Plots3.fig.pickle', 'wb') as file3: figc = pickle.dump(f3, file3)
    with open('Extracted Data/Plots4.fig.pickle', 'wb') as file4: figd = pickle.dump(f4, file4)
    with open('Extracted Data/Plots5.fig.pickle', 'wb') as file5: figd = pickle.dump(f5, file5)
    with open('Extracted Data/data.pkl','wb') as file6: pickle.dump(data, file6) # Saves data as backup

    plt.show()

def replot():
    with open('Sample Results\DataSet3 SPM-PS 10um/1629/Data.pkl', 'rb') as file: data = pickle.load(file)
    events_E1629 = [12, 106, 274, 336, 346, 394, 414, 666, 852, 898, 982, 1076, 1216, 1254, 1292,
                        1438, 1478, 1502, 1860, 1922, 2016, 2040, 2868, 3048, 3210, 3836, 4848, 5434]
        
    scale = 106/100 # Pixel/Micrometer
    channel = [10, 1200, 140, 400, 721, 835]
    plot_results(data, events_E1629, channel[2:4], scale)
