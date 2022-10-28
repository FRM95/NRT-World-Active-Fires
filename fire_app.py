#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import streamlit as st
import folium
from time import gmtime, strftime, localtime
from datetime import date, timedelta
import nasaAPI
from streamlit_folium import st_folium, folium_static

# Creates a map with fire points based on API df and centered on coordinates
def showFireMap(df,coordinates,date):
    coordinates = coordinates.split(',')
    coordinates = [float(i) for i in coordinates]
    map_return = folium.Map(min_lon=coordinates[0], #min lon
                          max_lon=coordinates[2], #min lat
                          min_lat=coordinates[1], #max lon
                          max_lat=coordinates[3], #min lon
                          max_bounds=False)
    folium.FitBounds([([coordinates[1], coordinates[0]]), ([coordinates[3], coordinates[2]])]).add_to(map_return)
    df = df[df['acq_date'] == date] # selects fire from actual date in map_return
    df.reset_index(drop=True,inplace=True)
    for i in df.index:
        lat, lon = df.iloc[i, df.columns.get_loc('latitude')], df.iloc[i, df.columns.get_loc('longitude')]
        folium.Marker(location=[float(lat), float(lon)],
              tooltip=f'Latitude: {lat} Longitude: {lon}',
              icon=folium.Icon(icon='fire', icon_color='orange', color='red')).add_to(map_return)
    return map_return

# Creates an empty world default map
def showdefaultmap():
    map_return = folium.Map(zoom_start=2, location=[0, 0])
    return map_return

# Generates number fires based on API df
@st.cache
def showStatistics(df,today,yesterday):
    n_fires_today = len(df[df['acq_date'] == today].index)
    n_fires_yest = len(df[df['acq_date'] == yesterday].index)
    n_fires_3days = len(df.index)
    return n_fires_today, n_fires_yest, n_fires_3days



# App attributes
app_tittle = f'NRT Active fires Map'
api_url = nasaAPI.endpoint
streamlit = 'https://streamlit.io/'


# Main program
def main():

    # Fire NASA API call
    # todo convert to object for st cache
    nasa_object = nasaAPI.nasaFire()

    # Saves information from every country and area
    # todo convert to object for st cache
    country_info = nasa_object.getCountriesCoord()
    area_info = nasa_object.getAreaCoord()

    # Date and time variables
    current_time = strftime("%A, %d %b %Y %H:%M", localtime())
    current_date = strftime("%Y-%m-%d", localtime())
    yesterday_date = str(date.today() - timedelta(days=1))

    # APP structure definition
    st.set_page_config(page_title=app_tittle, layout='wide')
    st.title(app_tittle)
    st.markdown(f'Open Source interactive [Streamlit]({streamlit}) app to visualize near-real-time [NASA]({api_url[:-5]}) active fires around the globe.')

    # Default number fires found today, yesterday and 3 past days
    f_today, f_yest, f_3days = '0', '0', '0'
    leftpage, rightpage = st.columns([1,3],gap='medium')

    with leftpage:
        # Input area to generate a map
        location_input = st.text_input(label = 'example',
                                   placeholder='Introduce country or area to search active fires Example: Spain or Europe',
                                   label_visibility='hidden')

        #col1, col2, col3 = st.columns(3)
        #with col1:
        #    st.metric(label='Fires today', value=f_today)
        #with col2:
        #    st.metric(label='Fires yesterday', value=f_yest)
        #with col3:
        #    st.metric(label='Fires last 3 days', value=f_3days)

    with rightpage:

        st.markdown("\n\n\n") # allows me to use same space
        st.markdown('') # alows me to use same space
        st.markdown(f'Current local date: {current_time}') # Date above the map

        # If location is introduced
        if location_input:

            # If location represents a country
            if location_input in country_info['name'].values:
                coordinates = country_info[country_info['name'] == location_input]['geom'].values[0] # country coordinates
                abreviation = country_info[country_info['name'] == location_input]['abreviation'].values[0] # country abreviation
                country_fire_coordinates = nasa_object.getCountryFire(country=abreviation,dayrange=3) # active fires in country
                f_today, f_yest, f_3days = showStatistics(country_fire_coordinates, current_date, yesterday_date)
                final_map = showFireMap(country_fire_coordinates, coordinates, date=current_date)

            # If location represents an area
            elif location_input in area_info['area'].values:
                coordinates = area_info[area_info['area'] == location_input]['geom'].values[0] # area coordinates
                area_fire_coordinates = nasa_object.getAreaFire(area=coordinates, dayrange=3) # active fires in area
                f_today, f_yest, f_3days = showStatistics(area_fire_coordinates, current_date, yesterday_date)
                final_map = showFireMap(area_fire_coordinates, coordinates, date=current_date)

            # Wrong location: no statistics to show and empty map
            else:
                st.warning('Wrong country or area', icon="⚠")
                final_map = showdefaultmap()

            # Display fire map based on input
            folium_static(final_map, width=1000, height=550)

        # No location then displays world map
        else:
            final_map = showdefaultmap()
            folium_static(final_map, width=1000, height=550)

    with leftpage:
        st.metric(label='Fires today', value=f_today)
        st.metric(label='Fires yesterday', value=f_yest)
        st.metric(label='Fires last 3 days', value=f_3days)




if __name__ == "__main__":
    main()

