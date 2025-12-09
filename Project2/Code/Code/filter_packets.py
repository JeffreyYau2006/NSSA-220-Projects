def filter(node):
    fInputFile = './../NSSA-220-Projects/Project2/Captures/Captures/' + "Node" + str(node) + ".txt"
    f = open(fInputFile, 'r')

    outputFile = "Node" + str(node) + "_filtered_output.txt"
    out = open(outputFile, 'w')

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
filter(1)