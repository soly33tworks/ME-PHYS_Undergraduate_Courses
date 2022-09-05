"""
Shows the time evolution of a wave packet using the dispersion relation
Three options are given as examples: w=k, w=(k^2)/2 and w=2sqrt(k)
"""

from numpy import *
import matplotlib.pyplot as plt

def init():
  plt.clf()
  plt.axis([-10, 40, -3.7, 4])
  plt.grid("on")

  x = array(arange(-10,40, 0.01))
  t=0
  return x,t

def A(k):
  val=e**(-25*((k-1)**2))
  return val

def OptionA(steps=42):
  "w=k"
  x,t = init()
  for i in range(steps):
      t+=0.5
      plt.clf()
      wave = 0
      for j in range(7,14):
        k = j/10
        wave += A(k)*cos((k)*x-(k)*t)

      plt.plot(x,wave)
      plt.grid()
      plt.pause(0.1)

def OptionB(steps=42):
  "w=(k^2)/2"
  x,t = init()
  def w1(k):
    val=(k**2)/2
    return val

  for i in range(steps):
      t+=0.5
      plt.clf()
      pt=0
      for i in range(-3, 4, 1):
          pn=A(1+i/10)*cos((1+i/10)*x-w1(1+i/10)*t)
          pt+=pn
      
      wave=pt
      plt.plot(x,wave)
      plt.grid()
      plt.pause(0.1)

def OptionC(steps=42):
  "w=2sqrt(k)"
  x,t = init()
  def w2(k):
    val=2*sqrt(k)
    return val

  for i in range(steps):
      t+=0.5
      plt.clf()
      pt=0
      for i in range(-3, 4, 1):
          pn=A(1+i/10)*cos((1+i/10)*x-w2(1+i/10)*t)
          pt+=pn
      
      wave=pt
      plt.plot(x,wave)
      plt.grid()
      plt.pause(0.1)

"""Uncomment to choose"""

# OptionA()
OptionB()
# OptionC()

# plt.show() # Add this to the end of the functions if plots dont show up
