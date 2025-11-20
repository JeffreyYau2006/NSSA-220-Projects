lst = [ [5.1, 3.5, 1.4, 0.2, 'Iris-setosa'], [7.0, 3.2] ]
strSplit=''
lst1 = []
# reading
f = open('iris.txt', 'r')

# first line
line = f.readline().strip(" ")

# keep reading till no more lines
for i in line:
    print(line)
    strSplit = strSplit + line
    lst1.append(strSplit.split())
    # read next line
    line = f.readline().strip(" ")


f.close

print(lst1)
a = open('new_iris.txt', 'w')

count1=0

for i in lst1:

    for j in lst1[count1]:
        if type(j) == str:
            floatedJ = float(j)*2
            line = str(floatedJ) + ","
            a.write(line)
        else:
            line = str(j) + ","
            a.write(line)
    count1=count1+1
a.close