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

	def vis(self):
		for i in self.run:
			fig, ax = plt.subplots()
			im, cbar = heatmap(i, self.mod.brange, self.mod.grange, vmin=0)
			fig.tight_layout()
		plt.show()

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
		return ggreater > gless
