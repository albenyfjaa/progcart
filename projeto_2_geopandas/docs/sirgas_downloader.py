# skiprows: pular linhas do arquivo sirgas baixado e extraido

import gzip
import shutil


class sirgas_downloader():
    def __init__(self):
        self.multianual_coord_url = ""
        self.multianual_speed_url = ""


    def decompress(file_name):
        out_file_name: file_name.replace()
        with open('/home/joe/file.txt', 'rb') as f_in:
            with gzip.open('/home/joe/file.txt.gz', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)


class downloader:
    def __init__(self, server_url_format, destination_folder):
        self.server_url_format = server_url_format # Stores the URL in the instance attribute
        self.destination_folder = destination_folder # Stores the destination folder in the instance attribute
        self.file_Path_extraction = None # Initialize the instance attribute as None
        
        if not os.path.exists(self.destination_folder): # Creates a folder if it doesn't exist
            os.makedirs(self.destination_folder)
            print("A seguinte pasta foi criada: ", self.destination_folder)

    # Method download_file 
    def download_file(self):
        file_name = os.path.basename(self.server_url_format) # Get the base name in specified path. Use os.path.split() method to split the specified path into a pair (head, tail)    
        
        # If file_name has invalid characters or is empty
        invalid_chars = r'[<>:"/\\|?*]' # Creates a character class with invalid characters
        if not file_name or re.search(invalid_chars, file_name): # Checks if the file_name is empty or contains invalid characters (re.search looks for any invalid characters)
            file_name = f"download_{random.randint(1, 99999)}.zip"  # Nome padrão com número aleatório

        file_path = os.path.join(self.destination_folder, file_name) # Create the destination path based on the destination folder and the file name
        
        response = requests.get(self.server_url_format) # Getting the url
        if response.status_code == 200: #If ok, downloads the file
            with open(file_path, 'wb') as file: # When opening files using open(), the WITH statement ensures that the file is closed automatically after operations are completed. 
                file.write(response.content)
                print("Arquivo salvo em: ", file_path)
        else:
            print('Falha ao realizar download')
            return
        
        self.file_Path_extraction = os.path.splitext(file_path)[0] # Save extraction path to instance attribute. Splits the path name into a pair root and ext and gets the root.
      
if __name__ == "__main__":
    teste_obj.sirgas_downloader()
    saved_file_name = teste_obj.downloader()
    pass



# Projeto 1

class downloader:
    def __init__(self, server_url_format, destination_folder):
        self.server_url_format = server_url_format # Stores the URL in the instance attribute
        self.destination_folder = destination_folder # Stores the destination folder in the instance attribute
        self.file_Path_extraction = None # Initialize the instance attribute as None
        
        if not os.path.exists(self.destination_folder): # Creates a folder if it doesn't exist
            os.makedirs(self.destination_folder)
            print("A seguinte pasta foi criada: ", self.destination_folder)

    # Method download_file 
    def download_file(self):
        file_name = os.path.basename(self.server_url_format) # Get the base name in specified path. Use os.path.split() method to split the specified path into a pair (head, tail)    
        
        # If file_name has invalid characters or is empty
        invalid_chars = r'[<>:"/\\|?*]' # Creates a character class with invalid characters
        if not file_name or re.search(invalid_chars, file_name): # Checks if the file_name is empty or contains invalid characters (re.search looks for any invalid characters)
            file_name = f"download_{random.randint(1, 99999)}.zip"  # Nome padrão com número aleatório

        file_path = os.path.join(self.destination_folder, file_name) # Create the destination path based on the destination folder and the file name
        
        response = requests.get(self.server_url_format) # Getting the url
        if response.status_code == 200: #If ok, downloads the file
            with open(file_path, 'wb') as file: # When opening files using open(), the WITH statement ensures that the file is closed automatically after operations are completed. 
                file.write(response.content)
                print("Arquivo salvo em: ", file_path)
        else:
            print('Falha ao realizar download')
            return
        
        self.file_Path_extraction = os.path.splitext(file_path)[0] # Save extraction path to instance attribute. Splits the path name into a pair root and ext and gets the root.
  