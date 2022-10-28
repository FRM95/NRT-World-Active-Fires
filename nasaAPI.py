import requests
import pandas as pd
import pprint
import csv
import folium
from datetime import datetime
import numpy as np

# NASA API Services variables and description
area = 'area'; area_desc = 'Fire detection hotspots based on area, date and sensor in CSV format'
countries = 'countries'; countries_desc = 'List of supported countries'
country = 'country'; country_desc = 'Fire detection hotspots based on country, date and sensor in CSV format'
data_availability = 'data_availability'; data_availability_desc = 'Date availability of SP and NRT data'
kml_fire_footprints = 'kml_fire_footprints'; kml_fire_footprints_desc = 'KML fire detection footprints'

# NASA APi attributes
endpoint = 'https://firms.modaps.eosdis.nasa.gov/api/'
key_value = ''
source = 'VIIRS_SNPP_NRT'
output = ['json','csv']

class nasaFire(object):


    def __init__(self):
        self.endpoint = 'https://firms.modaps.eosdis.nasa.gov/api/'

    # Function to request information from url
    def requestURL(self,url):
        try:
            api_response = requests.get(url=url, timeout=40, stream=True)
            api_response.raise_for_status()
            print('OK')
            return api_response
        except requests.exceptions.HTTPError as errh:
            print(f'Error: {errh} has occurred!')
        except requests.exceptions.ConnectionError as errc:
            print(f'Error: {errc} has occurred!')
        except requests.exceptions.Timeout as errt:
            print(f'Error: {errt} has occurred!')
        except requests.exceptions.RequestException as err:
            print(f'Error: {err} has occurred!')

    # Function to process requests responses as dataframe
    def processResponse(self,response):
        lines = response.text.splitlines()
        data_req = [i.split(sep=',') for i in lines[1:]]
        data_columns = lines[0].split(sep=',')
        result_df = pd.DataFrame(data=data_req, columns=data_columns)
        return result_df

    # Function that returns area coordinates as dataframe
    def getAreaCoord(self):
        area = ['World', 'Canada', 'Alaska', 'USA_Hawaii', 'Central_America', 'South_America', 'Europe',
                'North_Central_Africa',
                'South_Africa', 'Russia_Asia', 'South_Asia', 'South_East_Asia', 'Australia_NewZealand']
        coordinates = ['-180,-90,180,90', '-150,40,-49,79', '-180,50,-139,72', '-160.5,17.5,-63.8,50',
                       '-119.5,7,-58.5,33.5',
                       '-112,-60,-26,13', '-26,34,35,82', '-27,-10,52,37.5', '10,-36,58.5,-4', '26,9,180,83.5',
                       '54,5.5,102,40',
                       '88,-12,163,31', '110,-55,180,-10']
        result_df = pd.DataFrame(data=list(zip(area, coordinates)), columns=['area', 'geom'])
        return result_df

    def getSources(self):
        url = f'{endpoint}data_availability/csv/{key_value}/ALL'
        request_list = self.requestURL(url)
        result = self.processResponse(request_list)
        return result

    # Function that returns country coordinates as dataframe
    def getCountriesCoord(self):
        url = f'{endpoint}countries/?format=json'
        countries_list = self.requestURL(url).json()
        country_data = [list(i.values()) for i in countries_list]
        data_columns = list(countries_list[0].keys())
        result_df = pd.DataFrame(data=country_data, columns=data_columns)
        result_df.drop('id', axis=1, inplace=True)
        new_coord = []
        for i in result_df['geom']:
            a = str(i)[3:].replace(" ", ",").replace("(", "").replace(")", "").strip()
            new_coord.append(a)
        result_df['geom'] = new_coord
        return result_df

    # Function that returns fire coordinates from country as dataframe
    def getCountryFire(self,country, source='VIIRS_SNPP_NRT', dayrange=1, date=''):
        url = f'{endpoint}country/csv/{key_value}/{source}/{country}/{dayrange}/{date}'
        request_list = self.requestURL(url)
        result = self.processResponse(request_list)
        return result

    # Function that returns fire coordinates from area as dataframe
    def getAreaFire(self,area, source='VIIRS_SNPP_NRT', dayrange=1, date=''):
        url = f'{endpoint}area/csv/{key_value}/{source}/{area}/{dayrange}/{date}'
        request_list = self.requestURL(url)
        result = self.processResponse(request_list)
        return result