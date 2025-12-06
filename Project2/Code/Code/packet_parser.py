def parse():
    packets = []
    f = open('Node1.txt', "r")
    line = f.readline()
    while line:
        line = line.strip(" ")
        if "ICMP" in line and "Echo (ping)" in line:
            parts = line.split()
            try:
                timestamp = float(parts[1])
                src_ip = parts[2]
                dst_ip = parts[3]
                frame_len = int(parts[5])
                if "Echo (ping) request" in line:
                    icmp_type = 8
                elif "Echo (ping) reply" in line:
                    icmp_type = 0
                else:
                    line = f.readline()
                    continue
                icmp_id = 0
                icmp_seq = 0
                ip_ttl = 0
                for p in parts:
                    if p.startswith("id="):
                        val = p.split("=", 1)[1].rstrip(",")
                        if val.startswith("0x") or val.startswith("0X"):
                            icmp_id = int(val, 16)
                        else:
                            icmp_id = int(val)
                    elif p.startswith("seq="):
                        val = p.split("=", 1)[1]
                        val = val.split("/", 1)[0].rstrip(",")
                        icmp_seq = int(val)
                    elif p.startswith("ttl="):
                        val = p.split("=", 1)[1].rstrip(",)")
                        ip_ttl = int(val)
                icmp_payload_len = max(0, frame_len - 42)
                pkt = {
                    "timestamp": timestamp,
                    "src_ip": src_ip,
                    "dst_ip": dst_ip,
                    "frame_len": frame_len,
                    "icmp_payload_len": icmp_payload_len,
                    "icmp_type": icmp_type,
                    "icmp_id": icmp_id,
                    "icmp_seq": icmp_seq,
                    "ip_ttl": ip_ttl,
                }
                packets.append(pkt)
            except:
                pass
        line = f.readline()
    f.close()
    return packets
