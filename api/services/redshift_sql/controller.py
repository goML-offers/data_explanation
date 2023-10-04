import json
from services.redshift_sql.chatgpt import ChatGPT
from services.redshift_sql.redshift_sql_connector import AWSRedshift
import configparser
import os
from dotenv import load_dotenv
load_dotenv()
# Read the config file
config = configparser.ConfigParser()
config.read("config.ini")

# Access the config values
dbname= os.getenv('dbname')
host=os.getenv('host')
port=os.getenv('port')
user=os.getenv('user')
password= os.getenv('password')
database=os.getenv('dbname')
openai_api_key = os.getenv('OPEN_API_KEY')
# openai_org = config.get("openai", "org")
# openai_model = config.get("openai", "model")
 

class Controller:

    def __init__(self):
        # initialise all the things
        self.redshift_sql = AWSRedshift( host, database, user, password)
        self.redshift_sql.connect()
        self.chatModel = ChatGPT(openai_api_key)

    def run(self, message, sender, counter=0):
        if (counter > 4):
            print(1)
            return 'error: too many requests'
        responseString = self.chatModel.message(message, sender)
        try:
            print(2)
            response = json.loads(responseString[:-1] if responseString.endswith('.') else responseString)
        except ValueError:
            print(3)
            return self.run("Please repeat that answer but use valid JSON only.", "SYSTEM", counter + 1)
        match response["recipient"]:
            case "USER": 
                print(4)
                return response["message"]
            case "SERVER":
                print(5)
                match response["action"]:
                    case "QUERY":
                        print(6)
                        result = self.redshift_sql.execute_query(response["message"])
                        return self.run(result, None, counter + 1)
                    case "SCHEMA":
                        print(7)
                        result = self.redshift_sql.execute_schema(response["message"])
                        return self.run(result, None, counter + 1)
                    case _:
                        print(8)
                        print('error invalid action')
                        print(response)
            case _:
                print('error, invalid recipient')
                print(response)


    def reset(self):
        self.chatModel.reset()
