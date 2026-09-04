# Experiment 3 — Retrieval-Augmented Generation (RAG)

## Retrieval-Augmented Generation using FAISS Vector Database, HuggingFace Embeddings, and Llama 3.2

---

## 1. Aim

To implement a Retrieval-Augmented Generation (RAG) system that retrieves relevant information from a PDF document using semantic search and a FAISS vector database, and then uses a local Llama 3.2 Large Language Model to generate an answer based only on the retrieved information.

---

## 2. Objective

The main objectives of this experiment are:

- Load and process a PDF document.
- Split the document into smaller text chunks.
- Convert text chunks into numerical vector embeddings.
- Store embeddings in a FAISS vector database.
- Accept a question from the user.
- Retrieve the most relevant chunks from the PDF.
- Provide the retrieved information as context to an LLM.
- Generate an answer using the local Llama 3.2 model.
- Prevent the model from using outside knowledge.
- Measure retrieval and LLM generation performance.

---

## 3. What is RAG?

**Retrieval-Augmented Generation (RAG)** is a technique that combines:

1. Information Retrieval
2. Large Language Models (LLMs)

Instead of asking an LLM to answer a question only from its pre-trained knowledge, RAG first searches an external knowledge source and provides the relevant information to the LLM.

### Traditional LLM

```text
User Question
      |
      v
     LLM
      |
      v
    Answer
```

The LLM generates the answer using information learned during model training.

---

### RAG

```text
                   +----------------+
                   |   PDF Document |
                   +-------+--------+
                           |
                           v
                  +------------------+
                  |  Text Chunking   |
                  +--------+---------+
                           |
                           v
                  +------------------+
                  |    Embeddings    |
                  +--------+---------+
                           |
                           v
                  +------------------+
                  | FAISS Vector DB  |
                  +--------+---------+
                           |
                           |
User Question -------------+
                           |
                           v
                  +------------------+
                  | Semantic Search  |
                  +--------+---------+
                           |
                           v
                  +------------------+
                  | Relevant Context |
                  +--------+---------+
                           |
                           v
                  +------------------+
                  |   Llama 3.2 LLM  |
                  +--------+---------+
                           |
                           v
                       Answer
```

The important idea is:

> **Retrieve relevant information first, then generate an answer using that information.**

---

# 4. Technologies Used

This experiment uses:

- Python
- LangChain
- LangChain Community
- PyPDF
- HuggingFace Embeddings
- Sentence Transformers
- FAISS
- Ollama
- Llama 3.2
- LangChain Ollama integration

---

# 5. Prerequisites

## 5.1 Python

Python 3.10 or newer is recommended.

Check the installed Python version:

```powershell
python --version
```

Example:

```text
Python 3.12.10
```

---

# 6. Install Required Python Packages

The packages used during the development of this experiment include:

```powershell
python -m pip install langchain
python -m pip install langchain-community
python -m pip install langchain-google-genai
python -m pip install langchain-text-splitters
python -m pip install langchain-huggingface
python -m pip install sentence-transformers
python -m pip install chromadb
python -m pip install pypdf
python -m pip install python-dotenv
```

However, the current Experiment 3 implementation specifically uses **FAISS and Ollama**, so install these additional packages:

```powershell
python -m pip install faiss-cpu
python -m pip install langchain-ollama
```

### Recommended complete installation command

You can install everything with one command:

```powershell
python -m pip install langchain langchain-community langchain-google-genai langchain-text-splitters langchain-huggingface sentence-transformers chromadb pypdf python-dotenv faiss-cpu langchain-ollama
```

---

# 7. Check Installed Packages

To check whether the required packages are installed:

```powershell
python -m pip show langchain langchain-community langchain-google-genai langchain-text-splitters langchain-huggingface sentence-transformers chromadb pypdf python-dotenv faiss-cpu langchain-ollama
```

If a package is installed, information such as the following will be displayed:

```text
Name: langchain
Version: ...
Location: ...
```

If a package is not installed, install it using:

```powershell
python -m pip install package-name
```

---

# 8. Ollama Setup

This experiment uses a **local Llama 3.2 model through Ollama**.

Ollama must be installed separately from Python packages.

After installing Ollama, verify that it is available:

```powershell
ollama --version
```

Then download the Llama 3.2 model:

```powershell
ollama pull llama3.2
```

Check the installed models:

```powershell
ollama list
```

You should see something similar to:

```text
NAME        ID              SIZE
llama3.2     ...             ...
```

The Python program uses:

```python
llm = ChatOllama(
    model="llama3.2",
    temperature=0
)
```

Therefore, the model name must match the model installed in Ollama.

---

# 9. Project Structure

The recommended project structure is:

```text
rag_lab/
│
├── main.py
├── README.md
├── .gitignore
└── sample.pdf
```

