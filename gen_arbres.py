import os
import sys

# pdf_path = os.getcwd() + f"/input/CE2254EVK-a87a3-FR.pdf"
from main import read_pdf
import json
from openai import AzureOpenAI
import pandas as pd

from prompts import prompt_arbres

def extract_information(pdf_path):
    # Call the function and print the result
    treated_pdf = read_pdf(pdf_path)

    ## Appel api
    client = AzureOpenAI(
    azure_endpoint = "https://francecentral-openai.openai.azure.com/", 
    api_key="7e93421f46cd4680831023addcb0f42d",  
    api_version="2024-02-15-preview"
    )

    # the system context is contained in config.py in the variable prompt_example
    message_text = [{"role":"system","content":"You are a specialist in finance and Python expert on decision trees."},{"role":"user","content":prompt_arbres + treated_pdf}]
    response = client.chat.completions.create(
    model="gpt-35-turbo", 
    messages = message_text,
    temperature=0.5,
    max_tokens=500,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None
    )
    response_str = response.choices[0].message.content
    return response_str

if __name__ == '__main__':
    pdf_path = 'input/' + sys.argv[1]
    code_path = sys.argv[1][:-4] + '.py'
    code_path = code_path.replace('/', '_')
    code_path = code_path.replace(' ', '')
    gen_code = extract_information(pdf_path)[9:-4]
    with open(code_path, 'w') as f:
        f.write(gen_code)