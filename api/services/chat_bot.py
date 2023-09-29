from pandas import DataFrame
import requests
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

OPEN_API_KEY = os.getenv('OPEN_API_KEY')

def analyze_dataframe(df: pd.DataFrame, question: str) -> str:
    # Round floating-point columns to a reasonable number of decimal places (e.g., 6)
    df = df.round(6)

    # Convert all DataFrame columns to strings
    df = df.astype(str)

    # Create an instance of the OpenAI API
    llm = OpenAI(api_token=os.getenv('OPEN_API_KEY'))

    # Create an instance of PandasAI
    pandas_ai = PandasAI (llm, conversational=False)
    
    # Ask a question about the DataFrame
    response = pandas_ai(df, question+",strictly only give me answer as text")
   
    return response