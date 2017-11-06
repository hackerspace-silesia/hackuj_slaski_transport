import csv

with open('count_matrix.txt', 'r') as f:
    count = f.readlines()

count = [x.split() for x in count]

with open('wspolrzedne.txt', 'r') as f:
    coors = f.readlines()

coors = [x.split() for x in coors]


lines = []
for i in range(0,len(coors)):
    for j in range(i,len(coors)):
        if int(count[i][j])!=0:
            line = "LINESTRING ("+coors[i][1]+" "+coors[i][0]+", "+coors[j][1]+" "+coors[j][0]+")"
            lines.append([count[i][j],line])

with open('KZKgraf.csv', 'w') as fp:
    a = csv.writer(fp, delimiter=',')
    a.writerows(lines)