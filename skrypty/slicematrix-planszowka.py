import geojson
import csv
# from sklearn.cluster import MeanShift, estimate_bandwidth
from numpy import array, unique

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
stepdens = maxdens/7
denssteps = {
    xrange(0, stepdens): '',
    xrange(0, 2*stepdens): '1',
    xrange(0, 3*stepdens): '2',
    xrange(0, 4*stepdens): '3',
    xrange(0, 5*stepdens): '4',
    xrange(0, 6*stepdens): '5',
    xrange(0, 7*stepdens): '6',
}

slicedaft = []
for line in sliced:
    temp = []
    for item in line:
        for key in denssteps:
            if item in key:
                temp.append(denssteps[key])
                break
    slicedaft.append(temp)

with open('GOP2.csv', 'wb') as f:
    writer = csv.writer(f, delimiter=';')
    for i in reversed(range(len(slicedaft))):
        writer.writerow(slicedaft[i])