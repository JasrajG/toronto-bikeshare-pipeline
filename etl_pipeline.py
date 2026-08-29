import requests
import pandas as pd
import os
from sqlalchemy import create_engine
import folium
import datetime
from dotenv import load_dotenv



# This library helps read our hidden .env file
from dotenv import load_dotenv 

def extract_data():
    """Pulls data from the GBFS API."""
    print("Extracting data...")
    print("1. Fetching data from Toronto Bike Share...")
    discovery_data = requests.get("https://toronto.publicbikesystem.net/customer/gbfs/v3.0/gbfs.json").json()

    #the data urls are inside of the feeds key which is inside the data key
    feeds = discovery_data['data']['feeds']

    info_url = next(feed['url'] for feed in feeds if feed['name'] == 'station_information')
    status_url = next(feed['url'] for feed in feeds if feed['name'] == 'station_status')

    #fetch JSON payloads, flatten the nested arrays into dataframes
    #subset only required columns
    df_info = pd.DataFrame(requests.get(info_url).json()['data']['stations'])[['station_id', 'name', 'lat', 'lon']]
    df_status = pd.DataFrame(requests.get(status_url).json()['data']['stations'])[['station_id', 'num_vehicles_available']]

    # Return df_info and df_status
    return df_info, df_status

def transform_data(df_info, df_status):
    """Cleans and merges the data."""
    print("Transforming data...")
    print("Transforming data...")
    
    # We have two separate tables we need to do join the 'station_id' column 
    # so that Station Name, Lat/Lon, and Vehicle Count are all in one flat table.
    
    clean_data = pd.merge(df_info, df_status, on='station_id')
    clean_data['name'] = clean_data['name'].apply(lambda x: x[0]['text'])
    
    # Time Series Timestamp
    # the data tells us how many bikes are there, but not when
    # create a brand new column called 'last_updated' and set every 
    # row in that column to the exact current time from our local machine

    clean_data['last_updated'] = datetime.datetime.now()
    
    return clean_data

def load_data(df_merged):
    """Saves the data to the Postgres database."""
    print("Loading data into Database...")
    
    # Load database URL from .env file
    load_dotenv()
    db_url = os.getenv("DATABASE_URL")
    
    # Create the SQLAlchemy engine (bridge to database)
    engine = create_engine(db_url)
    
    # Load the data into the database
    clean_data.to_sql(name='bike_station_status', con=engine, index=False, if_exists='append')
    pass


if __name__ == "__main__":
    print("Starting ETL Pipeline...")
    
    # 1. Extract
    info, status = extract_data()
    
    # 2. Transform
    clean_data = transform_data(info, status)
    
    # 3. Load
    load_data(clean_data)
    
    print("ETL Pipeline completed successfully!")