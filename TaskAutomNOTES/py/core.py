def read_points(filename):
    """Reads a file containing x,y coordinates (floats) and returns a list of (x, y) tuples."""
    f = open(filename, "r")
    points = []
    for i in f:
        line = i.strip()
        print(line)
        print(i)
    f.close()

read_points("iris.txt")