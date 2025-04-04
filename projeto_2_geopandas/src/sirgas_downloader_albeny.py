import os
import gzip
import shutil
import requests
import re
import random
from zipfile import ZipFile
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt
import numpy as np

class Downloader:
    def __init__(self, server_url_format_crd, server_url_format_vel, destination_folder):
        self.server_url_format_crd = server_url_format_crd # Stores the URL in the instance attribute
        self.server_url_format_vel = server_url_format_vel # Stores the URL in the instance attribute
        self.destination_folder = destination_folder # Stores the destination folder in the instance attribute
        # self.file_Path_extraction = None # Initialize the instance attribute as None
        
        if not os.path.exists(self.destination_folder): # Creates a folder if it doesn't exist
            os.makedirs(self.destination_folder)
            print("A seguinte pasta foi criada: ", self.destination_folder)

    # Method download_file 
    def download_file(self):
        file_name_crd = os.path.basename(self.server_url_format_crd) # Get the base name in specified path. Use os.path.split() method to split the specified path into a pair (head, tail)            
        print(file_name_crd)
        # If file_name_crd has invalid characters or is empty
        invalid_chars = r'[<>:"/\\|?*]' # Creates a character class with invalid characters
        if not file_name_crd or re.search(invalid_chars, file_name_crd): # Checks if the file_name_crd is empty or contains invalid characters (re.search looks for any invalid characters)
            file_name_crd = f"download_{random.randint(1, 99999)}.zip"  # Nome padrão com número aleatório

        file_path_crd = os.path.join(self.destination_folder, file_name_crd) # Create the destination path based on the destination folder and the file name

        response = requests.get(self.server_url_format_crd) # Getting the url
        if response.status_code == 200: #If ok, downloads the file
            with open(file_path_crd, 'wb') as file: # When opening files using open(), the WITH statement ensures that the file is closed automatically after operations are completed. 
                file.write(response.content)
                print("Arquivo salvo em: ", file_path_crd)
        else:
            print('Falha ao realizar download')        

        # Download VEL
        file_name_vel = os.path.basename(self.server_url_format_vel) # Get the base name in specified path. Use os.path.split() method to split the specified path into a pair (head, tail)            
        # If file_name_vel has invalid characters or is empty
        invalid_chars = r'[<>:"/\\|?*]' # Creates a character class with invalid characters
        if not file_name_vel or re.search(invalid_chars, file_name_vel): # Checks if the file_name_vel is empty or contains invalid characters (re.search looks for any invalid characters)
            file_name_vel = f"download_{random.randint(1, 99999)}.zip"  # Nome padrão com número aleatório

        file_path_vel = os.path.join(self.destination_folder, file_name_vel) # Create the destination path based on the destination folder and the file name
        print("file_path_vel: ", file_path_vel)

        response = requests.get(self.server_url_format_vel) # Getting the url
        if response.status_code == 200: #If ok, downloads the file
            with open(file_path_vel, 'wb') as file: # When opening files using open(), the WITH statement ensures that the file is closed automatically after operations are completed. 
                file.write(response.content)
                print("Arquivo salvo em: ", file_path_vel)
        else:
            print('Falha ao realizar download')

        # Decompress and creates the CRD Data Frame
        df_crd = pd.read_csv(file_path_crd, compression='gzip', encoding="ANSI", on_bad_lines='skip', skiprows=18, sep="\s+", header=None)
        csv_path_crd = os.path.join(self.destination_folder, "df_crd.csv")


        # Define headers CRD df
        headers = ["NUM", "STATION", "NAME", "X[m]", "sig_X[m]", "Y[m]", "sig_Y[m]", "Z[m]", "sig_Z[m]", "A1", "A2", "START", "END"]
        df_crd.columns = headers
        df_crd['ID-SNX'] = df_crd['A1'].astype(str) + df_crd['A2'].astype(str)
        df_crd = df_crd.drop('A1', axis=1)
        df_crd = df_crd.drop('A2', axis=1)
        # Export CSV CRD
        df_crd.to_csv(csv_path_crd, index=False)
        print("CSV path", csv_path_crd)


        # Decompress and creates the VEL df
        df_vel = pd.read_csv(file_path_vel, compression='gzip', encoding="ANSI", on_bad_lines='skip', skiprows=18, sep="\s+", header=None)
        csv_path_vel = os.path.join(self.destination_folder, "df_vel.csv")


        # Define Headers VEL df
        headers = ["NUM", "STATION", "NAME", "VX[m/a]", "sig_VX[m/a]", "VY[m/a]", "sig_Y[m]", "VZ[m/a]", "sig_VZ[m/a]", "A1", "A2", "START", "END"]
        df_vel.columns = headers
        df_vel['ID-SNX'] = df_vel['A1'].astype(str) + df_vel['A2'].astype(str)
        df_vel = df_vel.drop('A1', axis=1)
        df_vel = df_vel.drop('A2', axis=1)
        # Export CSV VEL
        print("CSV path", csv_path_vel)
        df_vel.to_csv(csv_path_vel, index=False)

        # Join df_crd with df_vel
        df_merge = pd.merge(df_crd, df_vel, how='left', left_index=True, right_index=True)
        df_merge['geometry'] = df_merge.apply(lambda row: Point(row['X[m]'], row['Y[m]']), axis=1)
        csv_path_merge = os.path.join(self.destination_folder, "df_merge.csv")
        df_merge.to_csv(csv_path_merge, index=False)

        # Convert DataFrame to a GeoDataFrame
        gdf_merge = gpd.GeoDataFrame(df_merge, geometry='geometry')
        
        # Save shapefile
        shp_path_merge = os.path.join(self.destination_folder, "estacoes_sirgas.shp")
        gdf_merge.to_file(shp_path_merge, driver="ESRI Shapefile")
        print("Shapefile salvo em: ", shp_path_merge)

""" link_crd = "https://www.sirgas.org/archive/gps/SIRGAS/SIRGAS2022/SIRGAS2022_XYZ.CRD.gz"
link_vel = "https://www.sirgas.org/archive/gps/SIRGAS/SIRGAS2022/SIRGAS2022_XYZ.VEL.gz"
folder = "C:\\Users\\filip\\progcart\\projeto_2_geopandas\\docs\\files\\download_teste"

sirgascon_obj = downloader(link_crd, link_vel, folder)
obj_teste.download_file() """