import geopandas as gpd
import pandas as pd

def read_sirgas_dataframe(filename):
    df = pd.read_fwf(filename, skiprows=17, encoding='latin-1')
    
    return df

if __name__ == "__main__":
    from sirgas_downloader import sirgas_downloader
    test_obj = sirgas_downloader()

    saved_file_name = test_obj.download(test_obj.multianual_coord_url)
    decompressed_crd_file = test_obj.decompress(saved_file_name)    
    
    df = read_sirgas_dataframe(decompressed_crd_file)

    print(df)