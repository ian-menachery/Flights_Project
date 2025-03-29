import pandas as pd


df = pd.read_csv('asia_routes.csv')
print(df.columns)
df = df[['iata', 'name', 'country', 'city_name', 'latitude', 'longitude']]
df.to_csv('airport_coordinates.csv')
print(df.columns)
print(df.head())
