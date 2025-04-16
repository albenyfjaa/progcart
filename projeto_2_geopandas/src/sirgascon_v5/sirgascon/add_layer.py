import os
from qgis.core import QgsVectorLayer, QgsProject, QgsRasterLayer, QgsWkbTypes, QgsCoordinateReferenceSystem
import processing
from PyQt5.QtWidgets import QMessageBox

class AddLayer:
    def __init__(self, destination_folder, layer_extent):
        self.layer_extent = layer_extent
        self.destination_folder = destination_folder
        
        # Add Sirgas Stations Layer
        layer = os.path.join(self.destination_folder, "estacoes_sirgas.shp")
        layer_obj = QgsVectorLayer(layer, os.path.basename(layer)[:-4], "ogr") # Creates a QgsVectorLayer object for vector layers

        
        # If NO polygon is provided, add the original layer
        if not self.layer_extent:
            QgsProject.instance().addMapLayer(layer_obj)
            QMessageBox.information(None, "Layer carregada", "Camada com todas as estações adicionada ao mapa.")
            return  

        # Add Layer Extent
        if self.layer_extent:
            layer_extent_obj = QgsVectorLayer(self.layer_extent, os.path.basename(self.layer_extent)[:-4], "ogr")
            if layer_extent_obj.isValid():
                geometry_type = QgsWkbTypes.geometryType(layer_extent_obj.wkbType())
                if geometry_type == QgsWkbTypes.PolygonGeometry:
                    QgsProject.instance().addMapLayer(layer_extent_obj)
                    print("Layer de extensão adicionada ao mapa:", self.layer_extent)

                    # Perform clip operation
                    clipped_output = os.path.join(self.destination_folder, "estacoes_sirgas_clip.shp")
                    processing.run("native:clip", {
                        'INPUT': layer_obj,
                        'OVERLAY': layer_extent_obj,
                        'OUTPUT': clipped_output
                    })

                    clipped_layer = QgsVectorLayer(clipped_output, "estacoes_sirgas_clip", "ogr")
                   
                  
                    # Messagebox added to inform the user
                    if clipped_layer.isValid():
                        QgsProject.instance().addMapLayer(clipped_layer)
                        QMessageBox.information(None, "Clip realizado", f"Layer clipado adicionado ao mapa:\n{clipped_output}")
                    else:
                        QMessageBox.warning(None, "Erro ao carregar", "Falha ao carregar camada clipada.")

                else:
                    QMessageBox.warning(None, "Geometria inválida", "Camada de extensão ignorada: não é do tipo polígono.")

            else:
                QMessageBox.critical(None, "Erro ao carregar", f"Falha ao carregar camada de extensão:\n{self.layer_extent}")

        else:
            QMessageBox.information(None, "Nenhum polígono", "Nenhuma camada de extensão foi fornecida.")
