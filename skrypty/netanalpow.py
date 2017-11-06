from qgis.utils import iface
from qgis.analysis import QgsGeometryAnalyzer 
from qgis.networkanalysis import *
import os
import os.path
import processing
import time
from PyQt4.QtCore import QVariant

path = os.path.dirname(QgsProject.instance().fileName())+"/warstwy/"
graf = QgsVectorLayer(path+"powiaty_graf.shp", "graf", "ogr")
QgsMapLayerRegistry.instance().addMapLayer(graf)

director = QgsLineVectorLayerDirector(graf, -1, '', '', '', 3)
properter = QgsDistanceArcProperter()
director.addProperter(properter)

builder = QgsGraphBuilder(QgsCoordinateReferenceSystem(2177, QgsCoordinateReferenceSystem.EpsgCrsId))
graph = builder.graph()

#defining area for GrassGIS
ext = graf.extent()
a = str(ext.xMinimum())
b = str(ext.xMaximum())
c = str(ext.yMinimum())
d = str(ext.yMaximum())


QgsMapLayerRegistry.instance().removeMapLayer( graf.id() )