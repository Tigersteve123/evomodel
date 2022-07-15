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
	for b0 in np.arange(.0001, .001, .0001):
		for g0 in np.arange(.1, 1, .1):
			for ps in np.arange(.1, 1, .1):
				mod = model(b0, .0001, 11, g0, 0.001, 5, ps)
				total = np.zeros((1, len(mod.brange), len(mod.grange)), dtype=int)
				total_i1 = total.copy()
				total_i2 = total.copy()
				total_I = np.array([], dtype=int)
				total_S = np.array([], dtype=int)
				#print(total)
				#i0_uniform = np.ones((len(mod.brange), len(mod.grange)), dtype=int)
				#i0_worstcorner = np.zeros((len(mod.brange), len(mod.grange)), dtype=int)
				#i0_bestcorner = i0_worstcorner.copy()
				i0_center = np.zeros((len(mod.brange), len(mod.grange)), dtype=int)
				#i0_worstcorner[0, 0] = 50
				#i0_bestcorner[9, 4] = 50
				i0_center[5, 2] = 50
				#print(i0_center)
				for i in range(1000):
					lst1, lst2, lstI, lstS, lstAv = mod.sim(1500, i0_center.copy())
#					print(np.sum(lst1, 0), np.sum(lst2, 0), lstI, lstS)
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
				filename = 'runs/test_'+str(b0)+'_'+str(g0)+'_'+str(ps)+'.npy'
				with open(filename, 'wb') as f:
					np.save(f, out_array)

	#for i in total:
	#plt.imshow(i, cmap='gray', vmin=0, vmax=255)
	#	fig, ax = plt.subplots()
	#	im, cbar = heatmap(i, mod.brange, mod.grange)
	#	fig.tight_layout()
	#	plt.show()
	#print(lst1)
	#print(lst2)

'''mod = model(.0005, .0001, 10, 0.5, 0.001, 5, .5)
i0 = np.ones((len(mod.brange), len(mod.grange)), dtype=int) #test case
print(mod.sim(1500, i0))'''


'''runs_I = []
runs_S = []
for i in range(100):
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
