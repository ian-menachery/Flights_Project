import pandas as pd
import folium

def plot_flight_routes(country1, country2):
    df = pd.read_csv('all_connections_coordinates.csv')
    filtered_df = df[((df['Origin Country'] == country1) & (df['Destination Country'] == country2)) |
                     ((df['Origin Country'] == country2) & (df['Destination Country'] == country1))]
    
    if not filtered_df.empty:
        avg_lat = (filtered_df['Origin Latitude'].mean() + filtered_df['Destination Latitude'].mean()) / 2
        avg_lon = (filtered_df['Origin Longitude'].mean() + filtered_df['Destination Longitude'].mean()) / 2
    else:
        avg_lat, avg_lon = 35, 85
    
    flight_map = folium.Map(location=[avg_lat, avg_lon], zoom_start=4)
    
    if filtered_df.empty:
        folium.Marker(
            location=[avg_lat, avg_lon],
            icon=folium.DivIcon(html='<div style="background-color: gray; padding: 10px; border-radius: 5px; font-size: 24px; font-weight: bold; text-align: center; color: white; width: 250px; margin: 0 auto;">No Direct Flights Available</div>')
        ).add_to(flight_map)

        flight_map.options['zoomControl'] = False
        flight_map.options['dragging'] = False
        flight_map.options['scrollWheelZoom'] = False
        flight_map.options['touchZoom'] = False

    else:
        for _, row in filtered_df.iterrows():
            origin = [row['Origin Latitude'], row['Origin Longitude']]
            destination = [row['Destination Latitude'], row['Destination Longitude']]
            
            origin_color = 'red' if row['Origin Country'] == country1 else 'blue'
            destination_color = 'red' if row['Destination Country'] == country1 else 'blue'
            
            folium.CircleMarker(origin, radius=5, color=origin_color, fill=True, fill_color=origin_color, fill_opacity=0.7, popup=row['Origin']).add_to(flight_map)
            folium.CircleMarker(destination, radius=5, color=destination_color, fill=True, fill_color=destination_color, fill_opacity=0.7, popup=row['Destination']).add_to(flight_map)
        
            folium.PolyLine([origin, destination], color='black', weight=2, opacity=0.7).add_to(flight_map)
    
    return flight_map

origin, destination = "Pakistan", "Pakistan"
flight_map = plot_flight_routes(origin, destination)
flight_map.save(f"flight_routes_{origin.replace(' ', '_')}_{destination.replace(' ', '_')}.html")