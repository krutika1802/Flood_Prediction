import pandas as pd
from datetime import datetime, timedelta
import requests
from geopy.geocoders import Nominatim

def get_monthly_rainfall(latitude, longitude, year):
    current_date = datetime.now()
    if current_date.year == year:
        # Get the last day of the previous month
        last_day_prev_month = current_date.replace(day=1) - timedelta(days=1)
        end_date = last_day_prev_month.strftime('%Y-%m-%d')
    else:
        end_date = f"{year}-12-31"

    # Define the API URL and parameters for daily precipitation data
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": f"{year}-01-01",
        "end_date": end_date,
        "daily": "precipitation_sum",
        "timezone": "Asia/Singapore"
    }

    # Make the API request
    response = requests.get(url, params=params)
    
    # Ensure the request was successful
    if response.status_code != 200:
        raise Exception(f"Error fetching data from Open-Meteo API: {response.status_code}")

    # Process the response (JSON format)
    data = response.json()

    # Extract the daily precipitation data
    daily_precipitation_sum = data['daily']['precipitation_sum']
    daily_dates = data['daily']['time']

    # Convert to DataFrame
    daily_data = pd.DataFrame({
        "date": pd.to_datetime(daily_dates),
        "precipitation_sum": daily_precipitation_sum
    })

    # Set the date column as index
    daily_data.set_index('date', inplace=True)

    # Group by month and sum the precipitation
    monthly_precipitation = daily_data.resample('M').sum()

    # Return the monthly rainfall array
    return monthly_precipitation['precipitation_sum'].values


def get_area_name(latitude, longitude):
    geolocator = Nominatim(user_agent="area_lookup")
    location = geolocator.reverse((latitude, longitude), language='en', timeout=10)
    if location:
        return location.address
    else:
        return "Area not found"