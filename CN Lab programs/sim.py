import multiprocessing as mp
import threading as t
import random

mtu=10

def packetize(data):	
	packets=[]
	for i in range(int(len(data)/mtu)):
		packets.append((i, data[i*mtu:i*mtu+mtu]))
	return packets
	
def sender(data, conn):
	with open(data) as f:
		packets=packetize(f.read())
		for packet in packets:
			conn.send(packet)

def receiver(data):
	print('receiver')

def channel(conn):
	def corrupt_data(data):
		if random.choice([True, False]):
			chars=list(data[1])
			chars[random.randint(0, len(chars)-1)]='0'
			return True, (data[0], ''.join(chars))
		return False, data
		
	def listen():
		while True:
			data=conn.recv()			
			print(corrupt_data(data))
	ch=t.Thread(target=listen)
	ch.start()
	ch.join()
	
if __name__=='__main__':
	p, c=mp.Pipe()
	s=mp.Process(target=sender, args=('data.txt', p))	
	c=mp.Process(target=channel, args=(c, ))
	s.start()
	c.start()
	c.join()
	s.join()

