import time

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_ollama import ChatOllama


# ============================================================
# Retrieval-Augmented Generation (RAG)
# Vector Database / FAISS with User Query Retrieval
# and Performance Benchmarking
# ============================================================


# ============================================================
# STEP 1: Load the PDF
# ============================================================

print("========================================")
print("STEP 1: Loading PDF")
print("========================================")

loader = PyPDFLoader("sample.pdf")
documents = loader.load()

print("PDF loaded successfully!")
print("Number of pages:", len(documents))


# ============================================================
# STEP 2: Split the PDF into Chunks
# ============================================================

print("\n========================================")
print("STEP 2: Splitting PDF into Chunks")
print("========================================")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = text_splitter.split_documents(documents)

print("Number of chunks:", len(chunks))

if len(chunks) > 0:
    print("\nFirst Chunk:")
    print(chunks[0].page_content)

if len(chunks) > 1:
    print("\nSecond Chunk:")
    print(chunks[1].page_content)


# ============================================================
# STEP 3: Create the Embedding Model
# ============================================================

print("\n========================================")
print("STEP 3: Creating Embedding Model")
print("========================================")

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print("Embedding model loaded successfully!")


# ============================================================
# STEP 4: Create FAISS Vector Store
# ============================================================

print("\n========================================")
print("STEP 4: Creating FAISS Vector Store")
print("========================================")

vectorstore = FAISS.from_documents(
    chunks,
    embedding_model
)

print("FAISS vector store created successfully!")


# ============================================================
# STEP 5: Get User Query
# ============================================================

print("\n========================================")
print("STEP 5: User Query")
print("========================================")

query = input(
    "\nEnter your question about the PDF: "
)

print("\nUser Query:")
print(query)


# ============================================================
# STEP 6: Semantic Search / Retrieval
# ============================================================

print("\n========================================")
print("STEP 6: Semantic Search / Retrieval")
print("========================================")

retrieval_start = time.time()

context = vectorstore.similarity_search(
    query,
    k=5
)

retrieval_time = time.time() - retrieval_start

print("\nTop 5 Relevant Chunks:")

for i, doc in enumerate(context):
    print(f"\n--- Result {i + 1} ---")
    print(doc.page_content)


# ============================================================
# STEP 7: Create Retrieved Context
# ============================================================

print("\n========================================")
print("STEP 7: Creating Retrieved Context")
print("========================================")

context_text = "\n\n".join(
    doc.page_content for doc in context
)

print("\nRetrieved Context:")
print(context_text)


# ============================================================
# STEP 8: Create Local Llama 3.2 Model
# ============================================================

print("\n========================================")
print("STEP 8: Connecting to Llama 3.2")
print("========================================")

llm = ChatOllama(
    model="llama3.2",
    temperature=0
)

print("Local Llama 3.2 model connected successfully!")


# ============================================================
# STEP 9: Create RAG Prompt
# ============================================================

print("\n========================================")
print("STEP 9: Creating RAG Prompt")
print("========================================")

prompt = f"""
You are a helpful assistant.

Answer the question ONLY using the context provided below.

If the answer cannot be found in the context, say:

"I could not find the answer in the provided PDF."

Do not use outside knowledge.

Context:
{context_text}

Question:
{query}

Answer:
"""

print("RAG prompt created successfully!")


# ============================================================
# STEP 10: Generate Answer using Llama
# ============================================================

print("\n========================================")
print("STEP 10: Generating Answer")
print("========================================")

generation_start = time.time()

response = llm.invoke(prompt)

generation_time = time.time() - generation_start


# ============================================================
# STEP 11: Display Final Answer
# ============================================================

print("\n========================================")
print("FINAL ANSWER")
print("========================================")

print(response.content)


# ============================================================
# STEP 12: Benchmarking
# ============================================================

total_time = retrieval_time + generation_time

print("\n========================================")
print("BENCHMARK RESULTS")
print("========================================")

print("Number of PDF pages:", len(documents))
print("Number of chunks:", len(chunks))
print("Number of retrieved chunks:", len(context))

print(f"\nRetrieval Time: {retrieval_time:.4f} seconds")
print(f"LLM Generation Time: {generation_time:.4f} seconds")
print(f"Total Processing Time: {total_time:.4f} seconds")

print("\n========================================")
print("RAG EXPERIMENT COMPLETED")
print("========================================")