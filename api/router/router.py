import sys
from fastapi import FastAPI, File,  UploadFile
from fastapi import APIRouter, HTTPException, Response
from services.redshift import create_and_insert_table
from services.chat_bot import analyze_dataframe
from services.csv_to_redshift import export_redshift_table_to_dataframe
from services.summary_gen import summary_generation
import os
from fastapi.responses import JSONResponse
import json
from dotenv import load_dotenv
load_dotenv()


router = APIRouter()
@router.post('/goml/LLM marketplace/data summary and query/upload_file', status_code=201)
def data_generator(file: UploadFile):
    try:
        UPLOAD_DIR = "/api/uploads"

        if not os.path.exists(UPLOAD_DIR):
            os.makedirs(UPLOAD_DIR)
        # Generate a unique file name to avoid overwriting existing files
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        
        with open(file_path, "wb") as f:
            f.write(file.file.read())
            f.close()
        
        data_loc = create_and_insert_table(file_path)
    
        os.remove(file_path)
        return data_loc
    except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
   
@router.post('/goml/LLM marketplace/data summary and query/summary_generator', status_code=201)
async def accuracy_generator(table_name: str):
    try:
        dataframe = export_redshift_table_to_dataframe(table_name)
        

        summary  = summary_generation(dataframe)
        print(summary)
  
        return summary
    except Exception as e:
            
            raise HTTPException(status_code=400, detail=str(e))
            return 


@router.post('/goml/LLM marketplace/data summary and query/chatbot/', status_code=201)
def validating_test(query: str, table_name: str):
    try:
        
        dataframe = export_redshift_table_to_dataframe(table_name)
        data_loc = analyze_dataframe(dataframe,query)
    
        return data_loc
    except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

