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

class downloader:
    def __init__(self, server_url_format_crd, server_url_format_vel, destination_folder, start_date, end_date):
        self.server_url_format_crd = server_url_format_crd # Stores the URL in the instance attribute
        self.server_url_format_vel = server_url_format_vel # Stores the URL in the instance attribute
        self.destination_folder = destination_folder # Stores the destination folder in the instance attribute
        self.start_date = start_date # Stores the start data in the instance attribute
        self.end_date = end_date # Stores the end data in the instance attribute
        # self.file_Path_extraction = None # Initialize the instance attribute as None
        
        if not os.path.exists(self.destination_folder): # Creates a folder if it doesn't exist
            os.makedirs(self.destination_folder)
            print("A seguinte pasta foi criada: ", self.destination_folder)

                
    def download_file(self):
        # === DOWNLOAD CRD ===
        file_name_crd = os.path.basename(self.server_url_format_crd)
        if not file_name_crd or re.search(r'[<>:"/\\|?*]', file_name_crd):
            file_name_crd = f"download_{random.randint(1, 99999)}.gz"
        file_path_crd = os.path.join(self.destination_folder, file_name_crd)
        response = requests.get(self.server_url_format_crd)
        if response.status_code == 200:
            with open(file_path_crd, 'wb') as file:
                file.write(response.content)
        else:
            print("Falha ao baixar CRD")

        # === DOWNLOAD VEL ===
        file_name_vel = os.path.basename(self.server_url_format_vel)
        if not file_name_vel or re.search(r'[<>:"/\\|?*]', file_name_vel):
            file_name_vel = f"download_{random.randint(1, 99999)}.gz"
        file_path_vel = os.path.join(self.destination_folder, file_name_vel)
        response = requests.get(self.server_url_format_vel)
        if response.status_code == 200:
            with open(file_path_vel, 'wb') as file:
                file.write(response.content)
        else:
            print("Falha ao baixar VEL")

        # === LEITURA CRD ===
        df_crd = pd.read_csv(
            file_path_crd,
            compression='gzip',
            encoding="ANSI",
            on_bad_lines='skip',
            skiprows=18,
            sep=r"\s+",
            header=None
        )

        df_crd.columns = ["NUM", "STATION", "NAME", "X[m]", "sig_X[m]", "Y[m]", "sig_Y[m]",
                        "Z[m]", "sig_Z[m]", "A1", "A2", "START", "END"]
        df_crd['ID-SNX'] = df_crd['STATION']
        df_crd = df_crd.drop(['A1', 'A2'], axis=1)

        # Convert dates and rename
        df_crd['START'] = pd.to_datetime(df_crd['START'], errors='coerce')
        df_crd['END'] = pd.to_datetime(df_crd['END'], errors='coerce')
        df_crd.rename(columns={'START': 'START_crd', 'END': 'END_crd'}, inplace=True)

        # Save CSV
        csv_path_crd = os.path.join(self.destination_folder, "df_crd.csv")
        df_crd.to_csv(csv_path_crd, index=False)

        # === LEITURA VEL ===
        df_vel = pd.read_csv(
            file_path_vel,
            compression='gzip',
            encoding="ANSI",
            on_bad_lines='skip',
            skiprows=18,
            sep=r"\s+",
            header=None
        )

        df_vel.columns = ["NUM", "STATION", "NAME", "VX[m/a]", "sig_VX[m/a]", "VY[m/a]", "sig_Y[m]",
                        "VZ[m/a]", "sig_VZ[m/a]", "A1", "A2", "START", "END"]
        df_vel['ID-SNX'] = df_vel['STATION']
        df_vel = df_vel.drop(['A1', 'A2'], axis=1)

        # Convert dates and rename
        df_vel['START'] = pd.to_datetime(df_vel['START'], errors='coerce')
        df_vel['END'] = pd.to_datetime(df_vel['END'], errors='coerce')
        df_vel.rename(columns={'START': 'START_vel', 'END': 'END_vel'}, inplace=True)

        # Save CSV
        csv_path_vel = os.path.join(self.destination_folder, "df_vel.csv")
        df_vel.to_csv(csv_path_vel, index=False)

        # === MERGE === 
        # Rename NUM 
        df_crd = df_crd.rename(columns={"NUM": "NUM_crd"})
        df_vel = df_vel.rename(columns={"NUM": "NUM_vel"})
        # Merge based on NUM
        df_merge = pd.merge(
            df_crd,
            df_vel,
            how='inner',
            left_on='NUM_crd',
            right_on='NUM_vel',
            suffixes=('_c', '_v')
        )

        # === DATE FILTER: only intersecting periods ===
        start = pd.to_datetime(self.start_date)
        end = pd.to_datetime(self.end_date)

        df_merge = df_merge[
            (df_merge['START_vel'] >= start) & 
            (df_merge['END_vel'] <= end)
        ]


        # === 3D GEOMETRY ===
        df_merge['geometry'] = df_merge.apply(
            lambda row: Point(row['X[m]'], row['Y[m]'], row['Z[m]']), axis=1
        )

        # === SAVE MERGE ===
        csv_path_merge = os.path.join(self.destination_folder, "df_merge.csv")
        df_merge.to_csv(csv_path_merge, index=False)

        # === Convert datetime to string (shapefile does not accept datetime) ===
        for col in df_merge.columns:
            if pd.api.types.is_datetime64_any_dtype(df_merge[col]):
                df_merge[col] = df_merge[col].dt.strftime('%Y-%m-%d')

        # === GENERATE SHAPEFILE ===
        df_merge = df_merge.drop(columns=['START_crd', 'END_crd'])
        gdf_merge = gpd.GeoDataFrame(df_merge, geometry='geometry', crs=9378)
        gdf_2d = gdf_merge.to_crs("EPSG:4674")
        gdf_2d.columns = [col[:10] for col in gdf_2d.columns]
        shp_path_merge = os.path.join(self.destination_folder, "estacoes_sirgas.shp")
        gdf_2d.to_file(shp_path_merge, driver="ESRI Shapefile")
