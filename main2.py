from model import model
from heatmap import heatmap

import matplotlib.pyplot as plt
import numpy as np
import math
import concurrent.futures as futures

#np.random.seed(0)

#mod = model(.001, .001, 3, 0, 0, 1, 1) #"base" Reed-Frost

if __name__ == '__main__':
	mod = model(0.0006000000000000001, .0001, 11, 0.1, 0.001, 5, .6)
	total = np.zeros((1, len(mod.brange), len(mod.grange)), dtype=int)
	total1 = total.copy()
	total2 = total.copy()
	i0_center = np.zeros((len(mod.brange), len(mod.grange)), dtype=int)
	i0_center[5, 2] = 50
	for i in range(1000):
		lst1, lst2, lstI, lstS = mod.sim(1500, i0_center.copy())
		for x in range(len(lst1)):
			try:
				total[x] = total[x]+lst1[x]+lst2[x]
				total1[x] = total1[x]+lst1[x]
				total2[x] = total2[x]+lst2[x]
			except:
				total = np.concatenate((total, [lst1[x]+lst2[x]]))
				total1 = np.concatenate((total1, [lst1[x]]))
				total2 = np.concatenate((total2, [lst2[x]]))
	print(np.sum(total), np.sum(total1), np.sum(total2))
	#filename = 'runs/test_'+str(b0)+'_'+str(g0)+'_'+str(ps)+'.npy'
	with open('test1.npy', 'wb') as f:
		np.save(f, total)

	#for i in total:
	#plt.imshow(i, cmap='gray', vmin=0, vmax=255)
	#	fig, ax = plt.subplots()
	#	im, cbar = heatmap(i, mod.brange, mod.xirange)
	#	fig.tight_layout()
	#	plt.show()
	#print(lst1)
	#print(lst2)
