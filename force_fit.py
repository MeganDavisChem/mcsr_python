#!/usr/bin/python
import os.path
harm = False
file = open('anpass2.out', 'r')
anData = file.readlines()
file.close()
file = open('fort.9903', 'r')
fortData = file.readlines()
file.close()
print('Squared Residuals:')
print(anData[len(anData)-1].split()[6])
print('Force constants:')
for i in fortData:
	if "1    1    0    0" in i:
		harm = True
	if harm:
		print(i.split()[4])
