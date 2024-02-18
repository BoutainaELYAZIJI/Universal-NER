from src.components.data_ingestion import *
import streamlit as st
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter
from src.components.model_implementation import load_llm_and_prompt
from langchain.chains import LLMChain

# Load your JSON data

def load_json_text():
    with open('./scraped_data/scraped_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    text = data['text']  # Assuming the key for your text in JSON is 'text'
    return text

def main():
    st.header("Universal-NER PDF Analysis 💬")
    pdf = st.file_uploader("Upload your PDF", type='pdf')
    entity_type = st.text_input("Enter the entity type you're interested in (e.g., 'Person', 'Location'):")

    if pdf is not None and entity_type:
        base_dir, images_path = create_directories()

        text, images = extract_text_images(pdf, images_path)

        tables = extract_tables(pdf)

        save_data_as_json(text, images_path, tables, base_dir)

        # Optionally display some results
        st.text_area("Extracted Text", text, height=300)

        text = load_json_text()
        text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap  = 32,
        length_function = len,
        )
        texts = text_splitter.split_text(text)
        # Load llm and prompt
        llm, prompt = load_llm_and_prompt()

        # Initialize LLMChain with the loaded llm and prompt
        llm_chain = LLMChain(prompt=prompt, llm=llm)

        # Initialize a variable to store the whole result
        whole_result = []

        for i, chunk_text in enumerate(texts, start=1):
            result = llm_chain.run({"input_text": chunk_text, "entity_name": entity_type})
            
            st.write(f"Chunk {i} result:", result)

            # Append the result of the current chunk to the whole result
            whole_result.append(result)

        # display the whole  result at the end
        st.write("Whole compiled result:")
        st.write(whole_result)



if __name__ == "__main__":
    main()
