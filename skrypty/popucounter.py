from qgis.utils import iface
from qgis.analysis import QgsGeometryAnalyzer 
import os
import os.path
import processing
import time
from PyQt4.QtCore import QVariant

		
#INPUT PARAMETERS START
#path to input, temporary and output layers
path = os.path.dirname(QgsProject.instance().fileName())+"/warstwy/"  
#input layers 
#density = path+"GOP_gestosc_zaludnienia.shp"
density = path+"PD_BREC_2012_OBW.shp"
line = path+"LK142.shp"
#bufsize and scale
bufsize = 1000 #in meters
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

#makes buffer from points and intersect this buffer with density layer
QgsGeometryAnalyzer().buffer(linia, path+"bufor.shp", bufsize, False, False, -1)
bufor = QgsVectorLayer(path+"bufor.shp", 
"bufor", "ogr")
QgsMapLayerRegistry.instance().addMapLayer(bufor)
processing.runalg("qgis:intersection", bufor,gestosc,path+"przeciecie.shp")

#add przeciecie layer to registry
przeciecie = QgsVectorLayer(path+"przeciecie.shp", "przeciecie", "ogr")
QgsMapLayerRegistry.instance().addMapLayer(przeciecie)

#calculating population ic each of buffers based on area procentage in each density map district
expression = QgsExpression("$area")
popu = []
for feature in przeciecie.getFeatures():
    value = expression.evaluate(feature)
    #diva = feature.attributes()[2]*value/1000000 #for 1km grid ;crucial point - needs to be determine
    diva = feature.attributes()[11]*value/feature.attributes()[10] #for BREC 
    popu.append(diva)

print sum(popu)
#deleting temp layers
QgsMapLayerRegistry.instance().removeMapLayer( przeciecie.id() )
QgsMapLayerRegistry.instance().removeMapLayer( bufor.id() )
