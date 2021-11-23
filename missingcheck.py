#!/usr/bin/python
#run as missingcheck.py <filename> <# points>
import os 
from sys import argv
#read in energy.dat
#energy_file = open("energy.dat", "r")
energy_file = open("{}".format(argv[1]), "r")
energies = energy_file.readlines()
energy_file.close()
#specify qffSize
qffSize = int(argv[2])

#initialize stuff
miss = 1
missing = False
missing_numbers = []

#start searching through energies
for i in range(0,len(energies)):
    #set current number to iteration + number of missing points
    j = i + miss
    number = '.{:04}.'.format(j)

    #check if current number is missing
    if not (number in energies[i]):
        missing = True

    #iterate over missing points until one is found
    while missing:
        miss = miss + 1
        missing_numbers.append(number)
        j = i + miss
        number = '.{:04}.'.format(j)
        #return to main loop once a number is found
        if number in energies[i]:
            missing = False

#check for final point
if not ('.{:04}.'.format(qffSize) in energies[len(energies)-1]):
    missing_numbers.append('.{:04}.'.format(qffSize))

#write submit script for eland or mcsr
missingscript = "submiss_{}".format(argv[1].split(".")[0])

f = open(missingscript,"w")
if os.uname()[1] == 'master':
    for num in missing_numbers:
        f.write("sbatch *"+num+'sh\n')
else:
    for num in missing_numbers:
        f.write("qsub *"+num+'pbs\n')
f.close()
os.chmod(missingscript, 0755)
