        file_name_vel = os.path.basename(self.server_url_format_vel) # Get the base name in specified path. Use os.path.split() method to split the specified path into a pair (head, tail)            
        # If file_name_vel has invalid characters or is empty
        invalid_chars = r'[<>:"/\\|?*]' # Creates a character class with invalid characters
        if not file_name_vel or re.search(invalid_chars, file_name_vel): # Checks if the file_name_vel is empty or contains invalid characters (re.search looks for any invalid characters)
            file_name_vel = f"download_{random.randint(1, 99999)}.zip"  # Nome padrão com número aleatório

        file_path = os.path.join(self.destination_folder, file_name_vel) # Create the destination path based on the destination folder and the file name
        
        response = requests.get(self.server_url_format_vel) # Getting the url
        if response.status_code == 200: #If ok, downloads the file
            with open(file_path, 'wb') as file: # When opening files using open(), the WITH statement ensures that the file is closed automatically after operations are completed. 
                file.write(response.content)
                print("Arquivo salvo em: ", file_path)
        else:
            print('Falha ao realizar download')
            return