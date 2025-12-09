def parse(line):
    parts = line.split()

    number = parts[0]
    time = float(parts[1])
    srcIP = parts[2]
    dstIP = parts[3]
    length = int(parts[5])
    dataBytes = length - 42 # 42 because of Ethernet Header (14 bytes) + IPv4 (20 bytes) + ICMP Type 8 (8 bytes) = 42
	# above info is taken from wireshark pcap if you want to look, says the info under each of the header.
    
    icmpType = None
    if "Echo (ping) request" in line:
        icmpType = "request"
    elif "Echo (ping) reply" in line:
        icmpType = "reply"
    else:
        return None

    for i in parts:
        if "seq=" in i:
            # p example: seq=93/23808,
            rightSide = i.split("=")[1]      # "93/23808,"
            seqPart = rightSide.split("/")[0]  # "93"

    # return the parsed packet fields
    packet = {"number": number,  "time": time, "srcIP": srcIP, "dstIP": dstIP, "length": length, "dataBytes": dataBytes, "icmpType": icmpType, "seq": seqPart}

    return packet
