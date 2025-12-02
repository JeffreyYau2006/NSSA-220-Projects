class ICMPPacket:
    def __init__(self, timestamp, src_ip, dst_ip,
                 frame_len, icmp_payload_len,
                 icmp_type, icmp_id, icmp_seq, ip_ttl):
        self.timestamp = timestamp
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.frame_len = frame_len
        self.icmp_payload_len = icmp_payload_len
        self.icmp_type = icmp_type   
        self.icmp_id = icmp_id
        self.icmp_seq = icmp_seq
        self.ip_ttl = ip_ttl


def parse_filtered_file(path):
    packets = []
    with open(path, "r") as f:
        block = []
        for line in f:
            if line.startswith("No."):
                if block:
                    pkt = _parse_packet_block(block)
                    if pkt is not None:
                        packets.append(pkt)
                    block = []
            block.append(line)

        if block:
            pkt = _parse_packet_block(block)
            if pkt is not None:
                packets.append(pkt)
    return packets


def _parse_packet_block(block):
    summary = None
    for line in block:
        if "ICMP" in line and "Echo (ping)" in line:
            summary = line
            break
    if summary is None:
        return None
    parts = summary.split()
    try:
        timestamp = float(parts[1])
        src_ip = parts[2]
        dst_ip = parts[3]
        frame_len = int(parts[5])
        if "request" in summary:
            icmp_type = 8
        else:
            icmp_type = 0
        icmp_id = 0
        icmp_seq = 0
        ip_ttl = 0
        for p in parts:
            if p.startswith("id="):
                val = p.split("=", 1)[1].rstrip(",")
                if val.startswith("0x"):
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

        return ICMPPacket(
            timestamp,
            src_ip,
            dst_ip,
            frame_len,
            icmp_payload_len,
            icmp_type,
            icmp_id,
            icmp_seq,
            ip_ttl
        )

    except:
        return None
