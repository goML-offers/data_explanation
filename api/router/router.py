import sys
from typing import List
from pydantic import BaseModel
from fastapi import FastAPI, File,  UploadFile
from fastapi import APIRouter, HTTPException, Response
from services.redshift import create_and_insert_table
from services.redshift_sql.terminal import chat_bot
from services.csv_to_redshift import export_redshift_table_to_dataframe,get_all_table_names,get_table_schema
from services.summary_gen import summary_generation
import os
from fastapi.responses import JSONResponse
import json
from dotenv import load_dotenv
load_dotenv()


router = APIRouter()

class RedshiftCredentials(BaseModel):
    dbname: str
    user: str
    password: str
    host: str
    port: int

@router.post("/goml/LLM marketplace/data summary and query/redshift_credentials/")
async def update_redshift_credentials(credentials: RedshiftCredentials):
    try:
        print(credentials.__dict__)
        env_path = "api/.env"
        with open(env_path, "r") as env_file:
            lines = env_file.readlines()

        # Update the values or add them if they don't exist
        updated_lines = []
        for line in lines:
            key = line.split("=")[0].strip()
            if key in ["dbname", "user", "password", "host", "port"]:
                updated_lines.append(f"{key}={getattr(credentials, key)}\n")
            else:
                updated_lines.append(line)

        # Write the updated values back to the .env file
        with open(env_path, "w") as env_file:
            env_file.writelines(updated_lines)
            return True
    except Exception as e:
        return False

@router.post('/goml/LLM marketplace/data summary and query/upload_file', status_code=201)
def data_generator(files: List[UploadFile]):
    try:
        UPLOAD_DIR = "/api/uploads"

        if not os.path.exists(UPLOAD_DIR):
            os.makedirs(UPLOAD_DIR)

        data_locations = []

        for file in files:
            # Generate a unique file name to avoid overwriting existing files
            file_path = os.path.join(UPLOAD_DIR, file.filename)
            
            with open(file_path, "wb") as f:
                f.write(file.file.read())
            
            data_loc = create_and_insert_table(file_path)
            data_locations.append(data_loc)

            # Remove the file after processing
            os.remove(file_path)
        
        return data_locations
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
   
@router.post('/goml/LLM marketplace/data summary and query/summary_generator', status_code=201)
async def accuracy_generator(table_name: str):
    try:
        table_name = table_name.replace(' ', '_')
        dataframe = export_redshift_table_to_dataframe(table_name)
        

        summary  = summary_generation(dataframe)
        print(summary)
  
        return summary
    except Exception as e:
            
            raise HTTPException(status_code=400, detail=str(e))
            return 


@router.post('/goml/LLM marketplace/data summary and query/chatbot/', status_code=201)
def validating_test(query: str):
    try:
        
        data_loc = chat_bot(query)
    
        return data_loc
    except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

@router.post('/goml/LLM marketplace/data summary and query/view/', status_code=201)
def validating_test(table_name: str):
    try:
        table_name = table_name.replace(' ', '_')
        dataframe = export_redshift_table_to_dataframe(table_name)
        df_string = dataframe.to_csv()
        # print(type(df_string),df_string)
        return df_string
    except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

@router.get('/goml/LLM marketplace/data summary and query/table_list/', status_code=201)
def validating_test():
    try:
        
        dataframe = get_all_table_names()

        # print(type(df_string),df_string)
        return dataframe
    except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
@router.post('/goml/LLM marketplace/data summary and query/table_schema/', status_code=201)
def validating_test(table_names:str):
    try:
        # dataframe=[]
        # for table_name in table_names:
        schema = get_table_schema(table_names)
        # dataframe.append({table_name:schema})
        # print(type(df_string),df_string)
        return schema
    except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))