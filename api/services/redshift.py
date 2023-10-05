import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from datetime import datetime
import os
import boto3
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

bucket_name= os.getenv('bucket_name')
redshift_params = {
        'dbname':  os.getenv('dbname'),
        'user':  os.getenv('user'),
        'password':  os.getenv('password'),
        'host':  os.getenv('host'),
        'port':  os.getenv('port')
    }
aws_access_key =  os.getenv('aws_access_key')
aws_secret_key =  os.getenv('aws_secret_key')

# def upload_to_s3(csv_file_path, table_name):
#     # Initialize AWS S3 client
#     s3 = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
#     # Extract file name from CSV file path
#     file_name = os.path.basename(csv_file_path)

#     # Specify the S3 folder path (inside 'redshift') using the table name
#     s3_folder_path = f'LLM-reshift/{table_name}.csv'

#     # Upload the CSV file to S3
#     try:
#         s3.upload_file(csv_file_path, bucket_name, s3_folder_path)
#         print(f'File successfully uploaded to S3: s3://{bucket_name}/{s3_folder_path}')
#         s3_file_path = f's3://{bucket_name}/{s3_folder_path}'
#         return s3_file_path
#     except Exception as e:
#         print(f'Error uploading file to S3: {e}')

def create_and_insert_table(csv_file_path):
    # Extract table name from CSV file name, replace spaces with underscores
    table_name = os.path.splitext(os.path.basename(csv_file_path))[0]
    table_name = table_name.replace(' ', '_')
    # s3_file_path = upload_to_s3(csv_file_path, table_name)
    # Read the CSV file into a DataFrame
    dataframe = pd.read_csv(csv_file_path)

    # Create a connection to Redshift
    conn = psycopg2.connect(
        dbname=redshift_params['dbname'],
        user=redshift_params['user'],
        password=redshift_params['password'],
        host=redshift_params['host'],
        port=redshift_params['port']
    )
    # Create a cursor to execute SQL statements
    conn_string = f"postgresql://{redshift_params['user']}:{redshift_params['password']}@{redshift_params['host']}:{redshift_params['port']}/{redshift_params['dbname']}"

    # Create a Redshift engine using SQLAlchemy
    engine = create_engine(conn_string)
    cur = conn.cursor()
    table_name= table_name.lower()
    # Check if the table already exists
    table_exists_query = f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = '{table_name}');"
    cur.execute(table_exists_query)
    table_exists = cur.fetchone()[0]

    if table_exists:
        # Append data to the existing table
        dataframe.to_sql(table_name, engine, if_exists='append', index=False, schema='public')
        print(f'Data successfully appended to Amazon Redshift table: {table_name}')
    else:
        # Create a new table and insert data
        dataframe.to_sql(table_name, engine, if_exists='replace', index=False, schema='public')
        print(f'New table created and data successfully inserted into Amazon Redshift: {table_name}')

    return table_name
    # return {"database_name": table_name}
