import geojson
import csv
from sklearn.cluster import MeanShift, estimate_bandwidth
from numpy import array, unique

#converting jakdojeade data to list
with open("D:\Git\mapotrans\skrypty\GEOSTAT_grid_POP_1K_2011_V2_0_1.csv", 'rU') as f:
        reader = csv.reader(f,delimiter=',')
        reader = list(reader)[1:]

EN = [int(str(line[1])[4:8]) for line in reader]
N = sorted(unique(EN))
EE = [int(str(line[1])[9:13]) for line in reader]
E = sorted(unique(EE))
CNT = [int(line[0]) for line in reader]

matrix = [[0]*len(E) for item in N]

for i in range(len(reader)):
    ene = EN[i]
    eee = EE[i]
    value = CNT[i]
    nind = N.index(ene)
    eind = E.index(eee)
    matrix[nind][eind] = value


with open('eggs.csv', 'wb') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow([0] + E)
    for i in range(len(N)):
        writer.writerow([int(N[i])] + matrix[i])

