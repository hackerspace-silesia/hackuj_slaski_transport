registry = QgsMapLayerRegistry.instance()

line = registry.mapLayersByName('gopcent20km')
polygon = registry.mapLayersByName('GOP_density')

feats_lines = [ feat for feat in line[0].getFeatures() ]
feats_polygons = [ feat for feat in polygon[0].getFeatures() ]

crs = line[0].crs()
epsg = crs.postgisSrid()

uri = "Linestring?crs=epsg:" + str(epsg) + "&field=id:integer""&index=yes"

mem_layer = QgsVectorLayer(uri,
                           'lines',
                           'memory')

polygon[0].startEditing()

for i, feat_line in enumerate(feats_lines):
    for j, feat_polygon in enumerate(feats_polygons):
        if feat_polygon.geometry().intersects(feat_line.geometry()):
            #feat_polygon["kolej"] = 1
            feat_polygon["20km"]=feat_line["id"]
            polygon[0].updateFeature(feat_polygon)
            
polygon[0].commitChanges()

QgsMapLayerRegistry.instance().addMapLayer(mem_layer)