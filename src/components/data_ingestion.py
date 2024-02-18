import fitz  # PyMuPDF
import pdfplumber
import pandas as pd
from PIL import Image
import io
import os
import json
import base64



def save_image(image_bytes, images_path, img_index):
    """
    Save an image to the specified path.
    """
    image_path = f"{images_path}/image_{img_index}.png"
    with open(image_path, "wb") as img_file:
        img_file.write(image_bytes)
    return image_path

def extract_text_images(uploaded_file, images_path):
    """
    Extract text and images from a PDF uploaded as a BytesIO object.
    """
    text = ""
    image_paths = []
    # Open the PDF from the BytesIO object
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            # Extract text
            page_text = page.get_text().replace('\n', ' ').strip()
            text += page_text + " "
            
            # Extract images and save them
            for img_index, img in enumerate(page.get_images(full=True)):
                base_image = doc.extract_image(img[0])
                image_bytes = base_image["image"]
                # Save and track the image
                image_path = save_image(image_bytes, images_path, img_index + len(image_paths))
                image_paths.append(image_path)
                
    return text, image_paths

def extract_tables(pdf_path):
    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            for table in page.extract_tables():
                df = pd.DataFrame(table[1:], columns=table[0])
                tables.append(df.to_dict('records'))  # Convert each table to a list of dictionaries
    return tables

def create_directories(base_dir='scraped_data', images_dir='images'):
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    images_path = os.path.join(base_dir, images_dir)
    if not os.path.exists(images_path):
        os.makedirs(images_path)
    return base_dir, images_path

def save_text_to_file(text, base_dir, filename='extracted_text.txt'):
    filepath = os.path.join(base_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(text)
    print(f"Text saved to {filepath}")
    
def save_tables(tables, base_dir, filename='extracted_tables.xlsx'):
    # Ensure the directory exists
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    
    filepath = os.path.join(base_dir, filename)
    
    # Save tables to an Excel file with each table in a separate sheet
    with pd.ExcelWriter(filepath) as writer:
        for i, table_data in enumerate(tables):
            # Ensure table_data is a DataFrame
            if not isinstance(table_data, pd.DataFrame):
                table_data = pd.DataFrame(table_data)
            table_data.to_excel(writer, sheet_name=f'Table_{i}')
    print(f"Tables saved to {filepath}")

def save_data_as_json(text, image_paths, tables, base_dir, filename='scraped_data.json'):
    data = {
        'text': text,
        'image_paths': image_paths,
        'tables': tables
    }
    with open(os.path.join(base_dir, filename), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Data saved to {os.path.join(base_dir, filename)}")

