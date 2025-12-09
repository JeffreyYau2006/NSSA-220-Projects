def filter(node):
    fInputFile = './../NSSA-220-Projects/Project2/Captures/Captures/' + "Node" + str(node) + ".txt" 
    f = open(fInputFile, 'r') # open capture file for reading

    outputFile = "Node" + str(node) + "_filtered_output.txt" # creates output file
    out = open(outputFile, 'w') # open outfile file for writing

    line = f.readline() # read first line of the input file


    while line: # process file line by line
        stripped = line.strip() # remove whitespace

        if "ICMP" in stripped: # make sure line contains ICMP traffic
            if "Echo (ping) request" in stripped or "Echo (ping) reply" in stripped:
                out.write(line) # write matching packet line to output
                line = f.readline()
                continue
        line = f.readline() # read next line if there are no matches

    f.close() # close input file
    out.close() # close output file
filter(1) # run filter for Node 1