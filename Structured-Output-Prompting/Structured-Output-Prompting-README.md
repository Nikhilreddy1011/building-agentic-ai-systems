# Experiment 2 — Structured Outputs and Data Handling

This experiment demonstrates how to interact with a local Large Language Model (LLM) using **Ollama and Llama 3.2**, generate responses through prompting, produce structured JSON output, and parse the generated JSON data using Python.

## 📌 Objectives

- Generate basic text responses from a local LLM.
- Use prompting to request structured JSON responses.
- Parse JSON responses returned by the LLM.
- Extract individual values from structured data.

## 🧪 Experiments

### 2.1 — Generating Basic Text Responses using Ollama

A simple prompt is sent to the Llama 3.2 model using Ollama.

**Prompt:**

```text
What is Python?
```

The generated response is retrieved from the Ollama response object and displayed.

**Key concept:**

- Basic LLM prompting
- Ollama chat API
- Handling model responses

---

### 2.2 — Generating Structured JSON Output using Ollama

The LLM is instructed through a prompt to return information in JSON format.

**Prompt:**

```text
Return ONLY valid JSON.

Topic: Python

Include these fields:
- language
- creator
- year
```

The model generates a structured response containing the requested fields.

**Key concept:**

- Prompt-based structured output
- JSON-formatted LLM responses
- Controlling the structure of model output

---

### 2.3 — Parsing and Extracting Data from Structured JSON Responses

The model is instructed to return JSON using Ollama's JSON output format.

The returned JSON text is then parsed using Python's built-in `json` module.

```python
data = json.loads(json_text)
```

Individual values are extracted from the parsed data:

```python
data["language"]
data["creator"]
data["year"]
```

**Key concept:**

- JSON parsing
- Data extraction
- Handling structured LLM responses programmatically

## 🔄 Experiment Workflow

```text
                User Prompt
                     │
                     ▼
              Ollama Chat API
                     │
                     ▼
                Llama 3.2
                     │
          ┌──────────┴──────────┐
          │                     │
      Text Output          JSON Output
          │                     │
          ▼                     ▼
     Display Response      Parse JSON
                                │
                                ▼
                       Extract Individual
                             Values
```

## 🛠️ Technologies Used

- **Python**
- **Ollama**
- **Llama 3.2**
- **JSON**
- **Prompting**

## 📋 Prerequisites

Make sure the following are installed before running the experiments:

- Python
- Ollama
- Llama 3.2 model

Check whether Llama 3.2 is available:

```bash
ollama list
```

If the model is not available, download it using:

```bash
ollama pull llama3.2
```

Install the Python Ollama package:

```bash
pip install ollama
```

## 🚀 How to Run

Clone the repository and navigate to this experiment:

```bash
cd Structured-Output-Prompting
```

Run each experiment separately:

### Experiment 2.1

```bash
python 2.1-basic-text-response.py
```

### Experiment 2.2

```bash
python 2.2-structured-json.py
```

### Experiment 2.3

```bash
python 2.3-json-parsing.py
```

> **Note:** Use the actual filenames in the repository if they differ from the names shown above.

## 📂 Project Structure

```text
Structured-Output-Prompting/
│
├── README.md
│
├── 2.1-basic-text-response.py
├── 2.2-structured-json.py
└── 2.3-json-parsing.py
```

## 📚 Learning Outcomes

After completing this experiment, the following concepts are demonstrated:

1. Interacting with a local LLM using Ollama.
2. Sending prompts to the Llama 3.2 model.
3. Generating basic text responses.
4. Using prompts to request structured JSON output.
5. Parsing JSON responses using Python.
6. Extracting specific fields from structured LLM responses.

## 📝 Summary

This experiment demonstrates the progression from **basic LLM prompting to structured data handling**.

The three stages are:

```text
2.1 → Basic Text Response
       ↓
2.2 → Structured JSON Output
       ↓
2.3 → JSON Parsing & Data Extraction
```

These techniques provide a foundation for using LLMs in applications where model responses need to be processed programmatically.
