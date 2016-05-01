def bin_dec(bins):
	binary=bins
	d=int(binary,2)
	return d

def func_ip(ip):
	version=ip[0:4]
	print("version : "+str(bin_dec(version)))
	ihl=ip[4:8]
	print("ihl : "+str(bin_dec(ihl)*4))
	types=ip[8:16]
	print("type : "+str(bin_dec(types)))
	total_length=ip[16:32]
	print("total length : "+str(bin_dec(total_length)))
	identification=ip[32:48]
	print("identification : "+str(bin_dec(identification)))
	flags=ip[48:51]
	print("flags : "+str(bin_dec(flags)))
	offset=ip[51:64]
	print("offset : "+str(bin_dec(offset)))
	ttl=ip[64:72]
	print("ttl : "+str(bin_dec(ttl)))
	protocol=ip[72:80]
	print("protocol : "+str(bin_dec(protocol)))
	checksum=ip[80:96]
	print("checksum : "+str(bin_dec(checksum)))
	source_ip=ip[96:128]
	f1=ip[96:104]
	f2=ip[104:112]
	f3=ip[112:120]
	f4=ip[120:128]
	print("source ip : "+str(bin_dec(f1))+"."+str(bin_dec(f2))+"."+str(bin_dec(f3))+"."+str(bin_dec(f4)))
	f1=ip[128:136]
	f2=ip[136:144]
	f3=ip[144:152]
	f4=ip[152:]
	print("dest ip : "+str(bin_dec(f1))+"."+str(bin_dec(f2))+"."+str(bin_dec(f3))+"."+str(bin_dec(f4)))
	data=ip[160:]
	
def func_tcp(tcp):
	sp=tcp[0:16]
	print("source port : "+str(bin_dec(sp)))
	dp=tcp[16:32]
	print("dest port : "+str(bin_dec(dp)))
	seqno=tcp[32:64]
	print("seq no : "+str(bin_dec(seqno)))
	ackno=tcp[16:32]
	print("ack no : "+str(bin_dec(ackno)))
	header=tcp[32:36]
	print("header length : "+str(bin_dec(header)))
	reserve=tcp[36:42]
	print("reserve : "+str(bin_dec(reserve)))
	code=tcp[42:48]
	print("code : "+str(bin_dec(code)))
	window=tcp[48:64]
	print("window : "+str(bin_dec(window)))
	checksum=tcp[64:80]
	print("checksum : "+str(hex(bin_dec(checksum))))
	urgent=tcp[80:96]
	print("urgent : "+str(bin_dec(urgent)))
	options=tcp[96:128]
	print("options : "+str(bin_dec(options)))
	
	
	
data_input="0100010100000000000000100001110100000001110011010100000000000000100000000000011000000000000000001100000010101000000000010110011010000000011101111111010100001100000100000001111100000000010100001111010100110010011001001011001001100100101100100110101110100110010101001001001001010000000110000011100110100010000000000000000011111111111111111111111111111111111111111111111111111111111111111111111111111111"
ip=data_input[0:160]
tcp=data_input[160:320]
dummy=data_input[320:400]
print("ORIGINALLY")
print("-------------------------------------------------------------")
print("ip",ip)
print("tcp",tcp)
print("dummy",dummy)
print("-------------------------------------------------------------")
print("IP PDU")
func_ip(ip)
print("-------------------------------------------------------------")
print("TCP PDU")
func_tcp(tcp)	
print("-------------------------------------------------------------")

	

