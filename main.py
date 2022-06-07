from model import model
from heatmap import heatmap

import matplotlib.pyplot as plt
import numpy as np
import math

#np.random.seed(0)

#mod = model(.001, .001, 3, 0, 0, 1, 1) #"base" Reed-Frost

#mod = model(.001, .001, 10, 0.5, 0.001, 5, .5) #initial test case
#i0 = np.zeros((len(mod.brange), len(mod.xirange)), dtype=int)
#i0[0, 0] = 60
mod = model(.01, .001, 10, 0.5, 0.001, 5, .5)
i0 = np.ones((len(mod.brange), len(mod.xirange)), dtype=int) #test case
lst1, lst2, lstI, lstS = mod.sim(1500, i0)
lstI_sep = [lst1[x]+lst2[x] for x in range(len(lst1))]
for i in lstI_sep:
	#plt.imshow(i, cmap='gray', vmin=0, vmax=255)
	fig, ax = plt.subplots()
	im, cbar = heatmap(i, mod.xirange, mod.brange)
	fig.tight_layout()
	plt.show()
	#plt.show()
#print(lst1)
#print(lst2)

runs_I = []
runs_S = []
'''for i in range(100):
	lst1, lst2, lstI, lstS = mod.sim((0, 0), 60, 1500)
	runs_I.append(lstI)
	runs_S.append(lstS)
#plt.hist([max([i[0] for i in x]) for x in runs])
average_dis = [sum(x)/len(x) for x in zip(*runs_I)]
std_dis = [np.std(x) for x in zip(*runs_I)]
print(average_dis)
print(std_dis)
plt.plot([x for x in range(len(average_dis))], average_dis)
plt.plot([x for x in range(len(std_dis))], std_dis)
plt.show()'''
