import processing
import math
import numpy as np
from PyQt4.QtCore import *

#treshold (percent of maximum population) defining urban area
treshold = 0.25

#input layer - extent of analysis
registry = QgsMapLayerRegistry.instance()
obwod = registry.mapLayersByName('SwionyCH')
obwod = obwod[0]
xmin = (obwod.extent().xMinimum())
xmax =  (obwod.extent().xMaximum())
X = xmax - xmin
ymin = (obwod.extent().yMinimum())
ymax = (obwod.extent().yMaximum())
Y = ymax - ymin
extent = str(xmin)+ ',' + str(xmax)+ ',' +str(ymin)+ ',' +str(ymax)

#reference grid, data from GUS
referencja = registry.mapLayersByName('PD_BREC_2011_OBW')
data = processing.runalg('qgis:intersection', obwod, referencja[0], False, None)
data = processing.getObject(data['OUTPUT'])
feats_data = [ feat for feat in data.getFeatures() ]

#gridsizes matrix
gridsizes = [1000]
boxcount = []
fullcount  = []
                
for gridsize in gridsizes:
    grid = processing.runalg('qgis:vectorgrid', extent, gridsize, gridsize, 0, None)
    grid = processing.getObject(grid['OUTPUT'])
    grid.dataProvider().addAttributes([QgsField('popu', QVariant.Int)])
    grid.dataProvider().addAttributes([QgsField('popuind', QVariant.Int)])
    grid.dataProvider().addAttributes([QgsField('popudiv', QVariant.Int)])
    grid.updateFields()
    feats_grid = [ feat for feat in grid.getFeatures() ]
    #making reference and grid intersection
    rgrid = processing.runalg('qgis:intersection', grid, data, True, None)
    rgrid = processing.getObject(rgrid['OUTPUT'])
    rgrid.dataProvider().addAttributes([QgsField('popu', QVariant.Int)])
    rgrid.updateFields()
    feats_rgrid = [ feat for feat in rgrid.getFeatures() ]
    #fillin grid with data - part 1, caluclating small pieces
    rgrid.startEditing()
    for i, feat_data in enumerate(feats_data):
        expr = QgsExpression('"OBWOD"=%s' % feat_data["OBWOD"])
        dupa = rgrid.getFeatures( QgsFeatureRequest( expr ) )
        for feat in dupa:
            areaa = feat.geometry().area()
            areab = feat_data.geometry().area()
            feat["popu"]=feat_data["TOTAL_POP"]*areaa/areab
            rgrid.updateFeature(feat)
    rgrid.commitChanges()
    #fillin frid with data - part 2, summing all mall pieces into one grid cell
    #creating array from grid
    Xr = math.ceil(X/gridsize)
    Yr = math.ceil(Y/gridsize)
    gridarray = [[0 for i in xrange(Xr)] for j in xrange(Yr)]
    grid.startEditing()
    for i, feat_grid in enumerate(feats_grid):
        expr = QgsExpression('"id"=%d' % feat_grid["id"])
        dupa = rgrid.getFeatures( QgsFeatureRequest( expr ) )
#        for feat in dupa:
#            if feat["popu"] == NULL: feat["popu"] = 0
        popu = [feat["popu"] for feat in dupa]
        popu = sum(popu)
        feat_grid["popu"] = popu
        gridarray[i/Xr][i%Xr] = popu
        grid.updateFeature(feat_grid)
    #counting divergence (optional)
#    A = np.array(gridarray)
#    GA = np.gradient(A)
#    GD = np.sum(GA,axis=0)
#    griddiv = GD.tolist()
    #quantization and summing boxes - making indexes from population
    maximum = grid.maximumValue(grid.fieldNameIndex('popu'))
    factor = treshold * maximum
    boxcounter = 0
    for i, feat_grid in enumerate(feats_grid):
        expr = QgsExpression("floor(popu/%d)" % factor)
        value = expr.evaluate(feat_grid, grid.pendingFields())
        if value > 0:
            feat_grid["popuind"] = 1
            boxcounter = boxcounter +1
        else:
            feat_grid["popuind"] = 0
#        feat_grid["popudiv"] = griddiv[i/X][i%X]
        grid.updateFeature(feat_grid)
    grid.commitChanges()
    boxcount.append(boxcounter)
    fullcount.append(int(grid.featureCount()))
    
    QgsMapLayerRegistry.instance().addMapLayer(grid)


#making gradient

scalingfactor = [gridsizes[0]/item for item in gridsizes]

print scalingfactor
print boxcount
print fullcount
    