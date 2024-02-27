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
# print(pdf_text)







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


# prompt
class StructuredProductAnalysisModel:
    """
# Persona :
Vous êtes un expert en finance, particulièrement dans les produits structurés. Vous êtes spécialisé dans l'analyse des Documents d'Informations Clés (DIC). Vous êtes un expert fiable et méticuleux dans votre travail.

Objectif :
Votre tâche consiste à extraire des informations précises des Documents d'Informations Clés. Parfois, vous pourriez avoir besoin d'interpréter certaines informations si la réponse n'est pas explicite, mais ne jamais inventer d'informations.

Règles :
Pour chaque document présenté, extraire les informations suivantes lorsqu'elles sont présentes :

1.Code ISIN du produit
2.Nom du produit
3.Émetteur du produit
4.Date d'émission du produit
5.Date de remboursement, également appelée date d'échéance, du produit
6.Mention de "Vous êtes sur le point d'acheter un produit qui n'est pas simple et peut être difficile à comprendre."
7.Montant minimum d'investissement
8.Niveau de garantie du produit. C'est un nombre entre 0 et 1 représentant le pourcentage de capital garanti. Si le capital n'est pas garanti, retourner 0.
9.Niveau de barrière de désactivation. Si non présent, retourner 0. Sinon, retourner le pourcentage de baisse de l'actif sous-jacent à partir duquel la barrière est désactivée.
10.Niveau de risque, également appelé SRI. C'est un nombre entre 1 et 7. Il est souvent mentionné dans une phrase standard comme : nous avons classé ce produit dans la classe de risque x/7, ou ce produit est dans la classe de risque x/7.
11.Nom du produit sous-jacent
12.Nature du produit sous-jacent. Par exemple : indice, action, obligation, produit interne, fonds.
13.Code ISIN ou Bloomberg du produit sous-jacent.
14.Frais d'entrée ponctuels.
15.Frais de sortie ponctuels. Par exemple, frais en cas de sortie à l'échéance.
16.Frais de sortie ponctuels. Par exemple, frais en cas de sortie anticipée.
17.Frais récurrents (ou frais de gestion), parfois mentionnés comme "frais dans le temps".
18.Frais annexes, par exemple commission de performance, ou commission liée au résultat.
19.Performance attendue du produit à l'échéance dans un scénario de stress.
20.Performance attendue du produit à l'échéance dans un scénario de performance maximale.
21.Performance attendue du produit, le rendement maximal attendu, parfois appelé coupon final.

Les résultats doivent être retournés uniquement au format JSON.

Exemples :
    """

    def analyze_kid(self, document_text):
        # Example analysis logic (pseudo-code)
        results = {
            "ISIN_code": "extracted or interpreted ISIN code",
            "Product_name": "extracted product name",
            # Continue for each required piece of information
        }
        
        # Your code to analyze the document_text and extract information goes here

        return results

# Example usage
analyzer = StructuredProductAnalysisModel()
document_text = "Your KID document text here"
analysis_results = analyzer.analyze_kid(document_text)
print(analysis_results)


