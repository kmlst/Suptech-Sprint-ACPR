import fitz 
import os
from openai import AzureOpenAI
from config import prompt_example
import pandas as pd

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


def extract_information(pdf_path):
    # Call the function and print the result
    treated_pdf = read_pdf(pdf_path)

    ## Appel api
    client = AzureOpenAI(
    azure_endpoint = "https://francecentral-openai.openai.azure.com/", 
    api_key="7e93421f46cd4680831023addcb0f42d",  # clef d'api sous forme plus safe...
    api_version="2024-02-15-preview"
    )

    # the system context is contained in config.py in the variable prompt_example
    message_text = [{"role":"system","content":prompt_example},{"role":"user","content":treated_pdf}]

    response = client.chat.completions.create(
    model="gpt-35-turbo", 
    messages = message_text,
    temperature=0.,
    max_tokens=800,
    top_p=0.,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None
    )

    response_str = response.choices[0].message.content 
    # output example 

    # {
    #   "code_ISIN": "XS2442385998",
    #   "nom_du_produit": "Calliandra Mai 2028",
    #   "emetteur_du_produit": "BNP Paribas Issuance B.V.",
    #   "date_emission": "2023-03-08",
    #   "date_remboursement": "2028-06-01",
    #   "mention_complexite": true,
    #   "montant_minimum_investissement": "Non spécifié",
    #   "niveau_garantie": 1,
    #   "niveau_barriere_desactivante": 100,
    #   "niveau_risque": 2,
    #   "produit_sous_jacent": "Indice EURO STOXX 50",
    #   "nature_sous_jacent": "indice",
    #   "code_ISIN_sous_jacent": "Non applicable",
    #   "frais_ponctuels_entree": "3.96%",
    #   "frais_ponctuels_sortie": "0.5% du montant nominal",
    #   "frais_recurrents": "0% de votre investissement par an",
    #   "frais_accessoires": "Aucune commission liée aux résultats n'existe pour ce produit",
    #   "performance_tension": "-13.01%",
    #   "performance_maximale": "4.67%",
    #   "espérance_maximale_rendement": "Non spécifié"
    # }

    # response_str is a string containing the JSON response from the API
    # we want to extract the JSON from the string and convert it to a dictionary
    response_str = response_str[8:-3]
    response_str = response_str.replace('{', '')
    response_str = response_str.replace('}', '')
    response_str = response_str.replace('\n', '')
    response_str = response_str.replace('\n ', '')
    response_str = response_str.replace(' \n', '')
    response_str = response_str.replace('  ', '')
    result = {}
    response_str = response_str.split(',')
    for text in response_str:
        ligne = text.split(": ")
        key, value = ligne[0].replace('"', ''), ligne[1].replace('"', '')
        result[key] = value

    #view the result
    # for i in result.keys():
    #     print(i, ":", result[i])

    # save the result in the csv file of the output folder

    # final version of the columns
    # true_columns = [
    #     "code_ISIN",
    #     "nom_du_produit",
    #     "emetteur_du_produit",
    #     "date_emission",
    #     "date_remboursement",
    #     "mention_complexite",
    #     "montant_minimum_investissement",
    #     "niveau_garantie",
    #     "niveau_barriere_desactivante",
    #     "niveau_risque",
    #     "produit_sous_jacent",
    #     "nature_sous_jacent",
    #     "code_ISIN_sous_jacent",
    #     "frais_ponctuels_entree",
    #     "frais_ponctuels_sortie_echeance",
    #     "frais_ponctuels_sortie_anticipée",
    #     "frais_recurrents",
    #     "frais_accessoires",
    #     "performance_tension",
    #     "performance_maximale",
    #     "espérance_maximale_rendement"
    # ]

    # meanwhile we will use the following columns
    columns = ["code_ISIN", "nom_du_produit", "emetteur_du_produit", "date_emission", "date_remboursement", "mention_complexite", "montant_minimum_investissement", "niveau_garantie", "niveau_barriere_desactivante", "niveau_risque", "produit_sous_jacent", "nature_sous_jacent", "code_ISIN_sous_jacent", "frais_ponctuels_entree", "frais_ponctuels_sortie", "frais_recurrents", "frais_accessoires", "performance_tension", "performance_maximale", "espérance_maximale_rendement"]

    if os.listdir("output") == []:
        data = pd.DataFrame(columns=columns)
    else:
        data = pd.read_csv("output/bdd_DIC.csv")


    if result['code_ISIN'] in data['code_ISIN'].values:
        print(f"Le document avec l'ISIN {result['code_ISIN']} déjà été traité")
    else:
        # result is a dictionary containing the extracted information
        # Add the result to the DataFrame without using append
        data = data.append(result, ignore_index=True)
        data.to_csv("output/bdd_DIC.csv", index=False)


# now we want to read all the pdf files in the input folder and extract the information from them


print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
print("EXEMPLES INCOMPLETS DANS LES DOSSIERS : 20 features seulement, il faut corriger les json mis en examples")
print("Rajouter un champs pour la date d'actualisation de traitement du document")
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")



files = os.listdir("input")
for file in files:
    pdf_path = os.getcwd() + f"/input/{file}"
    extract_information(pdf_path)