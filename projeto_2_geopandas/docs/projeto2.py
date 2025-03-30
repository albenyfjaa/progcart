import gzip
filename = "C://Users//filip//progcart//projeto_2_geopandas//docs//SIRGAS2022_XYZ.CRD.gz"

with gzip.open(filename, 'wb') as f:
    f.write("C://Users//filip//progcart//projeto_2_geopandas//docs//SIRGAS2022_XYZ_extract")

