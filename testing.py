
import openai

from fastapi import FastAPI, HTTPException, Depends

from pydantic import BaseModel

import json

import os 

from fastapi.middleware.cors import CORSMiddleware

# Functions



def get_response(prompt):

    '''

    Get the ChatGPT response for a given prompt using the provided API key.

    '''

    api_key="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"

    completion = openai.ChatCompletion.create(

    model='gpt-3.5-turbo',

    messages=[{'role': 'user', 'content': prompt}],

    temperature=0.2,

    api_key=api_key

    )



    return completion['choices'][0]['message']['content']





# FastAPI Application



app = FastAPI()

app.add_middleware(



    CORSMiddleware,



    allow_origins=["*"],



    allow_credentials=True,



    allow_methods=["GET", "OPTIONS", "POST", "PUT", "DELETE"],



    allow_headers=["*"],



)

class InputData(BaseModel):

    code: str





@app.post("/process_code/")

async def process_code(code: str):

    '''

    Process the provided code using ChatGPT.

    '''
    print(code)
    if not code:

        raise HTTPException(status_code=400, detail="Code not provided in the request")



    prompt = text + code

    response = get_response(prompt)

    exp_response =get_response(response.code+explanation_prompt)
    print(response,exp_response)
    return {'code':response,

    'exp':exp_response}





# Constants



text = '''

Please refactor the provided Python code snippet to incorporate the following changes:



1. Properly add comments to explain the code when needed.

2. Follow naming conventions for variables and functions and function parameters.

3. Add appropriate type annotations to function parameters and return types.

4. Include docstrings for functions.

5. Organize imports in a clean and orderly manner and remove unnecessary modules.

6. Remove any unnecessary extra lines and spaces.

7. Use f-strings wherever required

Don't explain the changes made

Below is the code snippet:



'''

explanation_prompt="Explain the changes made in the above code"




if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)