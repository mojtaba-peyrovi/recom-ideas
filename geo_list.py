from geopy.geocoders import Nominatim
from geopy.distance import great_circle
import pandas as pd

df = pd.read_csv('C:\\Users\\mojiway\\Desktop\\recom\\hotels_searches.csv')
lats = df['lat']
lons = df['lon']
df_geo = pd.concat([df['Hotel_ID'], lats, lons], axis=1)

lat_long = (13.7259, 100.526)
d = 1

x = [tuple(x) for x in df_geo.loc[:, df_geo.columns != 'Hotel_ID'].values]
dist_function = lambda x: round(great_circle(lat_long, x).miles, 2)
final_dist =list(map(dist_function, x))
df_geo['distance'] = final_dist

list = df_geo.loc[df_geo['distance'] < 10].sort_values('distance').drop_duplicates()
final_list = list[list['distance'] != 0]
print(final_list['Hotel_ID'].values)

def top_searches(df):
    if df['searches'] > 100:
        df['ranking'] = 10
