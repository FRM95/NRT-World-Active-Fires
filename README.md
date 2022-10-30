# NRT-World-Active-Fires

Hello everyone, this is a near real time web [Streamlit](https://streamlit.io/) app of active fires around the globe, extracted from [NASA FIRMS API](https://firms.modaps.eosdis.nasa.gov/).

Written with Python and created with Streamlit which allows us to simplify the frontend process. Also implemented with folium library which generates a map based on box coordinates and active fires in that zone :fire:.

Application in [fire_app.py](./fire_app.py), backend file with REST API methods at [nasaAPI.py](./nasaAPI.py). 


### 1. Get a NASA FIRMS API key to execute request calls.

First of all, you need a key from [NASA api](https://api.nasa.gov/) which allows us to get fire active data.

You will normally receive this key through your email after a registration process.

Then introduce this key at [nasaAPI.py](./nasaAPI.py) into "key_value" string. 

It is mandatory to acquire this key, otherwise main program won't be able to communicate with NASA REST API to get fires data.

### 2. Install requirements

Install necessary modules with pip at the project work directory.
```
pip install -r requirements.txt
```
### 3. Execute App

Execute via command line [defineModel.py](./defineModel.py) to generate a local web browser app.  
```
streamlit run fire_app.py
```
