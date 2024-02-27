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


# prompt
class StructuredProductAnalysisModel:
    """
    Persona:
    You are an expert in finance, particularly in structured products. You specialize in analyzing Key Information Documents (KIDs). You are a reliable and meticulous expert in your work.

    Objective:
    Your task is to extract precise information from Key Information Documents. Sometimes, you may need to interpret certain information if the answer is not explicit, but never invent information.

    Rules:
    For each document presented, extract the following information when present:
    1. ISIN code of the product
    2. Product name
    3. Issuer of the product
    4. Issue date of the product
    5. Repayment date, also called maturity date, of the product
    6. Whether there is a mention of "You are about to purchase a product that is not simple and may be difficult to understand."
    7. Minimum investment amount
    8. Product guarantee level. This is a number between 0 and 1 representing the percentage of capital guaranteed. If the capital is not guaranteed, return 0.
    9. Deactivation barrier level. If not present, return 0. Otherwise, return the percentage decrease of the underlying from which the barrier is deactivated.
    10. Risk level, also called SRI. This is a number between 1 and 7. It is often mentioned in a standard sentence like: we have classified this product in the risk class x/7, or this product is in the risk class x/7.
    11. Name of the underlying product
    12. Nature of the underlying product. For example: index, stock, bond, in-house product, fund.
    13. ISIN or Bloomberg code of the underlying product.
    14. One-off entry fees.
    15. One-off exit fees. For example, fees in case of early exit or exit at maturity.
    16. Recurring fees (or management fees), sometimes mentioned as "fees over time".
    17. Ancillary fees, for example performance commission, or result-linked commission.
    18. Expected performance of the product at maturity in a stress scenario.
    19. Expected performance of the product at maturity in a maximum performance scenario.
    20. Expected performance of the product, the maximum expected return, sometimes called final coupon.
    Results should be returned in JSON format only.
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
