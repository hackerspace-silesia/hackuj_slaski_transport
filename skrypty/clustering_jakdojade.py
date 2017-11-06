#about
import geojson
import csv
from sklearn.cluster import MeanShift, estimate_bandwidth
from numpy import array, unique

#converting jakdojeade data to list
def csvtopoints(filename):
    with open(filename, 'rU') as f:
        reader = csv.reader(f,delimiter=';')
        reader = list(reader)[1:]
        print "dupa"
        points = [[[float(line[3]),float(line[4])],[float(line[1]),float(line[2])]] for line in reader]
        return points

def makeclusters(points):

    points = array(points).reshape(len(points)*2,2)
    bandwidth = estimate_bandwidth(points,n_samples=1000)/16
    cluster = MeanShift(bandwidth=bandwidth)
    cluster.fit(points)
    labels = cluster.labels_
    cluster_centers = cluster.cluster_centers_
    clusters = cluster_centers.tolist()

    lines = []
    for i in range(len(clusters)):
        for j in range(i,len(clusters)):
            lines.append([clusters[i],clusters[j],0,i,j])
    print len(clusters),len(unique(labels)),len(lines)
    print lines

    for i in range(0,len(labels)/2):
        source = labels[2*i]
        dest = labels[2*i+1]
        if source>dest: source, dest = dest, source
        index = source*len(unique(labels)) - sum(range(source+1)) + dest
        # print sum(range(source+1)),source, dest, index
        lines[index][2]+=1

    #saving lines to csv
    data=[]
    centers=[]
    filteredlines=[]
    specified = [71,233,375,186]
    for item in lines:
        if (item[0][1]==item[1][1]) and (item[0][0]==item[1][0]):
            point = "POINT ("+str(item[1][1])+" "+str(item[1][0])+")"
            centers.append([item[2],point])
            print item[2]
        else:
            linestring = "LINESTRING ("+str(item[0][1])+" "+str(item[0][0])+", "+str(item[1][1])+" "+str(item[1][0])+")"
            data.append([item[2],linestring,item[3],item[4]])
            if item[3] in specified or item[4] in specified: filteredlines.append([item[2],linestring,item[3],item[4]])
    print data
    print centers

    with open('lines.csv', 'w') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerows(data)

    with open('filteredlines.csv', 'w') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerows(filteredlines)

    with open('centers.csv', 'w') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerows(centers)

    orgpoints = points.tolist()
    savepoints = []
    for i in range(len(labels)):
        point = "POINT ("+str(orgpoints[i][1])+" "+str(orgpoints[i][0])+")"
        savepoints.append([labels[i],point])

    print savepoints
    with open('points.csv', 'w') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerows(savepoints)

points = csvtopoints('trips-GOP-luty-min-3-pojazdy.csv')
print "dupa"
makeclusters(points)