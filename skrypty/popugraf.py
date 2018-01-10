from qgis.utils import iface
from qgis.analysis import QgsGeometryAnalyzer 
import os
import os.path
import processing
import time
from PyQt4.QtCore import QVariant

#creating pattern for line to points
def pattern(len,step):
    n = int(len/step)
    patt = []
    for i in range(n):
        patt.append("P "+str(i)+" 1 "+str(i*step))
    with open(path+"rule.txt", "w") as file:
        for item in patt:
            print>>file, item

#creating pattern for line to points with offset
def segments(distance,step):
    n = len(distance)
    patt = []
    for i in range(n-1):
        patt.append("P "+str(i)+" 1 "+str(i*step)+" "+str(distance[i]))
    for i in reversed(range(n-1)):
        patt.append("P "+str(i)+" 1 "+str(i*step)+" -"+str(distance[i]))
#        patt.append("L "+str(i)+" 1 "+str(i*step)+" "+str((i+1)*step)+" "+str(distance[i]))
#        patt.append("L "+str(i)+" 1 "+str(i*step)+" "+str((i+1)*step)+" -"+str(distance[i]))
    with open(path+"path.txt", "w") as file:
        for item in patt:
            print>>file, item    

			
#INPUT PARAMETERS START
#path to input, temporary and output layers
path = os.path.dirname(QgsProject.instance().fileName())+"/warstwy/"  
#input layers 
#density = path+"GOP_gestosc_zaludnienia.shp"
density = path+"PD_BREC_2012_OBW.shp"
line = path+"KSS8.shp"
outputf = path+"dup"
outputfile = outputf+".shp"
#bufsize and scale
bufsize = 500 #in meters
span = 1500 #max value on popugraf
scale = 20000 #peoples per span m (needed for offset visualization)
step = 100 #segments size in meters
#INPUT PARAMETERS STOP

#deleting old temp layers
if os.path.isfile(path+"bufor.shp"): os.remove(path+"bufor.shp")
if os.path.isfile(path+"bufor.dbf"): os.remove(path+"bufor.dbf")
if os.path.isfile(path+"bufor.shx"): os.remove(path+"bufor.shx")
if os.path.isfile(path+"bufor.prj"): os.remove(path+"bufor.prj")
if os.path.isfile(path+"bufor.cpg"): os.remove(path+"bufor.cpg")
if os.path.isfile(path+"bufor.qpj"): os.remove(path+"bufor.qpj")

if os.path.isfile(path+"przeciecie.shp"): os.remove(path+"przeciecie.shp")
if os.path.isfile(path+"przeciecie.dbf"): os.remove(path+"przeciecie.dbf")
if os.path.isfile(path+"przeciecie.shx"): os.remove(path+"przeciecie.shx")
if os.path.isfile(path+"przeciecie.prj"): os.remove(path+"przeciecie.prj")
if os.path.isfile(path+"przeciecie.cpg"): os.remove(path+"przeciecie.cpg")
if os.path.isfile(path+"przeciecie.qpj"): os.remove(path+"przeciecie.qpj")

if os.path.isfile(path+"punkty.shp"): os.remove(path+"punkty.shp")
if os.path.isfile(path+"punkty.dbf"): os.remove(path+"punkty.dbf")
if os.path.isfile(path+"punkty.shx"): os.remove(path+"punkty.shx")
if os.path.isfile(path+"punkty.prj"): os.remove(path+"punkty.prj")
if os.path.isfile(path+"punkty.cpg"): os.remove(path+"punkty.cpg")
if os.path.isfile(path+"punkty.qpj"): os.remove(path+"punkty.qpj")

#input - density layer and communication line
gestosc = QgsVectorLayer(density, 
"gestosc", "ogr")
linia = QgsVectorLayer(line, 
"linia", "ogr")
#QgsMapLayerRegistry.instance().addMapLayer(gestosc)

#defining area for GrassGIS
ext = gestosc.extent()
a = str(ext.xMinimum())
b = str(ext.xMaximum())
c = str(ext.yMinimum())
d = str(ext.yMaximum())

#line to points - pattern and apply
#counting total lenght of line
#then create pattern and apply grass algorithm
expression = QgsExpression("$length")
totlen=0
for feature in linia.getFeatures():
    value = expression.evaluate(feature)
    totlen = totlen+int(value)
pattern(totlen,step)
size = a + ',' + b + ',' + c + ',' + d
processing.runalg("grass:v.segment", linia, path+"rule.txt",
size,-1,0,1,path+"punkty.shp")

#add points layer to registry
punkty = QgsVectorLayer(path+"punkty.shp", 
"punkty", "ogr")
QgsMapLayerRegistry.instance().addMapLayer(punkty)

#makes buffer from points and intersect this buffer with density layer
QgsGeometryAnalyzer().buffer(punkty, path+"bufor.shp", bufsize, False, False, -1)
bufor = QgsVectorLayer(path+"bufor.shp", 
"bufor", "ogr")
QgsMapLayerRegistry.instance().addMapLayer(bufor)
processing.runalg("qgis:intersection", bufor,gestosc,path+"przeciecie.shp")

#add przeciecie layer to registry
przeciecie = QgsVectorLayer(path+"przeciecie.shp", "przeciecie", "ogr")
QgsMapLayerRegistry.instance().addMapLayer(przeciecie)

#calculating population ic each of buffers based on area procentage in each density map district
expression = QgsExpression("$area")
n = int(totlen/step)
offset = n*[0]
for feature in przeciecie.getFeatures():
    value = expression.evaluate(feature)
    #diva = feature.attributes()[2]*value/1000000 #for 1km grid ;crucial point - needs to be determine
    diva = feature.attributes()[11]*value/feature.attributes()[10] #for BREC 
    cat = feature.attributes()[0]
    offset[cat]=offset[cat]+int(diva)
    
#normalizing poulation offset for line acording to scale
offset = [span*item/scale for item in offset]

#making line offset according to population offset
segments(offset,step)
processing.runalg("grass:v.segment", linia, path+"path.txt",
size,-1,0,1,outputfile)

#add przeciecie layer to registry
final = QgsVectorLayer(outputfile, "final", "ogr")
QgsMapLayerRegistry.instance().addMapLayer(final)

#deleting temp layers
QgsMapLayerRegistry.instance().removeMapLayer( punkty.id() )
QgsMapLayerRegistry.instance().removeMapLayer( przeciecie.id() )
QgsMapLayerRegistry.instance().removeMapLayer( bufor.id() )
QgsMapLayerRegistry.instance().removeMapLayer( final.id() )
