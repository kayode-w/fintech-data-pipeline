import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from datetime import datetime, timedelta

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
S3_BUCKET = os.getenv('S3_BUCKET')

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")


def load_sql(df: pd.DataFrame, tbl_name: str, engine):

    try:
        start_time = datetime.now()
        
        print(f'Begining load of {tbl_name} into postgres...')
        df.to_sql(tbl_name, con=engine, if_exists='replace', index=False)
        end_time = datetime.now()

        duration = end_time - start_time

        print(f'{tbl_name} loaded in {duration.seconds // 60}:{duration.seconds} seconds')
        
    except Exception as e:
        raise Exception(f'An error occurred while loading the table {tbl_name}... : {str(e)}')
