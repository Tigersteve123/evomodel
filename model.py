import numpy as np
import math
#import concurrent.futures as futures

#from multiprocessing import Process

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

	def sim(self, s:int, i0:np.ndarray, tc=0, acc=1, acc_S=1):
		lstS = [s]
		lstIhat = [np.sum(i0)]
		lstI1 = [i0.copy()]
		lstI2 = [np.zeros((len(self.brange), len(self.grange)), dtype=int)]
		lstQS = [0]
		lstQI1 = [0]
		lstQI2 = [np.zeros((len(self.brange), len(self.grange)), dtype=int)]
		lstAvg = []
		lstCumAvg = []
		totalSplitTotal = np.zeros((len(self.brange), len(self.grange)), dtype=int)
		t = 0
		
		Ihat2 = np.zeros((len(self.brange), len(self.grange)), dtype=int)
		p = np.zeros((len(self.brange), len(self.grange)), dtype=float)
		Ibar = np.zeros((len(self.brange), len(self.grange)), dtype=int)
		st = np.zeros((len(self.brange), len(self.grange)), dtype=int)
		sbar = np.zeros((len(self.brange), len(self.grange)), dtype=int)
		I1 = i0.copy()
		I2 = np.zeros((len(self.brange), len(self.grange)), dtype=int)
		QI2 = I2.copy()
		
		while np.sum(I1)+np.sum(I2) > 0 and lstS[-1] > 0:
			### Trend Tracking ###
			I1_lastPeriod = lstI1[-1]
			I2_lastPeriod = lstI2[-1]
			ITotal_lastPeriod = I1_lastPeriod+I2_lastPeriod
			S_lastPeriod = lstS[-1]
			totalSplitTotal += ITotal_lastPeriod
			averageB = np.sum(np.sum(ITotal_lastPeriod, 1)*self.brange)/np.sum(ITotal_lastPeriod)
			averageG = np.sum(np.sum(ITotal_lastPeriod, 0)*self.grange)/np.sum(ITotal_lastPeriod)
			averageBCum = np.sum(np.sum(totalSplitTotal, 1)*self.brange)/np.sum(totalSplitTotal)
			averageGCum = np.sum(np.sum(totalSplitTotal, 0)*self.grange)/np.sum(totalSplitTotal)
			
			### Infection ###
			for i in range(len(self.brange)):
				for j in range(len(self.grange)):
					Ihat2[i, j] = np.random.binomial(I1_lastPeriod[i, j], self.grange[j])
			Ihat = np.random.binomial(S_lastPeriod, (1-math.prod( (np.subtract(1, self.brange))**(np.sum(I1_lastPeriod, 1)+np.sum(I2_lastPeriod, 1)) )))
			Shat = S_lastPeriod-Ihat
			
			tau = min(tc/(S_lastPeriod+np.sum(Ihat2)), 1)
			
			QS = np.random.binomial(Shat, tau*(1-acc_S))
			try: QS2 = lstQS[-2]
			except: QS2 = 0
			S = Shat-QS+QS2
			
			QI = np.random.binomial(Ihat, tau*acc)
			I = Ihat-QI
			for i in range(len(self.brange)):
				for j in range(len(self.grange)):
					QI2[i, j] = np.random.binomial(Ihat2[i, j], tau*acc)
			I2 = Ihat2-QI2
			
			for i in range(len(self.brange)):
				for j in range(len(self.grange)):
					p[i, j] = self.brange[i]*(ITotal_lastPeriod[i, j])/np.sum(self.brange* np.sum(ITotal_lastPeriod, 1)) #calculate denominator separately for efficiency
			Ibar = np.reshape(np.random.multinomial(I, p.flatten()), (len(self.brange), len(self.grange)))
			for i in range(len(self.brange)):
				for j in range(len(self.grange)):
					st[i, j] = np.random.binomial(Ibar[i, j], self.ps)
					sbar = Ibar-st
			I1 = st.copy()
			
			### Evolution ###
			for i in range(len(self.brange)):
				for j in range(len(self.grange)):
					probs = [1/len(self.neighborcoords(i, j)) for a in range(len(self.neighborcoords(i, j)))]
					neighborParray = np.random.multinomial(sbar[i, j], probs)
					narray = self.neighborcoords(i, j)
					for x in range(len(narray)):
						I1[narray[x]] = I1[narray[x]]+neighborParray[x]
			
			### Data ###
			lstS.append(S)
			lstIhat.append(Ihat)
			lstI1.append(I1)
			lstI2.append(I2)
			lstQS.append(QS)
			lstQI1.append(QI)
			lstQI2.append(QI2)
			lstAvg.append((averageB.copy(), averageG.copy()))
			lstCumAvg.append((averageBCum, averageGCum))
			t += 1
		return np.array(lstI1), np.array(lstI2), np.array(lstIhat), np.array(lstS), lstAvg, lstCumAvg, np.array(lstQS), np.array(lstQI1), np.array(lstQI2), t
