import packet_parser 

def compute(node):
    # Counters
    ICMPcounterRequestSent = 0
    ICMPcounterRequestReceive = 0
    ICMPcounterReplySent = 0
    ICMPcounterReplyReceive = 0

    requestBytesSent = 0
    requestBytesReceived = 0
    requestDataSent = 0
    requestDataReceived = 0

    request_times = {}  # key: seq, value: time sent
    rtt_total = 0
    rtt_count = 0
    reply_delays = []

    # For average reply delay (time request -> reply received by 192.168.100.1)
    reply_delays = []

    fInputFile = "./" + "Node" + str(node) + "_filtered_output.txt"
    f = open(fInputFile, 'r')                    
    line = f.readline()

    while line:
        line = line.strip(" ")

        parsed = packet_parser.parse(line)

        if parsed != None:

            srcIP = parsed["srcIP"]
            dstIP = parsed["dstIP"]
            length = parsed["length"]
            dataBytes = parsed["dataBytes"]
            icmpType = parsed["icmpType"]
            seq = parsed["seq"]
            time = parsed["time"]


            # Request sent
            if icmpType == "request" and srcIP == "192.168.100.1": # if request is in the line and source ip is 100.1, since 100.1 is source sending, counter for sent +1
                ICMPcounterRequestSent += 1
                requestBytesSent += length
                requestDataSent += dataBytes
                request_times[seq] = time  # store send time for RTT

            # Request received
            if icmpType == "request" and dstIP == "192.168.100.1": # same as above but since dst is 100.1, that means it is receieving
                ICMPcounterRequestReceive += 1
                requestBytesReceived += length
                requestDataReceived += dataBytes

            # Reply sent
            if icmpType == "reply" and srcIP == "192.168.100.1": 
                ICMPcounterReplySent += 1

            # Reply received
            if icmpType == "reply" and dstIP == "192.168.100.1":
                ICMPcounterReplyReceive += 1

                # rtt calculation
                if seq in request_times:
                    rtt = (time - request_times[seq]) * 1000  # convert to ms
                    rtt_total += rtt
                    rtt_count += 1
                    reply_delays.append(rtt * 1000)  # store in microseconds

        line = f.readline()

    f.close()
    # Metrics calculations
    avg_rtt = rtt_total / rtt_count if rtt_count > 0 else 0

    total_time = 0
    if request_times:
        total_time = max(request_times.values()) - min(request_times.values())

    throughput_kB = requestBytesSent / 1024 / total_time
    goodput_kB = requestDataSent / 1024 / total_time
    avg_reply_delay_us = sum(reply_delays) / len(reply_delays) if reply_delays else 0
    print("Echo Requests Sent", ICMPcounterRequestSent)
    print("Echo Requests Received", ICMPcounterRequestReceive)
    print("Echo Replies Sent", ICMPcounterReplySent)
    print("Echo Replies Received", ICMPcounterReplyReceive)

    print("Echo Request Bytes Sent", requestBytesSent)
    print("Echo Request Bytes Received", requestBytesReceived)
    print("Echo Request Data Sent", requestDataSent)
    print("Echo Request Data Received", requestDataReceived)

    print(f"Average RTT (ms): {avg_rtt:.2f}")
    print(f"Echo Request Throughput (kB/sec): {throughput_kB:.1f}")
    print(f"Echo Request Goodput (kB/sec): {goodput_kB:.1f}")
    print(f"Average Reply Delay (us): {avg_reply_delay_us:.2f}")
    print(parsed)
compute(1)