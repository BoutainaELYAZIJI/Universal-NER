# Universal-NER PDF Analysis 

## Description

This Streamlit-based web application is designed to process PDF documents for Named Entity Recognition (NER) tasks. It allows users to upload PDF files, from which the application extracts text, images, and tables. The extracted text is then used to identify entities based on a user-specified entity type (e.g., 'Person', 'Location').

## Screenshots

<img  src="https://github.com/BoutainaELYAZIJI/Named-Entity-Recognition/Universal-NER PDF Analysis.png" >

## Features

- PDF Upload: Users can upload PDF documents to be processed.
- Entity Type Specification: Users can specify the type of entity they're looking for.
- Text Extraction: The application extracts and displays the text from the uploaded PDF.
- Image Extraction: Any images in the PDF are saved and can be displayed or further processed.
- Table Extraction: The application is capable of extracting tables from the PDF.
- Entity Recognition: The extracted text is processed to identify entities of interest.

## Installation

To set up the project, you need to have Python installed on your system. Follow these steps:

1. Clone the repository to your local machine.
2. Navigate to the project directory and install the required dependencies:
    ```sh
   pip install -r requirements.txt

3. ```sh
   streamlit run src/app.py
   



