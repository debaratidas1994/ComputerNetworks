import os, time, signal
import multiprocessing

class Node(multiprocessing.Process):
	def __init__(self, in_port, out_port):
		super().__init__()
		
		self.in_port = in_port
		self.out_port = out_port

		self.frame_buf = None
		self.message_buf = []
		self.link_pid = None
		self.rcvr_pid = None
		self.msg_rcvd = ""		

		self.seq = 0
		self.ack = 0
		
		self.start()		
	
	def initHandler(self, signo, frame):
		op, data = self.in_port.recv()
		if op == 'SET_LINK': self.link_pid = data
		elif op == 'SET_BUF': 
			self.rcvr_pid = data[0]
			self.message_buf = [data[1][i:i+5] for i in range(0,len(data[1]),5)]
			self.next_frame = {
				'sndr':self.pid, 
				'rcvr':self.rcvr_pid, 
				'data':self.message_buf.pop(0),
				'seq': self.seq
			}
			print("sndr: sending first frame- -",self.next_frame)
			self.frame_buf = self.next_frame
			self.seq = 0 if self.seq else 1
			signal.alarm(4)		
			os.kill(self.link_pid, signal.SIGUSR1)
			self.out_port.send(self.next_frame)			
	
	def recieveFrame(self, signo, frame):
		frame = self.in_port.recv()
		if 'seq' in frame: #addressed to reviever
			if frame['seq'] == self.ack:
				print("rcvr: recieved frame- ",frame)
				self.msg_rcvd += frame['data']
				print("rcvr: total message ",self.msg_rcvd)
				self.ack = 0 if self.ack else 1
			else:
				print("rcvr: frame already received- ",frame)
			self.new_frame = {
				'sndr': frame['rcvr'],
				'rcvr': frame['sndr'],
				'ack': self.ack
			}
			os.kill(self.link_pid, signal.SIGUSR2)
			self.out_port.send(self.new_frame)
		elif 'ack' in frame: #addressed to sender
			print("sndr: recieved ack frame- ",frame)
			if len(self.message_buf) ==	0: signal.alarm(0);return		
			if frame['ack'] == self.seq:
				 self.next_frame = {
					'sndr':self.pid, 
					'rcvr':self.rcvr_pid, 
					'data':self.message_buf.pop(0),
					'seq': self.seq
				 } 
			else:
				self.next_frame = self.frame_buf

			print("sndr: sending frame- ",self.next_frame)
			self.frame_buf = self.next_frame
			self.seq = 0 if self.seq else 1
			signal.alarm(4)
			os.kill(self.link_pid, signal.SIGUSR1)			
			self.out_port.send(self.next_frame)			

	def timeoutHandler(self, signo, frame):
		print("sndr: timeout occoured, resending frame-",self.frame_buf)
		self.frame_buf = self.next_frame
		signal.alarm(4)			
		os.kill(self.link_pid, signal.SIGUSR1)
		self.out_port.send(self.next_frame)	

	def run(self):
		print("node {}: starting node process".format(os.getpid()))

		signal.signal(signal.SIGUSR1, self.initHandler)
		signal.signal(signal.SIGUSR2, self.recieveFrame)
		signal.signal(signal.SIGALRM, self.timeoutHandler)
		while True:
			pass
			
