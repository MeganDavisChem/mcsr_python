#!/usr/bin/python
import sys
import os
#Call with folder name and number of points
times = 0
folderName = sys.argv[1]
for i in os.listdir(folderName+'/inp'):
    if ".out" in i:
         file = open(folderName + '/inp/' + i)
         data = file.readlines()
         times = times + float(data[len(data)-1].split()[5].strip('s'))
	 print(times)
         file.close()
print("Total time (hours): {}".format((times)/(60*60)))
