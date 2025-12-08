def filter():
    f = open('./NSSA-220-Projects/Project2/Captures/Captures/Node1.txt', 'r')
    out = open('./filtered_output.txt', 'w')

    line = f.readline()


    while line:
        stripped = line.strip()

        if "ICMP" in stripped:
            if "Echo (ping) request" in stripped or "Echo (ping) reply" in stripped:
                out.write(line)
                line = f.readline()
                continue
        line = f.readline()

    f.close()
    out.close()
filter()