def OLD_FILTER_filter():
	ICMPcounterRequestSent = 0
	ICMPcounterRequestReceive = 0
	ICMPcounterReplySent = 0
	ICMPcounterReplyReceive = 0

	requestBytesSent = 0
	requestBytesReceived = 0
	requestDataSent = 0
	requestDataReceived = 0

	# reading
	f = open('./NSSA-220-Projects/Project2/Captures/Captures/Node1.txt', 'r')

	# first line
	line = f.readline().strip(" ")

	# keep reading till no more lines
	while line:
		line = line.strip(" ")
		#print(line)

		if "ICMP" in line: 
			lineParts = line.split() #example: [1 0.000000] [192.168.200.1] [192.168.100.1] [ICMP]     74     Echo (ping) request  id=0x0001, seq=14/3584, ttl=128 (reply in 2)
			#print(lineParts)

			srcIP = lineParts[2] # need to know source and destination ip to check for sent vs receive
			#print(srcIP)
			dstIP = lineParts[3] 
			#print(dstIP)
			lengthByte = int(lineParts[5]) # UNDER "LENGTH"

			time = float(lineParts[1])
			if "seq=" in line:
				seq = lineParts[10]
				print(seq)
			else:
				line = f.readline().strip(" ")
				continue

			dataByte = lengthByte - 42 # 42 because of Ethernet Header (14 bytes) + IPv4 (20 bytes) + ICMP Type 8 (8 bytes) = 42
			# above info is taken from wireshark pcap if you want to look, says the info under each of the header.

			if "Echo (ping) request" in line and srcIP == "192.168.100.1": # if request is in the line and source ip is 100.1, since 100.1 is source sending, counter for sent +1
				ICMPcounterRequestSent = ICMPcounterRequestSent + 1
				requestBytesSent += lengthByte
				requestDataSent += dataByte
	
			if "Echo (ping) request" in line and dstIP == "192.168.100.1": # same as above but since dst is 100.1, that means it is receieving 
				ICMPcounterRequestReceive = ICMPcounterRequestReceive + 1
				requestBytesReceived += lengthByte      
				requestDataReceived += dataByte    

			if "Echo (ping) reply" in line and srcIP == "192.168.100.1":
				ICMPcounterReplySent = ICMPcounterReplySent + 1

			if "Echo (ping) reply" in line and dstIP == "192.168.100.1":
				ICMPcounterReplyReceive = ICMPcounterReplyReceive + 1

		# read next line
		line = f.readline().strip(" ")
	#print(strSplit)

	print("Requests Sent:", ICMPcounterRequestSent)
	print("Requests Received:", ICMPcounterRequestReceive)
	print("Replies Sent:", ICMPcounterReplySent)
	print("Replies Received:", ICMPcounterReplyReceive)

	print("Echo Request Bytes Sent:", requestBytesSent)
	print("Echo Request Bytes Received:", requestBytesReceived)      
	print("Echo Request Data Sent:", requestDataSent)
	print("Echo Request Data Received:", requestDataReceived)    
	f.close()
	
OLD_FILTER_filter()
