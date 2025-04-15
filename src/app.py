import os 
os.environ["TOKENIZERS_PARALLELIM"] = "false"

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from langserve import add_routes

from src.core.model import get_hf_llm
from src.core.main import build_rag_chain, InputQA, OutputQA

llm = get_hf_llm(temperature=0.9)

genai_doc = "./data/papers_pdf"

genai_chain= build_rag_chain(
    llm,
    data_dir=genai_doc,
    data_type="pdf"
)

#  ---------------------- Chains ---------------------- 
app = FastAPI(
    title="LangChain Server",
    description="GenAI is a generative AI model for document understanding and question answering.",
    version="0.1.0",
)

#  ---------------------- App - FastAPI ----------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

#  ---------------------- Routes - FastAPI ----------------------
@app.get("/check")
async def check():
    return {"status": "ok"}

@app.post("/rag", response_model=OutputQA)
async def rag(input: InputQA):
    """RAG Chain"""
    answer = genai_chain.invoke(input.question)
    return {"answer": answer}

#  ---------------------- LangServe - FastAPI ----------------------
add_routes(app, 
           genai_chain,
           playground_type="default",
           path="/rag",)