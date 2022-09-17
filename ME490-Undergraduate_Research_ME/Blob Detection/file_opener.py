# Example code on opening pickle files

import matplotlib.pyplot as plt
import pickle

#################### WRITE FIG FILE ######################
# fig,ax = plt.subplots()
# ax.plot([1,2,3],[10,-10,30])
# with open('FigureObject.fig.pickle', 'wb') as file: figx = pickle.dump(fig, file)

################### OPEN FIG FILE ######################
directory = r'Sample Results\DataSet3 SPM-PS 10um/1629/Plots.fig.pickle' # Write the directory here (sometimes it can't read the directory, move the folder in the same folder as the code and try again)
with open(directory, 'rb') as file: figx = pickle.load(file)
plt.show() # Show the figure, edit it, etc.!

################## DATA EXTRACTION (OPTIONAL) ###########
x,y = figx.axes[0].lines[0].get_data()
