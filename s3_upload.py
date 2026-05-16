import boto3
import os 
from dealer import DATA_TABLES
from dotenv import load_dotenv


load_dotenv()


S3_BUCKET = os.getenv('S3_BUCKET') #s3 location
s3 = boto3.client('s3') #s3 engine


def upload_to_s3(file_dir: str, tbl_name: str) -> None:

    src  = os.path.join(file_dir, f'{tbl_name}') # folder_name/table_name.csv
    s3_key = f'raw/{tbl_name}' # Save location on s3

    if not os.path.exists(src):
        raise FileNotFoundError(f'The file: {tbl_name} does not exist at the {file_dir} location.')
    
    s3.upload_file(src, S3_BUCKET, s3_key)
    print(f'{tbl_name} has successfully been uploaded to s3://{S3_BUCKET}/{s3_key}')


for each in os.listdir(DATA_TABLES):
    upload_to_s3(DATA_TABLES, each)
    
