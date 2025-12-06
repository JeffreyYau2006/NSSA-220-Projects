import packet_parser   

def infer_hops_from_ttl(ttl):
    if ttl <= 32:
        init = 32
    elif ttl <= 64:
        init = 64
    elif ttl <= 128:
        init = 128
    else:
        init = 255
    hops = init - ttl
    if hops < 0:
        return 0
    else:
        return hops + 1



def compute_metrics_for_node(packets, node_ip):
    req_sent = 0
    req_recv = 0
    rep_sent = 0
    rep_recv = 0
    req_bytes_sent = 0
    req_bytes_recv = 0
    req_data_sent = 0
    req_data_recv = 0
    requests = []
    replies = []
    for p in packets:
        icmp_type = p["icmp_type"]
        src = p["src_ip"]
        dst = p["dst_ip"]
        sent = (src == node_ip)
        received = (dst == node_ip)
        if icmp_type == 8:  
            if sent:
                req_sent += 1
                req_bytes_sent += p["frame_len"]
                req_data_sent += p["icmp_payload_len"]
            if received:
                req_recv += 1
                req_bytes_recv += p["frame_len"]
                req_data_recv += p["icmp_payload_len"]
            requests.append(p)
        elif icmp_type == 0:  
            if sent:
                rep_sent += 1
            if received:
                rep_recv += 1
            replies.append(p)
    sent_req_map = {}   
    for p in requests:
        if p["src_ip"] == node_ip:
            key = (p["src_ip"], p["dst_ip"], p["icmp_id"], p["icmp_seq"])
            sent_req_map[key] = p
    incoming_req_map = {} 
    for p in requests:
        if p["dst_ip"] == node_ip:
            key = (p["src_ip"], p["dst_ip"], p["icmp_id"], p["icmp_seq"])
            incoming_req_map[key] = p
    rtts = []
    total_req_bytes_for_rtt = 0
    total_req_data_for_rtt = 0
    hop_counts = []
    for rep in replies:
        key = (rep["dst_ip"], rep["src_ip"], rep["icmp_id"], rep["icmp_seq"])
        req = sent_req_map.get(key)
        if req is None:
            continue
        rtt = rep["timestamp"] - req["timestamp"]
        if rtt <= 0:
            continue
        rtts.append(rtt)
        total_req_bytes_for_rtt += req["frame_len"]
        total_req_data_for_rtt += req["icmp_payload_len"]
        hop_counts.append(infer_hops_from_ttl(rep["ip_ttl"]))
    if len(rtts) > 0:
        sum_rtt = 0.0
        i = 0
        while i < len(rtts):
            sum_rtt += rtts[i]
            i += 1
        avg_rtt_ms = (sum_rtt / len(rtts)) * 1000.0
        throughput_kBps = (total_req_bytes_for_rtt / 1000.0) / sum_rtt
        goodput_kBps = (total_req_data_for_rtt / 1000.0) / sum_rtt
        if len(hop_counts) > 0:
            sum_hops = 0.0
            i = 0
            while i < len(hop_counts):
                sum_hops += hop_counts[i]
                i += 1
            avg_hops = sum_hops / len(hop_counts)
        else:
            avg_hops = 0.0
    else:
        avg_rtt_ms = 0.0
        throughput_kBps = 0.0
        goodput_kBps = 0.0
        avg_hops = 0.0
    reply_delays = []
    for rep in replies:
        if rep["src_ip"] != node_ip:
            continue
        key = (rep["dst_ip"], rep["src_ip"], rep["icmp_id"], rep["icmp_seq"])
        req_in = incoming_req_map.get(key)
        if req_in is None:
            continue
        delay = rep["timestamp"] - req_in["timestamp"]
        if delay <= 0:
            continue
        reply_delays.append(delay)
    if len(reply_delays) > 0:
        sum_delays = 0.0
        i = 0
        while i < len(reply_delays):
            sum_delays += reply_delays[i]
            i += 1
        avg_reply_delay_us = (sum_delays / len(reply_delays)) * 1_000_000.0
    else:
        avg_reply_delay_us = 0.0
    metrics = {}
    metrics["requests_sent"] = req_sent
    metrics["requests_received"] = req_recv
    metrics["replies_sent"] = rep_sent
    metrics["replies_received"] = rep_recv
    metrics["request_bytes_sent"] = req_bytes_sent
    metrics["request_bytes_received"] = req_bytes_recv
    metrics["request_data_sent"] = req_data_sent
    metrics["request_data_received"] = req_data_recv
    metrics["avg_rtt_ms"] = avg_rtt_ms
    metrics["throughput_kBps"] = throughput_kBps
    metrics["goodput_kBps"] = goodput_kBps
    metrics["avg_reply_delay_us"] = avg_reply_delay_us
    metrics["avg_hops_per_request"] = avg_hops
    return metrics

def compute():
    packets = packet_parser.parse()
    node_ip = "192.168.100.1"
    metrics = compute_metrics_for_node(packets, node_ip)
    print("Echo Requests Sent", metrics["requests_sent"])
    print("Echo Requests Received", metrics["requests_received"])
    print("Echo Replies Sent", metrics["replies_sent"])
    print("Echo Replies Received", metrics["replies_received"])
    print("Echo Request Bytes Sent", metrics["request_bytes_sent"])
    print("Echo Request Bytes Received", metrics["request_bytes_received"])
    print("Echo Request Data Sent", metrics["request_data_sent"])
    print("Echo Request Data Received", metrics["request_data_received"])
    print("Average RTT (ms)", round(metrics["avg_rtt_ms"], 2))
    print("Echo Request Throughput (kB/sec)", round(metrics["throughput_kBps"], 1))
    print("Echo Request Goodput (kB/sec)", round(metrics["goodput_kBps"], 1))
    print("Average Reply Delay (us)", round(metrics["avg_reply_delay_us"], 2))
    print("Average Echo Request Hop Count", round(metrics["avg_hops_per_request"], 2))
