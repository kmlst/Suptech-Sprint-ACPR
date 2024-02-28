import fitz 
import os
import json
from openai import AzureOpenAI
from config import prompt_example, columns_to_use, prompt_contrequalif
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
    max_tokens=1400,
    top_p=0.,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None
    )
    try :
        response_str = response.choices[0].message.content
    except :
        print("document corrompu", pdf_path)
        return None
    

    # response_str is a string containing the JSON response from the API
    # we want to extract the JSON from the string and convert it to a dictionary
    response_str = response_str.replace("```", '') # cleaning
    response_str = response_str.replace('json', '') # cleaning
    response_str = response_str.replace('\n', '') # cleaning

    result = json.loads(response_str)
    result["date_actualisation"] = pd.to_datetime("today").strftime("%Y-%m-%d")

    # add a counter qualificator of the result that re-reads the result 
    # and the text from the pdf to check if the result is correct
    # if not we mention the number of correctly extracted pieces of information

    # contrequalification

    # query = f"Here is the json file, {result} \n \n Here is the text from the pdf {treated_pdf}"
    # message_text = [{"role":"system","content":prompt_contrequalif},{"role":"user","content":query}]
    # response = client.chat.completions.create(
    # model="gpt-35-turbo", 
    # messages = message_text,
    # temperature=0.,
    # max_tokens=800,
    # top_p=0.,
    # frequency_penalty=0,
    # presence_penalty=0,
    # stop=None
    # )

    # print(response.choices[0].message.content)

    
    #check if the csv file exists and if not create it
    if "bdd_DIC.csv" not in os.listdir("output"):
            data = pd.DataFrame(columns=columns_to_use)
    else:
        data = pd.read_csv("output/bdd_DIC.csv")
        
    # save the result in the csv file of the output folder
    print(result["code_ISIN"])
    if result["code_ISIN"] in data['code_ISIN'].values:
        # print(f"Le document avec l'ISIN {result['code_ISIN']} déjà été traité")
        # check the date of the last update : more than 1 month we update the data
        last_update = data[data['code_ISIN'] == result['code_ISIN']]['date_actualisation'].values[0]
        if pd.to_datetime("today") - pd.to_datetime(last_update) > pd.Timedelta(30, unit='D'):
            print(f"Le document avec l'ISIN {result['code_ISIN']} n'a pas été actualisé depuis plus d'un mois, nous mettons à jour les données")
            data = data[data['code_ISIN'] != result['code_ISIN']]
            data = pd.concat([data, pd.DataFrame([result])], ignore_index=True, axis=0)
            data.to_csv("output/bdd_DIC.csv", index=False)

    else:
        # Add the result to the DataFrame without using append
        data = pd.concat([data, pd.DataFrame([result])], ignore_index=True, axis=0)
        # save the result in the csv file of the output folders
        data.to_csv("output/bdd_DIC.csv", index=False)

    


 # ---------- MAIN ---------------------------
# list all the files in the input folder and extract the information from them
def main():
    banques = ["Goldmann", "BNP", "Natixis", "SG"]
    for b in banques:
        i = 1
        files = os.listdir(f"input/{b}/")
        if i < 5:
            for file in files:
                pdf_path = os.getcwd() + f"/input/{b}/{file}"
                print(pdf_path)
                extract_information(pdf_path)
                i += 1
                if i > 5:
                    break


if __name__== '__main__':
    # Run the whole process
    main()

