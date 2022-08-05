import numpy as np
import matplotlib.pyplot as plt

from model import model
from heatmap import heatmap

class summary:
	def __init__(self, run:np.ndarray, params=None, mod=None):
		self.run = run
		self.runtotal = np.sum(run, axis=0)
		if params != None: self.mod = model(params[0], .001, 10, params[1], .001, 5, params[2])
		elif mod != None: self.mod = mod
		else: self.mod = model(.0005, .0001, 11, .5, .001, 5, .5)

	def vis(self, savedirec=None, show=True):
		for i in range(len(self.run)):
			fig, ax = plt.subplots()
			im, cbar = heatmap(self.run[i], np.around(self.mod.brange, decimals=7), np.around(self.mod.grange, decimals=5), vmin=0, cmap='Greys')
			ax.set_xlabel("Latency")
			ax.set_ylabel("Infectivity")
			fig.tight_layout()
			if savedirec:
				out_path = savedirec+'/period_'+str(i)+'.png'
				plt.savefig(out_path)
		if show: plt.show()

	def vistotal(self):
		fig, ax = plt.subplots()
		im, cbar = heatmap(self.runtotal, self.mod.brange, self.mod.grange, vmin=0)
		fig.tight_layout()
		plt.show()

	def evolvedGreaterB(self):
		bless = np.sum(self.runtotal[0:5])
		bgreater = np.sum(self.runtotal[6:10])
		return bgreater > bless

	def evolvedGreaterG(self):
		gless = np.sum(self.runtotal[:, 0:2])
		ggreater = np.sum(self.runtotal[:, 3:5])
		self.gDiff = gless-ggreater
		return ggreater > gless

	def startCoords(self):
		return self.mod.brange[5], self.mod.grange[2], self.mod.ps
		
	def visAverages(self, avgArray, savedirec=None, show=True):
		plt.clf()
		for i in avgArray:
			i = np.transpose(i)
			plt.plot(i[0], i[1], c='gray')
		#print([avgArray[0][0]], [avgArray[0][1]])
		plt.plot(avgArray[0][0][0], avgArray[0][0][1], c='black', marker='o')
		plt.xlabel('beta')
		plt.ylabel('gamma')
		#print(avgArray)
		if savedirec:
			out_path = savedirec+'/average_cumulative.png'
			plt.savefig(out_path)
		if show: plt.show()
	
	def visEndAverages(self, avgArray, savedirec=None, show=True):
		plt.clf()
		ends = np.transpose(np.array([(i[-1][0], i[-1][1], len(i)) for i in avgArray]))
		#print(ends)
		plt.scatter(ends[0], ends[1], c=ends[2], cmap='gray')
		plt.plot(avgArray[0][0][0], avgArray[0][0][1], c='blue', marker='o')
		plt.xlabel('beta')
		plt.ylabel('gamma')
		if savedirec:
			out_path = savedirec+'/average_ends.png'
			plt.savefig(out_path)
		if show: plt.show()
