import sys

def trace_function(frame, event, arg):
    print(f"Tracing {frame.f_code.co_filename}, event: {event}, line: {frame.f_lineno}")
    return trace_function

sys.settrace(trace_function)

from typing import Any
import os
from unstructured.partition.pdf import partition_pdf
import pytesseract
import base64

pytesseract.pytesseract.tesseract_cmd = r'/user/local/bin/tesseract'


input_path = os.getcwd() + "/input"
output_path = os.path.join(os.getcwd(), "images")

raw_pdf_elements = partition_pdf(
    filename=os.path.join(input_path, "CE2254EVK-a87a3-FR.pdf"),
    extract_images_in_pdf=False,
    infer_table_structure=True,
    chunking_strategy="by_title",
    max_characters=4000,
    new_after_n_chars=3800,
    combine_text_under_n_chars=2000,
    image_output_dir_path=output_path,
)


text_elements = []
table_elements = []

# image_elements = []

# # Function to encode images
# def encode_image(image_path):
#     with open(image_path, "rb") as image_file:
#         return base64.b64encode(image_file.read()).decode('utf-8')

for element in raw_pdf_elements:
    if 'CompositeElement' in str(type(element)):
        text_elements.append(element)
    elif 'Table' in str(type(element)):
        table_elements.append(element)

table_elements = [i.text for i in table_elements]
text_elements = [i.text for i in text_elements]

print("Text elements and table elements")
print(text_elements)
print(table_elements)

print("Length of text and table elements")
print(len(table_elements))
print(len(text_elements))
