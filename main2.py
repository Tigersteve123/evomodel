from model import model
from heatmap import heatmap

import matplotlib.pyplot as plt
import numpy as np
import math

#np.random.seed(0)

if __name__ == '__main__':
	b0 = 0.0000001; g0 = 0.4
	mod = model(0.0000001, .0000001, 11, 0.4, 0.05, 5, .9)
	total = np.zeros((1, len(mod.brange), len(mod.grange)), dtype=int)
	total_i1 = total.copy()
	total_i2 = total.copy()
	total_I = np.array([], dtype=int)
	total_S = total_I.copy()
	i0_center = np.zeros((len(mod.brange), len(mod.grange)), dtype=int)
	i0_center[5, 2] = 50
	all_listAv = []
	for i in range(100):
		lst1, lst2, lstI, lstS, lstAv, lstCuAv, lstQS, lstQI1, lstQI2, t = mod.sim(1500000, i0_center.copy())
		all_listAv.append(lstCuAv.copy())
	with open('lstAv_large_cu_new.npy', 'wb') as f:
		np.save(f, all_listAv)
