import pandas as pd
import shapely
import geopandas as gpd 

lnd_point = shapely.Point(0.1, 51.5)
paris_point = shapely.Point(2.3, 48.9)
towns_geom = gpd.GeoSeries([lnd_point, paris_point], crs=4326)
towns_data = {
    'name' : ['London', 'Paris'],
    'temperature' : [25, 27],
    'date' : ['2013-06-21','2013-06-21'],
    'geometry' : towns_geom
}
towns_layer = gpd.GeoDataFrame(towns_data)

file_path = "C:\\Users\\filip\\progcart\\projeto_2_geopandas\\docs\\towns.shp"

towns_layer.to_file(file_path)
print("O arquivo foi salvo em: ", file_path)

filename = "C:\\Users\\filip\\progcart\\projeto_2_geopandas\\docs\\teste.csv"

df2 = pd.read_csv(filename)

print(df2)

for id, row in df2.iterrows():
    print([row["nome"]])