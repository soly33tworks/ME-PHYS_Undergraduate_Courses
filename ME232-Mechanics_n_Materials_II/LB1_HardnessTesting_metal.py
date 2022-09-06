"""
Includes the data and the evaluation for hardness 
testing experiment for metals.
Relevant method: Vickers Hardness (HV or VHN), ASTM E92 test standard

Check my researchgate page for the relevant report.
"""

from numpy import *
from matplotlib.pyplot import *
clf()

"1) DATA"
"STEEL"
dS1=[0.0691, 0.0704, 0.0734, 0.0734, 0.0674, 0.0674, 0.0734, 0.0734, 
 0.0728, 0.0728, 0.0704, 0.0704, 0.0742, 0.0742, 0.0761, 0.0761, 
 0.0759, 0.0759, 0.0699, 0.0699, 0.0656, 0.0656, 0.0765, 0.0765, 
 0.0682, 0.0682]
dS2=[0.0682, 0.0684, 0.0707, 0.0707, 0.0675, 0.0675, 0.0718, 0.0718,
     0.0732, 0.0732, 0.0746, 0.0746, 0.0719, 0.0719, 0.0718, 0.0718,
     0.0698, 0.0698, 0.0733, 0.0733, 0.0727, 0.0727, 0.0724, 0.0724,
     0.0737, 0.0737]

n_samples = len(dS1)
dS = zeros(n_samples)

for i in range(n_samples):
    dS[i]=(dS1[i]+dS2[i])/2

HVS=[394,385,358,358,408,408,352,352,348,348,353,353,348,
     348,340,340,350,350,362,362,388,388,335,335,369,369]    

"COPPER"
dC1=[0.1381, 0.1459, 0.1388, 0.1388, 0.1358, 0.1358, 0.1456, 0.1456, 0.1377, 
      0.1377, 0.1406, 0.1406, 0.1396, 0.1396, 0.1386, 0.1386, 0.1544, 0.1544, 
      0.1516, 0.1516, 0.151, 0.151, 0.147, 0.147, 0.1406, 0.1406]
dC2=[0.1383, 0.1461, 0.1401, 0.1401, 0.1342, 0.1342, 0.1423, 0.1423, 0.1359, 
     0.1359, 0.142, 0.142, 0.142, 0.142, 0.136, 0.136, 0.1506, 0.1506, 0.1513, 
     0.1513, 0.147, 0.147, 0.1458, 0.1458, 0.139, 0.139]
dC = zeros(n_samples)

i=0
for i in range(n_samples):
    dC[i]=(dC1[i]+dC2[i])/2

HVC=[97,87,95,95,102,102,90,90,99,99,93,93,94,94,98,98,80,
     80,81,81,84,84,87,87,95,95]

"ALUMINUM"
dA1=[0.1277, 0.1252, 0.1315, 0.1315, 0.1256, 0.1256, 0.1293, 0.1293, 0.1283, 
     0.1283, 0.1266, 0.1266, 0.1332, 0.1332, 0.129, 0.129, 0.1263, 0.1263, 
     0.1322, 0.1322, 0.1295, 0.1295, 0.1315, 0.1315, 0.126, 0.126]

dA2=[0.1247, 0.1254, 0.1282, 0.1282, 0.126, 0.126, 0.1274, 0.1274, 0.1269, 
     0.1269, 0.1256, 0.1256, 0.1327, 0.1327, 0.1261, 0.1261, 0.1285, 0.1285, 
     0.1306, 0.1306, 0.1289, 0.1289, 0.1304, 0.1304, 0.1253, 0.1253]

dA = zeros(n_samples)

i=0
for i in range(n_samples):
    dA[i]=(dA1[i]+dA2[i])/2
    
HVA=[116,118,110,110,117,117,113,113,114,114,117,117,105,105,114,
     114,114,114,107,107,111,111,108,108,118,118]

"2) MEAN VALUES"
dSu=0
HVSu=0

dCu=0
HVCu=0

dAu=0
HVAu=0

i=0
for i in range(n_samples):
    dSu+=dS[i]/n_samples
    HVSu+=HVS[i]/n_samples
    dCu+=dC[i]/n_samples
    HVCu+=HVC[i]/n_samples
    dAu+=dA[i]/n_samples
    HVAu+=HVA[i]/n_samples

"3) STANDARD DEVIATION"
dSd=0
HVSd=0

dCd=0
HVCd=0

dAd=0
HVAd=0

i=0
for i in range(n_samples):
    dSd+=((dS[i]-dSu)**2)/n_samples
    HVSd+=((HVS[i]-HVSu)**2)/n_samples
    dCd+=((dC[i]-dCu)**2)/n_samples
    HVCd+=((HVC[i]-HVCu)**2)/n_samples
    dAd+=((dA[i]-dAu)**2)/n_samples
    HVAd+=((HVA[i]-HVAu)**2)/n_samples
    
dSd=dSd**0.5
HVSd=HVSd**0.5

dCd=dCd**0.5
HVCd=HVCd**0.5

dAd=dAd**0.5
HVAd=HVAd**0.5

"4) GRAPHS"
x = array(arange(0,450,0.001))
yS = (1/(HVSd*sqrt(2*pi)))*(e**(-0.5*(((x-HVSu)/HVSd)**2)))
yC = (1/(HVCd*sqrt(2*pi)))*(e**(-0.5*(((x-HVCu)/HVCd)**2)))
yA = (1/(HVAd*sqrt(2*pi)))*(e**(-0.5*(((x-HVAu)/HVAd)**2)))

plot(x, yS, "k")
plot(x, yC, "r")
plot(x, yA)

xlabel('Vickers Hardness (HV)')
ylabel('Probability')
title('Gaussian Distribution of Vickers Hardness for the Specimens')
grid("on")
axis([0, 430, 0, 0.1])
legend(['Steel', 'Copper', 'Aluminum'])

show()
