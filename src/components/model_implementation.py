from transformers import AutoTokenizer, AutoModelForCausalLM 
from langchain.llms.huggingface_pipeline import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from transformers import pipeline
import torch

def load_llm_and_prompt():
        
    tokenizer = AutoTokenizer.from_pretrained("Universal-NER/UniNER-7B-all")
    model = AutoModelForCausalLM.from_pretrained("Universal-NER/UniNER-7B-all")
    
    ner_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer,max_length=1000,trust_remote_code=True,
        device_map="auto",
        do_sample=True,
        torch_dtype=torch.bfloat16,
        top_k=10,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,)
    llm = HuggingFacePipeline(pipeline = ner_pipeline, model_kwargs = {'temperature':0})


    prompt_template = """A virtual assistant answers questions from a user based on the provided text.
    USER: Text: {input_text}
    ASSISTANT: I’ve read this text.
    USER: What describes {entity_name} in the text?
    ASSISTANT:
    """
    # Create a prompt using the template
    prompt = PromptTemplate(
        input_variables=["input_text", "entity_name"],
        template=prompt_template
    )

    return llm , prompt


