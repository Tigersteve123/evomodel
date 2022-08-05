import numpy as np
import os
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import copy
from scipy.stats import chisquare
import re

from summary import summary
from model import model

directory_in_str = './runs/'

directory = os.fsencode(directory_in_str)

runsArr = []
avgArr = []

cnt = 0

for file in os.listdir(directory):
	filename = directory_in_str+os.fsdecode(file)
	params = filename.split('_')[1:]
	params[2] = params[2][:-4]
	params = [float(x) for x in params]
	mod = model(params[0], .0000001, 11, params[1], 0.05, 5, params[2])
	tc, acc = re.split('./runs/testQuarantineTc|Acc|_', filename)[1:3] #parameters from filename
	data = np.load(filename, allow_pickle=True)
	run = data[0] #total infected in data[0]
	summ = summary(data[0], mod=mod)
	lstAvg = []
	lstCumAvg = []
	totalSplitTotal = np.zeros((len(mod.brange), len(mod.grange)), dtype=int)
	for i in run:
		if np.sum(i) > 0:
			totalSplitTotal += i
			averageB = np.sum(np.sum(i, 1)*mod.brange)/np.sum(i)
			averageG = np.sum(np.sum(i, 0)*mod.grange)/np.sum(i)
			averageBCum = np.sum(np.sum(totalSplitTotal, 1)*mod.brange)/np.sum(totalSplitTotal)
			averageGCum = np.sum(np.sum(totalSplitTotal, 0)*mod.grange)/np.sum(totalSplitTotal)
			lstAvg.append((averageB.copy(), averageG.copy()))
			lstCumAvg.append((averageBCum, averageGCum))
	runsArr.append((lstCumAvg[-1][0], lstCumAvg[-1][1], len(run), int(tc), float(acc))) #ending average beta, ending average gamma, total length, capacity, accuracy
	avgArr.append(lstAvg)
runsT = np.transpose(runsArr)
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter(runsT[3], runsT[4], runsT[2])#, c=runsT[3], cmap='gray')
ax.set_xlabel('test capacity')
ax.set_ylabel('accuracy')
ax.set_zlabel('run length')
plt.show()