### Files

| File | Purpose |
|---|---|
| `main.py` | Main RAG implementation |
| `README.md` | Experiment documentation |
| `.gitignore` | Prevents unnecessary/local files from being committed |
| `sample.pdf` | PDF used as the knowledge source |

---

# 10. What Should `sample.pdf` Contain?

The `sample.pdf` file is the **knowledge source** for the RAG system.

The program does not require a specific PDF format.

You can use a PDF containing meaningful text, such as:

- Internship description
- Job description
- College syllabus
- Research paper
- Technical documentation
- Company information
- Course notes
- Project documentation
- Product documentation
- Public reports
- A textbook chapter
- A public-domain document

### Recommended PDF for this experiment

For demonstrating the question:

```text
What are the responsibilities of the AI Engineering intern?
```

a good `sample.pdf` would be an **AI Engineering internship/job description** containing information such as:

```text
AI Engineering Intern

Responsibilities:

1. Assist in developing AI and machine learning applications.
2. Work with Large Language Models.
3. Build and test RAG pipelines.
4. Prepare and process datasets.
5. Develop Python-based AI applications.
6. Experiment with embeddings and vector databases.
7. Evaluate AI model performance.
8. Collaborate with engineering teams.
```

Then the user can ask:

```text
What are the responsibilities of the AI Engineering intern?
```

The RAG system should retrieve the relevant sections from the PDF and provide them to Llama 3.2.

---

# 11. Important Note About `sample.pdf`

The PDF should contain the information you want the system to answer questions about.

For example, if your PDF contains information about:

```text
Artificial Intelligence
Machine Learning
RAG
Vector Databases
Internship Responsibilities
```

you can ask questions related to those topics.

If you ask:

```text
What are the responsibilities of the AI Engineering intern?
```

the answer should be based on the PDF.

If the PDF does not contain the answer, the program is instructed to return:

```text
I could not find the answer in the provided PDF.
```

---

# 12. How the RAG System Works

The implementation consists of several steps.

## Step 1 — Load the PDF

The program uses:

```python
from langchain_community.document_loaders import PyPDFLoader
```

Then:

```python
loader = PyPDFLoader("sample.pdf")
documents = loader.load()
```

This loads the PDF and converts its pages into LangChain documents.

The program displays:

```text
PDF loaded successfully!
Number of pages: ...
```

---

# 13. Step 2 — Split the PDF into Chunks

Large documents should not be sent directly to the LLM.

The document is divided into smaller pieces called **chunks**.

The program uses:

```python
RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
```

### Chunk size

```text
chunk_size = 500
```

This means each chunk contains approximately 500 characters.

### Chunk overlap

```text
chunk_overlap = 50
```

This allows neighboring chunks to share some content.

For example:

```text
Chunk 1:
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

Chunk 2:
                    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
```

The overlap helps preserve context when important information is near a chunk boundary.

---

# 14. Step 3 — Create Embeddings

The system uses:

```python
HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
```

An embedding converts text into a numerical vector.

For example:

```text
"Python is a programming language"
                 |
                 v
        [0.21, -0.43, 0.67, ...]
```

Similar pieces of text produce vectors that are close to each other in vector space.

This allows the system to perform **semantic search**.

---

# 15. Step 4 — Create the FAISS Vector Database

FAISS is used to efficiently search through vectors.

The program creates the vector store using:

```python
vectorstore = FAISS.from_documents(
    chunks,
    embedding_model
)
```

The process is:

```text
PDF Chunks
    |
    v
Embeddings
    |
    v
FAISS Vector Database
```

FAISS allows the program to find the chunks that are most similar to the user's question.

---

# 16. Step 5 — User Query

The program asks the user for a question:

```python
query = input(
    "\nEnter your question about the PDF: "
)
```

For example:

```text
Enter your question about the PDF:
What are the responsibilities of the AI Engineering intern?
```

This makes the experiment interactive.

---

# 17. Step 6 — Semantic Search

The query is searched against the FAISS vector database:

```python
context = vectorstore.similarity_search(
    query,
    k=5
)
```

The value:

```text
k=5
```

means that the system retrieves the **top 5 most relevant chunks**.

The process is:

```text
User Question
      |
      v
Convert Query to Embedding
      |
      v
Search FAISS
      |
      v
Find Similar Chunks
      |
      v
Top 5 Relevant Chunks
```

---

# 18. Step 7 — Create Context

The retrieved chunks are combined:

```python
context_text = "\n\n".join(
    doc.page_content for doc in context
)
```

This creates the context that will be passed to the LLM.

---

# 19. Step 8 — Connect to Llama 3.2

The experiment uses a local Llama 3.2 model through Ollama:

```python
llm = ChatOllama(
    model="llama3.2",
    temperature=0
)
```

