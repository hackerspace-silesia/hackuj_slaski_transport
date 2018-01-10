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
CNT = [str(line[2]) for line in reader] #numer kolumny z atrybutem

matrix = [[''] * len(E) for item in N]

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
with open("temp.csv", 'rU') as f:
        reader = csv.reader(f,delimiter=';')
        reader = list(reader)

E = [int(item) for item in reader[0]]
E = E[1:]

N = []
density = []
for line in reader[1:]:
    N.append(int(line[0]))
    density.append([str(item) for item in line[1:]])

iNmin = N.index(Nmin)
iNmax = N.index(Nmax)
iEmin = E.index(Emin)
iEmax = E.index(Emax)

sliced = []
for line in density[iNmin:iNmax]:
    sliced.append(line[iEmin:iEmax])

slicedaft = []
for line in sliced:
    temp = []
    for item in line:
        temp.append(item)
    slicedaft.append(temp)

#dogeszczanie (na razie razy 2)
slicedaft2 = []
# for line in slicedaft:
#     temp = []
#     for item in line:
#         temp.append(item)
#         temp.append(item)
#     slicedaft2.append(temp)
#     slicedaft2.append(temp)

with open('mpGOPk.csv', 'wb') as f:
    writer = csv.writer(f, delimiter=';')
    for i in reversed(range(len(slicedaft))):
        writer.writerow(slicedaft[i])