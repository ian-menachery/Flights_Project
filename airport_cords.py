import pandas as pd


df = pd.read_csv('asia_routes.csv')
df = df[['iata', 'country_code', 'latitude', 'longitude']]
df.to_csv('airport_coordinates.csv')
print(df.columns)
print(df.head())
