import numpy as np
from scipy.signal import butter, lfilter, freqz, filtfilt
import matplotlib.pyplot as plt
import pickle

# Improve this using: https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.filtfilt.html

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    #y = lfilter(b, a, data)
    y = filtfilt(b, a , data) # Double filters in both directions to avoid 0 offset at beginning and avoid x-shift throughout
    return y

def Butterworth(n=3, f_sampling=100, f_cutoff=1.0):
    # Filter parameters
    order = round(n)
    fs = f_sampling     # sample rate, Hz
    cutoff = float(f_cutoff)  # desired cutoff frequency of the filter, Hz
    b, a = butter_lowpass(cutoff, fs, order) # Get the filter coefficients so we can check its frequency response.

    # Plot the frequency response.
    w, h = freqz(b, a, worN=8000)
    f1 = plt.figure(2)
    plt.plot(0.5*fs*w/np.pi, np.abs(h), 'b')
    plt.plot(cutoff, 0.5*np.sqrt(2), 'ko')
    plt.axvline(cutoff, color='k')
    plt.xlim(0, 3*cutoff)
    plt.title("Lowpass Filter Frequency Response")
    plt.xlabel('Frequency [Hz]')
    plt.grid("on")

    f1.savefig("Extracted Data/DataFilter_FrequencyResponse.jpg")
    # Import data
    plt.figure(4)
    directory = r'Extracted Data/Raw_Plot.fig.pickle' # Write the directory here as "r string"
    with open(directory, 'rb') as file: figx = pickle.load(file)
    t, data = figx.axes[0].lines[0].get_data()

    # Filter the data, and plot both the original and filtered signals.
    y = butter_lowpass_filter(data, cutoff, fs, order)
    plt.close(4)
    plt.close(5)
    f2 = plt.figure(3)
    plt.plot(t, data, 'b-', label='data')
    plt.plot(t, y, 'g-', linewidth=2, label='filtered data')
    plt.title('Position Plot (Raw vs Low Pass)')
    plt.xlabel('Time [sec]')
    plt.ylabel("Displacement [μm]")
    plt.grid("on")
    plt.legend()

    f3 = plt.figure(6)
    plt.plot(t, y, 'g-', linewidth=2, label='filtered data')
    plt.title('Position Plot (Low Pass Filtered)')
    plt.xlabel('Time [sec]')
    plt.ylabel("Displacement [μm]")
    plt.grid("on")
    plt.legend()

    f2.savefig("Extracted Data/Comparison_Plot.jpg")
    f3.savefig("Extracted Data/Filtered_Plot.jpg")
    with open('Extracted Data/Comparison_Plot.fig.pickle', 'wb') as file: figy = pickle.dump(f2, file)
    with open('Extracted Data/Filtered_Plot.fig.pickle', 'wb') as file: figz = pickle.dump(f3, file)

    return t, data
