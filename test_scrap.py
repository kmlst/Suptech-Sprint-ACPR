import fitz 
import os

os.getcwd()

def read_pdf(pdf_path):
    # Open the provided PDF file
    doc = fitz.open(pdf_path)
    
    # Initialize a text variable to store all the extracted text
    full_text = ""
    
    # Iterate through each page in the PDF
    for page in doc:
        # Extract text from the current page
        text = page.get_text()
        
        # Append the extracted text to the full_text variable
        full_text += text + "\n"  # Add a newline character for readability
    
    # Close the PDF document
    doc.close()
    
    return full_text

# Define the path to the PDF file
pdf_path = os.getcwd() + "/input/CE2421EVK-c33ce-FR.pdf"

# Call the function and print the result
pdf_text = read_pdf(pdf_path)
print(pdf_text)


## Appel api

import os
from openai import AzureOpenAI


client = AzureOpenAI(
  azure_endpoint = "https://francecentral-openai.openai.azure.com/", 
  api_key="7e93421f46cd4680831023addcb0f42d",  
  api_version="2024-02-15-preview"
)


message_text = [{"role":"system","content":"You are an AI assistant that helps people find information."},{"role":"user","content":"give me the recipe for crepes"}]


completion = client.chat.completions.create(
  model="gpt-35-turbo", 
  messages = message_text,
  temperature=0.7,
  max_tokens=800,
  top_p=0.95,
  frequency_penalty=0,
  presence_penalty=0,
  stop=None
)

print(completion)