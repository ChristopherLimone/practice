# https://www.kaggle.com/alexisbcook/your-first-map
# source env/Scripts/activate

# %%
import numpy as np
import math
import pandas as pd
import geopandas as gpd
import geopy as gpy
from shapely.geometry import LineString
import folium
from folium import Choropleth, Circle, Marker
from folium.plugins import HeatMap, MarkerCluster

# %%
my_zip = "02370"
my_country = "USA"
locator = gpy.Nominatim(user_agent="myGeocoder")
address = {"postalcode": my_zip, "country": my_country}
location = [locator.geocode(address).latitude, locator.geocode(address).longitude]

# %%
# tiles='cartodbdark_matter'
# tiles='cartodbpositron'
# tiles='cartodbpositronnolabels'
# tiles='cartodbpositrononlylabels'
# tiles='openstreetmap'
# tiles='stamenterrain'
# tiles='stamentoner'
# tiles='stamentonerbackground'
# tiles='stamentonerlabels'
# tiles='stamenwatercolor'

# Rockland, MA location=[42.130,-70.912]

m_1 = folium.Map(location=location, tiles='cartodbpositron', zoom_start=10)
m_1



# %%
# Load the data
crimes = pd.read_csv("data/crime.csv", encoding='latin-1')

# Drop rows with missing locations
crimes.dropna(subset=['Lat', 'Long', 'DISTRICT'], inplace=True)

# Focus on major crimes in 2018
crimes = crimes[crimes.OFFENSE_CODE_GROUP.isin([
    'Larceny', 'Auto Theft', 'Robbery', 'Larceny From Motor Vehicle', 'Residential Burglary',
    'Simple Assault', 'Harassment', 'Ballistics', 'Aggravated Assault', 'Other Burglary', 
    'Arson', 'Commercial Burglary', 'HOME INVASION', 'Homicide', 'Criminal Harassment', 
    'Manslaughter'])]
crimes = crimes[crimes.YEAR>=2018]

# Print the first five rows of the table
crimes.head()

# %%
daytime_robberies = crimes[((crimes.OFFENSE_CODE_GROUP == 'Robbery') & \
                            (crimes.HOUR.isin(range(9,18))))]
                            
# Create a map
m_2 = folium.Map(location=[42.32,-71.0589], tiles='cartodbpositron', zoom_start=13)

# Add points to the map
for idx, row in daytime_robberies.iterrows():
    Marker([row['Lat'], row['Long']]).add_to(m_2)

# Display the map
m_2

# %%
# Create the map
m_3 = folium.Map(location=[42.32,-71.0589], tiles='cartodbpositron', zoom_start=13)

# Add points to the map
mc = MarkerCluster()
for idx, row in daytime_robberies.iterrows():
    if not math.isnan(row['Long']) and not math.isnan(row['Lat']):
        mc.add_child(Marker([row['Lat'], row['Long']]))
m_3.add_child(mc)

# Display the map
m_3

# %%
# Create a base map
m_4 = folium.Map(location=[42.32,-71.0589], tiles='cartodbpositron', zoom_start=13)

def color_producer(val):
    if val <= 12:
        return 'forestgreen'
    else:
        return 'darkred'

# Add a bubble map to the base map
for i in range(0,len(daytime_robberies)):
    Circle(
        location=[daytime_robberies.iloc[i]['Lat'], daytime_robberies.iloc[i]['Long']],
        radius=20,
        color=color_producer(daytime_robberies.iloc[i]['HOUR'])).add_to(m_4)

# Display the map
m_4

# %%
# Create a base map
m_5 = folium.Map(location=[42.32,-71.0589], tiles='cartodbpositron', zoom_start=12)

# Add a heatmap to the base map
HeatMap(data=crimes[['Lat', 'Long']], radius=10).add_to(m_5)

# Display the map
m_5

# %%
# GeoDataFrame with geographical boundaries of Boston police districts
districts_full = gpd.read_file('data/Police_Districts.geojson')
districts = districts_full[["DISTRICT", "geometry"]].set_index("DISTRICT")
districts.head()

# %%
# Number of crimes in each police district
plot_dict = crimes.DISTRICT.value_counts()
plot_dict.head()

# %%
# Create a base map
m_6 = folium.Map(location=[42.32,-71.0589], tiles='cartodbpositron', zoom_start=12)

# Add a choropleth map to the base map
Choropleth(geo_data=districts.__geo_interface__, 
           data=plot_dict, 
           key_on="feature.id", 
           fill_color='YlGnBu', 
           legend_name='Major criminal incidents (Jan-Aug 2018)'
          ).add_to(m_6)

# Display the map
m_6

# %%
