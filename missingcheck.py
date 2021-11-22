#!/usr/bin/python
import os 
import sys
energy_file = open("energy.dat", "r")
energies = energy_file.readlines()
energy_file.close()
qff_size = int(sys.argv[1])
#qff_size = 723

miss = 1
missing = False

missing_numbers = []
for i in range(0,len(energies)):
	j = i + miss
	if j < 10:
		number = '.000%d.'%j
	elif j < 100:
		number = '.00%d.'%j
	elif j < 1000:
		number = '.0%d.'%j
	else:
		number = '.%d.'%j
	if not (number in energies[i]):
		missing = True
	while missing:
		miss = miss + 1
		missing_numbers.append(number)
		j = i + miss
		if j < 10:
			number = '.000%d.'%j
		elif j < 100:
			number = '.00%d.'%j
		elif j < 1000:
			number = '.0%d.'%j
		else:
			number = '.%d.'%j
		if number in energies[i]:
			missing = False

if qff_size < 10:
	number = '.000%d.'%qff_size
elif qff_size < 100:
	number = '.00%d.'%qff_size
elif qff_size < 1000:
	number = '.0%d.'%qff_size
else:
	number = '.%d.'%qff_size
if not (number in energies[len(energies)-1]):
	missing_numbers.append(number)

f = open("submitmissing","w")
for num in missing_numbers:
	f.write("qsub *"+num+'pbs\n')
f.close()
os.chmod("submitmissing", 0755)