### Why temperature is 0

A temperature of:

```text
0
```

makes the response more deterministic.

This is useful for document-based question answering because we want the model to focus on the provided context instead of generating creative or unrelated information.

---

# 20. Step 9 — RAG Prompt

The retrieved context is inserted into a prompt:

```python
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
```

This is an important part of the RAG system.

The model receives:

```text
Retrieved Context
       +
User Question
       |
       v
    Llama 3.2
       |
       v
    Final Answer
```

---

# 21. Step 10 — Generate the Answer

The model is called using:

```python
response = llm.invoke(prompt)
```

The final answer is displayed using:

```python
print(response.content)
```

---

# 22. Step 11 — Benchmarking

The experiment also measures performance.

The program measures:

### Retrieval Time

Time required to search the FAISS vector database:

```text
Retrieval Time: 0.0123 seconds
```

### LLM Generation Time

Time required by Llama 3.2 to generate the answer:

```text
LLM Generation Time: 2.5432 seconds
```

### Total Processing Time

The total time is:

```text
Total Processing Time:
Retrieval Time + LLM Generation Time
```

Example:

```text
========================================
BENCHMARK RESULTS
========================================
Number of PDF pages: 4
Number of chunks: 12
Number of retrieved chunks: 5

Retrieval Time: 0.0123 seconds
LLM Generation Time: 2.5432 seconds
Total Processing Time: 2.5555 seconds
```

---

# 23. Complete RAG Pipeline

The complete process can be represented as:

```text
                  SAMPLE.PDF
                      |
                      v
                PDF Loader
                      |
                      v
              Text Extraction
                      |
                      v
                Text Chunking
                      |
                      v
                 Embeddings
                      |
                      v
              FAISS Vector DB
                      |
                      |
               User Question
                      |
                      v
             Semantic Search
                      |
                      v
            Top 5 Relevant Chunks
                      |
                      v
              Retrieved Context
                      |
                      v
               RAG Prompt
                      |
                      v
                Llama 3.2
                      |
                      v
                Final Answer
                      |
                      v
                Benchmarking
```

---

# 24. Example Execution

Run the program:

```powershell
python main.py
```

The program will display:

```text
========================================
STEP 1: Loading PDF
========================================

PDF loaded successfully!
Number of pages: 4
```

Then:

```text
========================================
STEP 2: Splitting PDF into Chunks
========================================

Number of chunks: 12
```

Then:

```text
========================================
STEP 4: Creating FAISS Vector Store
========================================

FAISS vector store created successfully!
```

Then:

```text
========================================
STEP 5: User Query
========================================

Enter your question about the PDF:
```

Enter:

```text
What are the responsibilities of the AI Engineering intern?
```

The system retrieves the relevant chunks and sends them to Llama 3.2.

Finally:

```text
========================================
FINAL ANSWER
========================================

The AI Engineering intern is responsible for ...
```

Then:

```text
========================================
BENCHMARK RESULTS
========================================

Number of PDF pages: 4
Number of chunks: 12
Number of retrieved chunks: 5

Retrieval Time: 0.0123 seconds
LLM Generation Time: 2.5432 seconds
Total Processing Time: 2.5555 seconds
```

---

# 25. Example Questions

Depending on the content of your PDF, you can ask:

```text
What are the responsibilities mentioned in the document?
```

```text
What skills are required?
```

```text
What technologies are mentioned?
```

```text
What are the main objectives?
```

```text
Who is the target audience?
```

```text
What projects are described in the document?
```

The question should be related to the information present in `sample.pdf`.

---

# 26. Testing the RAG System

You should test the system with at least two types of questions.

### Test 1 — Information Present in PDF

Ask:

```text
What are the responsibilities of the AI Engineering intern?
```

Expected behavior:

```text
The system retrieves relevant chunks and generates an answer.
```

### Test 2 — Information Not Present in PDF

Ask something unrelated:

```text
Who is the current President of the United States?
```

If this information is not present in your PDF, the expected response is:

```text
I could not find the answer in the provided PDF.
```

This demonstrates that the RAG prompt instructs the LLM not to rely on outside knowledge.

---

# 27. Why FAISS?

FAISS stands for:

**Facebook AI Similarity Search**

It is a library for efficient similarity search over vector embeddings.

In this experiment, FAISS is responsible for:

```text
Storing embeddings
       +
Searching similar embeddings
       +
Returning relevant document chunks
```

---

# 28. Why HuggingFace Embeddings?

The experiment uses:

```text
sentence-transformers/all-MiniLM-L6-v2
```

This model converts text into numerical vectors.

It is lightweight and suitable for local semantic-search experiments.

---

# 29. Why Ollama?

Ollama allows the LLM to run locally.

This experiment uses:

