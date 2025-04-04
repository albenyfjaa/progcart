import os
from qgis.core import QgsVectorLayer, QgsProject, QgsRasterLayer, QgsWkbTypes

class AddLayer:
    def __init__(self, destination_folder):
        self.destination_folder = destination_folder
        layer = os.path.join(self.destination_folder, "estacoes_sirgas.shp")
        layer_obj = QgsVectorLayer(layer, os.path.basename(layer)[:-4], "ogr") # Creates a QgsVectorLayer object for vector layers
        QgsProject.instance().addMapLayer(layer_obj)
        print("Layer adicionada ao mapa: ", layer)


""" import os
from qgis.core import QgsVectorLayer, QgsProject, QgsRasterLayer, QgsWkbTypes

class AddLayer:
    def __init__(self, destination_folder):
        self.destination_folder = destination_folder
        layer = os.path.join(self.destination_folder, "estacoes_sirgas.shp")
        layer_obj = QgsVectorLayer(layer, os.path.basename(layer)[:-4], "ogr") # Creates a QgsVectorLayer object for vector layers
        QgsProject.instance().addMapLayer(layer_obj)
        print("Layer adicionada ao mapa: ", layer)

AddLayer("C:\\Users\\filip\\progcart\\projeto_2_geopandas\\docs\\files\\download_teste") """