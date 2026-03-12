import requests
import time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Configuration of pulls
BASE_URL = "https://transtats.bts.gov/PREZIP/On_Time_Reporting_Carrier_On_Time_Performance_1987_present"
RAW_DATA_PATH = Path("data/raw")
START_YEAR = 2019
END_YEAR = 2024

def download_dot_data(year, month): 
    """Download a single month of DOT on-time performance data."""
    filename = f"OTP_{year}_{month:02d}.zip"
    filepath = RAW_DATA_PATH / filename
    
    #Skip if file already downloaded
    if filepath.exists():
        print(f"{filename} already exists, skipping download.")
        return filepath
    
    url = f"{BASE_URL}_{year}_{month}.zip"
    print(f"Downloading {filename}...")

    try:
        response = requests.get(url, timeout=30)  # Set a timeout for the request
        response.raise_for_status()  # Check for HTTP errors

        with open(filepath, "wb") as f:
            f.write(response.content)
        print(f"Downloaded {filename} successfully.")
        return filepath

    except requests.exceptions.RequestException as e:
        print(f"Error downloading {filename}: {e}")
        return None
    
def download_all(start_year = START_YEAR, end_year=END_YEAR):               
    """Download DOT on-time performance data for a range of years."""
    RAW_DATA_PATH.mkdir(parents=True, exist_ok=True)  # Ensure the raw data directory exists

    successful = 0
    failed = 0

    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            result = download_dot_data(year, month)
            if result:
                successful += 1
            else:
                failed += 1
            time.sleep(1)  # Sleep to avoid overwhelming the server

    print(f"Download complete. Successful: {successful}, Failed: {failed}")

if __name__ == "__main__":
    download_all()
    