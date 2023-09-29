import psycopg2
from dotenv import load_dotenv
import os
import pandas as pd

# Load environment variables from .env file
load_dotenv()

def export_redshift_table_to_dataframe(table_name):
    # Load Redshift parameters from environment variables
    print(table_name)
    redshift_params = {
        'dbname': os.getenv('dbname'),
        'user': os.getenv('user'),
        'password': os.getenv('password'),
        'host': os.getenv('host'),
        'port': int(os.getenv('port'))
    }

    # Create a connection to Redshift
    conn = psycopg2.connect(
        dbname=redshift_params['dbname'],
        user=redshift_params['user'],
        password=redshift_params['password'],
        host=redshift_params['host'],
        port=redshift_params['port']
    )

    # Create a cursor to execute SQL statements
    cur = conn.cursor()

    # Execute a SELECT query to fetch data from the table
    select_query = f"SELECT * FROM {table_name}"
    cur.execute(select_query)

    # Fetch all rows from the result
    rows = cur.fetchall()

    # Get the column names from the cursor description
    col_names = [desc[0] for desc in cur.description]

    # Create a DataFrame from the fetched rows and column names
    df = pd.DataFrame(rows, columns=col_names)

    # Commit the SQL transaction
    conn.commit()

    # Close the cursor and connection
    cur.close()
    conn.close()

    return df

# Usage example
