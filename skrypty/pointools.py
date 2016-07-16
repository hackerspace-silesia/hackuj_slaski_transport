from qgis.core import (QgsFeature, QgsGeometry,
                       QgsVectorLayer, QgsMapLayerRegistry,
                       QgsField)
from PyQt4.QtCore import QVariant
from qgis.utils import iface
 
def createPointsAt(distance, geom):
    length = geom.length()
    currentdistance = distance
    feats = []
 
    while currentdistance < length:
        # Get a point along the line at the current distance
        point = geom.interpolate(currentdistance)
        # Create a new QgsFeature and assign it the new geometry
        fet = QgsFeature()
        fet.setAttributeMap( { 0 : currentdistance } )
        fet.setGeometry(point)
        feats.append(fet)
        # Increase the distance
        currentdistance = currentdistance + distance
 
    return feats
 
def pointsAlongLine(distance):
    # Create a new memory layer and add a distance attribute
    vl = QgsVectorLayer("Point", "distance nodes", "memory")
    pr = vl.dataProvider()
    pr.addAttributes( [ QgsField("distance", QVariant.Int) ] )
    layer = iface.mapCanvas().currentLayer()
    # Loop though all the selected features
    for feature in layer.selectedFeatures():
        geom = feature.geometry()
        features = createPointsAt(distance, geom)
        pr.addFeatures(features)
        vl.updateExtents()
 
    QgsMapLayerRegistry.instance().addMapLayer(vl)