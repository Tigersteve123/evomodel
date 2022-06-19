import numpy as np
import math
#import concurrent.futures as futures

#from multiprocessing import Process

class model:
	def __init__(self, b0:float, db:float, nb:int, xi0:float, dxi:float, nxi:int, ps:float):
		self.ps = ps
		#self.parray = np.array([[(b0+i*db, xi0+j*dxi) for j in range(nxi)] for i in range(nb)])
		self.brange = [b0+i*db for i in range(nb)]
		self.xirange = [xi0+j*dxi for j in range(nxi)]
		#self.shape = np.shape(self.parray)

	def e(self, n):
		return [1 for i in range(n)]

	def neighbors(self, i, j):
		neighbors = [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]
		neighbors = [x for x in neighbors if (x[0] in range(len(self.brange)) and x[1] in range(len(self.xirange)))]
		narray = np.zeros((len(self.brange), len(self.xirange)), dtype=int)
		for i in neighbors: narray[i] = 1
		return narray

	def neighborcoords(self, i, j):
		neighbors = [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]
		return [x for x in neighbors if (x[0] in range(len(self.brange)) and x[1] in range(len(self.xirange)))]

	def sim(self, s:int, i0:np.ndarray):
		lst1 = [] #history of infected
		lst2 = lst1.copy()
		lstS = [s]
		lstI = [np.sum(i0)]
		S = s #matches notation
		I1 = i0 #tracks infected in period 1
		I2 = np.zeros((len(self.brange), len(self.xirange)), dtype=int)
		p = np.zeros((len(self.brange), len(self.xirange)), dtype=float) #p(i, j)
		st = I2.copy() #s_{t, (i, j)}
		sbart = I2.copy()
		Ibar = I2.copy()
		d = I2.copy() #delta(i, j)->(i', j')
		lst1.append(I1.copy()) #current period
		lst2.append(I2.copy())
		lstS.append(S)

		def eq1(i, j):
			I2[i, j] = np.random.binomial(lst1[-1][i, j], self.xirange[j])
		def eq5(i, j):
			p[i, j] = self.brange[i]*(I1[i, j]+I2[i, j])/denom5
		def eq67(i, j):
			st[i, j] = np.random.binomial(Ibar[i, j], self.ps) #eq. 6
			sbart[i, j] = Ibar[i, j]-st[i, j]
			darray = []
			for x in self.neighborcoords(i, j): #for every neighbor
				#print(self.neighborcoords(i, j))
				probs = [1/len(self.neighborcoords(i, j)) for a in range(len(self.neighborcoords(i, j)))]
				#print(probs)
				neighborParray = np.random.multinomial(sbart[x], probs)
				print(sbart[x], neighborParray)
				narray = self.neighbors(i, j)
				#print(i, j)
				#print(narray)
				for x in range(len(self.brange)):
					for y in range(len(self.xirange)):
						if narray[x, y] == 1:
							last, neighborParray = neighborParray[-1], neighborParray[:-1] #pop
							darray.append(last)
			d[i, j] = np.sum(darray) #eq. 7
			I1[i, j] = st[i, j]+d[i, j] #eq. 8

		#executor = futures.ProcessPoolExecutor()

		while (S > 0) and (np.sum(I1)+np.sum(I2) > 0): #infected and susceptible > 0
			#with futures.ProcessPoolExecutor() as executor:
			for i in range(len(self.brange)):
				for j in range(len(self.xirange)):
					eq1(i, j)
					#Process(target=eq1, args=(i, j)).start()
					#I2[i, j] = np.random.binomial(lst1[-1][i, j], self.xirange[j]) #eq. 1
			I = np.random.binomial(S, 1-math.prod((np.subtract(1,self.brange))**(np.sum(I1, 1)+np.sum(I2, 1)))) #eq. 2
			S = lstS[-1]-I #eq. 3
			#print(I, S)
			Isum = np.sum(I1, 1)+np.sum(I2, 1)
			denom5 = np.sum(self.brange*Isum) #eq. 5 denominator
			#print("Denom ", denom5)
			if denom5 > 0: #we do need this check
			#	with futures.ProcessPoolExecutor() as executor:
				for i in range(len(self.brange)):
					for j in range(len(self.xirange)):
						eq5(i, j)
						#Process(target=eq5, args=(i, j)).start()
						#p[i, j] = self.brange[i]*(I1[i, j]+I2[i, j])/denom5 #eq. 5
					#print("Beta ", self.brange[i])
				#print("p ", p)
				Ibar_flat = np.random.multinomial(I, p.flatten()) #eq. 4
				#print(Ibar_flat)
				Ibar = np.reshape(Ibar_flat, (len(self.brange), len(self.xirange))) #eq. 4
			#else: Ibar = np.zeros(len(self.brange), len(self.xirange), dtype=int)
			#print("I ", I1+I2)
			#print("Ibar ", Ibar)
			#with futures.ProcessPoolExecutor() as executor:
			for i in range(len(self.brange)):
				for j in range(len(self.xirange)):
					#eq67(i, j)
					#Process(target=eq67, args=(i, j)).start()
					st[i, j] = np.random.binomial(Ibar[i, j], self.ps) #eq. 6
					sbart[i, j] = Ibar[i, j]-st[i, j]
			I1 = st.copy()
			for i in range(len(self.brange)):
				for j in range(len(self.xirange)):
					probs = [1/len(self.neighborcoords(i, j)) for a in range(len(self.neighborcoords(i, j)))]
					neighborParray = np.random.multinomial(sbart[i, j], probs)
					narray = self.neighborcoords(i, j)
					#print(narray)
					for x in range(len(narray)):
						#print(I1[narray[x]])
						I1[narray[x]] = I1[narray[x]]+neighborParray[x]
			#		darray = []
			#		for x in self.neighborcoords(i, j): #for every neighbor
			#			#print(self.neighborcoords(i, j))
			#			neighborParray = np.random.multinomial(sbart[x], [1/len(self.neighborcoords(i, j)) for a in range(len(self.neighborcoords(i, j)))] )
			#			narray = self.neighbors(i, j)
			#			#print(i, j)
			#			#print(narray)
			#			for x in range(len(self.brange)):
			#				for y in range(len(self.xirange)):
			#					if narray[x, y] == 1:
			#						last, neighborParray = neighborParray[-1], neighborParray[:-1] #pop
			#						darray.append(last)
			#		d[i, j] = np.sum(darray) #eq. 7
			#		I1[i, j] = st[i, j]+d[i, j]
			#print(st)
			#print("D ", d)
			#print(I1)
			lst1.append(I1.copy())
			lst2.append(I2.copy())
			lstI.append(np.sum(I1)+np.sum(I2))
			lstS.append(S)
			#print("==================================================")
		#print(lst1)
		return lst1, lst2, lstI, lstS
