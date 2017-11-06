import geojson
import csv
# from sklearn.cluster import MeanShift, estimate_bandwidth
# from numpy import array, unique

treshold = 0.25
Nmin = 3037
Nmax = 3081
Emin = 4923
Emax = 4995
# Nmin = 3278
# Nmax = 3307
# Emin = 5059
# Emax = 5088


#converting jakdojeade data to list
with open("eggs.csv", 'rU') as f:
        reader = csv.reader(f,delimiter=';')
        reader = list(reader)

E = [int(item) for item in reader[0]]
E = E[1:]

N = []
density = []
for line in reader[1:]:
    N.append(int(line[0]))
    density.append([int(item) for item in line[1:]])
    
iNmin = N.index(Nmin)
iNmax = N.index(Nmax)
iEmin = E.index(Emin)
iEmax = E.index(Emax)

sliced = []
maxy = []

for line in density[iNmin:iNmax]:
    sliced.append(line[iEmin:iEmax])
    maxy.append(max(line))

maxdens = max(maxy)

slicedaft = []
for line in sliced:
    temp = []
    for item in line:
        if item > treshold*maxdens:
            temp.append(1)
        else:
            temp.append('')
    slicedaft.append(temp)

with open('GOP2.csv', 'wb') as f:
    writer = csv.writer(f, delimiter=';')
    for i in reversed(range(len(slicedaft))):
        writer.writerow(slicedaft[i])