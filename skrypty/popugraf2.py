import processing
import math
from PyQt4.QtCore import *
from qgis.analysis import QgsGeometryAnalyzer 

def pattern(len,step):
    n = int(len/step)
    patt = []
    for i in range(n):
        patt.append("P "+str(i)+" 1 "+str(i*step))
    with open("D:/rule.txt", "w") as file:
        for item in patt:
            print>>file, item

buffers = [2000, 1000, 500] # in meters
step = 50 # step between buffers

#input line
registry = QgsMapLayerRegistry.instance()
line = registry.mapLayersByName('KSS892')
line = line[0]
#density map
density = registry.mapLayersByName('PD_BREC_2011_OBW')
density = density[0]
#extent of analysis
xmin = (density.extent().xMinimum())
xmax =  (density.extent().xMaximum())
ymin = (density.extent().yMinimum())
ymax = (density.extent().yMaximum())
extent = str(xmin)+ ',' + str(xmax)+ ',' +str(ymin)+ ',' +str(ymax)
#making intermadiate points bys tep in which buffer will be calculated
expression = QgsExpression("$length")
totlen=0
for feature in line.getFeatures():
    value = expression.evaluate(feature)
    totlen = totlen+int(value)
pattern(totlen,step)
interpoints = processing.runalg("grass:v.segment", line, "D:/rule.txt",extent,-1,0,1, None)
interpoints = processing.getObject(interpoints['output'])

#make buffers around intemediate points
totalpop = []
for buffer in buffers:
    bufor = processing.runalg("qgis:fixeddistancebuffer", interpoints, buffer, 99, False, None)
    bufor = processing.getObject(bufor['OUTPUT'])
    rbufor = processing.runalg('qgis:intersection', bufor, density, False, None)
    rbufor = processing.getObject(rbufor['OUTPUT'])
#    QgsMapLayerRegistry.instance().addMapLayer(rbufor)
    
    #making output - paraller and segment line
    popugraf = processing.runalg("grass7:v.parallel", line, buffer, buffer, 0, 2, 1,False,True, extent,-1,0,2,None)
    popugraf = processing.getObject(popugraf['output'])
    popugraf = processing.runalg("grass:v.split.length", popugraf, step, extent,-1,0,2,None)
    popugraf = processing.getObject(popugraf['output'])
    popugraf.dataProvider().addAttributes([QgsField('popu', QVariant.Int)])
    popugraf.updateFields()
#    QgsMapLayerRegistry.instance().addMapLayer(popugraf)
       
    #counting population in segments (cat is buffer number indictor after intersection)
    n = int(totlen/step)
    popu = n*[0]
    for feature in rbufor.getFeatures():
        areaa = feature.geometry().area()
        diva = feature["TOTAL_POP"]*areaa/feature["area"] #for BREC 
        cat = feature["cat"]
        popu[cat]=popu[cat]+int(diva)
        
    #assigning popu values to segments
    totalparts = popugraf.featureCount() 
    side = (totalparts - 2*n)/2
    offset = (side - buffer/step)/2
    squish = math.ceil(4.00*buffer/step)
    print offset
    popugraf.startEditing()
    for i, feature in enumerate(popugraf.getFeatures()):
        if i>offset-1 and i<offset+n: 
            feature["popu"] = popu[n-1-i+offset]
        if i>offset+n+side-1 and i<offset+2*n+side: 
            feature["popu"] = popu[i-offset-n -side]
        popugraf.updateFeature(feature)
    popugraf.commitChanges()
    
    QgsMapLayerRegistry.instance().addMapLayer(popugraf)
    
    #counting whole population in buffer
    bufor = processing.runalg("qgis:fixeddistancebuffer", line, buffer, 99, False, None)
    bufor = processing.getObject(bufor['OUTPUT'])
    rbufor = processing.runalg('qgis:intersection', bufor, density, False, None)
    rbufor = processing.getObject(rbufor['OUTPUT'])
    
    totpop = 0
    for feature in rbufor.getFeatures():
        totpop = feature["TOTAL_POP"] + totpop
        
    totalpop.append(totpop)
    
print totalpop