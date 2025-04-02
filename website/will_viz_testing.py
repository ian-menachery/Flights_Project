import pandas as pd
import seaborn as sns
import holoviews as hv
from holoviews import dim
import matplotlib.pyplot as plt
from bokeh.io import show
hv.extension('bokeh')


df = pd.read_csv('Final_Asia-Only_Flight_Routes.csv')

print(df.head())
print(df.columns)
'''
# Airports by # of Airlines Serving
df_exploded = df.explode('Airlines')
airport_airline_counts = df_exploded.groupby('Origin IATA')['Airlines'].nunique().reset_index()

airport_airline_counts.columns = ['Airport', 'Airlines']
top_airports = airport_airline_counts.sort_values(by='Airlines', ascending=False).head(10)

sns.set_theme()

plt.bar(top_airports['Airport'], top_airports['Airlines'])
plt.xlabel('Airport')
plt.ylabel('Number of Airlines')
plt.show()
'''

# Chord Diagram
iata_to_country = df.set_index('Origin IATA')['Origin Country'].to_dict()
df['Destination Country'] = df['Destination'].map(iata_to_country)
df = df.dropna(subset=['Destination Country'])

hv.extension('bokeh')

country_routes = df.groupby(['Origin Country', 'Destination Country']).size().reset_index(name = 'Flights')
country_routes = country_routes[country_routes['Origin Country'].isin(['Singapore', 'Malaysia', 'Thailand', 'Viet Nam'])]
country_routes = country_routes[country_routes['Destination Country'].isin(['Singapore', 'Malaysia', 'Thailand', 'Viet Nam'])]
country_routes = country_routes[country_routes['Destination Country'] != country_routes['Origin Country']]
chord_data = [(row['Origin Country'], row['Destination Country'], row['Flights']) for _, row in country_routes.iterrows()]

countries = ['Malaysia', 'Singapore',  'Thailand', 'Viet Nam']
custom_colors = ['#354698', '#E62837', '#28224F', '#F4ED3C']

nodes_df = pd.DataFrame({
    'index': countries,
    'name': countries,
    'color': custom_colors
})

nodes = hv.Dataset(nodes_df, 'index')

country_routes = df.groupby(['Origin Country', 'Destination Country']).size().reset_index(name='Flights')
country_routes = country_routes[
    country_routes['Origin Country'].isin(countries) &
    country_routes['Destination Country'].isin(countries)
]
country_routes = country_routes[country_routes['Destination Country'] != country_routes['Origin Country']]

chord_data = [
    (row['Origin Country'], row['Destination Country'], row['Flights'])
    for _, row in country_routes.iterrows()
]
chord_df = pd.DataFrame(chord_data, columns=['source', 'target', 'value'])

chord = hv.Chord((chord_df, nodes)).opts(
    width=800, height=800,
    title="Country-to-Country Flight Connectivity",
    node_color='color',
    labels='name',
    edge_color=dim('source'),
    edge_line_width=dim('value'),
    cmap=custom_colors
)

show(hv.render(chord, backend='bokeh'))
