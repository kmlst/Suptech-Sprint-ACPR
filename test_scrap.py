import fitz 
import os
import json
from openai import AzureOpenAI
from config import prompt_example, columns_to_use
import pandas as pd


# va partir -----------------
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
    message_text = [{"role":"system","content":prompt_example},{"role":"user","content":treated_pdf}]
    response = client.chat.completions.create(
    model="gpt-35-turbo", 
    messages = message_text,
    temperature=0.,
    max_tokens=400,
    top_p=0.,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None
    )

    response_str = response.choices[0].message.content 
    # response_str is a string containing the JSON response from the API
    # we want to extract the JSON from the string and convert it to a dictionary
    response_str = response_str.replace("```", '') # cleaning
    response_str = response_str.replace('json', '') # cleaning
    response_str = response_str.replace('\n', '') # cleaning

    result = json.loads(response_str)
    
    result = pd.DataFrame(result, index=[0])
    result["date_actualisation"] = pd.to_datetime("today").strftime("%Y-%m-%d")

    #check if the csv file exists and if not create it
    if os.listdir("output") == []:
            data = pd.DataFrame(columns=columns_to_use)
    else:
        data = pd.read_csv("output/bdd_DIC.csv")
        
    # save the result in the csv file of the output folder
    if result["code_ISIN"] in data['code_ISIN'].values:
        print(f"Le document avec l'ISIN {result['code_ISIN']} déjà été traité")
    else:
        # Add the result to the DataFrame without using append
        data = data.append(result, ignore_index=True)
        # save the result in the csv file of the output folders
        data.to_csv("output/bdd_DIC.csv", index=False)

# now we want to read all the pdf files in the input folder and extract the information from them

print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
print("EXEMPLES INCOMPLETS DANS LES DOSSIERS : 20 features seulement, il faut corriger les json mis en examples")
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")

 # ---------- MAIN ---------------------------
# list all the files in the input folder and extract the information from them
def main():
    files = os.listdir("input")
    for file in files:
        pdf_path = os.getcwd() + f"/input/{file}"
        extract_information(pdf_path)

if __name__== '__main__':
    # Run the whole process
    main()

