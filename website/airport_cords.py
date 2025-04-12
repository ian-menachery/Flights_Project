import pandas as pd

def coordinates_file(df, non_asia):
    coordinates_df = df[['iata', 'name', 'country', 'city_name', 'latitude', 'longitude']]
    coordinates_df = coordinates_df[~coordinates_df['iata'].isin(non_asia)]
    #coordinates_df.to_csv('airport_coordinates.csv')
    return coordinates_df

def num_connections(df, non_asia):
    df_routes = df[~df['Origin'].isin(non_asia) & ~df['Destination'].isin(non_asia)]
    df_routes = df.groupby('Origin')['Destination'].nunique().reset_index()
    df_routes.columns = ['Airport', 'Num_Routes']
    return df_routes

def major_airports(df_routes, coordinates_df, large_threshold = 20):
    large_airports = df_routes[df_routes['Num_Routes'] > large_threshold]
    large_airport_cords = pd.merge(large_airports, coordinates_df, left_on='Airport', right_on='iata', how='inner')
    large_airport_cords = large_airport_cords.drop(columns=['Airport'])
    #large_airport_cords.to_csv('large_airport_coordinates.csv')
    return large_airport_cords 


def major_routes(large_coordinates_df, asia_only, non_asia):
    asia_only = asia_only[~asia_only['Origin'].isin(non_asia) & ~asia_only['Destination'].isin(non_asia)]
    asia_only = asia_only[asia_only['Origin'].isin(large_coordinates_df['iata'])]
    asia_only = asia_only.merge(large_coordinates_df[['iata', 'latitude', 'longitude']], 
                            left_on='Destination', right_on='iata', how='left')
    asia_only.rename(columns={'latitude': 'Destination_Latitude', 'longitude': 'Destination_Longitude'}, inplace=True)
    large_connections = asia_only[['Origin', 'Destination', 'Destination_Latitude', 'Destination_Longitude']]
    large_connections = large_connections.dropna()
    large_connections.to_csv('large_connections.csv')
    print(large_connections)

if __name__ == "__main__":
    non_asia = ['LHN', 'KUB', 'ZGC', 'MZW', 'DBB', 'SPX', 'GOY', 'LLM', 'WBM', 'LAB']
    df = pd.read_csv('asia_routes.csv')
    asia_only = pd.read_csv('Final_Asia-Only_Flight_Routes.csv')
    df_routes = num_connections(asia_only, non_asia)
    coordinates_df = coordinates_file(df, non_asia)
    large_airport_cords = major_airports(df_routes, coordinates_df)
    large_coordinates_df = coordinates_file(large_airport_cords, non_asia)
    major_routes(large_coordinates_df, asia_only, non_asia)