##Molpro UCCSD(T) Version
from __future__ import division
import glob
from decimal import *
import numpy as np
times = 0
finalEnergies = list()
filePaths = sorted(glob.glob('*/inp/*.0001.out'))
totalPoints = len(glob.glob('*/inp/*.com')) // len(filePaths)
for i,line in enumerate(filePaths):
    filePaths[i] = line[:-9]
for i in range(totalPoints):
    if i < 9:
        point = '.000' + str(i+1)
    elif i < 99:
        point = '.00' + str(i+1)
    elif i < 999:
        point = '.0' + str(i+1)
    else:
        point = '.' + str(i+1)
    eE = []
    for q in filePaths:
        file = open(q + point + '.out', 'r')
        data = file.readlines()
        times = times + float(data[len(data)-11].split()[3])
        for line in data:
            if line.find('RHF-UCCSD(T) energy') != -1:
                eE.append(float(line.split()[2]))
        file.close()
    CBS = Decimal(eE[6]-((eE[5]-eE[6])/(np.power(4.5,-4)-np.power(3.5,-4)))*np.power(3.5,-4)+((eE[0]-eE[6]+((eE[5]-eE[6])/\
            (np.power(4.5,-4)-np.power(3.5,-4)))*(np.power(3.5,-4)-np.power(5.5,-4)))/(0.7477488413*((np.power(3.5,-4)-np.power(5.5,-4)))\
            -np.power(3.5,-6)+np.power(5.5,-6)))*((0.7477488413*(np.power(3.5,-4)))-np.power(3.5,-6)))
    MTcore = Decimal(eE[4] - eE[3])
    DKrel = Decimal(eE[2] - eE[1])
    totalEnergy = CBS + MTcore + DKrel
    finalEnergies.append(totalEnergy)
f=open('energy.dat', 'w')
f.write('Total CcCR time (hours): {}\n'.format((times)/(60*60)))
f.write('Energies:\n')
for i in finalEnergies:
    f.write('{:.12f}\n'.format(round(i-min(finalEnergies),12)))
f.close()
