import os
from pathlib import Path

from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain

load_dotenv()

# Project Paths

BASE_DIR = Path(__file__).resolve().parent          # Backend/
PROJECT_ROOT = BASE_DIR.parent                      # D:/rag/

PDF_PATH = PROJECT_ROOT / "data" / "ml.pdf"
CHROMA_DB = PROJECT_ROOT / "chroma_db"


class RAGSystem:

    def __init__(self):

       
        print("Initializing RAG System...")
       

        print(f"Project Root : {PROJECT_ROOT}")
        print(f"PDF Path     : {PDF_PATH}")
        print(f"Chroma Path  : {CHROMA_DB}")

        if not PDF_PATH.exists():
            raise FileNotFoundError(
                f"\nPDF not found!\nExpected:\n{PDF_PATH}"
            )

        print("PDF Found ✅")

        # Embedding Model

        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        print("Embedding Model Loaded ✅")

        # Vector Store

        self.vector_store = self.load_or_create_vectorstore()

        print("Vector Store Ready ✅")

        # Retriever

        self.retriever = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5}
        )

        # LLM

        self.llm = ChatGroq(
            model_name="llama-3.3-70b-versatile",
            api_key=os.getenv("GROQ_API_KEY")
        )

        print("Groq Connected ✅")

        # Prompt
        
        self.prompt = self.create_prompt()

        # Document Chain

        self.document_chain = create_stuff_documents_chain(
            self.llm,
            self.prompt
        )

        # Retrieval Chain

        self.chain = create_retrieval_chain(
            self.retriever,
            self.document_chain
        )

        print("=" * 60)
        print("RAG SYSTEM READY 🚀")
        print("=" * 60)


    def load_or_create_vectorstore(self):

        if CHROMA_DB.exists() and any(CHROMA_DB.iterdir()):

            print("Loading Existing ChromaDB...")

            return Chroma(
                persist_directory=str(CHROMA_DB),
                embedding_function=self.embeddings
            )

        print("Creating New ChromaDB...")

        loader = PyPDFLoader(str(PDF_PATH))

        documents = loader.load()

        print(f"Loaded {len(documents)} pages")

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        docs = splitter.split_documents(documents)

        print(f"Created {len(docs)} chunks")

        vector_store = Chroma.from_documents(
            documents=docs,
            embedding=self.embeddings,
            persist_directory=str(CHROMA_DB)
        )

        print("ChromaDB Created Successfully ✅")

        return vector_store


    def create_prompt(self):

        return ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are a friendly and knowledgeable Machine Learning Tutor Bot.

Answer ONLY using the retrieved context.

Instructions:

- Explain in simple language.
- Give definition.
- Give intuition.
- Give an example whenever possible.
- Never hallucinate.
- If answer is unavailable, reply:

"I could not find enough information in the provided study material."

Context:
{context}
"""
                ),
                ("human", "{input}")
            ]
        )


    def ask(self, question: str):

        response = self.chain.invoke(
            {
                "input": question
            }
        )

        return response["answer"]



rag = RAGSystem()