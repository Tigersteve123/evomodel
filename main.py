from model import model
from heatmap import heatmap

import matplotlib.pyplot as plt
import numpy as np
import math
import concurrent.futures as futures

#np.random.seed(0)

#mod = model(.001, .001, 3, 0, 0, 1, 1) #"base" Reed-Frost

#mod = model(.001, .001, 10, 0.5, 0.001, 5, .5) #initial test case
#i0 = np.zeros((len(mod.brange), len(mod.grange)), dtype=int)
#i0[0, 0] = 60
if __name__ == '__main__':
	b0 = 0.0000001; g0 = 0.4
	mod = model(b0, .0000001, 11, 0.4, 0.05, 5, .9)
	total = np.zeros((1, len(mod.brange), len(mod.grange)), dtype=int)
	total_i1 = total.copy()
	total_i2 = total.copy()
	total_I = np.array([], dtype=int)
	total_S = np.array([], dtype=int)
	total_QS = np.array([], dtype=int)
	total_QI1 = total.copy()
	total_QI2 = total.copy()
	i0_center = np.zeros((len(mod.brange), len(mod.grange)), dtype=int)
	i0_center[5, 2] = 50
	for i in range(1000):
		lst1, lst2, lstI, lstS, lstAv, lstCuAv, lstQS, lstQI1, lstQI2 = mod.sim(1500000, i0_center.copy(), tc=0, acc=0)
		for x in range(len(lst1)):
			#lists = [[total, lst1+lst2], [total_i1, lst1], [total_i2, lst2], [total_I, lstI], [total_S, lstS]]
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
			try:
				total_QS[x] = total_QS[x]+lstQS[x]
			except:
				total_QS = np.concatenate((total_QS, [lstQS[x]]))
			try:
				total_QI1[x] = total_QI1[x]+lstQI1[x]
			except:
				total_QI1 = np.concatenate((total_QI1, [lstQI1[x]]))
			try:
				total_QI2[x] = total_QI2[x]+lstQI2[x]
			except:
				total_QI2 = np.concatenate((total_QI2, [lstQI2[x]]))
			
	output_lst = [total, total_i1, total_i2, total_I, total_S, total_QS, total_QI1, total_QI2]
	out_array = np.empty(len(output_lst), dtype=object)
	out_array[:] = output_lst
	#filename = 'runs/test_'+str(b0)+'_'+str(g0)+'_'+str(ps)+'.npy'
	filename = 'testNoQuarantine_'+str(b0)+'_'+str(g0)+'_0.9.npy'
	with open(filename, 'wb') as f:
		np.save(f, out_array)
