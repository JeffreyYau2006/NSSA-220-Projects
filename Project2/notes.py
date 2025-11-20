# notes, don't use your own data use data supplied by lab
# scapy library, project 2 i don't think we're using?

'C:\Users\jeffr\AppData\Roaming\Python\Python312\Scripts\scapy' 
from scapy.all import *
packets = rpcap('example.pcap')
print(packets)
print(packets[1])
len(packets)
p0=packets[0]
len(p0[Ether]), len(p0[IP]), len(p0[ICMP]) # size of each object