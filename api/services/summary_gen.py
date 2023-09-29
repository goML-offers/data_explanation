import openai
import csv
from dotenv import load_dotenv
import os
import pandas as pd
# Load environment variables from .env file
load_dotenv()

OPEN_API_KEY = os.getenv('OPEN_API_KEY')

# Set your OpenAI API key
openai.api_key = OPEN_API_KEY
# #Function to load and preprocess the dataset
# def load_and_preprocess_dataset(file_path):
#     try:
#         # Read the data into a pandas DataFrame
#         data_df = pd.read_csv(file_path)

#         # Extract only the first 5 rows
#         data_df = data_df.head(5)

#         return data_df
#     except Exception as e:
#         return str(e)


# Load and preprocess the dataset


def summary_generation(file_path):
    # Generate a detailed description of the CSV file using OpenAI's GPT-3 model
    print(file_path)
    print("\n",file_path.head(5))
    # data_text = load_and_preprocess_dataset(file_path)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": """You are an AI assistant, Assume the role of a business analyst who has a good knowledge of data science and data analysis.
            You'll receive a CSV or Excel file. Examine its column headers and the content of the first five rows, 
            presented as a data frame's head. Your task is to understand the dataset's business context and provide
            a brief description, without delving into technical details like data types. Instead, focus on its 
            business implications. For instance, if columns include 'Name', 'Birthday', 'Sex', and 'Hospital', 
            your interpretation might be: "The dataset contains birth records of children from hospitals in a 
            specific region." Your description should be text-based and only 150 words.
            Try and categorize them under a specific function in an industry. Below are the outputs that you 
            need to generate. For industry, pick one of the industried recognized by Global Industry Classification Standard (GICS)
            For function, choose one of the following functions that's most appropriate - Sales, Marketing, Operations, Delivery,
            HR, Finance, Accounting, Legal, Compliance, Supply Chain, Project Delivery, Business Development
            Industry:
            Function:
            Category:
            Description:"""},
            {"role": "user", "content": f"{file_path.head()}"}
        ]
    )

    # Extract the description from the response
    description = response['choices'][0]['message']['content']

    # Print the detailed description to the console
    return description