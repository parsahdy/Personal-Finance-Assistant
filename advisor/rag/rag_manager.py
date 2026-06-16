from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings 
from langchain_chroma import Chroma


RAG_DIR = Path(__file__).resolve().parent 
DOCUMENT_DIR = RAG_DIR / "documents" 


def build_vectorstore():
    docs = []

    for pdf_file in DOCUMENT_DIR.glob("*.pdf"):
        loader = PyPDFLoader(str(pdf_file))
        docs.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2",
        encode_kwargs={"normalize_embeddings": True},
    )

    return Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(RAG_DIR / "chroma_db"),
        collection_name="finance_collection"
    )

vector_store = build_vectorstore()

retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)

def retrieve(question):
    return retriever.invoke(question)