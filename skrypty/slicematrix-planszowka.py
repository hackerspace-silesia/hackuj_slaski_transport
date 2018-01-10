import geojson
import csv
# from sklearn.cluster import MeanShift, estimate_bandwidth
from numpy import array, unique
import numpy as np

with open("D:\Git\mapotrans\skrypty\gopdensity.csv", 'rU') as f:
    reader = csv.reader(f, delimiter=';')
    reader = list(reader)[1:]

EN = [int(str(line[1])[4:8]) for line in reader]
N = sorted(unique(EN))
EE = [int(str(line[1])[9:13]) for line in reader]
E = sorted(unique(EE))
CNT = [int(line[0]) for line in reader]

matrix = [[0] * len(E) for item in N]

for i in range(len(reader)):
    ene = EN[i]
    eee = EE[i]
    value = CNT[i]
    nind = N.index(ene)
    eind = E.index(eee)
    matrix[nind][eind] = value

with open('temp.csv', 'wb') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow([0] + E)
    for i in range(len(N)):
        writer.writerow([int(N[i])] + matrix[i])

# treshold = 0.25
Nmin = 3037
Nmax = 3081
Emin = 4923
Emax = 4995

dogeszczanie = 2
# Nmin = 3278
# Nmax = 3307
# Emin = 5059
# Emax = 5088


#converting jakdojeade data to list
with open("temp.csv", 'rU') as f:
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

flatsliced = [item for sublist in sliced for item in sublist]

maxdens = max(maxy)
stepdens = maxdens/7
denssteps = {
    xrange(0, stepdens): '',
    xrange(stepdens, 2*stepdens): '1',
    xrange(2*stepdens, 3*stepdens): '2',
    xrange(3*stepdens, 4*stepdens): '3',
    xrange(4*stepdens, 5*stepdens): '4',
    xrange(5*stepdens, 6*stepdens): '5',
    xrange(6*stepdens, 7*stepdens): '6',
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

#dogeszczanie (na razie razy 2)
# slicedaft2 = []
# for line in slicedaft:
#     temp = []
#     for item in line:
#         temp.append(item)
#         temp.append(item)
#     slicedaft2.append(temp)
#     slicedaft2.append(temp)

with open('mpGOPd.csv', 'wb') as f:
    writer = csv.writer(f, delimiter=';')
    for i in reversed(range(len(slicedaft))):
        writer.writerow(slicedaft[i])