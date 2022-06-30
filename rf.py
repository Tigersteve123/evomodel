import numpy as np
import matplotlib.pyplot as plt

def rf(i0, s0, p):
	#i = number infected
	#s = number susceptible
	#p = probability of infection
	i = i0
	s = s0
	arr_i = []
	arr_s = []
	arr_r = []
	while i > 0 and s > 0:
		#print(i, s)
		arr_i.append(i)
		arr_s.append(s)
		arr_r.append((i0+s0)-(i+s))
		i = np.random.binomial(s, (1-(1-p)**i))
		s -= i
	return arr_i, arr_s, arr_r

np.random.seed(0)
runs_i = []
runs_s = []
for i in range(100):
	i, s, r = rf(60, 1440, .001)
	runs_i.append(i)
	runs_s.append(s)
#plt.hist([len(i) for i in runs])
#plt.hist([max([i[0] for i in x]) for x in runs])
#plt.show()
average_dis = [sum(x)/len(x) for x in zip(*runs_i)]
print([sum(x)/len(x) for x in zip(*runs_i)])
std_dis = [np.std(x) for x in zip(*runs_i)]
print(std_dis)
plt.plot([x for x in range(len(average_dis))], average_dis)
#plt.plot([x for x in range(len(std_dis))], std_dis)
plt.show()