```text
Llama 3.2
```

Advantages include:

- Local execution
- No external LLM API required for generation
- No API key required for Llama generation
- Useful for experimentation with local AI systems

---

# 30. Why RAG Instead of Only Using an LLM?

A normal LLM may not know information contained in a private or newly created document.

RAG allows the system to provide the relevant document information to the LLM.

For example:

```text
Private PDF
     |
     v
Vector Database
     |
     v
Relevant Information
     |
     v
LLM
     |
     v
Answer
```

This makes RAG useful for:

- Company documents
- College notes
- Research papers
- Technical documentation
- Internal knowledge bases
- Manuals
- Reports

---

# 31. `.gitignore`

A `.gitignore` file can be used to prevent unnecessary files from being committed.

Recommended:

```gitignore
__pycache__/
*.py[cod]

venv/
.venv/
env/

.env
.env.*

.vscode/
.idea/

.ipynb_checkpoints/

faiss_index/
vectorstore/
*.faiss
*.pkl

*.log
*.tmp
*.temp

.DS_Store
Thumbs.db
```

If `sample.pdf` contains a private or restricted document, also add:

```gitignore
sample.pdf
```

Do not commit private/company documents to a public GitHub repository unless you have permission to distribute them.

---

# 32. Troubleshooting

## Error: `No module named langchain_ollama`

Install:

```powershell
python -m pip install langchain-ollama
```

---

## Error: `No module named faiss`

Install:

```powershell
python -m pip install faiss-cpu
```

---

## Error: `No module named pypdf`

Install:

```powershell
python -m pip install pypdf
```

---

## Error: `sample.pdf` not found

Make sure the PDF is located in the same directory as `main.py`:

```text
rag_lab/
├── main.py
└── sample.pdf
```

---

## Error: Ollama model not found

Run:

```powershell
ollama pull llama3.2
```

Then check:

```powershell
ollama list
```

---

## Check Ollama

Run:

```powershell
ollama --version
```

---

# 33. Important Difference Between FAISS and Chroma

The package list also contains:

```text
chromadb
```

However, the current implementation uses:

```python
from langchain_community.vectorstores import FAISS
```

Therefore, **ChromaDB is not required by the current `main.py`**.

It was included in the broader LangChain setup you previously used, but this experiment specifically demonstrates:

```text
FAISS Vector Database
```

So the important packages for the current implementation are:

```text
langchain
langchain-community
langchain-text-splitters
langchain-huggingface
sentence-transformers
pypdf
faiss-cpu
langchain-ollama
```

---

# 34. Important Difference Between Google Gemini and Ollama

You previously installed:

```text
langchain-google-genai
```

That package is used for Google Gemini models.

The current experiment does **not** use Gemini.

The current experiment uses:

```text
Ollama
   |
   v
Llama 3.2
```

Therefore, no Google API key is required for this RAG implementation.

---

# 35. Learning Outcomes

After completing this experiment, the learner should understand:

- What Retrieval-Augmented Generation is.
- How PDF documents can be loaded using LangChain.
- Why documents are divided into chunks.
- What embeddings are.
- How semantic search works.
- How FAISS stores and searches vector embeddings.
- How retrieved documents can be provided as context to an LLM.
- How local LLMs can be used with Ollama.
- How RAG reduces dependence on the model's outside knowledge.
- How retrieval and generation performance can be benchmarked.

---

# 36. Conclusion

This experiment demonstrates a complete Retrieval-Augmented Generation pipeline using a local PDF document, HuggingFace embeddings, FAISS vector search, and the Llama 3.2 model running through Ollama.

The system first retrieves relevant information from the PDF and then provides that information to the LLM as context. This allows the LLM to generate answers based on the contents of the document rather than relying only on its pre-trained knowledge.

The experiment also measures retrieval time, LLM generation time, and total processing time to provide basic performance benchmarking.

---

## RAG Architecture Summary

```text
PDF
 |
 v
PyPDFLoader
 |
 v
Document Chunks
 |
 v
HuggingFace Embeddings
 |
 v
FAISS Vector Database
 |
 v
User Query
 |
 v
Similarity Search
 |
 v
Top-K Relevant Chunks
 |
 v
Retrieved Context
 |
 v
Llama 3.2 via Ollama
 |
 v
Final Answer
 |
 v
Performance Benchmark
```

---

## Experiment Information

**Experiment:** 3

**Topic:** Retrieval-Augmented Generation (RAG)

**Vector Database:** FAISS

**Embedding Model:** `sentence-transformers/all-MiniLM-L6-v2`

**LLM:** Llama 3.2

**LLM Runtime:** Ollama

**Framework:** LangChain

**Document Source:** PDF

**Retrieval Method:** Semantic Similarity Search

**Retrieved Documents:** Top 5 chunks