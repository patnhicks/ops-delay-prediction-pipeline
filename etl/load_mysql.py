import pandas as pd
from pathlib import Path

from pandas.io import parquet
import mysql.connector
from sqlalchemy import create_engine
import logging
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Paths
PROCESSED_DATA_PATH = Path("data/processed") 
# MySQL connection parameters from environment variables
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "ops_logistics")

def get_engine():
    """Create SQLAlchemy engine"""
    return create_engine(f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')

def load_file(parquet_path, engine):
    """Load file"""
    filename = parquet_path.stem
    logger.info(f"Loading {filename} into MySQL")

    try:
         df = pd.read_parquet(parquet_path)

         # Rename columns
         df = df.rename(columns={
              'Flight_Number_Reporting_Airline': 'Flight_Number'})

         # Load into MySQL
         df.to_sql(
            name='flights',
            con=engine,
            if_exists='append', 
            index=False, 
            chunksize=10000)
    
         logger.info(f"Finished loading {len(df):,} rows from {filename}")
         return True
    
    except Exception as e:
         logger.error(f"Error loading {filename}: {e}")
         return False
    
def load_all():
    """Load all files"""
    engine = get_engine()
    files = sorted(PROCESSED_DATA_PATH.glob("*.parquet"))
    logger.info(f"Found {len(files)} parquet files to load.")

    successful = 0
    failed = 0

    for parquet_path in files:
        result = load_file(parquet_path, engine)
        if result:
            successful += 1
        else:
            failed += 1

    logger.info(f"Finished loading. Successful: {successful}, Failed: {failed}")

if __name__ == "__main__":
    load_all()
        
 