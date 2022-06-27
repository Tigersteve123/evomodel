import numpy as np
import os
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

from summary import summary
from model import model

directory_in_str = './runs/'

directory = os.fsencode(directory_in_str)

notGreaterArr = []
expArr = []

cnt = 0

for file in os.listdir(directory):
	filename = directory_in_str+os.fsdecode(file)
	params = filename.split('_')[1:]
	params[2] = params[2][:-4]
	params = [float(x) for x in params]
	mod = model(params[0], .0001, 11, params[1], 0.001, 5, params[2])
	data = np.load(filename)
	sum = summary(data, mod=mod)
	if not(sum.evolvedGreaterB() and sum.evolvedGreaterG()):
		str1 = filename
		#if not sum.evolvedGreaterB(): str1 += " B"
		#if not sum.evolvedGreaterB(): str1 += " X"
		notGreaterArr.append(sum.startCoords())
		print(sum.gDiff)
	else: expArr.append(sum.startCoords())
	cnt += 1
print(len(notGreaterArr)/cnt)
for x in sorted(notGreaterArr):
    print(x)

fig = plt.figure()
notGreaterArr_t = np.transpose(notGreaterArr)
expArr_t = np.transpose(expArr)
'''ax = plt.axes(projection='3d')
ax.scatter(notGreaterArr_t[0], notGreaterArr_t[1], notGreaterArr_t[2], c='red')
#ax.scatter(expArr_t[0], expArr_t[1], expArr_t[2], c='blue')
ax.set_xlabel("beta")
ax.set_ylabel("gamma")
ax.set_zlabel("prob. of staying")'''
ax = plt.axes()
'''ax.hist(notGreaterArr_t[1], bins=9)
ax.set_xlabel('gamma')'''
'''ax.hist(notGreaterArr_t[0], bins=9)
ax.set_xlabel('beta')'''
ax.hist(notGreaterArr_t[2], bins=9)
ax.set_xlabel('ps')

plt.show()
