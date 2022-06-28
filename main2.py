from model import model
from heatmap import heatmap

import matplotlib.pyplot as plt
import numpy as np
import math
import concurrent.futures as futures

#np.random.seed(0)

#mod = model(.001, .001, 3, 0, 0, 1, 1) #"base" Reed-Frost

if __name__ == '__main__':
	mod = model(0.0009000000000000001, .0001, 11, 0.2, 0.001, 5, 1)
	total = np.zeros((1, len(mod.brange), len(mod.grange)), dtype=int)
	total_i1 = total.copy()
	total_i2 = total.copy()
	total_I = np.array([], dtype=int)
	total_S = total_I.copy()
	i0_center = np.zeros((len(mod.brange), len(mod.grange)), dtype=int)
	i0_center[5, 2] = 50
	for i in range(1):
		lst1, lst2, lstI, lstS = mod.sim(1500, i0_center.copy())
#		print(np.sum(lst1, 0), np.sum(lst2, 0), lstI, lstS)
		for x in range(len(lst1)):
			try:
				total[x] = total[x]+lst1[x]+lst2[x]
			except:
				total = np.concatenate((total, [lst1[x]+lst2[x]]))
			try:
				total_i1[x] = total_i1[x]+lst1[x]
			except:
				total_i1 = np.concatenate((total_i1, [lst1[x]]))
			try:
				total_i2[x] = total_i2[x]+lst2[x]
			except:
			    total_i2 = np.concatenate((total_i2, [lst2[x]]))
			try:
				total_I[x] = total_I[x]+lstI[x]
			except:
				total_I = np.concatenate((total_I, [lstI[x]]))
			try:
				total_S[x] = total_S[x]+lstS[x]
			except:
				total_S = np.concatenate((total_S, [lstS[x]]))
	output_lst = [total, total_i1, total_i2, total_I, total_S]
	out_array = np.empty(len(output_lst), dtype=object)
	out_array[:] = output_lst
	with open('test_new2.npy', 'wb') as f:
		np.save(f, out_array)
