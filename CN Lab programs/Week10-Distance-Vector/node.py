import os, time, signal, copy
import multiprocessing

class Node(multiprocessing.Process):
	def __init__(self, node_id, cm, out, inp, main_rcv):
		super().__init__()
	
		self.nid = node_id
		self.cm = cm
		self.dv = copy.deepcopy(cm)
		self.out = out
		self.inp = inp
		self.main_rcv = main_rcv	
		self.npt = None	#node pid table
		
		self.start()		
	
	def initHandler(self, signo, frame):
		op, data = self.main_rcv.recv()
		if op == 'SET_NPT':
			self.npt = data
		elif op == 'START_DV':
			for nid in self.out:
				os.kill(self.npt[nid], signal.SIGUSR2)
				self.out[nid].send((self.nid,self.dv))	
		elif op == 'SET_COST':
			self.cm[data[0]] = data[1]
			if self.dv[data[0]]>self.cm[data[0]]:
				self.dv[data[0]] = data[1]
				for nid in self.out:
					os.kill(self.npt[nid], signal.SIGUSR2)
					self.out[nid].send((self.nid,self.dv))
	
	def messageHandler(self, signo, frame):
		nnid, ndv = self.inp.recv()
		dv_changed = False
		for nid in self.dv:
			old = self.dv[nid]
			self.dv[nid] = min(self.cm[nnid]+ndv[nid], self.dv[nid])
			if self.dv[nid]!=old: dv_changed = True
		if dv_changed:
			print("dv updated",self.pid,self.nid,self.dv)
			for nid in self.out:
				os.kill(self.npt[nid], signal.SIGUSR2)
				self.out[nid].send((self.nid,self.dv))

	def run(self):
		print("node {}: starting node process".format(os.getpid()))

		signal.signal(signal.SIGUSR1, self.initHandler)
		signal.signal(signal.SIGUSR2, self.messageHandler)
		while True:
			pass
			
