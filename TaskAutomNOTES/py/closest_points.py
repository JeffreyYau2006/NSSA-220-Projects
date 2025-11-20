import sys
import math

def read_points(filename):
    """Reads a file containing x,y coordinates (floats) and returns a list of (x, y) tuples."""
    f = open(filename, "r")
    points = []
    for line in f:
        line = line.strip()
        if len(line) > 0:
            parts = line.split(',')
            x_str = parts[0]
            y_str = parts[1]
            x = float(x_str)
            y = float(y_str)
            points.append((x, y))
    f.close()
    return points


def euclidean_distance(p1, p2):
    """Calculates the Euclidean distance between two points (x1, y1) and (x2, y2)."""
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def find_closest_points(points1, points2):
    """For each point in points1, find the closest point in points2.
    Returns a list of tuples (index_of_closest, sum_of_x_values)."""
    result = []
    for p1 in points1:
        min_dist = float('inf')
        min_index = -1
        for i, p2 in enumerate(points2):
            dist = euclidean_distance(p1, p2)
            if dist < min_dist:
                min_dist = dist
                min_index = i
                closest_point = p2
        result.append((min_index, p1, closest_point, p1[0] + closest_point[0]))
    return result


def main():
    # Check that exactly two filenames are provided
    if len(sys.argv) != 3:
        print("Usage: python closest_points.py <file1> <file2>")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]

    points1 = read_points(file1)
    points2 = read_points(file2)

    results = find_closest_points(points1, points2)

    # Output results in the required format
    for i, (closest_index, p1, p2, x_sum) in enumerate(results):
        print(f"The smallest distance of point {i} ({p1}) is {closest_index}=({p2[0]}, {p2[1]}). Sum is {x_sum}")


if __name__ == "__main__":
    main()
