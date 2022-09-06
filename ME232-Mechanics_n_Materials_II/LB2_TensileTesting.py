"""
Includes the data and the evaluation for tensile 
testing experiment for steel and polyurethane.
See: https://dl.asminternational.org/handbooks/book/47/chapter/535487/Uniaxial-Tension-Testing

Data extraction: Transform the excel file into text file as given in the example files
Example data: LB2_data.rar, extract them to the same folder as the code

Check my researchgate page for the relevant report.
"""
from numpy import *
from matplotlib.pyplot import *
import pylab
clf()

"0. LOADING DATA"
def getData(filename):
    dataFile = open(filename, 'r')
    strains = []
    pressures = []
    dataFile.readline()
    for line in dataFile:
        s,p = line.split('	')
        strains.append(float(s))
        pressures.append(float(p))    
    E=0
    S0=0
    Su=0
    offset=0
    if filename[0]=='p':
        E= (pressures[150]-pressures[100])/(strains[150]-strains[100])
        offset=(array(strains)-0.2)*E
        idx = argwhere(diff(sign(array(pressures) - offset))).flatten()
        S0= pressures[idx[0]]
        Su= max(pressures)
    
    else:
        E= (pressures[6000]-pressures[4500])/(strains[6000]-strains[4500])
        offset=(array(strains)-0.2)*E
        idx = argwhere(diff(sign(array(pressures) - offset))).flatten()
        S0= pressures[idx[0]]
        Su= max(pressures)

    e_t=[0]*len(pressures)
    for i in range(0,len(pressures)):
        e_t[i]=(log(1+(strains[i]/100)))*100
        
    s_t=[0]*len(pressures)
    for i in range(0,len(pressures)):
        s_t[i]=pressures[i]*(1+(strains[i]/100))
    
    dataFile.close()
    return(strains, pressures, E, S0, Su, e_t, s_t)

def plotData(inputfile, form):
    strain, pressure, E, S0, Su, tru_strain, tru_pressure = getData(inputfile)    
    pylab.plot(strain, pressure, form)
    "pylab.plot(strain, off)"
    "pylab.plot(tru_strain, tru_pressure)"
    pylab.xlabel('Elongation (%)')
    pylab.ylabel('Standard Force (MPa)')
    print("(",E/10, S0, Su,")")

"1. STEEL"   
def steel():
    figure(1)
    plotData('m8.txt', 'r')
    plotData('m9.txt', 'b')
    plotData('m10.txt', 'g')
    plotData('m11.txt', 'm')
    plotData('m12.txt', 'y')
    plotData('m13.txt', 'k')

    title('Stress-Strain Curve for Steel')
    axis([0, 30, 0, 500])
    grid("on")
    legend(['Program 8', 'Program 9', 'Program 10', 'Program 11', 'Program 12', 
            'Program 13'])

"2. POLYMER"
def polymer():
    figure(2)
    plotData('p8.txt', 'r')
    plotData('p9.txt', 'b')
    plotData('p10.txt', 'g')
    plotData('p11.txt', 'm')
    plotData('p12.txt', 'y')
    plotData('p13.txt', 'k')

    title('Stress-Strain Curve for Polymer')
    axis([0, 600, 0, 25])
    grid("on")
    legend(['Program 8', 'Program 9', 'Program 10', 'Program 11', 'Program 12', 
            'Program 13']) 

steel()
polymer()
show()
