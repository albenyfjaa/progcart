# skiprows: pular linhas do arquivo sirgas baixado e extraido
import os
import gzip
import shutil
import requests
import re
import random
from zipfile import ZipFile
import pandas as pd

class downloader:
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
        # Download CRD
        file_name_crd = os.path.basename(self.server_url_format_crd) # Get the base name in specified path. Use os.path.split() method to split the specified path into a pair (head, tail)            
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
            return
        
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
            return

        # self.file_Path_extraction_crd = os.path.splitext(file_path_crd)[0] # Save extraction path to instance attribute. Splits the path name into a pair root and ext and gets the root.
        # print("file_Path_extraction_crd: ", self.file_Path_extraction_crd)

        # Decompress and creates the CRD Data Frame
        df_crd = pd.read_csv(file_path_crd, compression='gzip', encoding="ANSI", on_bad_lines='skip', skiprows=16)
        print("CRD: ", df_crd)

        df_vel = pd.read_csv(file_path_vel, compression='gzip', encoding="ANSI", on_bad_lines='skip', skiprows=16)
        print("VEL: ", df_crd)
        
        #reset = df_crd.drop(index=df_crd.index[:40])

        #print(reset)



        # Decompress and creates the VEL Data Frame
        #df_vel = pd.read_csv(file_path_vel, compression='gzip', encoding="ANSI", on_bad_lines='skip')
        #print("VEL: ", df_vel)



link_crd = "https://www.sirgas.org/archive/gps/SIRGAS/SIRGAS2022/SIRGAS2022_XYZ.CRD.gz"
link_vel = "https://www.sirgas.org/archive/gps/SIRGAS/SIRGAS2022/SIRGAS2022_XYZ.VEL.gz"
folder = "C:\\Users\\filip\\progcart\\projeto_2_geopandas\\docs\\files\\download_teste"

obj_teste = downloader(link_crd, link_vel, folder)
obj_teste.download_file()

        # Zip chinese characters error
        # with open(file_path_crd, 'rb') as f_in:
        #     with gzip.open(self.file_Path_extraction_crd, 'wb') as f_out:
        #         shutil.copyfileobj(f_in, f_out)

# class sirgas_downloader():
#     def __init__(self):
#         self.multianual_coord_url = ""
#         self.multianual_speed_url = ""


#     def decompress(file_name_crd):
#         out_file_name_crd: file_name_crd.replace()
#         with open('/home/joe/file.txt', 'rb') as f_in:
#             with gzip.open('/home/joe/file.txt.gz', 'wb') as f_out:
#                 shutil.copyfileobj(f_in, f_out)

# Projeto 1

# if __name__ == "__main__":
#     teste_obj.sirgas_downloader()
#     saved_file_name_crd = teste_obj.downloader()
#     pass

# class downloader:
#     def __init__(self, server_url_format, destination_folder):
#         self.server_url_format = server_url_format # Stores the URL in the instance attribute
#         self.destination_folder = destination_folder # Stores the destination folder in the instance attribute
#         self.file_Path_extraction = None # Initialize the instance attribute as None
        
#         if not os.path.exists(self.destination_folder): # Creates a folder if it doesn't exist
#             os.makedirs(self.destination_folder)
#             print("A seguinte pasta foi criada: ", self.destination_folder)

#     # Method download_file 
#     def download_file(self):
#         file_name_crd = os.path.basename(self.server_url_format) # Get the base name in specified path. Use os.path.split() method to split the specified path into a pair (head, tail)    
        
#         # If file_name_crd has invalid characters or is empty
#         invalid_chars = r'[<>:"/\\|?*]' # Creates a character class with invalid characters
#         if not file_name_crd or re.search(invalid_chars, file_name_crd): # Checks if the file_name_crd is empty or contains invalid characters (re.search looks for any invalid characters)
#             file_name_crd = f"download_{random.randint(1, 99999)}.zip"  # Nome padrão com número aleatório

#         file_path = os.path.join(self.destination_folder, file_name_crd) # Create the destination path based on the destination folder and the file name
        
#         response = requests.get(self.server_url_format) # Getting the url
#         if response.status_code == 200: #If ok, downloads the file
#             with open(file_path, 'wb') as file: # When opening files using open(), the WITH statement ensures that the file is closed automatically after operations are completed. 
#                 file.write(response.content)
#                 print("Arquivo salvo em: ", file_path)
#         else:
#             print('Falha ao realizar download')
#             return
        
#         self.file_Path_extraction = os.path.splitext(file_path)[0] # Save extraction path to instance attribute. Splits the path name into a pair root and ext and gets the root.
  