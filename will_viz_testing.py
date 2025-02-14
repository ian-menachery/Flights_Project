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
chord_data = [(row['Origin Country'], row['Destination Country'], row['Flights']) for _, row in country_routes.iterrows()]

chord = hv.Chord(chord_data).opts(
    width=800, height=800,
    title="Country-to-Country Flight Connectivity",
    cmap='Category20',
    edge_color=dim('source').str(),
    node_color=dim('index').str(),
    labels='name'
)

#chord
show(hv.render(chord, backend='bokeh'))