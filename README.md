# NRT-World-Active-Fires

Hello everyone, this is a near real time web [Streamlit](https://streamlit.io/) app of active fires around the globe, extracted from [NASA FIRMS API](https://firms.modaps.eosdis.nasa.gov/).

Created with Streamlit which allows us to simplify the frontend process and folium library which generates a map based on box coordinates and active fires in that zone :fire:.

Backend file with REST API methods in [nasaAPI.py](./nasaAPI.py), application in [fire_app.py](./fire_app.py)


### 1. Get a NASA FIRMS API key to execute request calls.

First of all, you need a key from [NASA api](https://api.nasa.gov/) which allows us to get fire active data.
Then introduce this key into "key_value" string at [nasaAPI.py](./nasaAPI.py)

### 2. Install requirements

Install modules with pip at project work directory.
```
pip install -r requirements.txt
```
### 3. Execute App

Execute via command line [defineModel.py](./defineModel.py) to generate a local web browser app.  
```
streamlit run fire_app.py
```
