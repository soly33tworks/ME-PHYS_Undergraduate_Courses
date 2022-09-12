"""
Plotting for the visualization of a 2D membrane nodal lines
"""
from mpl_toolkits import mplot3d
from numpy import *
import matplotlib.pyplot as plt

x = linspace(0, pi, 130)
y = linspace(0, pi, 130)

X, Y = meshgrid(x, y)
Z1 = sin(X)*sin(2*Y)
Z2 = sin(2*X)*sin(Y)
Z3 = sin(2*X)*sin(Y) + sin(X)*sin(2*Y)
Z4 = sin(2*X)*sin(Y) - sin(X)*sin(2*Y)

ax = plt.axes(projection='3d')
ax.contour3D(X, Y, Z4, 50, cmap='binary')
ax.plot_surface(X, Y, Z4, rstride=1, cstride=1,cmap='jet', edgecolor='none')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.set_title('Square Membrane (A + B = 0)')

plt.show()

