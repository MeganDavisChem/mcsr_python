import os
energy_file = open("energy.dat", "r")
energies = energy_file.readlines()
energy_file.close()
qff_size = 625

#Get total number of points missing
#For each line, check if the value in the line matches up with the count up to 625
#If it doesn't, increment counter by an additional value, repeat until they match up before going on to the next line
#For each time they don't match up, write the missing value to a new file

#Get number of points missing
missing = qff_size - len(energies)


#.0084 should be my first missing value!

missing_counter = 1
missing_numbers = []
for i, line in enumerate(energies):
	searching_for = i + missing_counter
	if searching_for < 10:
		is_there = line.find('.000%d.' % searching_for)
		if is_there < 0:
			missing_numbers.append(searching_for)
			while is_there < 0:
				missing_counter += 1
				searching_for += 1
				is_there = line.find('000%d.' % searching_for)
				if is_there <0:
					missing_numbers.append(searching_for)
	elif searching_for < 100:
		is_there = line.find('.00%d.' % searching_for)
		if is_there < 0:
			missing_numbers.append(searching_for)
			while is_there < 0:
				missing_counter += 1
				searching_for += 1
				is_there = line.find('00%d.' % searching_for)
				if is_there <0:
					missing_numbers.append(searching_for)
	elif searching_for < 1000:
		is_there = line.find('.0%d.' % searching_for)
		if is_there < 0:
			missing_numbers.append(searching_for)
			while is_there < 0:
				missing_counter += 1
				searching_for += 1
				is_there = line.find('0%d.' % searching_for)
				if is_there <0:
					missing_numbers.append(searching_for)

f=open('submitmissing', 'a')
for num in missing_numbers:
	if num < 10:
		f.write('000%d\n' % num)
	elif num < 100:
		f.write('00%d\n' % num)
	elif num < 1000:
		f.write('0%d\n' % num)
f.close

