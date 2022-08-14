import numpy as np
import os
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import copy
from scipy.stats import chisquare
import re

from summary import summary
from model import model

directory_in_str = './runsDeterministic/'

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

fig1, ax1 = plt.subplots() #Generate new figures. Must call all figures and plot sequentially for output to correctly save
'''for i in sorted(set(runsT[3])):
	filtered = np.transpose(sorted([x for x in runsArr if x[3] == i], key=lambda x: x[4]))
	if i > 350000/1500000 and i < 650000/1500000:
		summ.plot(ax1, filtered[4], filtered[1], 'accuracy', 'average γ', style='plot', legend=range(400000, 650000, 50000), savedirec=savedirec)'''
summ.plot(ax1, runsT[4], runsT[1], 'accuracy', 'average γ', style='scatter', color=runsT[3], savedirec=savedirec)
fig2, ax2 = plt.subplots()
'''for i in sorted(set(runsT[3])):
	filtered = np.transpose(sorted([x for x in runsArr if x[3] == i], key=lambda x: x[4]))
	if i > 350000/1500000 and i < 650000/1500000:
		summ.plot(ax2, filtered[4], filtered[0], 'accuracy', 'average β', style='plot', legend=range(400000, 650000, 50000), savedirec=savedirec)'''
summ.plot(ax2, runsT[4], runsT[0], 'accuracy', 'average β', style='scatter', color=runsT[3], savedirec=savedirec)
fig3, ax3 = plt.subplots()
for i in [runs50, runs70, runs95]:
	summ.plot(ax3, i[3], i[1], 'test capacity', 'average γ', style='plot', legend=['50%', '70%', '95%'], savedirec=savedirec)
fig4, ax4 = plt.subplots()
for i in [runs50, runs70, runs95]:
	summ.plot(ax4, i[3], i[0], 'test capacity', 'average β', style='plot', legend=['50%', '70%', '95%'], savedirec=savedirec)
fig5, ax5 = plt.subplots()
for i in [runs50, runs70, runs95]:
	summ.plot(ax5, i[3], i[6], 'test capacity', 'average run length', style='plot', savedirec=savedirec, legend=['50%', '70%', '95%'])
fig6, ax6 = plt.subplots()
for i in sorted(set(runsT[3])):
	filtered = np.transpose(sorted([x for x in runsArr if x[3] == i], key=lambda x: x[4]))
	if i > 350000/1500000 and i < 650000/1500000:
		summ.plot(ax6, filtered[4], filtered[6], 'accuracy', 'average run length', style='plot', legend=range(400000, 650000, 50000), savedirec=savedirec)
fig7, ax7 = plt.subplots()
for i in [runs50, runs70, runs95]:
	summ.plot(ax7, i[3], i[5]/1000, 'test capacity', 'average total infected', style='plot', savedirec=savedirec, legend=['50%', '70%', '95%'])
fig8, ax8 = plt.subplots()
for i in sorted(set(runsT[3])):
	filtered = np.transpose(sorted([x for x in runsArr if x[3] == i], key=lambda x: x[4]))
	if i > 350000/1500000 and i < 650000/1500000:
		summ.plot(ax8, filtered[4], filtered[5]/1000, 'accuracy', 'average total infected', style='plot', legend=range(400000, 650000, 50000), savedirec=savedirec)
#plt.show()
