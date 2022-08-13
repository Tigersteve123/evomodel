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
			ax.set_xlabel("Latency γ")
			ax.set_ylabel("Infectivity β")
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
		plt.xlabel('β')
		plt.ylabel('γ')
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
		plt.xlabel('β')
		plt.ylabel('γ')
		if savedirec:
			out_path = savedirec+'/average_ends.png'
			plt.savefig(out_path)
		if show: plt.show()
	
	def plot(self, ax, param1, param2, xlabel, ylabel, style='scatter', color=None, legend=None, savedirec=None, show=False):
		ax.set_xlabel(xlabel)
		ax.set_ylabel(ylabel)
		if style == 'scatter':
			if color is not None: ax.scatter(param1, param2, c=color)
			else: ax.scatter(param1, param2)
		elif style == 'plot':
			if color is not None: ax.plot(param1, param2, c=color)
			else: ax.plot(param1, param2)
		else: raise ValueError('invalid plot type')
		if legend:
			ax.legend(legend)
		if savedirec:
			out_path = savedirec+'/graph_'+xlabel+'_'+ylabel+'.png'
			plt.savefig(out_path)
	
	def plotQuarantine(self, qs, qi1, qi2, savedirec=None, show=False):
		fig, ax = plt.subplots()
		t = range(len(qs))
		ax.plot(t, qs)
		ax.plot(t, qi1)
		ax.plot(t, np.sum(qi2, (1, 2)))
		ax.legend(['QS', 'QI1', 'QI2'])
		ax.set_xlabel('time')
		ax.set_ylabel('individuals')
		if savedirec:
			out_path = savedirec+'/quarantine.png'
			plt.savefig(out_path)
		if show:
			plt.show()
