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
	runsArr.append((lstCumAvg[-1][0], lstCumAvg[-1][1], len(run), int(tc)/1500000, round(float(acc), 2), np.sum(data[1]), np.average(data[8]))) #ending average beta, ending average gamma, total length, capacity, accuracy, total infected, average run length
	avgArr.append(lstAvg)
runsT = np.transpose(runsArr)
runs50 = np.transpose(sorted([x for x in runsArr if x[4] == .5], key=lambda x:x[3]))
runs70 = np.transpose(sorted([x for x in runsArr if x[4] == .7], key=lambda x:x[3]))
runs95 = np.transpose(sorted([x for x in runsArr if x[4] == .9], key=lambda x:x[3]))

savedirec='/tmp/ramdisk/'
#savedirec = None

fig, ax = plt.subplots() #Generate new figure
for i in sorted(set(runsT[3])):
	filtered = np.transpose(sorted([x for x in runsArr if x[3] == i], key=lambda x: x[4]))
	if i > 350000/1500000 and i < 650000/1500000:
		summ.plot(ax, filtered[4], filtered[1], 'accuracy', 'average gamma', style='plot', legend=range(400000, 650000, 50000), savedirec=savedirec)
fig, ax = plt.subplots() #Generate new figure
for i in sorted(set(runsT[3])):
	filtered = np.transpose(sorted([x for x in runsArr if x[3] == i], key=lambda x: x[4]))
	if i > 350000/1500000 and i < 650000/1500000:
		summ.plot(ax, filtered[4], filtered[0], 'accuracy', 'average beta', style='plot', legend=range(400000, 650000, 50000), savedirec=savedirec)
fig, ax = plt.subplots() #Generate new figure
for i in [runs50, runs70, runs95]:
	summ.plot(ax, i[3], i[1], 'test capacity', 'average gamma', style='plot', legend=['50%', '70%', '95%'], savedirec=savedirec)
fig, ax = plt.subplots() #Generate new figure
for i in [runs50, runs70, runs95]:
	summ.plot(ax, i[3], i[0], 'test capacity', 'average beta', style='plot', legend=['50%', '70%', '95%'], savedirec=savedirec)
fig, ax = plt.subplots() #Generate new figure
summ.plot(ax, runsT[3], runsT[6], 'test capacity', 'run length', style='scatter', color=runsT[4], savedirec=savedirec)
fig, ax = plt.subplots() #Generate new figure
summ.plot(ax, runsT[4], runsT[6], 'accuracy', 'run length', style='scatter', color=runsT[3], savedirec=savedirec)
fig, ax = plt.subplots() #Generate new figure
summ.plot(ax, runsT[3], runsT[5], 'test capacity', 'total infected', style='scatter', color=runsT[4], savedirec=savedirec)
fig, ax = plt.subplots() #Generate new figure
summ.plot(ax, runsT[4], runsT[5], 'accuracy', 'total infected', style='scatter', color=runsT[3], savedirec=savedirec)

'''fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
for i in sorted(set(runsT[3])):
	filtered = np.transpose(sorted([x for x in runsArr if x[3] == i], key=lambda x: x[4]))
	if i > 350000/1500000 and i < 650000/1500000:
		summ.plot(ax1, filtered[4], filtered[1], 'accuracy', 'average gamma', style='plot', legend=range(400000, 650000, 50000), savedirec=savedirec)
		summ.plot(ax2, filtered[4], filtered[0], 'accuracy', 'average beta', style='plot', legend=range(400000, 650000, 50000), savedirec=savedirec)

for i in [runs50, runs70, runs95]:
	summ.plot(ax3, i[3], i[1], 'test capacity', 'average gamma', style='plot', legend=['50%', '70%', '95%'], savedirec=savedirec)
	summ.plot(ax4, i[3], i[0], 'test capacity', 'average beta', style='plot', legend=['50%', '70%', '95%'], savedirec=savedirec)

fig, axs = plt.subplots(2, 2)
summ.plot(axs[0][0], runsT[3], runsT[6], 'test capacity', 'run length', style='scatter', color=runsT[4], savedirec=savedirec)
summ.plot(axs[0][1], runsT[4], runsT[6], 'accuracy', 'run length', style='scatter', color=runsT[3], savedirec=savedirec)
summ.plot(axs[1][0], runsT[3], runsT[5], 'test capacity', 'total infected', style='scatter', color=runsT[4], savedirec=savedirec)
summ.plot(axs[1][1], runsT[4], runsT[5], 'accuracy', 'total infected', style='scatter', color=runsT[3], savedirec=savedirec)'''
plt.show()
