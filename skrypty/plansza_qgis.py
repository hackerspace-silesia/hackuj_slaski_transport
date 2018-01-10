import processing

registry = QgsMapLayerRegistry.instance()

siatka = registry.mapLayersByName('wrocsiatka')
polygon = registry.mapLayersByName('wroilo')
referencja = registry.mapLayersByName('wroobw')

feats_siatka = [ feat for feat in siatka[0].getFeatures() ]
feats_polygons = [ feat for feat in polygon[0].getFeatures() ]
feats_referencja = [ feat for feat in referencja[0].getFeatures() ]

#polygon[0].startEditing()
#for i, feat_referencja in enumerate(feats_referencja):
#    expr = QgsExpression('"OBWOD"=%s' % feat_referencja["OBWOD"])
#    dupa = polygon[0].getFeatures( QgsFeatureRequest( expr ) )
#    for feat in dupa:
#        feat["popu"]=feat_referencja["TOTAL_POP"]*feat["area"]/feat_referencja["area"]
#        polygon[0].updateFeature(feat)
#polygon[0].commitChanges()

siatka[0].startEditing()
for i, feat_siatkaa in enumerate(feats_siatka):
    expr = QgsExpression('"id"=%d' % feat_siatkaa["id"])
    dupa = polygon[0].getFeatures( QgsFeatureRequest( expr ) )
    pop = [feat["TOTAL_POP"]for feat in dupa]
    popu = sum(pop)
    feat_siatkaa["pop"] = popu
    siatka[0].updateFeature(feat_siatkaa)
siatka[0].commitChanges()
    
#    for j, feat_polygon in enumerate(feats_polygons):
#        if feat_polygon.geometry().intersects(feat_siatkaa.geometry()):
#            #feat_polygon["kolej"] = 1
#            polygon_area = QgsExpression("$area").evaluate(feat_polygon)
#            print siatka_area, polygon_area
#            feat_polygon["20km"]=feat_line["id"]
#            polygon[0].updateFeature(feat_polygon)
            
#