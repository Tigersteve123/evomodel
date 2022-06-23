import numpy as np
import os

from summary import summary

directory_in_str = './runs/'

directory = os.fsencode(directory_in_str)

notGreaterArr = []

cnt = 0

for file in os.listdir(directory):
	filename = directory_in_str+os.fsdecode(file)
	data = np.load(filename)
	sum = summary(data)
	if not(sum.evolvedGreaterB() and sum.evolvedGreaterG()):
		str1 = filename
		#if not sum.evolvedGreaterB(): str1 += " B"
		#if not sum.evolvedGreaterB(): str1 += " X"
		notGreaterArr.append(str1)
		print(sum.evolvedGreaterB(), sum.evolvedGreaterG())
	cnt += 1
print(len(notGreaterArr)/cnt)
print(sorted(notGreaterArr))
