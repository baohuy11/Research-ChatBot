import os
import json
import time
from dotenv import load_dotenv
from pinecone import Pinecone as PineconeNonGRPC, ServerlessSpec
from pinecone.grpc import PineconeGRPC
from langchain_pinecone import PineconeVectorStore
from langchain_ollama import OllamaEmbeddings
from langchain.schema import Document

load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

# Initialize both GRPC and non-GRPC clients
pc_non_grpc = PineconeNonGRPC(api_key=PINECONE_API_KEY)
pc_grpc = PineconeGRPC(api_key=PINECONE_API_KEY)

index_name = "research_chatbot"

def load_data_from_local(filename: str, directory: str) -> tuple:
    file_path = os.path.join(directory, filename)
    with open(file_path, 'r') as file:
        data = json.load(file)
    print(f'Data load from {file_path}')
    return data, filename.rsplit('.', 1)[0].replace('_', ' ')

def vector_database_summarize(filename: str, directory: str, index_name: str) -> PineconeVectorStore:
    """Create/update Pinecone vector database from local data."""
    embeddings = OllamaEmbeddings(model='nomic-embed-text')
    
    local_data, _ = load_data_from_local(filename, directory)
    
    # Load and process data
    data, _ = load_data_from_local(filename, directory)
    documents = [
        Document(
            page_content=f"{entry['title']}: {entry['summary']}",
            metadata={k: v for k, v in entry.items() if k != "summary"}
        )
        for entry in data
    ]
    
    # Create index if it doesn't exist
    if index_name not in pc_non_grpc.list_indexes().names():
        print(f"Creating index {index_name}...")
        pc_non_grpc.create_index(
            name=index_name,
            dimension=768,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
        while not pc_non_grpc.describe_index(index_name).status['ready']:
            time.sleep(1)
    
    # Store documents in Pinecone
    docsearch = PineconeVectorStore.from_documents(
        documents=documents,
        embedding=embeddings,
        index_name=index_name
    )
    print(f'Successfully added {len(documents)} documents to {index_name}')
    return docsearch

def enrich_metadata(json_entry: str, chunk_id: str) -> dict:
    return {
        "title": json_entry['title'],
        "source": json_entry['arxiv_pdf'],
        "chunk_id": chunk_id,
        "github": json_entry['github_page'],
        "project": json_entry['project_page'],
        "arxiv": json_entry['arxiv_page'],
    }