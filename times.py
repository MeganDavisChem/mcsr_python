#!/usr/bin/python
import sys
import os
#Call with folder name and number of points
times = 0
folderName = os.listdir('.')
print(folderName)
for j in folderName:
	if os.path.isdir(j):
		for i in os.listdir(j +'/inp'):
		    if ".out" in i:
			 file = open(j + '/inp/' + i)
			 data = file.readlines()
			 times = times + float(data[len(data)-1].split()[5].strip('s'))
			 print(times)
			 file.close()
print("Total time (hours): {}".format((times)/(60*60)))
