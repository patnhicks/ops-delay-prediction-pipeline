import zipfile
import pandas as pd
from pathlib import Path
import logging

#COnfigure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

#Paths
RAW_DATA_PATH = Path("data/raw")
PROCESSED_DATA_PATH = Path("data/processed")

#Keep necessary columns
KEEP_COLUMNS = [
    # Time variables
    'Year', 'Quarter', 'Month', 'DayofMonth', 'DayOfWeek', 'FlightDate',
    # Carrier and flight variables
    'Reporting_Airline', 'Flight_Number_Reporting_Airline', 'Tail_Number',
    # Routing
    'Origin', 'OriginCityName', 'OriginState',
    'Dest', 'DestCityName', 'DestState',
    'Distance','DistanceGroup',
    #Departure Performance
    'CRSDepTime', 'DepTime', 'DepDelay', 'DepDelayMinutes', 'DepDel15',
    #Arrival Performance
    'CRSArrTime', 'ArrTime', 'ArrDelay', 'ArrDelayMinutes', 'ArrDel15',
    #Delay Causes
    'CarrierDelay', 'WeatherDelay', 'NASDelay', 'SecurityDelay', 'LateAircraftDelay',
    #Flight Status
    'Cancelled', 'CancellationCode', 'Diverted', 'CRSElapsedTime', 'ActualElapsedTime', 'AirTime'
]

def extract_csv_from_zip(zip_path):
    """Extract a CSV file from a ZIP file and return as df."""
    with zipfile.ZipFile(zip_path) as z:
            csv_name = [f for f in z.namelist() if f.endswith('.csv')][0]
            with z.open(csv_name) as f:
                df = pd.read_csv(f, low_memory=False)
    return df

def transform(df):
    """Cleans and standardizes df"""
    #Keep relevant columns
    df = df[[col for col in KEEP_COLUMNS if col in df.columns]]
    # Convert time to datetime
    df['FlightDate'] = pd.to_datetime(df['FlightDate'], errors='coerce')
    # Fill delay cause nulls with 0 (no delay = 0 minutes)
    delay_cols = ['CarrierDelay', 'WeatherDelay', 'NASDelay', 'SecurityDelay', 'LateAircraftDelay']
    df[delay_cols] = df[delay_cols].fillna(0)

    # Fill nulls in DepDelay and ArrDelay with 0 (assume no delay if not specified)
    df['DepDelay'] = df['DepDelay'].fillna(0)
    df['ArrDelay'] = df['ArrDelay'].fillna(0)
    df['DepDelayMinutes'] = df['DepDelayMinutes'].fillna(0)
    df['ArrDelayMinutes'] = df['ArrDelayMinutes'].fillna(0)
    # Ensure delay indicators are binary
    df['Cancelled'] = df['Cancelled'].fillna(0).astype(int)
    df['Diverted'] = df['Diverted'].fillna(0).astype(int)
    df['DepDel15'] = df['DepDel15'].fillna(0).astype(int)
    df['ArrDel15'] = df['ArrDel15'].fillna(0).astype(int)

    # Strip whitespace from string columns
    str_cols = ['Reporting_Airline', 'Origin', 'Dest', 'OriginCityName', 'DestCityName', 'OriginState', 'DestState']
    for col in str_cols:
         if col in df.columns:
            df[col] = df[col].str.strip()

    return df 

def process_file(zip_path):
    """Extract, transform, and save a single file."""
    filename = zip_path.stem  # Get filename without .zip
    output_path = PROCESSED_DATA_PATH / f"{filename}_processed.parquet"

    # Skip if already processed
    if output_path.exists():
        logger.info(f"Already processed: {filename}")
        return output_path

    logger.info(f"Processing: {filename}")

    try: 
        df = extract_csv_from_zip(zip_path)
        df = transform(df)
        df.to_parquet(output_path, index=False)
        logger.info(f"Saved: {output_path} ({len(df):,} rows)")
        return output_path
    
    except Exception as e:
        logger.error(f"Error processing {filename}: {e}")
        return None
    
def  process_all():
    """Process all ZIP files in the raw data directory."""
    PROCESSED_DATA_PATH.mkdir(parents=True, exist_ok=True)  # Ensure processed data directory exists
    zip_files = sorted(RAW_DATA_PATH.glob("*.zip"))
    logger.info(f"Found {len(zip_files)} files to process.")

    successful = 0
    failed = 0

    for zip_path in zip_files:
        result = process_file(zip_path)
        if result:
            successful += 1
        else:
            failed += 1

    logger.info(f"Processing complete. Successful: {successful}, Failed: {failed}")

if __name__ == "__main__":
    process_all()