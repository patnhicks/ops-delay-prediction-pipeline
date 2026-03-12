from etl.transform import process_file
from pathlib import Path

process_file(Path('data/raw/OTP_2019_01.zip'))
