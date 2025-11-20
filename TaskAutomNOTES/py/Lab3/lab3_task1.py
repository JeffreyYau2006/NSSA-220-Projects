#!/usr/bin/python
import sys

def main():
    # python lab3.py iris.txt
    filename = sys.argv[1]

    sepal_length = []
    sepal_width = []
    petal_length = []
    petal_width = []
    iris_setosa_count = 0
    iris_versicolor_count = 0
    iris_virginica_count = 0

    f = open(filename, "r")

    for line in f:
        line = line.strip()
        if line == "":
            continue
        if line.startswith("@"):
            continue
        if line.startswith("%"):
            continue

        data = line.split(",")
       # print(data)
        if len(data) != 5:
            continue

        sl, sw, pl, pw, iris_type = data
        sepal_length.append(float(sl))
        sepal_width.append(float(sw))
        petal_length.append(float(pl))
        petal_width.append(float(pw))

        if iris_type == "Iris-setosa":
            iris_setosa_count += 1
        if iris_type == "Iris-versicolor":
            iris_versicolor_count += 1
        if iris_type == "Iris-virginica":
            iris_virginica_count += 1

    f.close()

    def stats(values):
        return min(values), max(values), sum(values)/len(values)

    sl_min, sl_max, sl_avg = stats(sepal_length)
    sw_min, sw_max, sw_avg = stats(sepal_width)
    pl_min, pl_max, pl_avg = stats(petal_length)
    pw_min, pw_max, pw_avg = stats(petal_width)

    print(f"Sepal Length: min = {sl_min}, max = {sl_max}, average = {sl_avg:.2f}")
    print(f"Sepal Width: min = {sw_min}, max = {sw_max}, average = {sw_avg:.2f}")
    print(f"Petal Length: min = {pl_min}, max = {pl_max}, average = {pl_avg:.2f}")
    print(f"Petal Width: min = {pw_min}, max = {pw_max}, average = {pw_avg:.2f}")

    print("Iris Types: " + "Iris Setosa = " + str(iris_setosa_count) + "Iris Setosa = " + str(iris_setosa_count) + "Iris Versicolor = " + str(iris_versicolor_count) + "Iris Virginica  = " + str(iris_virginica_count))

main()
