import matplotlib.pyplot as plt
import pickle
import numpy as np
from ButterworthFilter import Butterworth

def plot_results(data, parameters):
    t = data[2:len(data)+1, 1].astype(np.float64)
    x = data[2:len(data)+1, 2].astype(np.float64)
    
    f1 = plt.figure(1)
    plt.plot(t, x, 'blue')
    plt.xlabel("Time (seconds)")
    plt.ylabel("Displacement [μm]")
    plt.title("Position plot")
    plt.grid(True)
    
    with open('Extracted Data/Raw_Plot.fig.pickle', 'wb') as file: figa = pickle.dump(f1, file) # Saves plot as backup
    with open('Extracted Data/data.pkl','wb') as file5: pickle.dump(data, file5) # Saves data as backup

    Butter_n, Butter_FPS, Butter_cutoff = parameters
    Butterworth(Butter_n, Butter_FPS, Butter_cutoff)

    plt.show()

def replot():
    directory = r'Extracted Data/Output_data.pkl'
    with open(directory, 'rb') as file: data = pickle.load(file)
    plot_results(data)
