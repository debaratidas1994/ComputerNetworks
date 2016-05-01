import os, time, signal
import multiprocessing
import node

if __name__ == '__main__':	
	n0_rcv, n0_snd = multiprocessing.Pipe()
	n1_rcv, n1_snd = multiprocessing.Pipe()
	n2_rcv, n2_snd = multiprocessing.Pipe()
	n3_rcv, n3_snd = multiprocessing.Pipe()
	
	main_rcv, main_snd = multiprocessing.Pipe()

	G = [
		[0,1,3,7],
		[1,0,1,-1],
		[3,1,0,2],
		[7,-1,2,0]
	]

	#Number os Nodes in network
	N = 4
	d_n0 = {0:0,1:1,2:3,3:7}
	d_n1 = {0:1,1:0,2:1,3:999}
	d_n2 = {0:3,1:1,2:0,3:2}
	d_n3 = {0:7,1:999,2:2,3:0}
	
	a_n0 = {1:n1_snd, 2:n2_snd, 3:n3_snd}
	a_n1 = {0:n0_snd, 2:n2_snd}
	a_n2 = {1:n1_snd, 0:n0_snd, 3:n3_snd}
	a_n3 = {1:n1_snd, 2:n2_snd}
		
	n0 = node.Node(0,d_n0,a_n0,n0_rcv,main_rcv)
	n1 = node.Node(1,d_n1,a_n1,n1_rcv,main_rcv)
	n2 = node.Node(2,d_n2,a_n2,n2_rcv,main_rcv)
	n3 = node.Node(3,d_n3,a_n3,n3_rcv,main_rcv)
	
	time.sleep(2)
	
	npid = {
		0: n0.pid,
		1: n1.pid,
		2: n2.pid,
		3: n3.pid						
	}
	print(npid)
	
	os.kill(n0.pid, signal.SIGUSR1)
	main_snd.send(('SET_NPT',npid))
	os.kill(n1.pid, signal.SIGUSR1)
	main_snd.send(('SET_NPT',npid))
	os.kill(n2.pid, signal.SIGUSR1)
	main_snd.send(('SET_NPT',npid))
	os.kill(n3.pid, signal.SIGUSR1)
	main_snd.send(('SET_NPT',npid))
	
	time.sleep(2)
	
	os.kill(n0.pid, signal.SIGUSR1)
	main_snd.send(('START_DV',None))
	os.kill(n1.pid, signal.SIGUSR1)
	main_snd.send(('START_DV',None))
	os.kill(n2.pid, signal.SIGUSR1)
	main_snd.send(('START_DV',None))
	os.kill(n3.pid, signal.SIGUSR1)
	main_snd.send(('START_DV',None))
	
	#time.sleep(10)
	
	#print("changed c")
	#os.kill(n0.pid, signal.SIGUSR1)
	#main_snd.send(('SET_COST',(3,2)))
	
	#os.kill(n3.pid, signal.SIGUSR1)
	#main_snd.send(('SET_COST',(0,2)))
	
