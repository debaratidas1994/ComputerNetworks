import os, time, signal, random
import multiprocessing
from threading import Thread

class Link(multiprocessing.Process):
	def __init__(self, sndr_pid, sndr_in_port, sndr_out_port,
		               rcvr_pid, rcvr_in_port, rcvr_out_port):
		super().__init__()
		
		self.sndr_pid = sndr_pid
		self.rcvr_pid = rcvr_pid
		self.in_port = {sndr_pid: sndr_in_port, rcvr_pid: rcvr_in_port}	
		self.out_port = {sndr_pid: sndr_out_port, rcvr_pid: rcvr_out_port}	

		self.delayed_frame = None
		self.start()
	
	def sndrCallHandler(self, signo, sigframe):
		frame = self.in_port[self.sndr_pid].recv()
		print("link: recieved seq frame- ",frame)
		if random.randint(1,10) != 5:
			os.kill(frame['rcvr'], signal.SIGUSR2)
			self.out_port[frame['rcvr']].send(frame)
		else:
			print("link: seq frame lost")

	def rcvrCallHandler(self, signo, sigframe):
		frame = self.in_port[self.rcvr_pid].recv()
		print("link: recieved ack frame- ",frame)
		rand = random.randint(1,10)
		if rand == 3:
			print("link: ack frame lost")
		elif rand == 6:
			print("link: ack frame delayed")
			signal.alarm(5)
			self.delayed_frame = frame
		else:
			os.kill(frame['rcvr'], signal.SIGUSR2)
			self.out_port[frame['rcvr']].send(frame)			

	def timeoutHandler(self, signo, sigframe):			
		os.kill(self.delayed_frame['rcvr'], signal.SIGUSR2)
		self.out_port[self.delayed_frame['rcvr']].send(self.delayed_frame)

	def run(self):
		print("link {}: starting link process".format(os.getpid()))

		signal.signal(signal.SIGUSR1, self.sndrCallHandler)
		signal.signal(signal.SIGUSR2, self.rcvrCallHandler)
		signal.signal(signal.SIGALRM, self.timeoutHandler)

		os.kill(self.sndr_pid, signal.SIGUSR1)
		self.out_port[self.sndr_pid].send(("SET_LINK",self.pid))

		os.kill(self.rcvr_pid, signal.SIGUSR1)
		self.out_port[self.rcvr_pid].send(("SET_LINK",self.pid))

		while True:
			pass
		
