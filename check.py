import numpy as np
import os
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import copy
from scipy.stats import chisquare

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
	mod = model(params[0], .0000001, 11, params[1], 0.05, 5, params[2])
	data = np.load(filename, allow_pickle=True)
	summ = summary(data[1], mod=mod)
	if not(summ.evolvedGreaterB() and summ.evolvedGreaterG()):
		str1 = filename
		notGreaterArr.append(summ.startCoords())
		#print(summ.gDiff)
	else: expArr.append(summ.startCoords())
	cnt += 1
print(len(notGreaterArr)/cnt)
#for x in sorted(notGreaterArr):
#    print(x)

fig = plt.figure()
notGreaterArr_t = np.transpose(notGreaterArr)
expArr_t = np.transpose(expArr)
labels = ['Did not evolve greater', 'Evolved greater']
'''ax = plt.axes(projection='3d')
ax.scatter(notGreaterArr_t[0], notGreaterArr_t[1], notGreaterArr_t[2], c='red')
#ax.scatter(expArr_t[0], expArr_t[1], expArr_t[2], c='blue')
ax.set_xlabel("beta")
ax.set_ylabel("gamma")
ax.set_zlabel("prob. of staying")'''
ax = plt.axes()
'''for i in range(3):
    numInBins = ax.hist([notGreaterArr_t[i], expArr_t[i]], bins=9, stacked=True, label=labels)
    print(chisquare(numInBins[0][0]))
    print(sorted(numInBins[0][0]))
    ax.set_xlabel(['beta', 'gamma', 'ps'][i])
    ax.set_ylabel('Runs')
    ax.legend()
    #plt.show()
    #plt.savefig('/tmp/ramdisk/'+['beta', 'gamma', 'ps'][i]+'.png')
    ax.clear()'''
