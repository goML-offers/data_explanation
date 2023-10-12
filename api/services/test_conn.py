# import psycopg2
# import os
# from dotenv import load_dotenv
# load_dotenv()

# def get_table_metadata(database_name, schema_name):
#     try:
#         # Connect to the Redshift cluster
#         conn = psycopg2.connect(
#             dbname=os.getenv('dbname'),
#             host=os.getenv('host'),
#             port=os.getenv('port'),
#             user=os.getenv('user'),
#             password=os.getenv('password')
#         )

#         # Create a cursor to execute SQL queries
#         cur = conn.cursor()

#         # SQL query to retrieve table metadata, primary keys, and foreign keys
#         query = f"""
#             SELECT 
#                 t.table_name, 
#                 c.column_name, 
#                 c.data_type,
#                 CASE WHEN pk.constraint_type = 'PRIMARY KEY' THEN 'PRIMARY KEY' ELSE '' END AS key_type,
#                 CASE WHEN fk.constraint_type = 'FOREIGN KEY' THEN fk.table_name ELSE '' END AS foreign_key_table
#             FROM 
#                 information_schema.columns c
#                 JOIN information_schema.tables t
#                     ON c.table_name = t.table_name
#                     AND c.table_schema = t.table_schema
#                 LEFT JOIN (
#                     SELECT
#                         kcu.table_name,
#                         tc.constraint_type
#                     FROM 
#                         information_schema.key_column_usage kcu
#                         JOIN information_schema.table_constraints tc
#                             ON kcu.constraint_name = tc.constraint_name
#                             AND kcu.table_name = tc.table_name
#                     WHERE 
#                         tc.constraint_type = 'PRIMARY KEY'
#                         AND kcu.table_schema = '{schema_name}'
#                 ) pk
#                 ON t.table_name = pk.table_name
#                 LEFT JOIN (
#                     SELECT
#                         kcu.table_name,
#                         tc.constraint_type
#                     FROM 
#                         information_schema.key_column_usage kcu
#                         JOIN information_schema.table_constraints tc
#                             ON kcu.constraint_name = tc.constraint_name
#                             AND kcu.table_name = tc.table_name
#                     WHERE 
#                         tc.constraint_type = 'FOREIGN KEY'
#                         AND kcu.table_schema = '{schema_name}'
#                 ) fk
#                 ON t.table_name = fk.table_name
#             WHERE 
#                 c.table_schema = '{schema_name}'
#         """

#         # Execute the query
#         cur.execute(query)

#         # Fetch all the rows
#         rows = cur.fetchall()

#         # Close the cursor and connection
#         cur.close()
#         conn.close()

#         # Organize the results
#         table_metadata = {}
#         for row in rows:
#             table_name, column_name, data_type, key_type, foreign_key_table = row
#             if table_name not in table_metadata:
#                 table_metadata[table_name] = {'columns': [], 'primary_keys': [], 'foreign_keys': []}

#             if key_type == 'PRIMARY KEY':
#                 table_metadata[table_name]['primary_keys'].append(column_name)

#             if foreign_key_table:
#                 table_metadata[table_name]['foreign_keys'].append((column_name, foreign_key_table))

#             table_metadata[table_name]['columns'].append((column_name, data_type))

#         return table_metadata

#     except Exception as e:
#         print(f"An error occurred: {str(e)}")
#         return None

# # Example usage
# database_name = 'dev'
# schema_name = 'public'  # Replace with your schema name
# table_metadata = get_table_metadata(database_name, schema_name)

# # Print the metadata for each table
# if table_metadata:
#     for table, metadata in table_metadata.items():
#         print(f"Table: {table}")
#         print("  - Entire Row:")
#         for row in metadata['columns']:
#             print(f"    - {row}")

import psycopg2
from psycopg2 import OperationalError
import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

def check_redshift_connection():
    try:
        # Establish a connection to the Redshift cluster
        conn = psycopg2.connect(
        dbname=redshift_params['dbname'],
        user=redshift_params['user'],
        password=redshift_params['password'],
        host=redshift_params['host'],
        port=redshift_params['port']
    )

        # Close the connection
        conn.close()

        return True

    except OperationalError as e:
        print(f"Connection failed: {e}")
        return False

# Example usage
redshift_params = {
        'dbname':  os.getenv('dbname'),
        'user':  os.getenv('user'),
        'password':  os.getenv('password'),
        'host':  os.getenv('host'),
        'port':  os.getenv('port')
    }

is_connected = check_redshift_connection()

# print(f"Connection status: {is_connected}")