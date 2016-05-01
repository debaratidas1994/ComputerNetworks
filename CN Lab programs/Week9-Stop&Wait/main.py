import os, time, signal
import multiprocessing
import link, node

if __name__ == '__main__':	
	sc_out, cs_in = multiprocessing.Pipe()
	sc_in, cs_out = multiprocessing.Pipe()

	rc_out, cr_in = multiprocessing.Pipe()
	rc_in, cr_out = multiprocessing.Pipe()

	sndr = node.Node(sc_in, sc_out)
	rcvr = node.Node(rc_in, rc_out)
	
	time.sleep(1)
	chnl = link.Link(sndr.pid, cs_in, cs_out,
	  			     rcvr.pid, cr_in, cr_out)

	time.sleep(1)
	
	msg = "CS is the best branch at PESIT, I'm glad to be studing here."	
	
	os.kill(sndr.pid, signal.SIGUSR1)
	cs_out.send(('SET_BUF',(rcvr.pid, msg)))
