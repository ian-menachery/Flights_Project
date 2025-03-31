import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import folium

df = pd.read_csv('Final_Asia-Only_Flight_Routes.csv')
coordinate_df = pd.read_csv('airport_coordinates.csv')

coordinate_df = coordinate_df[['iata', 'latitude', 'longitude']]

airport_counts = df.groupby('Origin')['Destination'].nunique()
airport_data = coordinate_df.merge(airport_counts, how='left', left_on='iata', right_on='Origin')

airport_name = df[['Origin', 'Origin City']]
airport_name = airport_name.drop_duplicates()
airport_data = airport_data.merge(airport_name, how='left', left_on='iata', right_on='Origin')

airport_data = airport_data.dropna()
airport_data['Destination'] = airport_data['Destination'].astype('int')
m = folium.Map(location=[20, 100], zoom_start=3)

def get_color(destinations):
    if destinations > 75:
        return "#16099e"
    elif destinations >= 25:
        return "#aa0086"
    else:
        return "#ff6c47"


for _, row in airport_data.iterrows():
    tooltip_text = f"Airport: {row['iata']}<br>City: {row['Origin City']}<br>Direct Destinations: {row['Destination']}"
    color = get_color(row['Destination'])
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=row['Destination'] * .1,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=.8,
        tooltip=tooltip_text
    ).add_to(m)

m.save('airport_bubble_map.html')
