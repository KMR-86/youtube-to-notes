# YouTube to Notes AI

A FastAPI application that uses LangChain, LangGraph, and OpenAI to convert YouTube video links into structured, educational notes, with support for saving directly to Google Docs.

## Prerequisites

* **Python:** Version 3.11 or higher (Tested on 3.12.7)
* **API Keys:**
    * OpenAI API Key
    * LangSmith API Key (for tracing)
    * Google Cloud Credentials (for Docs integration)

## Installation

### 1. Clone or Download the repository
Navigate to the project folder in your terminal.

### 2. Set up the Virtual Environment
It is recommended to isolate dependencies using a virtual environment.

```bash
# Create the virtual environment named 'youtube-notes'
python3 -m venv youtube-notes

# Activate the environment:

# On macOS/Linux:
source youtube-notes/bin/activate

# On Windows (Command Prompt):
youtube-notes\Scripts\activate

# On Windows (PowerShell):
youtube-notes\Scripts\Activate.ps1
```

### 3. Install Dependencies
Install all required packages from the requirements file.

```bash
pip install -r requirements.txt
```

## Configuration

1. Create a `.env` file in the root directory:

```bash
touch .env
```

2. Add your API keys to the .env file:

```bash
OPENAI_API_KEY="sk-..."
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT="[https://api.smith.langchain.com](https://api.smith.langchain.com)"
LANGCHAIN_API_KEY="lsv2_..."
LANGCHAIN_PROJECT="youtube-notes-app"
```