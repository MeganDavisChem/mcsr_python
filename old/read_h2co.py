#!/usr/bin/python
import os.path
import subprocess
import sys
anHarm = False
geomGot = False
rots = []
distort = []
"""
if os.path.isfile('spectro2.out'):
	file = open('spectro2.out', 'r')
elif os.path.isfile('spectro1.out'):
	file = open('spectro1.out', 'r')
else:
	file = open('spectro.out', 'r')
"""
file = open(sys.argv[1],'r')
data = file.readlines()	

for i,line in enumerate(data):
	if "BAND" in line:
		print("Harmonics (v1/v2/v3) (cm-1)")
		print(data[i+4].split()[1])
		print(data[i+5].split()[1])
		print(data[i+6].split()[1])
	if "STATE NO." in line:
		anHarm = True
		print("Anharmonics (v1/v2/v3) (cm-1)")
 	if anHarm:
		if "1    0    0" in line:
			nu1 = line.split()[2]
		elif "0    1    0" in line:
			nu2 = line.split()[2]
		elif "0    0    1" in line:
			nu3 = line.split()[2]
		elif "0    0    0" in line:
			zp = line.split()[1]
	if "ROTATIONAL ENERGY LEVEL" in line:
		anHarm = False
		print(nu1)
		print(nu2)
		print(nu3)
		print("Zero point! (cm-1)")
		print(zp)
	if "INT COORD TYPE" in line and not geomGot:
		print("Geom (ang/deg):")
		print(data[i+2].split()[4])
		print(data[i+3].split()[4])
		print(data[i+4].split()[4])
		geomGot = True
	if "Be" in line:
		rots.append(line.split()[2])
	if "BZS" in line:
		rots.append(data[i+1].split()[2])
		rots.append(data[i+1].split()[0])
		rots.append(data[i+1].split()[1])
	if "D J  :" in line:
		distort.append(data[i].split()[4])
		distort.append(data[i+1].split()[4])
		distort.append(data[i+2].split()[4])
		distort.append(data[i+3].split()[4])
		distort.append(data[i+4].split()[4])
	if "H J  :" in line:
		distort.append(data[i].split()[4])
		distort.append(data[i+1].split()[4])
		distort.append(data[i+2].split()[4])
		distort.append(data[i+3].split()[4])
		distort.append(data[i+4].split()[4])
		distort.append(data[i+5].split()[4])
		distort.append(data[i+6].split()[4])

print("Rotations (Be/B0/B1/B2/B3) (cm-1)")
for i in range(0,15):
	print(rots[i])
print("Distortions (Hz):")
for i in distort:
	if "D" in i:
		print(i.replace("D","E"))
	else:
		print(i)
subprocess.call('force_fit.py',shell=True)
