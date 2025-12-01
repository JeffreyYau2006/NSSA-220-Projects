# notes, don't use your own data use data supplied by lab
# scapy library, project 2 don't use scapy

from scapy.all import *
packets = rdpcap('./NSSA-220-Projects/Project2/example.pcap')
print(packets)
print(packets[1])
print(len(packets))
p0=packets[0]
print(len(p0[Ether]), len(p0[IP]), len(p0[ICMP])) # size of each object