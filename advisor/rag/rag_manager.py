from pathlib import Path
from langchain_huggingface import HuggingFaceEmbeddings 
from langchain_chroma import Chroma


RAG_DIR = Path(__file__).resolve().parent 
PERSIST_DIR = RAG_DIR / "chroma_db"


embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2",
        encode_kwargs={"normalize_embeddings": True},
    )

vector_store = Chroma(
    persist_directory=str(PERSIST_DIR),
    embedding_function=embeddings,
    collection_name="finance_collection"
)

retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)

def retrieve(question):
    return retriever.invoke(question)