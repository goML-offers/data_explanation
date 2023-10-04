import psycopg2
import csv
import logging
import os
from datetime import date, timedelta
from dotenv import load_dotenv
load_dotenv()
from io import StringIO

class AWSRedshift:

    def __init__(self, host, database, user, password, port='5439'):
        self.host = os.getenv('host')
        self.database = os.getenv("dbname")
        self.user = os.getenv("user")
        self.password = os.getenv("password")
        self.port = os.getenv("port")

    def connect(self):
        try:
            print("aws1")
            self.conn = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )
            return True
        except Exception as e:
            return str(e)

    def close(self):
        self.conn.close()

    def execute_query(self, query):
        print(f'\033[94mExecuting Query: {query}\033[0m')
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )
            print("aws main")
            cursor = self.conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            if len(result) == 0:
                result = "0 rows returned"
                logging.debug(result)
                print(f'\033[96m{result}\033[0m')
                return result

            headers = [desc[0] for desc in cursor.description]
            output = StringIO()
            csv_writer = csv.writer(output)
            csv_writer.writerow(headers)
            csv_writer.writerows(result)
            result = output.getvalue()
            logging.debug(result)
            print(f'\033[96m{result}\033[0m')
            return result
        except Exception as e:
            print("Error:", e)
            return str(e)

    def process_table_string(self, input_str):
        print("aws3")
        items = input_str.split(',')
        items = [item.split('.')[-1] for item in items]
        formatted_str = "', '".join(items)
        result = f"'{formatted_str}'"
        return result

    def execute_schema(self, table_list):
        print("aws4")
        query_part = self.process_table_string(table_list)
        return f"SELECT 'Table: ' || table_schema || '.' || table_name || ', Column: ' || column_name || ', DataType: ' || data_type AS 'Table, Column, DataType' FROM information_schema.columns WHERE table_name IN ({query_part})"
