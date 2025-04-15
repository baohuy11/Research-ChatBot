import torch
from transformers import BitsAndBytesConfig
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLLM
from langchain.llms.huggingface_pipeline import HuggingFacePipeline
from config.config import settings 

def summarizer_model():
    summarizer = pipeline("summarization", model=settings.SUMMARIZATION_MODEL)
    return summarizer

def tokenizer_model():
    tokenizer = AutoTokenizer.from_pretrained(settings.SUMMARIZATION_MODEL)
    return tokenizer

nf4_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
)

def get_hf_llm(model_name: str = "meta-llama/Llama-3.2-3B-Instruct",
                  max_new_tokens: int = 1024,
                  **kwargs) -> HuggingFacePipeline:
    
    model = AutoModelForCausalLLM.from_pretrained(
        model_name,
        quantization_config=nf4_config,
        low_cpu_mem_usage=True,
    )    
    
    tokeinzer = AutoTokenizer.from_pretrained(model_name)
    
    model_pipeline = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokeinzer,
        max_new_tokens=max_new_tokens,
        pad_token_id=tokeinzer.eos_token_id,
        device_map="auto",
    )
    
    llm = HuggingFacePipeline(
        pipeline=model_pipeline,
        model_kwargs=kwargs,
    )
    
    return llm