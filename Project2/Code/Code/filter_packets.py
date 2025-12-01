def filter():
	ICMPcounterRequestSent = 0
	ICMPcounterRequestReceive = 0
	ICMPcounterReplySent = 0
	ICMPcounterReplyReceive = 0

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

			srcIP = lineParts[2]
			#print(srcIP)
			dstIP = lineParts[3]
			#print(dstIP)

			if "Echo (ping) request" in line and srcIP == "192.168.100.1":
				ICMPcounterRequestSent = ICMPcounterRequestSent + 1
			if "Echo (ping) request" in line and dstIP == "192.168.100.1":
				ICMPcounterRequestReceive = ICMPcounterRequestReceive + 1

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
	f.close()
	
filter()
