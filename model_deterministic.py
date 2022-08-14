import numpy as np
import math

class model:
	def __init__(self, b0:float, db:float, nb:int, g0:float, dg:float, ng:int, ps:float):
		self.ps = ps
		self.brange = [b0+i*db for i in range(nb)]
		self.grange = [g0+j*dg for j in range(ng)]

	def e(self, n):
		return [1 for i in range(n)]

	def neighbors(self, i, j):
		neighbors = [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]
		neighbors = [x for x in neighbors if (x[0] in range(len(self.brange)) and x[1] in range(len(self.grange)))]
		narray = np.zeros((len(self.brange), len(self.grange)), dtype=int)
		for i in neighbors: narray[i] = 1
		return narray

	def neighborcoords(self, i, j):
		neighbors = [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]
		return [x for x in neighbors if (x[0] in range(len(self.brange)) and x[1] in range(len(self.grange)))]
	
	def sim(self, s, i0:np.ndarray, C=0, alpha=0):
		lstS = [s]
		lstIhat = [np.sum(i0)]
		lstI1 = [i0.copy()]
		lstI2 = [np.zeros((len(self.brange), len(self.grange)))]#, dtype=int)]
		lstQS = [0]
		lstQI1 = [0]
		lstQI2 = [np.zeros((len(self.brange), len(self.grange)))]#, dtype=int)]
		t = 0
		
		Ihat2 = np.zeros((len(self.brange), len(self.grange)))#, dtype=int)
		p = np.zeros((len(self.brange), len(self.grange)), dtype=float)
		Ibar = np.zeros((len(self.brange), len(self.grange)))#, dtype=int)
		st = np.zeros((len(self.brange), len(self.grange)))#, dtype=int)
		sbar = np.zeros((len(self.brange), len(self.grange)))#, dtype=int)
		I1 = i0.copy()
		I2 = np.zeros((len(self.brange), len(self.grange)))#, dtype=int)
		QI2 = I2.copy()
		
		while np.sum(I1)+np.sum(I2) > 0.1 and lstS[-1] > 0.1:
			#print(np.sum(I1)+np.sum(I2), lstS[-1])
			I1_lastPeriod = lstI1[-1]
			I2_lastPeriod = lstI2[-1]
			ITotal_lastPeriod = I1_lastPeriod+I2_lastPeriod
			S_lastPeriod = lstS[-1]
			
			### Infection ###
			for i in range(len(self.brange)):
				for j in range(len(self.grange)):
					Ihat2[i, j] = (I1_lastPeriod[i, j]*self.grange[j])
			Ihat = (S_lastPeriod*(1-math.prod( (np.subtract(1, self.brange))**(np.sum(I1_lastPeriod, 1)+np.sum(I2_lastPeriod, 1)) )))
			Shat = S_lastPeriod-Ihat
			
			tau = min(C/(S_lastPeriod+np.sum(Ihat2)), 1)
			
			QS = (Shat*tau*(1-alpha))
			try: QS2 = lstQS[-2]
			except: QS2 = 0
			S = Shat-QS+QS2
			
			QI = (Ihat*tau*alpha)
			I = Ihat-QI
			for i in range(len(self.brange)):
				for j in range(len(self.grange)):
					QI2[i, j] = (Ihat2[i, j]*tau*alpha)
			I2 = Ihat2-QI2
			
			for i in range(len(self.brange)):
				for j in range(len(self.grange)):
					p[i, j] = self.brange[i]*(ITotal_lastPeriod[i, j])/np.sum(self.brange* np.sum(ITotal_lastPeriod, 1)) #calculate denominator separately for efficiency
					Ibar[i, j] = (I*p[i, j])
					st[i, j] = (Ibar[i, j]*self.ps) #take out of loop
					sbar[i, j] = Ibar[i, j]-st[i, j]
			I1 = st.copy()
			
			### Evolution ###
			for i in range(len(self.brange)):
				for j in range(len(self.grange)):
					probs = [1/len(self.neighborcoords(i, j)) for a in range(len(self.neighborcoords(i, j)))]
					neighborParray = [(x) for x in np.multiply(sbar[i, j], probs)]
					narray = self.neighborcoords(i, j)
					for x in range(len(narray)):
						I1[narray[x]] = I1[narray[x]]+neighborParray[x]
			#print(I1)
			
			### Data ###
			lstS.append(S)
			lstIhat.append(Ihat)
			lstI1.append(I1)
			lstI2.append(I2)
			lstQS.append(QS)
			lstQI1.append(QI)
			lstQI2.append(QI2)
			t += 1
		return np.array(lstS), np.array(lstIhat), np.array(lstI1), np.array(lstI2), np.array(lstQS), np.array(lstQI1), np.array(lstQI2), t

mod = model(.0000001, .0000001, 11, .4, 0.05, 5, .9)
i0 = np.zeros((len(mod.brange), len(mod.grange)))#, dtype=int)
i0[5, 2] = 50
for tc in range(0, 1500000, 50000):
	#acc = 0.95
	#if acc == 0.95:
	for acc in np.arange(0, 1, .1):
		lstS, lstIhat, lstI1, lstI2, lstQS, lstQI1, lstQI2, t = mod.sim(1500000, i0.copy(), tc, acc)
		output_lst = [lstI1+lstI2, lstS, lstIhat, lstI1, lstI2, lstQS, lstQI1, lstQI2, t]
		out_array = np.empty(len(output_lst), dtype=object)
		out_array[:] = output_lst
		filename = 'runsDeterministic/testQuarantineTc'+str(tc)+'Acc'+str(acc)+'_'+str(0.0000001)+'_'+str(0.4)+'_0.9.npy'
		print(filename)
		with open(filename, 'wb') as f:
			np.save(f, out_array)
