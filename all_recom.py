from geopy.geocoders import Nominatim
from geopy.distance import great_circle
import pandas as pd
import numpy as np
from scipy.stats import norm

# dataframe:
df = pd.read_csv('C:\\Users\\mojiway\\Desktop\\recom\\recom_table_2.csv')

df['commission'] =  0.15

# input fields:
city_input = 'Bangkok'
lat_input =  13.7232287506169
lon_input = 100.539687774827
distance_input = 1
stars_input = '5-star'

# data slicing based on the distribution:
def dist(col):
    mean, std = norm.fit(col)
    p0 = mean + 2 * std
    p1 = mean + std
    p2 = mean
    p3 = mean-std if std < mean else mean-0.4*std
    return p0, p1, p2, p3

# gbv_per_rns rank
gbv_rns_slices = dist(df['GBV_per_RNS'])
df.loc[df['GBV_per_RNS'] > gbv_rns_slices[0], 'gbv_rns_rank'] = 1000
df.loc[(df['GBV_per_RNS'] <gbv_rns_slices[0]) & (df['GBV_per_RNS'] > gbv_rns_slices[1]) , 'gbv_rns_rank'] = 750
df.loc[(df['GBV_per_RNS'] <gbv_rns_slices[1]) & (df['GBV_per_RNS'] > gbv_rns_slices[2]) , 'gbv_rns_rank'] = 500
df.loc[(df['GBV_per_RNS'] <gbv_rns_slices[2]) & (df['GBV_per_RNS'] > gbv_rns_slices[3]) , 'gbv_rns_rank'] = 250
df.loc[df['GBV_per_RNS'] < gbv_rns_slices[3], 'gbv_rns_rank'] = 100

#calculate estimated_revenue
df['estimated_revenue'] = df['gbv_rns_rank'] * df['commission']

# estimated_revenue rank
estimated_revenue_slices = dist(df['estimated_revenue'])
df.loc[df['estimated_revenue'] > estimated_revenue_slices[0], 'revenue_rank'] = 1000
df.loc[(df['estimated_revenue']< estimated_revenue_slices[0]) & (df['estimated_revenue'] > estimated_revenue_slices[1]) , 'revenue_rank'] = 750
df.loc[(df['estimated_revenue']< estimated_revenue_slices[1]) & (df['estimated_revenue'] > estimated_revenue_slices[2]) , 'revenue_rank'] = 500
df.loc[(df['estimated_revenue']< estimated_revenue_slices[2]) & (df['estimated_revenue'] > estimated_revenue_slices[3]) , 'revenue_rank'] = 250
df.loc[df['estimated_revenue'] < estimated_revenue_slices[3], 'revenue_rank'] = 100

#city rank
df['city_rank'] = np.where(df['city']== city_input, 1, 0)

#star rank
df['star_rank'] = np.where(df['stars']== stars_input, 1, 0)


#booking rank
booking_slices = dist(df['bookings'])
df.loc[df['bookings'] > booking_slices[0], 'booking_rank'] = 1000
df.loc[(df['bookings'] < booking_slices[0]) & (df['bookings'] > booking_slices [1]) , 'booking_rank'] = 750
df.loc[(df['bookings'] <booking_slices[1]) & (df['bookings'] > booking_slices [2]) , 'booking_rank'] = 500
df.loc[(df['bookings'] < booking_slices[2]) & (df['bookings'] > booking_slices [3]) , 'booking_rank'] = 250
df.loc[df['bookings'] < booking_slices[3], 'booking_rank'] = 100

#gbv rank
gbv_slices = dist(df['GBV'])
df.loc[df['GBV'] > gbv_slices[0], 'GBV'] = 1000
df.loc[(df['GBV'] < gbv_slices[0]) & (df['GBV'] > gbv_slices[1]) , 'gbv_rank'] = 750
df.loc[(df['GBV'] < gbv_slices[1]) & (df['GBV'] >gbv_slices[2]) , 'gbv_rank'] = 500
df.loc[(df['GBV'] < gbv_slices[2]) & (df['GBV'] > gbv_slices[3]) , 'gbv_rank'] = 250
df.loc[df['GBV'] < gbv_slices[3], 'gbv_rank'] = 100


#distance calculator
def distancer(row):
    coords_1 = (row['lat'], row['lon'])
    coords_2 = (lat_input, lon_input)
    return round(great_circle(coords_1, coords_2).miles,2)

df['distance'] = df.apply(distancer, axis=1)

#distance rank
df['distance_rnk'] = np.where(df['distance'] < distance_input, 1, 0)

# remove self hotel
df = df[df['distance'] != 0]

# final formula to calculate the final rank
df['rnk'] = (2*df['gbv_rns_rank'] + 2*df['booking_rank'] + 2*df['gbv_rank'] + 5*df['estimated_revenue']) *df['city_rank'] * df['star_rank'] * df['distance_rnk']

# sort by final rank
df.sort_values(by=['rnk'], ascending=False)

#output hotels
# df_json = df[df['rnk'] != 0].to_json(orient='split')
# print(df_json)

print(df['Hotel_ID'].values)
