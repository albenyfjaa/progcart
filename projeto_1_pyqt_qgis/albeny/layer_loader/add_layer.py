import os
from qgis.core import QgsVectorLayer, QgsProject, QgsRasterLayer, QgsWkbTypes

class AddLayer:
    def __init__(self, file_Path_extraction):
        
        # Create a list for all the found files
        items = []
        
        # Create lists for different layer types.
        polygon_layers = []
        line_layers = []
        point_layers = []
        raster_layers = []
        
        ext = (".shp", ".tif")

        # Add the all the files found in the foders and subfolders in the items list
        for root, dirs, files in os.walk(file_Path_extraction):
            for file in files:
                if file.endswith(ext):
                    items.append(os.path.join(root, file)) 
                    
        

        for layer in items: # Iterates through the items list
            if layer.endswith(".shp"): # If the file is a shapefile 
                layer_obj = QgsVectorLayer(layer, os.path.basename(layer)[:-4], "ogr") # Creates a QgsVectorLayer object for vector layers
                if layer_obj.isValid(): # Check if the object is valid
                    geom_type = layer_obj.geometryType() # Get the geometry type
                    if geom_type == QgsWkbTypes.PolygonGeometry: # If polygon, add to polygon list
                        polygon_layers.append(layer_obj)
                    elif geom_type == QgsWkbTypes.LineGeometry: # If line, add to line list
                        line_layers.append(layer_obj)
                    elif geom_type == QgsWkbTypes.PointGeometry: # If point, add to point list
                        point_layers.append(layer_obj)
            
            elif layer.endswith(".tif"): # If the file is a raster layer
                layer_obj = QgsRasterLayer(layer, os.path.basename(layer)[:-4], "gdal") # Create q QgsRasterLayer object
                if layer_obj.isValid(): # Check if the object is valid
                    raster_layers.append(layer_obj) # Add to raster list
        
        # Add all valid layers to the QGIS project in the following order: raster > polygon > line > point
        for layer in raster_layers + polygon_layers + line_layers + point_layers:
            QgsProject.instance().addMapLayer(layer)
            print("Layer adicionada ao mapa: ", layer)
